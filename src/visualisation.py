import matplotlib.pyplot as plt 
import numpy as np
import random as rd


def F(X):
    return np.array([[0.5, 1], [1, 0.5]]) @ X + np.array([[-3/2], [0]])

def affine(X, A):
    """
    X : invariant point
    A : coeff directeur 
    """
    T = X - A @ X
    return lambda K : np.array(A @ K + T)[0]  

def plot_orbite(f, nb_rd, min_rd, max_rd, nb_orbite,X=None, c=False, l=1):
    """
    affiche l'orbite du point x par la fonction X 
   
    """
    if X == None:
        for i in range(nb_rd):
            for j in range(nb_rd):
                X = np.array([[min_rd+(max_rd-min_rd)*i/nb_rd], [min_rd+(max_rd-min_rd)*j/nb_rd]])
                orbite = [X]
                for _ in range(1, nb_orbite):
                    orbite.append(f(orbite[-1]))
                colors = [(i/nb_rd, j/nb_rd, k/nb_orbite) for k in range(nb_orbite)]
                plt.scatter([point[0] for point in orbite], [point[1] for point in orbite], marker='o', s=0.1, c=colors)
        plt.show()
    else: 
        orbite = [X]
        for i in range(1, nb_orbiteœ):
            orbite.append(f(orbite[-1]))
            plt.text(orbite[-1][0], orbite[-1][1], str(i), fontsize=7)

        plt.scatter([point[0] for point in orbite], [point[1] for point in orbite], marker='x', linewidths=0.1)
        
        plt.xlabel(" X ")
        
        plt.ylabel(" Y")
        plt.show()

if __name__ == "__main__":
    f = affine(np.array([[[1], [2]]]), np.array([[0.5, 0.2], [0.1, 0.3]]))
    #print(f(np.array([[1], [3]])))
    #plot_orbite(f , np.array([[1], [3]]), 100)
    plot_orbite(f, 100, 0, 10, 10)