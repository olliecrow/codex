# Project Preferences (Going Forward)

These preferences define how `codex` should be maintained as an open-source-ready runtime/docs repository.

## Quality and Scope

- Keep container/runtime behavior explicit and reproducible.
- Keep skills and docs composable, minimal, and aligned with actual workflows.
- Prefer narrow, reviewable changes over broad refactors.

## Security and Confidentiality

- Never commit secrets, credentials, tokens, API keys, or private key material.
- Never commit private/sensitive machine paths; use placeholders such as `/path/to/project`, `/Users/YOU`, `/home/user`, or `C:\\Users\\USERNAME`.
- Keep local runtime state untracked (`.env*`, `.claude/`, `.codex/`, temp artifacts).
- If sensitive data is found in history, rotate credentials and scrub history before publication.

## Documentation Expectations

- Keep `README.md`, `AGENTS.md`, and `docs/` synchronized with real behavior.
- Ensure docs remain human-usable and remove redundant/stale guidance quickly.

## Verification Expectations

- Run relevant checks for touched areas (container sanity, script checks, skills validation).
- Capture verification evidence in PR descriptions when practical.

## Collaboration Preferences

- Preserve accurate author/committer attribution for each contributor.
- Avoid destructive history rewrites unless required for secret/confidentiality remediation.
