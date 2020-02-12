
import re

class CongClosure: 

    #===========================================================================================
    #===========================================================================================    

    class Parser:

        EQ = "=="
        NEQ = "!="
        FRENN = "\w+[(](\w+,)*\w+[)]"
        FRE = "\w+[(].*[)]"
        FTRE = "\w+([(](\w+,)*\w+[)]){,1}"

        def break_func(term):
            if not CongClosure.Parser.is_function(term):
                raise Exception("Term " + term + " is not a function")
            term = CongClosure.Parser.clean(term)
            function_name = term[:term.find("(")]
            arguments = []
            args_raw = CongClosure.Parser.clean(term[term.find("("):])
            p_cnt = 0
            gathered = ""
            print("Found args_raw=" + args_raw)
            for c in args_raw:
                if c == "(":
                    gathered += c
                    p_cnt += 1
                elif c == ")":
                    gathered += c
                    p_cnt -= 1
                elif p_cnt == 0 and  c == ",":
                    if len(gathered) > 0:
                        arguments.append(gathered)
                    gathered = ""
                else:
                    gathered += c
            if len(gathered) > 0:
                arguments.append(gathered)
            return (function_name, arguments)
        
        def clean(string):
            string = string.rstrip().strip().replace(" ", "")
            while string.startswith("(") and string.endswith(")"):
                string = string[1:-1]
            return string

        def is_function(term):
            return bool(re.match(CongClosure.Parser.FRE + "$", CongClosure.Parser.clean(term)))

        def is_function_not_nesting(term):
            return bool(re.match(CongClosure.Parser.FRENN + "$", CongClosure.Parser.clean(term)))
                
        def is_eq(phrase):
            return bool(re.match(CongClosure.Parser.FTRE + CongClosure.Parser.EQ + CongClosure.Parser.FTRE + "$", CongClosure.Parser.clean(phrase)))
            #phrase = CongClosure.Parser.clean(phrase)
            #if NEQ not in phrase and (phrase.count(EQ) == 1):
            #    return True
            #return False

        def is_neq(phrase):
            return bool(re.match(CongClosure.Parser.FTRE + CongClosure.Parser.NEQ + CongClosure.Parser.FTRE + "$", CongClosure.Parser.clean(phrase)))
            #phrase = CongClosure.Parser.clean(phrase)
            #if EQ not in phrase and (phrase.count(NEQ) == 1):
            #    return True
            #return False
    
        def split_tuf_eq(phrase):
            phrase = CongClosure.Parser.clean(phrase)
            if (phrase.count(CongClosure.Parser.EQ) > 1) or (phrase.count(CongClosure.Parser.NEQ) > 1) or (CongClosure.Parser.EQ in phrase and CongClosure.Parser.NEQ in phrase):
                raise Exception("Bad Phrase - more than a single equality term:" + phrase)
            if   EQ     in phrase and NEQ not in phrase:
                sep = EQ
            elif EQ not in phrase and NEQ     in phrase:
                sep = NEQ
            split_phrase = phrase.split(sep)
            return(CongClosure.Parser.clean(split_phrase[0]),sep,CongClosure.Parser.clean(split_phrase[1]))

    #===========================================================================================
    #===========================================================================================        
    
    class Node:

        def __init__(self, key):
            self.parent = key
            self.rank = 0
            self.key = key

        def __str__(self):
            return "(k=" + str(self.key) + ",r=" + str(self.rank) + ")=>p=" + str(self.parent) + "\t"


    #===========================================================================================
    #===========================================================================================
    
    def __init__(self):
        self.nodes = dict()

    def create_database(self, phrases):
        terms = set()
        for p in phrases:
            (lhs, op, rhs) = CongClosure.Parser.split_tuf_eq(phrase)
            terms.add(lhs)
            terms.add(rhs)
        self.make_sets(terms)

    def enforce_eq(self, phrase):
        (lhs, op, rhs) = CongClosure.Parser.split_tuf_eq(phrase)
        if op != EQ:
            raise Exception("Cannot enforce phrase which is not equality phrase")
        self.union(lhs,rhs)
        #TODO propegate to other terms        

    def check_eq(self, phrase):
        (lhs, op, rhs) = CongClosure.Parser.split_tuf_eq(phrase)
        if op == EQ:
            return self.find(x) == self.find(y)
        if op == NEQ:
            return self.find(x) != self.find(y)
        else: 
            raise Exception("Cannot check phrase which is not equality or inequality phrase")           

    def make_sets(self, keys):
        for key in keys:
            if key not in self.nodes:
                self.nodes[key] = CongClosure.Node(key)

    def find(self, x):
        if self.nodes[x].parent != x:
            self.nodes[x].parent = self.find(self.nodes[x].parent)
        return self.nodes[x].parent

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return        
        if self.nodes[x_root].rank < self.nodes[y_root].rank:
            self.nodes[x_root].parent = y_root
        elif self.nodes[x_root].rank > self.nodes[y_root].rank:
            self.nodes[y_root].parent = x_root
        else:
            self.nodes[y_root].parent = x_root
            self.nodes[x_root].rank = self.nodes[x_root].rank + 1

    def __str__(self):
        out =  ("------------------------------\n")
        out += ("Congruance Closure=\n")
        for i,n in enumerate(self.nodes.values()):
            out += str(n)
            WIDTH = 10
            if (i % WIDTH) == WIDTH-1:
                out += "\n"
        out += ("------------------------------\n")
        return out
