from LP.linear_programing_tools import linearPrograming
import numpy as np


def is_b_negative(b):
    for i in b:
        if i < 0:
            return True
    return False


def simplex_result(matrix_A, vector_b, vector_c):
    # if is_b_negative(vector_b):
    #     min_b = vector_b[0]
    #     for i in vector_b:
    #         if min_b > i:
    #             min_b = i
    #
    #     A = np.zeros((matrix_A.shape[0], matrix_A.shape[1]+1))
    #     x = -1 * np.ones(matrix_A.shape[0])
    #     A = np.hstack((x[:,np.newaxis], matrix_A))
    #     C = np.zeros(len(vector_c))
    #     C[0] = -1
    #     preprocess = linearPrograming(A, vector_b, C)
    #     d = np.copy(matrix_A[:, matrix_A.shape[1]+1]) # TODO: bug here
    #     preprocess.swap_entering_leaving(i, 0)
    #     preprocess.update_result(d, 0)
    #     res = preprocess.run_simplex()
    #     if res != 0:
    #         return "no solution"

    s = linearPrograming(matrix_A, vector_b, vector_c)
    result = s.run_simplex()
    if result != -1:
        return s.solution[result]
    elif result == -1:
        x_max = np.zeros(s.num_rows + s.num_cols)
        for i in range(s.num_rows):
            x_max[s.bases_vars[i] - 1] = s.xB[i]
        pad = np.zeros(s.num_rows)
        c_new = np.hstack((s.c, pad))
        return np.dot(c_new, x_max)
