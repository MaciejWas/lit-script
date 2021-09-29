from lark import Transformer, TransformerChain

def create_transformer() -> TransformerChain:
    return (
        TerminalTransformer() *
        ExpressionTransformer() *
        FinalTransformer()
    )

class TerminalTransformer(Transformer):
    def STRING(self, x):
        pass
    
    def ESPCAPED_STRING(self, x):
        pass

    def NUMBER(self, x):
        pass


class ExpressionTransformer(Transformer):
    
    def expression(self, x):
        pass

    def new_variable(self, x):
        pass

    def variable(self, x):
        pass

    def value(self, x):
        pass

    def function_call(self, x):
        pass

    def function(self, x):
        pass

    def function_arg(self, x):
        pass


class FinalTransformer(Transformer):

    def all(self, x):
        pass

    def line(self, x):
        pass

    def definition(self, x):
        pass

    def declaration(self, x):
        pass
