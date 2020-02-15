
import sys
sys.path.append("/cs/usr/matanos/ARAS-Final-Project")
sys.path.append("/cs/usr/matanos/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/SMT")

from smt_solver import smt_solver as smt

PASS = True

smt.Parser.tuf_to_tree("(a)+(b)")
smt.Parser.tuf_to_tree("(c)*(d)")
smt.Parser.tuf_to_tree("(e)<->(f)")
smt.Parser.tuf_to_tree("(g)->(h)")
smt.Parser.tuf_to_tree("-(d )")
smt.Parser.tuf_to_tree("-((a)*(b))")
smt.Parser.tuf_to_tree("(a==b)*((b)+(c))")

if not PASS:
    print ("FAIL")
else:
    print ("PASS")
