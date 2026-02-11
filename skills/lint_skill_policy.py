#!/usr/bin/env python3
"""
Lint skill policy requirements across SKILL.md files.

Checks for the shared autonomy/looping/checkpoint language that should be
present in versioned skills.
"""

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PATTERNS = [
    (
        "proactive section header",
        r"^## Proactive autonomy and knowledge compounding$",
    ),
    (
        "long-task checkpoint section header",
        r"^## Long-task checkpoint cadence$",
    ),
    (
        "autonomous execution default",
        r"Default to autonomous execution: do not pause for confirmation between normal in-scope steps\.",
    ),
    (
        "strict user-input escalation policy",
        r"Request user input only when absolutely necessary:",
    ),
    (
        "adaptive loop requirement",
        r"Treat iterative execution as the default for non-trivial work; run adaptive loop passes",
    ),
    (
        "explicit loop-to-completion criterion",
        r"(Keep looping until actual completion criteria are met:|completion criteria are met)",
    ),
    (
        "organise-docs checkpoint behavior",
        r"Run `organise-docs` frequently during execution",
    ),
    (
        "git-commit checkpoint behavior",
        r"Create small checkpoint commits frequently with `git-commit`",
    ),
    (
        "merge-only history rule",
        r"Never squash commits; always use merge commits when integrating branches\.",
    ),
]

FORBIDDEN_PATTERNS = [
    (
        "blocking approval gate phrase",
        r"\bafter explicit approval\b",
    ),
    (
        "blocking wait phrase",
        r"\bwait for results before continuing\b",
    ),
    (
        "blocking pause phrase",
        r"\bpause until the user reports back\b",
    ),
    (
        "blocking ask phrase",
        r"\bstop and ask\b",
    ),
    (
        "blocking pause execution phrase",
        r"\bpause execution\b",
    ),
]


def repo_root_from_script() -> Path:
    # script: skills/lint_skill_policy.py
    return Path(__file__).resolve().parents[1]


def discover_skill_files(skills_root: Path, include_system: bool) -> list[Path]:
    skill_files: list[Path] = []
    for child in sorted(skills_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") and not include_system:
            continue
        skill_md = child / "SKILL.md"
        if skill_md.exists():
            skill_files.append(skill_md)
    if include_system:
        for skill_md in sorted(skills_root.glob(".system/*/SKILL.md")):
            if skill_md not in skill_files:
                skill_files.append(skill_md)
    return skill_files


def normalize_targets(targets: list[str]) -> list[Path]:
    normalized: list[Path] = []
    for raw in targets:
        path = Path(raw).expanduser().resolve()
        if path.is_dir():
            skill_md = path / "SKILL.md"
            if not skill_md.exists():
                raise FileNotFoundError(f"SKILL.md not found in directory: {path}")
            normalized.append(skill_md)
            continue
        if path.is_file() and path.name == "SKILL.md":
            normalized.append(path)
            continue
        raise FileNotFoundError(f"Target must be a skill directory or SKILL.md file: {path}")
    return normalized


def lint_skill(skill_md: Path) -> tuple[list[str], list[str]]:
    content = skill_md.read_text(encoding="utf-8")
    missing: list[str] = []
    for label, pattern in REQUIRED_PATTERNS:
        if re.search(pattern, content, re.MULTILINE) is None:
            missing.append(label)
    forbidden: list[str] = []
    for label, pattern in FORBIDDEN_PATTERNS:
        for match in re.finditer(pattern, content, flags=re.IGNORECASE | re.MULTILINE):
            line_no = content.count("\n", 0, match.start()) + 1
            line_text = content.splitlines()[line_no - 1].strip()
            forbidden.append(f"{label} at line {line_no}: {line_text}")
    return missing, forbidden


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lint SKILL.md files for shared autonomy/looping policy requirements."
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Optional skill directories or SKILL.md files. Defaults to repo skills/*.",
    )
    parser.add_argument(
        "--include-system",
        action="store_true",
        help="Include skills under skills/.system/*.",
    )
    args = parser.parse_args()

    repo_root = repo_root_from_script()
    skills_root = repo_root / "skills"

    if args.targets:
        skill_files = normalize_targets(args.targets)
    else:
        skill_files = discover_skill_files(skills_root, args.include_system)

    if not skill_files:
        print("No SKILL.md files found to lint.")
        return 1

    failures: list[tuple[Path, list[str], list[str]]] = []
    for skill_md in skill_files:
        missing, forbidden = lint_skill(skill_md)
        if missing or forbidden:
            failures.append((skill_md, missing, forbidden))

    if failures:
        print(f"Skill policy lint failed: {len(failures)} skill(s) need fixes.")
        for skill_md, missing, forbidden in failures:
            rel = skill_md.relative_to(repo_root)
            print(f"- {rel}")
            for item in missing:
                print(f"  - missing: {item}")
            for item in forbidden:
                print(f"  - forbidden: {item}")
        return 1

    print(f"Skill policy lint passed for {len(skill_files)} skill(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
