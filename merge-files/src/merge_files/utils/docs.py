import ast
import inspect

from pydantic import BaseModel


# todo: maybe call this from a base model and have it inject the docs into
# the filed metadata. Then we can generate help text for the CLI from the
# source code directly, as well as introspect at runtime.
def get_field_docs(cls: BaseModel):
    """
    Gets docstrings for fields in a pydantic model.

    Python doesn't export this by default, so we parse the source code using
    ast, and then extract a docstring from the line after an assignment.
    """

    keys = cls.__fields__.keys()
    tree = ast.parse(inspect.getsource(cls))
    body = tree.body[0].body

    docs = {}

    i = 0
    while i < len(body):
        node = body[i]
        is_assignment = isinstance(node, (ast.Assign, ast.AnnAssign))

        if is_assignment:
            name = node.target.id

            if name not in keys:
                i += 1
                continue

            docs[name] = ""

            in_range = i + 1 < len(body)

            if in_range and isinstance(body[i + 1], ast.Expr):
                value = body[i + 1].value.s
                docs[name] = value
                i += 1
        i += 1

    return docs
