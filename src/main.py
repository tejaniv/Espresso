import sys

from lexer import *
from parser import *
from interpreter import *

def process_terminal(line):
    print(line)

    # Create tokens
    lexer = Lexer()
    tokens, error = lexer.tokenize(line)

    print("vvv TOKENS vvv")
    print(tokens)
    print()

    # Run them through parser
    parser = Parser()
    tree = parser.create_AST(tokens)
    
    print("vvv TREE vvv")
    print(tree)
    print()

    # Evaluate
    interpreter = Interpreter()
    result = interpreter.interpret(tree)

    print ("vvv INTERPRETER vvv")
    print("Result: " , result)
    print()

def process_file(file):
    pass
    # create tokens
    # run through parser
    # evaluate

def run_terminal():
    print("Welcome to the Espresso Terminal! \nEnter .q or .quit to exit the terminal")
    user_input = '1 * 2 + 4'
    run_terminal = True
    
    while run_terminal:
        user_input = input("Esp >> ")
        if (not user_input.strip() == ".q") and (not user_input.strip() == ".quit"):        
            process_terminal(user_input)
        else:
            run_terminal = False
        
    

if __name__ == "__main__":
    # Use sys.argv[x] to take input. Could use for file input
    # sys.argv[0] will always be "./espresso" when running Espresso
    print("Welcome to Espresso")

    if len(sys.argv) == 1:
        run_terminal()
    #elif len(sys.argv) == 2:
    #    process_file(sys.argv[1])
