from Tree import Tree
from Tsetin_transformation import TsetinTransformation
from CNF_formula import *

def simple_test_or():
    """
    q = 1||2 convert to (3||!1)&&(3||!2)&&(!3||1||2)
    :return:
    """
    equation = Tree('OR')
    operation = equation.get_root()
    operation.set_left_son(1)
    operation.set_right_son(2)
    new_equation = TsetinTransformation(2)
    cnf_equation = CNF_formula()
    cnf_equation = new_equation.run_TsetinTransformation(operation)
    print(cnf_equation)

def test_or_not():
    """
    q = !(1||2) convert to (3||!1)&&(3||!2)&&(!3||1||2)
    :return:
    """
    equation = Tree('NOT')
    operation = equation.get_root()
    operation.set_left_son('OR')
    left = operation.get_left_son()
    left.set_right_son(1)
    left.set_left_son(2)
    new_equation = TsetinTransformation(2)
    cnf_equation = CNF_formula()
    cnf_equation = new_equation.run_TsetinTransformation(operation)
    print(cnf_equation)

if __name__ == "__main__":
    simple_test_or()
    print("\n")
    test_or_not()
