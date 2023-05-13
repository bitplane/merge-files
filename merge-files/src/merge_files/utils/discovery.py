import importlib
from pathlib import Path
from typing import List, Type


def subclasses(cls: Type) -> List[Type]:
    """
    Get all subclasses of a type
    """
    res = []
    for cls in cls.__subclasses__():
        res.append(cls)
        res.extend(subclasses(cls))

    return res

    # ChatGPT's suggestion, without recursion.
    # need a test before trusting the lying sack of shit
    # res = []
    # queue = [cls]
    # while queue:
    #     cls = queue.pop(0)
    #     subclasses = cls.__subclasses__()
    #     res.extend(subclasses)
    #     queue.extend(subclasses)
    # return res


def search_subclasses(search_dir: Path, cls: Type) -> List[Type]:
    """
    Look in search_dir, find all subclasses of cls
    """
    for file in search_dir.rglob("*.py"):
        if file.name == "__init__.py":
            continue

        # handle subdirs
        relative_path = file.relative_to(search_dir)
        module_name = ".".join(relative_path.parts)[:-3]

        spec = importlib.util.spec_from_file_location(module_name, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    # find all subclasses, including subclasses of subclasses
    return subclasses(cls)
