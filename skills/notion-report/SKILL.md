---
name: notion-report
description: Create and maintain scientific/empirical experiment or investigation reports in Notion via MCP from freeform artifacts. Default to direct Notion editing; support local-first draft QA before publishing when explicitly requested.
---

# Notion Report

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

Create and refine a single canonical report page in Notion from evidence artifacts.

This skill is cross-project by default. It is designed for scientific/empirical reports in any domain. Domain overlays (for example trading/market experiments) are optional and only apply when relevant.

## Core principles (must follow)

- no fixed input schema required
- accept freeform evidence inputs: notes, logs, tables, plots, artifacts, and run outputs
- descriptive-first reporting by default: factual, evidence-backed, and non-prescriptive unless user explicitly requests guidance
- for most experiment/investigation reports, make explicit `Question` -> `Answer` flow the narrative backbone
- if a report type is not naturally question-driven (for example operational status output), explicitly state objective/outcome framing instead of forcing Q/A scaffolding
- unless failure behavior is the explicit experiment question, do not make failure-rate metrics the primary headline; treat them as reliability context supporting core outcomes
- one canonical page per report identity; refine in place (no `v2`/`final` forks)
- when publishing into a reports hub, create report pages as direct children of that hub only (no nested/recursive report pages)
- consolidation-first: keep the fewest report pages that still map cleanly to distinct report identities/questions
- plot-first for quantitative reporting; tables are supporting precision
- follow normal report naming convention used by recent reports: `YYYY-MM-DD - <clear human title>`
- avoid opaque shorthand/acronym-heavy naming in titles/headings/captions (for example coded labels like `RB1200` or `B500`); prefer plain-language wording
- explicit opener emphasis hierarchy for scanability:
  - bold label-first opener
  - concise high-signal callouts
  - bold key metrics/status tokens only (no blanket bolding)
- opener clarity is mandatory:
  - first `Top Takeaways` line must contain the explicit report question and a direct answer
  - opener wording must be self-contained plain language; a new reader should not need prior thread context
  - use direct answer tokens (`yes`, `no`, `inconclusive`, or equivalent), not vague status-only wording
  - if outcome is mixed, map it to explicit direct-answer tokens in the opener (for example `runtime yes, performance no` or `inconclusive`)
  - avoid opener text like `Question + answer status: answered` without concrete question text
- if more than one key question is covered, use numbered `Question n` / `Answer n` pairs with strict adjacency (each answer immediately follows its question)
- for multi-question or mixed-certainty investigations, add a dedicated `Question Decomposition` section immediately after `Top Takeaways` using strict `Question n` -> `Answer n` -> `Status n` triples, with one concrete empirical evidence line in each answer
- keep the opener focused on the true experiment objective; do not let reliability/failure-rate stats become the lead claim unless failure analysis is the stated question
- if user scope is a report collection/hub, audit every in-scope report page one-by-one (no sampling)
- legacy-summary fallback rule: if the first summary section is not `Top Takeaways` (for example `Key Takeaways` or `Executive Summary`), enforce the same explicit question+answer opener in that section's first line
- reports and report-generation helpers are ephemeral artifacts:
  - keep under `plan/`
  - never commit under tracked code paths (`tools/`, `src/`, `experiments/`, `docs/`)
- keep report presentation human-facing:
  - reports should read as human-authored and human-consumable
  - do not add Codex/Claude labels in report titles or main body sections
  - keep exactly one small attribution footer note at the end containing `Prepared with support from Codex and Claude. codex-managed: true`
  - if any extra Codex/Claude references are found during refinement, remove them before publish
- if original numeric artifacts still exist, regenerate publication-grade plots from source data; do not use lightweight Notion-native chart specs (for example Mermaid `xychart-beta`) for quantitative findings
- do not upload report artifacts to third-party public/temporary file hosts (for example tmpfiles.org, catbox, imgur, file.io) unless the user explicitly approves
- default to Notion-managed file/image uploads for report visuals (prefer `notion-upload-local` when available); if upload is unavailable in the current toolchain, add `Artifacts to attach` placeholders rather than using unapproved external hosts
- hide local paths, hostnames, tokens, and secrets in report body text
- define acronyms on first use

## Local-first mode (only when user explicitly requests)

- build a deterministic local bundle before Notion writes:
  - report body (`.html` or `.md`)
  - summary payload (`.json`)
  - high-resolution plots (`>=220 dpi`)
