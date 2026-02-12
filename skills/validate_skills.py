#!/usr/bin/env python3
"""
Validate skills end-to-end.

Runs policy lint plus quick frontmatter validation for each skill.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def repo_root_from_script() -> Path:
    # script: skills/validate_skills.py
    return Path(__file__).resolve().parents[1]


def discover_skill_dirs(skills_root: Path, include_system: bool) -> list[Path]:
    skill_dirs: list[Path] = []
    for child in sorted(skills_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") and not include_system:
            continue
        if (child / "SKILL.md").exists():
            skill_dirs.append(child)
    if include_system:
        for system_skill in sorted(skills_root.glob(".system/*")):
            if system_skill.is_dir() and (system_skill / "SKILL.md").exists():
                if system_skill not in skill_dirs:
                    skill_dirs.append(system_skill)
    return skill_dirs


def normalize_targets(targets: list[str]) -> list[Path]:
    normalized: list[Path] = []
    for raw in targets:
        path = Path(raw).expanduser().resolve()
        if path.is_dir() and (path / "SKILL.md").exists():
            normalized.append(path)
            continue
        if path.is_file() and path.name == "SKILL.md":
            normalized.append(path.parent)
            continue
        raise FileNotFoundError(f"Target must be a skill directory or SKILL.md file: {path}")
    return sorted(set(normalized))


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True)


ALLOWED_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024


def extract_frontmatter(content: str) -> str | None:
    # Keep this intentionally simple and dependency-free so CI can run it without pip installs.
    lines = content.splitlines()
    if not lines:
        return None
    if lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i])
    return None


_TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")
_BLOCK_SCALAR_MARKERS = {"|", ">", "|-", "|+", ">-", ">+"}
_INT_RE = re.compile(r"^[+-]?[0-9]+$")
_FLOAT_RE = re.compile(r"^[+-]?(?:[0-9]+\.[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?$")


def _strip_inline_comment(value: str) -> str:
    # YAML comments start with '#' when not inside quotes.
    in_single = False
    in_double = False
    for i, ch in enumerate(value):
        if ch == "'" and not in_double:
            in_single = not in_single
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            continue
        if ch == "#" and not in_single and not in_double:
            if i == 0 or value[i - 1].isspace():
                return value[:i].rstrip()
    return value.rstrip()


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) < 2:
        return value
    if value[0] == value[-1] and value[0] in {"'", '"'}:
        inner = value[1:-1]
        # Minimal escape handling; keep this conservative (CI should be stable, not clever).
        if value[0] == '"':
            inner = inner.replace('\\"', '"').replace("\\\\", "\\")
        if value[0] == "'":
            inner = inner.replace("''", "'")
        return inner
    return value


def _parse_yaml_scalar(value: str) -> object:
    value = value.strip()
    if value == "":
        return None
    if value[0] in {"'", '"'}:
        return _unquote(value)
    lower = value.lower()
    if lower in {"null", "~"}:
        return None
    if lower == "true":
        return True
    if lower == "false":
        return False
    if _INT_RE.fullmatch(value):
        try:
            return int(value)
        except ValueError:
            return value
    if _FLOAT_RE.fullmatch(value):
        try:
            return float(value)
        except ValueError:
            return value
    return value


def parse_frontmatter_mapping(frontmatter_text: str) -> dict[str, object] | None:
    mapping: dict[str, object] = {}
    lines = frontmatter_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped == "" or stripped.startswith("#"):
            i += 1
            continue
        if line.startswith((" ", "\t")):
            # Nested YAML for keys like metadata; ignored by this top-level parser.
            i += 1
            continue
        match = _TOP_LEVEL_KEY_RE.match(line)
        if not match:
            return None
        key = match.group(1)
        raw_value = match.group(2).lstrip()
        if raw_value in _BLOCK_SCALAR_MARKERS:
            block_lines: list[str] = []
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if next_line.strip() == "":
                    block_lines.append("")
                    i += 1
                    continue
                if not next_line.startswith((" ", "\t")):
                    break
                block_lines.append(next_line.lstrip(" \t"))
                i += 1
            mapping[key] = "\n".join(block_lines)
            continue
        if raw_value == "":
            mapping[key] = None
        else:
            mapping[key] = _parse_yaml_scalar(_strip_inline_comment(raw_value))
        i += 1
    return mapping or None


def validate_skill_dir(skill_dir: Path) -> tuple[bool, str]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    frontmatter_text = extract_frontmatter(content)
    if frontmatter_text is None:
        return False, "Invalid frontmatter format"

    frontmatter = parse_frontmatter_mapping(frontmatter_text)
    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a YAML dictionary"

    unexpected_keys = set(frontmatter.keys()) - ALLOWED_FRONTMATTER_KEYS
    if unexpected_keys:
        allowed = ", ".join(sorted(ALLOWED_FRONTMATTER_KEYS))
        unexpected = ", ".join(sorted(unexpected_keys))
        return (
            False,
            f"Unexpected key(s) in SKILL.md frontmatter: {unexpected}. Allowed properties are: {allowed}",
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return (
                False,
                f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return (
                False,
                f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
            )
        if len(name) > MAX_SKILL_NAME_LENGTH:
            return (
                False,
                f"Name is too long ({len(name)} characters). "
                f"Maximum is {MAX_SKILL_NAME_LENGTH} characters.",
            )

    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > MAX_DESCRIPTION_LENGTH:
            return (
                False,
                f"Description is too long ({len(description)} characters). Maximum is {MAX_DESCRIPTION_LENGTH} characters.",
            )

    return True, "Skill is valid!"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run policy lint and quick validation for skills."
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Optional skill directories or SKILL.md files. Defaults to all versioned skills.",
    )
    parser.add_argument(
        "--include-system",
        action="store_true",
        help="Include skills under skills/.system/*.",
    )
    parser.add_argument(
        "--skip-policy-lint",
        action="store_true",
        help="Skip policy lint and only run quick_validate on targets.",
    )
    args = parser.parse_args()

    repo_root = repo_root_from_script()
    skills_root = repo_root / "skills"
    lint_script = skills_root / "lint_skill_policy.py"

    if args.targets:
        skill_dirs = normalize_targets(args.targets)
    else:
        skill_dirs = discover_skill_dirs(skills_root, args.include_system)

    if not skill_dirs:
        print("No skills found to validate.")
        return 1

    if not args.skip_policy_lint:
        lint_cmd = [sys.executable, str(lint_script)]
        lint_cmd.extend(str(p) for p in skill_dirs)
        lint_result = run(lint_cmd)
        if lint_result.stdout:
            print(lint_result.stdout, end="")
        if lint_result.stderr:
            print(lint_result.stderr, end="", file=sys.stderr)
        if lint_result.returncode != 0:
            return lint_result.returncode

    failures: list[tuple[Path, str]] = []
    for skill_dir in skill_dirs:
        valid, message = validate_skill_dir(skill_dir)
        if not valid:
            failures.append((skill_dir, message))

    if failures:
        print(f"Skill validation failed: {len(failures)} skill(s).")
        for path, message in failures:
            rel = path.relative_to(repo_root)
            print(f"- {rel}: {message}")
        return 1

    print(f"Skill validation passed for {len(skill_dirs)} skill(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
