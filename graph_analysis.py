# Ce fichier contient l'espoire futile de reeimpleementer networkx (mais en pire) avec pour seul avantage qu'on y comprenne queque chose
import os

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

print(len(graph.keys()))
print(backtrack(graph, [], [], []))     