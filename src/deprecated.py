def backtrack_rec(g, debug=1):
    """
    DEPRECATED
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

    """
    DEPRECATED
    """

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


def generate_path_via_point(graph, flag_to_visit, debug=1):
    """
    backtracking itératif mais en ne passant obligatoirement que sur certain point (vise a remplacer backtrack_iter et backtrack_rec)
    """

    if debug:
        progression_bar = tqdm(total=len(flag_to_visit), desc='Longueur du chemin')

    chemin = []
    visited = []
    flag_visited = [] # parmis les sommet de flag_to_visite: sommet deja visiter
    first_sommet_tried = [] # sommet de flag_to_visite n'ayant rien donné

    

    while len(first_sommet_tried) != len(flag_to_visit):
        
        if debug:
            progression_bar.n = len(first_sommet_tried)
            progression_bar.refresh()

        if len(flag_visited) == len(flag_to_visit):
            break

        if chemin == []:
            new_point = False
            for point in flag_to_visit:
                if point not in first_sommet_tried:
                    chemin = [point]
                    first_sommet_tried.append(point)
                    flag_visited.append(point)
                    visited= []
                    break
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
        return False, []
    return True, chemin