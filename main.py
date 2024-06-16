import random
import matplotlib.pyplot as plt

from src.graph_analysis import parcours_exaustive, generate_path_via_point
from src.polygone_analysis import generate_grid
from src.christofides import christofides_tsp, convert_graph_list_to_dict

#graph = {1:[2, 4, 5], 2:[1, 4], 3:[7], 4:[1, 2, 6, 7], 5:[1, 6], 6:[4, 5], 7:[3, 4]}

polygone = [(1,0),(0.71,0.71),(0,1),(-0.71, 0.71),(-1,0),(-0.71,-0.71),(0,-1),(0.71,-0.71)]
polygone = [(2, 2), (2, 5), (10, 4), (9, 0), (6,1), (5, -1), (4, 3)]

resolution = 15
l_point, graph, f = generate_grid(polygone, resolution)
#graph = convert_graph_list_to_dict(graph)
#print(graph)
chemin = parcours_exaustive(graph, list(graph.keys())[0])

#chemin = max(l_chemin, key=len)
#chemin = christofides_tsp(graph)

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