from CNF_formula import Literal, CNF_formula
from CNF_formula import Clause


class TsetinTransformation:

    def __init__(self, max_var_name):
        self.var_name = max_var_name
        self.f = CNF_formula()

    def generate_name(self):
        self.var_name += 1
        return self.var_name

    # def from_iff_to_cnf(self, x, y):
    #     c1 = Clause()
    #     c2 = Clause()
    #     c1.append(-x)
    #     c1.append(y)
    #     c2.append(x)
    #     c2.append(-y)
    #     sub_f = CNF_formula()
    #     sub_f.append(c1)
    #     sub_f.append(c2)
    #     return sub_f


    # def base_case(self, literal):
    #     """
    #
    #     :param literal:
    #     :return:
    #     """
    #     g = Literal(self.generate_name())
    #     c = Clause()
    #
    #     c.append(self.from_iff_to_cnf(g, literal))
    #     self.f.append(c)
    #     return g

    def or_clause(self, tseitin_literal_x, tseitin_literal_y):
        g = Literal(self.generate_name())
        c = Clause()
        c.append(-tseitin_literal_x)
        c.append(g)
        self.f.append(c)
        c = Clause()
        c.append(-tseitin_literal_y)
        c.append(g)
        self.f.append(c)
        c = Clause()
        c.append(tseitin_literal_x)
        c.append(tseitin_literal_y)
        c.append(-g)
        self.f.append(c)
        return g

    def not_clause(self, tseitin_literal):
        g = Literal(self.generate_name())
        c = Clause()
        c.append(-tseitin_literal)
        c.append(-g)
        self.f.append(c)
        c = Clause()
        c.append(tseitin_literal)
        c.append(g)
        self.f.append(c)
        return g

    def and_clause(self, tseitin_literal_x, tseitin_literal_y):
        """
        get equation (x||y) and append to f (x||y) iff g
        witch in CNF it: (x||-g)&&(y||-g)&&(-x||-y||g)
        :param tseitin_literal_x
        :param tseitin_literal_y
        :return: the new name of (x||y)
        """
        g = Literal(self.generate_name())
        c = Clause()
        c.append(tseitin_literal_x)
        c.append(-g)
        self.f.append(c)
        c = Clause()
        c.append(tseitin_literal_y)
        c.append(-g)
        self.f.append(c)
        c = Clause()
        c.append(-tseitin_literal_x)
        c.append(-tseitin_literal_y)
        c.append(g)
        self.f.append(c)
        return g

    def if_clause(self, tseitin_literal_x, tseitin_literal_y):
        """
        get equation (x -> y) and append to f (x -> y) <-> g
        witch in CNF it: (-x||y||-g)&&(-x||g)&&(-y||g)
        :param tseitin_literal_x
        :param tseitin_literal_y
        :return: the new name of (x->y)
        """
        g = Literal(self.generate_name())
        c = Clause()
        c.append(-tseitin_literal_x)
        c.append(tseitin_literal_y)
        c.append(-g)
        self.f.append(c)
        c = Clause()
        c.append(tseitin_literal_x)
        c.append(g)
        self.f.append(c)
        c = Clause()
        c.append(-tseitin_literal_y)
        c.append(g)
        self.f.append(c)
        return g

    def iff_clause(self, tseitin_literal_x, tseitin_literal_y):
        """
        get equation (x <-> y) and append to f (x <-> y) <-> g
        witch in CNF it: (x||-y||-g)&&(-x||y||-g)&&(g||y||x)&&(-x||-y||g)
        :param tseitin_literal_x
        :param tseitin_literal_y
        :return: the new name of (x <-> y)
        """
        g = Literal(self.generate_name())
        c = Clause()
        c.append(tseitin_literal_x)
        c.append(-tseitin_literal_y)
        c.append(-g)
        self.f.append(c)
        c = Clause()
        c.append(-tseitin_literal_x)
        c.append(tseitin_literal_y)
        c.append(-g)
        self.f.append(c)
        c = Clause()
        c.append(-tseitin_literal_x)
        c.append(-tseitin_literal_y)
        c.append(g)
        self.f.append(c)
        c = Clause()
        c.append(tseitin_literal_x)
        c.append(tseitin_literal_y)
        c.append(g)
        self.f.append(c)
        return g

    def parser(self, equation):
        opers = {'NOT': self.not_clause, 'OR': self.or_clause,
                 'AND': self.and_clause, 'IF': self.if_clause,
                 'IFF': self.iff_clause}

        leftC = equation.get_left_son()
        rightC = equation.get_right_son()

        if leftC and rightC:
            fn = opers[equation.get_value()]
            x = self.parser(leftC)
            y = self.parser(rightC)
            return fn(x,y)
        if leftC:
            fn = opers[equation.get_value()]
            x = self.parser(leftC)
            return fn(x)
        if rightC:
            fn = opers[equation.get_value()]
            x = self.parser(rightC)
            return fn(x)
        else:
            return equation.get_value()


    def run_TsetinTransformation(self, tree):
        self.parser(tree)
        c = Clause()
        c.append(self.var_name)
        self.f.append(c)
        return self.f







