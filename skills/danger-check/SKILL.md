---
name: danger-check
description: Assess a codebase for potentially dangerous or malicious behavior before running it. Use when the user wants a safety audit of an untrusted repo, scripts, installers, build/test pipelines, or dependencies to decide whether to run locally or only in a sandbox/container.
---

# Dangercheck

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
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Long-task checkpoint cadence

- For any non-trivial task (including long efforts), run recurring checkpoint cycles instead of waiting for a single end-of-task wrap-up.
- At each meaningful milestone with commit-eligible changes, and at least once per major phase, invoke `git-commit` to create a small logical checkpoint commit once relevant checks are green and repo policy permits commits.
- At the same cadence, invoke `organise-docs` whenever durable learnings/decisions appear, and prune stale `plan/` scratch artifacts.
- If either checkpoint is blocked (for example failing checks or low-confidence documentation), resolve or record the blocker immediately and retry before expanding scope.

## Overview

Assess a repo for malicious or risky behavior without executing code. This skill is strictly static analysis: read files only, do not run code, do not install dependencies, and do not execute any scripts or binaries. Conduct a deep, thorough review of all relevant files, entrypoints, and dependencies, and reason through every finding. Focus on entrypoints, scripts, dependency hooks, and suspicious patterns that could exfiltrate data, modify the system, or download and execute remote content.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Never execute code or install dependencies in danger-check; there is no approval path for execution.
- State assumptions explicitly; if a finding has multiple interpretations, list them and note uncertainty.
- Prefer the simplest explanation supported by evidence; do not assume safety or malice without proof.
- Keep scope surgical and static-only; do not expand into unrelated audits or execution.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.
If no decision is required, say so explicitly and continue.

## Rationale capture

When you make a remediation recommendation or reach an important decision, capture the "why" in a durable place (code comments, docs, ADR, or tests) if changes are made. Do not rely only on `plan/` scratch notes. In your report, mention where the rationale was recorded.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Quick start

- Identify repo root and languages; enforce a no-execution rule.
- Map entrypoints and auto-run hooks using the checklists in `references/entrypoints.md`.
- Run the red-flag scans in `references/patterns.md` and inspect each hit in context.
- Inventory dependencies and any fetched binaries.
- Summarize risk and recommend containment using `references/report-template.md`.

## Workflow

### 1) Scope, inventory, and guardrails

- Confirm the static-only rule: do not run code, do not install deps, do not execute scripts or binaries.
- Never trigger build/test/format/lint commands; only read/scan files.
- Identify repo root, primary languages, and build tooling.
- Inventory files and size so you know what you are scanning.
- Ensure every relevant area is reviewed; explicitly call out any unscanned scope.
- If the user is re-running danger-check, review prior findings and avoid duplicating the same probes.

Suggested commands (adapt):
- `rg --files -g '!.git/**' -g '!**/node_modules/**' -g '!**/vendor/**'`
- `find . -type f -size +5M -print`
- `find . -type f \( -name '*.exe' -o -name '*.dll' -o -name '*.so' -o -name '*.dylib' \) -print`

If the repo is huge, note unscanned areas explicitly (for example: large `vendor/`, `dist/`, `build/`, `node_modules/`).

### 2) Map execution entrypoints and auto-run mechanisms

- Enumerate install/build/test/run entrypoints and automation hooks.
- Use `references/entrypoints.md` for ecosystem-specific locations and files.
- Pay special attention to hooks that run automatically (install hooks, git hooks, editor tasks, CI).

### 3) Static scan for red flags

- Use `references/patterns.md` to scan for:
  - network download + execution
  - dynamic execution (`eval`, `exec`, `Function`, `subprocess`, `os.system`)
  - privilege escalation and persistence
  - credential access and data exfiltration
  - obfuscation and encoded payloads
  - filesystem destruction
- For each hit, open the file and evaluate context, intent, and reachability.
- Track a lightweight investigation log in `plan/current/danger-check.md` (untracked) with probes and outcomes. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
- For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

### 4) Dependency and supply-chain review

- Identify lockfiles and manifest files; look for git/url/path dependencies.
- Check for install-time scripts or build hooks that run during install or build.
- Flag dependencies that download or execute binaries.
- Note any custom registries, extra index URLs, or disabled TLS verification.

### 5) Persistence and system modification review

- Look for edits to shell profiles, SSH keys, cron/launchd/systemd, registry, or system paths.
- Scan for `sudo`, `setcap`, `chown`, `chmod +s`, `launchctl`, `systemctl`, `crontab`.
- Check for modification of browser profiles, keychains, or credential stores.

### 6) Binaries and blobs (no execution)

- Identify unexpected binaries and large blobs; inspect using `file` and `strings` only.
- If binaries are essential (for example: prebuilt tools), note their provenance and checksums if present.

### 7) Risk evaluation and containment recommendation

- Categorize findings:
  - High: clearly malicious or dangerous behavior
  - Medium: suspicious or unnecessary risk without justification
  - Low: expected for the toolchain but still needs awareness
- Recommend a safe execution context (container/VM/restricted user) if any risk exists.
- If uncertain, recommend not running locally.
- If the assessment is incomplete, explicitly list what remains and what deeper check you will do next.

## Repeat invocations

When danger-check is called multiple times on the same repo, expand coverage rather than repeat the same scans.

- Review the prior `plan/current/danger-check.md` log and avoid duplicate probes unless validating a fix.
- Add new perspectives: different entrypoints, less common ecosystems, or deeper analysis of suspicious files.
- Increase depth in stages:
  1) New entrypoints and hooks not previously scanned.
  2) Deeper dependency inspection (transitives, lockfile diffs, vendored deps).
  3) Binary inspection with `file`/`strings` and checksum verification if available.
  4) Focused manual review of suspicious files and call chains.
- If new findings appear, re-evaluate risk and update containment recommendations.

## Output format

Use the template in `references/report-template.md`.

Call out:
- key risks with file paths and evidence
- unscanned areas or large binaries
- clear "safe to run?" recommendation
- next steps (sandboxing, request user intent, or deeper analysis)
- a plain, concise, and intuitive summary with brief context so a new reader can follow it
- no analogies; use simple, direct explanations and define any necessary technical terms

## Static-only enforcement

- Never execute code, never install dependencies, and never run repo-provided scripts.
- Use read-only commands and file inspection tools only (`rg`, `sed`, `cat`, `file`, `strings`, `find`).
- If any step would require execution to confirm behavior, stop and flag it as a risk with a containment recommendation.
