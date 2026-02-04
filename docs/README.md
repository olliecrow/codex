# Docs Directory

This directory holds long-term, agent-focused documentation for this repo. It is not intended for human readers and is committed to git. Repo-wide rules live in `AGENTS.md`; this directory should only add durable, cross-cutting guidance that does not belong in code comments or tests.

Docs principles (additive to `AGENTS.md`):
- Keep entries concise and high-signal.
- Prefer updating existing docs over adding new files unless the content is clearly distinct.
- Avoid time- or date-dependent language and keep content aligned with the codebase.

Relationship to `/plan/`:
- `/plan/` is a short-term, disposable scratch space for agents and is not committed to git.
- `/docs/` is long-lived; only stable guidance should live here.
