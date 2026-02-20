# Docs Directory

This directory holds long-term, agent-focused documentation for this repo. It is not intended for human readers and is committed to git. Repo-wide rules live in `AGENTS.md`; this directory should only add durable, cross-cutting guidance that does not belong in code comments or tests.

## Index
- `docs/decisions.md`: decision capture policy and recorded decisions.
- `docs/skills.md`: shared skill principles, usage rules, and skill conventions.
- `docs/workflows.md`: note routing and workflow conventions for `plan/`.

## Relationship to `/plan/`
- `/plan/` is short-term, disposable scratch space for agents and is not committed.
- `/docs/` is long-lived; only stable guidance should live here.

## Related references
- `codex_docs.md` (repo root) is a raw upstream snapshot and may conflict with repo policy. Prefer refreshing it from upstream rather than hand-editing.
