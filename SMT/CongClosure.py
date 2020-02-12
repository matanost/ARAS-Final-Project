
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

        def check_cong(f1, f2):
            if not (CongClosure.Parser.is_function(f1) and CongClosure.Parser.is_function(f2)):
                return False
            return CongClosure.Parser.break_func(f1)[0] == CongClosure.Parser.break_func(f2)[0] #Check name equality
            
        def break_func(term):
            if not CongClosure.Parser.is_function(term):
                return (term, [])
            term = CongClosure.Parser.clean(term)
            function_name = term[:term.find("(")]
            arguments = []
            args_raw = CongClosure.Parser.clean(term[term.find("("):])
            p_cnt = 0
            gathered = ""
            #print("Found args_raw=" + args_raw)
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

        #def is_function_not_nesting(term):
        #    return bool(re.match(CongClosure.Parser.FRENN + "$", CongClosure.Parser.clean(term)))
                
        def is_eq(phrase):
            return bool(re.match(CongClosure.Parser.FTRE + CongClosure.Parser.EQ + CongClosure.Parser.FRE + "$", CongClosure.Parser.clean(phrase)))
            #phrase = CongClosure.Parser.clean(phrase)
            #if NEQ not in phrase and (phrase.count(EQ) == 1):
            #    return True
            #return False

        def is_neq(phrase):
            return bool(re.match(CongClosure.Parser.FRE + CongClosure.Parser.NEQ + CongClosure.Parser.FRE + "$", CongClosure.Parser.clean(phrase)))
            #phrase = CongClosure.Parser.clean(phrase)
            #if EQ not in phrase and (phrase.count(NEQ) == 1):
            #    return True
            #return False
    
        def split_tuf_eq(phrase):
            phrase = CongClosure.Parser.clean(phrase)
            if (phrase.count(CongClosure.Parser.EQ) > 1) or (phrase.count(CongClosure.Parser.NEQ) > 1) or (CongClosure.Parser.EQ in phrase and CongClosure.Parser.NEQ in phrase):
                raise Exception("Bad Phrase - more than a single equality term:" + phrase)
            if   CongClosure.Parser.EQ     in phrase and CongClosure.Parser.NEQ not in phrase:
                sep = CongClosure.Parser.EQ
            elif CongClosure.Parser.EQ not in phrase and CongClosure.Parser.NEQ     in phrase:
                sep =CongClosure.Parser. NEQ
            split_phrase = phrase.split(sep)
            return(CongClosure.Parser.clean(split_phrase[0]),sep,CongClosure.Parser.clean(split_phrase[1]))

    #===========================================================================================
    #===========================================================================================        
    
    class Node:

        def __init__(self, key):
            self.rep = key
            self.rank = 0
            self.key = key
            self.parents = frozenset()

        def __str__(self):
            return "(k=" + str(self.key) + ",r=" + str(self.rank) + ")=>Rep=" + str(self.rep) + ")=>p=" + str(self.parents) + "\t"


    #===========================================================================================
    #===========================================================================================

    def parse_term(self, term):
        subterms = set()
        if not CongClosure.Parser.is_function(term):
            name = term
            args = []
        else:
            name, args = CongClosure.Parser.break_func(term)
        for arg in args:
            (arg_name, arg_subterms) = self.parse_term(arg)
            subterms.add(arg)
            for st in arg_subterms:
                subterms.add(st)
        self.make_sets([term])
        subterms.add(term)
        for arg in args:
            if arg not in self.terms:
                print(str(self.terms))
            self.terms[arg].parents =  frozenset.union(self.terms[arg].parents, frozenset({term})) #Add name too?
        return (name,subterms)
            
    def __init__(self):
        self.terms = dict()

    def create_database(self, phrases):
        subterms = set()
        for p in phrases:
            (lhs, op, rhs) = CongClosure.Parser.split_tuf_eq(p)
            (lhs_name, lhs_subterms) = self.parse_term(lhs)
            (rhs_name, rhs_subterms) = self.parse_term(rhs)
            subterms.add(lhs)
            subterms.add(rhs)
            for st in lhs_subterms:
                subterms.add(st)
            for st in rhs_subterms:
                subterms.add(st)
        return subterms

    def enforce_eq(self, phrases):
        for phrase in phrases:
            (lhs, op, rhs) = CongClosure.Parser.split_tuf_eq(phrase)
            if op != CongClosure.Parser.EQ:
                raise Exception("Cannot enforce phrase which is not equality phrase")
            self.union(lhs,rhs)

    def check_eq(self, phrase):
        (lhs, op, rhs) = CongClosure.Parser.split_tuf_eq(phrase)
        if op == CongClosure.Parser.EQ:
            return self.find(lhs) == self.find(rhs)
        if op == CongClosure.Parser.NEQ:
            return self.find(lhs) != self.find(rhs)
        else: 
            raise Exception("Cannot check phrase which is not equality or inequality phrase")           

    def make_sets(self, keys):
        for key in keys:
            if key not in self.terms:
                self.terms[key] = CongClosure.Node(key)

    def find(self, x):
        if self.terms[x].rep != x:
            self.terms[x].rep = self.find(self.terms[x].rep)
        return self.terms[x].rep

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return
        x_parents = self.terms[x_root].parents
        y_parents = self.terms[y_root].parents
        if self.terms[x_root].rank < self.terms[y_root].rank:
            self.terms[x_root].rep = y_root
            self.terms[y_root].parents = frozenset.union(self.terms[x_root].parents, self.terms[y_root].parents)
        elif self.terms[x_root].rank > self.terms[y_root].rank:
            self.terms[y_root].rep = x_root
            self.terms[x_root].parents = frozenset.union(self.terms[x_root].parents, self.terms[y_root].parents)
        else:
            self.terms[y_root].rep = x_root
            self.terms[x_root].rank = self.terms[x_root].rank + 1
            self.terms[x_root].parents = frozenset.union(self.terms[x_root].parents, self.terms[y_root].parents)

        for px in x_parents:
            for py in y_parents:
                name_px, args_px = CongClosure.Parser.break_func(px)
                name_py, args_py = CongClosure.Parser.break_func(py)
                if len(args_px) == len(args_py) and name_px == name_py:                    
                    if all([self.find(item[0]) == self.find(item[1]) for item in zip(args_px, args_py)]):
                        self.union(px, py)      


    def __str__(self):
        out =  ("------------------------------\n")
        out += ("Congruance Closure=\n")
        for i,n in enumerate(self.terms.values()):
            out += str(n)
            WIDTH = 10
            if (i % WIDTH) == WIDTH-1:
                out += "\n"
        out += ("\n------------------------------\n")
        return out
