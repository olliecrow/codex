---
name: dangercheck
description: Assess a codebase for potentially dangerous or malicious behavior before running it. Use when the user wants a safety audit of an untrusted repo, scripts, installers, build/test pipelines, or dependencies to decide whether to run locally or only in a sandbox/container.
---

# Dangercheck

## Overview

Assess a repo for malicious or risky behavior without executing code. This skill is strictly static analysis: read files only, do not run code, do not install dependencies, and do not execute any scripts or binaries. Focus on entrypoints, scripts, dependency hooks, and suspicious patterns that could exfiltrate data, modify the system, or download and execute remote content.

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
- If the user is re-running dangercheck, review prior findings and avoid duplicating the same probes.

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
- Track a lightweight investigation log in `plan/dangercheck.md` (untracked) with probes and outcomes.
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

When dangercheck is called multiple times on the same repo, expand coverage rather than repeat the same scans.

- Review the prior `plan/dangercheck.md` log and avoid duplicate probes unless validating a fix.
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
