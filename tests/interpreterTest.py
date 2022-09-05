import unittest
import sys

sys.path.append("../../Espresso")

from src.interpreter import *
from src.parser import *
from src.lexer import *

class InterpreterTest(unittest.TestCase):

    '''Test simple addition'''
    def test_simple_addition(self):
        i = Interpreter()

        tok_l = Token(type=Token_Types.TT_LITERAL, kind="INT", value="3")
        ast_l = Num(tok_l)

        tok_op = Token(type=Token_Types.TT_OPERATOR, kind="PLUS", value="+")
        
        tok_r = Token(type=Token_Types.TT_LITERAL, kind="INT", value="2")
        ast_r = Num(tok_r)
        
        tree = BinOp(ast_l, tok_op, ast_r)
        print(tree)

        result = i.interpret(tree)
        
        self.assertEqual(result, 5.0)

    '''Manually add a variable to the assignments dictionary and try addition with it'''
    def test_variable_addition1(self):
        i = Interpreter()
        i.assignments["x"] = Variable(name="x", type=Variable_Types.VT_INT, value="3")

        tok_l = Token(type=Token_Types.TT_IDENTIFIER, kind="IDENTIFIER", value="x")
        ast_l = Num(tok_l)

        tok_op = Token(type=Token_Types.TT_OPERATOR, kind="PLUS", value="+")
        
        tok_r = Token(type=Token_Types.TT_LITERAL, kind="INT", value="2")
        ast_r = Num(tok_r)
        
        tree = BinOp(ast_l, tok_op, ast_r)
        print(tree)

        result = i.interpret(tree)
        
        self.assertEqual(result, 5.0)
        
    '''Check that error is raised when an invalid type is passed into an addition operation'''
    def test_invalid_variable_type(self):
        i = Interpreter()
        i.assignments["x"] = Variable(name='x', type=Variable_Types.VT_STRING, value="hello") 

        tok_l = Token(type=Token_Types.TT_IDENTIFIER, kind="IDENTIFIER", value="x")
        ast_l = Num(tok_l)

        tok_op = Token(type=Token_Types.TT_OPERATOR, kind="PLUS", value="+")
        
        tok_r = Token(type=Token_Types.TT_LITERAL, kind="INT", value="2")
        ast_r = Num(tok_r)
        
        tree = BinOp(ast_l, tok_op, ast_r)
        
        self.assertRaises(TypeError, i.interpret, tree) 

    def test_int_declaration(self):
        i = Interpreter()

        tok_l = Token(type=Token_Types.TT_IDENTIFIER, kind="IDENTIFIER", value="x")
        ast_l = IdentityOp(tok_l)

        tok_op = Token(type=Token_Types.TT_OPERATOR, kind="DECLARE", value="=")

        tok_r = Token(type=Token_Types.TT_LITERAL, kind="INT", value="3")
        ast_r = Num(tok_r)

        tree = BinOp(ast_l, tok_op, ast_r)
        i.interpret(tree)

        tok_l2 = Token(type=Token_Types.TT_IDENTIFIER, kind="IDENTIFIER", value="x")
        ast_l2 = Num(tok_l2)

        tok_op2 = Token(type=Token_Types.TT_OPERATOR, kind="PLUS", value="+")
        
        tok_r2 = Token(type=Token_Types.TT_LITERAL, kind="INT", value="2")
        ast_r2 = Num(tok_r2)
        
        tree2 = BinOp(ast_l2, tok_op2, ast_r2) 
        result = i.interpret(tree2)

        self.assertEquals(result, 5.0)

if __name__ == "__main__":
    unittest.main()