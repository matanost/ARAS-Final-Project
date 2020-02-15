
from CNF_formula import Literal
from Tsetin_transformation import TsetinTransformation as TT
from Tree import Node as TN
from CongClosure import Parser as CCP
import re

class SMTSolver:
    
    class Parser:

        def __init__(self):        
            self.avail_literal = 1
            self.legal_2ops = ["+", "*", "->", "<->"]
            self.legal_1ops = ["-"]
            self.match_2op_re = "([(].*[)])(\W+)([(].*[)])$"
            self.match_1op_re = "(-)([(].*[)])$"             
                
        def tuf_to_tree(self, tuf): #TODO
            tuf = tuf.strip().rstrip().replace(" ","")
            match_2op = re.match(self.match_2op_re,tuf)
            match_1op = re.match(self.match_1op_re,tuf)                        
            if bool(match_1op) and bool(match_2op):
                raise Exception("Both 2op and 1op matched: tuf=" + tuf)
            if not bool(match_1op) and not bool(match_2op):
                lit = self.avail_literal
                self.avail_literal += 1
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

    
    
    #===========================================================================================
    #===========================================================================================
    
    def propagate():
        pass

    def decide():
        pass

    def conflict():
        pass

    def explain():
        pass

    def backjump():
        pass

    def fail():
        pass

    def t_conflict():
        pass

    def t_propagate():
        pass

    def t_explain():
        pass

    def learn():
        pass

    def forget():
        pass

    def restart():
        pass
    
