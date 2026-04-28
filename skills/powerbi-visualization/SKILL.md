---
name: powerbi-visualization
description: "Power BI report and visualization design guidance. Use when the user asks to choose a chart type, redesign a page, improve report layout or readability, design for mobile, address accessibility, or build dashboards/operational/analytical reports. Couples chart-selection rules with performance-aware design and Microsoft Learn citations."
---

# Power BI Visualization

Design reports that communicate the data story clearly, perform well, and meet accessibility standards. Match the visual to the question, not to whoever has the loudest opinion.

## When to Use This Skill

- "Which chart should I use for…?"
- Report page layout / dashboard design
- Mobile or embedded scenarios
- Accessibility review (color contrast, screen reader, keyboard)
- Theme / color / typography decisions
- Building executive vs analytical vs operational reports

## Prerequisites

- **`microsoft-learn`** — chart guidance and accessibility checklists.
- **`powerbi-modeling-mcp`** — only if a measure or relationship change is required to support a redesign.

## Workflow

1. **Identify the question** the page must answer in one sentence. ("How are sales trending vs target by region?" — not "I need a sales report.")
2. **Identify the audience** (executive / analyst / operator) and **medium** (desktop / mobile / embedded / printed PDF).
3. **Pick the chart family** from the relationship type (see [CHART-SELECTION.md](references/CHART-SELECTION.md)).
4. **Lay out the page** following the patterns in [LAYOUT.md](references/LAYOUT.md).
5. **Validate accessibility** with the checklist in [ACCESSIBILITY.md](references/ACCESSIBILITY.md).
6. **Test on the target medium** — mobile preview, embedded host, or print to PDF.
7. **Performance pass** — use the report rules from `powerbi-performance/REPORT-OPT.md`.

## Quick chart selection

| Question shape | Default visual |
|---|---|
| Compare values across categories | Horizontal bar |
| Trend over time | Line (≤6 series) |
| Cumulative trend | Area |
| Composition (≤6 parts) | Stacked bar (preferred over pie) |
| Composition (hierarchical) | Treemap |
| Two-measure correlation | Scatter |
| Distribution | Histogram or box plot (built-in or AppSource certified) |
| Single KPI vs target | Card + bullet chart |
| Categorical sequence | Funnel / Sankey (certified custom) |

Pie / donut: only ≤5 slices and only when the "share of total" is the message.

## Layout rules

- One primary visual per page that answers the page question; everything else supports it.
- Z-pattern reading: top-left = title + key KPIs, working down-right.
- Whitespace > grid lines > borders, in that priority.
- Filter panel: top or right; never spread filters across the page.
- Sticky page header with title, last refresh time, applied filters summary.

## Color rules

- Use ≤2 brand colors + 1 accent + neutrals. Don't color-code categories that don't have semantic meaning.
- Reserve red/green for negative/positive deltas — never for arbitrary categories.
- Pair color with shape, icon, or label. Color must never be the **only** information channel.
- Theme via JSON (`base.json`) so every report stays consistent.

## Mobile

- Use the explicit Mobile Layout pane.
- 1 column, ≤4 visuals per page.
- Card visuals + simple bar/line charts only. No matrices, no scatter.
- Touch targets ≥44 px.

## Accessibility floor

- ≥4.5:1 contrast for text, ≥3:1 for graphical objects.
- Tab order set explicitly (Selection pane).
- Alt text on every visual.
- Title and category labels readable without hovering.
- Don't disable focus rings or default keyboard shortcuts.

See [ACCESSIBILITY.md](references/ACCESSIBILITY.md) for the full audit.

## Testing protocol

For every shipped report:
- [ ] Performance Analyzer baseline (page load <5 s)
- [ ] Mobile preview opens and is usable
- [ ] Color contrast checked with theme tool
- [ ] Tab order verified with keyboard only
- [ ] Tested in the actual delivery medium (Service, Embedded, Teams, etc.)

## Reference Files

- [CHART-SELECTION.md](references/CHART-SELECTION.md) — fuller chart taxonomy
- [LAYOUT.md](references/LAYOUT.md) — page templates by audience
- [ACCESSIBILITY.md](references/ACCESSIBILITY.md) — WCAG-aligned checklist
- [MOBILE.md](references/MOBILE.md) — mobile design patterns
