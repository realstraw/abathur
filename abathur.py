#!/usr/bin/env python

import argparse
import sys


def _perform_extraction(ident_file, query_file, output_file, query_ident):
    """
    query_ident: whether we should query the IDs or just use the file as IDs
    """


def perform_extraction(prog, raw_args):
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Extract (aggregated) features from a sql database.")
    parser.add_argument(
        "ident", help="the ID file or queries")
    parser.add_argument(
        'queries', help="the set of queries and feature names to be executed.")
    parser.add_argument(
        'output', help="the output file")
    parser.add_argument(
        "--query-ident",
        dest="query_ident",
        action="store_true",
        help="the given id file is a query file. by default we assume it's a "
        "file that contains a list of IDs.")
    args = parser.parse_args(raw_args)

    print "queries: {}\noutput: {}".format(args.queries, args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=sys.argv[0], description="Execute abathur commands.")
    parser.add_argument(
        'command', choices=['extract'], help="the command to be executed")
    args = parser.parse_args(args=sys.argv[1:2])

    if args.command == "extract":
        new_prog = "-".join(sys.argv[:2])
        new_args = sys.argv[2:]

        perform_extraction(new_prog, new_args)
