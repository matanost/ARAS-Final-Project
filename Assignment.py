
from CNF_formula import Literal
    
class Assignment:

    @staticmethod
    def get_literals(formula):
        literals = set()
        for clause in formula:
                for l in clause:
                    literals.add(l)
        return literals
         
    @staticmethod
    def get_variables(formula):
        variables = set()
        for l in Assignment.get_literals(formula):
            variables.add(l.x)
        return variables

    @staticmethod
    def find_pure_literals(formula):
        literals = Assignment.get_literals(formula)
        return set([l for l in literals if -l not in literals])
        
    @classmethod
    def plp_iteration(self):        
        for l in Assignment.find_pure_literals(self.formula):
            self.assign_variable(l.x,bool(l.sgn))            
        
    @classmethod
    def get_unassigned(self, clause):
        return [l for l in clause if l.x not in self.variable_assignments] #Assume no clause contains a literal and its negation.
    
    @classmethod    
    def find_watch_literals(self, clause):
        unassigned = self.get_unassigned(clause)
        return unassigned if len(unassigned) < 2 else unassigned[0:1]  
    
    @classmethod
    def update_watch_literals_clause(self, clause):
        if clause not in self.watch_literals:
            self.watch_literals[clause] = []       
        if all([(l.x not in self.variable_assignments) for l in self.watch_literals[clause]]) and self.watch_literals[clause]:
            return        
        watch_literals = self.find_watch_literals(clause)
        if len(watch_literals) == 0:
            self.clause_satisfied.add(clause)                       
        elif len(watch_literals) == 1:
            self.bcp_eligible.add(clause)
            self.watch_literals[clause] = watch_literals
        else : 
            self.watch_literals[clause] = watch_literals
            
    @classmethod
    def update_watch_literals_formula(self):
        for clause in self.clauses:
            if clause not in self.clause_satisfied:
                self.update_watch_literals_clause(clause)
            
    @classmethod
    def unassign_variable(self, var):
        if var not in self.variable_assignments:
            raise Exception("Attempt to unassign unassigned variable {}".format(var))
        self.variable_assignments.pop(var)
        
    @classmethod
    def assign_variable(self, var, value):
        if var in self.variable_assignments:
            raise Exception("Attempt to assign assigned variable {}".format(var))
        self.variable_assignments[var] = {"value" : value, "level" : self.level}
        for clause in self.containing_clauses[var]:            
            self.update_watch_literals_clause(clause)

    @classmethod    
    def bcp_iteration(self):
        if not self.bcp_eligible:
            return
        clause = self.bcp_eligible.pop()
        if len(self.watch_literals[clause]) != 1:
            raise Exception("Clause was eligable to BCP with other than 1 unassigned variable, clause={}, watch_lit={}".format(clause,self.watch_literals[clause]))
        unassigned_literal = self.watch_literals[clause].pop()
        if unassigned_literal.x in self.variable_assignments:
            raise Exception("Variable {} was watch literal for clause {} but is assigned".format(unassigned_literal.x, clause))
        self.assign_variable(unassigned_literal.x, bool(unassigned_literal.sgn)) #TODO propegate the assignment to other clauses and check conflicts.
        self.clause_satisfied.add(clause)
        self.watch_literals.pop(clause)
    
    @classmethod    
    def is_bcp_eligible(self):
        return self.bcp_eligible

    @classmethod
    def __init__(self, formula):
        self.level = 0
        self.formula = formula
        self.variables = Assignment.get_variables(formula)
        self.literals = Assignment.get_literals(formula)
        self.clauses = [clause for clause in self.formula]                
        self.containing_clauses = {v : [] for v in self.variables}        
        for l in self.literals:
            for clause in self.clauses:
                if l in clause:                
                    self.containing_clauses[l.x].append(clause)                    
        self.variable_assignments = dict() # Var : {value : True/False , level: unsigned int}        
        self.clause_satisfied = set() # clause in set iff all literals are assigned and is satisfied.
        self.watch_literals = dict() # Clause : literal list
        self.bcp_eligible = set()
        self.update_watch_literals_formula()
        
    def __str__(self):
        out = ""
        for var in self.variables:
            if var in self.variable_assignments:
                out += "<{}{}:{}>".format(("" if self.variable_assignments[var]["value"] else "-"), var, self.variable_assignments[var]["level"])
        return out