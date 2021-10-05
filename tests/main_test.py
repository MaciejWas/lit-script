import os, sys

sys.path.append(".")

import pytest

from lit_script import Interpreter
from lit_script import expressions as ex


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
