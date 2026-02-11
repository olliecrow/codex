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
- When a conversation is being started or re-oriented and autonomy posture is unclear, run `prime` first to establish startup familiarization plus recurring docs/commit/cleanup/verification loops.
- Default to autonomous execution for normal in-scope steps; do not pause for avoidable confirmations.
- Request user input only when absolutely necessary: ambiguous requirements, material-risk trade-offs, missing required data/access, or destructive/irreversible actions outside policy.
- Drive work end-to-end with verification; prefer complete outcomes over partial handoffs.
- Treat iterative loop passes as the default for non-trivial work; adapt loop shape by skill and keep looping until no actionable in-scope items remain, verification is green, and confidence is high.
- Before reporting blocked, attempt high-confidence fallbacks and bounded retries for transient command/tool/environment failures, and capture failure evidence.
- On repeated invocations of the same objective, resume from prior artifacts and prioritize net-new progress over rerunning identical work unless reruns are required for verification.
- Keep repository documentation accurate: promote durable learnings and decisions to `docs/` as part of normal skill execution.
- Run `organise-docs` frequently during execution when durable learnings or decisions appear; do not defer all documentation to the end.
- For any non-trivial task, run recurring milestone checkpoints instead of a single end wrap-up: use `git-commit` frequently for small logical commits and `organise-docs` to promote durable learnings, then prune stale `plan/` artifacts.
- For git/PR workflows, always check active PR metadata at the end and update stale title/body when needed.
- Never create draft PRs when opening a PR; open ready-for-review PRs only.
- If a pre-existing draft PR is encountered and the work is review-ready, promote it with `gh pr ready` before finishing.
- If a skill is missing or blocked, say so briefly and use the closest safe fallback.
- If applicability is unclear, infer from skill descriptions and task intent first; ask only if ambiguity remains materially blocking.

## Shared Requirements and Conventions
For decision framing, rationale capture, plan/docs robustness, git safety, and reporting style, follow the repo-wide policies in `AGENTS.md` and `docs/decisions.md`.
- After editing skill definitions, run policy lint and quick validation before committing:
  - `python3 /Users/oc/repos/me/codex/skills/lint_skill_policy.py`
  - `python3 /Users/oc/repos/me/codex/skills/.system/skill-creator/scripts/quick_validate.py <skill_directory>`

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
