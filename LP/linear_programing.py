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

        x = -1 * np.ones(matrix_A.shape[0])
        A = np.copy(np.hstack((x[:, np.newaxis], matrix_A)))
        C = np.zeros(len(vector_c) + 1)
        C[0] = -1
        preprocess = linearPrograming(A, vector_b, C)
        d = np.copy(x)
        preprocess.leaving_vars.append(leaving_var)
        eta = np.identity(preprocess.num_rows)
        eta[:, preprocess.leaving_vars[len(preprocess.leaving_vars) - 1]] = np.copy(d)
        preprocess.eta_matrix.append(np.copy(eta))
        preprocess.swap_entering_leaving(0, leaving_var)
        preprocess.update_result(leaving_var, d)
        res = preprocess.simplex_iteration()
        if res != -1:
            return preprocess.solution[res]
        elif res == -1:
            x_max = preprocess.assign()
            if x_max[0] != 0:
                return preprocess.solution[-3]
        s = linearPrograming(matrix_A, vector_b, vector_c)

        entering_vars = []
        for i in range(len(preprocess.bases_vars)):
            if preprocess.bases_vars[i] >= 1 and preprocess.bases_vars[i] <= s.num_cols:
                entering_vars.append([i, preprocess.bases_vars[i]-2])
        leaving_vars = []
        for i in range(len(preprocess.non_bases_vars)):
            if preprocess.non_bases_vars[i]-1 > s.num_cols:
                leaving_vars.append((i, preprocess.non_bases_vars[i]-2))
        for i in range(len(entering_vars)):
            d = np.copy(s.AN[:, entering_vars[i][1]])
            s.leaving_vars.append(leaving_vars[i][1]-s.num_cols)
            eta = np.identity(s.num_rows)
            eta[:, s.leaving_vars[len(s.leaving_vars) - 1]] = np.copy(d)
            s.eta_matrix.append(np.copy(eta))
            s.swap_entering_leaving(entering_vars[i][1],leaving_vars[i][1]-s.num_cols)

        for i in range(len(s.bases_vars)):
            s.xB[i] = x_max[s.bases_vars[i]]

        res = s.simplex_iteration()
        if res != -1:
            return preprocess.solution[res]
        elif res == -1:
            x_max = preprocess.assign()
            if x_max[0] != 0:
                return preprocess.solution[-3]
        return x