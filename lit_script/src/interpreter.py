from lark import Lark
from lark.visitors import TransformerChain

from .core import ExpressionLine, Expression

from .transformer import create_transformer
from .compiler import Compilable, Compiler, Atom


def load_parser() -> Lark:
    with open("language/grammar.lark", "r") as f:
        grammar = f.read()

    return Lark(grammar, start="all")


class Interpreter:
    def __init__(self):
        self.parser: Lark = load_parser()
        self.transformer: TransformerChain = create_transformer()
        self.compiler = Compiler()

        self.compiler.setup_inbuilt()

    def compile(self, line: str) -> str:
        program: Compilable = self.read(line)
        python: str = self.compiler.compile(program)
        return python

    def read_expression(self, line: str) -> Expression:
        program = self.read(line)
        assert len(program) == 1 and isinstance(program[0], ExpressionLine)
        return program[0].expr

    def resolve_expression(self, expr: Expression) -> Atom:
        return self.compiler.resolve(expr)

    def read(self, line: str) -> Compilable:
        tree = self.parser.parse(line)
        program: Compilable = self.transformer.transform(tree)

        return program
