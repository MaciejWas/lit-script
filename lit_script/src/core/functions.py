from typing import Optional, Callable

from .basic import Atom, Expression, Variable


class Function:
    def __init__(
        self,
        argument: Optional[Variable] = None,
        expression: Optional[Expression] = None,
        python_fn: Optional[Callable[[Atom], Atom]] = None,
    ):
        self.argument = argument
        self.expression = expression
        self.python_fn = python_fn

    @classmethod
    def from_python_fn(cls, fn: Callable[[Atom], Atom]) -> "Function":
        return cls(python_fn=fn)

    @classmethod
    def from_expression(cls, expr: Expression, arg: Variable) -> "Function":
        return cls(argument=arg, expression=expr)

    def __call__(self, a: Atom) -> Atom:
        if self.python_fn:
            return self.python_fn(a)
        else:
            raise NotImplementedError()

    def __repr__(self) -> str:
        return f"<Function :: sadface>"
