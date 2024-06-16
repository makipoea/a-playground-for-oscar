#from multiprocessing import Pool, Manager
from src.graph_analysis import generate_path_via_point_from_first_point, generate_grid
import multiprocessing as mp

import sys
import logging
import numpy as np
#import square_generation as oscar 
import matplotlib.pyplot as plt 
from tqdm import tqdm
import random 


def worker(graph, chemins, output_queue):
    local_longest_path = []
    l_new_chemin = []
    for chemin in chemins:
        dernier_point = chemin[-1]
        voisins_non_visites = [voisin for voisin in graph[dernier_point] if voisin not in chemin]
        if voisins_non_visites:
            for voisin in voisins_non_visites:
                l_new_chemin.append(chemin + [voisin])
        elif len(chemin) > len(local_longest_path):
            local_longest_path = chemin
    output_queue.put((l_new_chemin, local_longest_path))

def parcours_exhaustif(graph, first_point):
    """
    graph : dictionnaire d'adjacence
    first_point : Point
    """
    manager = mp.Manager()
    output_queue = manager.Queue()

    l_chemin_en_construction = [[first_point]]
    plus_long_chemin = []
    num_workers = mp.cpu_count()

    pbar = tqdm(total=len(list(graph.keys())), desc="progression")

    while l_chemin_en_construction:
        chunks = [l_chemin_en_construction[i::num_workers] for i in range(num_workers)]
        processes = []

        for chunk in chunks:
            p = mp.Process(target=worker, args=(graph, chunk, output_queue))
            processes.append(p)
            p.start()

        l_chemin_en_construction = []
        for _ in range(num_workers):
            new_chemins, local_longest_path = output_queue.get()
            l_chemin_en_construction.extend(new_chemins)
            if len(local_longest_path) > len(plus_long_chemin):
                plus_long_chemin = local_longest_path

        for p in processes:
            p.join()

        pbar.n = len(plus_long_chemin)
        pbar.refresh()

    pbar.close()
    return plus_long_chemin

if __name__ == "__main__":
    polygone = [(1,0),(0.71,0.71),(0,1),(-0.71, 0.71),(-1,0),(-0.71,-0.71),(0,-1),(0.71,-0.71)]
    
    resolution = 8

    l_point, graph, f = generate_grid(polygone, resolution)

    chemin = parcours_exhaustif(graph, list(graph.keys())[0])

    #chemin = max(l_chemin, key=len)

    print(chemin)


    plt.plot([point[0]for point in polygone+[polygone[0]]], [point[1]for point in polygone+[polygone[0]]]) # affiche le polygone

    plt.scatter([point[0]for point in l_point], [point[1]for point in l_point], s=1, color='blue')

        #plt.scatter([f(point)[0]for point in flag_to_visit], [f(point)[1]for point in flag_to_visit], s=10, color='red')

    if chemin != []:
        last_point = chemin[0]
        for point in chemin:
            p1 = f(last_point)
            p2 = f(point)
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], lw = 0.5 ,color="red")
            last_point = point

    plt.show()