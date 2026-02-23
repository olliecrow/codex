# Docs Directory

This directory holds long-term, agent-focused documentation for this repo. It is not intended for human readers and is committed to git. Repo-wide rules live in `AGENTS.md`; this directory should only add durable, cross-cutting guidance that does not belong in code comments or tests.

Docs principles (see `AGENTS.md` for full repo policy):
- Keep entries concise, evergreen, and aligned with the codebase.
- Prefer updating existing docs over adding new files unless the content is clearly distinct.
- Reusable skill prompt templates are documented in `prompt-cookbook.md`.

Relationship to `/plan/`:
- `/plan/` is a short-term, disposable scratch space for agents and is not committed to git.
- `/docs/` is long-lived; only stable guidance should live here.

Other docs:
- `codex_docs.md` is a raw upstream snapshot for reference only and may conflict with repo policy. Treat `AGENTS.md` as authoritative.
