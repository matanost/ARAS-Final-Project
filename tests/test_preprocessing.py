
import sys
sys.path.append("/cs/usr/matanos/ARAS-Final-Project")
sys.path.append("/cs/usr/matanos/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/tests")

from Preprocess import remove_redundant_clauses
from CNF_formula import CNF_formula, Clause, Literal

f = CNF_formula()

c1 = Clause()
c2 = Clause()
c3 = Clause()
c4 = Clause()
c5 = Clause()
c6 = Clause()
for i in {1,2,3}:
    c1.append(Literal(i))
    c2.append(Literal(i))
for i in {1,2,2}:
    c3.append(Literal(i))
for i in {1,2,-2}:
    c4.append(Literal(i))

f.append(c1)
f.append(c2)
f.append(c3)
f.append(c4)
f.append(c5)
f.append(c6)

f_pp = remove_redundant_clauses(f)

f_target = CNF_formula()
c1_target = Clause()
c2_target = Clause()
for i in {1,2,3}:
    c1_target.append(Literal(i))
for i in {1,2}:
    c2_target.append(Literal(i))
f_target.append(c1_target)
f_target.append(c2_target)

print("Original:")
print(f)
print("\nPreProcessed:")
print(f_pp)

print("\nExpected:")
print(f_target)

print("Result is {}".format("Success" if (f_pp == f_target) else "Fail"))
