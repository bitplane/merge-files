import sys
from typing import List

from merge_files.merge.options import Arguments, MainOptions, UnparsedStage


def parse_args(argv: List[str] = sys.argv[1:]) -> Arguments:
    """
    Parses the command line arguments into main options and a list of stages.
    """

    # let's not mutate the system variables
    argv = list(argv)

    main = MainOptions(consume_opts(argv, main=True))

    stages = []
    while argv:
        stages.append(UnparsedStage(consume_opts(argv)))

    args = Arguments(main=main, stages=stages)

    return args


def consume_opts(argv: List[str], main=False) -> dict[str, str]:
    """
    Generates arguments
    """
    opts = {}

    while argv:
        arg = argv[0]

        if arg == "--":
            argv.pop()
            break

        elif arg.startswith("--"):
            # process an option
            option = arg[2:]

            if main and option not in MainOptions.__fields__:
                # end of main options
                break

            value = True

            if "=" in option:
                option, value = option.split("=", maxsplit=1)

            option = option.replace("-", "_")

            opts[option] = value
            argv.pop()

            if option == "target":
                # might as well support --target=foo as positional
                break
        else:
            # positional argument
            opts["target"] = arg
            argv.pop()

    return opts
