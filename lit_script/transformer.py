import dataclasses
from lark import Transformer
from lark.visitors import TransformerChain
from dataclasses import dataclass
from typing import Optional, Any, Union

from .expressions import FunctionCallExpression, Atom, AtomExpression, Variable, FunctionCall, Chain, Expression, VariableExpression


AnyExpression = Union[Variable, Atom, FunctionCall, Chain]


def create_transformer() -> TransformerChain:
    return (
        TerminalTransformer() *
        ExpressionTransformer() *
        FinalTransformer()
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

    def expression(self, xs: list[AnyExpression]):
        assert len(xs) == 1
        x = xs[0]

        if isinstance(x, Atom):
            return AtomExpression(x)

        elif isinstance(x, Variable):
            return VariableExpression(x)
        
        elif isinstance(x, FunctionCall):
            return FunctionCallExpression(x)

        else:
            raise NotImplementedError(f"Intermediate expression {type(x)} not implemented")

    def new_variable(self, var: Variable):
        return var

    def variable(self, vars: list[Variable]):
        assert len(vars) == 1
        return vars[0]

    def value(self, vals: list[Atom]):
        assert len(vals) == 1
        return vals[0]

    def function_call(self, exprs: list[Expression]):
        fun, arg = exprs
        return FunctionCall(fun, arg)

    def function(self, expr: Expression):
        return expr

    def function_arg(self, expr: Expression):
        return expr


class FinalTransformer(Transformer):

    def all(self, x):
        pass

    def line(self, x):
        pass

    def definition(self, x):
        pass

    def declaration(self, x):
        pass
