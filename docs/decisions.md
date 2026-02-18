# Decision Capture Policy

This document defines how to record fixes and important decisions so future work does not re-litigate the same questions. It is written to stay accurate over time; avoid time-specific language.

## When to record
- Any fix for a confirmed bug, regression, or safety issue.
- Any deliberate behavior choice that differs from intuitive defaults.
- Any trade-off decision that affects modeling or behavior.
- Any change that affects external behavior, invariants, or public APIs.

## Where to record
Use the smallest, most local place that makes the decision obvious:
- **Code comments** near the behavior when the rationale is not obvious.
- **Tests** with names/assertions that encode the invariant.
- **Docs** (this file or another focused doc) when the decision is cross-cutting.

Prefer updating an existing note over creating a new file.

## What to record
Keep entries short and focused:
- **Decision**: what was chosen.
- **Context**: what problem or risk it addresses.
- **Rationale**: why this choice was made.
- **Trade-offs**: what we are not doing.
- **Enforcement**: which tests or code paths lock it in.
- **References** (optional): file paths, tests, or PRs that embody the decision.

## Recorded decisions
Decision: Skills default to proactive, autonomous execution for normal in-scope work, and user input is requested only when absolutely necessary.
Context: Repeated invocations were losing momentum due to avoidable check-ins and partial handoffs.
Rationale: Minimizing interruptions improves throughput while preserving safety by narrowing prompts to true blockers and risk decisions.
Trade-offs: Less routine human checkpointing; mitigated by strict escalation triggers for ambiguity, material-risk trade-offs, missing required access/data, and destructive/irreversible actions outside policy.
Enforcement: Shared principles in `docs/skills.md`, repo guidance in `AGENTS.md`, and per-skill `Proactive autonomy and knowledge compounding` sections in `skills/*/SKILL.md`.
References: `docs/skills.md`, `AGENTS.md`, `skills/organise-docs/SKILL.md`, `skills/git-commit/SKILL.md`.

Decision: Non-trivial skill workflows run adaptive loop passes until completion criteria are met.
Context: One-pass execution was leaving actionable issues unresolved between passes.
Rationale: Adaptive loops improve quality by repeatedly investigating, fixing, verifying, and re-checking until evidence shows completion.
Trade-offs: Additional execution cycles on complex tasks; mitigated by explicit stop criteria and scope discipline.
Enforcement: Shared principles in `docs/skills.md`, loop requirements in per-skill proactive sections, and explicit repeat-pass workflow steps in key skills.
References: `docs/skills.md`, `skills/cleanup/SKILL.md`, `skills/git-review/SKILL.md`, `skills/battletest/SKILL.md`.

Decision: For any non-trivial task, run recurring checkpoints throughout the conversation (not only at the end) with frequent `organise-docs` updates and small logical `git-commit` checkpoints.
Context: Durable rationale and reviewable progress were drifting when updates were deferred to end-of-task.
Rationale: Frequent docs + commit checkpoints improve recoverability, reduce risk, and compound reusable knowledge while context is fresh.
Trade-offs: Adds lightweight process overhead; mitigated by keeping checkpoints small and tied to meaningful milestones.
Enforcement: Shared checkpoint guidance in `docs/skills.md`, repo policy in `AGENTS.md`, and per-skill `Long-task checkpoint cadence` sections.
References: `docs/skills.md`, `AGENTS.md`, `skills/organise-docs/SKILL.md`, `skills/git-commit/SKILL.md`.

Decision: Skills should default to autonomous fallback/retry/resume behavior before reporting blockers.
Context: Recent sessions showed repeated transient failures (timeouts, SSH/remote transport issues, missing tools/paths) and repeated re-invocations of the same objectives.
Rationale: Explicit fallback/retry/resume rules reduce avoidable interruptions, improve progress continuity, and keep agents focused on net-new work.
Trade-offs: Slightly more autonomous retries can add extra command attempts; mitigated by bounded retries, backoff, and explicit failure evidence before escalation.
Enforcement: Shared proactive-autonomy bullets in `skills/*/SKILL.md`, plus explicit transient-failure handling in cluster and wait workflows.
References: `skills/wait-for-job/SKILL.md`, `skills/cluster-check/SKILL.md`, `skills/cluster-optimise/SKILL.md`.

