# TODO: do not use unittest for functional tests

from lit_script.transformer import ExpressionTransformer
import unittest
import os

from lit_script import Interpreter
import lit_script.expressions as ex

TESTS_LOCATION = "language/tests"


def make_atom(value: int):
    return ex.Atom(value=value, type="Int")

def add_int_to_context(name: str, value: int):
    atom = make_atom(value=value)
    var = ex.Variable(name=name)
    ex.Expression.context.add_variable(var, ex.AtomExpression(atom=atom))

def increase(a: ex.Atom):
    x = a.value
    return ex.Atom(
        value=x + 100,
        type="Int"
    )

def add(a: ex.Atom): # TODO This is a fucnking mess

    def half_add(b: ex.Atom):
        return ex.Atom(value=b.value + a.value, type="Int")

    half_add = ex.Function.from_python_fn(half_add)
    
    return ex.Atom(value=half_add, type="Function")


class TestLitScript(unittest.TestCase):

    def test_create_interpreter(self):
        interpreter = Interpreter()

    def test_interpreter_read(self):
        interpreter = Interpreter()

        for file in os.listdir(TESTS_LOCATION):
            test_file_path = os.path.join(TESTS_LOCATION, file)
            with open(test_file_path, "r") as f:
                code = f.read()
                interpreter.read(code)


class TestExpressions(unittest.TestCase):
    
    def test_create_function(self):

        increase_fn = ex.Function.from_python_fn(func=increase)

        a = make_atom(100)

        self.assertEqual(
            increase_fn(a),
            ex.Atom(value=200, type="Int")
        )

    def test_call_function_from_context(self):

        increase_fn = ex.Function.from_python_fn(func=increase)

        ex.Expression.context.add_variable(
            ex.Variable(name="increase"),
            ex.AtomExpression(atom=increase_fn)
        )
        
        a = make_atom(100)

        e = ex.FunctionCallExpression(
            fncall=ex.FunctionCall(
                fun=ex.VariableExpression(ex.Variable(name="increase")),
                arg=ex.AtomExpression(a)
            )
        )

        result = e.resolve()

        self.assertIsInstance(result, ex.Atom)
        self.assertEqual(result.value, 200)

    def test_context(self):
        ex.Expression.context.add_variable(
            ex.Variable(name="maciek"),
            expr=ex.AtomExpression(atom=ex.Atom(value=3, type="Int"))
        )

        e = ex.VariableExpression(variable=ex.Variable(name="maciek"))
        result = e.resolve()
        
        self.assertIsInstance(result, ex.Atom)
        self.assertEqual(result.value, 3)

    def test_curried_fncs(self):
        # make the function usable
        add_fn = ex.Function.from_python_fn(func=add)

        # Create add atom
        fn_atom = ex.Atom(value=add_fn, type="Function")

        # Record add
        ex.Expression.context.add_variable(
            var=ex.Variable(name="add"),
            expr=ex.AtomExpression(atom=fn_atom)
        )

        # Inside expression
        add_reference = ex.VariableExpression(variable=ex.Variable(name="add"))
        argument = ex.AtomExpression(make_atom(100))
        inside_e = ex.FunctionCallExpression(fncall=ex.FunctionCall(fun=add_reference, arg=argument))
        
        # Whole expression
        e = ex.FunctionCallExpression(fncall=ex.FunctionCall(
            fun = inside_e,
            arg = ex.AtomExpression(make_atom(200))
        ))

        e.resolve()

    def test_nested_funcs(self):
        # make the function usable
        add_fn = ex.Function.from_python_fn(func=add)

        # Create add atom
        fn_atom = ex.Atom(value=add_fn, type="Function")

        # Record add
        ex.Expression.context.add_variable(
            var=ex.Variable(name="add"),
            expr=ex.AtomExpression(atom=fn_atom)
        )

        # 1
        add_reference = ex.VariableExpression(variable=ex.Variable(name="add"))
        argument = ex.AtomExpression(atom=make_atom(100))
        e1 = ex.FunctionCallExpression(fncall=ex.FunctionCall(fun=add_reference, arg=argument))
        
        # 2
        e2 = ex.FunctionCallExpression(fncall=ex.FunctionCall(
            fun = e1,
            arg = ex.AtomExpression(atom=make_atom(200))
        ))

        # 3
        inside_e3 = ex.FunctionCallExpression(fncall=ex.FunctionCall(
            fun = ex.AtomExpression(atom=fn_atom),
            arg = e2
        ))

        e3 = ex.FunctionCallExpression(fncall=ex.FunctionCall(
            fun = inside_e3,
            arg = ex.AtomExpression(make_atom(300))
        ))

        e3.resolve()

if __name__ == '__main__':
    unittest.main()