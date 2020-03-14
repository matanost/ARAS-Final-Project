
import sys
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project")

from SMT.SMTSolver import SMTSolver_Parser as SMTP

PASS = True
parser = SMTP()
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
