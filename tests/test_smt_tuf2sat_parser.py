
import sys
sys.path.append("/cs/usr/matanos/ARAS-Final-Project")
sys.path.append("/cs/usr/matanos/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/SMT")

from SMTSolver import SMTSolver as SMT

PASS = True
parser = SMT.Parser()
formulas = list()
formulas.append("a!=b")
formulas.append("a==b")
formulas.append("(a)+(b)")
formulas.append("(c)*(d)")
formulas.append("(e)<->(f)")
formulas.append("(g)->(h)")
formulas.append("-(d )")
formulas.append("-((a)*(b))")
formulas.append("(a==b)*((b)+(c))")
formulas.append("((a==b)*((b)+(c)))+(a!=b)")
formulas.append("(a <= b)+(c > d)")
formulas.append("((a <= b)+(c >= d))*((a > b) + (c < d))")
formulas.append("((a <= b)+(c >= d))*((a > b) + (c1+c2 < d))")

for f in formulas:
    parser.reset(f)
    print(f + " => " + str(parser.tuf_to_tree(f)))
    print(str(parser.var2eq.items()))

if not PASS:
    print ("FAIL")
else:
    print ("PASS")
