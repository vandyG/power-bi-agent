---
name: powerbi-performance
description: "Diagnose and resolve Power BI performance issues across models, DAX queries, reports, refresh, and capacity. Use when the user reports a slow report or visual, refresh failures or timeouts, high capacity utilization, DirectQuery latency, or asks for a Performance Analyzer / DAX Studio review. Produces a structured diagnosis with reproducible measurements before recommending fixes, and grounds advice in Microsoft Learn performance documentation."
---

# Power BI Performance

Apply a measure-first methodology: never recommend a fix without a baseline number. Reuse the diagnostic toolkit before reaching for guesses.

## When to Use This Skill

- "Report is slow" / "page takes >10 s to load"
- Visual or slicer interactions feel laggy
- Refresh failures, timeouts, or unexpected refresh duration growth
- DirectQuery / composite model query latency
- Premium/Fabric capacity at sustained high CPU or memory
- Asks involving Performance Analyzer, DAX Studio, server timings, VertiPaq Analyzer

## Prerequisites

- **`powerbi-modeling-mcp`** — required: `model_operations(operation: "GetStats")`, `dax_query_operations` for DAX timing.
- **`microsoft-learn`** — required: ground every recommendation in the latest "Optimization guide for Power BI" / "DAX query performance" pages.

## Diagnostic Workflow

### 1. Define the symptom precisely
Capture: **what** is slow, **where** (which page/visual), **when** (always vs intermittent), **who** (one user vs all), and the **target** (e.g., page load <5 s).

### 2. Establish the baseline
| Layer | Tool | Metric |
|---|---|---|
| Visual | Performance Analyzer (Desktop) | DAX query (ms), visual display (ms), other (ms) |
| DAX query | DAX Studio | Total, FE %, SE %, scans, materialized rows |
| Model | `model_operations(GetStats)` + VertiPaq Analyzer | Table size, column cardinality, dictionary size |
| Refresh | Refresh History / Profiler | Step durations, peak memory |
| Capacity | Fabric Capacity Metrics App | CU(s), throttling events |

### 3. Localize
See [DIAGNOSTICS.md](references/DIAGNOSTICS.md) for the decision tree that maps the dominant time bucket (FE, SE, visual, network) to a fix family.

### 4. Apply the smallest fix that works
Prefer DAX rewrites and visual reductions over capacity scaling.

### 5. Re-measure
Repeat step 2 and report before/after numbers.

## Top Fixes by Layer

### Model
- Drop unused columns (vertical slicing) — each high-cardinality text column you remove saves more than reducing rows.
- Replace text/datetime keys with integer surrogates.
- Disable Auto Date/Time. Use a single marked `'Date'` dimension.
- Move calculated columns off large fact tables — compute in Power Query or source.
- Set unsummarizable columns to `summarizeBy: "None"`.

### DAX
- See `powerbi-dax` skill, especially [ANTI-PATTERNS.md](../powerbi-dax/references/ANTI-PATTERNS.md).
- Add `VAR` to cache repeated subexpressions.
- Replace `FILTER(BigTable, …)` with column predicates.
- Replace bidirectional relationships with `CROSSFILTER(...)` scoped per measure.
- Push iterators down to dimensions, not facts.

### Report
- ≤ 6–8 visuals per page. Use bookmarks/tabs/drillthrough for "more".
- Apply page-level filters early.
- Disable cross-highlighting on visuals where it isn't useful (Format → Edit interactions).
- Replace high-cardinality slicers (>1 k items) with search-enabled dropdowns or hierarchy slicers.
- For matrices: limit row count, disable totals you don't need.

### DirectQuery / Composite
- Ensure query folding (Query Diagnostics — last step should fold).
- Add user-defined aggregations for frequent grain combinations.
- Make dimensions Dual storage; keep facts DirectQuery.
- Keep measures simple — no `EARLIER`, no large iterators.
- Push complex transformations to source views/materialized views.

### Refresh
- Enable incremental refresh on date-partitioned facts.
- Reduce parallelism if hitting source contention; increase if CPU is idle.
- Move heavy M transformations to source SQL.
- Disable "Include in report refresh" on staging queries.

### Capacity (Premium / Fabric)
- Use Capacity Metrics App to find the offending dataset and time of day.
- Reschedule refreshes off-peak.
- Consider scale-out read replicas for highly concurrent reports.
- Right-size only after model and DAX are clean — capacity rarely fixes a bad model.

## Reference Files

- [DIAGNOSTICS.md](references/DIAGNOSTICS.md) — decision tree and tool cheatsheet
- [MODEL-OPT.md](references/MODEL-OPT.md) — model size and shape fixes
- [REPORT-OPT.md](references/REPORT-OPT.md) — visual and interaction tuning
- [MONITORING.md](references/MONITORING.md) — KQL queries, alerts, KPI thresholds

## Reporting Format

When delivering a diagnosis, structure it as:

1. **Symptom & target** (1 line)
2. **Baseline measurements** (table with the metrics from step 2)
3. **Root cause** (1 paragraph + which time bucket dominated)
4. **Fixes applied** (numbered, each with the exact change)
5. **Post-fix measurements** (same table as baseline)
6. **Citations** (Microsoft Learn URLs)
