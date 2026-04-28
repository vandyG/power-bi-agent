# DAX Pattern Library

Curated, performance-aware DAX patterns. All patterns assume a star-schema model with a marked `'Date'` dimension. Cross-reference Microsoft Learn before adapting to unusual models.

## Aggregations

```dax
Total Sales        = SUM(Sales[Amount])
Order Count        = COUNTROWS(Sales)
Distinct Customers = DISTINCTCOUNT(Sales[CustomerKey])
Avg Order Value    = DIVIDE([Total Sales], [Order Count])
```

Prefer `COUNTROWS` over `COUNT(column)` when no specific column is needed — fewer scans.

## Time Intelligence

```dax
YTD Sales        = TOTALYTD([Total Sales], 'Date'[Date])
MTD Sales        = TOTALMTD([Total Sales], 'Date'[Date])
QTD Sales        = TOTALQTD([Total Sales], 'Date'[Date])
PY Sales         = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))
PY YTD Sales     = CALCULATE([YTD Sales], SAMEPERIODLASTYEAR('Date'[Date]))

Sales 3M Rolling =
VAR EndDate   = MAX('Date'[Date])
VAR StartDate = EDATE(EndDate, -2)
RETURN
CALCULATE(
    [Total Sales],
    DATESBETWEEN('Date'[Date], StartDate, EndDate)
)
```

## Year-over-Year

```dax
Sales YoY $ =
VAR Curr = [Total Sales]
VAR Prev = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))
RETURN Curr - Prev

Sales YoY % =
VAR Curr = [Total Sales]
VAR Prev = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))
RETURN DIVIDE(Curr - Prev, Prev)
```

## Ratios over a Total

```dax
Sales % of All Products =
DIVIDE([Total Sales], CALCULATE([Total Sales], REMOVEFILTERS(Product)))

Sales % of Visible Products =
DIVIDE([Total Sales], CALCULATE([Total Sales], ALLSELECTED(Product)))
```

`REMOVEFILTERS` ignores slicers (true global total). `ALLSELECTED` honors the user's slicer context.

## Top-N

```dax
Top 5 Customers Sales =
CALCULATE(
    [Total Sales],
    KEEPFILTERS(TOPN(5, ALLSELECTED(Customer[CustomerKey]), [Total Sales]))
)
```

## Role-Playing Dates

```dax
Sales by Ship Date =
CALCULATE([Total Sales], USERELATIONSHIP(Sales[ShipDate], 'Date'[Date]))
```

## Snapshot / Semi-Additive

```dax
Closing Inventory =
CALCULATE(SUM(Inventory[Qty]), LASTNONBLANK('Date'[Date], [Total Sales]))
```

## Calculation Groups

Define one calculation group `'Time Intelligence'` with calculation items. Each item modifies the selected base measure:

```dax
-- Calculation item: Current
SELECTEDMEASURE()

-- Calculation item: YTD
CALCULATE(SELECTEDMEASURE(), DATESYTD('Date'[Date]))

-- Calculation item: PY
CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))

-- Calculation item: YoY %
VAR Curr = SELECTEDMEASURE()
VAR Prev = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
RETURN DIVIDE(Curr - Prev, Prev)
```

Then a single base measure (`[Total Sales]`) plus the calc group replaces dozens of explicit time-intelligence measures.

## Dynamic Format Strings

Calculation items can carry a `formatStringDefinition` so the visual format adapts to the selected item (e.g., `0.0%` for `YoY %`, `$#,##0` for `Current`). Use this instead of separate `% Change` measures.

## Defensive Patterns

```dax
-- Selected single value or fallback
Selected Currency =
SELECTEDVALUE(Currency[Code], "USD")

-- Existence check before LOOKUPVALUE
Manager Region =
VAR User = USERPRINCIPALNAME()
RETURN
COALESCE(
    LOOKUPVALUE('User Region'[Region], 'User Region'[Email], User),
    "Unassigned"
)
```

## Iterator Performance

```dax
-- BAD: row-by-row context transition over large fact
Sales Cost =
SUMX(Sales, RELATED(Product[UnitCost]) * Sales[Qty])

-- GOOD: pre-compute in Power Query → SUM is then a column scan
Sales Cost = SUM(Sales[ExtendedCost])
```

If you must iterate, minimize what flows through `RELATED` and avoid `CALCULATE` inside `SUMX` when a plain expression suffices.
