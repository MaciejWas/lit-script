from .core import Line, Context

Compilable = list[Line]


def create_compiler() -> "Compiler":
    context = Context()
    return Compiler(context)


class Compiler:
    def __init__(self, context: Context):
        self.context = context

    def compile(self, lines: Compilable):
        print("Compiled! :)")
