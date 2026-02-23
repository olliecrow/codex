---
name: notion-report
description: Create and maintain experiment/investigation reports in Notion via the Notion MCP server from freeform inputs and artifacts. Default to direct Notion editing, but support local-first drafts (HTML/Markdown + plot assets) when the user explicitly asks for local QA before publishing.
---

# Notion Report

Create a report page directly in Notion (via MCP), filed under an appropriate project/workspace location.

- no fixed input schema required
- no fixed tooling required (Python optional for plots/visuals when available)
- accept freeform inputs: notes, logs, tables, images, artifacts, and run outputs
- default mode: work directly in Notion (create/add/edit pages)
- when the user explicitly requests local-first report QA, generate local draft artifacts first (HTML/Markdown + plots), review quality locally, then publish/update Notion from the approved local draft
- hide local paths and hostnames in visible text
- define acronyms on first use in the report

## Local-first mode (when explicitly requested)

- Create a deterministic local report bundle before any Notion writes:
  - report body (`.html` or `.md`)
  - summary metrics payload (`.json`)
  - high-resolution plots (`>=220 dpi`)
- Use full artifact rows for aggregate/distribution visuals (do not rely on display-only downsampled subsets for the core distributions unless explicitly labeled as sampled).
- Validate local output quality first:
  - axis labels and units are explicit
  - legends are readable
  - no overlap/clipping
  - key figures are decision-useful without zooming
- Only after local quality is acceptable, create/update the Notion page.
- Keep the local report bundle under `plan/artifacts/` for reproducibility and future edits.

## Codex-owned pages only (must follow)

Codex may only edit pages that Codex created. Never edit pages that were not created by Codex.

Implementation rule:
- Every page Codex creates MUST include a durable marker block near the end:
  - prefer a callout block (`icon: 🤖`) whose text includes:
    - `codex-managed: true`
    - `Only edit this page if this marker is present.`
  - if callout creation is unavailable, include a paragraph block containing `codex-managed: true` near the end.
- Before updating an existing page, fetch block children and verify the marker text is present. If missing, do not edit; create a new report page instead.

## Location routing (must follow)

Choose a parent location in Notion. Prefer an explicit parent URL from the user; otherwise, infer from project context.

1) If the user provides a Notion page/database URL or ID:
- use it as the parent.

2) Otherwise, try project hubs (known locations):
- GigaPlay hub: `https://www.notion.so/GigaPlay-2edf1d57cab880209415f67e7c65414f`
- GigaPlay reports (preferred when applicable): `https://www.notion.so/305f1d57cab8802eaac6d100dc242c5d`
- Mercantile hub: `https://www.notion.so/Mercantile-306f1d57cab8802a8b5cc2b513780742`
- Mercantile reports (preferred when applicable): `https://www.notion.so/306f1d57cab8808e9fafdbd0bb6c9d47`

3) Within a hub, try to file under an existing subpage (if present), using child-page enumeration and search + parent validation:
- prefer subpages named like: `Reports`, `Experiments`, `Research`, `Runs`, `Results`
- if no obvious subpage exists, create the report directly under the hub page.

4) If the correct hub/location is still unclear, fallback to personal notes:
- Ollie Notes (fallback): `https://www.notion.so/Ollie-Notes-21df1d57cab880e2af99fc37c6062b2e`

Ask at most one clarification question only if you cannot determine whether this is GigaPlay vs Mercantile and the fallback is not acceptable for the user.

## Scope and input handling

Take user inputs as the source of truth:
- If the user gives a directory, scan it recursively and use relevant files.
- If the user gives a file list, use that list.
- If both are mixed, combine both.
- If scope or intent is unclear, ask one short clarification question before writing.
- For remote content, either use content the user already surfaced locally or ask for a local copy/fetch command.

## Report behavior

