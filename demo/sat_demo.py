import sys
sys.path.append("/cs/usr/matanos/ARAS-Final-Project")
sys.path.append("/cs/usr/matanos/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/SMT")


from Preprocess import remove_redundant_clauses
from CNF_formula import CNF_formula, Clause, Literal
from Assignment import Assignment

formulas = list()
result_record = list()
required_results = list()
formulas.append("((a)*(b))+((-(a))*(c))")
required_results.append(True)
formulas.append("((a)*(b))<->((-(a))*(c))")
required_results.append(True)

formulas.append("((a)*(b))*(((a)*(b))->((-(a))*(c)))")
required_results.append(False)

formulas.append("((a)->(b))+((-(a))*(c))")
required_results.append(True)

formulas.append("((-(a))*(-(b)))*((-(a))*(b))")
required_results.append(False)


for i,f in enumerate(formulas):
    print("result for formula :" + str(i) + " = " + str(f))
    result, values = Assignment.sat_solve(f)
    if result[0]:
        print("SAT")
        #print(str(Clause.create_clause(result[1])))
        #print(values)
        print("{}".format(str([("" if lit in result[1] else "-") + val for lit,val in values.items()])))
    else:
        print("UNSAT")
    result_record.append(bool(result[0]))        
    print("Required result is :" + ("SAT" if required_results[i] else "UNSAT"))    
    print("\n\n")

formulas = list()
formulas.append(CNF_formula.create_formula([{-1,3},{-3,-1,2},{-3,4},{-4,-2}]))
required_results.append(True)
formulas.append(CNF_formula.create_formula([{1},{1}]))
required_results.append(True)
formulas.append(CNF_formula.create_formula([{1},{-1}]))
required_results.append(False)
formulas.append(CNF_formula.create_formula([{-1,2},{-1,-2,3},{-1,-3,4}]))
required_results.append(True)
formulas.append(CNF_formula.create_formula([{1},{-1},{1,-1}]))
required_results.append(False)
formulas.append(CNF_formula.create_formula([{-1},{-1},{1},{1,-1},{1},{-1}]))
required_results.append(False)
formulas.append(CNF_formula.create_formula([{1,2},{1,-2},{-1,2},{-1,-2}]))
required_results.append(False)
formulas.append(CNF_formula.create_formula([{1,4},{1,5},{1,3},{-1,2},{-2,3},{-2,-3}]))
required_results.append(True)

for i,f in enumerate(formulas):
    print("Preprocessed version=" + str(remove_redundant_clauses(f)))
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

    
print("Required:" + str(required_results))
print("Output  :"   + str(result_record))
if any([req != rec for req, rec in zip(required_results, result_record)]):
    print ("FAIL")
else:
    print ("PASS")
