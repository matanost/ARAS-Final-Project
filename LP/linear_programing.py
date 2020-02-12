import numpy as np


class linearPrograming:

    def __init__(self, matrix_A, vector_x, vector_b):
        self.A = matrix_A
        self.x = vector_x
        self.b = vector_b
        shape = self.A.shape()
        self.num_rows = shape[0]
        self.num_cols = shape[1]
        self.result = 0

    def find_basic_vars(self):
        num_of_one = 0
        flag = 0
        is_basic = np.zeros(self.num_cols)
        for j in range(self.num_cols):
            for i in range(self.num_rows):
                if self.A[i][j] == 1:
                    num_of_one += 1
                elif self.A[i][j] != 0:
                    flag = 1
                    break
            if num_of_one == 1 and flag == 0:
                is_basic[j] = 1
            flag = 0
        return is_basic


    def bland_selection_rule(self):
        for i in self.num_cols:
            if self.A[self.num_rows-1][i] > 0:
                return i
        return False

    def dantzig_selection_rule(self):
        max_in_row = -1
        for i in self.A[self.num_rows-1]:
            if i > max_in_row:
                max_in_row = i
        return i

    def is_optimal_solution(self):
        for i in self.A[self.num_rows - 1]:
            if i > 0:
                return False
        return True


    def pivote(self):


    def negative_b(self):




    def vector_norm(self):




