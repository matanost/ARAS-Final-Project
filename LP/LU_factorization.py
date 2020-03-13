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
        return np.dot(scipy.transpose(P), self.B), self.eta_matrix, self.leaving_vars

    def lower_triangle_to_eta(self, L):
        for j in range(self.num_cols):
            for i in range(self.num_rows-1, -1, -1):
                if L[i][j] != 0 and not (i == j and L[i][j] == 1):
                    eta = np.identity(self.num_rows)
                    self.leaving_vars.append(j)
                    eta[i][j] = np.copy(L[i][j])
                    self.eta_matrix.append(eta)

    def upper_triangle_to_eta(self, U):
        U_T = np.transpose(U)
        for j in range(self.num_cols-1, -1,-1):
            for i in range(self.num_rows -1, -1,-1):
                if U_T[i][j] != 0 and not (i == j and U_T[i][j] == 1):
                    eta = np.identity(self.num_rows)
                    self.leaving_vars.append(j)
                    eta[i][j] = np.copy(U_T[i][j])
                    self.eta_matrix.append(np.transpose(eta))
