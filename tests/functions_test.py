import sys

sys.path.append(".")

from lit_script import core
from lit_script import Interpreter


# Setting environment

c = core.Context()
core.Expression.set_global_context(c)

for name, fn in core.inbuilt_functions.items():
    core.add_function_to_context(fn, name)

TESTS_LOCATION = "language/tests"


# Helpers


def make_atom(value: int):
    return core.Atom(value=value, type="Int")


class TestInbuiltFuncs:
    def test_decides(self):
        interpreter = Interpreter()

        a: core.Expression = interpreter.read_expression("decides")
        assert a.resolve().is_function

        a: core.Expression = interpreter.read_expression("1 `decides` 4 8")
        result = a.resolve()
        assert result.value == 4

        a: core.Expression = interpreter.read_expression("0 `decides` 4 8")
        result = a.resolve()
        assert result.value == 8

    def test_add(self):
        a = make_atom(100)

        e = core.FunctionCallExpression(
            core.FunctionCall(
                fun=core.VariableExpression(core.Variable(name="add")),
                arg=core.AtomExpression(a),
            )
        )

        e2 = core.FunctionCallExpression(
            core.FunctionCall(
                fun=e,
                arg=core.AtomExpression(a),
            )
        )

        result: core.Atom = e2.resolve()

        assert result.value == 200

    def test_mul(self):
        a = make_atom(100)

        e = core.FunctionCallExpression(
            core.FunctionCall(
                fun=core.VariableExpression(core.Variable(name="mul")),
                arg=core.AtomExpression(a),
            )
        )

        e2 = core.FunctionCallExpression(
            core.FunctionCall(
                fun=e,
                arg=core.AtomExpression(a),
            )
        )

        result: core.Atom = e2.resolve()

        assert result.value == 100 * 100

    def test_incr(self):
        a = make_atom(100)

        e = core.FunctionCallExpression(
            core.FunctionCall(
                fun=core.VariableExpression(core.Variable(name="increase")),
                arg=core.AtomExpression(a),
            )
        )

        result: core.Atom = e.resolve()

        assert result.value == 100 + 100

    def test_neg(self):
        a = make_atom(100)

        e = core.FunctionCallExpression(
            core.FunctionCall(
                fun=core.VariableExpression(core.Variable(name="neg")),
                arg=core.AtomExpression(a),
            )
        )

        result: core.Atom = e.resolve()

        assert result.value == -1 * 100
