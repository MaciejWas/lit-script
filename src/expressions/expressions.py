from typing import Optional, Any, Callable, Protocol, runtime_checkable, Union
from dataclasses import dataclass

# ------------------------------
#     PARSING
# ------------------------------

class Line:
    pass

@dataclass
class Definition(Line):
    is_function: bool
    var: "Variable"
    expr: "Expression"

@dataclass
class Declaration(Line):
    var: "Variable"
    type: str # TODO: Fucging types

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

    def __repr__(self) -> str:
        return f"<Function :: sadface>"

@dataclass
class Atom:
    value: Union[int, float, str, Function]
    type: str

    @property
    def is_function(self):
        return isinstance(self.value, Function)

    def __repr__(self) -> str:
        return f"<Atom {self.value} :: {self.type}>"

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

    def __repr__(self) -> str:
        return f"<Variable {self.name} :: sadface>"

@dataclass
class FunctionCall:
    fun: "Expression"
    arg: "Expression"

    def __repr__(self):
        return f"<Application of {self.fun} on {self.arg}"

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

    def __repr__(self) -> str:
        raise NotImplementedError()

class AtomExpression(Expression):
    def __init__(self, atom: Atom):
        self.atom = atom
    
    def resolve(self) -> Atom:
        return self.atom

    def __repr__(self) -> str:
        return self.atom.__repr__()


class VariableExpression(Expression):
    def __init__(self, variable: Variable):
        self.variable = variable

    def resolve(self) -> Atom:
        behind_variable: Expression = self.context.lookup_variable(self.variable)
        return behind_variable.resolve()

    def __repr__(self) -> str:
        return self.variable.__repr__()


class FunctionCallExpression(Expression):
    def __init__(self, fncall: FunctionCall):
        self.fncall = fncall

    def resolve(self) -> Atom:
        actual_function: Atom = self.fncall.fun.resolve()
        actual_arg: Atom = self.fncall.arg.resolve()

        return actual_function(actual_arg)

    def __repr__(self) -> str:
        return self.fncall.__repr__()

class ChainExpression(Expression):
    pass # TODO: IMPL