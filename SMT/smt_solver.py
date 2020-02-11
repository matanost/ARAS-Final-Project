
from CNF_formula import Literal
class smt_solver:

    EQ = "=="
    NEQ = "!="

    def is_eq(phrase):
        phrase = phrase.rstrip().strip()
        phrase = phrase.replace(" ", "")
        if NEQ not in phrase and (phrase.count(EQ) == 1):
            return True
        return False

    def is_neq(phrase):
        phrase = phrase.rstrip().strip()
        phrase = phrase.replace(" ", "")
        if EQ not in phrase and (phrase.count(NEQ) == 1):
            return True
        return False
    
    def split_tuf_eq(phrase):
        phrase = phrase.rstrip().strip()
        phrase = phrase.replace(" ", "")
        if (phrase.count(EQ) > 1) or (phrase.count(NEQ) > 1) or (EQ in phrase and NEQ in phrase):
            raise Exception("Bad Phrase - more than a single equality term:" + phrase)
        if   EQ     in phrase and NEQ not in phrase:
            sep = EQ
        elif EQ not in phrase and NEQ     in phrase:
            sep = NEQ
        split_phrase = phrase.split(sep)
        return(split_phrase[0],sep,split_phrase[1])            
        
    class Assignment:

        def __init__(formula):
            self.formula = formula #Should be list of sets of strings. TODO other representation?
            self.lit = set():
            self.conflict = None

    def propagate:
        pass

    def decide:
        pass

    def conflict:
        pass

    def explain:
        pass

    def backjump:
        pass

    def fail:
        pass

    def t_conflict:
        pass

    def t_propagate:
        pass

    def t_explain:
        pass

    def learn:
        pass

    def forget:
        pass

    def restart:
        pass
    
