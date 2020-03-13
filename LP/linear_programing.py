from LP.linear_programing_tools import linearPrograming
import numpy as np


def is_b_negative(b):
    for i in b:
        if i < 0:
            return True
    return False


def simplex_result(matrix_A, vector_b, vector_c):
    if is_b_negative(vector_b):
        min_b = vector_b[0]
        min_b_index = 0
        for i in range(len(vector_b)):
            if min_b > vector_b[i]:
                min_b = vector_b[i]
                min_b_index = i
        leaving_var = matrix_A.shape[0] + min_b_index
        A = np.zeros((matrix_A.shape[0], matrix_A.shape[1]+1))
        x = -1 * np.ones(matrix_A.shape[0])
        A = np.hstack((x[:,np.newaxis], matrix_A))
        C = np.zeros(len(vector_c)+1)
        C[0] = -1
        preprocess = linearPrograming(A, vector_b, C)
        d = np.copy(x)
        preprocess.swap_entering_leaving(0, leaving_var)
        preprocess.update_result(d, leaving_var)
        res = preprocess.run_simplex()
        if res != 0:
            return "no solution"

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
