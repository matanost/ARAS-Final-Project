
import sys
sys.path.append("/cs/usr/matanos/ARAS-Final-Project")
sys.path.append("/cs/usr/matanos/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/SMT")

from SMTSolver import SMTSolver as SMT
from CNF_formula import CNF_formula

PASS = True
formulas = list()
var2eqs = list()
results = list()
req_result = list()

formulas.append([{1},{4,5}])
var2eqs.append({1:"a==b", 4:None, 5:None})
req_result.append(True)

formulas.append([{1,2},{-1,2},{-2,-3},{4,5}])
var2eqs.append({1:"a==b",2:"b==c", 3:"a==c", 4:None, 5:None})
req_result.append(True)

formulas.append([{-1,3},{-3,-1,2},{-3,4},{-4,-2}])
var2eqs.append({1:None, 2:None, 3:None, 4:None})
req_result.append(True)

formulas.append([{1},{1}])
var2eqs.append({1:None})
req_result.append(True)

formulas.append([{1},{-1}])
var2eqs.append({1:None})
req_result.append(False)

formulas.append([{-1,2},{-1,-2,3},{-1,-3,4}])
var2eqs.append({1:None, 2:None, 3:None, 4:None})
req_result.append(True)

formulas.append([{1},{-1},{1,-1}])
var2eqs.append({1:None})
req_result.append(False)

formulas.append([{-1},{-1},{1},{1,-1},{1},{-1}])
var2eqs.append({1:None})
req_result.append(False)

formulas.append([{1,2},{1,-2},{-1,2},{-1,-2}])
var2eqs.append({1:None, 2:None})
req_result.append(False)

formulas.append([{1,4},{1,5},{1,3},{-1,2},{-2,3},{-2,-3}])
var2eqs.append({1:None, 2:None, 3:None, 4:None, 5:None})
req_result.append(True)

formulas.append([{1,2},{3,4},{5,6},{-7}])
var2eqs.append({1:"x==y", 2:"x==z", 3:"f(x)==f(y)", 4:"f(x)==f(z)", 5:"f(f(x))==f(f(y))", 6:"f(f(x))==f(f(z))", 7:"f(f(f(y)))==f(f(f(z)))"})
req_result.append(True)

formulas.append([{1,2},{3,4},{5,6},{7}])
var2eqs.append({1:"x==y", 2:"x==z", 3:"f(x)==f(y)", 4:"f(x)==f(z)", 5:"f(f(x))==f(f(y))", 6:"f(f(x))==f(f(z))", 7:"f(f(f(y)))==f(g(f(z)))"})
req_result.append(True)

#formulas.append()
#var2eqs.append()
#req_result.append()

fails = set()
smt = SMT()
for i, f in enumerate(formulas):
    f_cnf = CNF_formula.create_formula(f)
    print("Solving f=" + str(f_cnf))
    results.append(smt.solve_cnf(f_cnf, var2eqs[i]))
    print("SAT("+str(i)+")= " + str(results[i][0]) + ", Assingment("+str(i)+")=" + str(results[i][1]))
    print("Formula at end=" + str(results[i][2]) + "\n")
    if results[i][0] != req_result[i]:
        PASS = False
        fails.add(i)

if not PASS:
    print ("FAIL")
    print (str(fails))
else:
    print ("PASS")
