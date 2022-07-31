from lexer import *

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.AST = []