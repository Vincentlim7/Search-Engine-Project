import pickle
import numpy as np

class Link_CLI():
    def __init__(self, param, fromFile=True):
        """
        Create link CLI matrix from file.

        Args:
            param (string or List<List<Float>>): either path to file or matrix to convert to CLI
            fromFile (boolean): True if creating matrix from file, else from matrix
        """
        if fromFile: # compute CLI from file
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
                        links = [int(id) for id in links]

                        nb_links = len(links)

                        if nb_links != 0: # if page has links
                            # Update C matrix (value)
                            C_bis = [1/nb_links] * nb_links
                            self.C.extend(C_bis)

                            # Update I matrix (col)
                            self.I.extend(sorted(links))

                        # Update L matrix (row)
                        self.L.append(len(self.C)) # an entire row of the matrix has been processed, so the next value is in a new row
            print("Computing pagerank")
            self.pagerank(1/7, 200)

            with open('data/link_CLI.pickle', 'wb') as f:
                # Pickle the 'data' dictionary using the highest protocol available.
                pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
            
        else: # compute CLI from matrix
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

    def compute_pi(self, epsilon, v):
        """
        Multiplication between v and CLI matrix (one iteration of pagerank)

        Args:
            epsilon (float): epsilon value
            v (List<float>): vector

        Returns:
            List<float>: vector
        """
        n = len(self.L)-1
        P = np.zeros(n)
        somme = 0
        for i in range(0, n):
            for j in range(self.L[i], self.L[i+1]):
                P[self.I[j]] += self.C[j] * v[i] # ou bien remplacer C[j] par 1/ L[i+1] - L[i]
            if self.L[i] == self.L[i+1]:
                somme += v[i]/n
        for k in range(0, n): 
            P[k] += somme
            P[k] = (1 - epsilon) * P[k] + epsilon/n
        return P


    def pagerank(self, epsilon, k):
        """
        Compute pagerank according to algorithm defined in Exercice 3 of TP2

        Args:
            epsilon (float): damping factor
            k (int): number of iterations
        """
        n = len(self.L)-1
        v = np.full(n, 1/n)
        for _ in range(k):
            v = self.compute_pi(epsilon, v)
        print(sum(v))
        self.v = v
        with open(f'data/pagerank{k}.pickle', 'wb') as f:
            pickle.dump(v, f, pickle.HIGHEST_PROTOCOL)
    
    def pagerank_compute_best_iterations(self, tol=0.001, err=1e-6, max_iter=1000):
        """
        Compute the appropriate number of iterations for pagerank according to a tolerance and error thresholds

        Args:
            tol (float, optional): tolerance threshold. Defaults to 0.001.
            err (_type_, optional): error threshold. Defaults to 1e-6.
            max_iter (int, optional): maximum number of iterations. Defaults to 1000.

        Returns:
            iter: number of iterations
        """
        epsilon = 1/7
        n = len(self.L)-1
        v = np.full(n, 1/n)

        iter = 0
        err_prev = 0
        while iter < max_iter:
            if iter % 50 == 0:
                print(f"{iter} itérations")
                print(f"sum v : {sum(v)}")
                with open(f'data/pagerank{iter}.pickle', 'wb') as f:
                    pickle.dump(v, f, pickle.HIGHEST_PROTOCOL)
            v_next = self.compute_pi(epsilon, v)
            err = np.linalg.norm(v_next - v, 1)
            if err_prev and abs(err - err_prev) < tol:
                break
            v = v_next
            iter += 1
            err_prev = err
        self.v = v
        with open('data/pagerank.pickle', 'wb') as f:
            pickle.dump(v, f, pickle.HIGHEST_PROTOCOL)
        return iter
    
    def pagerank_compute_best_params(self, tol=0.001, err=1e-6, max_iter=1000):
        """
        Compute the appropriate number of iterations and epsilon for pagerank according to a tolerance and error thresholds

        Args:
            tol (float, optional): tolerance threshold. Defaults to 0.001.
            err (type, optional): error threshold. Defaults to 1e-6.
            max_iter (int, optional): maximum number of iterations. Defaults to 1000.

        Returns:
            iter: number of iterations
            epsilon: best epsilon value
        """
        n = len(self.L) - 1
        v = np.full(n, 1 / n)

        epsilon_list = [0.1, 1/7, 0.2, 0.8, 0.85, 0.9]
        best_epsilon = None
        best_iter = None
        best_err = float('inf')

        for epsilon in epsilon_list:
            v_new = v.copy()
            iter = 0
            err_prev = 0
            while iter < max_iter:
                if iter % 50 == 0:
                    print(f"{iter} itérations")
                    print(f"sum v : {sum(v_new)}")
                    with open(f"data/pagerank_e{epsilon}_i{iter}.pickle", 'wb') as f:
                        pickle.dump(v_new, f, pickle.HIGHEST_PROTOCOL)
                v_prev = v_new.copy()
                v_new = self.compute_pi(epsilon, v_prev)
                err = np.linalg.norm(v_new - v_prev, 1)
                if err_prev and abs(err - err_prev) < tol:
                    break
                iter += 1
                err_prev = err
            if err < best_err:
                best_epsilon = epsilon
                best_iter = iter
                best_err = err

        self.v = v_new
        with open(f"data/pagerank_e{best_epsilon}_i{best_iter}.pickle", 'wb') as f:
            pickle.dump(v_new, f, pickle.HIGHEST_PROTOCOL)

        return best_iter, best_epsilon