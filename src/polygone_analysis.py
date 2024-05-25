import sys
import logging
import numpy as np
import matplotlib.pyplot as plt 
from tqdm import tqdm
import random 

from src.square_generation import square  # temporary

def is_in_polygone(point_to_compare, polygone):
    """
    take a polygone as a list of point and a point (cartesian coordinates) return boolen
    utilise la methode de raycasting avec une ligne horizontale
    # Cette fonction est EXTREMENT LENTE a utiliser avec parsismonie voir mieux a optimiser
    """
    is_inside = 0
    if polygone == []:
        logging.info("is_in_polygone a receive an empty polygone just sayin")
        return False

    last_point = polygone[0]
    for point in polygone[1::]+[last_point]:
        if min(point[1], last_point[1])<=point_to_compare[1] < max(point[1], last_point[1]): # il y a intersection <= ... < pemret de prendre le cas ou le projeter tombe sur un point(compter une seul fois oula je crois que je depasse les 80 characteres) 
            p = (point_to_compare[1] - last_point[1]) * (point[0] - last_point[0])
            if point[1] >= last_point[1] and ((point_to_compare[0]-last_point[0])*(point[1]-last_point[1]) <= p): #verifie si le point est avant l'intersection
                is_inside = 1-is_inside

            elif (point[1] < last_point[1]) and (point_to_compare[0]-last_point[0])*(point[1]-last_point[1]) >= p:
                is_inside = 1-is_inside
        last_point = point

    if is_inside in [0 , 1]: return is_inside
    else : raise TypeErrorError("la fonction is_in_polygone a lamentablement echouer ")


def generate_grid(polygone, nb_point):
    """
    point_to_compare : Point
    polygone : List Point
    ->
    l_point : List Point (cartesian coordonate)
    graph : Dictionnaire d'adjacence : cle coordonne entiere dans la grille
    func : Point(int*int) -> Point(float*float) : coordonne cartessiennes d'un point
    """
    graph = {}
    l_point = []
    carre = square(polygone)
    eps = (carre[1][0] - carre[0][0])/nb_point
    for i in tqdm(range(nb_point), desc="generation de la grille"):
        for j in range(nb_point):
            if is_in_polygone([carre[0][0]+i*eps, carre[0][1]+j*eps], polygone):
                #print("valide")
                l_point.append([carre[0][0]+i*eps, carre[0][1]+j*eps])
                graph[(i, j)] = [(i+1, j), (i-1, j),(i, j+1), (i, j-1)]
   
    for point in list(graph.keys()):
        graph[point] = [voisin for voisin in graph[point] if voisin in graph]

    return l_point, graph, lambda point:[carre[0][0]+point[0]*eps, carre[0][1]+point[1]*eps]