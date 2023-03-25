#!/usr/bin/env python3
"""Merges the source file into the destination file.

Supports .env, text and binary files.
"""
import argparse
import sys
from pathlib import Path
from typing import List

from .mergable import get
from .method import MergeMethod


def parse_args(command_line: List[str]) -> argparse.Namespace:
    """
    Parse the command line arguments, or a list of strings.

    Might call sys.exit() if the arguments are invalid.
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="List of files to merge. The last file will be the output.",
    )
    parser.add_argument(
        "--method",
        help="Merge method",
        default=MergeMethod.preserve,
        type=MergeMethod,
        choices=list(MergeMethod),
    )

    return parser.parse_args(command_line)


def main(cmdline=sys.argv[1:]):
    """
    Main entry point for the merge-files command line tool.
    """
    args = parse_args(cmdline)

    source = Path(args.source)
    dest = Path(args.dest)

    merger = get(args.source, args.dest)
    output_data = merger(source, dest, args.update)

    with open(args.dest, "wb") as output_file:
        output_file.write(output_data)


if __name__ == "__main__":
    main()
