# Skills

This doc describes how skills are organized in this repo. The canonical skill list lives in `AGENTS.md`; keep it updated whenever skills are added or removed.

## Skill Layout
- A skill is a reusable workflow defined by `skills/<name>/SKILL.md`.
- Skills may include `scripts/`, `assets/`, or `references/` used by the workflow.
- Skills in this repo are symlinked into `~/.codex/skills` so Codex loads them as user skills.

## Using Skills (Repo Expectations)
- Read `SKILL.md` first and follow its workflow; open only the referenced files you need.
- Use the smallest set of skills that covers the request; state the order if multiple are used.
- Prefer skill-provided scripts or templates over retyping workflows.
- Keep context tight: avoid bulk-loading folders; summarize long sections.
- If a skill is missing or blocked, say so briefly and use the closest safe fallback.

## Adding or Removing Skills
- Add or remove skill directories under `skills/`.
- Update the skill list in `AGENTS.md`.
- Keep the `~/.codex/skills` symlinks in sync with this repo.
