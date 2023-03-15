
def compute_CLI(matrix):
    """
    Create the CLI list from matrix

    Args:
        matrix (List<List<Float>>): Adjacency matrix
    """
    C = []
    L = []
    I = []
    cpt = 0 # cpt of non zero values
    n = len(matrix)
    for i in range(n):
        L.append(cpt)
        for j in range(n):
            if matrix[i][j] != 0 : 
                C.append(matrix[i][j])
                I.append(j)
                cpt += 1
    L.append(cpt)
    return C, L, I


# Exemple

# M1 = [[0, 3, 5, 8], [1, 0, 2, 0], [0, 0, 0, 0], [0, 3, 0, 0]]
# M2 = [[1, 0, 0, 2], [0, 0, 3, 0], [0, 0, 0, 0], [4, 0, 0, 5]]

# C, L, I = compute_CLI(M1)
# print(C)
# print(L)
# print(I)
# print("\n ----------- \n")

# C, L, I = compute_CLI(M2)
# print(C)
# print(L)
# print(I)
# print("\n ----------- \n")