import string
from parser import *

class Token:
    def __init__(self, type, value: string, line: int) -> None:
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self) -> str:
        return f"({self.type}: {self.value})"

class Tokenizer:
    def __init__(self) -> None:
        self.tokens = []
        
    
    def tokenize(self, file):
        self.file = open(file, "r")

        # Do the tokenizing

        self.file.close()
