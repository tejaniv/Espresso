import sys

from lexer import *
from parser import *

def process_terminal(line):
    print(line)
    lexer.tokenize(line)
    # Create tokens
    # Run them through parser
    # Evaluate

def process_file(file):
    pass
    # create tokens
    # run through parser
    # evaluate

def run_terminal():
    print("Welcome to the Espresso Terminal! \nEnter .q or .quit to exit the terminal")
    user_input = ""

    while (not user_input.strip() == ".q") and (not user_input.strip() == ".quit"):
        user_input = input("Esp >> ")
        process_terminal(user_input)
    

if __name__ == "__main__":
    # Use sys.argv[x] to take input. Could use for file input
    # sys.argv[0] will always be "./espresso" when running Espresso
    
    lexer = Lexer()

    #if len(sys.argv) == 1:
    #    run_terminal()
    #elif len(sys.argv) == 2:
    #    process_file(sys.argv[1])

    print("Welcome to Espresso")