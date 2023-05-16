import sys
from typing import List

from merge_files.merge.options import Arguments, MainOptions, UnparsedStage


def parse_args(argv: List[str] = sys.argv[1:]) -> Arguments:
    """
    Parses the command line arguments into main options and a list of stages.
    """

    # let's not mutate the system variables
    argv = list(argv)

    main = MainOptions.parse_obj(consume_opts(argv, main=True))

    stages = []
    while argv:
        stage = {"options": consume_opts(argv)}
        stage["target"] = stage["options"].pop("target", "")
        stages.append(UnparsedStage.parse_obj(stage))

    args = Arguments(options=main, stages=stages)

    return args


def consume_opts(argv: List[str], main=False) -> dict[str, str]:
    """
    Generates arguments
    """
    opts = {}

    while argv:
        end_of_options = False
        arg = argv[0]

        if arg == "--":
            if main:
                # no main options, first one was '--'
                break

            argv.pop(0)

            if not argv:
                raise ValueError("Unexpected end of arguments")

            arg = argv[0]
            end_of_options = True

        if arg.startswith("--") and not end_of_options:
            # process an option
            option = arg[2:]

            if "=" in option:
                option, value = option.split("=", maxsplit=1)
            else:
                value = True

            option = option.replace("-", "_")

            if main and option not in MainOptions.__fields__:
                # end of main options
                break

            opts[option] = value
            argv.pop(0)

            if option == "target":
                # might as well support --target=foo as named arg too
                break
        else:
            # positional argument is the file name
            if main:
                # don't consume it when parsing main options
                break
            else:
                opts["target"] = arg
                argv.pop(0)
                break

    return opts
