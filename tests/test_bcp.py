
import sys
sys.path.append("/cs/usr/matanos/ARAS-Final-Project")
sys.path.append("/cs/usr/matanos/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/tests")

from preprocess import remove_redundant_clauses
from CNF_formula import CNF_formula, Clause, Literal
from Assignment import Assignment

f = CNF_formula()

c1 = Clause()
c2 = Clause()
c3 = Clause()
c4 = Clause()
for i in {1}:
    c1.append(Literal(i))
for i in {-1,2}:
    c2.append(Literal(i))
for i in {-1,-2,3}:
    c3.append(Literal(i))
for i in {4}:
    c4.append(Literal(i))
f.append(c1)
f.append(c2)
f.append(c3)
f.append(c4)
print("Original formula={}\n".format(f))

a = Assignment(f)
print("Initial Assignment:{}\n".format(a))

a.plp_iteration()
print("Assignment after PLP:{}\n".format(a))

while a.is_bcp_eligible():
    a.bcp_iteration()
    print("Assignment after BCP iteration:{}\n".format(a))
    
print("Final Assignment:{}\n".format(a))


