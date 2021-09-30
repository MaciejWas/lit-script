from typing import Optional, Any, Callable, Protocol, runtime_checkable, Union
from dataclasses import dataclass


class Function:
    def __init__(
        self,
        argument: Optional["Variable"] = None,
        expression: Optional["Expression"] = None,
        python_fn: Optional[Callable[["Atom"], "Atom"]] = None
    ):
        self.argument = argument
        self.expression = expression
        self.python_fn = python_fn

    @classmethod
    def from_python_fn(cls, fn: Callable[["Atom"], "Atom"]):
        return cls(python_fn=fn)

    @classmethod
    def from_expression(cls, expr: "Expression", arg: "Variable"):
        return cls(argument=arg, expression=expr)
            
    def __call__(self, a: "Atom") -> "Atom":
        if self.python_fn:
            return self.python_fn(a)
        else:
            raise NotImplementedError()

@dataclass
class Atom:
    value: Union[int, float, str, Function]
    type: str

    @property
    def is_function(self):
        return isinstance(self.value, Function)

    def __call__(self, *args, **kwargs):
        if not isinstance(self.value, Function):
            raise Exception(f"You were trying to call {self.type}, which obviously failed. The atom has value {self.value}")
        else:
            return self.value(*args, **kwargs)

    def __add__(self, other: "Atom") -> "Atom":
        if self.type == other.type:
            if self.type in ["Int", "Float"]:
                assert isinstance(self.value, float) or isinstance(self.value, int)
                assert isinstance(other.value, float) or isinstance(other.value, int)
                
                return Atom(value=self.value + other.value, type=self.type) # mypy:
            else:
                raise NotImplementedError("Cant add that m8.")
        else:
            raise NotImplementedError("Cant add that m8.")

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
        try:
            return self.variables[var]
        except KeyError:
            raise KeyError(f"No such variable: {var}")


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

class ChainExpression(Expression):
    pass # TODO: IMPL