from LP.linear_programing import linearPrograming
import numpy as np


def class_example():
    A = np.array([[3, 2, 1, 2],
                  [1, 1, 1, 1],
                  [4, 3, 3, 4]])
    b = np.array([225, 117, 420])
    c = np.array([19, 13, 12, 17])
    c = c.transpose()
    s = linearPrograming(A, b, c)
    print(s.simplex_result())


def homework3_ex2():
    A = np.array([[1, 1, 2],
                  [2, 0, 3],
                  [2, 1, 3]])
    b = np.array([4, 5, 7])
    c = np.array([3, 2, 4])
    c = c.transpose()
    s = linearPrograming(A, b, c)
    print(s.simplex_result())


if __name__ == "__main__":
    class_example()
    print("\n")
    homework3_ex2()
