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
                    if line_nb % 97583 == 0:
                            print(f"{(line_nb / 975385) * 100} % (CLI)")
                    if line_nb % 5 == 4:
                        # retrieve links (page id)
                        links = line.split()
                        links = [int(id)-1 for id in links] # minus 1 since page id starts at 1

                        nb_links = len(links)

                        if nb_links != 0: # if page has links
                            # Update C matrix (value)
                            C_bis = [1/nb_links] * nb_links
                            self.C.extend(C_bis)

                            # Update I matrix (col)
                            self.I.extend(sorted(links))

                        # Update L matrix (row)
                        self.L.append(len(self.C)) # an entire row of the matrix has been processed, so the next value is in a new row
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




# Create CLI Matrix on page corpus

# mat = CLI_Matrix("data/wikiprocess.txt")
# print(f"len of C : {len(mat.C)}") # 6 159 228
# print(f"len of L : {len(mat.L)}") # 195 078
# print(f"len of I : {len(mat.I)}") # 6 159 228