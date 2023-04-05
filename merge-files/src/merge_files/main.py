#!/usr/bin/env python3
"""
Merges multiple files together
"""

from merge_files.merge.stage import parse_args


def main():
    """
    Entrypoint
    """
    stages = parse_args()

    for stage in stages:
        print(stage)

if __name__ == "__main__":
    main()
