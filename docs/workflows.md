# Operating Workflow

This doc defines how work is tracked so progress compounds without bloating repo docs. Repo-wide rules live in `AGENTS.md`; this file focuses on routing and workflow mechanics.

## Core routing
- Keep active, disposable notes in `plan/current/`.
- Promote durable guidance into `docs/`.
- Capture important rationale in the smallest durable place (code comments, tests, or docs).
- Keep the workflow spartan: short notes, clear routing, minimal ceremony.

## Note files
- `plan/current/notes.md`: running task notes, key findings, and next actions.
- `plan/current/notes-index.md`: compact index of active workstreams and pointers to detailed notes.
- `plan/current/orchestrator-status.md`: packet/status board for parallel or subagent work.
- `plan/handoffs/`: sequential handoff summaries for staged automation workflows.

## Parallel and subagent work
- Use isolated branches or dedicated working directories when streams are independent.
- Track each stream with owner, scope, status, blocker, and last update.
- Require each stream to produce a concise handoff summary before merge/synthesis.

## Promotion cycle
- During execution: write concise notes to `plan/current/notes.md`.
- At milestones: consolidate and de-duplicate active notes; update `plan/current/notes-index.md`.
- Before finishing: promote durable learnings to `docs/` and trim stale `plan/` artifacts.
- When docs promotion and commit checkpointing are needed in the same milestone, use the `checkpoint` skill alias workflow (`organise-docs -> cleanup -> git-commit`; push only when explicitly requested).

## Stop conditions
- Stop when acceptance checks pass, verification is green, risks are documented, and no unresolved blockers remain.
- If no new evidence appears, avoid repeating identical probes; report completion instead.
