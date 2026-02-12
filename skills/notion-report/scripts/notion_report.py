#!/usr/bin/env python3
"""
Generate a Notion-importable experiment report from local run artifacts.

Primary output: a single HTML file suitable for Notion import, with images
embedded as data URIs (no external files required).

Optional output: a Notion-importable zip (Markdown + images folder).

Plots are generated as PNG via matplotlib when available; otherwise the script
falls back to SVG plots.
"""

from __future__ import annotations

import argparse
import base64
import csv
import datetime as dt
import html
import io
import json
import math
import os
import re
import shutil
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

try:
    import tomllib  # py>=3.11
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]


DEFAULT_MAX_FILES_SCANNED = 20_000
DEFAULT_MAX_JSONL_RECORDS = 200_000
DEFAULT_MAX_POINTS_PER_SERIES = 2_000
DEFAULT_MAX_METRICS = 8
DEFAULT_MAX_IMAGES_PER_RUN = 12
DEFAULT_MAX_IMAGE_BYTES = 6 * 1024 * 1024
DEFAULT_MAX_CONFIG_BYTES = 512 * 1024
DEFAULT_MAX_CONFIG_KEYS = 12

IGNORE_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
}

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg"}

STEP_KEYS = [
    "_step",
    "step",
    "global_step",
    "timestep",
    "timesteps",
    "iteration",
    "iter",
    "epoch",
    "_runtime",
    "time",
]

SENSITIVE_CONFIG_KEY_TOKENS = (
    "path",
    "dir",
    "file",
    "output",
    "log",
    "logging",
    "checkpoint",
    "ckpt",
    "save",
    "load",
    "resume",
    "artifact",
    "cache",
    "wandb",
    "tensorboard",
    "tb",
    "hostname",
    "host",
    "user",
    "username",
    "machine",
    "node",
    "slurm",
    "job",
)


@dataclass
class CopiedImage:
    src_name: str
    dst: str


@dataclass
class EmbeddedImage:
    label: str
    src_name: str
    mime: str
    data_uri: str


@dataclass
class RunInfo:
    # Public label used in the report/zip. Avoid leaking local dir names.
    name: str
    # Internal: used for IO only. Never include in the report/zip.
    path: str
    source_dir_name: str
    config_path: str | None = None
    config_type: str | None = None
    config_summary: dict[str, str] = field(default_factory=dict)
    overrides: dict[str, str] = field(default_factory=dict)
    metrics_timeseries_path: str | None = None
    metrics_summary_path: str | None = None
    step_key: str | None = None
    n_records: int | None = None
    # metric -> points [(x, y), ...]
    series: dict[str, list[tuple[float, float]]] = field(default_factory=dict)
    # metric -> final value
    finals: dict[str, float] = field(default_factory=dict)
    copied_images: list[CopiedImage] = field(default_factory=list)
    embedded_images: list[EmbeddedImage] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def safe_exc_str(exc: BaseException) -> str:
    # Avoid leaking local paths that may appear in exception stringification.
    if isinstance(exc, OSError):
        parts: list[str] = []
        if getattr(exc, "errno", None) is not None:
            parts.append(f"errno={exc.errno}")
        if getattr(exc, "strerror", None):
            parts.append(str(exc.strerror))
        inner = ", ".join(parts)
        return f"{exc.__class__.__name__}({inner})" if inner else exc.__class__.__name__
    return exc.__class__.__name__


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    text = re.sub(r"-{2,}", "-", text)
    return text or "report"


def sanitize_filename(text: str, *, max_len: int = 80) -> str:
    text = text.strip()
    text = re.sub(r"[^A-Za-z0-9_.-]+", "_", text)
    text = text.strip("._-")
    if not text:
        return "item"
    return text[:max_len]


def try_float(val: Any) -> float | None:
    if isinstance(val, bool):
        return None
    if isinstance(val, (int, float)):
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return None
        return float(val)
    if isinstance(val, str):
        s = val.strip()
        if not s:
            return None
        try:
            f = float(s)
        except ValueError:
            return None
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    return None


def is_sensitive_config_key(key: str) -> bool:
    lower = key.lower()
    return any(tok in lower for tok in SENSITIVE_CONFIG_KEY_TOKENS)


def looks_like_private_path_value(text: str) -> bool:
    s = text.strip()
    if not s:
        return False
    # Avoid false positives on simple fractions.
    if re.match(r"^\\d+/\\d+$", s):
        return False
    if "://" in s:
        return True
    # Treat any path-ish values as private (absolute or relative).
    if s.startswith(("~", "/", "./", "../")):
        return True
    if re.match(r"^[A-Za-z]:[\\\\/]", s):
        return True
    if "/" in s or "\\" in s:
        return True
    # Common macOS/Linux home patterns.
    if "/users/" in s.lower() or "/home/" in s.lower():
        return True
    return False


def flatten_dict(obj: Any, prefix: str = "") -> dict[str, Any]:
    if not isinstance(obj, dict):
        return {}
    out: dict[str, Any] = {}
    for k, v in obj.items():
        key = str(k)
        full = f"{prefix}{key}" if not prefix else f"{prefix}/{key}"
        if isinstance(v, dict):
            out.update(flatten_dict(v, prefix=full))
        else:
            out[full] = v
    return out


def iter_files(root: Path, *, max_files: int) -> Iterable[Path]:
    seen = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIR_NAMES]
        for fname in filenames:
            seen += 1
            if seen > max_files:
                return
            yield Path(dirpath) / fname


def pick_step_key(records: list[dict[str, Any]]) -> str | None:
    for key in STEP_KEYS:
        for rec in records:
            if key in rec and try_float(rec.get(key)) is not None:
                return key
    return None


def downsample(points: list[tuple[float, float]], *, max_points: int) -> list[tuple[float, float]]:
    if len(points) <= max_points:
        return points
    step = len(points) / max_points
    out: list[tuple[float, float]] = []
    for i in range(max_points):
        out.append(points[int(i * step)])
    # Ensure last point is present (helps final-value visibility)
    if out and out[-1] != points[-1]:
        out[-1] = points[-1]
    return out


def read_jsonl(path: Path, *, max_records: int) -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                if idx >= max_records:
                    warnings.append(f"metrics file truncated at {max_records} records: {path.name}")
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(obj, dict):
                    records.append(flatten_dict(obj))
    except OSError as exc:
        warnings.append(f"failed to read metrics jsonl '{path.name}': {safe_exc_str(exc)}")
    return records, warnings


def read_csv(path: Path, *, max_records: int) -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                if idx >= max_records:
                    warnings.append(f"metrics file truncated at {max_records} records: {path.name}")
                    break
                records.append({k: v for k, v in row.items()})
    except OSError as exc:
        warnings.append(f"failed to read metrics csv '{path.name}': {safe_exc_str(exc)}")
    return records, warnings


def series_from_records(
    records: list[dict[str, Any]],
    *,
    step_key: str | None,
    max_points: int,
) -> tuple[dict[str, list[tuple[float, float]]], dict[str, float], str | None, int]:
    if not records:
        return {}, {}, step_key, 0

    resolved_step_key = step_key or pick_step_key(records)
    if resolved_step_key is None:
        resolved_step_key = "__index__"

    series: dict[str, list[tuple[float, float]]] = {}
    finals: dict[str, float] = {}

    for idx, rec in enumerate(records):
        x = try_float(rec.get(resolved_step_key)) if resolved_step_key != "__index__" else float(idx)
        if x is None:
            x = float(idx)
        for key, raw in rec.items():
            if key == resolved_step_key:
                continue
            if isinstance(key, str) and (key.startswith("_") or key.endswith("/_")):
                continue
            y = try_float(raw)
            if y is None:
                continue
            points = series.setdefault(str(key), [])
            points.append((x, y))
            finals[str(key)] = y

    for key, points in list(series.items()):
        if not points:
            series.pop(key, None)
            finals.pop(key, None)
            continue
        series[key] = downsample(points, max_points=max_points)
        finals[key] = series[key][-1][1]

    return series, finals, (resolved_step_key if resolved_step_key != "__index__" else None), len(records)


