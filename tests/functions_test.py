import sys

sys.path.append(".")

import src.expressions as ex


# Setting environment

c = ex.Context()
ex.Expression.set_global_context(c)

for name, fn in ex.inbuilt_functions.items():
    ex.add_function_to_context(fn, name)

TESTS_LOCATION = "language/tests"


# Helpers


def make_atom(value: int):
    return ex.Atom(value=value, type="Int")


class TestInbuiltFuncs:
    def test_add(self):
        a = make_atom(100)

        e = ex.FunctionCallExpression(
            ex.FunctionCall(
                fun=ex.VariableExpression(ex.Variable(name="add")),
                arg=ex.AtomExpression(a),
            )
        )

        e2 = ex.FunctionCallExpression(
            ex.FunctionCall(
                fun=e,
                arg=ex.AtomExpression(a),
            )
        )

        result: ex.Atom = e2.resolve()

        assert result.value == 200

    def test_mul(self):
        a = make_atom(100)

        e = ex.FunctionCallExpression(
            ex.FunctionCall(
                fun=ex.VariableExpression(ex.Variable(name="mul")),
                arg=ex.AtomExpression(a),
            )
        )

        e2 = ex.FunctionCallExpression(
            ex.FunctionCall(
                fun=e,
                arg=ex.AtomExpression(a),
            )
        )

        result: ex.Atom = e2.resolve()

        assert result.value == 100 * 100

    def test_incr(self):
        a = make_atom(100)

        e = ex.FunctionCallExpression(
            ex.FunctionCall(
                fun=ex.VariableExpression(ex.Variable(name="increase")),
                arg=ex.AtomExpression(a),
            )
        )

        result: ex.Atom = e.resolve()

        assert result.value == 100 + 100

    def test_neg(self):
        a = make_atom(100)

        e = ex.FunctionCallExpression(
            ex.FunctionCall(
                fun=ex.VariableExpression(ex.Variable(name="neg")),
                arg=ex.AtomExpression(a),
            )
        )

        result: ex.Atom = e.resolve()

        assert result.value == -1 * 100
