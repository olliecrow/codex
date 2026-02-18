---
name: notion-report
description: Create and maintain experiment/investigation reports directly in Notion via the Notion MCP server (automatic page creation/updates) from freeform inputs and artifacts. Use when the user wants reports created/edited/organized in Notion (no HTML or intermediate report formats).
---

# Notion Report

Create a report page directly in Notion (via MCP), filed under an appropriate project/workspace location.

- no fixed input schema required
- no fixed tooling required (Python optional for plots/visuals when available)
- accept freeform inputs: notes, logs, tables, images, tables, artifacts, and run outputs
- always work directly in Notion (create/add/edit pages); never generate HTML or other intermediate report formats
- hide local paths and hostnames in visible text
- define acronyms on first use in the report

## Codex-owned pages only (must follow)

Codex may only edit pages that Codex created. Never edit pages that were not created by Codex.

Implementation rule:
- Every page Codex creates MUST include a durable marker block near the end:
  - `<callout icon="🤖" color="gray_bg">\n\tcodex-managed: true\n\tOnly edit this page if this marker is present.\n</callout>`
- Before updating an existing page, fetch it and verify the marker is present. If missing, do not edit; create a new report page instead.

## Location routing (must follow)

Choose a parent location in Notion. Prefer an explicit parent URL from the user; otherwise, infer from project context.

1) If the user provides a Notion page/database URL or ID:
- use it as the parent.

2) Otherwise, try project hubs (known locations):
- GigaPlay hub: `https://www.notion.so/GigaPlay-2edf1d57cab880209415f67e7c65414f`
- GigaPlay reports (preferred when applicable): `https://www.notion.so/305f1d57cab8802eaac6d100dc242c5d`
- Mercantile hub: `https://www.notion.so/Mercantile-306f1d57cab8802a8b5cc2b513780742`
- Mercantile reports (preferred when applicable): `https://www.notion.so/306f1d57cab8808e9fafdbd0bb6c9d47`

3) Within a hub, try to file under an existing subpage (if present), using Notion search scoped to the hub page:
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
- for quantitative/search reports, follow with an `Executive Visual Snapshot` section immediately after `Top Takeaways` (compact, high-signal visuals first)
- default to a distilled high-impact narrative: prioritize the most decision-relevant findings and remove low-signal sections/plots
- include bullets, tables, and visuals where they improve understanding
- default to plot-first presentation for quantitative results (tables are supporting detail, not the primary narrative)
- prefer high-signal visuals over noisy plots
- no hard visual cap, but normally keep to ~6-9 high-impact visuals; if more than 9 are useful, prioritize top-value visuals
- include caveats for missing data, incomplete runs, or skipped comparisons
- keep wording objective and fact-based
- do not include any section that is only process-oriented; focus on what was run, what changed, and what happened
- do not include recommended next steps, follow-up tasks, or action plans; keep the report descriptive-only
- do not include a table of contents block (`<table_of_contents/>`)
- when quantitative outcomes are available, include high-signal plots in the report (not tables-only) unless explicitly instructed otherwise
- for hyperparameter/search reports, include plots with aggregated outcomes across important search dimensions (for example learning rate, batch size, regularization, model-size/probability knobs) when data is available
- reliability emphasis must be proportional: if job failure rate is below the active concern threshold, mention it briefly under reliability/limitations rather than making it a central narrative point (unless evidence shows material bias)

## Cross-project refinement defaults (must follow)

These defaults apply across all projects using this skill:
- optimize for reader impact density: concise wording, strongest findings first, and clear visual evidence
- keep reports scannable for busy readers: avoid long low-signal sections and repetitive charts
- maintain visual integration through the narrative (plot-first), but aggressively prune redundant visuals
- if user feedback asks for shorter reports, compress first by removing low-impact sections before removing required metrics

## Optional Claude-assisted drafting (when available and user wants it)

When the user explicitly wants Claude-style wording/visual structure, use Claude Code headless as an optional drafting aid:
- use non-interactive mode and high reasoning: `claude -p --model opus --effort high`
- for non-trivial refinements, generate multiple concise variants and compare before applying
- treat Claude output as a draft: validate all facts, units, and constraints before updating Notion
- always apply changes to the same canonical Codex-managed page (no new versions)
- after applying, immediately re-fetch the page and verify labels/units/legend requirements still hold

### Mercantile emphasis (must follow)

For Mercantile reports, `Top Takeaways` must explicitly cover both lenses:
- trader/quant/trading perspective:
  - implications for PnL, drawdown, risk, execution/runtime constraints, robustness, and deployability
- machine learning/deep learning perspective:
  - implications for generalization, model behavior, data/split effects, training/evaluation dynamics, and hyperparameter sensitivity

Keep this section factual and descriptive-only (no recommendations or action plans).

Do not describe chart type unless needed.
Direction cues are strongly encouraged for key metrics. When applicable, include explicit cues like `(higher is better)` or `(lower is better)` in a title, axis label, legend label, or caption.

Avoid filesystem path leakage in report body. Use neutral labels like `input image 1`, `input image 2`, etc.