Decision: Session startup should default to `prime` familiarization and contract setup before deep execution.
Context: Recent multi-repo sessions repeatedly spent early turns re-establishing autonomy expectations, local context, and hygiene cadence.
Rationale: A standardized prime pass improves first-pass quality by immediately grounding execution in repo docs/state and activating recurring `organise-docs`/`git-commit`/`cleanup`/verification loops.
Trade-offs: Adds lightweight startup overhead; mitigated by keeping prime preflight concise and immediately transitioning into execution.
Enforcement: `prime` skill workflow requirements, shared principles in `docs/skills.md`, and skill list routing in `AGENTS.md`.
References: `skills/prime/SKILL.md`, `docs/skills.md`, `AGENTS.md`.

Decision: Skill policy regressions should be caught with deterministic local checks and CI automation.
Context: Cross-skill wording drift can silently reintroduce avoidable pauses or weaken autonomous loop/checkpoint behavior.
Rationale: A deterministic policy lint provides fast, repeatable enforcement of required autonomy/loop/checkpoint language across all versioned skills.
Trade-offs: Adds a small extra check step during skill edits; mitigated by fast local runtime.
Enforcement: Run `validate_skills.py` (policy lint + quick validation) whenever skill definitions change; use targeted lint/quick checks as needed. CI also enforces this via `skills-validation.yml`.
References: `skills/validate_skills.py`, `skills/lint_skill_policy.py`, `skills/.system/skill-creator/scripts/quick_validate.py`, `.github/workflows/skills-validation.yml`, `docs/skills.md`.

Decision: Skill workflows must never squash commits and must use merge commits for branch integration.
Context: Squash merges collapse logical checkpoint history and weaken traceability of autonomous multi-pass work.
Rationale: Preserving granular commit history improves auditing, rollback precision, and review clarity across long-running skill loops.
Trade-offs: Merge history is more verbose than squash history; mitigated by keeping commits small, logical, and well-labeled.
Enforcement: Shared policy text in `AGENTS.md`, `docs/skills.md`, and per-skill proactive sections; enforced by `lint_skill_policy.py` and `validate_skills.py`.
References: `AGENTS.md`, `docs/skills.md`, `skills/lint_skill_policy.py`, `skills/validate_skills.py`, `skills/*/SKILL.md`.

Decision: Skill workflows should prefer simplification over additional complexity and aggressively clean up bloat as they proceed.
Context: Long-running autonomous sessions can accumulate unnecessary complexity when each pass only adds behavior without consolidation.
Rationale: Explicit simplification pressure keeps maintenance cost down, reduces regression surface area, and improves long-term execution speed and reliability.
Trade-offs: More frequent cleanup can add incremental short-term effort; mitigated by keeping cleanup changes scoped, verified, and tied to current work.
Enforcement: Shared policy text in `AGENTS.md`, `docs/skills.md`, and per-skill proactive sections; enforced by `lint_skill_policy.py` and `validate_skills.py`.
References: `AGENTS.md`, `docs/skills.md`, `skills/lint_skill_policy.py`, `skills/validate_skills.py`, `skills/*/SKILL.md`.

Decision: When translating technical work for quant/trading projects, prefer a trader framing that preserves full fidelity via explicit inventories, book-impact analysis, a term-mapping appendix, and (when latency matters) a step-by-step live timeline replay (acks/fills/cancels, inflight exposure).
Context: Non-trader explanations (ML/math/infra framing) can drop “minor” details that are material to live trading outcomes (fake backtest PnL, limit breaches, execution/microstructure drag, operational failure modes).
Rationale: A consistent trader lens keeps explanations anchored to what ultimately matters when running a book: PnL distribution, risk, costs, liquidity/capacity, execution, controls, and how the system fails.
Trade-offs: Explanations become longer and more structured; mitigated by progressive disclosure (keep the main narrative trader-focused and use appendices/references for completeness).
Enforcement: Use `skills/explain-trader/SKILL.md` workflow (detail inventory, topic routing, book-impact pass, second-pass completeness audit) and keep its references updated (`skills/explain-trader/references/*`).
References: `skills/explain-trader/SKILL.md`, `skills/explain-trader/references/checklist.md`, `skills/explain-trader/references/translations.md`, `skills/explain-trader/references/examples.md`.

