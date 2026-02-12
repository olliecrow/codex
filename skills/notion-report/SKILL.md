---
name: notion-report
description: Generate a standalone, Notion-ready report (copy/paste Markdown plus explicit image placeholders) from a specific set of experiment artifacts (local run folders, cluster job outputs). Use when the user asks for an objective experiment/cluster report to paste into Notion with tables, comparisons, and plots saved to disk.
---

# Notion Report

Create a self-contained experiment report suitable for copy/paste into Notion, with plots and other visuals written to an ephemeral output directory (default: `plan/artifacts/notion-report/...`).

The report must be:
- standalone: readable without external links or prior-run context
- scoped: only describe the runs/outputs explicitly included in this report
- objective: state facts and evidence; avoid subjective tone and speculative future work
- visual: prefer tables and plots over prose

Do not include subjective commentary (for example “promising”, “good/bad”, “I think”, “we believe”).
When comparing runs, use objective phrasing (for example “higher/lower”, “delta”, “rank”, “span”, “percent difference”).

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Proactive autonomy and knowledge compounding

- Be proactive: immediately take the next highest-value in-scope action when it is clear.
- Default to autonomous execution: do not pause for confirmation between normal in-scope steps.
- Request user input only when absolutely necessary: ambiguous requirements, material risk tradeoffs, missing required data/access, or destructive/irreversible actions outside policy.
- If blocked by command/tool/env failures, attempt high-confidence fallbacks autonomously before escalating (for example `rg` -> `find`/`grep`, `python` -> `python3`, alternate repo-native scripts).
- When the workflow uses `plan/`, ensure required plan directories exist before reading/writing them (create when edits are allowed; otherwise use an in-memory fallback and call it out).
- Treat transient external failures (network/SSH/remote APIs/timeouts) as retryable by default: run bounded retries with backoff and capture failure evidence before concluding blocked.
- On repeated invocations for the same objective, resume from prior findings/artifacts and prioritize net-new progress over rerunning identical work unless verification requires reruns.
- Drive work to complete outcomes with verification, not partial handoffs.
- Treat iterative execution as the default for non-trivial work; run adaptive loop passes. Example loops (adapt as needed, not rigid): issue-resolution `investigate -> plan -> fix -> verify -> battletest -> organise-docs -> git-commit -> re-review`; cleanup `scan -> prioritize -> clean -> verify -> re-scan`; docs `audit -> update -> verify -> re-audit`.
- Keep looping until actual completion criteria are met: no actionable in-scope items remain, verification is green, and confidence is high.
- Run `organise-docs` frequently during execution to capture durable decisions and learnings, not only at the end.
- Create small checkpoint commits frequently with `git-commit` when changes are commit-eligible, checks are green, and repo policy permits commits.
- Never squash commits; always use merge commits when integrating branches.
- Prefer simplification over added complexity: aggressively remove bloat, redundancy, and over-engineering while preserving correctness.
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Long-task checkpoint cadence

- For any non-trivial task (including long efforts), run recurring checkpoint cycles instead of waiting for a single end-of-task wrap-up.
- At each meaningful milestone with commit-eligible changes, and at least once per major phase, invoke `git-commit` to create a small logical checkpoint commit once relevant checks are green and repo policy permits commits.
- At the same cadence, invoke `organise-docs` whenever durable learnings/decisions appear, and prune stale `plan/` scratch artifacts.
- If either checkpoint is blocked (for example failing checks or low-confidence documentation), resolve or record the blocker immediately and retry before expanding scope.

## Output contract

Write the following to a single, isolated output directory (prefer under `plan/artifacts/` so it stays ephemeral and gitignored):
- `report.md`: Notion-ready Markdown with explicit placeholders for images.
- `images/`: generated plots (and any copied visuals) with stable filenames.
- `inventory.json`: the inputs discovered/used (paths, metrics sources, copied images, warnings).

Always surface the full output directory path at the end so the user can find the images.

## Notion formatting rules

- Prefer: headings, bullets, and Markdown tables.
- Do not rely on local-image Markdown embedding. Instead, include explicit placeholders like:
  - `[[INSERT IMAGE: images/metric_reward_overlay.svg]]`
- Keep placeholders adjacent to the caption text so it is obvious where to insert each image.
- Do not paste full configs into the report. If settings/configuration are relevant, include a condensed summary (a small table or bullets of key parameters) and a reference path to the config/artifact for reproducibility.

## Skill path (set once)

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export NOTION_REPORT_CLI="$CODEX_HOME/skills/notion-report/scripts/notion_report.py"
```

## Workflow

1. Lock report scope (must be explicit).
- Identify the exact run/job outputs to include.
- Do not include “other recent runs” unless the user explicitly asks.

2. Sync artifacts if needed.
- If outputs live on a cluster or remote machine, sync them locally first (for example by running `cluster-check` before reporting).

3. Render the report artifacts to an ephemeral directory.

Example (explicit run directories):

```bash
python3 "$NOTION_REPORT_CLI" \\
  --title "Experiment report: <short name>" \\
  --motivation "<why this was run (1-2 sentences)>" \\
  --run /path/to/run_a \\
  --run /path/to/run_b
```

4. Review and tighten the report for objectivity and self-containedness.
- Ensure “motivation” explains only the reason for this report’s scope.
- Ensure conclusions are phrased as objective findings tied to reported metrics/plots.
- Remove references to other past runs or upcoming work.
- If configs exist, summarize only the small set of key parameters needed to interpret the runs; do not paste entire config files.

5. Provide the copy/paste payload.
- Print the contents of `report.md` in the chat so the user can paste into Notion.
- Remind the user to insert images from `images/` at the placeholders.

## Script reference

- CLI: `scripts/notion_report.py`
- Standard library only (no required dependencies).
- Generates SVG plots when timeseries/final metrics are available; otherwise it emits a tables-only report and records missing-data warnings in `inventory.json`.
- Reads only JSON/TOML configs for condensed settings summaries (YAML is not parsed to keep dependencies minimal).
