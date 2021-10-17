from .core import Expression, Atom, Line, Context, inbuilt_functions

Compilable = list[Line]


class CompileLog:
    def __init__(self):
        self.events = []

    def log(self, info: str):
        self.events.append(info)

    def __repr__(self):
        return "\n".join(self.events)

    def __str__(self):
        return "\n".join(self.events)


class Compiler:
    def __init__(self):
        self.global_context = Context()

    def setup_inbuilt(self):
        self.global_context.add_variables(inbuilt_functions)

    def resolve(self, expr: Expression) -> Atom:
        return expr.resolve(self.global_context)

    def compile(self, lines: Compilable):

        type_check_passed = self.check_types(lines)
        if not type_check_passed:
            return Exception("Type check failed.")

        print("Compiled! :)")

    def check_types(self, lines: Compilable) -> bool:
        return True  # TODO: Impl
