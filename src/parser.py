from lexer import *

##############################
# Abstract Syntax Tree
##############################
class AST:
    def __init__(self) -> None:
        pass

class BinOp(AST):
    def __init__(self, left:Token, op:Token, right:Token) -> None:
        self.left = left
        self.token = op
        self.op = op.value
        self.right = right
    
    def __repr__(self) -> str:
        return f"{self.left} \n{self.op} \n  {self.right}"

class Num(AST):
    def __init__(self, token : Token) -> None:
        self.token = token
        self.value = token.value
    
    def __repr__(self) -> str:
        return f"{self.value}"

##############################
# Parser
##############################
class Parser:
    def __init__(self) -> None:
        pass

    def create_AST(self, token_list) -> AST:
        self.tokens = iter(token_list)
        self.current_token = self.get_next_token()
        print("cur_tok: ", self.current_token)

        return self.parse_expr()

    def advance(self, cur_kind):
        if self.current_token.kind == cur_kind:
            self.current_token = self.get_next_token()
            print("cur_tok: ", self.current_token)
        else:
            raise Exception('Invalid Syntax')
        
    
    def parse_factor(self):
        """
        factor : INT | LPAREN expr RPAREN
        """

        token = self.current_token
        if token.kind == "INT":
            self.advance("INT")
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

        while self.current_token.kind in ("MUL", "DIV"):
            token = self.current_token

            if token.kind == "MUL":
                self.advance("MUL")
            elif token.kind == "DIV":
                self.advance("DIV")

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

            if token.kind == "PLUS":
                self.advance("PLUS")
            elif token.kind == "MINUS":
                self.advance("MINUS")

            node = BinOp(left=node, op=token, right=self.parse_term())

        return node

    def get_next_token(self):
        return next(self.tokens)
