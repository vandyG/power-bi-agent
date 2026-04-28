#!/usr/bin/env python3
"""Convert a .sql file to a PowerBI M Sql.Database() expression."""

import argparse
import sys


def convert(sql: str, server: str, database: str) -> str:
    escaped = sql.replace("\n", "#(lf)")
    return f'= Sql.Database("{server}", "{database}", [Query="{escaped}"])'


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Wrap SQL content in a PowerBI Sql.Database() M expression."
    )
    parser.add_argument("file", nargs="?", help="Path to .sql file (omit for stdin)")
    parser.add_argument("--server", required=True, help="SQL Server hostname/instance")
    parser.add_argument("--database", required=True, help="Database name")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            sql = f.read()
    else:
        sql = sys.stdin.read()

    print(convert(sql.rstrip("\n"), args.server, args.database))


if __name__ == "__main__":
    main()
