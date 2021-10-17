import sys
import pytest

sys.path.append(".")

from lit_script import core
from lit_script import Interpreter


TESTS_LOCATION = "language/tests"


# Helpers

interpreter = Interpreter()


def make_atom(value: int):
    return core.Atom(value=value, type="Int")


class TestInbuiltFuncs:
    def test_decides(self):

        a: core.Expression = interpreter.read_expression("decides")
        assert interpreter.resolve_expression(a).is_function

        a: core.Expression = interpreter.read_expression("1 `decides` 4 8")
        result = interpreter.resolve_expression(a)
        assert result.value == 4

        a: core.Expression = interpreter.read_expression("0 `decides` 4 8")
        result = interpreter.resolve_expression(a)
        assert result.value == 8

        with pytest.raises(Exception):
            a: core.Expression = interpreter.read_expression('0 `decides` "444" 8')

        with pytest.raises(Exception):
            a: core.Expression = interpreter.read_expression('0 `decides` "444" "8"')

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

        result: core.Atom = interpreter.resolve_expression(e2)

        assert result.value == 200

        with pytest.raises(Exception):
            a: core.Expression = interpreter.read_expression('add "444" "8"')

        with pytest.raises(Exception):
            a: core.Expression = interpreter.read_expression('add 1 "8"')

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

        result: core.Atom = interpreter.resolve_expression(e2)

        assert result.value == 100 * 100

        with pytest.raises(Exception):
            a: core.Expression = interpreter.read_expression('mul "444" "8"')

        with pytest.raises(Exception):
            a: core.Expression = interpreter.read_expression('mul 1 "8"')

    def test_incr(self):
        a = make_atom(100)

        e = core.FunctionCallExpression(
            core.FunctionCall(
                fun=core.VariableExpression(core.Variable(name="increase")),
                arg=core.AtomExpression(a),
            )
        )

        result: core.Atom = interpreter.resolve_expression(e)
        assert result.value == 100 + 100

    def test_neg(self):
        a = make_atom(100)

        e = core.FunctionCallExpression(
            core.FunctionCall(
                fun=core.VariableExpression(core.Variable(name="neg")),
                arg=core.AtomExpression(a),
            )
        )

        result: core.Atom = interpreter.resolve_expression(e)

        assert result.value == -1 * 100
