import numpy as np
from LP.LU_factorization import LU_factorization


class linear_Programing:

    TRESHOLD_ETA = 100

    def __init__(self, matrix_A, vector_b, vector_c):
        self.epsilon = 0.01
        self.solution = {-2: 'unbounded solution', -3: 'There is no solution', -1: 'optimal solution'}
        self.A = np.copy(matrix_A)
        self.b = np.copy(vector_b)
        self.c = np.copy(vector_c)

        shape = self.A.shape
        #also num of slack vars
        self.num_rows = shape[0]
        self.num_cols = shape[1]

        self.Base = np.identity(self.num_rows)
        self.non_bases_vars = np.arange(start=1, stop=self.num_cols+1)
        self.bases_vars = np.arange(start=self.num_cols+1,
                                        stop=self.num_cols+1+self.num_rows)
        self.AN = np.copy(matrix_A)
        self.cN = np.copy(vector_c)
        self.cB = np.zeros(self.num_rows)
        self.xB = np.copy(vector_b)

        self.eta_matrix = []
        self.leaving_vars = []

        self.p = []

    def swap_entering_leaving(self, entering_var, leaving_var):
        #update base and AN
        temp_B = np.copy(self.Base[:,leaving_var])
        self.Base[:,leaving_var] = self.AN[:,entering_var]
        self.AN[:,entering_var] = temp_B

        #update cB and cN
        temp_c = np.copy(self.cB[leaving_var])
        self.cB[leaving_var] = self.cN[entering_var]
        self.cN[entering_var] = temp_c

        #update bases vars and non_bases_vars
        entering_var_index = self.non_bases_vars[entering_var]
        leaving_var_index = self.bases_vars[leaving_var]
        self.bases_vars[leaving_var] = entering_var_index
        self.non_bases_vars[entering_var] = leaving_var_index


    def is_x1_in_the_Base(self):
        for i in range(len(self.Base)):
            if self.bases_vars[i] == 1:
                return i
        return -1

    def is_optimal_solution(self, coefficient):
        for i in coefficient:
            if i > 0:
                return False
        return True

    def is_unbounded_solution(self, t_vector):
        return not np.any(t_vector > 0)

    def picking_entering_var_dantzig(self, y):
        coefficient = self.cN - np.dot(y,self.AN)
        for i in range(len(coefficient)):
            if abs(coefficient[i]) < self.epsilon:
                coefficient[i] = 0
        if self.is_optimal_solution(coefficient):
            return -1
        return np.argmax(coefficient)

    def picking_entering_var_bland(self,y):
        coefficient = self.cN - np.dot(y, self.AN)
        for i in range(len(coefficient)):
            if abs(coefficient[i]) < self.epsilon:
                coefficient[i] = 0
        if self.is_optimal_solution(coefficient):
            return -1
        index = self.num_rows+self.num_cols+1
        index_at_vector = 0
        for i in range(len(coefficient)):
            if coefficient[i] > 0 and self.non_bases_vars[i] < index:
                index = self.non_bases_vars[i]
                index_at_vector = i
        return index_at_vector

    def picking_leaving_var(self, d):
        t_vector = np.zeros(d.shape)
        for i in range(len(d)):
            if d[i] != 0:
                t_vector[i] = self.xB[i] / d[i]
        if self.is_unbounded_solution(t_vector):
            return -2
        min = t_vector[0]
        min_index = 0
        for i in range(len(t_vector)):
            if (t_vector[i] > 0 and min >= t_vector[i]) or (t_vector[i] > 0 and min < 0) :
                min = t_vector[i]
                min_index = i
            index_x1 = self.is_x1_in_the_Base()
            if index_x1 > -1:
                if t_vector[index_x1] == min:
                    min_index = index_x1
        self.leaving_vars.append(min_index)
        return min_index

    def update_result(self, leaving_var, d):
        t_vector = np.zeros(d.shape)
        for i in range(len(d)):
            if d[i] != 0:
                t_vector[i] = self.xB[i] / d[i]
        t = t_vector[leaving_var]
        d_with_t = (np.ones(t_vector.shape[0])*t)*d
        self.xB = self.xB - d_with_t
        self.xB[leaving_var] = t

    def BTRAN(self):
        known_result = self.cB
        for i in range(len(self.leaving_vars)-1, -1, -1):
            known_result = self.single_BTRAN(known_result, i)
        if len(self.p) != 0:
            return np.dot(known_result, self.p)
        return known_result

    def single_BTRAN(self, known_result, i):
        y = np.zeros(self.num_rows)
        eta_vector_index = self.leaving_vars[i]
        eta_vector = self.eta_matrix[i][:, eta_vector_index]
        factor = 0
        if abs(eta_vector[eta_vector_index]) > self.epsilon:
            factor = 1 / eta_vector[eta_vector_index]
        for j in range(self.num_rows):
            if j != eta_vector_index:
                y[j] = known_result[j]
            else:
                y[eta_vector_index] = factor * known_result[eta_vector_index]
                for k in range(self.num_rows):
                    if k != eta_vector_index:
                        y[eta_vector_index] -= factor*eta_vector[k]*known_result[k]
        return y

    def FTRAN(self, known_result):
        if len(self.p) != 0:
            known_result = np.dot(self.p, known_result)
        for i in range(0, len(self.leaving_vars)):
            known_result = self.single_FTRAN(known_result, i)
        return known_result

    def single_FTRAN(self, known_result, i):
        d = np.zeros(self.num_rows)
        eta_vector_index = self.leaving_vars[i]
        eta_vector = self.eta_matrix[i][:,eta_vector_index]
        factor = 0
        if abs(eta_vector[eta_vector_index]) > self.epsilon:
            factor = (1 / eta_vector[eta_vector_index])
        d[eta_vector_index] = factor * known_result[eta_vector_index]
        for j in range(self.num_rows):
            if j != eta_vector_index:
                d[j] = known_result[j]-eta_vector[j]*d[eta_vector_index]
        return d

    def clac_optimal_sol(self):
        x_max = self.assign()
        c_new = np.zeros(self.num_rows + self.num_cols)
        for i in range(len(self.cB)):
            c_new[self.bases_vars[i]-1] = self.cB[i]
        for i in range(len(self.cN)):
            c_new[self.non_bases_vars[i]-1] = self.cN[i]
        return np.dot(c_new, x_max)

    def assign(self):
        x_max = np.zeros(self.num_rows + self.num_cols)
        for i in range(self.num_rows):
            x_max[self.bases_vars[i] - 1] = self.xB[i]
        return x_max

    def simplex(self):
        result = self.run_simplex()
        if result != -1:
            if result == -2 and self.is_zero_sulotion():
                return 0
            return self.solution[result]
        elif result == -1:
            return self.clac_optimal_sol()

    def eta(self, d):
        eta = np.identity(self.num_rows)
        eta[:, self.leaving_vars[len(self.leaving_vars) - 1]] = np.copy(d)
        self.eta_matrix.append(np.copy(eta))


    def is_zero_sulotion(self):

        x = np.zeros(self.c.shape)
        for i in range(len(self.c)):
            if self.c[i] != 0:
                x[i] = 1
        y = []
        for i in range(len(x)):
            if len(self.b) > i:
                y.append(x[i]*self.b[i])
            if len(self.b)-1 < i:
                return False
        for j in range(len(x)):
            if x[j] != 0:
                if len(self.b) > j:
                    if 0 <= y[i]:
                        continue
                    else:
                        return False
                else:
                    return False
        return True

    def run_simplex(self):
        #first iteration is different because B=I and cB = 0
        # we don't need FTRAN and BTRAN then
        # y*Base = cB -> y = 0
        y = np.zeros(self.num_rows)
        entering_var = self.picking_entering_var_bland(y)
        if entering_var < 0:
            return entering_var
        # Base*d = a = self.AN[:entering_var] - > d = a
        d = np.copy(self.AN[:,entering_var])
        leaving_var = self.picking_leaving_var(d)
        if leaving_var < 0:
            return leaving_var
        self.eta(d)
        self.swap_entering_leaving(entering_var, leaving_var)
        self.update_result(leaving_var, d)
        return self.simplex_iteration()

    def simplex_iteration(self):
        while True:
            y = self.BTRAN()
            entering_var = self.picking_entering_var_bland(y)
            if entering_var < 0:
                return entering_var
            a = np.copy(self.AN[:, entering_var])
            d = self.FTRAN(a)
            leaving_var = self.picking_leaving_var(d)
            if leaving_var < 0:
                return leaving_var
            self.eta(d)
            self.swap_entering_leaving(entering_var, leaving_var)
            self.update_result(leaving_var, d)
            if (len(self.eta_matrix) >= self.TRESHOLD_ETA and len(self.p) == 0):
                s = LU_factorization(self.Base)
                self.p, self.eta_matrix, self.leaving_vars = s.run_LU_factorization()