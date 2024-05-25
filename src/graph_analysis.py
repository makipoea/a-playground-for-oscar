# Ce fichier contient l'espoire futile de reeimpleementer networkx (mais en pire) avec pour seul avantage qu'on y comprenne queque chose
import sys
import logging
import numpy as np
import matplotlib.pyplot as plt 
from tqdm import tqdm
import random 

from src.polygone_analysis import  generate_grid


sys.setrecursionlimit(100000000)

def tabu_search(graph, max_iterations, rnd = 0):
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
                if rnd:
                    next_node = random.choice(unvisited_neighbors)
                else: 
                    next_node = unvisited_neighbors[0]
            else:
                non_tabu_neighbors = [n for n in neighbors if n not in tabu_list]
                if non_tabu_neighbors:
                    if rnd:
                        next_node = random.choice(non_tabu_neighbors)
                    else:
                        next_node = non_tabu_neighbors[0]
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

"""
class Condition(type):
    def __new__(cls, name, bases, dct):
        required_methods = ['is_valide', 'update_add_point', 'update_supress_point']
        required_attributes = ['first_sommet_to_tried']

        for method in required_methods:
            if method not in dct:
                raise TypeError(f"{method} n'as pas ete implementer : la recherche ne peux pas etre effectuer")

        for attr in required_attributes:
            if attr not in dct:
                raise TypeError(f"{attr} : n'as pas ete implementer")
        
        return super().__new__(cls, name, bases, dct)
"""


class condition_visit_list_of_flag:#(metaclass=Condition):
    def __init__(self, flag_to_visit, first_sommet_to_tried):
        self.__flag_to_visit = flag_to_visit
        self.__flag_visited = []
        self.first_sommet_to_tried = first_sommet_to_tried

    def is_valide(self):
        return len(self.__flag_to_visit) == len(self.__flag_visited)

    def update_add_point(self, point):
        if point in self.__flag_to_visit:
            self.__flag_visited.append(point)

    def update_supress_point(self, point):
        if point in self.__flag_to_visit:
            self.__flag_visited.pop() # remove(point)

class condition_visit_sub_graph:

    def __init__(self, graph, pas):
        self.__square_to_visit = {}
        self.__pas = pas

        for point in graph.keys():
            self.__square_to_visit[(point[0]//pas, point[1]//pas)] = []

        self.first_sommet_to_tried = list(graph.keys())

    def is_valide(self):
        #print(self.__square_to_visit)
        return all(list(self.__square_to_visit.values()))

    def update_add_point(self, point):
        self.__square_to_visit[(point[0]//self.__pas, point[1]//self.__pas)].append(point)
    
    def update_supress_point(self, point):
        self.__square_to_visit[(point[0]//self.__pas, point[1]//self.__pas)].pop()

def generate_path_via_point(graph, condition ,debug=1):
    """
    backtracking itératif mais en ne passant obligatoirement que sur certain point (vise a remplacer backtrack_iter et backtrack_rec)
    """

    if debug:
        progression_bar = tqdm(total=len(condition.first_sommet_to_tried), desc='sommet a essayer')

    chemin = []
    visited = []
    first_sommet_tried = [] # sommet de flag_to_visite n'ayant rien donné

    while len(first_sommet_tried) != len(condition.first_sommet_to_tried):
        
        if debug:
            progression_bar.n = len(first_sommet_tried)
            progression_bar.refresh()

        if condition.is_valide():
            break

        if chemin == []:
            new_point = False
            for point in condition.first_sommet_to_tried:
                if point not in first_sommet_tried:
                    chemin = [point]
                    first_sommet_tried.append(point)
                    condition.update_add_point(point)
                    visited= []
                    break
        else:
            point = chemin[-1]
            new_point = False
            for voisin in graph[point]:
                if (visited == [] or new_point) and voisin not in chemin:
                    chemin.append(voisin)
                    condition.update_add_point(voisin)
                    visited = []
                    break
                elif visited and voisin == visited[-1]:
                    new_point = True
            else:
                visited = [chemin.pop()]
                condition.update_supress_point(point)
    else:
        return False, []
    return True, chemin

def generate_path_via_point_from_first_point(graph, flag_to_visit, first_point,debug=0):
    """
    backtracking itératif mais en ne passant obligatoirement que sur certain point (vise a remplacer backtrack_iter et backtrack_rec)
    """
    if debug:
        progression_bar = tqdm(total=len(flag_to_visit), desc='Longueur du chemin')

    chemin = [first_point]
    visited = []
    flag_visited = [first_point] # parmis les sommet de flag_to_visite: sommet deja visiter

    while len(flag_visited) != len(flag_to_visit):

        if debug:
            progression_bar.n = len(flag_visited)
            progression_bar.refresh()


        if chemin == []:
            return (False,[])
        else:
            point = chemin[-1]
            new_point = False
            for voisin in graph[point]:
                if (visited == [] or new_point) and voisin not in chemin:
                    chemin.append(voisin)
                    if voisin in flag_to_visit:
                        #print(f"voisina jouter {voisin}")
                        flag_visited.append(voisin)
                    visited = []
                    break
                elif visited and voisin == visited[-1]:
                    new_point = True
            else:
                visited = [chemin.pop()]
                if point in flag_to_visit:
                    #print(f"point retirer {point}")
                    flag_visited.pop()
    else:
        return True, chemin

def generate_path_throw_polygone(polygone, resolution, densite, debug=0, diplay=1):
    """
    polygone : liste de point
    resolution  <int> : largeur de la grille generer 
    densite  <float> between 0 1 : densité du maillage par lequelle est contraint de passer la ligne 
    """

    l_point, graph, f = generate_grid(polygone, resolution)




if __name__ == "__main__":
    """
    polygone = [(1,0),(0.71,0.71),(0,1),(-0.71, 0.71),(-1,0),(-0.71,-0.71),(0,-1),(0.71,-0.71)]
    
    resolution = 15
    pas = 3

    l_point, graph, f = generate_grid(polygone, resolution)

    for point in graph.keys():
        random.shuffle(graph[point])

    flag_to_visit = []

    for i in range(0, resolution, pas):
        for j in range(0, resolution, pas):
            if (i, j) in graph.keys(): 
                flag_to_visit.append((i, j))
    
    cond = condition_generate_path_on_defined_point(flag_to_visit, flag_to_visit)
    #graph = {1:[2, 4, 5], 2:[1, 4], 3:[7], 4:[1, 2, 6, 7], 5:[1, 6], 6:[4, 5], 7:[3, 4]}

    chemin = generate_path_via_point(graph, cond)[1]

    print("resultat ", chemin)

    
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
    
"""

def main_vraque():
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
    chemin = tabu_search(graph, 10000000, rnd=1)[1]
    print(len(chemin))
    
    last_point = chemin.pop(0)
    for point in chemin:
        p1 = f(last_point)
        p2 = f(point)
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]])
        last_point = point
    
    plt.show()
