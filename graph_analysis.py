# Ce fichier contient l'espoire futile de reeimpleementer networkx (mais en pire) avec pour seul avantage qu'on y comprenne queque chose
import sys
import logging
import numpy as np
import square_generation as oscar 
import matplotlib.pyplot as plt 
from tqdm import tqdm
import random 

sys.setrecursionlimit(100000000)

def tabu_search(graph, max_iterations):
    def get_neighbors(node):
        return graph[node]

    def is_hamiltonian_path(path):
        return len(path) == len(graph) and len(set(path)) == len(graph)

    def initialize_search():
        start_node = random.choice(list(graph.keys()))
        current_node = start_node
        path = [current_node]
        visited = {current_node}
        return start_node, current_node, path, visited

    best_path = None

    for start_iteration in tqdm(range(max_iterations), desc="Tabu Search Progress"):
        start_node, current_node, path, visited = initialize_search()
        tabu_list = []
        tabu_size = len(graph) // 2 

        for _ in range(max_iterations):
            if is_hamiltonian_path(path):
                return True, path

            neighbors = get_neighbors(current_node)
            unvisited_neighbors = [n for n in neighbors if n not in visited and n not in tabu_list]

            if unvisited_neighbors:
                next_node = random.choice(unvisited_neighbors)
            else:
                non_tabu_neighbors = [n for n in neighbors if n not in tabu_list]
                if non_tabu_neighbors:
                    next_node = random.choice(non_tabu_neighbors)
                else:
                    break

            if next_node not in visited:
                path.append(next_node)
                visited.add(next_node)
                current_node = next_node

                
                if len(tabu_list) >= tabu_size:
                    tabu_list.pop(0)
                tabu_list.append(next_node)
            else:
              
                start_node, current_node, path, visited = initialize_search()
                tabu_list = []

        if best_path is None or len(path) > len(best_path):
            best_path = path

    return best_path is not None and is_hamiltonian_path(best_path), best_path or []

def backtrack_rec(g, debug=1):
    """
    implementation pour un dictionnaire d'adjacence d'une recherche d'un chemin hamiltonien
    ACHTUNG ACHTUNG les liste de voisins doivent etre ordonner
    A optimiser avec du multithreading
    """
    #print(ham_path, l_deja_vu)
    def auxi(ham_path, l_deja_vu, l_first_sommet_tried):
        if debug:
            progression_bar.n = len(ham_path)
            progression_bar.refresh()
        if len(ham_path) >= len(g.keys()): 
            return True, ham_path

        if ham_path == []:
    
            l_sommet = sorted(list(g.keys()))
            for sommet in l_sommet:
                if sommet not in l_first_sommet_tried:
                    #l_first_sommet_tried += [sommet]
                    return auxi([sommet], [], l_first_sommet_tried)

            return False, []

        new_sommet = False

        for voisin in g[ham_path[-1]]:
            if voisin not in ham_path and (l_deja_vu == [] or new_sommet): # //////!!!!!!\\\\\\\\ les listes de voisisn sont ordonné et on les parcours dans l'ordre
                ham_path += [voisin]
                return auxi(ham_path, [], l_first_sommet_tried)
            if l_deja_vu!=[] and voisin == l_deja_vu[-1]:
                new_sommet = True

        s = ham_path.pop()
        if ham_path == []:
            l_first_sommet_tried += [s]
            return auxi(ham_path, [], l_first_sommet_tried)
        else : 
            return auxi(ham_path, [s], l_first_sommet_tried)
    
    if debug: # soyons claire c'est juste pour le style et quelle bonheure de pouvoire faire reculer uen barre de progression 
        progression_bar = tqdm(total=len(list(g.keys())), desc='lenght of ham path')
    
    return auxi([], [], [])

def backtrack_iter(g, debug=1):

    ham_path = []
    visited = []
    first_sommet_tried = []

 
    if debug:
        progression_bar = tqdm(total=len(g), desc='Longueur du chemin hamiltonien')

    l_sommet = sorted(list(g.keys()))

    while len(first_sommet_tried) != len(l_sommet):

        if debug:
            progression_bar.n = len(ham_path)
            progression_bar.refresh()

       
        if len(ham_path) == len(l_sommet):
            return True, ham_path

        if ham_path == []:
            for sommet in l_sommet:
                if sommet not in first_sommet_tried:
                    ham_path = [sommet]
                    first_sommet_tried.append(sommet)
                    print(first_sommet_tried)
                    visited = []
                    break
        else:
            sommet = ham_path[-1]
            nouveau_sommet = False
            for voisin in g[sommet]:
                if (visited == [] or nouveau_sommet) and voisin not in ham_path:
                    ham_path.append(voisin)
                    visited = []
                    break
                elif visited and voisin == visited[-1]:
                    nouveau_sommet = True

            
            else:
                visited.append(ham_path.pop())


    return False, []

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
    retourne une liste de point et un graph correspondant a une dictionnaire d'adjacence
    ainsi qu'une fonction qui prend un des coordonné et renvoie le point (pour des questions d'optimisation)
    la liste l_point n'est donne  qu'a titre indicatif
    """
    graph = {}
    l_point = []
    carre = oscar.square(polygone)
    eps = (carre[1][0] - carre[0][0])/nb_point
    for i in tqdm(range(nb_point), desc="generation de la grille"):
        for j in range(nb_point):
            if is_in_polygone([carre[0][0]+i*eps, carre[0][1]+j*eps], polygone):
                #print("valide")
                l_point.append([carre[0][0]+i*eps, carre[0][1]+j*eps])
                graph[(i, j)] = [(i, j-1), (i, j+1), (i-1, j), (i+1, j)]
   
    for point in list(graph.keys()):
        graph[point] = [voisin for voisin in graph[point] if voisin in graph]

    return l_point, graph, lambda point:[carre[0][0]+point[0]*eps, carre[0][1]+point[1]*eps]

if __name__ == "__main__":

    polygone = [(1,0),(0.71,0.71),(0,1),(-0.71, 0.71),(-1,0),(-0.71,-0.71),(0,-1),(0.71,-0.71)]
    l_point, graph, f = generate_grid(polygone,20)
    
    plt.plot([point[0]for point in polygone], [point[1]for point in polygone]) # affiche la grille
    
    plt.scatter([point[0]for point in l_point], [point[1]for point in l_point], s=1)

    """
    for point in graph.keys():
        for voisin in graph[point]:
            p1 = f(point)
            p2 = f(voisin)
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]])
    """
    #plt.show()
    
    #graph = {1:[2, 4, 5], 2:[1, 4], 3:[7], 4:[1, 2, 6, 7], 5:[1, 6], 6:[4, 5], 7:[3, 4]}
    #print(graph[(0, 52)])
    #a = backtrack_iter(graph, debug=0)
    #b = tabu_search(graph, 10000000)
    #print(b)   
    #print(a)
    #chemin = backtrack_iter(graph, debug=1)[1]   
    chemin = tabu_search(graph, 1000000)[1]
    print(len(chemin))
    
    last_point = chemin.pop(0)
    for point in chemin:
        p1 = f(last_point)
        p2 = f(point)
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]])
        last_point = point
    
    plt.show()