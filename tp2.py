import numpy as np
import matrix as ut
# calculer C L I
#exercice 1 tp2
# epsilon = 1/7
def compute_pi(epsilon, C, L, I, V):
    n = len(L)-1
    P = np.zeros(n)
    somme = 0
    for i in range(0, n):
        for j in range(L[i], L[i+1]):
            P[I[j]] += C[j] * V[i] # ou bien remplacer C[j] par 1/ L[i+1] - L[i]
        if L[i] == L[i+1]:
            somme += V[i]/n
    for k in range(0, n) : 
        P[k] += somme
        P[k] = (1 - epsilon) * P[k] + epsilon/n
    return P


def ex3q1(C,L,I,V,k): # k = 200 puis essayer d'autres valeurs
    epsilon = 1/7
    for _ in range(k):
        V = compute_pi(epsilon, C, L, I, V)
    print(sum(V))
    return V

M1 = [[0, 1/2, 0, 1/2],[0, 0, 1, 0], [1/4, 1/4, 1/4, 1/4], [1/3, 1/3, 1/3, 0]]

C, L, I = ut.compute_CLI(M1)

n = len(L)-1
print(n)
V = np.full(n, 1/n)
print(V)
print(ex3q1(C,L,I,V, 200))

