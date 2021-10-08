import sys

sys.path.append(".")

from lit_script import core


# Setting environment

c = core.Context()
core.Expression.set_global_context(c)

for name, fn in core.inbuilt_functions.items():
    core.add_function_to_context(fn, name)

TESTS_LOCATION = "language/tests"


# Helpers


def make_atom(value: int):
    return core.Atom(value=value, type="Int")


class TestExpressions:
    def test_create_function(self):

        id_fn = core.Function.from_python_fn(fn=lambda x: x)

        a = make_atom(100)

        assert id_fn(a) == core.Atom(value=100, type="Int")

    def test_call_function_from_context(self):

        a = make_atom(100)

        e = core.FunctionCallExpression(
            fncall=core.FunctionCall(
                fun=core.VariableExpression(core.Variable(name="increase")),
                arg=core.AtomExpression(a),
            )
        )

        result = e.resolve()

        assert isinstance(result, core.Atom)
        assert result.value == 200

    def test_context(self):
        core.Expression.add_to_global_context(
            core.Variable(name="maciek"),
            expr=core.AtomExpression(atom=core.Atom(value=3, type="Int")),
        )

        e = core.VariableExpression(variable=core.Variable(name="maciek"))
        result = e.resolve()

        assert isinstance(result, core.Atom)
        assert result.value == 3

    def test_curried_fncs(self):

        # Inside expression
        add_reference = core.VariableExpression(variable=core.Variable(name="add"))
        argument = core.AtomExpression(make_atom(100))
        inside_e = core.FunctionCallExpression(
            fncall=core.FunctionCall(fun=add_reference, arg=argument)
        )

        # Whole expression
        e = core.FunctionCallExpression(
            fncall=core.FunctionCall(
                fun=inside_e, arg=core.AtomExpression(make_atom(200))
            )
        )

        e.resolve()

    def test_nested_funcs(self):

        # 1
        add_reference = core.VariableExpression(variable=core.Variable(name="add"))
        argument = core.AtomExpression(atom=make_atom(100))
        e1 = core.FunctionCallExpression(
            fncall=core.FunctionCall(fun=add_reference, arg=argument)
        )

        # 2
        e2 = core.FunctionCallExpression(
            fncall=core.FunctionCall(
                fun=e1, arg=core.AtomExpression(atom=make_atom(200))
            )
        )

        # 3
        inside_e3 = core.FunctionCallExpression(
            fncall=core.FunctionCall(
                fun=core.VariableExpression(variable=core.Variable(name="add")), arg=e2
            )
        )

        e3 = core.FunctionCallExpression(
            fncall=core.FunctionCall(
                fun=inside_e3, arg=core.AtomExpression(make_atom(300))
            )
        )

        e3.resolve()
