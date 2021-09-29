import dataclasses
from lark import Transformer
from lark.visitors import TransformerChain
from dataclasses import dataclass
from typing import Optional, Any

from .expressions import Value, Variable, Expression

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
        return Value(value=value, type="Str")

    def NUMBER(self, value: str):
        return Value(value=value, type="Str")

class ExpressionTransformer(Transformer):
    """Every method is of type Variable/Value/Expression -> Expression"""

    def expression(self, x):
        pass

    def new_variable(self, x):
        pass

    def variable(self, x):
        pass

    def value(self, x: Variable):
        pass

    def function_call(self, x):
        pass

    def function(self, x):
        pass

    def function_arg(self, x):
        pass


class FinalTransformer(Transformer):

    def all(self, x):
        pass

    def line(self, x):
        pass

    def definition(self, x):
        pass

    def declaration(self, x):
        pass
