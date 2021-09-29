from lark import Lark

class Interpreter:
    def __init__(self):
        self.parser: Lark = self.load_parser()
        
    def load_parser(self) -> Lark:
        with open("language/grammar.lark", "r") as f:
            grammar = f.read()
        return Lark(grammar, start="all")

    def read(self, line: str):
        tree = self.parser(line)
        print(tree.pretty())
