import sys
sys.path.append("../../Espresso")


from lexer import *
from parser import *
from interpreter import *

def process_terminal(line):
    print(line)

    # Create tokens

    print("vvv TOKENS vvv")
    tokens, error = lexer.tokenize(line)
    print(tokens)
    print()

    # Run them through parser
    
    print("vvv TREE vvv")
    tree = parser.create_AST(tokens)
    print(tree)
    print()

    # Evaluate

    print ("vvv INTERPRETER vvv")
    result = interpreter.interpret(tree)
    print("variable assignments: ", interpreter.assignments)
    print("Result: " , result)
    print()

def process_file(file):
    f = open(file, 'r')
    for line in f:
    # create tokens
        tokens, error = lexer.tokenize(line.strip())
    # run through parser
        tree = parser.create_AST(tokens)
    # evaluate
        result = interpreter.interpret(tree)
        print(interpreter.assignments)

def run_terminal():
    print("Welcome to the Espresso Terminal! \nEnter .q or .quit to exit the terminal")
    user_input = ''
    run_terminal = True
    
    while run_terminal:
        user_input = input("Esp >> ")
        if user_input == '':
            continue
        elif (not user_input.strip() == ".q") and (not user_input.strip() == ".quit"):        
            process_terminal(user_input)
        else:
            run_terminal = False
        
    

if __name__ == "__main__":
    # Use sys.argv[x] to take input. Could use for file input
    # sys.argv[0] will always be "./espresso" when running Espresso
    print("Welcome to Espresso")

    lexer = Lexer()
    parser = Parser()
    interpreter = Interpreter()
    
    if len(sys.argv) == 1:
        run_terminal()
    elif len(sys.argv) == 2:
        process_file(sys.argv[1])
