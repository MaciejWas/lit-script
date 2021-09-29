import unittest

from lit_script import Interpreter

class TestLitScript(unittest.TestCase):

    def test_create_interpreter(self):
        interpreter = Interpreter()

if __name__ == '__main__':
    unittest.main()