def discover_metrics_files(run_dir: Path, files: list[Path]) -> tuple[Path | None, Path | None]:
    timeseries: list[Path] = []
    summary: list[Path] = []

    for p in files:
        name = p.name.lower()
        if name.endswith(".jsonl") and ("metrics" in name or "history" in name or "progress" in name):
            timeseries.append(p)
        elif name.endswith(".csv") and ("metrics" in name or "history" in name or "progress" in name):
            timeseries.append(p)
        elif name.endswith(".json") and any(tok in name for tok in ("summary", "results", "eval")):
            summary.append(p)

    def prefer(paths: list[Path], preferred_names: list[str]) -> Path | None:
        if not paths:
            return None
        by_name: dict[str, Path] = {p.name.lower(): p for p in paths}
        for n in preferred_names:
            if n in by_name:
                return by_name[n]
        # Prefer shallower paths, then smaller files.
        return sorted(paths, key=lambda p: (len(p.relative_to(run_dir).parts), p.stat().st_size))[0]

    ts = prefer(timeseries, ["metrics.jsonl", "metrics.csv", "history.csv", "progress.csv"])
    sm = prefer(summary, ["summary.json", "results.json", "eval.json"])
    return ts, sm


def discover_config_file(run_dir: Path, files: list[Path]) -> Path | None:
    candidates: list[Path] = []
    for p in files:
        name = p.name.lower()
        if name in {
            "config.json",
            "args.json",
            "hparams.json",
            "params.json",
            "run_config.json",
            "config.toml",
            "args.toml",
            "params.toml",
        }:
            candidates.append(p)

    def prefer(paths: list[Path], preferred_names: list[str]) -> Path | None:
        if not paths:
            return None
        by_name: dict[str, Path] = {p.name.lower(): p for p in paths}
        for n in preferred_names:
            if n in by_name:
                return by_name[n]
        # Prefer shallower paths, then smaller files.
        return sorted(paths, key=lambda p: (len(p.relative_to(run_dir).parts), p.stat().st_size))[0]

    return prefer(
        candidates,
        ["config.json", "args.json", "hparams.json", "params.json", "config.toml", "args.toml", "params.toml"],
    )


def read_config(path: Path, *, max_bytes: int) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    try:
        size = path.stat().st_size
    except OSError as exc:
        return {}, [f"failed to stat config '{path.name}': {safe_exc_str(exc)}"]
    if size > max_bytes:
        return {}, [f"skipped config >{max_bytes} bytes: {path.name} ({size} bytes)"]

    try:
        raw = path.read_bytes()
    except OSError as exc:
        return {}, [f"failed to read config '{path.name}': {safe_exc_str(exc)}"]

    suffix = path.suffix.lower()
    if suffix == ".json":
        try:
            obj = json.loads(raw.decode("utf-8"))
        except UnicodeDecodeError as exc:
            return {}, [f"failed to decode json config '{path.name}': {safe_exc_str(exc)}"]
        except json.JSONDecodeError as exc:
            return {}, [f"failed to parse json config '{path.name}': {safe_exc_str(exc)}"]
        if not isinstance(obj, dict):
            return {}, [f"json config is not an object/dict: {path.name}"]
        return obj, warnings

    if suffix == ".toml":
        if tomllib is None:
            return {}, ["tomllib not available; cannot parse toml configs"]
        try:
            obj = tomllib.loads(raw.decode("utf-8"))
        except UnicodeDecodeError as exc:
            return {}, [f"failed to decode toml config '{path.name}': {safe_exc_str(exc)}"]
        except Exception as exc:
            return {}, [f"failed to parse toml config '{path.name}': {safe_exc_str(exc)}"]
        if not isinstance(obj, dict):
            return {}, [f"toml config is not a dict: {path.name}"]
        return obj, warnings

    return {}, [f"unsupported config type (expected .json or .toml): {path.name}"]


def config_value_to_str(val: Any) -> str | None:
    if isinstance(val, (str, int, float, bool)) and not isinstance(val, bool):
        # bool is excluded from try_float; keep config values explicit.
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return None
        if isinstance(val, str):
            s = val.strip().replace("\n", " ")
            if looks_like_private_path_value(s):
                return None
            return s if s else None
        if isinstance(val, float):
            return format_float(val)
        return str(val)
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, list) and len(val) <= 10 and all(isinstance(x, (str, int, float, bool)) for x in val):
        parts: list[str] = []
        for x in val:
            s = config_value_to_str(x)
            if s is None:
                continue
            parts.append(s)
        return "[" + ", ".join(parts) + "]" if parts else None
    return None


def score_config_key(name: str) -> float:
    lower = name.lower()
    score = 0.0
    if any(tok in lower for tok in ("seed",)):
        score += 8.0
    if any(tok in lower for tok in ("lr", "learning_rate", "learning-rate")):
        score += 8.0
    if any(tok in lower for tok in ("batch", "microbatch")):
        score += 7.0
    if any(tok in lower for tok in ("env", "task", "suite")):
        score += 6.0
    if any(tok in lower for tok in ("algo", "algorithm", "agent")):
        score += 6.0
    if any(tok in lower for tok in ("model", "policy", "arch", "network", "hidden", "layers")):
        score += 5.0
    if any(tok in lower for tok in ("gamma", "lambda", "clip", "entropy", "vf", "grad", "weight_decay", "optimizer")):
        score += 4.0
    score -= name.count("/") * 0.6
    score -= min(len(lower), 160) * 0.02
    return score


def select_config_keys(
    configs_by_run: list[dict[str, str]],
    *,
    max_keys: int,
) -> list[str]:
    coverage: dict[str, int] = {}
    for cfg in configs_by_run:
        for k in cfg.keys():
            coverage[k] = coverage.get(k, 0) + 1

    ranked = sorted(
        coverage.keys(),
        key=lambda k: (coverage[k], score_config_key(k)),
        reverse=True,
    )
    return ranked[:max_keys]


def select_config_keys_for_overrides(
    configs_by_run: list[dict[str, str]],
    *,
    base_config: dict[str, str],
    max_keys: int,
) -> list[str]:
    all_keys: set[str] = set()
    for cfg in configs_by_run:
        all_keys.update(cfg.keys())
    if not all_keys or max_keys <= 0:
        return []

    diff_counts: dict[str, int] = {}
    for k in all_keys:
        base_v = base_config.get(k)
        diff = 0
        for cfg in configs_by_run:
            v = cfg.get(k)
            if v is None:
                continue
            if base_v is None:
                diff += 1
            elif v != base_v:
                diff += 1
        diff_counts[k] = diff

    ranked = sorted(
        all_keys,
        key=lambda k: (
            1 if diff_counts.get(k, 0) > 0 else 0,
            diff_counts.get(k, 0),
            score_config_key(k),
        ),
        reverse=True,
    )
    return ranked[:max_keys]


def read_summary_json(path: Path) -> tuple[dict[str, float], list[str]]:
    warnings: list[str] = []
    out: dict[str, float] = {}
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return {}, [f"failed to read summary json '{path.name}': {safe_exc_str(exc)}"]
    except json.JSONDecodeError as exc:
        return {}, [f"failed to parse summary json '{path.name}': {safe_exc_str(exc)}"]

    flat = flatten_dict(obj)
    for k, v in flat.items():
        if isinstance(k, str) and k.startswith("_"):
            continue
        f = try_float(v)
        if f is None:
            continue
        out[k] = f

    if not out:
        warnings.append(f"no numeric fields found in summary json: {path.name}")
    return out, warnings


def score_metric(name: str) -> float:
    lower = name.lower()
    if lower.startswith("_"):
        return -100.0
    score = 0.0
    # Prefer eval-ish metrics.
    if any(tok in lower for tok in ("eval", "val", "test")):
        score += 5.0
    if any(tok in lower for tok in ("return", "reward", "success", "accuracy", "acc")):
        score += 5.0
    if any(tok in lower for tok in ("loss", "error")):
        score += 3.0
    if any(tok in lower for tok in ("runtime", "time", "throughput")):
        score -= 3.0
    score -= min(len(lower), 80) * 0.02
    return score


