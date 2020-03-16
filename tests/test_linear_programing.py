
# from LP.linear_programing import simplex_result
import LP.linear_programing as lp
import numpy as np

TOLERANCE = 0.001

def class_example():
    A = np.array([[3, 2, 1, 2],
                  [1, 1, 1, 1],
                  [4, 3, 3, 4]])
    b = np.array([225, 117, 420])
    c = np.array([19, 13, 12, 17])
    c = c.transpose()
    s = lp.simplex_result(A, b, c)
    if s < 1827 + TOLERANCE and s > 1827 - TOLERANCE:
        print("sucssess")
    else:
        print("fail")


def homework3_ex2():
    A = np.array([[1, 1, 2],
                  [2, 0, 3],
                  [2, 1, 3]])
    b = np.array([4, 5, 7])
    c = np.array([3, 2, 4])
    c = c.transpose()
    s = lp.simplex_result(A, b, c)
    if s == 10.5:
        print("sucssess")
    else:
        print("fail")


def homework3_ex1():
    A = np.array([[-1, 1],
                  [-2, -2],
                  [-1, 4]])
    b = np.array([-1, -6, 2])
    c = np.array([1, 3])
    c = c.transpose()
    s = lp.simplex_result(A, b, c)
    if s == 'unbounded solution':
        print("sucssess")
    else:
        print("fail")


def test_unbounded():
    A = np.array([[1, 0]])
    b = np.array([3])
    c = np.array([0, 1])
    c = c.transpose()
    s = lp.simplex_result(A, b, c)
    if s == 'unbounded solution':
        print("sucssess")
    else:
        print("fail")

def test_unbounded1():
    A = np.array([[1, 0], [-1,0]])
    b = np.array([4,-4])
    c = np.array([0, 1])
    c = c.transpose()
    s = lp.simplex_result(A, b, c)
    if s == 'unbounded solution':
        print("sucssess")
    else:
        print("fail")


def test_unbounded5():
    A = np.array([[-1, 0, 0], [0 ,1, 0]])
    b = np.array([-4,3])
    c = np.array([0, 0, 1])
    c = c.transpose()
    s = lp.simplex_result(A, b, c)
    if s == 'unbounded solution':
        print("sucssess")
    else:
        print("fail")


def test_unbounded6():
    A = np.array([[1, 0, 0],[-1 ,0, 0], [0,1,0]])
    b = np.array([4,-4,3])
    c = np.array([0, 0, 1])
    c = c.transpose()
    s = lp.simplex_result(A, b, c)
    if s == 'unbounded solution':
        print("sucssess")
    else:
        print("fail")

if __name__ == "__main__":
    test_unbounded6()
    test_unbounded5()
    test_unbounded1()
    class_example()
    homework3_ex2()
    test_unbounded()
    homework3_ex1()





