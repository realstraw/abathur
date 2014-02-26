#!/usr/bin/env python

import argparse
import sys
from os.path import expanduser
import json
from sqlalchemy import create_engine
import csv


def _get_db_connection_string():
    config_file = expanduser("~/.abathur.conf")
    with open(config_file) as fp:
        configs = json.load(fp)

    return configs["db_connection_string"]


def _perform_extraction(ident_file, query_file, output_file, query_ident):
    """
    query_ident: whether we should query the IDs or just use the file as IDs
    """

    conn_string = _get_db_connection_string()
    engine = create_engine(conn_string)
    conn = engine.connect()

    id_list = []
    # first need to check whether we need to get a list of IDs.
    if query_ident:
        # need to find the list of IDs using the given query.
        with open(ident_file, "rb") as ident_query_file:
            the_query = ident_query_file.read()
            result = conn.execute(the_query)
            for row in result:
                id_list.append(row[0])
    else:
        with open(ident_file, "rb") as ident_query_file:
            for line in ident_query_file:
                if line[-1] == "\n":
                    line = line[:-1]
                id_list.append(line)

    # Now we have the ID list, parse and execute the queries in the query_file.
    query_file_dict = json.load(query_file)
    with open(output_file, "wb") as the_output_file:
        csvwriter = csv.writer(the_output_file)
        # write out the header
        csvwriter.writerow(query_file_dict.keys())

        for ident in id_list:
            row = [ident, ]
            for feat_name, feat_query in query_file_dict.iteritems():
                feat_value = conn.execute(feat_query.format(ident=ident))
                row.append(feat_value)
            csvwriter.writerow(row)


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

    print "Queries: {}\nOutput: {}".format(args.queries, args.output)


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