def select_metrics(
    runs: list[RunInfo],
    *,
    explicit: list[str] | None,
    max_metrics: int,
) -> list[str]:
    if explicit:
        return list(dict.fromkeys(explicit))[:max_metrics]

    coverage: dict[str, int] = {}
    for r in runs:
        for m in r.finals.keys():
            coverage[m] = coverage.get(m, 0) + 1

    # Prefer metrics present in more runs, then by heuristic score.
    ranked = sorted(
        coverage.keys(),
        key=lambda m: (coverage[m], score_metric(m)),
        reverse=True,
    )
    return ranked[:max_metrics]


def format_float(val: float | None) -> str:
    if val is None:
        return ""
    # Keep it copy/paste-friendly and stable.
    if abs(val) >= 10_000 or (abs(val) > 0 and abs(val) < 0.001):
        return f"{val:.3e}"
    if abs(val) >= 100:
        return f"{val:.2f}"
    return f"{val:.4f}".rstrip("0").rstrip(".")


def md_cell(text: str, *, max_len: int = 80) -> str:
    s = text.replace("\n", " ").strip()
    s = s.replace("|", "\\|")
    if len(s) > max_len:
        s = s[: max_len - 3] + "..."
    return s


def svg_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def svg_line_plot(
    *,
    series_by_run: list[tuple[str, list[tuple[float, float]]]],
    title: str,
    x_label: str,
    y_label: str,
    out_path: Path,
) -> bool:
    points_all = [pt for _, pts in series_by_run for pt in pts]
    if len(points_all) < 2:
        return False

    x_vals = [x for x, _ in points_all]
    y_vals = [y for _, y in points_all]
    x_min, x_max = min(x_vals), max(x_vals)
    y_min, y_max = min(y_vals), max(y_vals)
    if x_min == x_max:
        x_min -= 1.0
        x_max += 1.0
    if y_min == y_max:
        y_min -= 1.0
        y_max += 1.0

    width, height = 960, 540
    margin_l, margin_r, margin_t, margin_b = 70, 20, 40, 70
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b

    def x_px(x: float) -> float:
        return margin_l + (x - x_min) / (x_max - x_min) * plot_w

    def y_px(y: float) -> float:
        return margin_t + (1.0 - (y - y_min) / (y_max - y_min)) * plot_h

    palette = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]

    def ticks(min_v: float, max_v: float, n: int) -> list[float]:
        if n <= 1:
            return [min_v, max_v]
        step = (max_v - min_v) / (n - 1)
        return [min_v + i * step for i in range(n)]

    x_ticks = ticks(x_min, x_max, 6)
    y_ticks = ticks(y_min, y_max, 6)

    lines: list[str] = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    lines.append('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')
    lines.append(
        f'<text x="{width/2:.1f}" y="26" text-anchor="middle" font-size="16" font-family="Arial">{svg_escape(title)}</text>'
    )

    # Axes
    x0, y0 = margin_l, margin_t + plot_h
    lines.append(f'<line x1="{x0}" y1="{y0}" x2="{x0 + plot_w}" y2="{y0}" stroke="#111" stroke-width="1"/>')
    lines.append(f'<line x1="{x0}" y1="{margin_t}" x2="{x0}" y2="{y0}" stroke="#111" stroke-width="1"/>')

    # Grid + tick labels
    for xv in x_ticks:
        px = x_px(xv)
        lines.append(f'<line x1="{px:.2f}" y1="{margin_t}" x2="{px:.2f}" y2="{y0}" stroke="#eee" stroke-width="1"/>')
        lines.append(
            f'<text x="{px:.2f}" y="{y0 + 18}" text-anchor="middle" font-size="11" font-family="Arial" fill="#333">{svg_escape(format_float(xv))}</text>'
        )
    for yv in y_ticks:
        py = y_px(yv)
        lines.append(f'<line x1="{x0}" y1="{py:.2f}" x2="{x0 + plot_w}" y2="{py:.2f}" stroke="#eee" stroke-width="1"/>')
        lines.append(
            f'<text x="{x0 - 8}" y="{py + 4:.2f}" text-anchor="end" font-size="11" font-family="Arial" fill="#333">{svg_escape(format_float(yv))}</text>'
        )

    # Axis labels
    lines.append(
        f'<text x="{width/2:.1f}" y="{height - 24}" text-anchor="middle" font-size="12" font-family="Arial" fill="#111">{svg_escape(x_label)}</text>'
    )
    # y label rotated
    lines.append(
        f'<text x="18" y="{height/2:.1f}" text-anchor="middle" font-size="12" font-family="Arial" fill="#111" transform="rotate(-90 18 {height/2:.1f})">{svg_escape(y_label)}</text>'
    )

    # Plot lines
    legend_x = margin_l + 8
    legend_y = margin_t + 8
    legend_line_h = 16
    for idx, (run_name, pts) in enumerate(series_by_run):
        if len(pts) < 2:
            continue
        color = palette[idx % len(palette)]
        coords = " ".join(f"{x_px(x):.2f},{y_px(y):.2f}" for x, y in pts)
        lines.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{coords}"/>')
        ly = legend_y + idx * legend_line_h
        lines.append(f'<rect x="{legend_x}" y="{ly - 10}" width="22" height="3" fill="{color}"/>')
        lines.append(
            f'<text x="{legend_x + 28}" y="{ly - 7}" font-size="11" font-family="Arial" fill="#111">{svg_escape(run_name)}</text>'
        )

    lines.append("</svg>")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def svg_bar_chart(
    *,
    values_by_run: list[tuple[str, float]],
    title: str,
    y_label: str,
    out_path: Path,
) -> bool:
    if not values_by_run:
        return False

    vals = [v for _, v in values_by_run]
    y_min, y_max = min(vals), max(vals)
    if y_min == y_max:
        y_min -= 1.0
        y_max += 1.0

    width, height = 960, 540
    margin_l, margin_r, margin_t, margin_b = 70, 20, 40, 140
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b

    def y_px(y: float) -> float:
        return margin_t + (1.0 - (y - y_min) / (y_max - y_min)) * plot_h

    n = len(values_by_run)
    bar_w = plot_w / max(n, 1)

    lines: list[str] = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    lines.append('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')
    lines.append(
        f'<text x="{width/2:.1f}" y="26" text-anchor="middle" font-size="16" font-family="Arial">{svg_escape(title)}</text>'
    )

    x0, y0 = margin_l, margin_t + plot_h
    lines.append(f'<line x1="{x0}" y1="{y0}" x2="{x0 + plot_w}" y2="{y0}" stroke="#111" stroke-width="1"/>')
    lines.append(f'<line x1="{x0}" y1="{margin_t}" x2="{x0}" y2="{y0}" stroke="#111" stroke-width="1"/>')

    # y ticks
    for i in range(6):
        frac = i / 5
        yv = y_min + frac * (y_max - y_min)
        py = y_px(yv)
        lines.append(f'<line x1="{x0}" y1="{py:.2f}" x2="{x0 + plot_w}" y2="{py:.2f}" stroke="#eee" stroke-width="1"/>')
        lines.append(
            f'<text x="{x0 - 8}" y="{py + 4:.2f}" text-anchor="end" font-size="11" font-family="Arial" fill="#333">{svg_escape(format_float(yv))}</text>'
        )

    lines.append(
        f'<text x="18" y="{height/2:.1f}" text-anchor="middle" font-size="12" font-family="Arial" fill="#111" transform="rotate(-90 18 {height/2:.1f})">{svg_escape(y_label)}</text>'
    )

    palette = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]

    for idx, (run_name, val) in enumerate(values_by_run):
        x_left = margin_l + idx * bar_w + bar_w * 0.15
        x_right = margin_l + (idx + 1) * bar_w - bar_w * 0.15
        bar_width = max(1.0, x_right - x_left)
        y_top = y_px(val)
        bar_height = max(0.0, y0 - y_top)
        color = palette[idx % len(palette)]
        lines.append(
            f'<rect x="{x_left:.2f}" y="{y_top:.2f}" width="{bar_width:.2f}" height="{bar_height:.2f}" fill="{color}" opacity="0.9"/>'
        )
        # value label
        lines.append(
            f'<text x="{(x_left + bar_width/2):.2f}" y="{y_top - 6:.2f}" text-anchor="middle" font-size="11" font-family="Arial" fill="#111">{svg_escape(format_float(val))}</text>'
        )
        # run label (rotated)
        label_x = x_left + bar_width / 2
        label_y = y0 + 10
        lines.append(
            f'<text x="{label_x:.2f}" y="{label_y:.2f}" text-anchor="start" font-size="11" font-family="Arial" fill="#111" transform="rotate(60 {label_x:.2f} {label_y:.2f})">{svg_escape(run_name)}</text>'
        )

    lines.append("</svg>")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


