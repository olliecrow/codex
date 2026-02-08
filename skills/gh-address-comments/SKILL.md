---
name: gh-address-comments
description: Help address review/issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first and prompt the user to authenticate if not logged in.
metadata:
  short-description: Address comments in a GitHub PR review
---

# PR Comment Handler

Guide to find the open PR for the current branch and address its comments with gh CLI. Run all `gh` commands with elevated network access.

Prereq: ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` with escalated permissions (include workflow/repo scopes) so `gh` commands succeed. If sandboxing blocks `gh auth status`, rerun it with `sandbox_permissions=require_escalated`.

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Preflight (must run first)

- Confirm repo context and branch state (`git rev-parse --show-toplevel`, `git symbolic-ref -q --short HEAD`).
- Confirm `gh` availability/auth (`command -v gh`, `gh auth status`).
- If detached HEAD or branch PR lookup fails, require an explicit PR number/URL instead of guessing.
- Verify referenced paths exist before reading/writing helper outputs.

## 1) Inspect comments needing attention
- Run scripts/fetch_comments.py which will print out all the comments and review threads on the PR
- If branch-based PR discovery fails, retry with explicit `--repo <owner>/<repo>` and PR identifier.
- If the script fails due to `gh` JSON schema drift, rerun with a reduced field set and continue.

## 2) Ask the user for clarification
- Number all the review threads and comments and provide a short summary of what would be required to apply a fix for it
- Ask the user which numbered comments should be addressed

## 3) If user chooses comments
- Apply fixes for the selected comments

Notes:
- If gh hits auth/rate issues mid-run, prompt the user to re-authenticate with `gh auth login`, then retry.
- Treat `Unknown JSON field` as schema drift and reduce requested fields before failing.
- Treat `Not Found (404)` as repo/PR mismatch first; validate `--repo` and PR identity.