## Notion MCP workflow (must follow)

1) Fetch the Notion markdown spec before writing content:
- Use `read_mcp_resource` with `server: notion` and `uri: notion://docs/enhanced-markdown-spec` so the generated page content uses valid Notion-flavored Markdown.

2) Resolve the parent page:
- Use `mcp__notion__notion-fetch` on the chosen hub/parent URL to obtain a `page_id`.
- If choosing a subpage (Reports/Experiments/etc.), use `mcp__notion__notion-search` with `page_url` scoped to the hub to find the best target subpage, then fetch it to get its `page_id`.

3) Create the report page:
- Default to a single canonical page per report. Before creating, always search for an existing matching Codex-managed report and update it in-place (see Update behavior).
- Use `mcp__notion__notion-create-pages` with `parent` set to the chosen parent `page_id` only when you are sure no matching Codex-managed report exists (or the user explicitly asked for a new report).
- Title pattern (match existing report pages when possible): `<YYYY-MM-DD> - <topic>`
- Content should follow the quality checklist below.
- Include the Codex marker callout at the end of the page content.

4) Update behavior:
- Refinement means improving the same page over time. Do not create new copies/versions like `v2`, `v3`, `copy`, or `final`.
- Always prefer updating an existing Codex-managed report page in-place.
- Keep exactly one canonical report per topic/date in the target Reports location.
- If duplicates/older versions exist for the same topic/date, retain one canonical page and move non-canonical duplicates out of the Reports location (or archive/trash only with explicit user approval).
- Matching algorithm (most to least preferred):
- Exact title match within the chosen parent location (or its hub scope) for `<YYYY-MM-DD> - <topic>`.
- If no exact match and the user did not specify a date, pick the single best match by topic among recent reports (prefer the most recent date in the title).
- If multiple candidates remain, fetch each and pick the one that is Codex-managed and most semantically aligned to the user request (avoid splitting the narrative across pages).
- Fetch the candidate page(s) and only update a page if it contains the `codex-managed: true` marker (and preserve that marker on every update).
- If no matching Codex-managed page exists, create a new report page (and optionally link/mention the prior human-managed page without editing it).

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
- After creating/updating a report that includes images, immediately `mcp__notion__notion-fetch` the page and confirm each intended image appears as `<image source="https://...">...`.
- If any image refetches as `<image source="">...` (blank source) or disappears, treat it as a failed embedding attempt and fall back to the next option below.

Strive relentlessly to embed images/plots in the Notion page. Try (in this order), stopping only when you have exhausted the options:

1) If an image already has a stable `https://...` URL:
- Embed it directly using an Image block:
  - `<image source="https://example.com/plot.png">caption</image>`

2) If you can generate a plot as a URL-rendered chart (no file upload needed):
- Use a URL-rendered chart provider (for example `quickchart.io`) to generate a plot image from a chart spec, then embed that `https://...` image URL via `<image ...>`.
- Only use this when it preserves fidelity (do not distort results just to fit a chart spec).
- Treat third-party chart renderers as an explicit data-sharing decision: do not send real project data without explicit user approval.

3) If the image is local-only (no existing URL):
- You need an externally-resolvable `https://...` URL for Notion to render images reliably.
- Do not upload images to a public host without explicit user approval.
- Preferred hosting options (ask the user for one if not already available): a private artifact host that serves `https://...` URLs; a pre-signed `https://...` URL (ensure its expiry is acceptable for the report's expected lifetime); or a company-internal static host that Notion can fetch from without cookies/VPN.
- Then embed via `<image source="https://...">caption</image>` and re-fetch to verify persistence.

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
- Pass 3 (reader clarity): ensure the report is maximally clear for a reader and strictly descriptive; remove recommendations, next experiments, follow-up tasks, and decision directives; highlight the single most important outcome up front.

Mechanics:
- After each pass, update the same canonical Codex-managed report page in-place (do not fork versions).
- After updating, immediately re-fetch the page and re-read it as the reader to confirm the changes landed as intended (and that no paths/private details leaked).

## Quality checklist

- include: scope, what was run, what varied, measured outcomes, tables, top visuals, conclusions
- include `Top Takeaways` at the top of the page
- in Mercantile reports, ensure `Top Takeaways` has both trader/quant and ML/DL perspectives
- include an up-front summary of the single most important outcome in `Top Takeaways`
- for search-style reports, verify there are aggregated-dimension plots for important dimensions (or explicitly state why not available)
- verify every plot/table has clear title, axis/header labels, explicit units, and a short description
- verify axis labels are present directly in each plot block (not caption-only/title-only)
- verify each plot has a clear legend or explicit single-series label
- include directional cues (`higher is better`/`lower is better`) for key metrics when applicable
- include assumptions and limitations
- include missing-data caveats
- ensure reliability/failure commentary is proportional to impact; below-threshold failure rates should be brief unless materially biasing conclusions
- verify no explicit local paths appear in narrative text
- verify quantitative sections are plot-first, with tables used as supporting detail
- keep content concise, dense, and focused on highest-impact findings
