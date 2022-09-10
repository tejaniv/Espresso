from inspect import ArgSpec
import sys
sys.path.append("../../Espresso")


class BuiltInFunctions:

    def __init__(self) -> None:
        self.function_list = {
            "print": self.function_print,
            "add"  : self.function_add
        }

    def function_print(self, args) -> None:
        print("print output:")
        for arg in args:
            string = str(arg) + " "
        print(string.strip())
    
    def function_add(self, args):
        print("add output") 
        val = 0
        for arg in args:
            val += arg
        return val