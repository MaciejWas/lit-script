from typing import Optional, Any, Callable, Protocol, runtime_checkable, Union
from dataclasses import dataclass


class Function:
    def __init__(
        self,
        argument: "Variable",
        expression: "Expression",
        override: Optional[Callable[["Atom"], "Atom"]] = None
    ):
        self.argument = argument
        self.expression = expression
        self.override = override
            
    def __call__(self, a: "Atom") -> "Atom":
        if self.override:
            return self.override(a)
        else:
            raise NotImplementedError()

@dataclass
class Atom:
    value: Union[int, float, str, Function]
    type: str

    def __call__(self, *args, **kwargs):
        if not isinstance(self.value, Function):
            raise Exception(f"You were trying to call {self.type}, which obviously failed.")
        else:
            return self.value(*args, **kwargs)

    def __eq__(self, other: Any):
        if isinstance(other, Atom):
            return self.value == other.value # TODO: Types
        else:
            return False

@dataclass
class Variable:
    name: str

    def __hash__(self):
        return hash(self.name)

@dataclass
class FunctionCall:
    fun: "Expression"
    arg: "Expression"

class Chain:
    def __init__(self, exprs: list["Expression"]):
        self.exprs = exprs

class Context:
    def __init__(self):
        self.variables: dict[Variable, "Expression"] = {}

    def add_variable(self, var: Variable, expr: "Expression"):
        self.variables[var] = expr
    
    def lookup_variable(self, var: Variable) -> "Expression":
        return self.variables[var]


# ------------------------------
#     EXPRESSIONS
# ------------------------------


class Expression:
    context = Context()

    def __init__(self):
        self.local_context = Context()

    def resolve(self) -> Atom:
        raise NotImplementedError()

    def add_to_local_context(self, var: Variable, expr: "Expression"):
        raise NotImplementedError()

        self.local_context.add_variable(var, expr)

    def destroy_local_context(self):
        self.local_context = Context()


class AtomExpression(Expression):
    def __init__(self, atom: Atom):
        self.atom = atom
    
    def resolve(self) -> Atom:
        return self.atom


class VariableExpression(Expression):
    def __init__(self, variable: Variable):
        self.variable = variable

    def resolve(self) -> Atom:
        behind_variable: Expression = self.context.lookup_variable(self.variable)
        return behind_variable.resolve()


class FunctionCallExpression(Expression):
    def __init__(self, fncall: FunctionCall):
        self.fncall = fncall

    def resolve(self) -> Atom:
        actual_function: Atom = self.fncall.fun.resolve()
        actual_arg: Atom = self.fncall.arg.resolve()

        return actual_function(actual_arg)