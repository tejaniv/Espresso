import sys
sys.path.append("../../Espresso")

from lexer import *

##############################
# Abstract Syntax Tree
##############################
class AST:
    def __init__(self) -> None:
        pass

class BinOp(AST):
    def __init__(self, left:AST, op:Token, right:AST) -> None:
        self.left = left 
        self.token = op
        self.op = op.value
        self.right = right
    
    def __repr__(self) -> str:
        return f"({self.left} {self.op} {self.right})"

class Num(AST):
    def __init__(self, token : Token) -> None:
        self.token = token
        self.value = token.value
    
    def __repr__(self) -> str:
        return f"{self.value}"

class IdentityOp(AST):
    def __init__(self, token : Token) -> None:
        self.token = token
        self.value = token.value

    def __repr__(self) -> str:
        return f"{self.value}"

class FunctionCall(AST):
    def __init__(self, token : Token, parameters : AST) -> None:
        self.token = token
        self.value = token.value
        self.parameters = parameters

    def __repr__(self):
        return f"{self.value} ({self.parameters})"

class ParametersNode(AST):
    def __init__(self, node : AST, next : AST) -> None:
        self.node = node
        self.next = next
        self.value = node
    
    def __repr__(self) -> str:
        return f"{self.node} | {self.next}" if self.next is not None else f"{self.node}"


##############################
# Parser
##############################
class Parser:
    def __init__(self) -> None:
        pass

    def create_AST(self, token_list) -> AST:
        self.token_list = token_list
        self.tokens = iter(token_list)

        self.current_token = self.get_next_token
        print("cur_tok: ", self.current_token)

        return self.parse_declare()

    def advance(self, cur_kind):
        if self.current_token.kind == cur_kind:
            self.current_token = self.get_next_token
            print("cur_tok: ", self.current_token)
        else:
            raise Exception('Invalid Syntax')
        
    
    def parse_factor(self):
        """
        factor : INT | LPAREN expr RPAREN
        """

        token = self.current_token
        print("tok kind:" , token.type)
        if token.kind == "INT":
            self.advance("INT")
            return Num(token)

        elif token.kind == "FLOAT":
            self.advance("FLOAT")
            return Num(token)

        elif token.type == Token_Types.TT_IDENTIFIER:
            self.advance("IDENTIFIER")
            
            if self.current_token.kind == "LPAREN":
                return FunctionCall(token=token, parameters=self.process_parameters())

            return Num(token)

        elif token.kind == "LPAREN":
            self.advance("LPAREN")
            node = self.parse_expr()
            self.advance("RPAREN")
            return node

    def parse_exp(self):
        """
        exp : factor (EXPONENT factor)*
        factor : INT | LPAREN expr RPAREN
        """

        node = self.parse_factor()

        while self.current_token.kind == "EXPONENT":
            token = self.current_token
            self.advance("EXPONENT")
            node = BinOp(left=node, op=token, right=self.parse_factor())
            
        return node

    def parse_term(self):
        """
        term : exp ((MUL|DIV) exp)*
        exp : factor (EXPONENT factor)*
        factor : INT | LPAREN expr RPAREN
        """

        node  = self.parse_exp()

        while self.current_token.kind in ("MUL", "DIV", "MOD", "FLOOR"):
            token = self.current_token

            if token.kind == "MUL":
                self.advance("MUL")
            elif token.kind == "DIV":
                self.advance("DIV")
            elif token.kind == "MOD":
                self.advance("MOD")
            elif token.kind == "FLOOR":
                self.advance("FLOOR")

            node = BinOp(left=node, op=token, right=self.parse_exp())
        
        return node

    def parse_expr(self):
        """
        expr : term ((PLUS|MINUS) term)*
        term : exp ((MUL|DIV) exp)*
        exp : factor (EXPONENT factor)*
        factor : INT | LPAREN expr RPAREN
        """

        node = self.parse_term()

        while self.current_token.kind in ("PLUS", "MINUS"):
            token = self.current_token
            print("tok: ", token)

            if token.kind == "PLUS":
                self.advance("PLUS")
            elif token.kind == "MINUS":
                self.advance("MINUS")

            node = BinOp(left=node, op=token, right=self.parse_term())

        return node

    def parse_equality(self):
        '''
        equal : expr (EQUALITY expr)*
        expr : term ((PLUS|MINUS) term)*
        term : exp ((MUL|DIV) exp)*
        exp : factor (EXPONENT factor)*
        factor : INT | LPAREN expr RPAREN
        '''
        
        node = self.parse_expr()

        while self.current_token.kind in ("EQUALITY", "LESSTHAN", "LESSEQUAL", "GREATERTHAN", "GREATEREQUAL"):
            token = self.current_token

            if token.kind == "EQUALITY":
                self.advance("EQUALITY")

            elif token.kind == "LESSTHAN":
                self.advance("LESSTHAN")
            
            elif token.kind == "LESSEQUAL":
                self.advance("LESSEQUAL")

            elif token.kind == "GREATERTHAN":
                self.advance("GREATERTHAN")

            elif token.kind == "GREATEREQUAL":
                self.advance("GREATEREQUAL")

            node = BinOp(left = node, op=token, right=self.parse_expr())

        return node

    def parse_logical(self):
        node = self.parse_equality()

        while self.current_token in ("AND", "OR"):
            token = self.current_token

            if token.kind == "OR":
                self.advance("OR")

            elif token.kind == "AND":
                self.advance("AND")
            
            node = BinOp(left = node, token = token, right = self.parse_equality())
        
        return node
    
    def parse_identifier(self):
        
        node = None
        
        print("cur tok:" , self.current_token)
        if self.current_token.type is Token_Types.TT_IDENTIFIER:
            
            node = IdentityOp(self.current_token)
            self.current_token = self.get_next_token

        return node    

    def parse_declare(self):
        '''
        dec : (name DECLARE)? equal
        name : STRING
        STRING : /\w+/ || IDENTIFIER
        '''

        node = self.parse_identifier()

        if self.current_token.kind == "DECLARE":
            token = self.current_token

            self.advance("DECLARE")    
            node = BinOp(left=node, op=token, right=self.parse_logical())
            
            return node
        else:
            self.reset_token_gen()
            return self.parse_logical()

    def process_parameters(self):
        '''
        parameters : (equality (PIPE equality)*)
        '''

        self.advance("LPAREN")
        node = self.parse_parameter()
        self.advance("RPAREN")

        print("type:" ,type(node))
        return node

    def parse_parameter(self) -> ParametersNode:
        node = self.parse_logical()
        print("should be 1: ", node)

        while self.current_token.type == Token_Types.TT_SEPARATOR and self.current_token.kind == "PIPE":
            self.advance("PIPE")
            print("found pipe")
            node = ParametersNode(node, self.parse_parameter())

        if type(node) == ParametersNode:
            return node
        elif isinstance(node, AST):
            print("here")
            return ParametersNode(node, None)
        
    @property
    def get_next_token(self):
        return next(self.tokens)

    def reset_token_gen(self):
        '''
        Since the parse_<name> functions are irreversible, we need a way to be able to parse the
        tokens is there is a variable present but not a declaration statement. To achieve this, we need
        to reset the iterator
        '''
        print("We have reset")
        self.tokens = iter(self.token_list)
        self.current_token = self.get_next_token