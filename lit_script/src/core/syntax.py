from dataclasses import dataclass
from typing import Optional, Callable, Union, Any

from .basic import Expression, Variable


@dataclass
class FunctionCall:
    fun: Expression
    arg: Expression

    def __repr__(self) -> str:
        return f"<Application of {self.fun} on {self.arg}"


class Chain:
    def __init__(self, exprs: list[Expression]):
        self.exprs = exprs


class Line:
    pass


@dataclass
class Definition(Line):
    is_function: bool
    var: Variable
    expr: Expression


@dataclass
class Declaration(Line):
    var: Variable
    type: str  # TODO: Fucging types


@dataclass
class ExpressionLine(Line):
    expr: Expression
