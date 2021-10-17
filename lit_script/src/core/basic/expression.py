from .atoms import Atom
from .variables import Variable


class Context:
    def __init__(self):
        self.variables: dict[Variable, "Expression"] = {}

    def add_variable(self, var: Variable, expr: "Expression"):
        self.variables[var] = expr

    def add_variables(self, mapping: dict[Variable, "Expression"]):
        for var, expr in mapping.items():
            self.add_variable(var, expr)

    def has_variable(self, var: Variable) -> bool:
        return var in self.variables

    def lookup_variable(self, var: Variable) -> "Expression":
        try:
            return self.variables[var]
        except KeyError:
            raise KeyError(f"No such variable: {var}")


class Expression:
    def __init__(self):
        self.local_context = Context()

    def resolve(self, global_context: Context) -> Atom:
        raise NotImplementedError()

    def replace(self, var: Variable, expr: "Expression"):
        raise NotImplementedError()

    def __repr__(self) -> str:
        raise NotImplementedError()
