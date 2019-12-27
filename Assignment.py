
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
        return set([l.x for l in clause if !self.variable_assignments[l.x]])
    
    @classmethod    
    def find_watch_literals(self, clause):
        unassigned = self.get_unassigned(clause)
        if len(unassigned) < 2:
            return unassigned
        else:
            return unassigned[0:1]
    
    @classmethod
    def update_watch_literals_clause(self, clause):        
        update_clause = not self.watch_literals[clause]        
        for v in self.watch_literals[clause] if self.variable_assignments[v]:           
            update_clause = True
        if update_clause:
            self.watch_literals[clause] = self.find_watch_literals(clause)
            if len(self.watch_literals[clause]) == 0:
                self.clause_satisfied[clause] = True
            elif len(self.watch_literals[clause]) == 1:
                self.bcp_eligible.add(clause)
            
    @classmethod
    def update_watch_literals_formula(self):
        for clause in self.clauses if not self.clause_satisfied[clause]:
            self.update_watch_literals_clause(clause)
            
    @classmethod
    def unassign_variable(self, var):
        if self.variable_assignments[var] == 3STATE.UNASSIGNED:
            raise Exception("Attempt to unassign unassigned variable {}".format(var))
        self.variable_assignments[var] = 3STATE.UNASSIGNED
        self.variable_levels = -1
        
    @classmethod
    def assign_variable(self, var, value):
        if self.variable_assignments[var] != 3STATE.UNASSIGNED:
            raise Exception("Attempt to assign assigned variable {}".format(var))
        self.variable_assignments[var] = (3STATE.TRUE if value else 3STATE.FALSE)
        self.variable_levels[var] = self.level

    def bcp_iteration(self):
        if not self.bcp_eligible:
            return
        clause = self.bcp_eligible.pop()
        if len(self.watch_literals[clause]) != 1:
            raise Exception("Clause was eligable to BCP with more than 1 unassigned variable, clause={}".format(clause))
        unassigned_literal = self.watch_literals[clause][0]
        self.variable_assignments[unassigned_literal.x] = (3STATE.TRUE if unassigned_literal.sgn else 3STATE.FALSE)
        self.variable_levels[unassigned_literal.x] = self.level
        self.clause_satisfied[clause] = True
        self.watch_literals[clause] = list()

    @classmethod
    def __init__(self, formula):
        self.formula = formula    
        self.variables = get_literals(formula)
        self.literals = get_variables(formula)
        #self.variable_assignments = {v : 3STATE.UNASSIGNED for v in self.variables}
        #self.variable_levels = {v : -1 for v in self.variables}
        self.clauses = [clause for clause in self.formula]
        #self.clause_satisfied = {clause : False for clause in self.clauses}
        self.clause_satisfied
        self.watch_literals = {clause : list() for clause in self.clauses}
        self.bcp_eligible = set()
        self.update_watch_literals_formula()
        self.level = 0