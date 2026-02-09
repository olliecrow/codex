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
- Encourage multi-agent/subagent collaboration when it improves speed, quality, or confidence; split work into clear packets with synthesis checks.
- For experiment-heavy work, optimize for learning throughput and high-information outcomes, not only task completion.
- Default to autonomous execution when confidence is high and the workflow allows it; escalate when confidence is low.
- For git/PR workflows, always check active PR metadata (open draft or ready-for-review) at the end and update stale title/body when needed.
- If a skill is missing or blocked, say so briefly and use the closest safe fallback.
- If applicability is unclear, ask a brief clarifying question before proceeding.

## Shared Requirements and Conventions
For decision framing, rationale capture, plan/docs robustness, git safety, and reporting style, follow the repo-wide policies in `AGENTS.md` and `docs/decisions.md`.

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
