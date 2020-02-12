
from CNF_formula import Literal
class smt_solver:        
        
    class Assignment:

        def __init__(formula):
            self.formula = formula #Should be list of sets of strings. TODO other representation?
            self.lit = set():
            self.conflict = None

    def propagate:
        pass

    def decide:
        pass

    def conflict:
        pass

    def explain:
        pass

    def backjump:
        pass

    def fail:
        pass

    def t_conflict:
        pass

    def t_propagate:
        pass

    def t_explain:
        pass

    def learn:
        pass

    def forget:
        pass

    def restart:
        pass
    
