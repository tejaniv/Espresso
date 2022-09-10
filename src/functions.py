import sys
sys.path.append("../../Espresso")


class BuiltInFunctions:

    def __init__(self) -> None:
        self.function_list = {
            "print" : self.function_print,
            "add"   : self.function_add,
            "mul"   : self.function_mul,
            "mod"   : self.function_mod
        }

    def function_print(self, args) -> None:
        print("print output:")
        string = ""
        for arg in args:
            string += str(arg) + " "
        print(string.strip())
        return None
    
    def function_add(self, args):
        print("add output:") 
        val = 0
        for arg in args:
            val += arg
        return val

    def function_mul(self, args):
        print("mul output:")
        val = 1
        for arg in args:
            val *= arg
        return val

    def function_mod(self, args):
        pass