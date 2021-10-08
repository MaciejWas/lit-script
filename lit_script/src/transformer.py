from lark import Transformer
from lark.visitors import TransformerChain
from typing import Union

from .core import (
    Line,
    ExpressionLine,
    Definition,
    Declaration,
    LitType,
    BasicType,
    FunctionType,
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

    def STRING(self, value: str) -> Variable:
        return Variable(name=value)

    def ESPCAPED_STRING(self, value: str) -> Atom:
        return Atom(value=value, type="Str")

    def NUMBER(self, value: str) -> Atom:
        assert isinstance(value, str)
        return Atom(value=int(value), type="Str")


class ExpressionTransformer(Transformer):
    def expression(self, xs: list[PreExpression]) -> Expression:
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

    def new_variable(self, vars: list[Variable]) -> Variable:
        assert len(vars) == 1
        return vars[0]

    def variable(self, vars: list[Variable]) -> Variable:
        assert len(vars) == 1
        return vars[0]

    def value(self, vals: list[Atom]) -> Atom:
        assert len(vals) == 1
        return vals[0]

    def function_call(self, exprs: list[Expression]) -> FunctionCall:
        assert len(exprs) == 2
        fun, arg = exprs
        return FunctionCall(fun, arg)

    def function(self, exprs: list[Expression]) -> Expression:
        assert len(exprs) == 1
        return exprs[0]

    def function_arg(self, exprs: list[Expression]) -> Expression:
        assert len(exprs) == 1
        return exprs[0]

    def infix_call(self, infix_call: list[Union[Expression, Variable]]) -> FunctionCall:
        assert isinstance(infix_call[0], Expression)
        assert isinstance(infix_call[1], Variable)
        assert isinstance(infix_call[2], Expression)

        infix_fn = VariableExpression(infix_call[1])
        argument_1 = infix_call[0]
        argument_2 = infix_call[2]

        partially_applied_fn: Expression = self.expression(
            [FunctionCall(infix_fn, argument_1)]
        )

        return FunctionCall(partially_applied_fn, argument_2)

    def infix(self, vars: list[Variable]) -> Variable:
        assert len(vars) == 1
        return vars[0]


class TypeTransformer(Transformer):
    def type(self, types: list[LitType]) -> LitType:
        assert len(types) == 1
        return types[0]

    def atom_type(self, vars: list[Variable]):
        assert len(vars) == 1
        return BasicType(type=vars[0].name)

    def function_type(self, types: list[LitType]):
        assert len(types) == 2
        return FunctionType(from_=types[0], to=types[1])


class FinalTransformer(Transformer):
    def all(self, ls: list[Line]) -> list[Line]:
        return ls

    def line(self, ls: list[Union[Definition, Declaration, Expression]]) -> Line:
        assert len(ls) == 1

        if isinstance(ls[0], Expression):
            return ExpressionLine(expr=ls[0])

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
