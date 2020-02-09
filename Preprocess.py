
from itertools import combinations
import copy
from CNF_formula import CNF_formula

#Remove redundant clauses, either bacuase they are duplication of clauses, or becuase they're tautologies.
def remove_redundant_clauses(formula):

    formula = CNF_formula.create_formula(list(dict.fromkeys(formula)))
    formula_copy = copy.deepcopy(formula)
    for clause in formula:
        if len(clause) == 0:
            formula_copy.remove(clause)            
        else :
            for lit_comb in combinations(clause,2):
                l1,l2 = lit_comb
                if l1 == -l2:
                    formula_copy.remove(clause)
    return formula_copy                                              
    
