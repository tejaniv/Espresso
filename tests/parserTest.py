import unittest
import sys

sys.path.append("../../Espresso")

from src.parser import *
from src.lexer import *

class ParserTest(unittest.TestCase):

    def test_addition(self):
        p = Parser()

        tok_list = []

        tok_list.append(Token(type=Token_Types.TT_LITERAL, kind="INT", value="1"))
        tok_list.append(Token(type=Token_Types.TT_OPERATOR, kind="PLUS", value="+"))
        tok_list.append(Token(type=Token_Types.TT_LITERAL, kind="INT", value="2"))
        tok_list.append(Token(type=Token_Types.TT_EOF))

        realTree = p.create_AST(tok_list)
        correctTree = "(1 + 2)"

        self.assertEqual(correctTree, realTree.__repr__())
        

    def test_variable_assignment1(self):
        p = Parser()

        tok_list = []

        tok_list.append(Token(type=Token_Types.TT_IDENTIFIER, value = "x"))
        tok_list.append(Token(type=Token_Types.TT_OPERATOR, kind="DECLARE", value="="))
        tok_list.append(Token(type=Token_Types.TT_LITERAL, kind="INT", value="1"))
        tok_list.append(Token(type=Token_Types.TT_EOF))

        realTree = p.create_AST(tok_list)
        correctTree = "(x = 1)"

        self.assertEqual(correctTree, realTree.__repr__())

if __name__ == "__main__":
    unittest.main()