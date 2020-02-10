
import enum

class CNF_formula:
    def __init__(self):
        self.f = list()
        self.num_clause = 0

    def append(self, y):
        self.f.append(y)
        self.num_clause += 1
        
    def index(self, c):
        return self.f.index(c)

    def remove(self, c):
        if c in self.f:
            self.f.remove(c)
            self.num_clause -= 1
            
    def __iter__(self):
        return self.f.__iter__()

    def __next__(self):
        return self.f.__next__()

    def __eq__(self,other):
        if not isinstance(other, CNF_formula):
            return False
        if len(self.f) != len(other.f):
            return False
        for c, co in zip(self.f, other.f):
            if c != co:
                return False
        return True

    def __ne__(self,other):
        return not self == other

    def __str__(self):
        out = "("
        for i,c in enumerate(self.f):
            out = out + "<" "c" + str(i) +  "=" + str(c) + ">"
        out = out + ")"
        return out
        
    def __len__(self):
        return len(self.f)

    #Recieve a list of integer sets, and parse to CNF_formula
    @staticmethod
    def create_formula(clause_list):
        formula = CNF_formula()
        for c in clause_list:
            formula.append(Clause.create_clause(set([l for l in c])))
        return formula
    
class Sign(enum.Enum):
    
        POS = True
        NEG = False
        
        def __bool__(self):
            return self.value

        def __neg__(self):
            if self == Sign.NEG:
                return Sign.POS
            elif self == Sign.POS:
                return Sign.NEG
            else:
                raise Exception("Comparison problem enum={}".format(self.value))
        
class Literal:
        
    def __init__(self, y, sign=Sign.POS):
        if y < 0:
            self.x = -y
            self.sgn = Sign.NEG
        else:
            self.x = y
            self.sgn = sign

    def __eq__(self, other):
        if not isinstance(other, Literal):
            return False
        return (self.x == other.x) and (self.sgn == other.sgn)

    def __ne__(self, other):
        return not self == other

    def __neg__(self):
        return Literal(self.x, -self.sgn)

    def __hash__(self):
        return hash(self.x) if self.sgn else hash(-self.x)

    def __str__(self):
        return ("" if self.sgn else "-") + str(self.x)

class Clause:
    def __init__(self):
        self.c = frozenset()
        self.num_literal = 0
        self.is_sat = False

    def append(self, y):
        self.c = frozenset.union(self.c, frozenset({y}))
        self.num_literal += 1
        
    def get_num_literal(self):
        return self.num_literal

    def __iter__(self):
        return self.c.__iter__()

    def __next__(self):
        return self.c.__next__()


    #def remove(self, l):
    #    if l in self.c:
    #        temp_list = list(self.c).remove(l) #TODO
    #        self.c = frozenset(temp_list)
    #        self.num_literal -= 1

    def __eq__(self, other):
        if not isinstance(other, Clause):                                   
            return False        
        return self.c == other.c

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.c)

    def __str__(self):
        out = "{{"
        for i,l in enumerate(self.c):
            out += str(l) + ("," if i < (len(self.c) - 1) else "")
        out += "}}"
        return out 
    
    def __len__(self):
        return len(self.c)

    def __neg__(self):
        neg_c = Clause()
        for l in self.c:
            neg_c.append(-l)
        return neg_c

    #Recieve set of integers, and parse to Clause.
    @staticmethod
    def create_clause(literal_set):
        clause = Clause()
        for l in literal_set:
            if isinstance(l, Literal):
                clause.append(l)
            elif isinstance(l, int):
                clause.append(Literal(l))
            else:
                raise Exception("Clause input contains an object which is not Literal or int.")
        return clause
            
