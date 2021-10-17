from typing import Optional, Any, Callable, Union
from dataclasses import dataclass

from .basic import Atom, Variable, Expression, Context
from .syntax import FunctionCall


class AtomExpression(Expression):
    def __init__(self, atom: Atom):
        super().__init__()
        self.atom = atom

    def resolve(self, global_context: Context) -> Atom:
        assert isinstance(self.atom, Atom)
        return self.atom

    def replace(self, var: Variable, expr: Expression) -> Expression:
        return self

    def __repr__(self) -> str:
        return self.atom.__repr__()


class VariableExpression(Expression):
    def __init__(self, variable: Variable):
        super().__init__()
        self.variable = variable

    def resolve(self, global_context: Context) -> Atom:
        behind_variable: Expression

        behind_variable = global_context.lookup_variable(self.variable)

        x = behind_variable.resolve(global_context)
        assert isinstance(x, Atom)
        return x

    def replace(self, var: Variable, expr: Expression) -> Expression:
        if self.variable == var:
            return expr
        else:
            return self

    def __repr__(self) -> str:
        return self.variable.__repr__()


class FunctionCallExpression(Expression):
    def __init__(self, fncall: FunctionCall):
        super().__init__()
        self.fncall = fncall

    def resolve(self, global_context: Context) -> Atom:
        actual_function: Atom = self.fncall.fun.resolve(global_context)
        actual_arg: Atom = self.fncall.arg.resolve(global_context)

        assert callable(actual_function.value)
        result = actual_function.value(actual_arg)

        assert isinstance(result, Atom), f"{result} is not an atom"

        return result

    def __repr__(self) -> str:
        return self.fncall.__repr__()


class ChainExpression(Expression):
    pass  # TODO: IMPL
