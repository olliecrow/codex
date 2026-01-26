# Skills

This doc summarizes the version-controlled Codex skills that live in this repo and how agents should use them. It is agent-focused and meant to stay evergreen.

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
- Provide background context sufficient to make the decision.
- Include pros and cons for each viable option.
- Give a recommendation with reasoning; some skills also require explicit evidence for why the chosen lever is correct.

### Rationale capture
- Record the "why" for fixes and important decisions in a durable place (code comments, docs, ADR, or tests).
- Do not rely on `plan/` scratch notes; mention where the rationale was recorded in the summary/report.

### Plan/docs/decisions robustness
- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and call out that it was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed; if not, capture rationale in the smallest durable local place and call out the missing decision doc.

### Git safety and permissions (git-related skills)
- Follow repo git policy and session restrictions; if git writes/pushes are disallowed, provide commands instead of executing them.
- Never rewrite history or force push: avoid `git rebase`, `git commit --amend`, `git reset --hard/--soft/--mixed`, `git push --force/--force-with-lease`, `git filter-branch`, and `git clean -fdx`.

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
- battletest: Stress-test recent changes across configurations and perspectives.
- cleanup: Simplify recent changes without altering behavior.
- commit: Create small, well-described git commits (no pushing).
- dangercheck: Safety audit before running untrusted code.
- decisions: Deep, thorough decision support with research and consolidated recommendations.
- execute: Run an existing plan end-to-end and report results.
- familiarize: Orient to the repo, structure, and workflows.
- gitmerge: Prepare a branch to merge cleanly into main.
- gitreview: Deep review of a branch for merge readiness.
- gitsummary: Concise PR-ready summary of diffs vs main.
- investigate: Deep-dive investigation with evidence and tests.
- plan: Create comprehensive, high-conviction change plans.
- setup: Initialize docs/plan/decisions conventions.
- summarize: Concise, decision-ready summaries with evidence.
- techdebt: Identify and reduce technical debt safely.
- verify: Run checks to confirm recent work is correct.
