from lark import Lark, TransformerChain

from .transformer import create_transformer

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
