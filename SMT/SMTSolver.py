

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
            self.match_2op_re = "([(].*[)])(\W+)([(].*[)])$"
            self.match_1op_re = "(-)([(].*[)])$"
            self.var2eq = dict()
            self.op_translate = {"+":"OR", "*":"AND", "->":"IF", "<->":"IFF", "-":"NOT"}

        def reset(self):
            self.avail_literal = 1
            self.var2eq = dict()

        def clean_recursion(self, string):
            if string.startswith("(") and string.endswith(")"):
                string = string[1:-1]
            return string.rstrip().strip().replace(" ", "")                
                
        def tuf_to_tree(self, tuf):
            tuf = tuf.strip().rstrip().replace(" ","")
            match_2op, match_1op = re.match(self.match_2op_re,tuf), re.match(self.match_1op_re,tuf)
            if bool(match_1op) and bool(match_2op):
                raise Exception("Both 2op and 1op matched: tuf=" + tuf)
            elif not bool(match_1op) and not bool(match_2op):
                for var, eq in self.var2eq.items():
                    if eq == tuf:
                        return TN(None, var)
                    if eq == CCP.negate(tuf):
                        return TN(None, -var)
                lit = self.avail_literal
                self.avail_literal += 1
                if CCP.is_neq(tuf):
                    tuf, lit = CCP.negate(tuf), -lit
                self.var2eq[abs(lit)] = tuf
                return TN(None, lit)
            elif bool(match_1op):             
                lhs, op, rhs  = None, match_1op.group(1), match_1op.group(2)
                right_tree = self.tuf_to_tree(self.clean_recursion(rhs))
            elif bool(match_2op):
                terms, p_cnt, gathered = [], 0, ""
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
                lhs, op, rhs = terms[0], terms[1], terms[2]
                left_tree, right_tree = self.tuf_to_tree(lhs), self.tuf_to_tree(rhs)

            new_node, equalities = TN(None, self.op_translate[op]), []
            if rhs:
                new_node.right_son = right_tree
                new_node.right_son.parent = new_node
            if lhs:
                new_node.left_son = left_tree
                new_node.left_son.parent = new_node
            return new_node

    #===========================================================================================
    #===========================================================================================

    def __init__(self):
        self.phrases = list()
        self.a = None
        self.cc = None
        self.var2eq = None
        self.formula = None
        self.smt_parser = SMTSolver.Parser()

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

    def solve(self, tuf):
        self.smt_parser.reset()
        formula_tree = self.smt_parser.tuf_to_tree(tuf)              
        tt = TT(self.smt_parser.avail_literal-1)
        formula_cnf = tt.run_TsetinTransformation(formula_tree)
        formula_cnf = remove_redundant_clauses(formula_cnf)        
        sat, assignment, formula_learnt = self.solve_cnf(formula_cnf, self.smt_parser.var2eq)        
        pos, neg = self.split_pos_neg()
        if sat:
            return sat, pos + [CCP.negate(n) for n in neg]
        return sat, []

    def solve_cnf(self, formula, var2eq):
        varis = set()
        for c in formula:
            for l in c:
                varis.add(l.x)
        for var in [v for v in varis if v not in var2eq]:
            var2eq[var] = None
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
