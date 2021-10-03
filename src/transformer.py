import dataclasses
from lark import Transformer
from lark.visitors import TransformerChain
from dataclasses import dataclass
from typing import Optional, Any, Union

from .expressions import (
    Line,
    Definition,
    Declaration,
    Expression,
    Atom,
    AtomExpression,
    Variable,
    VariableExpression,
    FunctionCallExpression,
    FunctionCall,
    Chain,
)

PreExpression = Union[Variable, Atom, FunctionCall, Chain]


def create_transformer() -> TransformerChain:
    return (
        TerminalTransformer()
        * ExpressionTransformer()
        * TypeTransformer()
        * FinalTransformer()
    )


class TerminalTransformer(Transformer):
    """Transforming lark's terminal characters."""

    def STRING(self, value: str):
        return Variable(name=value)

    def ESPCAPED_STRING(self, value: str):
        return Atom(value=value, type="Str")

    def NUMBER(self, value: str):
        return Atom(value=value, type="Str")


class ExpressionTransformer(Transformer):
    """Every method is of type Variable/Value/Expression -> Expression"""

    def expression(self, xs: list[PreExpression]):
        assert len(xs) == 1
        x = xs[0]

        if isinstance(x, Atom):
            return AtomExpression(x)

        elif isinstance(x, Variable):
            return VariableExpression(x)

        elif isinstance(x, FunctionCall):
            return FunctionCallExpression(x)

        else:
            raise NotImplementedError(
                f"Intermediate expression {type(x)} not implemented"
            )

    def new_variable(self, vars: list[Variable]):
        assert len(vars) == 1
        return vars[0]

    def variable(self, vars: list[Variable]):
        assert len(vars) == 1
        return vars[0]

    def value(self, vals: list[Atom]):
        assert len(vals) == 1
        return vals[0]

    def function_call(self, exprs: list[Expression]):
        fun, arg = exprs
        return FunctionCall(fun, arg)

    def function(self, exprs: list[Expression]):
        assert len(exprs) == 1
        return exprs[0]

    def function_arg(self, exprs: list[Expression]):
        assert len(exprs) == 1
        return exprs[0]


class LitType:
    pass


@dataclass
class AtomType(LitType):
    var: Variable


@dataclass
class FunctionType(LitType):
    from_: LitType
    to: LitType


class TypeTransformer(Transformer):
    def type(self, types: list[LitType]) -> LitType:
        assert len(types) == 1
        return types[0]

    def atom_type(self, vars: list[Variable]):
        assert len(vars) == 1
        return AtomType(var=vars[0])

    def function_type(self, types: list[LitType]):
        assert len(types) == 2
        return FunctionType(from_=types[0], to=types[1])


class FinalTransformer(Transformer):
    def all(self, ls: list[Line]):
        return ls

    def line(self, ls: list[Line]):
        assert len(ls) == 1
        return ls[0]

    def variable_defn(self, xs):
        new_variable: Variable = xs[0]
        expr: Expression = xs[1]
        return Definition(is_function=False, var=new_variable, expr=expr)

    def function_defn(self, xs):
        new_variable: Variable = xs[0]
        expr: Expression = xs[-1]
        return Definition(is_function=True, var=new_variable, expr=expr)

    def definition(self, defns: list[Definition]) -> Definition:
        assert len(defns) == 1
        return defns[0]

    def declaration(self, xs):
        new_variable: Variable = xs[0]
        type: LitType = xs[1]
        return Declaration(var=new_variable, type=type)


def codecov_test():
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
    print("t")
