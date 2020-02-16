

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

    def __init__(self): #TODO
        self.t_prop_elig = set()

    def is_t_prop_eligible(self, assignments, phrases):
        pass

    def solve_cnf(self, formula, var2eq):
        formula = remove_redundant_clauses(formula)
        if len(formula) == 0:
            return True, []
        a = As(formula)
        while not (a.SAT and a.all_var_assigned()) and not a.UNSAT:
            print("Start")
            if a.is_bcp_eligible(): #TODO add T-propegate
                print("BCP")
                a.bcp_iteration()
            else:
                print("decide")
                if a.SAT:
                    a.decide(Literal(a.get_unassigned()[0], Sign.POS))
                else:    
                    a.decide(a.get_decision())
            if a.UNSAT:
                break
            cc = CC() #inefficient
            phrases = [eq for eq in var2eq.values() if eq is not None] #inefficient
            #print(str(phrases))
            cc.create_database(phrases)
            assigned_lits = a.get_assignment()
            #print(str([str(l) for l in assigned_lits]))
            pos_vars = [l.x for l in assigned_lits if var2eq[l.x] is not None and     bool(l.sgn)]
            neg_vars = [l.x for l in assigned_lits if var2eq[l.x] is not None and not bool(l.sgn)]
            cc.enforce_eq([var2eq[v] for v in pos_vars])
            #print(str(neg_vars))
            if any([cc.check_eq(var2eq[v]) for v in neg_vars]):
                print("T - conflict")
                #print(str(a))
                formula.append(Clause.create_clause(set([int(-lit) for lit in assigned_lits])))
                a = As(formula) #Reset
        if a.SAT:
            return True, [int(l) for l in a.get_assignment()], formula
        return False, None, formula 
                    
            
    #===========================================================================================
    #===========================================================================================
