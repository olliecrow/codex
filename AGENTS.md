# Repository Guidelines

## Project Structure & Module Organization
- `container/`: Codex CLI container. Primary entrypoint for sandboxed automation.
- `codex_docs.md`: Local copy of Codex docs used by this repo.
- No bundled `prompts/` directory; provide your own prompt files when using automation scripts.

## Build, Test, and Development Commands
- Build Codex image (always fresh): `./container/build.sh`
- Run Codex against a project: `./container/run.sh /path/to/project`
  - Shell instead of TUI: `./container/run.sh /path/to/project --shell`

Sanity checks after run:
- Write works: `echo ok > /workspace/_codex_test.txt`
- Git disabled: `git status` → prints error
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
- Commits: concise, imperative subject (“Add Codex git wrappers”), small scoped diffs.
- PRs: include purpose, key changes, how to build/run, and validation steps. Link issues when applicable. Add screenshots/terminal excerpts for UX changes.

## Security & Configuration Tips
- Host isolation: only mount the project directory and `~/.codex`.
- Git is blocked: not installed, apt‑pinned, and wrapped (`/usr/local/bin/git`). `.git/` is mounted read‑only.
- Codex autonomy: launched with `--dangerously-bypass-approvals-and-sandbox` and `approval_policy=never`.
- Defaults: model `gpt-5.2-codex`, reasoning effort `high`.
- Do not mount extra host secrets (e.g., SSH keys). Avoid expanding writable mounts.

## Agent‑Specific Instructions
- When editing files under `container/`, preserve: non‑root user, git pin + wrappers, two mounts only, and always‑fresh builds.
- Do not add new mounts or relax security without explicit approval.
