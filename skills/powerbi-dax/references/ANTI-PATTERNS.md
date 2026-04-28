# DAX Anti-Patterns

Reject these and propose the corrected form. Each entry: symptom → why it's bad → fix.

## 1. `IFERROR` / `ISERROR` for safe division

```dax
-- BAD
Margin = IF(ISERROR([Profit] / [Sales]), BLANK(), [Profit] / [Sales])
```
Triggers exception machinery and double evaluation.
```dax
-- GOOD
Margin = DIVIDE([Profit], [Sales])
```

## 2. Coercing `BLANK()` to `0`

```dax
-- BAD
Sales = IF(ISBLANK(SUM(Sales[Amount])), 0, SUM(Sales[Amount]))
```
Forces totals to materialize for every empty cell, breaks PivotTable suppression and visual sparsity.
```dax
-- GOOD
Sales = SUM(Sales[Amount])
```

## 3. Repeated subexpression

```dax
-- BAD
Growth =
DIVIDE(
    [Sales] - CALCULATE([Sales], DATEADD('Date'[Date], -1, YEAR)),
    CALCULATE([Sales], DATEADD('Date'[Date], -1, YEAR))
)
```
Engine evaluates the prior-year branch twice.
```dax
-- GOOD
Growth =
VAR Prev = CALCULATE([Sales], DATEADD('Date'[Date], -1, YEAR))
RETURN DIVIDE([Sales] - Prev, Prev)
```

## 4. Nested `CALCULATE`

```dax
-- BAD
M = CALCULATE(CALCULATE(SUM(Sales[Amount]), Product[Cat]="A"), 'Date'[Year]=2025)
```
Two context modifications when one suffices.
```dax
-- GOOD
M = CALCULATE(SUM(Sales[Amount]), Product[Cat]="A", 'Date'[Year]=2025)
```

## 5. `FILTER(Table, …)` as a `CALCULATE` filter

```dax
-- BAD
M = CALCULATE([Sales], FILTER(Sales, Sales[Amount] > 100))
```
Forces a row-by-row scan of `Sales`.
```dax
-- GOOD
M = CALCULATE([Sales], Sales[Amount] > 100)
```
Use `FILTER` only when the predicate references a measure or needs row context (then prefer iterating a small dimension).

## 6. Calculated columns on large fact tables

```dax
-- BAD (calculated column on Sales with millions of rows)
Sales[FullName] = RELATED(Customer[FirstName]) & " " & RELATED(Customer[LastName])
```
Bloats model size, breaks compression. Push to Power Query or compute in the dimension.

## 7. Bidirectional cross-filter "just in case"

Avoid setting cross-filter to `Both` on relationships by default. It:
- creates ambiguous filter paths
- degrades performance
- can produce surprising results in matrix visuals.

When a measure genuinely needs filter to flow back, scope it locally:
```dax
Distinct Categories Sold =
CALCULATE(
    DISTINCTCOUNT(Product[Category]),
    CROSSFILTER(Sales[ProductKey], Product[ProductKey], BOTH)
)
```

## 8. Auto Date/Time tables

Disable the Power BI auto date/time hierarchies. They create one hidden date table per date column, balloon model size, and prevent fiscal calendars. Use a single marked `'Date'` dimension.

## 9. `VALUES()` to read a single selected value

```dax
-- BAD: errors when more than one
Sel = VALUES(Customer[CustomerKey])
```
```dax
-- GOOD
Sel = SELECTEDVALUE(Customer[CustomerKey], BLANK())
```

## 10. `EARLIER` for self-reference

`EARLIER` is rarely needed in modern DAX. Use `VAR` to capture row context:
```dax
-- BAD
Rank = COUNTROWS(FILTER(Sales, Sales[Amount] > EARLIER(Sales[Amount])))

-- GOOD (in a calculated column)
Rank =
VAR ThisAmount = Sales[Amount]
RETURN COUNTROWS(FILTER(Sales, Sales[Amount] > ThisAmount))
```
