import unittest
import sys

sys.path.append("../../Espresso")
from src.lexer import *


class LexerTest(unittest.TestCase):
    def test_single_token(self):
        l = Lexer()
        input = "1"

        actual, _ = l.tokenize(input)
        expected = [Token(type=Token_Types.TT_LITERAL, kind="INT", value="1"),
                    Token(type=Token_Types.TT_EOF)]
        

        self.assertListEqual(expected, actual)

    def test_simple_expression1(self):
        l = Lexer()
        input = "1+2"

        actual, _ = l.tokenize(input)
        expected = [Token(Token_Types.TT_LITERAL, "INT", "1"), 
                    Token(Token_Types.TT_OPERATOR, "PLUS", "+"),
                    Token(Token_Types.TT_LITERAL, "INT", "2"),
                    Token(Token_Types.TT_EOF)] 

        self.assertListEqual(expected, actual)

    def test_equality_expression1(self):
        l = Lexer()
        input = "1==2"

        actual, _ = l.tokenize(input)
        expected = [Token(Token_Types.TT_LITERAL, "INT", "1"), 
                    Token(Token_Types.TT_OPERATOR, "EQUALITY", "=="),
                    Token(Token_Types.TT_LITERAL, "INT", "2"),
                    Token(Token_Types.TT_EOF)] 

        self.assertListEqual(expected, actual) 

    def test_simple_declaration_statement(self):
        l = Lexer()
        input = "x=2"

        actual, _ = l.tokenize(input)
        expected = [Token(type=Token_Types.TT_IDENTIFIER, kind="IDENTIFIER", value="x"),
                    Token(type=Token_Types.TT_OPERATOR, kind="DECLARE", value="="),
                    Token(type=Token_Types.TT_LITERAL, kind="INT", value="2"),
                    Token(type=Token_Types.TT_EOF)]

        self.assertListEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()