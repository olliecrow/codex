---
name: familiarize
description: Meticulously familiarize with a codebase to understand structure, purpose, and workflows; use when asked to get the lay of the land, orient in a repo, summarize architecture, or assess current branch changes vs main.
---

# Familiarize

## Overview

Build a clear, accurate mental model of the codebase: layout, purpose, key flows, and current change state.

## Workflow

1. Establish scope and constraints:
   - Identify repo root and primary language/tooling.
   - Clarify any time constraints or areas of focus if the user is vague.
   - Prefer read-only exploration; do not modify files unless explicitly asked.

2. Map the repository layout:
   - Scan top-level structure and key directories.
   - Read the primary docs (README, docs/, CONTRIBUTING, ARCHITECTURE) if present.
   - Identify entrypoints, build/test scripts, and configuration files.

3. Understand how the system works:
   - Locate main modules, services, or packages and their responsibilities.
   - Trace high-level data flows or request paths through the code.
   - Note external dependencies and integrations.
   - Identify any conventions (naming, folder roles, patterns).

4. Capture developer workflows and interfaces:
   - Build/run/test map: capture canonical commands and where they live (scripts, Makefile, CI).
   - Config and environment: list required env vars, config files, secrets expectations, and local dev setup.
   - Interfaces: enumerate public APIs/CLIs or entrypoints for users/services.
   - Note similar onboarding essentials when present (e.g., CI/CD, release flow, data stores).

5. Inspect current working tree state:
   - Check `git status -sb`.
   - Review `git diff` and `git diff --staged` for local changes.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands and wait for results before continuing.

6. Compare against main when relevant:
   - If the current branch is not main, review diffs vs main (e.g., `git diff main...HEAD` and relevant logs).
   - Summarize how the current branch diverges (scope and intent) and which areas are affected.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands and wait for results before continuing.

7. Optional deeper dives (as needed):
   - Read critical modules or hot paths to validate understanding.
   - Skim tests to understand expected behavior and coverage.
   - Identify any missing or outdated documentation.

8. Summarize findings:
   - Provide a concise, intuitive summary of the repo structure, purpose, and key workflows.
   - Include brief context for a new reader (what the system does, how parts fit together).
   - Summarize current git status, local diffs, and branch-vs-main diffs if applicable.
   - Note open questions, uncertainties, or areas that need deeper review.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.
