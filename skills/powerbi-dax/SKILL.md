---
name: powerbi-dax
description: "Power BI DAX assistant for authoring, optimizing, and debugging DAX measures, calculated columns, and queries. Use when the user asks to write or improve DAX, fix slow measures, work with time intelligence, calculation groups, variables, context transitions, or anti-patterns. Always grounds advice in current Microsoft Learn DAX documentation and validates suggestions against the live model when one is connected."
---

# Power BI DAX

Author and optimize DAX following Microsoft's official guidance. Prefer correctness, then performance, then readability — in that order, but iterate until all three are satisfied.

## When to Use This Skill

- Writing a new measure or calculated column
- Debugging a wrong-result or slow DAX expression
- Time intelligence (YTD, YoY, rolling averages, fiscal calendars)
- Calculation groups, field parameters, and dynamic format strings
- Translating business requirements into DAX patterns
- Performing a DAX-only code review

## Prerequisites

- **`powerbi-modeling-mcp`** — required to inspect the model and validate measures. Use `dax_query_operations(operation: "Validate")` and `Execute` for testing.
- **`microsoft-learn`** — recommended for DAX function semantics, new patterns, and edge cases.

## Workflow

### 1. Establish Context
```
1. measure_operations(operation: "List")           # see what already exists
2. table_operations(operation: "List")             # know fact vs dimension
3. relationship_operations(operation: "List")      # know filter propagation
4. If unfamiliar function or pattern: microsoft_docs_search
```

### 2. Author / Review
Apply the rules in [PATTERNS.md](references/PATTERNS.md). Reject anti-patterns from [ANTI-PATTERNS.md](references/ANTI-PATTERNS.md) and propose the corrected form.

### 3. Validate
```
dax_query_operations(operation: "Validate", expression: "<the new DAX>")
```
Then run a small probing query:
```
dax_query_operations(
  operation: "Execute",
  query: "EVALUATE ROW(\"Result\", [<Measure>])"
)
```

### 4. Persist
Use `measure_operations(operation: "Create" | "Update")` with `description` and `formatString` populated.

## Hard Rules

| Rule | Why |
|---|---|
| Always fully qualify columns: `Sales[Amount]` | Disambiguates row vs filter context |
| Never qualify measures: `[Total Sales]` not `Sales[Total Sales]` | Convention; breaks if measure moves |
| Use `VAR` for any expression evaluated more than once | Avoids re-evaluation; aids readability |
| `DIVIDE(n, d, alt?)` — never `n / d` | Safe BLANK on zero denominator |
| Preserve `BLANK()` — don't coerce to 0 | Better visual aggregation behavior |
| One `CALCULATE` with multiple filters > nested `CALCULATE` | Engine optimizes single context modification |
| Avoid `FILTER(Table, …)` as a `CALCULATE` filter when a column predicate works | `Sales[Amount] > 100` is faster than `FILTER(Sales, Sales[Amount] > 100)` |
| Use `KEEPFILTERS` when intersecting filters; default `CALCULATE` filter behavior is overwrite | Prevents subtle wrong-results in matrix visuals |

## Quick Patterns

See [PATTERNS.md](references/PATTERNS.md) for the full library.

```dax
// Safe ratio
Margin % = DIVIDE([Gross Profit], [Total Sales])

// YoY with VAR
Sales YoY % =
VAR Curr = [Total Sales]
VAR Prev = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))
RETURN DIVIDE(Curr - Prev, Prev)

// Top-N filter with KEEPFILTERS
Top 5 Customer Sales =
CALCULATE(
    [Total Sales],
    KEEPFILTERS(
        TOPN(5, ALLSELECTED(Customer[CustomerKey]), [Total Sales])
    )
)
```

## Optimizer Mode (when asked to "optimize this DAX")

For each input formula, produce four sections in this order:

1. **Diagnosis** — list the specific issues (repeated calls, FILTER misuse, context transitions in iterators, calculated-column-in-large-table, etc.).
2. **Optimized formula** — single fenced ` ```dax ` block, formatted with one statement per line.
3. **Why each change matters** — bullet per change, tying it to a Microsoft Learn DAX topic when relevant.
4. **How to verify** — a concrete `dax_query_operations(operation: "Execute", query: "EVALUATE …")` call that reproduces a representative result before/after.

## Calculation Groups

Use calculation groups for time-intelligence variants (`Current`, `YTD`, `QTD`, `PY`, `PY YTD`, `YoY %`) instead of duplicating measures. See [PATTERNS.md](references/PATTERNS.md#calculation-groups). Create with:
```
calculation_group_operations(operation: "Create", definitions: [...])
```

## Output Conventions

- Tag fences with `dax`.
- One blank line between top-level statements (`VAR`, `RETURN`).
- Keep variable names in PascalCase, descriptive.
- For new measures, always supply `formatString` (`"$#,##0"`, `"0.0%"`, `"#,##0"` etc.) and `description`.