_MPL_AVAILABLE: bool | None = None
_MPL_PLT: Any | None = None


def get_mpl_pyplot():
    global _MPL_AVAILABLE, _MPL_PLT
    if _MPL_AVAILABLE is False:
        return None
    if _MPL_PLT is not None:
        return _MPL_PLT
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt  # type: ignore[import-not-found]
    except Exception:
        _MPL_AVAILABLE = False
        return None
    _MPL_AVAILABLE = True
    _MPL_PLT = plt
    return plt


def mpl_line_overlay_png(
    *,
    series_by_run: list[tuple[str, list[tuple[float, float]]]],
    title: str,
    x_label: str,
    y_label: str,
) -> bytes | None:
    plt = get_mpl_pyplot()
    if plt is None:
        return None

    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=120)
    for run_name, pts in series_by_run:
        if len(pts) < 2:
            continue
        xs = [x for x, _ in pts]
        ys = [y for _, y in pts]
        ax.plot(xs, ys, label=run_name, linewidth=1.6)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(True, alpha=0.25)
    if 1 < len(series_by_run) <= 10:
        ax.legend(loc="best", fontsize="small")

    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    return buf.getvalue()


def mpl_bar_chart_png(
    *,
    values_by_run: list[tuple[str, float]],
    title: str,
    y_label: str,
) -> bytes | None:
    plt = get_mpl_pyplot()
    if plt is None:
        return None
    if not values_by_run:
        return None

    names = [n for n, _ in values_by_run]
    vals = [v for _, v in values_by_run]

    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=120)
    xs = list(range(len(vals)))
    ax.bar(xs, vals, color="#1f77b4", alpha=0.9)
    ax.set_xticks(xs)
    ax.set_xticklabels(names, rotation=45, ha="right")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.grid(True, axis="y", alpha=0.25)

    # Value labels.
    y_min = min(vals)
    y_max = max(vals)
    span = (y_max - y_min) if y_max != y_min else 1.0
    for i, v in enumerate(vals):
        offset = 0.02 * span
        y = v + offset if v >= 0 else v - offset
        va = "bottom" if v >= 0 else "top"
        ax.text(i, y, format_float(v), ha="center", va=va, fontsize=8)

    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    return buf.getvalue()


def make_embedded_overlay_plot(
    *,
    series_by_run: list[tuple[str, list[tuple[float, float]]]],
    title: str,
    x_label: str,
    y_label: str,
    label_base: str,
) -> EmbeddedImage | None:
    png = mpl_line_overlay_png(series_by_run=series_by_run, title=title, x_label=x_label, y_label=y_label)
    if png is not None:
        return embed_image_bytes(label=f"{label_base}.png", mime="image/png", data=png)

    with tempfile.TemporaryDirectory() as td:
        out_path = Path(td) / f"{label_base}.svg"
        ok = svg_line_plot(
            series_by_run=series_by_run,
            title=title,
            x_label=x_label,
            y_label=y_label,
            out_path=out_path,
        )
        if not ok:
            return None
        return embed_image_bytes(label=f"{label_base}.svg", mime="image/svg+xml", data=out_path.read_bytes())


def make_embedded_bar_chart(
    *,
    values_by_run: list[tuple[str, float]],
    title: str,
    y_label: str,
    label_base: str,
) -> EmbeddedImage | None:
    png = mpl_bar_chart_png(values_by_run=values_by_run, title=title, y_label=y_label)
    if png is not None:
        return embed_image_bytes(label=f"{label_base}.png", mime="image/png", data=png)

    with tempfile.TemporaryDirectory() as td:
        out_path = Path(td) / f"{label_base}.svg"
        ok = svg_bar_chart(values_by_run=values_by_run, title=title, y_label=y_label, out_path=out_path)
        if not ok:
            return None
        return embed_image_bytes(label=f"{label_base}.svg", mime="image/svg+xml", data=out_path.read_bytes())


def copy_run_images(
    *,
    run_dir: Path,
    run_label: str,
    files: list[Path],
    images_dir: Path,
    max_images: int,
    max_image_bytes: int,
) -> tuple[list[CopiedImage], list[str]]:
    warnings: list[str] = []
    candidates_sorted = rank_image_candidates(files)
    copied: list[CopiedImage] = []
    for src in candidates_sorted:
        if len(copied) >= max_images:
            break
        ext = src.suffix.lower()
        dst_name = f"{sanitize_filename(run_label)}_image_{(len(copied) + 1):02d}{ext}"
        dst = images_dir / dst_name
        try:
            size = src.stat().st_size
        except OSError as exc:
            warnings.append(f"failed to stat image '{src.name}': {safe_exc_str(exc)}")
            continue
        if size > max_image_bytes:
            warnings.append(f"skipped image >{max_image_bytes} bytes: {src.name} ({size} bytes)")
            continue
        try:
            shutil.copy2(src, dst)
        except OSError as exc:
            warnings.append(f"failed to copy image '{src.name}': {safe_exc_str(exc)}")
            continue
        copied.append(CopiedImage(src_name=src.name, dst=f"images/{dst_name}"))
    if candidates_sorted and not copied:
        warnings.append("found images but copied none (permissions/IO issues)")
    return copied, warnings


def rank_image_candidates(files: list[Path]) -> list[Path]:
    candidates: list[tuple[int, int, Path]] = []
    for p in files:
        if p.suffix.lower() not in IMAGE_EXTS:
            continue
        try:
            size = p.stat().st_size
        except OSError:
            continue
        lower_parts = [part.lower() for part in p.parts]
        # Prefer likely-visual subdirs.
        priority = 0
        if any(tok in lower_parts for tok in ("plots", "figures", "images", "rollouts", "media", "videos")):
            priority -= 2
        candidates.append((priority, size, p))

    return [p for _, _, p in sorted(candidates, key=lambda t: (t[0], -t[1]))]


def image_mime_type(path: Path) -> str | None:
    ext = path.suffix.lower()
    if ext == ".png":
        return "image/png"
    if ext in (".jpg", ".jpeg"):
        return "image/jpeg"
    if ext == ".gif":
        return "image/gif"
    if ext == ".svg":
        return "image/svg+xml"
    return None


def embed_image_bytes(*, label: str, mime: str, data: bytes) -> EmbeddedImage:
    b64 = base64.b64encode(data).decode("ascii")
    return EmbeddedImage(label=label, src_name=label, mime=mime, data_uri=f"data:{mime};base64,{b64}")


def embed_image_file(*, path: Path, label: str, max_bytes: int) -> tuple[EmbeddedImage | None, str | None]:
    try:
        size = path.stat().st_size
    except OSError as exc:
        return None, f"failed to stat image '{path.name}': {safe_exc_str(exc)}"
    if size > max_bytes:
        return None, f"skipped image >{max_bytes} bytes: {path.name} ({size} bytes)"
    mime = image_mime_type(path)
    if mime is None:
        return None, f"unsupported image type for embedding: {path.name}"
    try:
        data = path.read_bytes()
    except OSError as exc:
        return None, f"failed to read image '{path.name}': {safe_exc_str(exc)}"
    return embed_image_bytes(label=label, mime=mime, data=data), None


