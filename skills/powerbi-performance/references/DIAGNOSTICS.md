# Performance Diagnostics

## Decision Tree: where is the time going?

Run Performance Analyzer in Desktop, click "Refresh visuals", and read the dominant bucket per visual.

```
DAX query >> 80% of total
  ├─ FE % > 50%  → DAX engine is the bottleneck
  │   ├─ many context transitions / row context  → rewrite measure with VAR; avoid CALCULATE in iterators
  │   ├─ FILTER on big fact                       → swap to column predicate
  │   └─ time intelligence in CALCULATE chain     → use calculation groups
  └─ SE % > 50%  → storage engine is the bottleneck
      ├─ Import: high-cardinality column          → reduce dictionary (split datetime, round decimals)
      ├─ Import: big materialization              → pre-aggregate in Power Query
      └─ DirectQuery: slow source                 → check folding, add aggs, source indexes

Visual display >> 50%
  ├─ many marks (1k+ data points)                  → use top-N + drillthrough
  ├─ custom visual                                 → swap to certified built-in
  └─ matrix with totals everywhere                 → disable totals you don't need

Other (network/render) high
  ├─ Power BI Service in remote region             → check user/datacenter geography
  ├─ embedded scenario                             → confirm token, check browser console
  └─ slow gateway                                  → see gateway logs / parallelism
```

## Tool Cheatsheet

| Tool | What it tells you | When to reach for it |
|---|---|---|
| **Performance Analyzer** (Desktop) | Per-visual ms breakdown (DAX, display, other) | Always start here |
| **DAX Studio — Server Timings** | FE/SE split, scan count, materialized rows, query plan | Whenever DAX query > a few hundred ms |
| **DAX Studio — VertiPaq Analyzer** | Per-column dictionary size, hierarchy size, total table size | Reducing model size, picking which column to fix |
| **Power Query — Query Diagnostics** | Whether each step folds; per-step duration | DirectQuery latency, refresh slowness |
| **`model_operations(GetStats)`** (MCP) | Table sizes, row counts, partitions | Quick sanity check from inside the agent |
| **Fabric Capacity Metrics App** | CU(s), throttling, refresh impact | Capacity-level questions |
| **Azure Monitor / Log Analytics** | Long-term query trends, error rates | Production datasets with diagnostic logging |

## Useful KQL queries (Log Analytics)

```kusto
// Average DAX query duration per dataset, last 7 days
PowerBIDatasetsWorkspace
| where TimeGenerated > ago(7d)
| where OperationName == "QueryEnd"
| summarize avg(DurationMs), p95=percentile(DurationMs, 95), count() by ArtifactName
| order by p95 desc
```

```kusto
// Slowest queries in last 24h
PowerBIDatasetsWorkspace
| where TimeGenerated > ago(1d)
| where OperationName == "QueryEnd"
| top 20 by DurationMs desc
| project TimeGenerated, ArtifactName, ExecutingUser, DurationMs, CpuTimeMs, ApplicationName
```

```kusto
// Refresh duration trend
PowerBIDatasetsWorkspace
| where TimeGenerated > ago(30d)
| where OperationName == "RefreshEnd"
| summarize avg(DurationMs), max(DurationMs) by bin(TimeGenerated, 1d), ArtifactName
```

## KPI Thresholds (defaults; tune to your audience)

| Metric | Target | Warn | Fail |
|---|---|---|---|
| Page load | <3 s | 3–10 s | >10 s |
| Visual interaction | <1 s | 1–3 s | >3 s |
| DAX query (P95) | <2 s | 2–10 s | >10 s |
| Refresh duration | within window | within window + 25% | exceeds window |
| Capacity CPU (sustained) | <70% | 70–85% | >85% |
| Memory headroom | >25% | 10–25% | <10% |
