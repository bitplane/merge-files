from pathlib import Path
from typing import List, Type

from merge_files import mergeable_types
from merge_files.mergeable_types.mergeable import Mergeable


class Merger:
    """
    The merge manager.
    """
    def __init__(self):
        self.mergeable_types = find_mergeable_types()

        self.supported_types: Dict[Priority, Support] = self._load_supported_types()
    
    def _load_supported_types(self) -> Dict[Priority, Support]:


def find_mergeable_types() -> List[Type[Mergeable]]:
    """
    Find all the mergeable types
    """

    # import everything so we can find the subclasses
    search_dir = Path(mergeable_types.__file__).parent

    for file in search_dir.rglob("*.py"):
        if file.name == "__init__.py":
            continue

        # handle subdirs
        relative_path = file.relative_to(search_dir)
        module_name = ".".join(relative_path.parts)[:-3]

        __import__(f"merge_files.mergeable_types.{module_name}")

    # find all subclasses, including subclasses of subclasses
    
    return get_subclasses(Mergeable)


def get_subclasses(t: type) -> List[type]:
    res = []
    for cls in t.__subclasses__():
        res.append(cls)
        res.extend(get_subclasses(cls))

    return res