- one concise but information-dense Notion page
- always start the page with a `Top Takeaways` section at the very top (before other sections)
- prefer using an explicit `## Top Takeaways` heading as the first line; top-level `#` may be normalized away in some create-page flows
- in `Top Takeaways`, begin with a one-line `question + answer status` statement (what question this report answers, and whether the available evidence answers it for this batch)
- for experiment/search reports, add an `Experiment Definition` section immediately after `Top Takeaways` and before visuals
- `Experiment Definition` must state in plain language: what question is being tested, what was searched/varied (search space), what was held fixed, how the search/randomization was sampled or assigned, why this search design was used, what evaluation environment(s) were used (including env variants/config names plus eval-only overrides and OOD/stress regimes when applicable), and whether this report answered the question for this batch (with a short why)
- when rerun-corrected batches supersede earlier batches, add an explicit provenance-lock statement in `Experiment Definition` naming the exact corrected `search_id`s used for primary metrics; treat pre-correction batches as context-only unless the user explicitly asks for direct rerun-vs-prior analysis
- when available from artifacts, explicitly report effective evaluation concurrency (for example `eval_num_learned_agents`) rather than inferring it from training/search settings
- when DR on/off appears, define what each means in the report context (for example randomized training settings vs fixed control settings)
- for quantitative/search reports, follow `Experiment Definition` with an `Executive Visual Snapshot` section (compact, high-signal visuals first)
- when an interpretation depends on causal isolation (for example \"axis X caused uplift\"), include both campaign-level deltas and an axis-isolated slice within a shared search distribution when available, and label any sample-size limits explicitly
- for paired mode comparisons, report pair-specific overlap counts for each comparison (not only the all-mode intersection) and bind each paired effect to its own overlap size
- when compared variants have non-trivial failure counts, add a selection-bias stress check (failure-rate by key buckets plus a sensitivity re-estimate on a less failure-prone slice)
- for 3+ mode comparisons, add an all-mode intersection robustness slice (for example triple-overlap) and confirm ranking/effect directions remain stable there
- in `Executive Visual Snapshot`, lead with primary performance comparisons first (for example DR on/off, return, profitable-episode share, and key OOD performance)
- when per-run time-series artifacts are available, include a compact `Run Spotlight` subsection with 1-3 explicitly selected runs (best/most interesting), in addition to aggregate views
- default run-spotlight selection order: highest out-of-sample Sharpe run; highest out-of-sample turnover run with positive out-of-sample PnL/return; one additional notable run (for example strongest return or unusual turnover/risk profile)
- for each spotlighted run, include equity-growth and turnover-over-time plots:
  - equity growth must be normalized to starting capital (`1.00x` at start; `2.00x` doubles capital; `0.50x` halves capital)
  - turnover over time should use intuitive units: `turns/day` preferred, `USD/day` acceptable when relative turnover time-series is unavailable
- use out-of-sample by default for run-spotlight charts; if in-sample is shown, label splits unambiguously
- if run-level time-series artifacts are unavailable, explicitly call out the artifact gap in limitations instead of silently omitting spotlights
- for Mercantile cluster-backed runs, verify run-level artifact availability by direct cluster access (read-only check/sync for the specific search ID) before declaring spotlight artifacts unavailable
- keep completion/failure information in the report, but de-emphasize it when reliability is not the central issue: prefer summary table + reliability section over the first/hero visual
- do not use completion/failure as a hero plot by default; only elevate failure visuals when reliability behavior materially changes interpretation
- for execution-intensity interpretation, prefer turnover metrics (`turns/day` and `USD/day` when available) over raw fill-count visuals
- if raw fill counts are included, keep them in supporting/appendix context unless the report is explicitly about fill mechanics
- include a `Definitions and Methodology` section for quantitative reports so metric meanings and calculations are explicit
- in `Definitions and Methodology`, define domain terms (for example OOD) specifically for the report context and include formulas for derived metrics (for example uplift)
- if OOD appears in `Top Takeaways` or early visuals, add a plain-language one-sentence OOD definition in `Top Takeaways` and a specific setup definition in `Experiment Definition`
- default to a distilled high-impact narrative: prioritize the most decision-relevant findings and remove low-signal sections/plots
- include bullets, tables, and visuals where they improve understanding
- default to plot-first presentation for quantitative results (tables are supporting detail, not the primary narrative)
- prefer high-signal visuals over noisy plots
- no hard visual cap, but normally keep to ~6-9 high-impact visuals; if more than 9 are useful, prioritize top-value visuals
- include caveats for missing data, incomplete runs, or skipped comparisons
- keep wording objective and fact-based
- do not include any section that is only process-oriented; focus on what was run, what changed, and what happened
- default to descriptive-only reporting (no recommendations/next-step plans). if the user explicitly requests prescriptive guidance, add a clearly labeled guidance section and keep every claim evidence-backed and numerically unchanged from verified artifacts
- do not include a table of contents block (`<table_of_contents/>`)
- when quantitative outcomes are available, include high-signal plots in the report (not tables-only) unless explicitly instructed otherwise
- for hyperparameter/search reports, include plots with aggregated outcomes across important search dimensions (for example learning rate, batch size, regularization, model-size/probability knobs) when data is available
- reliability emphasis must be proportional: if job failure rate is below the active concern threshold, mention it briefly under reliability/limitations rather than making it a central narrative point (unless evidence shows material bias)
- only elevate completion/failure visuals into top prominence when failure behavior materially changes interpretation of core performance conclusions
- for failure-mechanism claims, use retained forensics root-cause fields when available (for example `failed_run_forensics.json -> run_timing.error_type/error_message`) rather than artifact-wrapper labels alone

## Cross-project refinement defaults (must follow)

These defaults apply across all projects using this skill:
- optimize for reader impact density: concise wording, strongest findings first, and clear visual evidence
- keep reports scannable for busy readers: avoid long low-signal sections and repetitive charts
- maintain visual integration through the narrative (plot-first), but aggressively prune redundant visuals
- if user feedback asks for shorter reports, compress first by removing low-impact sections before removing required metrics

## Optional Claude-assisted drafting (when available and user wants it)

When the user explicitly wants Claude-style wording/visual structure, use Claude Code headless as a drafting aid, with Codex as final authority:
- use non-interactive mode and high reasoning: `claude -p --model opus --effort high`
- Codex owns data prep, tool calls, validation, and all Notion writes; Claude is draft-only
- do not ask Claude to infer missing numbers or invent results; pass only explicit evidence
- sanitize prompts before sending to Claude: remove local paths, hostnames, secrets, tokens, and private identifiers
- for non-trivial refinements, generate 2-3 concise variants and compare before applying
- when the user asks for clearer wording, prioritize plain-language definitions and explicit methodology/formulas over additional plot count
- always apply changes to the same canonical Codex-managed page (no new versions)
- after applying, immediately re-fetch the page and verify labels/units/legend requirements still hold

### Claude protocol for multi-agent report refinement (must follow when Claude is used)

1) Build an evidence packet first (before calling Claude):
- include only facts to be used: key metrics with units, assumptions, caveats, and section constraints
- include a compact claim map: `claim_id -> source artifact/table/line`

