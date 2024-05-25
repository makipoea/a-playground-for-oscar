from multiprocessing import Pool, Manager
from graph_analysis import generate_path_via_point_from_first_point, generate_grid


import sys
import logging
import numpy as np
import square_generation as oscar 
import matplotlib.pyplot as plt 
from tqdm import tqdm
import random 


def process_parcours(graph, flag_to_visit, sommet_de_depart, resultats_partages):
    r = generate_path_via_point_from_first_point(graph, flag_to_visit, sommet_de_depart) 
    
    resultats_partages.append(r)  # Ajoute True et le résultat du calcul à la liste partagée
    return r[0]

if __name__ == '__main__':
    # Créer une liste partagée pour stocker les résultats
    #graph = {1:[2, 4, 5], 2:[1, 4], 3:[7], 4:[1, 2, 6, 7], 5:[1, 6], 6:[4, 5], 7:[3, 4]}
    polygone = [(1,0),(0.71,0.71),(0,1),(-0.71, 0.71),(-1,0),(-0.71,-0.71),(0,-1),(0.71,-0.71)]
    
    resolution = 10
    pas = 3

    l_point, graph, f = generate_grid(polygone, resolution)

    for point in graph.keys():
        random.shuffle(graph[point])

    flag_to_visit = []

    for i in range(0, resolution, pas):
        for j in range(0, resolution, pas):
            if (i, j) in graph.keys(): 
                flag_to_visit.append((i, j))
    

    manager = Manager()
    resultats_partages = manager.list()

    # Créer un pool de processus
    with Pool(processes=4) as pool:  # Nombre de processus à utiliser
        # Lancer les calculs de manière asynchrone
        for sommet_de_depart in flag_to_visit:
            if process_parcours(graph, flag_to_visit, sommet_de_depart, resultats_partages):
                # Si un résultat positif est trouvé, terminer les autres processus
                pool.terminate()
                break

    # Trouver le premier résultat True
    for reussi, chemin in resultats_partages:
        if reussi:
            plt.plot([point[0]for point in polygone+[polygone[0]]], [point[1]for point in polygone+[polygone[0]]]) # affiche le polygone

            plt.scatter([point[0]for point in l_point], [point[1]for point in l_point], s=1, color='blue')

            plt.scatter([f(point)[0]for point in flag_to_visit], [f(point)[1]for point in flag_to_visit], s=10, color='red')

            if chemin != []:
                last_point = chemin[0]
                for point in chemin:
                    p1 = f(last_point)
                    p2 = f(point)
                    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], lw = 0.5 ,color="red")
                    last_point = point

            plt.show()
            break
    else:
        print("Aucun résultat True trouvé.")

 
