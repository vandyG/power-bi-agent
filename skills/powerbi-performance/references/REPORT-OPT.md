# Report Optimization

## Visuals per page

Hard limit: **6–8 visuals per page**. Each visual is at least one DAX query. More visuals = more parallel queries competing for the same engine threads.

When the page "needs" more:
- Use bookmarks to swap visual sets in place
- Use tabs (page navigation) for related views
- Use drillthrough for detail
- Use tooltip pages for hover-only context

## Slicers and filters

- Apply filters early — page-level or report-level — so visuals start from a smaller universe.
- High-cardinality slicers (>1 000 items) → use the **dropdown** style with search, not the list style.
- Hierarchy slicer for date/region trees.
- Avoid slicers that have no semantic relationship to most visuals on the page (they still trigger query refresh on selection).

## Cross-filtering / Edit interactions

By default, every visual filters every other visual on the page. This is rarely all desirable.

- Format → Edit interactions → set unrelated visuals to **None** or **Highlight**.
- KPI cards usually shouldn't be cross-filtered by detail visuals.
- Big matrices can be set to ignore most slicers if they're for reference data.

## Matrix / Table tuning

- Pre-sort by the column users care about; don't rely on visual-level sort.
- Disable Subtotals/Totals for rows or columns where they aren't read.
- Limit the row count via top-N filter; provide drill-through for full detail.
- Avoid conditional formatting that calls a measure not already in the visual — it doubles queries.

## Custom visuals

- Prefer **Microsoft-certified** custom visuals only.
- Each non-certified visual is an independent perf risk and a security concern (network access).
- Test rendering with realistic data volumes before adopting.

## Mobile layout

- Set explicit mobile layouts on dashboards intended for phones.
- Prefer KPI cards and simple bar/column charts.
- Keep ≤4 visuals per mobile page.

## Theme

- Define a JSON theme (corporate colors, fonts, default visual styles) once. Avoids per-visual styling that bloats the report file and slows authoring.

## Performance Analyzer-driven tuning loop

```
1. Open Performance Analyzer → Start recording
2. Refresh visuals
3. Sort by Total duration desc
4. For top 1–3 offenders:
     - copy the DAX query (Performance Analyzer → "Copy query")
     - run it in DAX Studio with Server Timings
     - apply the appropriate fix (DAX rewrite, model fix, or visual fix)
5. Stop / Restart recording → confirm improvement
```

## Embedded scenarios

- Pre-load the access token (don't fetch on every visual).
- Use `models.LayoutType.Custom` and pre-size visuals to avoid re-flow.
- Use `setSlicers` API to push initial filters instead of letting visuals query first then filter.