2) Prompt Claude with strict output boundaries:
- ask for wording/structure refinement only (not new analysis)
- require output to stay descriptive-only by default (no recommendations, no action plan) unless the user explicitly asked for prescriptive guidance
- require it to preserve section order constraints (`Top Takeaways` first, then required sections)
- ask for explicit placeholders when evidence is missing (for example `unit unavailable`)

Suggested prompt scaffold (fill in with current report context):
- role: "rewrite for clarity and impact density only; do not add new facts"
- hard constraints: required sections/order, descriptive-only default tone (unless explicitly overridden by user request), no local paths/hostnames
- evidence packet: compact fact list with units + claim map (`claim_id -> source`)
- output contract:
  - `variant_a`: concise rewrite
  - `variant_b`: concise rewrite with stronger plain-language definitions
  - `self_check`: list of any statements that may be unsupported by provided evidence

3) Run a Codex verification gate before Notion update:
- verify every quantitative claim in Claude output maps to evidence packet facts
- verify paired-difference direction/sign conventions explicitly (`A - B` labels match the computed sign)
- reject any new ungrounded claims, unit changes, sign flips, or scope drift
- verify no local paths/hostnames leaked
- verify required labels, units, legend clarity, and directional cues still hold

4) If Claude is unavailable or low quality:
- do not block report delivery; continue with Codex-only drafting and validation
- mention briefly in the final user update that Claude assistance was skipped or rejected

### Mercantile emphasis (must follow)

For Mercantile reports, `Top Takeaways` must explicitly cover both lenses:
- trader/quant/trading perspective:
  - implications for PnL, drawdown, risk, execution/runtime constraints, robustness, and deployability
- machine learning/deep learning perspective:
  - implications for generalization, model behavior, data/split effects, training/evaluation dynamics, and hyperparameter sensitivity

Keep this section factual and descriptive-only by default (no recommendations or action plans) unless the user explicitly requests prescriptive guidance.

