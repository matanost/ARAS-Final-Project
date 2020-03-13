from LP.linear_programing_tools import linearPrograming
import numpy as np


def is_b_negative(b):
    for i in b:
        if i < 0:
            return True
    return False



def simplex_result(matrix_A, vector_b, vector_c):
    if not is_b_negative(vector_b):
        s = linearPrograming(matrix_A, vector_b, vector_c)
        return s.simplex()
    else:

        min_b = vector_b[0]
        min_b_index = 0
        for i in range(len(vector_b)):
            if min_b > vector_b[i]:
                min_b = vector_b[i]
                min_b_index = i
        leaving_var = min_b_index
        leaving_var_index = min_b_index + matrix_A.shape[0]
        # A = np.zeros((matrix_A.shape[0], matrix_A.shape[1] + 1))
        x = -1 * np.ones(matrix_A.shape[0])
        A = np.copy(np.hstack((x[:, np.newaxis], matrix_A)))
        C = np.zeros(len(vector_c) + 1)
        C[0] = -1
        preprocess = linearPrograming(A, vector_b, C)
        d = np.copy(x)
        preprocess.swap_entering_leaving(0, leaving_var)
        preprocess.update_result(leaving_var, d)
        res = preprocess.simplex_iteration(d,leaving_var)
        if res != -1:
            return preprocess.solution[-3]
        elif res == -1:
            # index_vec = np.hstack((preprocess.non_bases_vars, preprocess.bases_vars))
            # x_0_index = 0
            # for i in range(len(index_vec)):
            #     if index_vec[i] == 1:
            #         x_0_index = i
            x_max = preprocess.assign()
            if x_max[0] != 0:
                return preprocess.solution[-3]
        s = linearPrograming(matrix_A, vector_b, vector_c)
        if preprocess == preprocess.solution[-3]:
            return preprocess.solution[-3]
        for i in range(len(preprocess.bases_vars)):
            if preprocess.bases_vars[i] >= 1 and preprocess.bases_vars[i] <= s.num_cols:
                s.swap_entering_leaving(preprocess.bases_vars[i]-2,
                                        preprocess.non_bases_vars[preprocess.bases_vars[i]-2] - preprocess.num_cols-2)
        x = s.simplex()
        return x