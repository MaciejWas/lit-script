import os, sys

sys.path.append(".")

import pytest

from lit_script import Interpreter
from lit_script import core


TESTS_LOCATION = "language/tests"


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
                interpreter.compile(code)


class TestAtoms:
    def test_dunders(self):
        a = core.Atom(value=1, type="Int")
        b = core.Atom(value="1", type="Str")

        assert a != b

        with pytest.raises(NotImplementedError):
            a + b
