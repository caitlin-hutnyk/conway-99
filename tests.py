import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import graph
import pickle
import sim_anneal
import time

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

def gaptest():
    two = 0
    three = 0
    four = 0
    five = 0
    for i in range(100):
        g = nx.random_regular_graph(14,99)
        gv = graph.eval(g)
        t = sim_anneal.step(g.copy(), 2)
        two += abs(gv - graph.eval(t))
        t = sim_anneal.step(g.copy(), 3)
        three += abs(gv - graph.eval(t))
        t = sim_anneal.step(g.copy(), 4)
        four += abs(gv - graph.eval(t))
        t = sim_anneal.step(g.copy(), 4)
        five += abs(gv - graph.eval(t))
    two /= 100
    three /= 100
    four /= 100
    five /= 100

    print(two)
    print(three)
    print(four)
    print(five)


def main():
    i = 0.98
    while i >= 0.90:
        values = []
        for j in range(10):
            print(j)
            g = nx.random_regular_graph(14,99)
            g, t = sim_anneal.sim_anneal(g, 80, 3, i, 3)
            values.append(t)
        avg = []
        times = []
        # print(values)
        for a in values:
            for j in range(len(a)):
                if len(avg) <= j:
                    avg.append(a[j])
                    times.append(1)
                else:
                    avg[j] += a[j]
                    times[j] += 1
        for j in range(len(avg)):
            avg[j] /= times[j]
        for j in values:
            plt.plot(list(range(len(j))), j)
        plt.ylabel('fitness')
        plt.xlabel('steps')
        plt.savefig('sim_anneal_tests/' + str(i) + '-all.png')
        plt.close()
        plt.plot(list(range(len(avg))), avg)
        plt.ylabel('fitness')
        plt.xlabel('steps')
        plt.savefig('sim_anneal_tests/' + str(i) + '-avg.png')
        plt.close()
        print(i)
        i -= 0.01

if __name__ == "__main__":
    gaptest()   