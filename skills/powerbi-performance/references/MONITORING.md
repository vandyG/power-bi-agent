# Monitoring

## Production datasets — checklist

- [ ] Diagnostic logs sent to Log Analytics (Azure portal → workspace → Diagnostic settings)
- [ ] Refresh failure email subscription enabled
- [ ] Capacity Metrics App pinned for the relevant Premium/Fabric capacity
- [ ] Alert rules for: refresh failure, P95 query > N seconds, capacity throttling
- [ ] Performance baseline screenshot stored alongside the .pbix

## Alert thresholds (starting points)

| Signal | Threshold | Action |
|---|---|---|
| Refresh failure | 1 occurrence | page on-call |
| Refresh duration | > 1.5× rolling 30-day avg | warn |
| P95 DAX query | > 10 s for 1h | warn |
| Capacity CPU | > 80% for 30 min | warn |
| Capacity throttling event | any | warn |

## KQL — saved queries

```kusto
// 1. Daily query volume + average duration
PowerBIDatasetsWorkspace
| where OperationName == "QueryEnd"
| summarize Queries=count(), AvgMs=avg(DurationMs), P95Ms=percentile(DurationMs, 95)
    by bin(TimeGenerated, 1d), ArtifactName
| order by TimeGenerated desc
```

```kusto
// 2. Top users by query volume
PowerBIDatasetsWorkspace
| where OperationName == "QueryEnd"
| where TimeGenerated > ago(7d)
| summarize Queries=count(), AvgMs=avg(DurationMs) by ExecutingUser, ArtifactName
| top 25 by Queries desc
```

```kusto
// 3. Refresh history with status
PowerBIDatasetsWorkspace
| where OperationName == "RefreshEnd"
| project TimeGenerated, ArtifactName, DurationMs, Status, OperationDetailName
| order by TimeGenerated desc
```

```kusto
// 4. DirectQuery latency outliers
PowerBIDatasetsWorkspace
| where OperationName == "QueryEnd"
| where TimeGenerated > ago(1d)
| extend DqMs = toint(parse_json(Metadata).directQueryTotalTimeMs)
| where DqMs > 5000
| project TimeGenerated, ArtifactName, DurationMs, DqMs, XmlaRequestId
```

## Capacity Metrics App — what to look at

1. **Items by CU(s)** — which dataset/report consumes the capacity.
2. **Throttling** — any minutes in the red? If yes, you're paying interactive latency cost during refresh windows.
3. **Background vs Interactive** — refresh shouldn't dominate interactive hours.
4. **Memory by item** — datasets approaching the per-item memory ceiling will eviction-thrash.

## On regression

When users report "it was fast yesterday":
1. Compare today's P95 to last week's via query #1.
2. Check refresh duration trend (query #3) — did the model size jump?
3. Check capacity throttling events.
4. Diff the .pbix against the last known-good version (Power BI Desktop's "Compare" feature, or version control on the .pbip / TMDL).