def embed_run_images(
    *,
    run_label: str,
    files: list[Path],
    max_images: int,
    max_image_bytes: int,
) -> tuple[list[EmbeddedImage], list[str]]:
    warnings: list[str] = []
    candidates_sorted = rank_image_candidates(files)
    embedded: list[EmbeddedImage] = []
    for src in candidates_sorted:
        if len(embedded) >= max_images:
            break
        ext = src.suffix.lower()
        label = f"{sanitize_filename(run_label)}_image_{(len(embedded) + 1):02d}{ext}"
        img, warn = embed_image_file(path=src, label=label, max_bytes=max_image_bytes)
        if warn:
            warnings.append(warn)
            continue
        if img is not None:
            # Preserve original filename only in metadata; do not surface in report unless explicitly added.
            img.src_name = src.name
            embedded.append(img)
    if candidates_sorted and not embedded:
        warnings.append("found images but embedded none (skipped/IO issues)")
    return embedded, warnings


def render_markdown_report(
    *,
    motivation: str | None,
    runs: list[RunInfo],
    base_run_name: str | None,
    base_config: dict[str, str],
    config_keys: list[str],
    selected_metrics: list[str],
    plots: list[tuple[str, str]],
) -> str:
    now = dt.datetime.now(dt.timezone.utc)

    lines: list[str] = []
    # Note: the Notion page title typically comes from the Markdown filename on import.
    # Avoid duplicating the title as an in-page H1.
    lines.append("## Purpose and scope")
    lines.append(f"- motivation: {motivation.strip() if motivation else 'not provided'}")
    lines.append(f"- scope: {len(runs)} run(s) included; this report describes only these runs.")
    if base_run_name and config_keys:
        lines.append(f"- config baseline: {base_run_name}")
    lines.append(f"- report generated (UTC): {now.isoformat(timespec='seconds')}")
    lines.append("")

    lines.append("## What was run (inventory)")
    has_cfg_any = any(r.config_path for r in runs)
    has_cfg_baseline = bool(base_run_name and config_keys)
    overrides_header = "overrides vs baseline" if has_cfg_baseline else "overrides"
    lines.append(f"| run | config | {overrides_header} | records | selected metrics present | visuals | warnings |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for r in runs:
        has_cfg = "yes" if r.config_path else "no"
        overrides = str(len(r.overrides)) if has_cfg_baseline else ""
        records = str(r.n_records) if r.n_records is not None else ""
        present = ""
        if selected_metrics:
            present_n = sum(1 for m in selected_metrics if m in r.finals)
            present = f"{present_n}/{len(selected_metrics)}"
        visuals = str(len(r.copied_images))
        warnings = md_cell("; ".join(r.warnings), max_len=120) if r.warnings else ""
        lines.append(f"| {r.name} | {has_cfg} | {overrides} | {records} | {present} | {visuals} | {warnings} |")
    lines.append("")

    if has_cfg_any:
        lines.append("## Run settings (condensed)")
        lines.append("- configs are parsed from JSON/TOML when present.")
        lines.append("- path-like keys/values are omitted to avoid leaking local filesystem structure.")
        lines.append("")
        if base_run_name and config_keys:
            lines.append("### Baseline config (key subset)")
            lines.append(f"- baseline run: {base_run_name}")
            lines.append("| key | baseline |")
            lines.append("| --- | --- |")
            for k in config_keys:
                v = base_config.get(k, "")
                if not v:
                    continue
                lines.append(f"| `{md_cell(k, max_len=72)}` | `{md_cell(v, max_len=96)}` |")
            lines.append("")

            lines.append("### Overrides by run (vs baseline, shown keys only)")
            for r in runs:
                if not r.config_path:
                    continue
                if not r.overrides:
                    lines.append(f"- {r.name}: no overrides vs baseline for shown keys.")
                    continue
                parts: list[str] = []
                for k in config_keys:
                    if k not in r.overrides:
                        continue
                    parts.append(f"`{md_cell(k, max_len=48)}`=`{md_cell(r.overrides[k], max_len=72)}`")
                if parts:
                    lines.append(f"- {r.name}: " + "; ".join(parts))
            lines.append("")
        else:
            lines.append("- configs were present, but no baseline/overrides were computed.")
            lines.append("")

    if selected_metrics:
        lines.append("## Metrics included")
        for m in selected_metrics:
            lines.append(f"- `{m}`")
        lines.append("")

    lines.append("## Results overview (final values)")
    if not selected_metrics:
        lines.append("- no numeric metrics were extracted from the provided runs.")
        lines.append("")
    else:
        header = ["run"] + selected_metrics
        lines.append("| " + " | ".join(header) + " |")
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")
        for r in runs:
            row = [r.name]
            for m in selected_metrics:
                row.append(format_float(r.finals.get(m)))
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")

    lines.append("## Comparisons (plots)")
    if not plots:
        lines.append("- no plots were generated (no suitable timeseries/final metrics).")
        lines.append("")
    else:
        for caption, rel_path in plots:
            lines.append(f"### {caption}")
            lines.append(f"![]({rel_path})")
            lines.append("")

    lines.append("## Insights and conclusions (objective)")
    if not selected_metrics:
        lines.append("- no numeric metrics were extracted; conclusions are limited to the artifact inventory above.")
        lines.append("")
    else:
        for m in selected_metrics:
            present = [(r.name, r.finals[m]) for r in runs if m in r.finals]
            if len(present) < 2:
                continue
            present_sorted = sorted(present, key=lambda t: t[1])
            min_run, min_val = present_sorted[0]
            max_run, max_val = present_sorted[-1]
            delta = max_val - min_val
            pct = None if min_val == 0 else (delta / abs(min_val)) * 100.0
            pct_str = f", {pct:.2f}%" if pct is not None else ""
            lines.append(
                f"- `{m}`: final values span {format_float(min_val)} ({min_run}) to {format_float(max_val)} ({max_run}); delta {format_float(delta)}{pct_str}."
            )
    lines.append("")

    lines.append("## Per-run visuals")
    any_visuals = any(r.copied_images for r in runs)
    if not any_visuals:
        lines.append("- no run-provided images were copied into this report output.")
        lines.append("")
    else:
        for r in runs:
            if not r.copied_images:
                continue
            lines.append(f"### {r.name}")
            for img in r.copied_images:
                lines.append(f"![]({img.dst})")
            lines.append("")

    lines.append("## Limitations / missing data")
    missing: list[str] = []
    if not motivation:
        missing.append("- motivation was not provided.")
    for r in runs:
        if not r.finals:
            missing.append(f"- {r.name}: no numeric metrics extracted.")
        if has_cfg_any and not r.config_path:
            missing.append(f"- {r.name}: no JSON/TOML config discovered.")
    if missing:
        lines.extend(missing)
    else:
        lines.append("- none identified from extracted artifacts.")
    lines.append("")

    return "\n".join(lines)


def html_escape(text: str) -> str:
    return html.escape(text, quote=True)


def truncate_text(text: str, *, max_len: int) -> str:
    s = text.replace("\n", " ").strip()
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."


def render_html_report(
    *,
    title: str,
    motivation: str | None,
    runs: list[RunInfo],
    base_run_name: str | None,
    base_config: dict[str, str],
    config_keys: list[str],
    selected_metrics: list[str],
    plot_images: list[tuple[str, EmbeddedImage]],
) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    esc = html_escape

    css = (
        "body { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; "
        "line-height: 1.45; color: #111; margin: 0; padding: 0; }\n"
        ".container { max-width: 980px; margin: 0 auto; padding: 32px 28px; }\n"
        "h1,h2,h3 { line-height: 1.2; }\n"
        "h1 { margin-top: 0; }\n"
        "code { background: #f6f8fa; padding: 2px 4px; border-radius: 4px; font-size: 0.95em; }\n"
        "pre code { display: block; padding: 12px 14px; overflow-x: auto; }\n"
        "table { border-collapse: collapse; width: 100%; margin: 12px 0 18px; }\n"
        "th, td { border: 1px solid #e5e7eb; padding: 6px 8px; text-align: left; vertical-align: top; font-size: 0.95em; }\n"
        "th { background: #f9fafb; }\n"
        "img { max-width: 100%; height: auto; display: block; margin: 10px 0 18px; }\n"
        "blockquote { margin: 12px 0; padding: 10px 14px; border-left: 4px solid #e5e7eb; background: #fafafa; }\n"
    )

    lines: list[str] = []
    lines.append("<!doctype html>")
    lines.append("<html>")
    lines.append("<head>")
    lines.append('  <meta charset="utf-8" />')
    lines.append('  <meta name="viewport" content="width=device-width, initial-scale=1" />')
    lines.append(f"  <title>{esc(title)}</title>")
    lines.append(f"  <style>{css}</style>")
    lines.append("</head>")
    lines.append("<body>")
    lines.append('  <div class="container">')
    lines.append(f"  <h1>{esc(title)}</h1>")
    lines.append("<p>This report is an objective summary of the runs included below.</p>")

    lines.append("<ul>")
    lines.append(f"<li>motivation: {esc(motivation.strip()) if motivation else 'not provided'}</li>")
    lines.append(f"<li>scope: {len(runs)} run(s) included; this report describes only these runs.</li>")
    if base_run_name and config_keys:
        lines.append(f"<li>config baseline: <code>{esc(base_run_name)}</code></li>")
    lines.append(f"<li>report generated (UTC): <code>{esc(now.isoformat(timespec='seconds'))}</code></li>")
    lines.append("</ul>")

    lines.append("<h2>What was run (inventory)</h2>")
    has_cfg_any = any(r.config_path for r in runs)
    has_cfg_baseline = bool(base_run_name and config_keys)
    overrides_header = "overrides vs baseline" if has_cfg_baseline else "overrides"

    headers = ["run", "config", overrides_header, "records", "selected metrics present", "visuals", "warnings"]
    lines.append("<table>")
    lines.append("<thead><tr>")
    for h in headers:
        lines.append(f"<th>{esc(h)}</th>")
    lines.append("</tr></thead>")
    lines.append("<tbody>")
    for r in runs:
        has_cfg = "yes" if r.config_path else "no"
        overrides = str(len(r.overrides)) if has_cfg_baseline else ""
        records = str(r.n_records) if r.n_records is not None else ""
        present = ""
        if selected_metrics:
            present_n = sum(1 for m in selected_metrics if m in r.finals)
            present = f"{present_n}/{len(selected_metrics)}"
        visuals = str(len(r.embedded_images))
        warn = truncate_text("; ".join(r.warnings), max_len=160) if r.warnings else ""
        lines.append("<tr>")
        lines.append(f"<td><code>{esc(r.name)}</code></td>")
        lines.append(f"<td>{esc(has_cfg)}</td>")
        lines.append(f"<td>{esc(overrides)}</td>")
        lines.append(f"<td>{esc(records)}</td>")
        lines.append(f"<td>{esc(present)}</td>")
        lines.append(f"<td>{esc(visuals)}</td>")
        lines.append(f"<td>{esc(warn)}</td>")
        lines.append("</tr>")
    lines.append("</tbody>")
    lines.append("</table>")

    if has_cfg_any:
        lines.append("<h2>Run settings (condensed)</h2>")
        lines.append("<ul>")
        lines.append("<li>configs are parsed from JSON/TOML when present.</li>")
        lines.append("<li>path-like keys/values are omitted to avoid leaking local filesystem structure.</li>")
        lines.append("</ul>")

        if base_run_name and config_keys:
            lines.append("<h3>Baseline config (key subset)</h3>")
            lines.append(f"<p>baseline run: <code>{esc(base_run_name)}</code></p>")
            lines.append("<table>")
            lines.append("<thead><tr><th>key</th><th>baseline</th></tr></thead>")
            lines.append("<tbody>")
            for k in config_keys:
                v = base_config.get(k, "")
                if not v:
                    continue
                lines.append("<tr>")
                lines.append(f"<td><code>{esc(truncate_text(k, max_len=96))}</code></td>")
                lines.append(f"<td><code>{esc(truncate_text(v, max_len=140))}</code></td>")
                lines.append("</tr>")
            lines.append("</tbody></table>")

            lines.append("<h3>Overrides by run (vs baseline, shown keys only)</h3>")
            lines.append("<ul>")
            for r in runs:
                if not r.config_path:
                    continue
                if not r.overrides:
                    lines.append(f"<li><code>{esc(r.name)}</code>: no overrides vs baseline for shown keys.</li>")
                    continue
                parts: list[str] = []
                for k in config_keys:
                    if k not in r.overrides:
                        continue
                    parts.append(f"<code>{esc(truncate_text(k, max_len=64))}</code>=<code>{esc(truncate_text(r.overrides[k], max_len=96))}</code>")
                if parts:
                    lines.append(f"<li><code>{esc(r.name)}</code>: " + "; ".join(parts) + "</li>")
            lines.append("</ul>")
        else:
            lines.append("<p>configs were present, but no baseline/overrides were computed.</p>")

    if selected_metrics:
        lines.append("<h2>Metrics included</h2>")
        lines.append("<ul>")
        for m in selected_metrics:
            lines.append(f"<li><code>{esc(m)}</code></li>")
        lines.append("</ul>")

    lines.append("<h2>Results overview (final values)</h2>")
    if not selected_metrics:
        lines.append("<p>no numeric metrics were extracted from the provided runs.</p>")
    else:
        lines.append("<table>")
        lines.append("<thead><tr>")
        lines.append("<th>run</th>")
        for m in selected_metrics:
            lines.append(f"<th>{esc(m)}</th>")
        lines.append("</tr></thead>")
        lines.append("<tbody>")
        for r in runs:
            lines.append("<tr>")
            lines.append(f"<td><code>{esc(r.name)}</code></td>")
            for m in selected_metrics:
                lines.append(f"<td>{esc(format_float(r.finals.get(m)))}</td>")
            lines.append("</tr>")
        lines.append("</tbody></table>")

    lines.append("<h2>Comparisons (plots)</h2>")
    if not plot_images:
        lines.append("<p>no plots were generated (no suitable timeseries/final metrics).</p>")
    else:
        for caption, img in plot_images:
            lines.append(f"<h3>{esc(caption)}</h3>")
            lines.append(f'<img src="{esc(img.data_uri)}" alt="{esc(img.label)}" />')

    lines.append("<h2>Insights and conclusions (objective)</h2>")
    if not selected_metrics:
        lines.append("<p>no numeric metrics were extracted; conclusions are limited to the artifact inventory above.</p>")
    else:
        items: list[str] = []
        for m in selected_metrics:
            present = [(r.name, r.finals[m]) for r in runs if m in r.finals]
            if len(present) < 2:
                continue
            present_sorted = sorted(present, key=lambda t: t[1])
            min_run, min_val = present_sorted[0]
            max_run, max_val = present_sorted[-1]
            delta = max_val - min_val
            pct = None if min_val == 0 else (delta / abs(min_val)) * 100.0
            pct_str = f", {pct:.2f}%" if pct is not None else ""
            items.append(
                f"<li><code>{esc(m)}</code>: final values span {esc(format_float(min_val))} ({esc(min_run)}) to "
                f"{esc(format_float(max_val))} ({esc(max_run)}); delta {esc(format_float(delta))}{esc(pct_str)}.</li>"
            )
        if items:
            lines.append("<ul>")
            lines.extend(items)
            lines.append("</ul>")
        else:
            lines.append("<p>insufficient metric coverage for cross-run comparisons.</p>")

    lines.append("<h2>Per-run visuals</h2>")
    any_visuals = any(r.embedded_images for r in runs)
    if not any_visuals:
        lines.append("<p>no run-provided images were embedded in this report.</p>")
    else:
        for r in runs:
            if not r.embedded_images:
                continue
            lines.append(f"<h3>{esc(r.name)}</h3>")
            for img in r.embedded_images:
                lines.append(f"<p><code>{esc(img.label)}</code></p>")
                lines.append(f'<img src="{esc(img.data_uri)}" alt="{esc(img.label)}" />')

    lines.append("<h2>Limitations / missing data</h2>")
    missing: list[str] = []
    if not motivation:
        missing.append("motivation was not provided.")
    for r in runs:
        if not r.finals:
            missing.append(f"{r.name}: no numeric metrics extracted.")
        if has_cfg_any and not r.config_path:
            missing.append(f"{r.name}: no JSON/TOML config discovered.")
    if missing:
        lines.append("<ul>")
        for m in missing:
            lines.append(f"<li>{esc(m)}</li>")
        lines.append("</ul>")
    else:
        lines.append("<p>none identified from extracted artifacts.</p>")

    lines.append("  </div>")
    lines.append("</body>")
    lines.append("</html>")
    return "\n".join(lines) + "\n"


def default_out_dir(*, title: str, base: Path) -> Path:
    stamp = dt.datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    slug = slugify(title)[:48]
    return base / "plan" / "artifacts" / "notion-report" / f"{stamp}_{slug}"


def default_out_html(*, title: str, base: Path) -> Path:
    stamp = dt.datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    slug = slugify(title)[:48]
    return base / "plan" / "artifacts" / "notion-report" / f"{stamp}_{slug}.html"


def notion_page_md_filename(title: str) -> str:
    # Notion import uses the Markdown filename as the page title.
    # Keep it readable and filesystem-safe.
    s = title.strip()
    s = s.replace("/", "-").replace("\\", "-")
    s = re.sub(r"[\x00-\x1f]", " ", s)
    s = re.sub(r"[<>:\"|?*]+", "-", s)
    s = re.sub(r"\\s+", " ", s).strip()
    if not s:
        s = "notion-report"
    if len(s) > 100:
        s = s[:100].rstrip()
    return f"{s}.md"


def notion_page_html_filename(title: str) -> str:
    # Keep it readable and filesystem-safe.
    s = title.strip()
    s = s.replace("/", "-").replace("\\", "-")
    s = re.sub(r"[\x00-\x1f]", " ", s)
    s = re.sub(r"[<>:\"|?*]+", "-", s)
    s = re.sub(r"\\s+", " ", s).strip()
    if not s:
        s = "notion-report"
    if len(s) > 100:
        s = s[:100].rstrip()
    return f"{s}.html"


def write_notion_import_zip(*, out_dir: Path, title: str, out_zip: Path | None) -> Path:
    report_md = out_dir / "report.md"
    images_dir = out_dir / "images"
    if not report_md.exists():
        raise FileNotFoundError(f"missing report.md in {out_dir}")
    if not images_dir.exists():
        raise FileNotFoundError(f"missing images/ in {out_dir}")

    zip_path = out_zip.resolve() if out_zip else (out_dir.parent / f"{out_dir.name}.zip").resolve()
    page_name = notion_page_md_filename(title)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(report_md, arcname=page_name)
        for img in sorted(images_dir.iterdir()):
            if not img.is_file():
                continue
            zf.write(img, arcname=f"images/{img.name}")

    return zip_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a Notion-ready report from run artifacts.")
    p.add_argument("--title", required=True, help="Report title")
    p.add_argument("--motivation", help="1-2 sentence motivation for why these runs were executed")
    p.add_argument(
        "--format",
        choices=["html", "zip", "dir"],
        default="html",
        help="Output format (default: html). 'html' writes a single Notion-importable HTML file with embedded images. "
        "'zip' writes a Notion-importable zip (Markdown + images). 'dir' writes the Markdown + images directory only.",
    )
    p.add_argument("--run", action="append", default=[], help="Run directory to include (repeatable)")
    p.add_argument("--out-html", help="Output HTML path (default: plan/artifacts/notion-report/<timestamp>_<slug>.html)")
    p.add_argument("--out-dir", help="Output directory (default: plan/artifacts/notion-report/<timestamp>_<slug>)")
    p.add_argument("--out-zip", help="Output zip path (default: <out-dir>.zip)")
    p.add_argument(
        "--no-zip",
        action="store_true",
        help="DEPRECATED: Do not create a Notion import zip (equivalent to --format dir).",
    )
    p.add_argument("--metric", action="append", default=[], help="Metric name to include/plot (repeatable)")
    p.add_argument("--max-metrics", type=int, default=DEFAULT_MAX_METRICS)
    p.add_argument("--max-config-keys", type=int, default=DEFAULT_MAX_CONFIG_KEYS)
    p.add_argument("--max-config-bytes", type=int, default=DEFAULT_MAX_CONFIG_BYTES)
    p.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES_SCANNED)
    p.add_argument("--max-jsonl-records", type=int, default=DEFAULT_MAX_JSONL_RECORDS)
    p.add_argument("--max-points", type=int, default=DEFAULT_MAX_POINTS_PER_SERIES)
    p.add_argument("--max-images-per-run", type=int, default=DEFAULT_MAX_IMAGES_PER_RUN)
    p.add_argument("--max-image-bytes", type=int, default=DEFAULT_MAX_IMAGE_BYTES)
    p.add_argument("--no-copy-images", action="store_true", help="Do not include run-provided images in the report output")
    p.add_argument(
        "--base-run",
        help="Baseline run for config overrides (1-based index or source dir name). Defaults to the first run with a config.",
    )
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    if not args.run:
        eprint("[ERROR] At least one --run path is required.")
        return 2

    base = Path.cwd().resolve()
    fmt = str(getattr(args, "format", "html")).strip().lower()
    if args.no_zip:
        if fmt == "html":
            eprint("[ERROR] --no-zip is not compatible with --format html.")
            return 2
        fmt = "dir"

    if fmt not in {"html", "zip", "dir"}:
        eprint(f"[ERROR] Unsupported --format: {fmt}")
        return 2

    out_dir: Path | None = None
    images_dir: Path | None = None
    out_html: Path | None = None

    if fmt == "html":
        if args.out_zip:
            eprint("[ERROR] --out-zip is only valid for --format zip.")
            return 2
        if args.out_html:
            out_html = Path(args.out_html).expanduser().resolve()
            out_html.parent.mkdir(parents=True, exist_ok=True)
        elif args.out_dir:
            out_dir = Path(args.out_dir).expanduser().resolve()
            out_dir.mkdir(parents=True, exist_ok=False)
            out_html = out_dir / notion_page_html_filename(args.title)
        else:
            out_html = default_out_html(title=args.title, base=base).resolve()
            out_html.parent.mkdir(parents=True, exist_ok=True)
        if out_html.exists():
            eprint(f"[ERROR] Output HTML already exists: {out_html.name}")
            return 2
    else:
        if args.out_html:
            eprint("[ERROR] --out-html is only valid for --format html.")
            return 2
        out_dir = Path(args.out_dir).expanduser() if args.out_dir else default_out_dir(title=args.title, base=base)
        out_dir = out_dir.resolve()
        images_dir = out_dir / "images"

        out_dir.mkdir(parents=True, exist_ok=False)
        images_dir.mkdir(parents=True, exist_ok=True)

    runs: list[RunInfo] = []
    configs_by_run: list[dict[str, str]] = []
    for idx, raw in enumerate(args.run, start=1):
        run_dir = Path(raw).expanduser().resolve()
        if not run_dir.exists() or not run_dir.is_dir():
            eprint(f"[ERROR] Run path is not a directory (run #{idx}).")
            return 2

        run_label = f"run_{idx:02d}"
        files = list(iter_files(run_dir, max_files=args.max_files))
        ts_path, sm_path = discover_metrics_files(run_dir, files)
        cfg_path = discover_config_file(run_dir, files)

        info = RunInfo(name=run_label, path=str(run_dir), source_dir_name=run_dir.name)

        # Condensed run settings (optional).
        run_cfg_values: dict[str, str] = {}
        if cfg_path is not None:
            info.config_path = cfg_path.name
            info.config_type = cfg_path.suffix.lower().lstrip(".") or None
            cfg_obj, warns = read_config(cfg_path, max_bytes=int(args.max_config_bytes))
            info.warnings.extend(warns)
            flat_cfg = flatten_dict(cfg_obj)
            for k, v in flat_cfg.items():
                k_str = str(k)
                if is_sensitive_config_key(k_str):
                    continue
                s = config_value_to_str(v)
                if s is None:
                    continue
                run_cfg_values[k_str] = s

        # Timeseries metrics (preferred).
        if ts_path is not None:
            info.metrics_timeseries_path = ts_path.name
            if ts_path.suffix.lower() == ".jsonl":
                records, warns = read_jsonl(ts_path, max_records=args.max_jsonl_records)
            else:
                records, warns = read_csv(ts_path, max_records=args.max_jsonl_records)
            info.warnings.extend(warns)
            series, finals, step_key, n_records = series_from_records(
                records,
                step_key=None,
                max_points=args.max_points,
            )
            info.series = series
            info.finals.update(finals)
            info.step_key = step_key
            info.n_records = n_records
            if not info.finals:
                info.warnings.append(f"no numeric metrics extracted from timeseries: {ts_path.name}")

        # Summary metrics (secondary).
        if sm_path is not None:
            info.metrics_summary_path = sm_path.name
            summary_metrics, warns = read_summary_json(sm_path)
            info.warnings.extend(warns)
            # Only add summary metrics that don't overwrite timeseries finals.
            for k, v in summary_metrics.items():
                if k not in info.finals:
                    info.finals[k] = v

        if args.no_copy_images:
            pass
        else:
            if fmt == "html":
                embedded, warns = embed_run_images(
                    run_label=run_label,
                    files=files,
                    max_images=args.max_images_per_run,
                    max_image_bytes=int(args.max_image_bytes),
                )
                info.embedded_images = embedded
                info.warnings.extend(warns)
            else:
                assert images_dir is not None
                copied, warns = copy_run_images(
                    run_dir=run_dir,
                    run_label=run_label,
                    files=files,
                    images_dir=images_dir,
                    max_images=args.max_images_per_run,
                    max_image_bytes=int(args.max_image_bytes),
                )
                info.copied_images = copied
                info.warnings.extend(warns)

        if ts_path is None and sm_path is None:
            info.warnings.append("no metrics files discovered (expected metrics/history/progress jsonl/csv or summary/results/eval json)")

        runs.append(info)
        configs_by_run.append(run_cfg_values)

    # Baseline config + per-run overrides.
    base_idx: int | None = None
    if args.base_run:
        raw_base = str(args.base_run).strip()
        if raw_base.isdigit():
            candidate = int(raw_base) - 1
            if not (0 <= candidate < len(runs)):
                eprint(f"[ERROR] --base-run index out of range: {args.base_run}")
                return 2
            base_idx = candidate
        else:
            for i, r in enumerate(runs):
                if r.source_dir_name == raw_base:
                    base_idx = i
                    break
            if base_idx is None:
                eprint(f"[ERROR] --base-run did not match any run dir name: {args.base_run}")
                return 2
    else:
        for i, cfg in enumerate(configs_by_run):
            if cfg:
                base_idx = i
                break

    base_cfg: dict[str, str] = configs_by_run[base_idx] if base_idx is not None else {}
    if not base_cfg:
        base_idx = None
        base_cfg = {}

    base_run_name = runs[base_idx].name if base_idx is not None else None
    selected_config_keys = select_config_keys_for_overrides(
        configs_by_run,
        base_config=base_cfg,
        max_keys=max(0, int(args.max_config_keys)),
    )
    base_config = {k: base_cfg.get(k, "") for k in selected_config_keys}

    if selected_config_keys:
        for info, cfg in zip(runs, configs_by_run):
            if not cfg:
                continue
            info.config_summary = {k: cfg[k] for k in selected_config_keys if k in cfg}
            if base_idx is None:
                continue
            overrides: dict[str, str] = {}
            for k in selected_config_keys:
                run_v = cfg.get(k)
                if run_v is None:
                    continue
                base_v = base_cfg.get(k)
                if base_v is None or run_v != base_v:
                    overrides[k] = run_v
            info.overrides = overrides

    selected_metrics = select_metrics(
        runs,
        explicit=args.metric if args.metric else None,
        max_metrics=max(0, int(args.max_metrics)),
    )

    if fmt == "html":
        plot_images: list[tuple[str, EmbeddedImage]] = []
        for metric in selected_metrics:
            series_by_run: list[tuple[str, list[tuple[float, float]]]] = []
            for r in runs:
                pts = r.series.get(metric)
                if pts:
                    series_by_run.append((r.name, pts))
            if series_by_run:
                metric_slug = sanitize_filename(metric)
                img = make_embedded_overlay_plot(
                    series_by_run=series_by_run,
                    title=f"{metric} (overlay)",
                    x_label=runs[0].step_key or "index",
                    y_label=metric,
                    label_base=f"plot_metric_{metric_slug}_overlay",
                )
                if img is not None:
                    plot_images.append((f"{metric} vs step (overlay)", img))

            values = [(r.name, r.finals[metric]) for r in runs if metric in r.finals]
            if values:
                metric_slug = sanitize_filename(metric)
                img = make_embedded_bar_chart(
                    values_by_run=values,
                    title=f"{metric} (final value)",
                    y_label=metric,
                    label_base=f"plot_metric_{metric_slug}_final",
                )
                if img is not None:
                    plot_images.append((f"{metric} final value by run", img))

        assert out_html is not None
        report_html = render_html_report(
            title=args.title,
            motivation=args.motivation,
            runs=runs,
            base_run_name=base_run_name,
            base_config=base_config,
            config_keys=selected_config_keys,
            selected_metrics=selected_metrics,
            plot_images=plot_images,
        )
        out_html.write_text(report_html, encoding="utf-8")
        print(str(out_html))
        return 0

    assert out_dir is not None
    assert images_dir is not None

    plots: list[tuple[str, str]] = []
    for metric in selected_metrics:
        # overlay line plot (requires series points)
        series_by_run: list[tuple[str, list[tuple[float, float]]]] = []
        for r in runs:
            pts = r.series.get(metric)
            if pts:
                series_by_run.append((r.name, pts))
        if series_by_run:
            metric_slug = sanitize_filename(metric)
            overlay_name = f"metric_{metric_slug}_overlay.svg"
            overlay_path = images_dir / overlay_name
            ok = svg_line_plot(
                series_by_run=series_by_run,
                title=f"{metric} (overlay)",
                x_label=runs[0].step_key or "index",
                y_label=metric,
                out_path=overlay_path,
            )
            if ok:
                plots.append((f"{metric} vs step (overlay)", f"images/{overlay_name}"))

        # final-value bar chart (requires finals)
        values = [(r.name, r.finals[metric]) for r in runs if metric in r.finals]
        if values:
            metric_slug = sanitize_filename(metric)
            bar_name = f"metric_{metric_slug}_final.svg"
            bar_path = images_dir / bar_name
            ok = svg_bar_chart(
                values_by_run=values,
                title=f"{metric} (final value)",
                y_label=metric,
                out_path=bar_path,
            )
            if ok:
                plots.append((f"{metric} final value by run", f"images/{bar_name}"))

    report_md = render_markdown_report(
        motivation=args.motivation,
        runs=runs,
        base_run_name=base_run_name,
        base_config=base_config,
        config_keys=selected_config_keys,
        selected_metrics=selected_metrics,
        plots=plots,
    )

    (out_dir / "report.md").write_text(report_md + "\n", encoding="utf-8")

    inventory_runs: list[dict[str, Any]] = []
    for r in runs:
        inventory_runs.append(
            {
                "run": r.name,
                "config_file": r.config_path,
                "config_type": r.config_type,
                "metrics_timeseries_file": r.metrics_timeseries_path,
                "metrics_summary_file": r.metrics_summary_path,
                "n_records": r.n_records,
                "selected_metrics_present": [m for m in selected_metrics if m in r.finals],
                "finals": {m: r.finals.get(m) for m in selected_metrics if m in r.finals},
                "config_baseline": (r.name == base_run_name) if base_run_name else False,
                "config_overrides": r.overrides,
                "warnings": r.warnings,
                "images": [img.dst for img in r.copied_images],
            }
        )

    inventory = {
        "title": args.title,
        "motivation": args.motivation,
        "runs": inventory_runs,
        "selected_config_keys": selected_config_keys,
        "selected_metrics": selected_metrics,
        "plots": [{"caption": c, "path": p} for c, p in plots],
    }
    (out_dir / "inventory.json").write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")

    if fmt == "dir":
        print(str(out_dir))
        return 0

    out_zip = Path(args.out_zip).expanduser() if args.out_zip else None
    zip_path = write_notion_import_zip(out_dir=out_dir, title=args.title, out_zip=out_zip)
    print(str(zip_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
