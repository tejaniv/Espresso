import sys
sys.path.append("../../Espresso")

from parser import *
from lexer import *

from enum import Enum

class Bool(Enum):
    Asleep = 0
    Awake = 1

class Variable_Types(Enum):
    VT_INT      = 1
    VT_FLOAT    = 2
    VT_STRING   = 3
    VT_FUNCTION = 4

class Variable:
    def __init__(self, name : str, type : Variable_Types, value) -> None:
        self.name = name
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return f"{self.type.name} {self.name}: {self.value}"

##############################
# Interpreter
##############################
class Interpreter:
    def __init__(self) -> None:
        self.assignments = {} # List of Variable objects

    def interpret(self, tree):
        return self.visit_node(tree)
        
    def visit_node(self, node):
        print("node:", node)
        if type(node) ==  BinOp:
            return self.eval_BinOp(node)
        elif type(node) == Num:
            if (node.token.type == Token_Types.TT_IDENTIFIER) and (node.value in self.assignments.keys()):
                if (self.assignments[node.value].type in (Variable_Types.VT_INT, Variable_Types.VT_FLOAT)):
                    return float(self.assignments[node.value].value)
                else:
                    raise TypeError("Variable is not of correct type")
            return float(node.value)
        elif type(node) == IdentityOp:
            print("id")
        elif node.value is None:
            raise Exception("Incomplete expression")

    def eval_BinOp(self, node):
        print("node op:", node.op)
        match node.op:
            case "+":
                if node.left is None:
                    return self.visit_node(node.right)
                else:
                    return self.visit_node(node.left) + self.visit_node(node.right)
            case "-":
                if node.left is None:
                    return -self.visit_node(node.right)
                else:
                    return self.visit_node(node.left) - self.visit_node(node.right)
            case "*":
                return self.visit_node(node.left) * self.visit_node(node.right)
            case "/":
                return self.visit_node(node.left) / self.visit_node(node.right)
            case "^":
                return self.visit_node(node.left) ** self.visit_node(node.right)
            case "//":
                return (self.visit_node(node.left) // self.visit_node(node.right))
            case "%":
                return self.visit_node(node.left) % self.visit_node(node.right)
            case "==":
                # Boolean Operator
                return Bool(self.visit_node(node.left) == self.visit_node(node.right)).name
            case "=":
                return self.process_assignment(node)

    def process_assignment(self, node):
        print("processing assignment")
        
        value = self.visit_node(node.right)
        
        # Assume the below is true
        #if type(node.right) == Num:
        #    var_type = Variable_Types.VT_FLOAT

        var = Variable(name = node.left.value, type = Variable_Types.VT_FLOAT, value = value)

        self.assignments[node.left.value] = var
