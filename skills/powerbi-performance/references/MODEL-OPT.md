# Model Optimization

## Size = the lever that matters most

Power BI compresses columns independently using VertiPaq. The model size is dominated by **column dictionary size**, which is driven by **cardinality**, not row count.

Open VertiPaq Analyzer (DAX Studio → Advanced → View Metrics) and sort columns by size. Fix the top 3 first.

## High-impact reductions

| Action | Typical savings |
|---|---|
| Drop unused columns | 20–60% |
| Split DateTime → Date + Time-of-day (15-min bucket) | 50–90% on that column |
| Round decimals to needed precision | 30–70% |
| Replace text key with integer surrogate | 70–95% on the key |
| Replace GUID with integer surrogate | 80–95% |
| Disable Auto Date/Time | varies; can be huge for date-heavy models |

## Column-level rules

- **Keys**: integer, hidden, `summarizeBy: None`.
- **Dates**: `Date` type (not DateTime) unless time-of-day is reported on. Mark the date table.
- **Decimals**: prefer **Fixed Decimal** when ≤4 decimal places — better compression than Decimal Number.
- **Text**: limit length; consider extracting prefix/suffix.
- **Booleans**: `True`/`False` compresses to 1 bit; cheap.
- **Hidden**: hide every column the report doesn't show. Tooltips and legends only need the visible column.

## Storage mode strategy

| Scenario | Mode |
|---|---|
| Fact ≤ a few hundred million rows, daily refresh OK | Import |
| Fact > 1B rows or near-real-time | DirectQuery (with aggregations) |
| Mix of both | Composite, dimensions Dual, fact partitions Import + DirectQuery |
| Static reference data | Import always |

## Calculated columns

Rule: if it can be computed at the source or in Power Query, do it there. Only use a DAX calculated column when it depends on model relationships at evaluation time and cannot be pre-computed.

Calculated columns:
- compute on every refresh
- compress worse than imported columns (no dictionary opt across rows)
- block query folding for any column that depends on them

## Relationships

- One-to-many, single direction by default.
- Integer key columns on both sides.
- Set "Assume referential integrity" only when the warehouse guarantees it (improves DirectQuery performance).
- Hide foreign keys from report view.

## Aggregations (DirectQuery / large Import)

For frequent grain combinations (e.g., monthly × product category), define an aggregation table. Power BI auto-routes matching queries to the smaller, faster aggregation. Manage via Modeling → Manage aggregations.

## Incremental refresh

- Define `RangeStart`/`RangeEnd` parameters in Power Query.
- Filter the fact by these parameters; ensure the predicate **folds** (verify with Query Diagnostics).
- Configure incremental policy: archive (e.g., 5 years) + refresh window (e.g., 10 days).
- Optional: enable detect data changes column for partition skipping.

## Validation checklist

- [ ] Top 5 columns by size are all justified
- [ ] No DateTime where Date suffices
- [ ] No GUID/text relationship keys
- [ ] Auto Date/Time disabled
- [ ] All technical columns hidden
- [ ] Calculated columns < 10% of model size
- [ ] Star schema (no snowflakes unless justified)
- [ ] Single-direction cross-filter unless documented exception