- use full artifact rows for core aggregate/distribution visuals unless explicitly labeled sampled
- do not downsample plotted data by default; this is especially required for time-series plots
- preserve native time cadence for time-series plots by default (no implicit temporal aggregation/resampling, e.g. day->month)
- prefer high-fidelity rendered images (PNG/SVG) generated from source artifacts over inline chart DSL blocks
- use Mermaid/Notion-native charts only as an explicit fallback when source data is irretrievably unavailable
- if downsampling or temporal aggregation is unavoidable for tooling/render limits, disclose it explicitly in both caption and methodology (method + factor + why)
- validate local quality before publishing:
  - explicit axis labels + units
  - readable legends
  - no overlap/clipping
  - decision-useful without zooming
- store local bundles in `plan/artifacts/`
- keep temporary helper scripts in `plan/experiments/` (or similar ephemeral `plan/` path)

## Codex-owned pages only (must follow)

Codex may edit only pages created by Codex.

Implementation:
- every Codex-created report page must include a durable marker near the end:
  - preferred: small footer callout containing:
    - `Prepared with support from Codex and Claude. codex-managed: true`
  - fallback: footer paragraph containing the same text
- do not add title suffixes or body labels such as `(Codex-managed regenerated)` or `Only edit this page if this marker is present.`
- before updating an existing page, fetch page blocks and verify marker exists
- if marker is missing, do not edit that page; create a new Codex-managed page

## Parent/location routing (must follow)

1. If user provides a Notion URL/ID, use that parent.
2. Otherwise, infer from explicit project context and existing report hubs.
3. Prefer existing subpages named like `Reports`, `Experiments`, `Research`, `Runs`, `Results`.
4. If still unclear, ask one short clarification question.

Publishing constraint:
- if user asks to add reports under a specific reports page, create report pages directly under that parent only; do not create nested report pages beneath newly created report pages

Current known hubs in this environment (use when relevant):
- GigaPlay hub: `https://www.notion.so/GigaPlay-2edf1d57cab880209415f67e7c65414f`
- GigaPlay reports: `https://www.notion.so/305f1d57cab8802eaac6d100dc242c5d`
- Mercantile hub: `https://www.notion.so/Mercantile-306f1d57cab8802a8b5cc2b513780742`
- Mercantile reports: `https://www.notion.so/306f1d57cab8808e9fafdbd0bb6c9d47`
- Ollie Notes fallback: `https://www.notion.so/Ollie-Notes-21df1d57cab880e2af99fc37c6062b2e`

## Scope and input handling

- if user gives directories: scan recursively for relevant artifacts
- if user gives file list: use the list
- if mixed: combine
- if scope intent is ambiguous: ask one short clarification question
- for remote content: use surfaced local copies, or ask for fetch/copy command

## Collection audit mode (must follow when requested)

- if the user asks to ensure quality across all reports in a hub/project, enumerate all report pages in scope first
- verify opener clarity on each page individually and patch each non-compliant page
- do not stop after spot-checks; completion requires all in-scope pages checked
- re-fetch each in-scope page and confirm opener line contains explicit question + direct answer after the pass

## Scientific/empirical report structure (default)

### 1) `Top Takeaways` (must be first section)

- use heading `## Top Takeaways` as first section
- first line must include both the explicit question and direct answer status
- required opener format: `Question + answer status: <explicit question>? <direct answer>.`
- disallowed opener pattern: status-only wording such as `Question + answer status: answered`
- for most empirical reports, use question/answer lines as the primary narrative driver in this section
- only skip explicit Q/A scaffolding when the report is clearly non-question-driven; in that case state objective and outcome explicitly
- legacy heading fallback: if first summary heading is `Key Takeaways`/`Executive Summary`, apply the same first-line opener rule there
- include the most important outcome immediately
- if there is a clear before/after baseline relation, include explicit delta line (`before -> after`, absolute + relative where available)
- apply emphasis hierarchy:
  - bold label-first opener
  - concise callouts for major win/loss tradeoff when both exist
  - selective bolding of key metrics/status only
- if multiple questions are answered, list numbered `Question n` then `Answer n` lines directly under the opener, keeping each answer immediately after its paired question
- when the report includes several sub-questions or mixed answer certainty, include a dedicated `Question Decomposition` section immediately after `Top Takeaways` with `Question n` -> `Answer n` -> `Status n` ordering and one empirical evidence line per answer

### 2) `Experiment Definition` (for experiment/search reports)

Include:
- question/hypothesis being tested
- what varied (search space)
- what was fixed (controls/constants)
- how samples were assigned/swept/randomized
- why this design was used
- evaluation setup/environment(s)
- answer wording that directly maps to the question terms (no implicit inference required)
- explicit answer status for this batch (`yes/no/inconclusive` or equivalent) with brief evidence-backed why

### 3) `Executive Visual Snapshot`

- place early, after `Experiment Definition`
- include compact high-signal visuals first
- prioritize visuals that answer the report question directly

