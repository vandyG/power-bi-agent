# Layout Patterns

## Executive dashboard (single landing page)

```
┌────────────────────────────────────────────────────────────┐
│  Title • Period • Last refreshed                           │
├──────────┬──────────┬──────────┬──────────┬───────────────┤
│  KPI 1   │  KPI 2   │  KPI 3   │  KPI 4   │  KPI 5        │
├──────────┴──────────┴──────────┴──────────┴───────────────┤
│                                                            │
│   Primary trend chart (line)            Drilldown table    │
│                                                            │
├────────────────────────────────────────────────────────────┤
│  Secondary breakdown (bar) │ Geospatial │  Supporting KPI  │
└────────────────────────────────────────────────────────────┘
```

- Hero KPIs in the header, sized larger than other text.
- One narrative chart below the KPIs.
- Filters as a slim panel on the left or top.

## Analytical report

- Multiple pages, each answering one sub-question.
- Page navigation buttons in a sidebar.
- Drill-through to detail pages from any visual.
- Tooltip pages on visuals to add context without leaving the page.
- "Reset filters" button on each page using a bookmark.

## Operational report

- Action-oriented: status indicators, exception highlighting.
- Designed for repeated daily use → information dense but not cluttered.
- Big "what changed since yesterday" panel.
- Real-time refresh where possible; otherwise show "as of" timestamp prominently.

## Page header anatomy

| Element | Notes |
|---|---|
| Title | 18–24 pt, brand font |
| Subtitle / period | 12 pt, muted |
| Last refresh time | Driven by `MAX('Date'[Date])` or refresh metadata |
| Applied filters summary | A small text box with selected slicer values (use SELECTEDVALUES + UNICHAR(8226) bullets) |
| Reset button | Bookmark that clears slicers |

## Whitespace & alignment

- 24 px gutter between visual containers.
- Visuals share grid columns — never align them by eye.
- Use the Selection pane to lock visual positions; group related visuals.

## Visual containers

- Always set a meaningful title on every visual; if the title is redundant with the chart axis, hide it but keep alt text.
- Use border-bottom or subtle background to group sibling visuals; avoid heavy borders.
- Don't put a visual inside a visual (no transparent overlays of cards on charts unless deliberate and tested).
