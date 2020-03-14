
from LP.linear_programing import linearPrograming
from SMT.SMTSolver import SMTSolver as SMT
from SAT.CNF_formula import CNF_formula

#==================================================================================================
#==================================================================================================
PASS = True
inequalities = list()
results = list()
req_result = list()

inequalities.append(["a1 + a2 < 3", "a1 <= 4", "a3 <= 5"])
inequalities.append(["a1 < 3", "a1 > 4"])
#req_result.append()

fails = set()
smt = SMT()
for i, ineq in enumerate(inequalities):
    print("Parsing ineq=" + str(ineq))
    results.append(smt.convert_to_simplex(ineq))
    print("Bound({0})= {2}, Matrix({0})={1}, Target({0})={3}\n".format(str(i), str(results[-1][0]), str(results[-1][1]), str(results[-1][2])))
    #if results[i][0] != req_result[i]:
    #    PASS = False
    #    fails.add((2,i))

fails = set()
smt = SMT()
for i, ineq in enumerate(inequalities):
    print("Solving ineq=" + str(ineq))
    results.append(smt.check_lp(ineq))
    print(results[-1])
    #if results[i][0] != req_result[i]:
    #    PASS = False
    #    fails.add((2,i))
   

if not PASS:
    print ("FAIL")
    print (str(fails))
else:
    print ("PASS")
