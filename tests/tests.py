# TODO: do not use unittest for functional tests

import unittest
import os

from lit_script import Interpreter
import lit_script.expressions as ex

TESTS_LOCATION = "language/tests"

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

        def increase(a: ex.Atom):
            x = a.value
            return ex.Atom(
                value=a.value + 100,
                type="Int"
            )

        increase_fn = ex.Function(
            argument=ex.Variable(name="x"),
            expression=ex.Expression(),
            override=increase
        )

        self.assertEqual(
            increase_fn(ex.Atom(value=100, type="Int")),
            ex.Atom(value=200, type="Int")
        )

        ex.Expression.context.add_variable(
            ex.Variable(name="increase"),
            ex.AtomExpression(atom=increase_fn)
        )

    def test_call_function(self):
        def increase(a: ex.Atom):
            return ex.Atom(
                value=a.value + 100,
                type="Int"
            )

        increase_fn = ex.Function(
            argument=ex.Variable(name="x"),
            expression=ex.Expression(),
            override=increase
        )

        ex.Expression.context.add_variable(
            ex.Variable(name="increase"),
            ex.AtomExpression(atom=increase_fn)
        )
        
        
        e = ex.FunctionCallExpression(
            fncall=ex.FunctionCall(
                fun=ex.VariableExpression(ex.Variable(name="increase")),
                arg=ex.AtomExpression(ex.Atom(value=100, type="Int"))
            )
        )

        result = e.resolve()

        self.assertIsInstance(result, ex.Atom)
        self.assertEqual(result.value, 200)


if __name__ == '__main__':
    unittest.main()