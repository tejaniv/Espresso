from parser import *

##############################
# Interpreter
##############################
class Interpreter:
    def __init__(self) -> None:
        pass

    def interpret(self, tree):
        return self.visit_node(tree)
        
    def visit_node(self, node):
        if type(node) ==  BinOp:
            return self.eval_BinOp(node)
        elif type(node) == Num:
            return int(node.value)
        elif node.value is None:
            raise Exception("Incomplete expression")

    def eval_BinOp(self, node):
        match node.op:
            case "+":
                return self.visit_node(node.left) + self.visit_node(node.right)
            case "-":
                return self.visit_node(node.left) - self.visit_node(node.right)
            case "*":
                return self.visit_node(node.left) * self.visit_node(node.right)
            case "/":
                return self.visit_node(node.left) / self.visit_node(node.right)
            case "^":
                return self.visit_node(node.left) ** self.visit_node(node.right)
