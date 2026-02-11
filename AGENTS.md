# Codex Repository

This repository hosts the Codex CLI container, agent documentation, and reusable skills that power automation workflows. This file serves as both the project README and the authoritative agent guidelines—keep it up to date without removing the sections below.

## Overview
- Purpose: provide a reproducible Codex container, curated skills, and agent-focused docs for reliable automation.
- Primary entrypoint: `container/` for building and running Codex against other projects.
- Human + agent usage: humans can use this as the README; agents must follow the guidelines in later sections.
- `README.md` and `CLAUDE.md` are symlinks to this file; edit `AGENTS.md` as the source of truth.

## Quick Start
- Build the Codex image (fresh): `./container/build.sh`
- Run Codex against a project: `./container/run.sh /path/to/project`
- Run with a shell: `./container/run.sh /path/to/project --shell`
- After a run, verify sanity checks listed below.

## What Lives Here
- Container and runtime setup in `container/`.
- Long-lived agent docs in `docs/`.
- Short-lived scratch work in `plan/` (do not commit).
- Versioned skills in `skills/` (symlinked into `~/.codex/skills`).
- `README.md` and `CLAUDE.md` are symlinks to `AGENTS.md` to keep guidance in one place.

# Repository Guidelines

## Project Structure & Module Organization
- `container/`: Codex CLI container. Primary entrypoint for sandboxed automation.
- `codex_docs.md`: Local copy of Codex docs used by this repo.
- `docs/`: Long-term, agent-focused documentation. Not for humans. Committed to git.
- `plan/`: Short-term, throwaway scratch space for agents. Not for humans. Do not commit.
- `skills/`: Version-controlled Codex skills. These are symlinked into `~/.codex/skills` so Codex loads them as user skills.
- No bundled `prompts/` directory; provide your own prompt files when using automation scripts.

## Docs, Plans, and Decisions (agent usage)
- `docs/` is long-lived and should stay aligned with the codebase. Keep it lean, evergreen, and high-signal.
- Avoid time- or date-dependent language in `docs/`. Prefer updating existing entries over adding new ones unless clearly distinct.
- `plan/` is short-lived and disposable. Keep it tidy, consolidate notes, and clean up artifacts as you go.
- Decision capture policy lives in `docs/decisions.md`. Record important fixes and decisions in the smallest local place (code, tests, or docs) per that policy.
- Skills should run proactively and autonomously on high-conviction, in-scope actions, complete work end-to-end with verification, and keep `docs/` accurate by promoting durable learnings/decisions from ongoing work.
- For large or long tasks/plans, run recurring milestone checkpoints: use `git-commit` for small logical commits and `organise-docs` to promote durable learnings/decisions into `docs/`.

## Plan Directory Structure (agent usage)
If `/plan/` does not exist, create it with the following subdirectories:
- `/plan/current/`: active planning notes, decisions, and live status for ongoing tasks.
- `/plan/backlog/`: future-task plans waiting to be promoted.
- `/plan/complete/`: archived finished plans.
- `/plan/experiments/`: temporary scripts, proofs of concept, debugging harnesses.
- `/plan/artifacts/`: short-lived outputs (logs, reports, coverage summaries).
- `/plan/scratch/`: quick throwaway notes/files; keep it empty when possible.
- `/plan/handoffs/`: sequential workflow handoffs from `container/run_sequence_*` scripts.

## Skills
- Current skills: `battletest`, `cleanup`, `cluster-check`, `consider`, `create-plan`, `danger-check`, `decisions`, `execute`, `familiarize`, `gh-address-comments`, `gh-fix-ci`, `git-commit`, `git-merge`, `git-review`, `git-summary`, `investigate`, `jupyter-notebook`, `learnings`, `openai-docs`, `organise-docs`, `plan`, `playwright`, `prime`, `review-branch`, `setup`, `summarize`, `tech-debt`, `verify`, `wait-for-job`, `yeet`.
- System skills remain in `~/.codex/skills/.system` and are not versioned in this repo.
- When adding/removing skills here, keep the `~/.codex/skills` symlinks in sync.

## Build, Test, and Development Commands
- Build Codex image (always fresh): `./container/build.sh`
- Run Codex against a project: `./container/run.sh /path/to/project`
  - Shell instead of TUI: `./container/run.sh /path/to/project --shell`

Sanity checks after run:
- Write works: `echo ok > /workspace/_codex_test.txt`
- Git disabled inside the container: `git status` → prints error
- Network available: `curl -I https://example.com`

## Coding Style & Naming Conventions
- Shell: Bash, `set -euo pipefail`, quote variables, 2‑space indent, long‑option flags preferred.
- Scripts: kebab or snake with `.sh` suffix (e.g., `build.sh`, `run.sh`).
- Dockerfiles: non‑root user, minimal deps, explicit versions, tidy caches.
- Keep mounts and environment flags explicit and minimal.

## Testing Guidelines
- No formal unit tests. Validate via the sanity checks above.
- For container changes, verify:
  1) Codex TUI launches; 2) `.git` is read‑only; 3) internet works; 4) writes to `/workspace` persist on host; 5) timezone is detected when possible.

## Commit & Pull Request Guidelines
- Commits: concise, imperative subject (“Add Codex git wrappers”), small scoped diffs, and commit little and often.
- Repo policy: commits and pushes are permitted when working directly in this repo on the host (outside the container).
- Rewriting git history is not allowed (e.g., `git rebase`, `git commit --amend`, `git reset` on commits, `git filter-branch`).
- Force pushes and other destructive git actions (e.g., `git push --force`, `git push --force-with-lease`, `git reset --hard`, `git clean -fdx`) are prohibited.
- PRs: include purpose, key changes, how to build/run, and validation steps. Link issues when applicable. Add screenshots/terminal excerpts for UX changes.

## Security & Configuration Tips
- Host isolation: only mount the project directory and `~/.codex` (with an extra read-only bind for `.git` when present to prevent repo mutations).
- Container git is blocked: not installed, apt-pinned, and wrapped (`/usr/local/bin/git`). `.git/` is mounted read-only.
- This container restriction does not apply to the host repo; normal git use in this repo is allowed.
- Codex autonomy: launched with `--dangerously-bypass-approvals-and-sandbox` and `approval_policy=never`.
- Defaults: model `gpt-5.2-codex`, reasoning effort `xhigh`.
- Do not mount extra host secrets (e.g., SSH keys). Avoid expanding writable mounts.

## Agent‑Specific Instructions
- When editing files under `container/`, preserve: non‑root user, git pin + wrappers, two mounts only, and always‑fresh builds.
- Do not add new mounts or relax security without explicit approval.