Do not describe chart type unless needed.
Direction cues are strongly encouraged for key metrics. When applicable, include explicit cues like `(higher is better)` or `(lower is better)` in a title, axis label, legend label, or caption.

Avoid filesystem path leakage in report body. Use neutral labels like `input image 1`, `input image 2`, etc.

## Notion MCP workflow (must follow)

Use the local MCP server/tool namespace `notion-local` for all Notion operations.

1) Connectivity check before writes:
- Call `mcp__notion-local__API-get-self` once per task to confirm auth/workspace.
- `list_mcp_resources` may return `Method not found` on this server; do not treat that as failure if Notion API calls succeed.

2) Resolve the parent page:
- If the user provides a Notion URL/ID, extract/normalize the page ID and verify it with `mcp__notion-local__API-retrieve-a-page`.
- If choosing a subpage (Reports/Experiments/etc.), first list hub children with `mcp__notion-local__API-get-block-children` and prefer existing `child_page` entries.
- If enumeration is not enough, use `mcp__notion-local__API-post-search` for candidate discovery, then validate parent/location with `mcp__notion-local__API-retrieve-a-page` (and parent-chain checks).

3) Create the report page:
- Default to a single canonical page per experiment or experiment batch.
- Before creating, always derive a report identity from available evidence (for example: experiment/search/run IDs, batch label, date window, method/variant) and search for an existing Codex-managed report with the same identity.
- Use `mcp__notion-local__API-post-page` with `parent` set to the chosen parent `page_id` only when you are sure no matching Codex-managed report exists for that identity.
- Add/update body sections with `mcp__notion-local__API-patch-block-children` / `mcp__notion-local__API-update-a-block` as needed.
- Do not create a new page just because the title wording changed; update the existing canonical page for the same experiment/batch.
- Title pattern (match existing report pages when possible): `<YYYY-MM-DD> - <topic>`
- Content should follow the quality checklist below.
- Include the Codex marker callout at the end of the page content.

4) Update behavior:
- Refinement means improving the same page over time. Do not create new copies/versions like `v2`, `v3`, `copy`, or `final`.
- Always prefer updating an existing Codex-managed report page in-place.
- Keep exactly one canonical report per experiment or experiment batch in the target Reports location.
- If duplicates/older versions exist for the same experiment/batch, retain one canonical page and move non-canonical duplicates out of the Reports location (or archive/trash only with explicit user approval).
- If two pages reference the same underlying experiment batch/data, consolidate to one canonical report page and avoid splitting updates across both.
- Before deduplicating, verify same-data identity using concrete evidence (for example run/search IDs, run directory names, budget, variant grid, and key aggregate counts). If evidence shows different batches, keep both pages.
- Matching algorithm precedence:
1. Identity match: same experiment/search/run IDs or same explicit experiment batch scope (preferred over title matching).
2. Exact title match within the chosen parent location (or its hub scope) for `<YYYY-MM-DD> - <topic>`.
3. If no exact match and the user did not specify a date, pick the single best match by topic among recent reports (prefer the most recent date in the title).
- If multiple candidates remain, fetch each and pick the one that is Codex-managed and most semantically aligned to the user request (avoid splitting the narrative across pages).
- Fetch candidate page blocks via `mcp__notion-local__API-get-block-children` and only update a page if it contains the `codex-managed: true` marker (and preserve that marker on every update).
- If no matching Codex-managed page exists, create a new report page (and optionally link/mention the prior human-managed page without editing it).
- If it is unclear whether the request is the same experiment/batch versus a genuinely new one, ask one short clarification question before creating a new page.
- For large section rewrites, prefer heading-to-heading range updates (for example `## Decision...## Submission Guidance`) over bullet-level snippet replacements, because Notion normalization can make heavily formatted bullet snippets unreliable to match.

5) Output contract:
- Return the created/updated Notion page URL (or ID) as the primary artifact.

## Visuals and artifacts

- Prefer embedding summary tables and key numeric outcomes over screenshots, but include plots/images whenever they materially improve understanding.

### Visual and table labeling standards (must follow)

Every plot and table must be self-explanatory to a reader with no external context.

