# Skills

This doc summarizes the version-controlled Codex skills that live in this repo and how agents should use them. It is agent-focused and meant to stay evergreen. The canonical skill list lives in `AGENTS.md` to avoid duplication; update both if a list must appear here.

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

## Shared Requirements and Conventions

### Decision framing
- Provide context, options, and a recommendation with reasoning (see `AGENTS.md` for the full policy).

### Rationale capture
- Record the "why" for fixes and important decisions in a durable place and call it out in summaries.

### Plan/docs/decisions robustness
- Keep `plan/` untracked and disposable; prefer durable notes in `docs/` or code when needed.
- Follow the decision capture policy in `docs/decisions.md`.

### Git safety and permissions (git-related skills)
- Follow repo git policy and session restrictions; never rewrite history or force push (see `AGENTS.md`).

### Reporting style
- Write summaries in plain, concise language with brief context.
- Avoid analogies; define technical terms when needed.

### Repeat invocations (where present)
- Continue from prior logs and avoid repeating identical probes unless verifying a fix.
- Expand coverage gradually and provide a cumulative summary of work completed so far.

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
