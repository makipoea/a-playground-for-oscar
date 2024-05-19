# Ce fichier contient l'espoire futile de reeimpleementer networkx (mais en pire) avec pour seul avantage qu'on y comprenne queque chose
import os
import logging
import numpy as np
import square_generation as oscar 
import matplotlib.pyplot as plt 


def backtrack(g, ham_path, l_deja_vu, l_first_sommet_tried):
    """
    implementation pour un dictionnaire d'adjacence d'une recherche d'un chemin hamiltonien
    ACHTUNG ACHTUNG les liste de voisins doivent etre trier^tm 
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
    retourne une liste de point mais aussi (et surtout) un graph correspondant a une dictionnaire d'adjacence
    """
    l_point = []
    carre = oscar.square(polygone)
    #print(carre)
    eps = (carre[1][0] - carre[0][0])/nb_point
    for i in range(nb_point):
        for j in range(nb_point):
            if is_in_polygone([carre[0][0]+i*eps, carre[0][1]+j*eps], polygone):
                #print("valide")
                l_point.append([carre[0][0]+i*eps, carre[0][1]+j*eps])
    return l_point

if __name__ == "__main__":

    polygone = [(1,0),(0.71,0.71),(0,1),(-0.71, 0.71),(-1,0),(-0.71,-0.71),(0,-1),(0.71,-0.71)]

    point = [0.6, 0.9]

    b = is_in_polygone(point, polygone)

    #print(f'resultat = {b}')
    
    plt.plot([point[0]for point in polygone], [point[1]for point in polygone])
    
    l_grille = generate_grid(polygone, 1000)
    #print(l_grille)
    plt.scatter([point[0]for point in l_grille], [point[1]for point in l_grille], s=1)

    print(len(l_grille))

    plt.show()
    
    #graph = {1:[2, 5], 2:[1, 4], 3:[7], 4:[1, 2, 6, 7], 5:[1, 6], 6:[4, 5], 7:[3, 4], 8:[]}
    #print(backtrack(graph, [], [], []))     