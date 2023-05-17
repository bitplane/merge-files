import importlib
from pathlib import Path
from typing import Set, Type

from merge_files.utils.logging import get_logger

logger = get_logger()


def subclasses(cls: Type) -> Set[Type]:
    """
    Get all subclasses of a type
    """
    res = []
    queue = [cls]

    while queue:
        cls = queue.pop(0)
        subclasses = cls.__subclasses__()
        res.extend(subclasses)
        queue.extend(subclasses)

    return set(res)


def search_subclasses(search_dir: Path, cls: Type) -> Set[Type]:
    """
    Look in search_dir, find all subclasses of cls
    """
    for file in search_dir.rglob("*.py"):
        if file.name == "__init__.py":
            continue

        # handle subdirs
        relative_path = file.relative_to(search_dir)
        module_name = ".".join(relative_path.parts)[:-3]

        try:
            spec = importlib.util.spec_from_file_location(module_name, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            logger.exception(f"Failed to load module {module_name}: {e}")

    # find all subclasses, including subclasses of subclasses
    return subclasses(cls)
