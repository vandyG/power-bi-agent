# Mobile Design

## Decision: do you need a mobile layout?

If the report will be opened in the Power BI mobile apps or in Teams on a phone — yes. Otherwise the desktop layout is auto-shrunk and reads poorly.

Set it explicitly via View → Mobile Layout in Power BI Desktop.

## Constraints

| Constraint | Value |
|---|---|
| Canvas | 320 × 568 px portrait (default phone) |
| Visuals per page | ≤4 |
| Touch target | ≥44 × 44 px |
| Font (body) | ≥12 pt |
| Font (KPI hero) | 24–32 pt |

## Layout pattern

```
┌─────────────────────┐
│ Title • Refresh     │
├─────────────────────┤
│      Hero KPI       │
├─────────────────────┤
│  Trend (line/bar)   │
├─────────────────────┤
│  Breakdown (bar)    │
├─────────────────────┤
│ [ View Full Report ]│
└─────────────────────┘
```

## What works

- Card / multi-row card visuals
- Horizontal bar with ≤7 categories
- Single-series line charts
- KPI visual

## What doesn't

- Matrices and tables (re-flow poorly, hard to scroll)
- Scatter and bubble charts
- Custom visuals not certified mobile-friendly
- Slicers with >10 items (use a dropdown, search-enabled)

## Filters

- Move filter pane to a separate page or behind a button — don't compete with content for vertical space.
- Default filters should match the most common phone use case (e.g., "today" + "my region").

## Cross-app behavior

- Test in the actual Power BI mobile app, not just the Desktop preview.
- Test landscape orientation if the audience rotates.
- For Teams: the report is rendered inside a Teams tab; verify on phone Teams as well as desktop Teams.
