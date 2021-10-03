import os, sys

sys.path.append(".")

import pytest

from src import Interpreter, codecov_test
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


def add_to_context(name: str, value: int):
    atom = make_atom(value=value)
    var = ex.Variable(name=name)
    ex.Expression.add_to_global_context(var, ex.AtomExpression(atom=atom))


# Tests


class TestLitScript:
    def test_codecov(self):
        codecov_test()

    def test_create_interpreter(self):
        Interpreter()

    def test_interpreter_read(self):
        interpreter = Interpreter()

        for file in os.listdir(TESTS_LOCATION):
            test_file_path = os.path.join(TESTS_LOCATION, file)

            with open(test_file_path, "r") as f:
                code = f.read()
                interpreter.read(code)


class TestAtoms:
    def test_dunders(self):
        a = ex.Atom(value=1, type="Int")
        b = ex.Atom(value="1", type="Str")

        assert a != b

        with pytest.raises(NotImplementedError):
            a + b


class TestExpressions:
    def test_create_function(self):

        id_fn = ex.Function.from_python_fn(fn=lambda x: x)

        a = make_atom(100)

        assert id_fn(a) == ex.Atom(value=100, type="Int")

    def test_call_function_from_context(self):

        a = make_atom(100)

        e = ex.FunctionCallExpression(
            fncall=ex.FunctionCall(
                fun=ex.VariableExpression(ex.Variable(name="increase")),
                arg=ex.AtomExpression(a),
            )
        )

        result = e.resolve()

        assert isinstance(result, ex.Atom)
        assert result.value == 200

    def test_context(self):
        ex.Expression.add_to_global_context(
            ex.Variable(name="maciek"),
            expr=ex.AtomExpression(atom=ex.Atom(value=3, type="Int")),
        )

        e = ex.VariableExpression(variable=ex.Variable(name="maciek"))
        result = e.resolve()

        assert isinstance(result, ex.Atom)
        assert result.value == 3

    def test_curried_fncs(self):

        # Inside expression
        add_reference = ex.VariableExpression(variable=ex.Variable(name="add"))
        argument = ex.AtomExpression(make_atom(100))
        inside_e = ex.FunctionCallExpression(
            fncall=ex.FunctionCall(fun=add_reference, arg=argument)
        )

        # Whole expression
        e = ex.FunctionCallExpression(
            fncall=ex.FunctionCall(fun=inside_e, arg=ex.AtomExpression(make_atom(200)))
        )

        e.resolve()

    def test_nested_funcs(self):

        # 1
        add_reference = ex.VariableExpression(variable=ex.Variable(name="add"))
        argument = ex.AtomExpression(atom=make_atom(100))
        e1 = ex.FunctionCallExpression(
            fncall=ex.FunctionCall(fun=add_reference, arg=argument)
        )

        # 2
        e2 = ex.FunctionCallExpression(
            fncall=ex.FunctionCall(fun=e1, arg=ex.AtomExpression(atom=make_atom(200)))
        )

        # 3
        inside_e3 = ex.FunctionCallExpression(
            fncall=ex.FunctionCall(
                fun=ex.VariableExpression(variable=ex.Variable(name="add")), arg=e2
            )
        )

        e3 = ex.FunctionCallExpression(
            fncall=ex.FunctionCall(fun=inside_e3, arg=ex.AtomExpression(make_atom(300)))
        )

        e3.resolve()
