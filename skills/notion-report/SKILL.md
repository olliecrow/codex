---
name: notion-report
description: Create and maintain scientific/empirical experiment or investigation reports in Notion via MCP from freeform artifacts. Default to direct Notion editing; support local-first draft QA before publishing when explicitly requested.
---

# Notion Report

Create and refine a single canonical report page in Notion from evidence artifacts.

This skill is cross-project by default. It is designed for scientific/empirical reports in any domain. Domain overlays (for example trading/market experiments) are optional and only apply when relevant.

## Core principles (must follow)

- no fixed input schema required
- accept freeform evidence inputs: notes, logs, tables, plots, artifacts, and run outputs
- descriptive-first reporting by default: factual, evidence-backed, and non-prescriptive unless user explicitly requests guidance
- one canonical page per report identity; refine in place (no `v2`/`final` forks)
- plot-first for quantitative reporting; tables are supporting precision
- explicit opener emphasis hierarchy for scanability:
  - bold label-first opener
  - concise high-signal callouts
  - bold key metrics/status tokens only (no blanket bolding)
- reports and report-generation helpers are ephemeral artifacts:
  - keep under `plan/`
  - never commit under tracked code paths (`tools/`, `src/`, `experiments/`, `docs/`)
- if original numeric artifacts still exist, regenerate publication-grade plots from source data; do not use lightweight Notion-native chart specs (for example Mermaid `xychart-beta`) for quantitative findings
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
  - preferred: callout with `🤖` containing:
    - `codex-managed: true`
    - `Only edit this page if this marker is present.`
  - fallback: paragraph containing `codex-managed: true`
- before updating an existing page, fetch page blocks and verify marker exists
- if marker is missing, do not edit that page; create a new Codex-managed page

## Parent/location routing (must follow)

1. If user provides a Notion URL/ID, use that parent.
2. Otherwise, infer from explicit project context and existing report hubs.
3. Prefer existing subpages named like `Reports`, `Experiments`, `Research`, `Runs`, `Results`.
4. If still unclear, ask one short clarification question.

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

## Scientific/empirical report structure (default)

### 1) `Top Takeaways` (must be first section)

- use heading `## Top Takeaways` as first section
- first line: `Question + answer status`
- include the most important outcome immediately
- if there is a clear before/after baseline relation, include explicit delta line (`before -> after`, absolute + relative where available)
- apply emphasis hierarchy:
  - bold label-first opener
  - concise callouts for major win/loss tradeoff when both exist
  - selective bolding of key metrics/status only

### 2) `Experiment Definition` (for experiment/search reports)

Include:
- question/hypothesis being tested
- what varied (search space)
- what was fixed (controls/constants)
- how samples were assigned/swept/randomized
- why this design was used
- evaluation setup/environment(s)
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

Use `notion-local` MCP namespace.

1) Connectivity check:
- call `mcp__notion-local__API-get-self` once per task

2) Resolve parent:
- normalize/verify user-supplied URL/ID with `mcp__notion-local__API-retrieve-a-page`
- otherwise enumerate/search candidate parents and validate

3) Create/update canonical page:
- derive report identity from evidence (experiment/search/run IDs, batch label/date, variant)
- search for existing matching Codex-managed page first
- create only if no matching Codex-managed page exists
- update in place otherwise
- avoid creating duplicates for title wording changes
- include Codex marker callout at end

4) Deduplication behavior:
- keep exactly one canonical page per report identity in target reports location
- when duplicates exist for same data identity, retain one canonical page; move/archive others only with user approval

5) Output contract:
- return created/updated Notion page URL (or ID)

## Image embedding constraints (Notion reality)

- reliable rendering requires externally fetchable `https://...` URL
- `data:` URIs and local-only schemes are not durable in Notion
- after write, re-fetch and verify image blocks still have non-empty external URLs

Embedding sequence:
1. existing stable `https://` image URL
2. URL-rendered chart image when fidelity is preserved
3. approved private/public hosting path to get `https://` URL
4. browser upload fallback (if available) on Codex-managed page
5. if all fail, add `Artifacts to attach` section with neutral labels + meaning

## Iteration loop and finish criteria

- run multi-pass reader-centric refinement:
  - pass 1: structure and narrative arc
  - pass 2: skeptical-reader questions and caveats
  - pass 3: clarity and emphasis hierarchy
- after each pass: update same canonical page and re-fetch to verify landing
- done when:
  - required sections present
  - claims are evidence-grounded
  - visual/table labeling standards met
  - no privacy leakage
  - no actionable quality gaps remain

## Quality checklist (core)

- `Top Takeaways` is first
- explicit `Question + answer status` opener exists
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
- canonical Codex-managed page marker present

## Quality checklist (optional overlays)

Apply only if relevant:
- trading overlay: trader/quant + ML/DL dual-lens takeaway coverage
- cluster overlay: artifact-availability verification before missing-artifact claims
- causal overlay: isolated evidence or explicit associational caveat