### 4) `Definitions and Methodology`

- define domain terms used in the report context
- define formulas for derived metrics and signs/directions
- include `unit unavailable` placeholders for unknown units; do not guess

### 5) `Limitations / Reliability`

- include missing data, incomplete runs, comparability gaps, and caveats
- keep reliability emphasis proportional to impact
- do not make completion/failure the hero narrative unless it materially changes conclusions
- when failure rates are not the explicit research target, report them as reliability support (not the primary report focal point)

### 6) `Run Spotlight` (when run-level time-series artifacts exist)

- include 1-3 explicitly selected runs
- show normalized trajectory views when possible (for example growth from `1.00x`)
- if unavailable, explicitly call out artifact gap in limitations

## Evidence discipline (must follow)

- every quantitative claim must map to explicit evidence artifacts
- maintain internal claim map (`claim_id -> artifact/source`) while drafting
- for causal/attribution claims, include isolating evidence or clearly label as associative
- for paired comparisons, report overlap/sample counts used for each pair
- when failure rates are non-trivial, run a basic selection-bias stress check
- preserve numerical/sign integrity (`A - B` direction, units, percent bases)

## Visual and table standards (must follow)

For plots:
- clear title with metric + cohort/slice
- axis labels with explicit units
- axis labels must appear in the plot block itself (not caption-only)
- clear legend/series semantics (or explicit single-series label)
- caption must start with concise `Takeaway:` lead-in, then brief support
- include direction cue where helpful (`higher is better` / `lower is better`)
- avoid unreadable layouts (overlap, clipped labels, ambiguous scales)

For tables:
- clear title
- explicit column headers + units
- clear derived-field names
- short caption with `Takeaway:` lead-in

General:
- plot-first for quantitative interpretation
- prefer fewer high-signal visuals over many redundant ones
- no downsampling by default, especially for time-series visuals
- no implicit temporal aggregation for time-series visuals; keep native cadence unless explicitly justified
- avoid Mermaid `xychart-beta` (or equivalent low-fidelity DSL charts) for empirical metric plots when source artifacts exist
- if downsampling or temporal aggregation is unavoidable, disclose exact method/factor and expected visual impact

## Cross-project refinement loop (must follow)

- keep the skill project-agnostic: domain specifics are overlays, not defaults
- benchmark draft quality against the strongest prior report style available for the current project/domain
- keep what improved readability/interpretability and remove low-signal sections/visuals
- use selective emphasis only (bold key conclusions/metrics/status), not blanket formatting
- ensure the final report remains descriptive-first unless recommendations were explicitly requested

## Optional domain overlays

Use only when relevant to the current project/domain.

### Trading/market experiments (optional overlay)

- include trader/quant lens and ML/DL lens in `Top Takeaways`
- common metrics may include PnL, Sharpe, drawdown, turnover, execution intensity, and robustness
- prefer interpretable intensity metrics (for example `turns/day`) over raw fill counts unless fill mechanics are the focus

### Cluster-backed artifacts (optional overlay)

- verify run-level artifact availability directly (read-only) before declaring missing
- when available, use retained forensics/root-cause fields for failure attribution rather than wrapper labels only

## Optional Claude-assisted drafting

Use only when user explicitly asks for Claude-style drafting/refinement.

- command: `claude -p --model opus --effort high`
- Codex remains source-of-truth for data prep, validation, and Notion writes
- Claude is wording/structure assist only
- pass explicit evidence only; no invented values
- sanitize prompts (paths/hosts/secrets/private IDs)
- require structured output variants + self-check
- run Codex verification gate before applying

Codex verification gate:
- all claims trace to evidence
- units/signs unchanged and correct
- no scope drift or unsupported claims
- no path/host leakage
- section-order constraints preserved

## Notion MCP workflow (must follow)

Use `notion-local` for page/database operations and `notion-upload-local` for direct image/file uploads.

1) Connectivity check:
- call `mcp__notion-local__API-get-self` once per task

2) If visuals are required, verify `notion-upload-local` upload capability before publishing image blocks.

3) Resolve parent:
- normalize/verify user-supplied URL/ID with `mcp__notion-local__API-retrieve-a-page`
- otherwise enumerate/search candidate parents and validate

4) Create/update canonical page:
- derive report identity from evidence (experiment/search/run IDs, batch label/date, variant)
- search for existing matching Codex-managed page first
- create only if no matching Codex-managed page exists
- update in place otherwise
- avoid creating duplicates for title wording changes
- keep pages flat under the chosen reports parent; do not create nested report pages inside report pages
- include one small footer attribution note at end with `Prepared with support from Codex and Claude. codex-managed: true`
  - before finalizing, confirm no other Codex/Claude references remain in title/body

