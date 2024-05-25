import random
import matplotlib.pyplot as plt

from src.graph_analysis import condition_visit_list_of_flag, condition_visit_sub_graph, generate_path_via_point
from src.polygone_analysis import generate_grid

polygone = [(1,0),(0.71,0.71),(0,1),(-0.71, 0.71),(-1,0),(-0.71,-0.71),(0,-1),(0.71,-0.71)]

resolution = 100
pas = 25

l_point, graph, f = generate_grid(polygone, resolution)

for point in graph.keys():
    random.shuffle(graph[point])

"""
flag_to_visit = []

for i in range(0, resolution, pas):
    for j in range(0, resolution, pas):
        if (i, j) in graph.keys(): 
            flag_to_visit.append((i, j))

cond = condition_visit_list_of_flag(flag_to_visit, flag_to_visit)
"""

cond = condition_visit_sub_graph(graph, pas)

res = generate_path_via_point(graph, cond)

print(res)
chemin = res[1]

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