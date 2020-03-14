
from SMT.SMTSolver import SMTSolver as SMT
from SAT.CNF_formula import CNF_formula

formulas = list()
req_result = list()
results = list()
fails = set()
smt = SMT()
PASS = True

formulas.append("(((x==y)+(x==z))*((f(x)==f(y))+(f(x)==f(z))))*(((f(f(x))==f(f(y)))+(f(f(x))==f(f(z))))*(f(f(f(y)))!=f(f(f(z)))))")
req_result.append(True)

formulas.append("(((x==y)+(x==z))*((f(x)==f(y))+(f(x)==f(z))))*(((f(f(x))==f(f(y)))+(f(f(x))==f(f(z))))*(f(f(f(y)))==f(g(f(z)))))")
req_result.append(True)

formulas.append("(((x==y)+(x==z))*((f(x)==f(y))+(f(x)==f(z))))*(((f(f(x))==f(f(y)))+(f(f(x))==f(f(z))))*(f(f(f(y)))==f(g(f(z)))))")
req_result.append(True)

formulas.append("(a==b)*(b==c)")
req_result.append(True)

formulas.append("(a==b)*(-(a==b))")
req_result.append(False)

formulas.append("((a)*(-(b))) + (c == d)")
req_result.append(True)

formulas.append("(x!=y)*(f(x)==f(y))")
req_result.append(True)

formulas.append("(x==g(y,z))->(f(x)==f(g(y,z)))")
req_result.append(True)

formulas.append("(f(a) == a)*(f(f(a)) != a)")
req_result.append(False)

formulas.append("(f(f(f(a))) == a)*((f(f(f(f(f(a))))) == a)*(f(a) != a))")
req_result.append(False)

formulas.append("((f(x1,y1,z1) == f(x2,y2,z2))*(x1 == x2))*((y1 == y2)*(z1 == z2))")
req_result.append(True)

formulas.append("((f(x1,y1,z1) == f(x2,y2,z2))*(x1 != x2))*((y1 == y2)*(z1 == z2))")
req_result.append(True)

formulas.append("((f(x1,y1,z1) != f(x2,y2,z2))*(x1 == x2))*((y1 == y2)*(z1 == z2))")
req_result.append(False)

for i, f in enumerate(formulas):
    print("Solving f=" + str(f))
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
