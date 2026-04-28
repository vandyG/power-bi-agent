---
name: powerbi-sql
description: "Convert a SQL file to a PowerBI M Sql.Database() query expression. Use when: generating PowerBI query from SQL file; wrapping SQL in Sql.Database(); creating M formula for Power Query; converting .sql to PowerBI; exporting SQL to Power BI data source."
argument-hint: "Optional: path to .sql file (defaults to current file)"
---

# PowerBI SQL Converter

Wraps a SQL file's content in a PowerBI M `Sql.Database()` expression, replacing newlines with `#(lf)` as required by Power Query.

## When to Use

- You have a `.sql` file and need the equivalent PowerBI M formula
- You are building a Power Query data source and need to embed a SQL query
- You need to copy a query into the Power BI query editor's Advanced Editor

## Output Format

```
= Sql.Database("<server>", "<database>", [Query="<sql with #(lf) line breaks>"])
```

## Procedure

### Step 1 — Identify the SQL file

Use the currently open `.sql` file, or the path provided as the skill argument.

### Step 2 — Gather connection details

Ask the user for:
1. **Server** — the SQL Server hostname/instance (e.g. `datamarts.PROD.isnforest.com\datamarts`)
2. **Database** — the database name (e.g. `DMAnalytics`)

If the user supplied these as arguments or they are visible in conversation context, skip asking.

### Step 3 — Run the conversion script

```bash
python3 ~/.copilot/skills/powerbi-sql/scripts/to_powerbi.py "<file>" --server "<server>" --database "<database>"
```

Or pipe the file via stdin:

```bash
cat "<file>" | python3 ~/.copilot/skills/powerbi-sql/scripts/to_powerbi.py --server "<server>" --database "<database>"
```

### Step 4 — Return the result

Present the full `= Sql.Database(...)` expression in a code block so the user can copy it directly into Power BI's Advanced Editor.

## Transformation Rules

| Input | Output |
|-------|--------|
| Newline (`\n`) | `#(lf)` |
| Trailing newline | Stripped before escaping |
| SQL content | Embedded verbatim (no other escaping needed for standard SQL) |

## Example

**Input** (`breaches.sql`):
```sql
SET NOCOUNT ON;
SELECT * FROM dm.MyTable
```

**Command**:
```bash
python3 ~/.copilot/skills/powerbi-sql/scripts/to_powerbi.py breaches.sql \
  --server "datamarts.PROD.isnforest.com\datamarts" \
  --database "DMAnalytics"
```

**Output**:
```
= Sql.Database("datamarts.PROD.isnforest.com\datamarts", "DMAnalytics", [Query="SET NOCOUNT ON;#(lf)SELECT * FROM dm.MyTable"])
```
