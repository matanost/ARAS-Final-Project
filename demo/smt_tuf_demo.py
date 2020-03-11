import sys
sys.path.append("/cs/usr/matanos/ARAS-Final-Project")
sys.path.append("/cs/usr/matanos/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/SMT")


from SMTSolver import SMTSolver as SMT
from CNF_formula import CNF_formula

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

for i, f in enumerate(formulas):
    print("Solving f=" + str(f))
    results.append(smt.solve(f))
    print("SAT("+str(i)+")= " + str(results[i][0]) + ", Assingment("+str(i)+")=" + str(results[i][1]) + "\n")
    if results[i][0] != req_result[i]:
        PASS = False
        fails.add((2,i))

if not PASS:
    print ("FAIL")
    print (str(fails))
else:
    print ("PASS")
