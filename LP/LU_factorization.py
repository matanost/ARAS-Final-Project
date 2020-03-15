import numpy as np
import scipy.linalg


class LU_factorization:

    def __init__(self, matrix_B):
        self.B = matrix_B
        self.eta_matrix= []
        self.leaving_vars = []
        self.L = []
        self.U = []
        shape = self.B.shape
        self.num_rows = shape[0]
        self.num_cols = shape[1]

    def run_LU_factorization(self):
        P, L, U = scipy.linalg.lu(self.B)
        self.lower_triangle_to_eta(L)
        self.upper_triangle_to_eta(U)
        # self.eta_matrix[0] = np.dot(P, self.eta_matrix[0])
        # p is unitary matrix then p^-1 = p^t
        return np.transpose(P), self.eta_matrix, self.leaving_vars

    def lower_triangle_to_eta(self, L):
        for j in range(self.num_cols):
            for i in range(self.num_rows-1, -1, -1):
                if L[i][j] != 0 and not (i == j and L[i][j] == 1):
                    eta = np.identity(self.num_rows)
                    self.leaving_vars.append(j)
                    eta[i][j] = np.copy(L[i][j])
                    self.eta_matrix.append(eta)

    def is_equal_vec(self, a, b):
        for i in range(len(a)):
            if a[i] != b[i]:
                return False
        return True

    def where_is_v(self, eta):
        for i in range(len(eta)):
            e = np.zeros((eta.shape[0], 1))
            e[i] = 1
            y = np.copy(eta[:,i])
            if not self.is_equal_vec(y, e):
                return i

    def upper_triangle_to_eta(self, U):
        U_T = np.transpose(U)
        for j in range(self.num_cols-1, -1,-1):
            for i in range(self.num_rows -1, -1,-1):
                if U_T[i][j] != 0 and not (i == j and U_T[i][j] == 1):
                    eta = np.identity(self.num_rows)
                    eta[i][j] = np.copy(U_T[i][j])
                    x = np.transpose(eta)
                    k = self.where_is_v(np.copy(x))
                    self.leaving_vars.append(k)
                    self.eta_matrix.append(x)
