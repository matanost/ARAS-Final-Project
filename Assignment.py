
from CNF_formula import Literal, Sign, Clause, CNF_formula
from ConflictAnalysis import impGraph
from Preprocess import remove_redundant_clauses
import copy
import Tseitin
    
class Assignment:

    '''
    Data Structures:
    variable_assignments : dict from variables to dict {"val","lvl"}
    bcp_eligible : set of clauses with a single unassigned watch literal.
    clause_satisfied : set containing cluase iff it is satisfied by current assignment.
    watch_literals : dict from clauses to literal lists.
    '''

    @staticmethod
    def resolve_clauses(c1, c2, lit):
        if (lit in c1) and (-lit in c2):
            pos = c1
            neg = c2
        elif (lit in c2) and (-lit in c1):
            pos = c2
            neg = c1
        else:
            raise Exception("Attempt to resolve clauses around a wrong literal. c1={} and c2={} literal={}".format(c1,c2,lit))        
        new_clause = Clause()
        for l in pos:
            if l != lit:
                new_clause.append(l)
        for l in neg:
            if l != -lit:
                new_clause.append(l)
        return new_clause
            
    def satisfy_clause(self, c):        
        self.clause_sat.add(c)
        if c in self.watch_lits:
            self.watch_lits.pop(c)
        if c in self.bcp_vld:
            self.bcp_vld.remove(c)
        if len(self.clause_sat) == len(self.formula):
            self.set_sat()
        
    def is_c_sat(self, c):
        for l in c:
            if l.x in self.var_assign:
                if self.var_assign[l.x]["val"] == bool(l.sgn):
                    return True
        return False
        
    def find_watch_lits(self, c):
        unassigned = [l for l in c if l.x not in self.var_assign]
        return unassigned if len(unassigned) < 2 else unassigned[:2]  
    
    def update_clause_state(self, c):
        if self.is_c_sat(c):
            self.satisfy_clause(c)
        if c in self.clause_sat:
            return
        if c not in self.watch_lits:
            self.watch_lits[c] = []
        if all([(l.x not in self.var_assign) for l in self.watch_lits[c]]) and self.watch_lits[c] and (len(self.watch_lits[c]) == 2):
            return
        watch_lits = self.find_watch_lits(c)       
        if len(watch_lits) == 0:
            for l in self.watch_lits[c]:
                if self.var_assign[l.x]["val"] == l.sgn:
                    self.satisfy_clause(c)
                    return
            self.conflict_found(c)
            return True
        elif len(watch_lits) == 1:
            self.bcp_vld.add(c)
            self.watch_lits[c] = watch_lits
        else : 
            self.watch_lits[c] = watch_lits
        return False

    def unassign_variable(self, var):       
        if var not in self.var_assign:
            raise Exception("Attempt to unassign unassigned variable {}".format(var))
        var_as_lit = Literal(var,Sign.POS if self.var_assign[var]["val"] else Sign.NEG)
        self.var_assign.pop(var)
        self.imp_graph.lit_assign_ord.remove(var_as_lit)
        self.imp_graph.del_node(var_as_lit)
        if var_as_lit in self.last_decision:
            self.last_decision.remove(var_as_lit)
        elif -var_as_lit in self.last_decision:
            self.last_decision.remove(-var_as_lit)
        for c in self.cont_clauses[var]:            
            if (var_as_lit in c) and (c in self.clause_sat and not self.is_c_sat(c)):
                self.clause_sat.remove(c)
            elif (-var_as_lit in c) and (c in self.bcp_vld):
                self.bcp_vld.remove(c)
            self.update_clause_state(c)
        
    def assign_variable(self, var, val):
        if var in self.var_assign:
            raise Exception("Attempt to assign assigned variable {}:{},{}".format(var,self.var_assign[var]["val"],self.var_assign[var]["lvl"]))
        self.var_assign[var] = {"val" : val, "lvl" : self.lvl}
        l = Literal(var,Sign.POS if val else Sign.NEG)
        self.imp_graph.lit_assign_ord.append(l)
        containing_clauses = copy.deepcopy(self.cont_clauses[var])
        for c in containing_clauses:
            if l in c and c not in self.clause_sat:
                self.satisfy_clause(c)            
            conflict = self.update_clause_state(c)
            if conflict:
                return

    def conflict_found(self, conflicting_clause):        
        self.imp_graph.add_conflict()
        for lit in conflicting_clause:
            self.imp_graph.add_edge_to_conflict(-lit, conflicting_clause)
        self.conflict = conflicting_clause
        self.resolve_conflict()
        
    def backjump(self, lvl):
        orig_lit_assign_ord = self.imp_graph.lit_assign_ord
        for lit in reversed(orig_lit_assign_ord):
            if self.var_assign[lit.x]["lvl"] > lvl:
                self.unassign_variable(lit.x)
        self.lvl = lvl

    def add_clause(self, c):
        for l in c:
            if l not in self.lits:
                self.lits.add(l)
                self.cont_clauses[l] = []            
            if l.x not in self.varis:
                self.varis.add(l.x)
                self.cont_clauses[l.x] = set()
            self.cont_clauses[l].append(c)
            self.cont_clauses[l.x].add(c)
        if c not in self.clauses:
            self.clauses.append(c)
        if c not in self.formula:
            self.formula.append(c)
        self.imp_graph.formula = self.formula
        self.update_clause_state(c)
        
    def resolve_conflict(self):
        calc_conflict = Clause()
        for l in self.imp_graph.lit_assign_ord:
            calc_conflict.append(-l)        
        f_len = len(self.formula)
        f_doc = self.formula
        conf_doc = self.conflict    
        if self.lvl == 0:
            self.set_unsat()
            return
        learnt_clause = self.imp_graph.explain(self.conflict, self.last_decision[0])
        self.imp_graph.del_conflicts()
        lvls = set([self.var_assign[l.x]["lvl"] for l in learnt_clause])
        if len(lvls) == 1:
            if lvls.pop() == 0:
                self.set_unsat()
                return
            else:
                backjump_lvl = 0
        else :
            lvls.remove(max(lvls))
            backjump_lvl = max(lvls)
        self.backjump(backjump_lvl)
        self.add_clause(learnt_clause)
        self.conflict = None
        
        if (f_len + 1) != len(self.formula):
            raise Exception("No clause learnt: " + str(learnt_clause) +"\n Old formula=" + str(f_doc) + "\nNew formula=" + str(self.formula) + "\nOriginal conflict=" + str(conf_doc) + "\nExplained=" + str(learnt_conflict) + "\nCalculated=" + str(calc_conflict))
    
    def decide(self, l):
        if l is None:
            return
        self.lvl += 1
        self.imp_graph.add_root(l, self.lvl)
        self.last_decision.insert(0,l)
        self.assign_variable(l.x, bool(l.sgn))    

    def decide_unassigned_variables(self):
        if len(self.clause_sat) != len(self.formula):
            raise Exception("SAT when not all clauses are sat")
        else:
            for var in [v for v in self.varis if v not in self.var_assign]:
                self.decide(Literal(var,Sign.POS))

    def deduce(self, l, clause=None):
        self.imp_graph.add_literal(l, self.lvl)
        if clause is not None:
            for lit in clause:
                if lit != l and lit.x in self.var_assign:
                    if -lit not in  self.imp_graph.nodes.keys():
                        raise Exception("Deducing when not all other literals are assigned lit=" + str(l)+ " clause=" + ("None" if clause is None else str(clause) + ",#" + str(self.formula.index(clause))))
                    self.imp_graph.add_edge(-lit, clause, l)
        self.assign_variable(l.x, bool(l.sgn))

    #DLIS    
    def get_decision(self):
        num_clauses = [(l, len([c for c in self.cont_clauses[l] if c not in self.clause_sat])) for l in self.lits if l.x not in self.var_assign]
        if (not num_clauses) or self.SAT or self.UNSAT:
            return None
        max_index, (lit, num_c) = max(enumerate(num_clauses), key=lambda tup: tup[1][1])
        return num_clauses[max_index][0]
        
        
    def is_bcp_eligible(self):
        if self.SAT or self.UNSAT:
            return False
        return self.bcp_vld
        
    def set_sat(self):
        self.SAT = True
        
    def set_unsat(self):
        self.UNSAT = True
    
    def __init__(self, formula):
        Assignment.reflection = self
        self.lvl = 0
        self.varis = set()
        self.lits = set()
        self.clauses = list()
        self.cont_clauses = dict()
        self.var_assign = dict() # Var : {val : True/False , lvl: unsigned int}
        self.clause_sat = set() # clause in set iff all literals are assigned and is satisfied.
        self.watch_lits = dict() # Clause : literal list
        self.bcp_vld = set()
        self.conflict = None
        self.SAT = False
        self.UNSAT = False
        self.last_decision = []
        self.formula = CNF_formula()
        for c in formula:
            self.formula.append(c)
        self.imp_graph = impGraph(self.formula)
        for clause in formula:
            self.add_clause(clause)                       
        
    def __str__(self):
        out = "\nAssigned Variables:"
        for var in self.varis:
            if var in self.var_assign:
                out += "<{}{}:{}>".format(("" if self.var_assign[var]["val"] else "-"), var, self.var_assign[var]["lvl"])
        out += "\n"
        out +=  "Status:" + ("Conflict" if self.conflict else "No Conflict") + "\n"
        out += "Satisfied Clauses: {}\n".format([self.clauses.index(c) for c in self.clause_sat])
        out += "Un-Satisfied Clauses: {}\n".format([self.clauses.index(c) for c in self.formula if c not in self.clause_sat])
        out += "BCP eligible clauses: {}\n".format([self.clauses.index(c) for c in self.bcp_vld])
        out += "Watch Literals:"        
        for clause, literals in self.watch_lits.items():
            out += "<c={}, {}>".format(self.clauses.index(clause), [str(l) for l in literals])
        out += "Last decision=" + ("None" if not self.last_decision else str(self.last_decision[0]))
        out += "\n"
        out += str(self.imp_graph)
        return out

    @staticmethod
    def sat_solve(formula_tree):
        
    
    @staticmethod
    def cnf_sat_solve(formula):
        formula = remove_redundant_clauses(formula)
        if len(formula) == 0:
            return True, []
        a = Assignment(formula)
        while not a.SAT and not a.UNSAT:
            while a.is_bcp_eligible():
                a.bcp_iteration()
            a.decide(a.get_decision())        
        if a.SAT:
            a.decide_unassigned_variables()
            return True, [var * (1 if a.var_assign[var]["val"] else -1) for var in a.varis]
        return False, None    
    
    def bcp_iteration(self):
        if not self.bcp_vld:
            return
        clause = self.bcp_vld.pop()
        if len(self.watch_lits[clause]) != 1:
            raise Exception("Clause was eligable to BCP with other than 1 unassigned variable, clause={}, watch_lit={}".format(clause,self.watch_lits[clause]))
        unassigned_literal = self.watch_lits[clause].pop()
        if unassigned_literal.x in self.var_assign:
            raise Exception("Variable {} was watch literal for clause {} but is assigned".format(unassigned_literal.x, clause))
        self.deduce(unassigned_literal, clause)        
        
    def plp_iteration(self):
        literals = set()
        for clause in [c for c in self.formula if c not in self.clause_sat]:
            for l in clause:
                literals.add(l)        
        pure_literals = set([l for l in literals if -l not in literals])
        for l in pure_literals:
            self.deduce(l)
        
