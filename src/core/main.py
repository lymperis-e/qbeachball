"""
Make beachballs (focal mechanism plots) from GCMT events in a sqlite database. 

Runs as a command-line script, taking the following arguments:
- sqlite_file: path to the SQLite database file
- table_name: name of the table to read from
- filter: a SQL expression (string) to filter the results
- csv_file: path to the CSV file
- max_rows: maximum number of rows to read
- directory: directory to save the beachballs
- fig_format: format to save the beachballs
- bb_size: size of the beachballs
- bb_width: width of the beachball lines

Can also be used as a module, in which case it provides a function, handler, that takes the same arguments as the command-line script.

------------------------------------------------------------------------------------------------------------------------
Adapted Richard Styron's [code](https://github.com/cossatot/gcmt_utils/blob/gem_desktop/scripts/make_bbs_from_sql.py), 
as presented in [this article](https://rocksandwater.net/blog/2017/09/plot-focal-mechs-in-qgis/)
"""

import os

from .beachball import make_beachball
from .readers.file_reader import read_from_csv, read_from_sqlite
from .readers.qgis_reader import read_from_layer


def make_bbs(
    rows,
    directory,
    fig_format,
    bb_size,
    bb_width,
    event_id,
    depth_based_color,
    depth_field,
    tensor_components,
):
    """
    Make beachballs from a list of rows.

    rows: a list of dictionaries of data
    directory: directory to save the beachballs
    fig_format: format to save the beachballs
    bb_size: size of the beachballs
    bb_width: width of the beachball lines
    dpi: resolution of the beachballs
    """
    succ = 0
    for i, row in enumerate(rows):
        make_beachball(
            event=row,
            fig_format=fig_format or "svg",
            directory=directory,
            bb_linewidth=bb_width or 2,
            bb_size=int(bb_size) or 20,
            bb_width=int(bb_width) or 10,
            bb_color="b",
            event_id=event_id,
            depth_based_color=depth_based_color,
            depth_field=depth_field,
            tensor_components=tensor_components,
        )
        if i % 1000 == 0:
            print(i)
        succ += 1

    return succ


def check_output_directory(directory):
    """
    Check that the output directory exists. Create it if it does not.

    directory: directory to check
    """

    if not os.path.exists(directory):
        os.makedirs(directory)


def handler(
    sqlite_file=None,
    table_name=None,
    filter=None,
    csv_file=None,
    qgs_layer=None,
    max_rows=None,
    directory=None,
    fig_format=None,
    bb_size=None,
    bb_width=None,
    event_id="Event",
    depth_based_color=True,
    depth_field="Depth",
    tensor_components=None,
):
    """
    Handle the process of making beachballs from a SQLite database or a CSV file.

    sqlite_file: path to the SQLite database file
    table_name: name of the table to read from
    filter: a SQL expression (string) to filter the results
    csv_file: path to the CSV file
    max_rows: maximum number of rows to read
    directory: directory to save the beachballs
    fig_format: format to save the beachballs
    bb_size: size of the beachballs
    bb_width: width of the beachball lines
    dpi: resolution of the beachballs
    """
    rows = None

    if not sqlite_file and not csv_file and not qgs_layer:
        raise ValueError("A file or layer must be provided.")

    if not directory:
        raise ValueError("output directory must be provided.")

    check_output_directory(directory)

    if sqlite_file:
        rows = read_from_sqlite(sqlite_file, table_name, filter)
    elif csv_file:
        rows = read_from_csv(csv_file, max_rows)
    elif qgs_layer:
        rows = read_from_layer(qgs_layer, max_rows)

    if not rows or len(rows) == 0:
        raise ValueError("No rows to process.")

    successes = make_bbs(
        rows,
        directory,
        fig_format,
        bb_size,
        bb_width,
        event_id,
        depth_based_color,
        depth_field,
        tensor_components,
    )
    return successes


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Make beachballs from GCMT events.")
    parser.add_argument(
        "--sqlite_file", help="path to the SQLite database file", default=None
    )
    parser.add_argument(
        "--table_name", help="name of the table to read from", default=None
    )
    parser.add_argument(
        "--sql_filter", help="a SQL expression to filter the results", default=None
    )
    parser.add_argument("--csv_file", help="path to the CSV file", default=None)
    parser.add_argument(
        "--csv_max_rows", help="maximum number of rows to read", default=None
    )
    parser.add_argument(
        "--directory", help="directory to save the beachballs", default=None
    )
    parser.add_argument(
        "--fig_format", help="format to save the beachballs", default=None
    )
    parser.add_argument("--bb_size", help="size of the beachballs", default=None)
    parser.add_argument("--bb_width", help="width of the beachball lines", default=None)

    args = parser.parse_args()
    handler(
        args.sqlite_file,
        args.table_name,
        args.sql_filter,
        args.csv_file,
        args.csv_max_rows,
        args.directory,
        args.fig_format,
        args.bb_size,
        args.bb_width,
    )

# Example CLI command:
# python scripts/main.py  --csv_file ./data/gcmt_2017_09_07.csv --csv_max_rows 1000 --directory ./data/bbs/svg --fig_format svg --bb_size 20 --bb_width 100
