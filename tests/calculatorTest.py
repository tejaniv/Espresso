import unittest
import sys

sys.path.append("../../Espresso")

from src.interpreter import *
from src.parser import *
from src.lexer import *

class CalculatorTest(unittest.TestCase):

    def test1(self):
        print("hello")

if __name__ == "__main__":
    unittest.main()