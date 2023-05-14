#!/usr/bin/env python3
"""
Merges multiple files together
"""

from merge_files.merge.merger import Merger
from merge_files.merge.stage import parse_args
from merge_files.utils import logging


def main():
    """
    Entrypoint
    """
    arguments = parse_args()

    logging.setup(arguments.options.log_level)

    if arguments.options.help:
        help_topics = [stage.target for stage in arguments.stages]
        print(f"Help topics: {help_topics}")

    merger = Merger(arguments)
    merger.merge()


if __name__ == "__main__":
    main()
