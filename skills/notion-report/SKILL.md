---
name: notion-report
description: Generate a standalone, Notion-importable HTML report from freeform inputs and artifacts.
---

# Notion Report

Generate a single, self-contained HTML report that can be imported to Notion directly.

- no fixed input schema required
- no Python tooling required
- accept freeform inputs: notes, logs, tables, images, tables, artifacts, and run outputs
- output exactly one `.html` file by default
- keep output out of git by default
- hide local paths and hostnames in visible text
- define acronyms on first use in the report

## Scope and input handling

Take user inputs as the source of truth:
- If the user gives a directory, scan it recursively and use relevant files.
- If the user gives a file list, use that list.
- If both are mixed, combine both.
- If scope or intent is unclear, ask one short clarification question before writing.
- For remote content, either use content the user already surfaced locally or ask for a local copy/fetch command.

## Report behavior

- one concise but information-dense Notion-ready HTML page
- include bullets, tables, and visuals where they improve understanding
- prefer high-signal visuals over noisy plots
- no hard visual cap, but normally keep to ~10 or fewer; if more than 10 are useful, prioritize top-value visuals
- include caveats for missing data, incomplete runs, or skipped comparisons
- keep wording objective and fact-based
- do not include any section that is only process-oriented; focus on what was run, what changed, and what happened

Do not describe chart type unless needed.
Direction cues (`higher is better`, etc.) are optional and should be used only when they materially improve clarity; they can be included in a caption or heading.

Avoid filesystem path leakage in report body. Use neutral labels like `input image 1`, `input image 2`, etc.

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
- At meaningful milestones, rerun quality checks and confirm the generated HTML still matches source evidence and privacy constraints.

## Output contract

- produce one `.html` file, single page, self-contained
- use embedded images (`data:image/...;base64,...`) in the HTML
- default path: `${HOME}/Downloads/notion-reports/notion_report_<timestamp>.html`
- print the absolute output path at the end

## Minimal template

Use this shell flow to create the HTML:

```bash
OUT_DIR="${HOME}/Downloads/notion-reports"
TS="$(date +%Y%m%d_%H%M%S)"
OUT_HTML="$OUT_DIR/notion_report_${TS}.html"
mkdir -p "$OUT_DIR"

cat > "$OUT_HTML" <<'HTML'
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Notion Report</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif; line-height: 1.45; color: #111; }
    .page { max-width: 980px; margin: 0 auto; padding: 24px; }
    h1, h2, h3 { line-height: 1.2; }
    table { border-collapse: collapse; width: 100%; margin: 8px 0 16px; }
    th, td { border: 1px solid #e5e7eb; padding: 6px 8px; text-align: left; font-size: 0.95rem; }
    th { background: #f9fafb; }
    img { max-width: 100%; height: auto; display: block; margin: 8px 0; }
    p, li, td { white-space: pre-wrap; }
  </style>
</head>
<body>
  <div class="page">
    <!-- generated content -->
  </div>
</body>
</html>
HTML

printf '%s\n' "$OUT_HTML"
```

Base64 helper for a local image:

```bash
IMG_B64=$(base64 -w0 /path/to/image.png 2>/dev/null || base64 /path/to/image.png | tr -d '\n')
echo "<img src=\"data:image/png;base64,${IMG_B64}\" alt=\"input image 1\" />"
```

## Quality checklist

- include: scope, what was run, what varied, measured outcomes, tables, top visuals, conclusions
- include assumptions and limitations
- include missing-data caveats
- verify no explicit local paths appear in narrative text
- keep content concise and dense
