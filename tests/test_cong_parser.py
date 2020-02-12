
import sys
sys.path.append("/cs/usr/matanos/ARAS-Final-Project")
sys.path.append("/cs/usr/matanos/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/tests")
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project/SMT")

from CongClosure import CongClosure as CC

functions = ["x", "f(x)", "f_Afeaf(x1)", "f(x,y)", "f(x,,t)", "f(x,a,s,)", "()", "f(,)x)", "f(x)f"]
req_result = [False, True, True, True, False, False, False, False, False]
PASS = True
for i,f in enumerate(functions):
    result = CC.Parser.is_function(f)
    if result != req_result[i]:
        PASS = False
    print(f + " : " + str(result))

functions = ["f(x,y,z)", "f(x,y,g(x))", "F(x(x),t(x),t(x,e,a,y(g_h)))"]
for f in functions:
    (name, args) = CC.Parser.break_func(f)
    print("Original=" + f)
    print("Name=" + name)
    print("Arguments=" + str(args) + "\n")
'''terms = ["x==q", "x="]
req_result_1 = []
req_result_2 = []
for i,f in enumerate(functions):
    result = CC.Parser.is_function(f)
    if result != req_result[i]:
        PASS = False
    print(f + " : " + str(result))'''
   

if not PASS:
    print ("FAIL")
else:
    print ("PASS")
