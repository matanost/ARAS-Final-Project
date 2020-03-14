
import sys
sys.path.append("/mnt/c/Users/Matan/Documents/ARAS-Final-Project")

from SMT.CongClosure import CongClosure as CC

N = 10
keys = [str(chr(ord('a') + i)) for i in range(N)]

cc = CC()
cc.make_sets(keys)

PASS = True

print("\nFirst version\n")
print(str(cc))

if any([cc.find(key) != key for key in keys]):
    PASS = False

for i in range(N-1):
    cc.union(keys[i],keys[i+1])

    print("Middle version (#1," + str(i) + ") - 0 to i+1 are united\n")
    print(str(cc))

    if any([cc.find(keys[j]) != cc.find(keys[i+1]) for j in range(i+2)]) or any([cc.find(keys[j]) != keys[j] for j in range(i+2,N)]): 
        PASS = False

    print("Middle version (#2," + str(i) + ") - 0 to i+1 are united, did some find\n")
    print(str(cc))

print("Final version #1 - All has been united\n")
print(str(cc))

if any([cc.find(keys[i]) != cc.find(keys[0]) for i in range(N)]):
    PASS = False

if any([not cc.find(keys[i]) == cc.find(keys[j]) for i in range(N) for j in range(N)]):
    PASS = False

print("Final version #2 - All has been united\n")
print(str(cc))

if not PASS:
    print ("FAIL")
else:
    print ("PASS")
