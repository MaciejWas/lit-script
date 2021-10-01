from lark import Lark
from lark.visitors import TransformerChain

from .transformer import create_transformer


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
        self.parser: Lark = self.load_parser()
        self.transformer: TransformerChain = self.load_transformer()

    def load_parser(self) -> Lark:
        with open("language/grammar.lark", "r") as f:
            grammar = f.read()
        return Lark(grammar, start="all")

    def load_transformer(self) -> TransformerChain:
        return create_transformer()

    def read(self, line: str):
        tree = self.parser.parse(line)
        print(tree.pretty())

        transformed_tree = self.transformer.transform(tree)
        print(transformed_tree)
