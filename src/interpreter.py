from lark import Lark
from lark.visitors import TransformerChain

from .transformer import create_transformer
from .compiler import Compilable, Compiler, create_compiler


class CompileLog:
    def __init__(self):
        self.events = []

    def log(self, info: str):
        self.events.append(info)

    def __repr__(self):
        return "\n".join(self.events)

    def __str__(self):
        return "\n".join(self.events)


class Interpreter:
    def __init__(self):
        self.log = CompileLog()
        self.parser: Lark = self.load_parser()
        self.transformer: TransformerChain = create_transformer()
        self.compiler: Compiler = create_compiler()

    def load_parser(self) -> Lark:
        with open("language/grammar.lark", "r") as f:
            grammar = f.read()
        return Lark(grammar, start="all")

    def read(self, line: str):
        self.log.log("Starting Compilation")

        tree = self.parser.parse(line)
        print(tree.pretty())

        program: Compilable = self.transformer.transform(tree)
        print(program)

        self.compiler.compile(program)

        self.log.log("End of Compilation")
        print(self.log)
