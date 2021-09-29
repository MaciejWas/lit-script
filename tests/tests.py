# TODO: do not use unittest for functional tests

import unittest
import os

from lit_script import Interpreter

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

if __name__ == '__main__':
    unittest.main()