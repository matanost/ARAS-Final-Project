

from SAT.CNF_formula import Literal, Clause, Sign
from SAT.Tsetin_transformation import TsetinTransformation as TT
from SAT.Tree import Node as TN
from SMT.CongClosure import Parser as CCP
from SAT.Assignment import Assignment
from SMT.CongClosure import CongClosure as CC
from SAT.Preprocess import remove_redundant_clauses
from LP.linear_programing_tools import linear_Programing
from LP.linear_programing import simplex_result
from SMT.SMTSolver_Parser import SMTSolver_Parser

import re
import numpy as np

class SMTSolver:                        

    #===========================================================================================
    #===========================================================================================
    def is_number(s):
        try: 
            float(s)
            return True
        except :
            return False
    
    def __init__(self):
        self.phrases = list()
        self.a = None
        self.cc = None
        self.var2eq = None
        self.formula = None
        self.smt_parser = SMTSolver_Parser()
        self.theory = None

    def split_pos_neg(self):
        assigned_lits = self.a.get_assignment()                
        pos = [self.var2eq[l.x] for l in assigned_lits if self.var2eq[l.x] is not None and     bool(l.sgn)]
        neg = [self.var2eq[l.x] for l in assigned_lits if self.var2eq[l.x] is not None and not bool(l.sgn)]
        return pos, neg

    def is_t_conflict(self):
        pos, neg = self.split_pos_neg()        
        if self.theory is "TUF":
            self.cc.enforce_eq(pos)
            return any([self.cc.check_eq(eq) for eq in neg])
        elif self.theory is "LP":
            inequalities = pos + [SMTSolver_Parser.negate(n) for n in neg]
            if not inequalities:
                return False
            sat, assign = self.check_lp(pos + [SMTSolver_Parser.negate(n) for n in neg])        
            return not sat

    def check_lp(self, inequalities):
        print(inequalities)
        matrix_A, vector_b, vector_c = self.convert_to_simplex(inequalities)
        matrix_A, vector_b, vector_c = np.array(matrix_A), np.array(vector_b), np.array(vector_c).transpose()
        print("matrix_A={}".format(matrix_A))
        print("vector_b={}".format(vector_b))
        print("vector_c={}".format(vector_c))        
        result = simplex_result(matrix_A, vector_b, vector_c)
        need_rsvd_var = any([op in ["<",">"] for op in []])
        print("Result=" + str(result))
        if SMTSolver.is_number(result):
            sat = result > 0
            assignment = []
        elif isinstance(result,str):
            sat = result == 'unbounded solution'
            assignment = []            
        elif len(result) > 1:
            result = list(result)
            sat = result[-1] > 0
            assignment = result[:-1]
        else:
            sat = False
            assignment = []
        print("SAT={} --> {}\n".format(sat, "No LP T-Conflict" if sat else "LP T-Conflict"))
        return sat, assignment

    def parse_ineq(ineq):
        split = list(filter(lambda s: s, re.split("[=<>!]", ineq)))
        if len(split) > 2:
            raise Exception("Split has too many elements:{}".format(str(split)))
        if not SMTSolver.is_number(split[1]) and not SMTSolver.is_number(split[0]):
            raise Exception("Split has no numeric elemet:{}".format(str(split)))
        if SMTSolver.is_number(split[1]) and SMTSolver.is_number(split[0]):
            raise Exception("Split has two numeric elemet:{}".format(str(split)))
            
        if not SMTSolver.is_number(split[1]) and SMTSolver.is_number(split[0]):
            bound = int(split[0])
            dot_prod = split[1]
            if ">=" in ineq:
                op = "<="
            elif "<=" in ineq:
                op = ">="
            elif ">" in ineq:
                op = "<"
            elif "<" in ineq:
                    op = ">"
        else:
            bound = int(split[1])
            dot_prod = split[0]
            if ">=" in ineq:
                op = ">="
            elif "<=" in ineq:
                op = "<="
            elif ">" in ineq:
                op = ">"
            elif "<" in ineq:
                op = "<"
        return dot_prod, op, bound

    def convert_to_simplex(self, inequalities):
        inequalities = [re.sub("\s","", ineq) for ineq in inequalities]
        RSVD = "RSVD"
        variables = set()
        term_regex = "^(-{0,1}\d*)([a-zA-Z_]\w*)$"
        for ineq in inequalities:
            for v in list(filter(lambda s: s and re.match(term_regex,s), re.split("[\s=<>!+]", ineq))):
                variables.add(re.search(term_regex, v).group(2))
        variables = list(variables)
        if RSVD in variables:
            variables.remove(RSVD)
        variables.append(RSVD)
        matrix_A = list()
        vector_b = list()
        vector_c = [0] * (len(variables)-1) + [1]
        for ineq in inequalities:
            dot_prod, op, bound = SMTSolver.parse_ineq(ineq)
            print("Processing:" + dot_prod + op + str(bound))
            int2str = lambda s: 1 if not s else (-1 if s is "-" else int(s))
            var_coef = {m.group(2) : int2str(m.group(1)) for m in [re.search(term_regex,t) for t in list(filter(lambda s: s, re.split("[\s+]", dot_prod)))]}
            if op == ">=" :
                bound = -bound
                var_coef = {k : -v  for k,v in var_coef.items()}
            elif op == "<":
                var_coef[RSVD] = 1
            elif op == ">":
                bound = -bound
                var_coef[RSVD] = 1
                var_coef = {k : -v if not k is RSVD else v for k,v in var_coef.items()}
            vector_b.append(bound)                            
            matrix_A.append([0 if v not in var_coef else var_coef[v] for v in variables])         
        return matrix_A, vector_b, vector_c

    #TODO Explain
    def tuf_explain(self):
        pos, neg = self.split_pos_neg()
        cc_explain = CC()
        cc_explain.create_database(self.phrases)
        cc_explain.enforce_eq(pos)
        failing_negs = [n for n in neg if cc_explain.check_eq(n)]
        cong_class = [(n,[p for p in pos if (cc_explain.find(CCP.split_tuf_eq(p)[0]) == cc_explain.find(CCP.split_tuf_eq(n)[0]))]) for n in failing_negs]
        min_size_cong = cong_class.sort(key=lambda elem : -len(elem[1]))[0]
        
    def t_explain(self):
        if self.theory is "TUF":
            #return self.tuf_explain()
            return Clause.create_clause(set([int(-lit) for lit in self.a.get_assignment()]))
        elif self.theory is "LP":
            return Clause.create_clause(set([int(-lit) for lit in self.a.get_assignment()]))
        
    def t_prop(self):
        if self.theory is "TUF":
            self.cc.enforce_eq(self.split_pos_neg()[0])
            for var in [v for v in self.a.get_unassigned() if self.var2eq[v] is not None]:
                if self.cc.check_eq(self.var2eq[var]):                    
                    self.a.decide(Literal(var, Sign.POS), inc_level=False)                
                    return True
            return False
        elif self.theory is "LP":
            return False
            

    def reset_assignment(self, RESET=True, clause=None):
        if RESET:
            if self.theory is "TUF":            
                self.cc = CC()
                #print(self.phrases)
                self.cc.create_database(self.phrases)
            self.a = Assignment(self.formula)
            return 
        
    def solve(self, tuf):
        self.smt_parser.reset(tuf)
        self.theory = self.smt_parser.theory
        formula_tree = self.smt_parser.tuf_to_tree(tuf)
        tt = TT(self.smt_parser.avail_literal-1)
        formula_cnf = tt.run_TsetinTransformation(formula_tree)
        formula_cnf = remove_redundant_clauses(formula_cnf)        
        sat, assignment, formula_learnt = self.solve_cnf(formula_cnf, self.smt_parser.var2eq)
        if sat:
            pos, neg = self.split_pos_neg()            
            return sat, pos + [SMTSolver_Parser.negate(n) for n in neg] + [p for b,p in self.bool_phrases.items() if b in assignment] + ["-" + p for b,p in self.bool_phrases.items() if -b in assignment]
        return sat, []

    def remove_redundant_phrases(self):
        none_or_bool = lambda p : p is None or all([sign not in p for sign in ["<", ">", "="]])
        self.bool_phrases = {var : eq for var,eq in self.var2eq.items() if none_or_bool(eq) and eq is not None}
        self.var2eq = {var : (None if none_or_bool(eq) else eq) for var,eq in self.var2eq.items()}                    
    def solve_cnf(self, formula, var2eq):       
        varis = set()
        for c in formula:
            for l in c:
                varis.add(l.x)
        for var in [v for v in varis if v not in var2eq]:
            var2eq[var] = None
        self.var2eq = var2eq
        self.formula = remove_redundant_clauses(formula)
        self.remove_redundant_phrases()
        self.phrases = [eq for eq in self.var2eq.values() if eq is not None]
        if len(self.formula) == 0:
            return True, []
        self.reset_assignment()
        #Should notice that "decide" and "bcp_iteration" perform CDCL conflict resolution for SAT-orignated conflicts.
        while not (self.a.SAT and self.a.all_var_assigned()) and not self.a.UNSAT:
            if self.t_prop():
                continue
            if self.a.is_bcp_eligible():
                self.a.bcp_iteration()
            else:
                if self.a.SAT:
                    self.a.decide(Literal(self.a.get_unassigned()[0], Sign.POS))
                else:                    
                    self.a.decide(self.a.get_decision())
            if self.a.UNSAT:
                break            
            if self.is_t_conflict():
                new_clause = self.t_explain()
                self.formula.append(new_clause)
                self.reset_assignment(clause=new_clause)
        if self.a.SAT:
            return True, [int(l) for l in self.a.get_assignment()], self.formula
        return False, None, self.formula 
                    
            
    #===========================================================================================
    #===========================================================================================
