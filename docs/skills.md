# Skills

This doc summarizes the version-controlled Codex skills that live in this repo and how agents should use them. It is agent-focused and meant to stay evergreen. The canonical skill list lives in `AGENTS.md`; avoid duplicating full skill inventories here.

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
- For any non-trivial task, run recurring milestone checkpoints throughout the conversation (not only at the end): use `git-commit` frequently for small logical commits and `organise-docs` to promote durable learnings, then prune stale `plan/` artifacts.
- Never squash commits in skill workflows; preserve history and use merge commits when integrating branches.
- Prefer simplification over added complexity in skill workflows: aggressively remove bloat, redundancy, and over-engineering while preserving correctness.
- For git/PR workflows, always check active PR metadata at the end and update stale title/body when needed.
- Never create draft PRs when opening a PR; open ready-for-review PRs only.
- If a pre-existing draft PR is encountered and the work is review-ready, promote it with `gh pr ready` before finishing.
- If a skill is missing or blocked, say so briefly and use the closest safe fallback.
- If applicability is unclear, infer from skill descriptions and task intent first; ask only if ambiguity remains materially blocking.

## Shared Requirements and Conventions
For decision framing, rationale capture, plan/docs robustness, git safety, and reporting style, follow the repo-wide policies in `AGENTS.md` and `docs/decisions.md`.
- After editing skill definitions, run policy lint and quick validation before committing:
  - preferred all-skills check: `python3 "${CODEX_HOME:-$HOME/.codex}/skills/validate_skills.py"`
  - targeted policy check: `python3 "${CODEX_HOME:-$HOME/.codex}/skills/lint_skill_policy.py" <skill_directory>`
  - targeted frontmatter check: `python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" <skill_directory>`
- CI enforces the same checks on skill/doc changes via `.github/workflows/skills-validation.yml`.
- Use `docs/prompt-cookbook.md` as the shared source for copy-paste prompt templates in this repo.
- For high-frequency skills, keep `Trigger phrases` and `Prompt templates` sections inside each `SKILL.md` so intent mapping and usage examples stay local to the skill.

### Repeat invocations (where present)
- Continue from prior logs and avoid repeating identical probes unless verifying a fix.
- Expand coverage gradually and provide a cumulative summary of work completed so far.

## Usage Rules
- Trigger: if the user explicitly names a skill, or the task clearly matches a skill description, use that skill.
- Always open the skill's `SKILL.md` first and follow its steps; only read referenced files that you need.
- Prefer existing scripts or templates in the skill over retyping large blocks.
- Keep context small and avoid loading unrelated files.

## Domain-Specific Framing

- For quant/trading work where the user wants a trader-perspective explanation (PnL, risk, exposure, execution, microstructure, latency, liquidity, limits, failure modes) rather than ML/math framing, use `skills/explain-trader/SKILL.md`.
- `explain-trader` is designed to preserve fidelity via a detail inventory, a topic-routing step (including HFT/latency-critical live behavior), a full book-impact pass, a structured term-mapping appendix, and a second-pass completeness gate (see its `references/` for checklists, translations, and examples).
- For branch/PR review requests (for example `git-review` / `review-branch`), prioritize finding critical red flags and serious issues first; present findings ordered by severity before secondary observations.
- For git synchronization requests (for example `git pull`, `pull most recent remote main`, `sync branch`), use `skills/git-sync/SKILL.md` for safe fast-forward sync and explicit branch-state verification.
- For competition submission-capability checks (for example AMMChallenge/Highload readiness), use `skills/competition-submit-check/SKILL.md` rather than plain browser automation.
- For combined milestone hygiene (`organise-docs` + `git-commit`), use `skills/checkpoint/SKILL.md`.
- For long-running Slurm monitoring where Codex should wait patiently, poll intermittently, and intervene only on systemic failure/low-learning conditions (for example repeated OOM rates crossing policy thresholds), use `skills/cluster-monitor/SKILL.md` (patient low-token monitoring loop, conservative thresholds with a projected-learning-value gate, diagnose-and-plan before cancellation, whole-batch intervention when systemic, decisive cleanup/fix/resubmit, and immediate post-completion sync/analysis).
- For cluster status-only prompts (for example per-node CPU/GPU usage, QoS, queue snapshot), use `skills/cluster-check/SKILL.md` quick-status mode; escalate to deep-check mode only when deeper diagnosis is requested.
- For experiment/investigation reporting where the user wants the report created/maintained in Notion, use `skills/notion-report/SKILL.md` (creates/updates pages via the Notion MCP tools; no HTML or intermediate formats; prefers a single canonical report page updated in-place; requires a `Top Takeaways` section at the top of every report; includes reader-centric multi-pass review loops; descriptive-only reporting with no next-step recommendations; enforces clear plot/table titles, axis/header labels, legends or single-series labels, short descriptions, explicit units, and directional cues when applicable; only edits Codex-managed pages).

## Adding or Removing Skills
- Add or remove skill directories under `skills/`.
- Keep the `~/.codex/skills` symlinks in sync with this repo.
- Keep the skill name, description, and file path accurate in any skill list that is updated.