For plots:
- prefer plots over tables when both can communicate the same quantitative takeaway; keep tables for precision/detail support
- include a clear title stating what is being measured (metric + cohort/strategy/slice when relevant)
- label all axes with metric names and explicit units (for example `ms`, `s`, `%`, `bps`, `USD`, `contracts`)
- axis labels must be embedded directly in the plot definition itself (for example the `x-axis` / `y-axis` label text inside the chart block), not only in surrounding prose, titles, or captions
- include a clear legend with unambiguous series names; for a single-series plot, include an explicit series label in either legend or caption
- include a short caption/description stating what the plot shows and the key takeaway
- include directional guidance for the primary metric when applicable (for example `(higher is better)` / `(lower is better)`)
- for time-series, include the time basis/timezone and aggregation interval when relevant
- avoid unlabeled dual-axis visuals; if dual-axis is necessary, both axes must be explicitly labeled with units
- Mermaid `xychart-beta` compatibility guards:
  - do not use empty category labels in `x-axis` tick lists
  - for signed/negative-valued series, use `line` charts instead of `bar`
  - if category/bin density causes overlap, rebucket/reduce ticks and state that adjustment in the caption

For tables:
- include a clear table title
- use explicit column headers (no ambiguous abbreviations) and include units in header names where applicable
- include units for all numeric columns (in headers or clearly stated note)
- ensure derived fields/ratios are named clearly enough that a reader can infer what they represent
- include a short caption/description stating what the table summarizes and the key takeaway
- include directional guidance for key metrics when applicable (for example `lower is better` for latency/error columns)

If any required label/unit is unknown, do not guess:
- use a neutral placeholder like `unit unavailable` and call the gap out in limitations.

### Images and plots (must follow)

Hard constraints (learned empirically via Notion MCP fetch round-trips):
- Notion requires an externally fetchable `https://...` URL for reliable image rendering in `<image source="...">`.
- Notion sanitizes/strips `data:` URIs (for example base64 `data:image/png;base64,...`), and the image will not persist (on refetch the block becomes `<image source="">...`).
- `file:`, `blob:`, and other non-`https` sources are not reliable for rendering/persistence.
- URLs that require interactive auth (cookies, VPN-only, private repos) often will not render for Notion; prefer truly fetchable URLs.

Verification rule:
- After creating/updating a report that includes images, immediately fetch page blocks via `mcp__notion-local__API-get-block-children` and confirm each intended image block has a non-empty external `https://...` URL.
- If any image refetches as `<image source="">...` (blank source) or disappears, treat it as a failed embedding attempt and fall back to the next option below.

Strive relentlessly to embed images/plots in the Notion page. Try (in this order), stopping only when you have exhausted the options:

1) If an image already has a stable `https://...` URL:
- Embed it directly using an Image block:
  - use a Notion image block with an external URL (for example `image.external.url = "https://example.com/plot.png"`).

2) If you can generate a plot as a URL-rendered chart (no file upload needed):
- Use a URL-rendered chart provider (for example `quickchart.io`) to generate a plot image from a chart spec, then embed that `https://...` image URL as an external image block.
- Only use this when it preserves fidelity (do not distort results just to fit a chart spec).
- Treat third-party chart renderers as an explicit data-sharing decision: do not send real project data without explicit user approval.

3) If the image is local-only (no existing URL):
- You need an externally-resolvable `https://...` URL for Notion to render images reliably.
- Do not upload images to a public host without explicit user approval.
- Preferred hosting options (ask the user for one if not already available): a private artifact host that serves `https://...` URLs; a pre-signed `https://...` URL (ensure its expiry is acceptable for the report's expected lifetime); or a company-internal static host that Notion can fetch from without cookies/VPN.
- Then embed as an external image block and re-fetch to verify persistence.

4) Last resort (still "directly in Notion", but not via MCP-only image sources):
- If Playwright/browser automation is available and you have access to the Notion UI, upload/attach the local image directly into the report page in Notion (so Notion hosts it).
- Only do this on Codex-managed pages (marker present).
- Re-fetch the page after upload to ensure the hosted image renders and persists.

5) If embedding is still not possible with the available MCP/API surface:
- Do not block report creation.
- Include a short `Artifacts to attach` section with neutral labels (no absolute paths) and a sentence for what each plot/image demonstrates, so a human can attach files later.

## Proactive autonomy and knowledge compounding

