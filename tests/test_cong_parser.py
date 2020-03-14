
from SMT.CongClosure import CongClosure as CC
from SMT.CongClosure import Parser as CCP
from SMT.SMTSolver_Parser import SMTSolver_Parser

print("Check is_function")
functions = ["x", "f(x)", "f_Afeaf(x1)", "f(x,y)", "f(x,,t)", "f(x,a,s,)", "()", "f(,)x)", "f(x)f"]
req_result = [False, True, True, True, True, True, False, True, False]
PASS = True
for i,f in enumerate(functions):
    result = CCP.is_function(f)
    if result != req_result[i]:
        PASS = False
    print(f + " : out=" + str(result) + ", req=" + str(req_result[i]))

print("Check parse_term")
functions = ["f(x,y,z)", "f(x,y,g(x))", "F(x(x),t(x),t(x,e,a,y(g_h)))"]
req_name = ["f", "f", "F"]
req_subterms = [["f(x,y,z)", "x", "y", "z"], ["f(x,y,g(x))", "x", "y", "g(x)"], ["F(x(x),t(x),t(x,e,a,y(g_h)))", "x(x)", "x", "t(x)", "t(x,e,a,y(g_h))", "e", "a", "y(g_h)", "g_h"]]
for i,f in enumerate(functions):
    cong = CC()
    (name, subterms) = cong.parse_term(f)
    print("Original=" + f)
    print("Name=" + name)
    print("Subterms=" + str(subterms) + "\n")
    #print(str(cong))
    if name != req_name[i] or (set(subterms) != set(req_subterms[i])):
        PASS = False    

print("Check union/find")
phrases = ["x==y", "x==z", "f(x)==w2", "g(z,y)==w1", "g(x,z)==w2", "x==x"]
cong = CC()
subterms = cong.create_database(phrases)
if subterms != {"x", "y", "z", "w1", "w2", "f(x)", "g(z,y)", "g(x,z)"}:
    print("Subterms error:" + str(subterms))
    PASS = False
cong.enforce_eq(phrases)
print(str(cong))
check_phrases = ["x != w1", "z != w1", "y == z", "z == y", "g(x,z) == g(z,y)", "f(x) == w1", "x == x", "x != w2"]
for p in check_phrases:
    if not cong.check_eq(p):
        print("Failed:" + p)
        PASS = False

check_phrases = ["x == w1", "z == w1", "y != z", "z != y", "g(x,z) != g(z,y)", "f(x) != w1", "x != x", "x == w2"]
for p in check_phrases:
    if cong.check_eq(p):
        print("Failed, should not be true:" + p)
        PASS = False

smt_p = SMTSolver_Parser()
tuf = ["a == b"]
for t in tuf:
    parsed = smt_p.tuf_to_tree(t)
    print(str(parsed) + "\n" + str(smt_p.var2eq.values()))
    
if not PASS:
    print ("FAIL")
else:
    print ("PASS")
