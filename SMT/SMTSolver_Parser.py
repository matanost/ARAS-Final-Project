from CongClosure import CongClosure as CC
from CongClosure import Parser as CCP
from Tree import Node as TN
from CNF_formula import Literal, Clause, Sign
import re

class SMTSolver_Parser:

    def __init__(self):        
        self.avail_literal = 1
        self.match_2op_re = "([(].*[)])(\W+)([(].*[)])$"
        self.match_1op_re = "(-)([(].*[)])$"
        self.var2eq = dict()
        self.op_translate = {"+":"OR", "*":"AND", "->":"IF", "<->":"IFF", "-":"NOT"}
        self.theory = "TUF"
            
    def reset(self, tuf):
        self.avail_literal = 1
        self.var2eq = dict()
        self.theory = "TUF"            
        if any([sign in tuf.replace("<->","").replace("->","") for sign in ["<", ">"]]):
            self.theory = "LP"

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
            tuf = SMTSolver_Parser.standard(tuf)
            for var, eq in self.var2eq.items():
                if eq == tuf:
                    return TN(None, var)
                if eq == SMTSolver_Parser.negate(tuf):
                    return TN(None, -var)
            lit = self.avail_literal
            self.avail_literal += 1
            if self.theory is "TUF":
                if CCP.is_neq(tuf) :
                    tuf, lit = SMTSolver_Parser.negate(tuf), -lit
            elif self.theory is "LP":                    
                if any([sign in tuf for sign in [">", "<", "!="]]) and not any([sign in tuf for sign in [">=", "<="]]):
                    tuf, lit = SMTSolver_Parser.negate(tuf), -lit
                if "==" in tuf:
                    self.avail_literal -= 1
                    print(tuf)
                    lhs, op, rhs = CCP.split_tuf_eq(tuf)
                    return self.tuf_to_tree("({0}<={1})*({1}<={0})".format(lhs, rhs))
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

    def standard_lp(phrase):
        if ">=" in phrase:
            terms = phrase.split(">=")
            return terms[1] + "<=" + terms[0]
        if "<" in phrase and "<=" not in phrase:
            terms = phrase.split("<")
            return terms[1] + ">" + terms[0]
        return phrase
        
    def negate_lp(phrase):
        if "<=" in phrase:
            phrase = phrase.replace("<=", ">")
        elif ">=" in phrase:
            phrase = phrase.replace(">=", "<")
        elif ">" in phrase:
            phrase = phrase.replace(">", "<=")
        elif "<" in phrase:
            phrase = phrase.replace("<", ">=")
        return phrase

    def standard(phrase):
        if any([sign in phrase for sign in ["<", ">", "<=", ">="]]):
            return SMTSolver_Parser.standard_lp(phrase)
        else:
            return phrase
        
    def negate(phrase):
        if any([sign in phrase for sign in ["<", ">", "<=", ">="]]):
            return SMTSolver_Parser.negate_lp(phrase)
        else:
            return CCP.negate(phrase) 
