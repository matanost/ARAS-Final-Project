

from CNF_formula import Literal, Clause, Sign
from Tsetin_transformation import TsetinTransformation as TT
from Tree import Node as TN
from CongClosure import Parser as CCP
from Assignment import Assignment as As
from CongClosure import CongClosure as CC
from Preprocess import remove_redundant_clauses

import re

class SMTSolver:
    
    class Parser:

        def __init__(self):        
            self.avail_literal = 1
            self.legal_2ops = ["+", "*", "->", "<->"]
            self.legal_1ops = ["-"]
            self.match_2op_re = "([(].*[)])(\W+)([(].*[)])$"
            self.match_1op_re = "(-)([(].*[)])$"
            self.var2eq = dict()
                
        def tuf_to_tree(self, tuf): #TODO
            tuf = tuf.strip().rstrip().replace(" ","")
            match_2op = re.match(self.match_2op_re,tuf)
            match_1op = re.match(self.match_1op_re,tuf)                        
            if bool(match_1op) and bool(match_2op):
                raise Exception("Both 2op and 1op matched: tuf=" + tuf)
            if not bool(match_1op) and not bool(match_2op):
                lit = self.avail_literal
                self.avail_literal += 1
                self.var2eq[lit.x] = tuf
                return {"tree" : TN(None, (-lit if CCP.is_neq(tuf) else lit)), "eq" : [tuf]}
            if bool(match_1op):             
                op = match_1op.group(1)
                lhs = None
                rhs = match_1op.group(2)
                right_tree = SMTSolver.Parser.tuf_to_tree(rhs)
            if bool(match_2op):
                terms = []
                p_cnt = 0
                gathered = ""
                for c in tuf:
                    if c in ["(", ")"]:
                        if (c is "(" and p_cnt == 0) or (c is ")" and p_cnt == 1):
                            if len(gathered) > 0:
                                terms.append(gathered)
                            gathered = ""
                        else:
                            gathered += c
                        p_cnt += (1 if c == "(" else -1)
                    else:
                        gathered += c
                if len(gathered) > 0:
                    terms.append(gathered)
                lhs = terms[0]
                op = terms[1]
                rhs = terms[2]
                left_tree = SMTSolver.Parser.tuf_to_tree(lhs)
                right_tree = SMTSolver.Parser.tuf_to_tree(rhs)

            new_node = TN(None, op)
            equalities = []
            if rhs:
                new_node.right_son = right_tree["tree"]
                new_node.right_son.parent = new_node
                equalities += right_tree["eq"]
            if lhs:
                new_node.left_son = left_tree["tree"]
                new_node.left_son.parent = new_node
                equalities += left_tree["eq"]
            return {"tree" : new_node, "eq" : equalities}

    #===========================================================================================
    #===========================================================================================

    def __init__(self):
        self.phrases = list()
        self.a = None
        self.cc = None
        self.var2eq = None
        self.formula = None

    def split_pos_neg(self):
        assigned_lits = self.a.get_assignment()
        pos = [self.var2eq[l.x] for l in assigned_lits if self.var2eq[l.x] is not None and     bool(l.sgn)]
        neg = [self.var2eq[l.x] for l in assigned_lits if self.var2eq[l.x] is not None and not bool(l.sgn)]
        return pos, neg

    def is_t_conflict(self):        
        pos, neg = self.split_pos_neg()
        self.cc.enforce_eq(pos)
        return any([self.cc.check_eq(eq) for eq in neg])

    def t_prop(self):        
        self.cc.enforce_eq(self.split_pos_neg()[0])
        for var in [v for v in self.a.get_unassigned() if self.var2eq[v] is not None]:
            if self.cc.check_eq(self.var2eq[var]):
                self.a.decide(Literal(var, Sign.POS))                
                return True
        return False

    def reset_assignment(self, RESET=True, clause=None):
        if RESET:
            self.cc = CC()
            self.cc.create_database(self.phrases)
            self.a = As(self.formula)
            return

    def solve_cnf(self, formula, var2eq):
        self.var2eq = var2eq
        self.formula = remove_redundant_clauses(formula)
        self.phrases = [eq for eq in self.var2eq.values() if eq is not None]
        if len(self.formula) == 0:
            return True, []
        self.reset_assignment()
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
                #TODO explain
                new_clause = Clause.create_clause(set([int(-lit) for lit in self.a.get_assignment()]))
                self.formula.append(new_clause)
                self.reset_assignment(clause=new_clause)
        if self.a.SAT:
            return True, [int(l) for l in self.a.get_assignment()], self.formula
        return False, None, self.formula 
                    
            
    #===========================================================================================
    #===========================================================================================
