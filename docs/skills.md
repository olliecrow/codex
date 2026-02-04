# Skills

This doc summarizes the version-controlled Codex skills that live in this repo and how agents should use them. It is agent-focused and meant to stay evergreen. The canonical skill list lives in `AGENTS.md`.

## What a Skill Is
- A skill is a reusable workflow, defined by a `SKILL.md` file inside `skills/<name>/`.
- Skills may include `scripts/`, `assets/`, or `references/` directories used by the workflow.
- Skills in this repo are symlinked into `~/.codex/skills` so Codex loads them as user skills.

## Shared Principles
- Prefer the smallest set of skills that fully covers the request; state the order if using more than one.
- Treat the `description` in `SKILL.md` as the primary trigger signal.
- Use progressive disclosure: open `SKILL.md` first, then only the referenced files you need.
- Keep context tight: avoid bulk-loading folders, and summarize long sections.
- Prefer skill-provided scripts or templates over retyping or reinventing workflows.
- If a skill is missing or blocked, say so briefly and use the closest safe fallback.
- If applicability is unclear, ask a brief clarifying question before proceeding.

## Shared Policies (Canonical in `AGENTS.md`)
- Decision framing, rationale capture, plan/docs hygiene, git safety, reporting style, and repeat-invocation rules are defined in `AGENTS.md`.
- This doc focuses on skill-specific usage to avoid duplicating those policies.

## Usage Rules
- Trigger: if the user explicitly names a skill, or the task clearly matches a skill description, use that skill.
- Always open the skill's `SKILL.md` first and follow its steps; only read referenced files that you need.
- Prefer existing scripts or templates in the skill over retyping large blocks.
- Keep context small and avoid loading unrelated files.
- If a skill is missing or blocked, say so briefly and continue with the closest safe fallback.

## Adding or Removing Skills
- Add or remove skill directories under `skills/`.
- Keep the `~/.codex/skills` symlinks in sync with this repo.
- Keep the skill name, description, and file path accurate in any skill list that is updated.

## Current Skills
- See `AGENTS.md` for the canonical skill list; keep it in sync if you mirror it here.
