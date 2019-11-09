import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import graph
import pickle
import sim_anneal

'''
def addTriangle(graph):
    g = nx.to_numpy_matrix(graph)
    full = [0]*99
    for i in range(99):
        for j in range(99):
            if g[i,j]:
                full[i] += 1
    poss = list(range(99)).filter(lambda x: full[x] != 14)
    random.shuffle(poss)
    # find the first two edges
    a,b
    for i in range(len(poss)):
        for j in range(i + 1, len(poss)):
            a = poss[i]
            b = poss[j]
            if g[a,b]:
                continue
            c_a = [n for n in graph.neighbours(a)]
            c_b = [n for n in graph.neighbours(b)]
            if bool(set(c_a) & set(c_b)):
                continue
            
            for k in range(j + 1, len(poss)):

def allPaired():
    # 97 and 98 are the two special vertices which will be saturated
    # 0-6 are the full vertcies which we append

    g = nx.Graph()
    g.add_nodes_from(range(99))
    edges = []
    start = 7
    for i in range(7):
        for j in range(start, start + 10):
            edges.append((i,j))
        for j in range(start, start + 10, 2):
            edges.append((j, j+1))
        edges.append((i, start + 10))
        edges.append((i, start + 11))
        edges.append((i, 97))
        edges.append((i, 98))
        edges.append((start + 10, 97))
        edges.append((start + 11, 98))
        start += 12
    g.add_edges_from(edges)

    # vertices that still need to be populated:
    # 7-96
    # number of edges still to be added: 693 - 147 = 546 (182 triangles)
    return g

'''

def main():
    yes = 0
    no = 0
    for i in range(100):
        g = nx.random_regular_graph(14,99)
        g = graph.mutate(g)
        if graph.verify(g):
            yes += 1
        else:
            no += 1

    print(yes)
    print(no)

if __name__ == "__main__":
    main()
