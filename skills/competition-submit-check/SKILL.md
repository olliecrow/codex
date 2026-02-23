---
name: competition-submit-check
description: Verify end-to-end ability to submit to competition platforms (for example AMMChallenge/Highload) using browser automation, with clear evidence and blocker diagnostics.
---

# competition-submit-check

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

## Overview

Verify whether Codex can submit to a competition platform right now, and explain precisely what is working vs blocked.

Primary targets:
- AMMChallenge
- Highload
- other browser-based competition submission portals with similar flows

Default mode is a non-destructive capability check. Perform an irreversible submission only when the user explicitly asks to submit now.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Use the `playwright` skill workflow/tools for browser automation.
- Treat "final submit click" as irreversible. Do not click final submit unless explicitly requested.
- Capture evidence for each checkpoint (URL reached, auth status, submit form availability, final-step readiness).
- Prefer quoted paths and explicit path checks when running shell commands to reduce avoidable glob/path failures.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Workflow

1. Identify target and mode:
   - Infer target platform from prompt (`ammchallenge`, `highload`, or explicit URL).
   - Select mode:
     - `capability-check` (default): verify ability to reach final submit step without sending.
     - `submit-now`: complete real submission only when explicitly requested.

2. Preflight:
   - Confirm browser automation path (`playwright-cli`/wrapper or available Playwright MCP tools).
   - Confirm presence of expected auth/session artifacts if project uses them (cookies/profile/storage state).
   - Confirm submission artifact exists when artifact upload is required.

3. Run capability probes:
   - Reach target site and challenge page.
   - Validate auth/session state (logged in, challenge accessible).
   - Navigate to submit flow and perform required pre-submit actions (file select, metadata fields).
   - In `capability-check`, stop at the last reversible step before final submit.

4. Optional real submission (`submit-now` only):
   - Proceed with final submit action.
   - Capture submission identifier/receipt if available.

5. Diagnose blockers when present:
   - Classify blocker as one of:
     - auth/session expired,
     - missing permissions,
     - site/network issue,
     - missing/invalid artifact,
     - automation flow drift (selector/UI changed).
   - Provide exact next command/action to unblock.

6. Output contract:
   - Return a binary verdict: `can-submit` or `blocked`.
   - Include mode used, platform, timestamp, and evidence for each checkpoint.
   - If blocked, include the minimal unblock plan and expected retry command(s).

## Reporting format

1. Target platform and mode.
2. Capability checkpoints (site, auth, submit form, final-step readiness).
3. Submission result (only for `submit-now` mode).
4. Blockers and root cause (if any).
5. Exact next command(s) to retry.
6. Evidence runbook (commands/pages/artifacts).

## Repeat invocations

- Reuse last known working auth/session path when still valid.
- Re-run only failed checkpoints first before repeating full flow.
- If previously `can-submit`, run a lightweight smoke path unless user requests full submission.
