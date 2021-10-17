import sys

sys.path.append(".")

from lit_script import core, Interpreter


TESTS_LOCATION = "language/tests"

interpreter = Interpreter()


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

        result = interpreter.resolve_expression(e)

        assert isinstance(result, core.Atom)
        assert result.value == 200

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

        interpreter.resolve_expression(e)

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

        interpreter.resolve_expression(e3)
