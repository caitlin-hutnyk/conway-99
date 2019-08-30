import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import graph
import pickle

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
    # number of edges still to be added: 693 - 147 = 546
    return g

def main():
    g = allPaired()
    g = graph.populate(g)
    e = graph.eval(g)
    if e > -1000:
        with open('luckygraph.pickle', 'wb') as f:
                pickle.dump(g, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(e)

    nx.draw(g)
    plt.show()

if __name__ == "__main__":
    main()
