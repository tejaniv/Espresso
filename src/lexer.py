from enum import Enum
import re


##############################
# TOKEN
##############################

class Token_Types(Enum):
    TT_PROGRAM          = 1
    TT_IDENTIFIER       = 2
    TT_KEYWORD          = 3
    TT_SEPARATOR        = 4
    TT_OPERATOR         = 5
    TT_LITERAL          = 6
    TT_COMMENT          = 7
    TT_EOF              = 8

class Token:
    def __init__(self, type, kind = None, value = None, line = 1, col = 0) -> None:
        self.type = type
        self.kind = kind
        self.value = value
        self.dec_line = line
        self.dec_col = col

    def __repr__(self) -> str:
        if self.value:
            if self.kind:
                return f"({self.kind}: '{self.value}')"
            else:
                return f"({self.type}: '{self.value}')"
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
            '{': "LBRACE",
            '}': "RBRACE",
            '[': "LSQUARE",
            ']': "RSQUARE"
        }
        self.operators = {
            '+': "PLUS",
            '-': "MINUS",
            '*': "MUL",
            '/': "DIV",
            '**': "EXPONENT",
            '=': "EQUAL"
        }
        self.literals = {
            'int': "INT",
            'float': "FLOAT",
            'bool': "BOOLEAN",
            'str': "STRING",
            'list': "LIST",
            'char': "CHARACTER"
        }

        self.booleans = ["Awake", "Asleep"] #True/False

    def tokenize(self, line) -> list:
        self.pos = 0
        cur_char = ''
        temp_type = ''
        temp_kind = ''
        first_index = 0
        self.line = line
        self.tokens = []
        self.line_num = 1

        self.Error_Code = 0

        while self.pos < len(line):
            #print()
            #print("cur pos: ", self.pos)
            cur_char = line[self.pos]

            temp_type = ''
            temp_kind = ''

            if cur_char == ' ':
                #print("Skipped space")
                self.pos += 1
            else:
                #print("cur char: ", cur_char)
                temp_type, temp_kind = self.find_type(cur_char)
                first_index = self.pos

                if temp_type in (Token_Types.TT_IDENTIFIER, Token_Types.TT_KEYWORD, Token_Types.TT_LITERAL):
                    self.find_end_of_type(temp_type, temp_kind)
                else:
                    self.pos += 1

                #print("indices:", first_index, "->", self.pos)

                #print("substring: ", self.line[first_index:self.pos])

                if temp_type == Token_Types.TT_IDENTIFIER:
                    temp_type, temp_kind = self.find_type(self.line[first_index:self.pos])
                elif temp_type == Token_Types.TT_LITERAL and temp_kind == "INT":
                    #print("HERE")
                    temp_type, temp_kind = self.find_type(self.line[first_index:self.pos])
                
                if type(temp_type) == Token_Types:
                    self.tokens.append(Token(temp_type, temp_kind, self.line[first_index:self.pos].strip(), self.line_num, self.pos))

        #print(self.tokens)
        self.tokens.append(Token(Token_Types.TT_EOF))
        return self.tokens, self.Error_Code

    def find_type(self, temp_str):
        #print("temp_str: ", temp_str)
        #print("is numeric: ",temp_str.isnumeric())
        #print("operator?: ", ('+' in self.operators))

        if temp_str in self.keywords:
            return Token_Types.TT_KEYWORD, self.keywords[temp_str]
        elif temp_str in self.separators:
            return Token_Types.TT_SEPARATOR, self.separators[temp_str]
        elif temp_str in self.operators:
            return Token_Types.TT_OPERATOR, self.operators[temp_str]
        elif (temp_str.isnumeric()) or (temp_str in self.booleans) or (self.isString(temp_str)) or (self.isFloat(temp_str)):
            #print("is literal")
            return Token_Types.TT_LITERAL, self.literal_type(temp_str) 
        else:
            return Token_Types.TT_IDENTIFIER, None
         

    def find_end_of_type(self, type, kind):
        #print("finding end for potential", type, "type")
        first = self.pos
        cur_type = type
        cur_kind = kind
        temp_str = self.line[self.pos]

        while (cur_type == type) and (self.pos < len(self.line)):
            self.pos += 1
            if self.pos < len(self.line):
                temp_str = self.line[self.pos]
                cur_type, cur_kind = self.find_type(temp_str)

    def isString(self, str):
        #print("checking if string: ", str)
        str_rex = r'(\'[a-zA-Z\d]+\')|(\"[a-zA-Z\d]+)\"'
        return bool(re.search(str_rex, str))

    def isFloat(self, str):
        float_rex = r'(\d+)?\.(\d+)?'
        #print("FLOAT: " , str)

        if bool(re.search(float_rex, str)):
            return True
        return False

    def literal_type(self, str):
        #print("checking literals")
        int_rex = r'^\d+$'
        float_rex = r'^(\d+)?\.(\d+)?$'
        
        if bool(re.search(int_rex, str)):
            #print("is int")
            return self.literals['int']
        elif bool(re.search(float_rex, str)):
            #print("is float")
            return self.literals['float']
        elif str in self.booleans:
            return self.literals['bool']
        elif self.isString(str):
            return self.literals['str']
        return None

        # Use regex to determine type