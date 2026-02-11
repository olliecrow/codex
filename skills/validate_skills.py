#!/usr/bin/env python3
"""
Validate skills end-to-end.

Runs policy lint plus quick frontmatter validation for each skill.
"""

import argparse
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
    quick_validate = skills_root / ".system" / "skill-creator" / "scripts" / "quick_validate.py"

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
        result = run([sys.executable, str(quick_validate), str(skill_dir)])
        if result.returncode != 0:
            output = (result.stdout + result.stderr).strip() or "quick_validate failed"
            failures.append((skill_dir, output))

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
