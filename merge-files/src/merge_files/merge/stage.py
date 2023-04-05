import sys

from typing import List, Optional
from pydantic import BaseModel


class Option(BaseModel):
    """
    Represents a command line option
    """
    name: str
    value: Optional[str]


class Stage(BaseModel):
    """
    Represents a merge destination and its options
    """
    options: List[Option] = []
    file: Optional[str] = None


def parse_args(argv: List[str] = sys.argv[1:]) -> List[Stage]:
    """
    Parses the command line arguments into a list of stages
    """
    stages: List[Stage] = []

    i = 0
    total_args = len(argv)
    stage = Stage()

    while i < total_args:

        arg = argv[i]

        if arg == '--':
            # finished options for this stage

            stage.file = argv[i+1]

            i += 1
            stages.append(stage)
            stage = Stage()

        elif arg.startswith('--'):
            # process an option

            option = arg[2:]
            value = None

            if '=' in option:
                option, value = option.split('=', maxsplit=1)

            stage.options.append(Option(name=option, value=value))

        else:
            # process file name
            stage.file = arg
            stages.append(stage)
            stage = Stage()
            
        i += 1

    # append the final stage
    if stage.file or stage.options:
        stages.append(stage)

    return stages
