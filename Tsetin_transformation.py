from CNF_formula import Literal
from CNF_formula import Clause



class TsetinTransformation:

    def __init__(self, max_var_name):
        var_name = max_var_name

    def generate_name(self):
        self.var_name+=1
        return self.var_name

    def basic_var_not(self, var):
        y = Literal(self.generate_name())
        c = Clause()
        c.append(y)
        negY =













