class Matrix:
    def __init__(self, matrix):
        """
        Create the CLI list from matrix

        Args:
            matrix (List<List<Float>>): Adjacency matrix
        """
        self.C = []
        self.L = []
        self.I = []
        cpt = 0 # cpt of non zero values
        n = len(matrix)
        for i in range(n):
            self.L.append(cpt)
            for j in range(n):
                if matrix[i][j] != 0 : 
                    self.C.append(matrix[i][j])
                    self.I.append(j)
                    cpt += 1
        self.L.append(cpt)


# Exemple

# M1 = [[0, 3, 5, 8], [1, 0, 2, 0], [0, 0, 0, 0], [0, 3, 0, 0]]
# M2 = [[1, 0, 0, 2], [0, 0, 3, 0], [0, 0, 0, 0], [4, 0, 0, 5]]

# m1= Matrix(M1)
# print(m1.C)
# print(m1.L)
# print(m1.I)
# print("\n ----------- \n")

# m2 = Matrix(M2)
# print(m2.C)
# print(m2.L)
# print(m2.I)