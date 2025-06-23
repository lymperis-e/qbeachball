"""
Read focal mechanism features from a csv/sqlite file and return them as a list of dictionaries.
"""

import csv
import sqlite3


def read_from_sqlite(sqlite_file, table_name, filter=None):
    """
    Read from a SQLite database.

    sqlite_file: path to the SQLite database file
    table_name: name of the table to read from
    filter: a SQL expression (string) to filter the results
    """
    con = sqlite3.connect(sqlite_file)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if filter:
        cur.execute(f"SELECT * FROM {table_name} WHERE {filter}")
    else:
        cur.execute("SELECT * FROM {table_name}")
    rows = cur.fetchall()
    con.close()
    return rows


def read_from_csv(csv_file, max_rows=None):
    """
    Read from a CSV file.

    csv_file: path to the CSV file
    max_rows: maximum number of rows to read
    """
    try:
        maxr = int(max_rows) if max_rows else None
    except ValueError as e:
        raise ValueError("max_rows must be an integer or None") from e

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [
            dict(zip(header, row))
            for i, row in enumerate(reader)
            if not max_rows or i < maxr
        ]
    return rows
