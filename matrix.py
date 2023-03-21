import pickle

class CLI_Matrix():
    def __init__(self, param, fromFile=True):
        """
        Create CLI matrix from file.

        Args:
            param (string or List<List<Float>>): either path to file or matrix to convert to CLI
            fromFile (boolean): True if creating matrix from file, else from matrix
        """
        if fromFile:
            self.C = []
            self.L = [0] # initialized with 0 since the first row of the matrix start at index 0 of self.C
            self.I = []
            with open(param, 'r') as file:
                for line_nb, line in enumerate(file, 1):
                    if line_nb % 5 == 4:
                        # retrieve links (page id)
                        links = line.split()
                        links = [int(id)-1 for id in links] # minus 1 since page id starts at 1

                        # Update C matrix (value)
                        nb_links = len(links)
                        C_bis = [1/nb_links] * nb_links
                        self.C.extend(C_bis)

                        # Update L matrix (row)
                        self.L.append(len(self.C)) # an entire row of the matrix has been processed, so the next value is in a new row

                        # Update I matrix (col)
                        # sorted_links = sorted(links)
                        self.I.extend(sorted(links))
            with open('data/CLI_Matrix.pickle', 'wb') as f:
                # Pickle the 'data' dictionary using the highest protocol available.
                pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        else:
            self.C = []
            self.L = []
            self.I = []
            cpt = 0 # cpt of non zero values
            n = len(param)
            for i in range(n):
                self.L.append(cpt)
                for j in range(n):
                    if param[i][j] != 0 : 
                        self.C.append(param[i][j])
                        self.I.append(j)
                        cpt += 1
            self.L.append(cpt)



# Exemple

# M1 = [[0, 3, 5, 8], [1, 0, 2, 0], [0, 0, 0, 0], [0, 3, 0, 0]]
# M2 = [[1, 0, 0, 2], [0, 0, 3, 0], [0, 0, 0, 0], [4, 0, 0, 5]]

# mat = CLI_Matrix(M1, False)
# print(mat.C)
# print(mat.L)
# print(mat.I)
# print("\n ----------- \n")

# mat = CLI_Matrix(M2, False)
# print(mat.C)
# print(mat.L)
# print(mat.I)
# print("\n ----------- \n")

# mat = CLI_Matrix("data/test.txt")
# print(mat.C)
# print(mat.L)
# print(mat.I)
# print("\n ----------- \n")