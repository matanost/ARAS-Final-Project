
class CNF_formula:
    def __init__(self):
        self.f = {}
        num_clause = 0


    def append(self, y):
        self.f.add(y)




class Literal:
    def __init__(self, y, sign):
        self.x = y
        if (sign == 0):
            self.sgn = False
        else:
            self.sgn = True


class Clause:
    def __init__(self):
        self.c = {}
        num_literal = 0
        is_sat = False


    def append(self, y):
        self.c.add(y)
        self.num_literal += 1
        
    def get_num_literal(self):
        return self.num_literal
