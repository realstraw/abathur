#!/usr/bin/env python

import argparse


def perform_extraction(queries, output):
    """
    """
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract (aggregated) features from a sql database.")
    parser.add_argument(
        'queries', help="the set of queries and feature names to be executed.")
    parser.add_argument(
        'output', help="the output file")
    args = parser.parse_args()

    perform_extraction(args.queries, args.output)
