---
name: notion-report
description: Create an experiment/investigation report directly in Notion via the Notion MCP server (automatic page creation) from freeform inputs and artifacts. Use when the user wants a Notion report created and filed in the right workspace location (no HTML import step).
---

# Notion Report

Create a report page directly in Notion (via MCP), filed under an appropriate project/workspace location.

- no fixed input schema required
- no Python tooling required
- accept freeform inputs: notes, logs, tables, images, tables, artifacts, and run outputs
- create a Notion page automatically by default (no HTML import)
- hide local paths and hostnames in visible text
- define acronyms on first use in the report

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

Ask at most one clarification question only if you cannot determine which hub/location is correct.

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
- Read the MCP resource `notion://docs/enhanced-markdown-spec` so the generated page content uses valid Notion-flavored Markdown.

2) Resolve the parent page:
- Use `mcp__notion__notion-fetch` on the chosen hub/parent URL to obtain a `page_id`.
- If choosing a subpage (Reports/Experiments/etc.), use `mcp__notion__notion-search` with `page_url` scoped to the hub to find the best target subpage, then fetch it to get its `page_id`.

3) Create the report page:
- Use `mcp__notion__notion-create-pages` with `parent` set to the chosen parent `page_id`.
- Title pattern (adapt as needed): `<Project> report: <topic> (<YYYY-MM-DD>)`
- Content should follow the quality checklist below.

4) Output contract:
- Return the created Notion page URL (or ID) as the primary artifact.
- Do not generate an HTML file unless the user explicitly asks for an offline/importable report.

## Visuals and artifacts

- Prefer embedding summary tables and key numeric outcomes over screenshots.
- If you cannot include local images directly in Notion via the available markdown/API surface, do not block. Instead:
  - include captions and what the image demonstrates
  - include a short `Artifacts` section with neutral labels (no absolute paths) so a human can attach files later if desired

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
