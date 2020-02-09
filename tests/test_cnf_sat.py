#sudo apt install zlib1g
#sudo apt install zlib1g-dev
#pip install python-sat

import sys
sys.path.append("/cs/usr/matanos/ARAS-Final-Project")
sys.path.append("/cs/usr/matanos/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/tests")

from Preprocess import remove_redundant_clauses
from CNF_formula import CNF_formula, Clause, Literal
from Assignment import Assignment

from random import randrange, sample
from itertools import chain
from pysat.solvers import Glucose3

ITERATION_NUM = 1000

SCALE = 10
def random_formula():
    CLAUSE_NUM = randrange(1, SCALE + 1)    
    LITERAL_NUM = randrange(1, SCALE + 1)
    lit_with_negs = [l for l in range(1,LITERAL_NUM+1)] + [-l for l in range(1,LITERAL_NUM+1)]   
    lit_in_clause = [randrange(1, 2 * LITERAL_NUM+1) for c in range(CLAUSE_NUM)]
    return [set(sample(lit_with_negs, lit_num)) for lit_num in lit_in_clause]

fail = False
fail_num = 0
false_sat = 0
false_unsat = 0
fail_formula = list()

g_sat_cnt = 0
g_unsat_cnt = 0
my_sat_cnt = 0
my_unsat_cnt = 0
for ii in range(ITERATION_NUM):
    formula = random_formula()
    my_formula = CNF_formula.create_formula(formula)
    g = Glucose3()
    for c in formula:
        g.add_clause(list(c))

    #print("Solving formula:" + str(my_formula))
    my_result = Assignment.cnf_sat_solve(my_formula)
    my_sat = my_result[0]
    my_model = my_result[1]
    g_sat = g.solve()
    g_model = g.get_model()
    g_sat_cnt    += 1 if g_sat      else 0
    my_sat_cnt   += 1 if my_sat     else 0
    g_unsat_cnt  += 1 if not g_sat  else 0
    my_unsat_cnt += 1 if not my_sat else 0
    if g_sat != my_sat:
        fail = True
        fail_num += 1        
        print("Failing formula: " + str(my_formula))
        print("Index is : " + str(ii))
        if g_sat: 
            print("Glucose thinks SAT : ")
            print(g_model)
            false_unsat += 1
            fail_formula.append((False, my_formula))
        else:
            print("My sat_solver thinks SAT : ")
            print(str(Clause.create_clause(my_model)))
            false_sat += 1
            fail_formula.append((True, my_formula))
    g.delete()
    #print("\n")
print("\n")    
print("FAIL" if fail else "PASS")
print("Failure: " + str(fail_num) + " Passing: " + str(ITERATION_NUM - fail_num))
print("False SAT: " + str(false_sat) + " False UNSAT: " + str(false_unsat))
print("Coverage:")
print("\tMY count      : SAT=" + str(my_sat_cnt) + ", UNSAT=" + str(my_unsat_cnt))
print("\tGlucose count : SAT=" + str(g_sat_cnt)  + ", UNSAT=" + str(g_unsat_cnt))
if fail:
    for f in fail_formula:
        print("False " + ("SAT  " if f[0] else "UNSAT") + str(f[1]))
