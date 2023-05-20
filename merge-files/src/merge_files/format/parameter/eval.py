import simpleeval
from pydantic import ConstrainedStr


class Eval(ConstrainedStr):
    """
    Execute a Python expression.
    """

    strip_whitespace = True
    min_length = 1

    @classmethod
    def validate(cls, v):
        try:
            simpleeval.SimpleEval().parse(v)
        except Exception as e:
            raise ValueError(f"Invalid expression: {v}") from e
        return v

    def __call__(self):
        """
        Execute the statement.
        """
        return simpleeval.SimpleEval().eval(self)
