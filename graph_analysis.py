# Ce fichier contient l'espoire futile de reeimpleementer networkx (mais en pire) avec pour seul avantage qu'on y comprenne queque chose
import os
import logging
import numpy as np
import square_generation as oscar 

graph = {1:[2, 5], 2:[1, 4], 3:[7], 4:[1, 2, 6, 7], 5:[1, 6], 6:[4, 5], 7:[3, 4], 8:[]}

def backtrack(g, ham_path, l_deja_vu, l_first_sommet_tried):
    """
    implementation pour un dictionnaire d'adjacence d'une recherche d'un chemin hamiltonien
    ACHTUNG ACHTUNG les liste de voisins doivent trier^tm 
    """
    #print(ham_path, l_deja_vu)
    if len(ham_path) >= len(g.keys()): 
        return True, ham_path

    if ham_path == []:
        l_sommet = sorted(list(g.keys()))
        for sommet in l_sommet:
            if sommet not in l_first_sommet_tried:
                return backtrack(g, [sommet], [], l_first_sommet_tried)

        return False, []

    for voisin in g[ham_path[-1]]:
        if voisin not in ham_path and (l_deja_vu == [] or voisin > l_deja_vu[-1]): # //////!!!!!!\\\\\\\\ les listes de voisisn sont supposer trier (on fait ce qu'on peut)
            ham_path += [voisin]
            return backtrack(g, ham_path, [], l_first_sommet_tried)
    
    s = ham_path.pop()
    if ham_path == []:
        l_first_sommet_tried += [s]
        return backtrack(g, ham_path, [], l_first_sommet_tried)
    else : 
        return backtrack(g, ham_path, [s], l_first_sommet_tried)


def is_in_polygone(point_to_compare, polygone):
    """
    take a polygone as a list of point and a point (cartesian coordinates) return boolen
    /////! !!!! ! ! ! ! ! ! ! \ Cette focntion ne marche pas 
    """
    is_inside = 0
    if polygone == []:
        logging.info("is_in_polygone a receive an empty polygone just sayin")
        return False

    last_point = polygone[-1]
    
    for point in polygone[1::]+last_point: # cheker si les point sont pas sur un sommet
        if min(last_point[1], point[1]) <= point_to_compare[1] < max(last_point[1], point[1]): # <= .. < evite theoriquement les cas ou in tombe sur un point
            if last_point[0] < point[0]:
                if point_to_compare[1]*(point[0]-last_point[0]) < (point[1]-last_point[1])*(point_to_compare[0] - last_point[0]) + point_to_compare:
                    is_inside = 1 - is_inside
            elif point_to_compare[1]*(point[0]-last_point[0]) < (point[1]-last_point[1])*(point_to_compare[0] - last_point[0]) + point_to_compare:
                is_inside = 1 - is_inside

    if is_inside in [0 , 1]: return is_inside
    else : raise TypeErrorError("la fonction is_in_polygone a lamentablement echouer ")


def generate_grid(polygone, nb_point):
    """
    retourne une liste de point mais aussi (et surtout) un graph correspondant a une dictionnaire d'adjacence
    """
    carre = oscar.square(polygone)

print(len(graph.keys()))
print(backtrack(graph, [], [], []))     