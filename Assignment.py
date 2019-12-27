
from CNF_formula import Literal
    
class Assignment:

    @staticmethod
    def get_literals(formula):
         set([l for l in clause for clause in formula]])
         
    @staticmethod
    def get_variables(formula):
         set([l.x for l in get_literals(formula)])

    @staticmethod
    def find_pure_literals(formula):
        literals = get_literals(formula)
        return set([l in literals if -l is not in literals])
        
    @classmethod
    def get_unassigned(self, clause):
        return set([v for v in self.variables if v not in self.variable_assignments])
    
    @classmethod    
    def find_watch_literals(self, clause):
        unassigned = self.get_unassigned(clause)
        if len(unassigned) < 2:
            return unassigned
        else:
            return unassigned[0:1]
    
    @classmethod
    def update_watch_literals_clause(self, clause):
        if clause not in self.watch_literals:
            self.watch_literals[clause] = []
        update_clause = not self.watch_literals[clause]
        for v in self.watch_literals[clause] if v in self.variable_assignments:           
            update_clause = True
        if update_clause:
            self.watch_literals[clause] = self.find_watch_literals(clause)
            if len(self.watch_literals[clause]) == 0:
                self.clause_satisfied.add(clause)
            elif len(self.watch_literals[clause]) == 1:
                self.bcp_eligible.add(clause)
            
    @classmethod
    def update_watch_literals_formula(self):
        for clause in self.clauses if not self.clause_satisfied[clause]:
            self.update_watch_literals_clause(clause)
            
    @classmethod
    def unassign_variable(self, var):
        if var not in self.variable_assignments
            raise Exception("Attempt to unassign unassigned variable {}".format(var))
        self.variable_assignments.pop(var)
        
    @classmethod
    def assign_variable(self, var, value):
        if var in self.variable_assignments:
            raise Exception("Attempt to assign assigned variable {}".format(var))
        self.variable_assignments[var] = {"value" : value, "level" : self.level}

    @classmethod    
    def bcp_iteration(self):
        if not self.bcp_eligible:
            return
        clause = self.bcp_eligible.pop()
        if len(self.watch_literals[clause]) != 1:
            raise Exception("Clause was eligable to BCP with more than 1 unassigned variable, clause={}".format(clause))
        unassigned_literal = self.watch_literals[clause].pop()
        if unassigned_literal.x in self.variable_assignments:
            raise Exception("Variable {} was watch literal but is assigned".format(unassigned_literal.x))
        self.assign_variable(unassigned_literal.x, bool(unassigned_literal.sgn)) #TODO propegate the assignment to other clauses and check conflicts.
        self.clause_satisfied.add(clause)
        self.watch_literals.pop(clause)

    @classmethod
    def __init__(self, formula):
        self.level = 0
        self.formula = formula
        self.variables = get_literals(formula)
        self.literals = get_variables(formula)
        self.clauses = [clause for clause in self.formula]        
        self.variable_assignments = dict() # Var : {value : True/False , level: unsigned int}        
        self.clause_satisfied = set() # clause in set iff all literals are assigned and is satisfied.
        self.watch_literals = dict() # Clause : literal list
        self.bcp_eligible = set()
        self.update_watch_literals_formula()        