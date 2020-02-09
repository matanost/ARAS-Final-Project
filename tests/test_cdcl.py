
import sys
sys.path.append("/cs/usr/matanos/ARAS-Final-Project")
sys.path.append("/cs/usr/matanos/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/tests")

from Preprocess import remove_redundant_clauses
from CNF_formula import CNF_formula, Clause, Literal
from Assignment import Assignment

formulas = list()
formulas.append(CNF_formula.create_formula([{-1,3},{-3,-1,2},{-3,4},{-4,-2}]))
formulas.append(CNF_formula.create_formula([{1},{1}]))
formulas.append(CNF_formula.create_formula([{1},{-1}]))
formulas.append(CNF_formula.create_formula([{-1,2},{-1,-2,3},{-1,-3,4}]))
#formulas.append()
required_results = [True, True, False, True]
result_record = list()
for i,f in enumerate(formulas):
    print("result for formula :" + str(i) + " = " + str(f))
    result = Assignment.cnf_sat_solve(f)
    if result[0]:
        print("SAT")
        print(str(Clause.create_clause(result[1])))
    else:
        print("UNSAT")
    result_record.append(bool(result[0]))
    print("Required result is :" + ("SAT" if required_results[i] else "UNSAT"))
    print("\n\n")

if any([required is not record for required in required_results for record in result_record]):
    print ("FAIL")
else:
    print ("PASS")
