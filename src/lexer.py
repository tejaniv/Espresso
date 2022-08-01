from string import digits
from parser import *
from enum import Enum


##############################
# TOKEN
##############################

class Token_Types(Enum):
    TT_IDENTIFIER       = 1
    TT_KEYWORD          = 2
    TT_SEPARATOR        = 3
    TT_OPERATOR         = 4
    TT_LITERAL          = 5
    TT_COMMENT          = 6

class Token:
    def __init__(self, type, kind = None, value = None) -> None:
        self.type = type
        self.value = value
        self.kind = kind
        self.line = 1

    def __repr__(self) -> str:
        if self.kind and self.value:
            return f"({self.type} - {self.kind}: '{self.value}') "
        elif self.value and not self.kind: 
            return f"({self.type}: '{self.value}')"
        elif self.kind and not self.value:
            return f"({self.type} - {self.kind})"
        return f"{self.type}"


##############################
# LEXER
##############################
        
class Lexer:
    def __init__(self) -> None:
        self.tokens = []
        
        self.keywords = {
            'print': "PRINT"
        }
        self.separators = {
            '(': "LPAREN",
            ')': "RPAREN",
        }
        self.operators = {
            '+': "PLUS",
            '-': "MINUS",
            '*': "MUL",
            '/': "DIV",
        }
        self.literals = {
            'int': "INT",
            'float': "FLOAT",
            'bool': "BOOLEAN",
            'str': "STRING",
            'list': "LIST",
            'char': "CHARACTER"
        }

        self.booleans = ["true", "false"]

    def tokenize_terminal(self, line):
        first_index = 0
        temp_type = ''
        self.pos = 0
        self.cur_char = None

        while self.pos <= len(line)-1:
            print()
            print("pos: ", self.pos)
            print("new char: ", line[self.pos])
            if line[self.pos] == ' ' or line[self.pos] == '\t':
                print("space found")
                self.cur_char = None
                temp_type = ''
                self.pos += 1
            else:
                self.cur_char = line[self.pos]
                temp_type, temp_kind = self.find_type(self.cur_char)

                first_index = self.pos
                
                self.find_end_of_type(temp_type, temp_kind, line)

                print("first: ", first_index, " last: ", self.pos)
                print("sub-line", line[first_index:self.pos])
                print("temp_type: ", temp_type)

            if temp_type == Token_Types.TT_LITERAL:
                self.tokens.append(Token(temp_type, line[first_index:self.pos]))
            elif temp_type == Token_Types.TT_OPERATOR:
                self.tokens.append(Token(temp_type, temp_kind, line[first_index:self.pos]))
            
            temp_type = ''
            
        print(self.tokens)
            
    def find_type(self, temp_str):
        print("temp_str: ", temp_str)
        #print("is numeric: ",temp_str.isnumeric())
        print("operator?: ", ('+' in self.operators))

        if temp_str in self.keywords:
            return Token_Types.TT_KEYWORD, self.keywords[temp_str]
        elif temp_str in self.separators:
            return Token_Types.TT_SEPARATOR, self.separators[temp_str]
        elif temp_str in self.operators:
            return Token_Types.TT_OPERATOR, self.operators[temp_str]
        elif (temp_str.isnumeric()) or (temp_str in self.booleans):
            return Token_Types.TT_LITERAL, "INT" # Change later
        else:
            return Token_Types.TT_IDENTIFIER, None
         

    def find_end_of_type(self, type, kind, line):
        print("finding end for ", type, " type")
        temp_str = ''
        cur_type = type
        cur_kind = kind

        while (type == cur_type) and (kind == cur_kind) and (self.pos <= len(line)-1):
            temp_str += line[self.pos]
            cur_type, cur_kind = self.find_type(temp_str)
            self.pos += 1

        print("new pos: ", self.pos)