- Default to autonomous execution: do not pause for confirmation between normal in-scope steps.
- Request user input only when absolutely necessary: ambiguous requirements, material tradeoffs, missing required data/access, or irreversible actions.
- If blocked by retries/fetch issues, attempt high-confidence fallbacks before escalation.
- Treat iterative execution as the default for non-trivial work; run adaptive loop passes.
- Keep looping until actual completion criteria are met: no actionable gaps remain, evidence is represented, and quality checks pass.
- Run `organise-docs` frequently during execution to capture durable decisions and learnings when scope changes.
- Create small checkpoint commits frequently with `git-commit` when checks are green and policy permits.
- Never squash commits; always use merge commits when integrating branches.
- Prefer simplification over added complexity: aggressively remove bloat, redundancy, and over-engineering while preserving correctness.

## Long-task checkpoint cadence

- For non-trivial report generation, use checkpoint cycles instead of single-pass handoffs.
- At meaningful milestones, rerun quality checks and confirm the generated Notion page still matches source evidence and privacy constraints.

## Reader-centric review loops (must follow)

Refinement is the default. Put yourself in the shoes of a busy reader who did not run the work and is deciding what to believe and what to do next.

Always do multiple rounds of review before considering a report "done":
- Pass 1 (structure): ensure `Top Takeaways` is the first section and then a crisp narrative arc: what question, what changed/was run, what evidence, what results, what conclusion.
- Pass 2 (reader questions): re-read top-to-bottom and answer the questions a skeptical reader will have inline (assumptions, baselines, comparisons, caveats, definitions, what could be wrong).
- Pass 3 (reader clarity): ensure the report is maximally clear for a reader and descriptive by default; remove unsolicited recommendations, next experiments, follow-up tasks, and decision directives; highlight the single most important outcome up front.

Mechanics:
- After each pass, update the same canonical Codex-managed report page in-place (do not fork versions).
- After updating, immediately re-fetch the page and re-read it as the reader to confirm the changes landed as intended (and that no paths/private details leaked).

## Quality checklist

- include: scope, what was run, what varied, measured outcomes, tables, top visuals, conclusions
- include `Top Takeaways` at the top of the page
- include an explicit `question + answer status` line near the top of `Top Takeaways`
- include an explicit `question + answer status + why` statement in `Experiment Definition`
- include explicit `what we searched over / how it was sampled or assigned / why this design` statements in `Experiment Definition`
- include explicit evaluation environment coverage in `Experiment Definition` (which env config/variant was used for evaluation, any eval-only overrides, and OOD/stress regimes when used)
- in Mercantile reports, ensure `Top Takeaways` has both trader/quant and ML/DL perspectives
- include an up-front summary of the single most important outcome in `Top Takeaways`
- for search-style reports, verify there are aggregated-dimension plots for important dimensions (or explicitly state why not available)
- when per-run time-series artifacts exist, verify there is a `Run Spotlight` section with 1-3 selected runs and both normalized equity-growth + turnover-over-time plots
- when run-level time-series artifacts are unavailable, verify that the limitations section explicitly states this gap
- verify every plot/table has clear title, axis/header labels, explicit units, and a short description
- verify axis labels are present directly in each plot block (not caption-only/title-only)
- verify each plot has a clear legend or explicit single-series label
- include directional cues (`higher is better`/`lower is better`) for key metrics when applicable
- include assumptions and limitations
- include missing-data caveats
- ensure reliability/failure commentary is proportional to impact; below-threshold failure rates should be brief unless materially biasing conclusions
- verify completion/failure is not a hero visual unless reliability is central to interpretation
- verify execution-intensity visuals use interpretable units (`turns/day`, optionally `USD/day`) rather than only raw fill counts
- verify the top of the report clearly states what the experiment/search is testing and what dimensions were searched
- verify DR on/off meaning is explicitly defined when used in comparisons
- verify `Experiment Definition` explicitly states `what/how/why` for the search design
- verify `Experiment Definition` explicitly states evaluation environment(s) and eval setup details
- verify methodology is explicit for derived metrics (for example uplift definitions/sign conventions and weighted means)
- if OOD or similar domain terms are used, verify they are defined concretely for the specific evaluation setup in this report
- verify no explicit local paths appear in narrative text
- verify quantitative sections are plot-first, with tables used as supporting detail
- keep content concise, dense, and focused on highest-impact findings