Decision: Notion reports are created and maintained directly in Notion via MCP only; never generate HTML or other intermediate report formats.
Context: Intermediate formats add manual steps, create filing drift, and complicate edits/iteration.
Rationale: Creating and updating pages via the Notion MCP tools makes reports automatic, linkable, and filed under the correct workspace location with less friction.
Trade-offs: API-created pages may have limitations (for example, embedding local image artifacts without an externally-resolvable URL). Mitigate by prioritizing tables/text summaries, using safe artifact URLs when available, and using neutral artifact labels when attachments must be added later.
Enforcement: `skills/notion-report/SKILL.md` resolves a Notion parent location and creates/updates report pages via `mcp__notion__notion-create-pages` / `mcp__notion__notion-update-page`.
References: `skills/notion-report/SKILL.md`, `skills/notion-report/agents/openai.yaml`.

Decision: Codex may only edit Notion pages that Codex created; never edit pages created by humans.
Context: Editing human pages can unintentionally overwrite human curation and violates safe-ownership boundaries.
Rationale: A durable “codex-managed” marker makes ownership explicit and keeps edits safe and auditable.
Trade-offs: Some edits will require creating a new report page instead of modifying an existing human page; mitigated by linking to the prior page and keeping naming consistent.
Enforcement: `skills/notion-report/SKILL.md` requires a marker block (`codex-managed: true`) on created pages and forbids editing pages without it.
References: `skills/notion-report/SKILL.md`.

Decision: Notion-report refinement should update a single canonical Codex-managed report page in place rather than creating copies/versions.
Context: Repeated revisions were at risk of producing `v2`/`copy` style page sprawl and splitting the narrative across multiple pages.
Rationale: In-place refinement preserves one source of truth, improves readability, and keeps historical context and links concentrated.
Trade-offs: Ambiguous matching across similarly titled pages requires extra candidate checks; mitigated by title/topic matching plus marker verification before updates.
Enforcement: `skills/notion-report/SKILL.md` requires searching for a matching Codex-managed report first and only creating a new page when no safe matching page exists (or user explicitly asks for a new report).
References: `skills/notion-report/SKILL.md`, `docs/skills.md`.

Decision: Notion reports should be refined via reader-centric multi-pass review loops before completion.
Context: Single-pass report writes can miss reader-critical clarity issues even when facts are correct.
Rationale: Structured review passes (structure, skeptical-reader questions, clarity pass) improve comprehension and reduce ambiguity for downstream readers.
Trade-offs: Additional review/edit cycles add time; mitigated by keeping each pass targeted and updating the same canonical page in place.
Enforcement: `skills/notion-report/SKILL.md` defines required reader-centric passes and requires re-fetch/re-read validation after updates.
References: `skills/notion-report/SKILL.md`, `docs/skills.md`.

Decision: Notion reports are descriptive-only and must not include recommended next steps or follow-up actions.
Context: Recommendation sections can blur reporting with planning and introduce scope the user did not request.
Rationale: Keeping reports strictly descriptive preserves objectivity and ensures the page reflects only what current evidence shows.
Trade-offs: Readers who want action plans need a separate planning artifact; mitigated by making findings and caveats explicit in the report body.
Enforcement: `skills/notion-report/SKILL.md` report behavior and reader-clarity pass explicitly remove recommendations, next experiments, follow-up tasks, and decision directives.
References: `skills/notion-report/SKILL.md`, `docs/skills.md`.

Decision: Notion-report image embedding should rely on externally fetchable `https://` image URLs and post-write fetch verification.
Context: MCP round-trip tests showed Notion sanitizes non-supported image sources (notably `data:` URIs), causing images to disappear or refetch with blank sources.
Rationale: Restricting to externally fetchable `https` sources plus immediate verification prevents silent image loss in published reports.
Trade-offs: Local-only images require an additional safe hosting step (or manual attach fallback), and third-party render/hosting can raise data-sharing concerns.
Enforcement: `skills/notion-report/SKILL.md` image policy requires `https` sources, forbids reliance on `data:` URLs, requires post-update `notion-fetch` checks, and defines fallback behavior when embedding cannot be confirmed.
References: `skills/notion-report/SKILL.md`.

## Template
```
Decision:
Context:
Rationale:
Trade-offs:
Enforcement:
References:
```