5) Upload visuals:
- prefer `notion-upload-local` tool path for direct Notion-managed uploads
- if upload tooling is unavailable, add `Artifacts to attach` placeholders rather than external-host workarounds

6) Deduplication behavior:
- keep exactly one canonical page per report identity in target reports location
- prefer consolidation into fewer pages when multiple pages represent the same identity/question
- when duplicates exist for same data identity, retain one canonical page; move/archive others only with user approval

7) Output contract:
- return created/updated Notion page URL (or ID)

## Image embedding constraints (Notion reality)

- preferred rendering path is Notion-managed file/image uploads
- do not use third-party public file hosting by default
- external hosting is allowed only with explicit user approval and should prefer first-party/org-controlled infrastructure
- `data:` URIs and local-only schemes are not durable in Notion
- after write, re-fetch and verify image/file blocks still have non-empty URLs and non-zero payloads at verification time

Embedding sequence:
1. `notion-upload-local` direct file/image upload (Notion-managed)
2. browser upload fallback (if available) on Codex-managed page (Notion-managed)
3. reuse existing Notion-managed file/image blocks when valid
4. explicitly approved first-party/org-controlled `https://` hosting path
5. if all fail, add `Artifacts to attach` section with neutral labels + meaning (do not use unapproved third-party hosts)

## Iteration loop and finish criteria

- run multi-pass reader-centric refinement:
  - pass 1: structure and narrative arc
  - pass 2: skeptical-reader questions and caveats
  - pass 3: clarity and emphasis hierarchy
- after each pass: update same canonical page and re-fetch to verify landing
- done when:
  - required sections present
  - opener includes explicit question text and direct answer status
  - opener question and answer are unambiguous to a cold reader
- when multiple questions are present, Q/A ordering is explicit and adjacent (`Question n` then `Answer n`)
- when `Question Decomposition` is present, each `Question n` has adjacent `Answer n` and `Status n` lines, and each `Answer n` includes one concrete empirical evidence line
  - claims are evidence-grounded
  - visual/table labeling standards met
  - no privacy leakage
  - no actionable quality gaps remain
  - for collection-scope tasks, every in-scope report page was individually checked and opener clarity is verified

## Quality checklist (core)

- `Top Takeaways` is first
- explicit `Question + answer status` opener exists
- opener includes explicit question text (not implied) and direct answer (`yes`/`no`/`inconclusive` or equivalent)
- when `Question Decomposition` exists, it uses strict `Question n` -> `Answer n` -> `Status n` ordering with one empirical evidence line per answer
- vague status-only opener answers (for example `mixed`, `answered`, `improved`) are non-compliant unless mapped to explicit direct-answer tokens
- opener question is self-contained plain language (no shorthand requiring external context)
- report naming is human-readable (`YYYY-MM-DD - <clear human title>`) and avoids opaque shorthand/acronym-heavy labels
- report page is a direct child of the target reports hub (no nested/recursive report pages)
- failure-rate metrics are present for reliability context but are not headline focal points unless failure behavior is the explicit research question
- no vague status-only opener wording (for example `answered`) without explicit question text
- legacy first-summary sections (`Key Takeaways`/`Executive Summary`) apply the same explicit opener rule when `Top Takeaways` is absent
- opener emphasis hierarchy is correct
- `Experiment Definition` includes what varied/fixed/how/why/eval setup/answer
- `Executive Visual Snapshot` is present for quantitative reports
- captions use `Takeaway:` lead-ins
- axis labels/units/legends are explicit and readable
- plotted series are not downsampled (or any unavoidable downsampling is explicitly disclosed with method/factor/why)
- time-series plots keep native artifact cadence (or any aggregation is explicitly disclosed with method/factor/why)
- empirical charts are regenerated from original artifacts (no low-fidelity Notion-native chart DSL when source data exists)
- limitations/reliability caveats are present and proportional
- report is descriptive-only unless user explicitly requested recommendations
- no table-of-contents block
- no local path/hostname leakage
- exactly one footer attribution marker is present (`Prepared with support from Codex and Claude. codex-managed: true`) and there are no other Codex/Claude references in title/body
- no third-party public file host usage unless explicitly approved by the user
- image/file blocks are Notion-managed by default and resolve to non-empty payloads at verification time
- if visuals are expected, upload capability is verified before publish (or placeholders are used when unavailable)
- for collection-scope tasks, all in-scope report pages were audited one-by-one (no sampling)

## Quality checklist (optional overlays)

Apply only if relevant:
- trading overlay: trader/quant + ML/DL dual-lens takeaway coverage
- cluster overlay: artifact-availability verification before missing-artifact claims
- causal overlay: isolated evidence or explicit associational caveat
