import heapq
import itertools

"""
pour des raison de flemmes internationnale ce code n'a pas été ecris par mes soins et je n'ai donc qu'une vague idée de ce qu'il fait 
"""

def convert_graph_list_to_dict(g):
    for sommet in g.keys():
        g[sommet] = {voisin:1 for voisin in g[sommet]}
    return g


def prim_mst(graph):
    start_node = next(iter(graph))
    mst = {start_node: {}}
    edges = [(weight, start_node, to) for to, weight in graph[start_node].items()]
    heapq.heapify(edges)
    while edges:
        weight, frm, to = heapq.heappop(edges)
        if to not in mst:
            mst[frm][to] = weight
            mst[to] = {frm: weight}
            for next_to, next_weight in graph[to].items():
                if next_to not in mst:
                    heapq.heappush(edges, (next_weight, to, next_to))
    return mst

def find_odd_degree_vertices(mst):
    degree = {}
    for u in mst:
        degree[u] = len(mst[u])
    return [v for v in degree if degree[v] % 2 != 0]

def minimum_weight_perfect_matching(graph, vertices):
    subgraph = [(graph[u][v], u, v) for u, v in itertools.combinations(vertices, 2) if v in graph[u]]
    subgraph.sort()
    matched = set()
    matching = []
    for weight, u, v in subgraph:
        if u not in matched and v not in matched:
            matched.add(u)
            matched.add(v)
            matching.append((u, v))
    return matching

def eulerian_tour(multi_graph):
    tour = []
    stack = [next(iter(multi_graph))]
    while stack:
        u = stack[-1]
        if multi_graph[u]:
            v = next(iter(multi_graph[u]))
            stack.append(v)
            multi_graph[u].remove(v)
            multi_graph[v].remove(u)
        else:
            tour.append(stack.pop())
    return tour

def eulerian_to_hamiltonian(eulerian_tour):
    path = []
    visited = set()
    for node in eulerian_tour:
        if node not in visited:
            visited.add(node)
            path.append(node)
    path.append(path[0])  # To form a cycle
    return path

def add_matching_to_mst(mst, matching):
    multi_graph = {u: set(v.keys()) for u, v in mst.items()}
    for u, v in matching:
        multi_graph[u].add(v)
        multi_graph[v].add(u)
    return multi_graph

def christofides_tsp(graph):
    # Step 1: Find a minimum spanning tree (MST)
    mst = prim_mst(graph)
    
    # Step 2: Find all vertices of odd degree in the MST
    odd_degree_vertices = find_odd_degree_vertices(mst)
    
    # Step 3: Find a minimum weight perfect matching for odd degree vertices
    matching = minimum_weight_perfect_matching(graph, odd_degree_vertices)
    
    # Step 4: Combine the matching edges with the MST to form a multigraph
    multi_graph = add_matching_to_mst(mst, matching)
    
    # Step 5: Find an Eulerian tour in the multigraph
    euleur_tour = eulerian_tour(multi_graph)
    
    # Step 6: Convert the Eulerian tour to a Hamiltonian cycle
    hamiltonian_cycle = eulerian_to_hamiltonian(euleur_tour)
    
    return hamiltonian_cycle


if __name__ == "__main__":
    graph = {'A':{'B': 1, 'C': 2, 'D':1, 'E':1}, 'B':{'A': 1, 'C':1, 'D': 2, 'E':1}, 'C':{'A': 2, 'B':1, 'D':1, 'E':1}, 'D':{'A':1, 'B':2, 'C':1, 'E':1}, 'E':{'A':1, 'B':1, 'C':1, 'D':1}}

    a = christofides_tsp(graph)
    print(a)