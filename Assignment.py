
from CNF_formula import Literal, Sign
from ConflictAnalysis import impGraph
    
class Assignment:

    '''
    Data Structures:
    variable_assignments : dict from variables to dict {"value","level"}
    bcp_eligible : set of clauses with a single unassigned watch literal.
    clause_satisfied : set containing cluase iff it is satisfied by current assignment.
    watch_literals : dict from clauses to literal lists.
    '''
    
    @staticmethod
    def get_literals(formula):
        literals = set()
        for clause in formula:
            for literal in clause:
                literals.add(literal)
        return literals
        
    def get_pure_literals(self, formula):
        literals = set()
        for clause in [c for c in formula if c not in self.clause_satisfied]:
            for literal in clause:
                literals.add(literal)
        return literals
         
    @staticmethod
    def get_variables(formula):
        variables = set()
        for l in Assignment.get_literals(formula):
            variables.add(l.x)
        return variables

    def find_pure_literals(self, formula):
        literals = self.get_pure_literals(formula)
        return set([l for l in literals if -l not in literals])

    @staticmethod
    def resolve_clauses(c1, c2, lit):
        resolving_lit = None
        if (lit in c1) and (-lit in c2):
            pos = c1
            neg = c2
        elif (lit in c2) and (-lit in c1):
            pos = c2
            neg = c1
        else:
            raise Exception("Attempt to resolve clauses around a wrong literal. c1={} and c2={} literal={}".format(c1,c2,lit))
        pos.remove(lit)
        neg.remove(-lit)
        for l in c2:
            c1.add(l)
        return c1

    def get_literal(self, var):
        if var not in self.variable_assignments:
            raise Exception("Attempt to get value of unassigned variable".format(var))
        return Literal(var,Sign.POS if self.variable_assignments[var]["value"] else Sign.NEG)
        
    def plp_iteration(self):        
        for l in self.find_pure_literals(self.formula):
            self.deduce(l)         
        
    def get_unassigned(self, clause):
        return [l for l in clause if l.x not in self.variable_assignments]
        
    def satisfy_clause(self, clause):
        self.clause_satisfied.add(clause)
        self.watch_literals.pop(clause)
        if clause in self.bcp_eligible:
            self.bcp_eligible.remove(clause)
        if len(self.clause_satisfied) == len(self.formula):
            self.set_sat()
        
    def is_clause_satisfied(self, clause):
        for l in clause:
            if l.x in self.variable_assignments:
                if self.variable_assignments[l.x]["value"] == l.sgn:
                    return True
        return False
        
    def find_watch_literals(self, clause):
        unassigned = self.get_unassigned(clause)
        return unassigned if len(unassigned) < 2 else unassigned[:2]  
    
    def update_clause_state(self, clause):
        if clause in self.clause_satisfied:
            return
        if clause not in self.watch_literals:
            self.watch_literals[clause] = []
        if all([(l.x not in self.variable_assignments) for l in self.watch_literals[clause]]) and self.watch_literals[clause]:
            return
        watch_literals = self.find_watch_literals(clause)       
        if len(watch_literals) == 0:
            for l in self.watch_literals[clause]:
                if self.variable_assignments[l.x]["value"] == l.sgn:
                    self.satisfy_clause(clause)
                    return
            self.conflict_found(clause)
        elif len(watch_literals) == 1:
            self.bcp_eligible.add(clause)
            self.watch_literals[clause] = watch_literals
        else : 
            self.watch_literals[clause] = watch_literals
            
    def update_formula_state(self):
        for clause in self.clauses:
            if clause not in self.clause_satisfied:
                self.update_clause_state(clause)

    #Return i iff this literal is the i-th literal to be assigned.
    def get_assignment_index(self, literal):
        return self.imp_graph.literal_assignments_ordered.index(literal)
        
    def unassign_variable(self, var):
        if var not in self.variable_assignments:
            raise Exception("Attempt to unassign unassigned variable {}".format(var))
        self.variable_assignments.pop(var)
        self.imp_graph.literal_assignments_ordered.remove(self.get_literal(var))
        self.imp_graph.remove_node(self.imp_graph.get_node(self.get_literal(var)))
        #TODO need to erase all assignment with bigger level than Var, maybe even the equal one?
        for clause in self.containing_clauses[var]:
            if not self.is_clause_satisfied(clause) and clause in self.clause_satisfied:
                self.clause_satisfied.remove(clause)
            self.update_clause_state(clause)
        
    def assign_variable(self, var, value):
        if var in self.variable_assignments:
            raise Exception("Attempt to assign assigned variable {}:{},{}".format(var,self.variable_assignments[var]["value"],self.variable_assignments[var]["level"]))
        self.variable_assignments[var] = {"value" : value, "level" : self.level}
        self.imp_graph.literal_assignments_ordered.append(self.get_literal(var))
        for clause in self.containing_clauses[var]:
            if self.get_literal(var) in clause:
                self.satisfy_clause(clause)
            self.update_clause_state(clause)

    def bcp_iteration(self):
        if not self.bcp_eligible:
            return
        clause = self.bcp_eligible.pop()
        if len(self.watch_literals[clause]) != 1:
            raise Exception("Clause was eligable to BCP with other than 1 unassigned variable, clause={}, watch_lit={}".format(clause,self.watch_literals[clause]))
        unassigned_literal = self.watch_literals[clause].pop()
        if unassigned_literal.x in self.variable_assignments:
            raise Exception("Variable {} was watch literal for clause {} but is assigned".format(unassigned_literal.x, clause))
        self.deduce(unassigned_literal, clause)        

    def conflict_found(self, conflicting_clause):
        print("Found conflict in clause" + str(conflicting_clause)) #FIXME
        self.imp_graph.add_conflict()
        for lit in conflicting_clause:
            self.imp_graph.add_edge_to_conflict(-lit, conflicting_clause)
        self.conflict = conflicting_clause
        self.resolve_conflict()
        
    def backjump(self, level):
        for lit in reversed(self.imp_graph.literal_assignments_ordered):
            if self.variable_assignments[lit.x]["level"] > level:
                self.unassign_variable(lit.x)
        
    def resolve_conflict(self):
        learnt_conflict = self.imp_graph.explain(self.conflict, self.last_decision)
        self.imp_graph.remove_conflicts()
        levels = set([self.variable_assignments[lit.x]["level"] for literal in learnt_conflict])
        if len(levels) == 1:
            if levels.pop() == 0:
                self.set_unsat()
                return
            else:
                backjump_level = 0
        else :
            levels.remove(max(levels))
            backjump_level = max(levels)
        self.backjump(backjump_level)
    
    def decide(self, literal):
        self.level += 1
        self.imp_graph.add_root(literal, self.level)
        self.last_decision = literal
        self.assign_variable(literal.x, bool(literal.sgn))

    def deduce(self, literal, clause=None):
        self.imp_graph.add_literal(literal, self.level)
        if clause is not None:
            for lit in clause:
                if lit != literal and lit.x in self.variable_assignments:
                    self.imp_graph.add_edge(-lit, clause, literal)
        self.assign_variable(literal.x, bool(literal.sgn)) #TODO check conflicts.

    def get_decision(self):
        num_clauses = [tuple(l, len([c for c in self.containing_clauses_literals[l] if c not in self.clause_satisfied])) for l in self.literals]
        max_index, (lit, num_c) = max(enumerate(num_clauses), key=lambda tup: tup[1][1])
        return num_clauses[max_index][0]
        
        
    def is_bcp_eligible(self):
        return self.bcp_eligible
        
    def set_sat(self):
        self.SAT = True
        
    def set_unsat(self):
        self.UNSAT = True

    def __init__(self, formula):
        self.level = 0
        self.formula = formula
        self.variables = Assignment.get_variables(formula)
        self.literals = Assignment.get_literals(formula)
        self.clauses = [clause for clause in self.formula]                
        self.containing_clauses = {v : [] for v in self.variables}  
        self.containing_clauses_literals = {l : [] for l in self.literals}        
        for l in self.literals:
            for clause in self.clauses:
                if l in clause:                
                    self.containing_clauses[l.x].append(clause)   
                    self.containing_clauses_literals[l].append(clause) 
        self.variable_assignments = dict() # Var : {value : True/False , level: unsigned int}
        self.clause_satisfied = set() # clause in set iff all literals are assigned and is satisfied.
        self.watch_literals = dict() # Clause : literal list
        self.bcp_eligible = set()
        self.update_formula_state()
        self.imp_graph = impGraph(self.formula)
        self.conflict = None
        self.SAT = False
        self.UNSAT = False
        self.last_decision = None
        
    def __str__(self):
        out = "\nAssigned Variables:"
        for var in self.variables:
            if var in self.variable_assignments:
                out += "<{}{}:{}>".format(("" if self.variable_assignments[var]["value"] else "-"), var, self.variable_assignments[var]["level"])
        out += "\n"
        out +=  "Status:" + ("Conflict" if self.conflict else "No Conflict") + "\n"
        out += "Satisfied Clauses: {}\n".format([self.clauses.index(c)+1 for c in self.clause_satisfied])
        out += "BCP eligible clauses: {}\n".format([self.clauses.index(c)+1 for c in self.bcp_eligible])
        out += "Watch Literals:"
        for clause, literals in self.watch_literals.items():
            out += "<c={}, {}>".format(self.clauses.index(clause)+1, [str(l) for l in literals])
        out += "\n"
        out += str(self.imp_graph)
        return out
    
    @staticmethod
    def sat_solve(formula):
        a = Assignment(f)
        while not a.SAT and not a.UNSAT:
            while a.is_bcp_eligible():
                a.bcp_iteration()
            a.decide(a.get_decision())
        if a.SAT:
            return True, [Literal(var,self.variable_assignments[var]["value"]) for var in self.variables]
        #a.UNSAT:
        return False, None
        
        
