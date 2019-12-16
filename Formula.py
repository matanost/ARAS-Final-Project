
class Formula:
    def __init__(self):
        self.f = {}

    def append(self, y):
        self.f.add(y)




    class Literal:
        def __init__(self, y):
            if ("-" in y):
                self.x = y[1]
                self.sgn = False
            else:
                self.x = y
                self.sgn = True


    class Clause:
        def __init__(self):
            self.c = {}
            num_literal = 0

        def append(self, y):
            self.c.add(y)
            self.num_literal += 1
        
        def get_num_literal(self):
            return self.num_literal
