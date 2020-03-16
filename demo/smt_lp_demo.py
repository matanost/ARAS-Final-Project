
from SMT.SMTSolver import SMTSolver as SMT
from SAT.CNF_formula import CNF_formula

formulas = list()
req_result = list()
results = list()
fails = set()
smt = SMT()
PASS = True

formulas.append("(a<=4)*(b<=3)")
req_result.append(True)
formulas.append("(-a>=-4)*(b<=3)")
req_result.append(True)
formulas.append("((3a1 + -a2 + 4a3 <=10)*(a1<=3))*(a2 <= 100)")
req_result.append(True)

formulas.append("(a<=4)*(4<=a)")
req_result.append(True)

formulas.append("(a<=4)+(4<=a)")
req_result.append(True)

for i, f in enumerate(formulas):
    print("Solving formula=" + str(f))
    results.append(smt.solve(f))
    print("SAT("+str(i)+")= " + str(results[i][0]) + ", Assingment("+str(i)+")=" + str(results[i][1]) + "\n")
    if results[i][0] != req_result[i]:
        PASS = False
        fails.add((i))

if not PASS:
    print ("FAIL")
    print (str(fails))
else:
    print ("PASS")
