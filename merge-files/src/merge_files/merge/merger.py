from pathlib import Path
from typing import List, Type

from merge_files import formats
from merge_files.formats.format import Format
from merge_files.merge.option import Option
from merge_files.merge.support import Support


class Merger:
    """
    The merge manager.
    """

    def __init__(self):
        self.formats = find_supported_formats()
        self.sources = {format: [] for format in self.formats}
        self.dests = {format: [] for format in self.formats}

        for format in self.formats:
            format.register(self)

    def register(self, source: Type[Format], dest: Type[Format], options: List[Option]):
        """
        Register a merge that we can do
        """
        support = Support(source=source, dest=dest, options=options)
        self.sources[source].append(support)
        self.dests[dest].append(support)


def find_supported_formats() -> List[Type[Format]]:
    """
    Find all the file formats we support
    """

    # import everything so we can find the subclasses
    search_dir = Path(formats.__file__).parent

    for file in search_dir.rglob("*.py"):
        if file.name == "__init__.py":
            continue

        # handle subdirs
        relative_path = file.relative_to(search_dir)
        module_name = ".".join(relative_path.parts)[:-3]

        __import__(f"merge_files.formats.{module_name}")

        #
        # spec = importlib.util.spec_from_file_location(module_name, file)
        # module = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(module)
        #

    # find all subclasses, including subclasses of subclasses

    return get_subclasses(Format)


def get_subclasses(t: type) -> List[type]:
    res = []
    for cls in t.__subclasses__():
        res.append(cls)
        res.extend(get_subclasses(cls))

    return res
