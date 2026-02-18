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
- include bullets, tables, and visuals where they improve understanding
- prefer high-signal visuals over noisy plots
- no hard visual cap, but normally keep to ~10 or fewer; if more than 10 are useful, prioritize top-value visuals
- include caveats for missing data, incomplete runs, or skipped comparisons
- keep wording objective and fact-based
- do not include any section that is only process-oriented; focus on what was run, what changed, and what happened

Do not describe chart type unless needed.
Direction cues (`higher is better`, etc.) are optional and should be used only when they materially improve clarity; they can be included in a caption or heading.

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

## Quality checklist

- include: scope, what was run, what varied, measured outcomes, tables, top visuals, conclusions
- include assumptions and limitations
- include missing-data caveats
- verify no explicit local paths appear in narrative text
- keep content concise and dense
