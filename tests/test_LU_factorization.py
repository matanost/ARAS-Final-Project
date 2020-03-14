from LP.LU_factorization import LU_factorization
import numpy as np


def class_example_LU_treshhold_2():
    A = np.array([[2,1,0],
                  [1,1,0],
                  [3,3,1]])
    s = LU_factorization(A)
    eta_matrix, leaving_vars = s.run_LU_factorization()


    res = np.identity(eta_matrix[0].shape[0])
    for i in range(len(eta_matrix)):
        res = np.dot(res, eta_matrix[i])
    print(A)
    print(res)


if __name__ == "__main__":
    class_example_LU_treshhold_2()