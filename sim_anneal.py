import graph
import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

SIZE = 99

# take a step to an adjacent graph
# n is the number of disjoin connected pairs of vertices to swap/cycle
# v is the number of vertices in the graph
def step(graph, n):
	if n < 2:
		raise Exception('Invalid parameter for step: n must be >= 2')

	# pick 4 random vertices
	g = nx.to_numpy_matrix(graph)

	poss = list(range(SIZE))
	a = random.choice(poss)

	poss = list(filter(lambda j: g[j,a] and j != a, poss))
	b = random.choice(poss)

	poss = list(filter(lambda j: j != a and j != b and not g[a,j] and not g[b,j], list(range(SIZE))))
	c = random.choice(poss)

	poss = list(filter(lambda j: not g[a,j] and not g[b,j] and not j == c and g[c,j], poss))
	d = random.choice(poss)

	if n > 2:
		# select the other n-2 pairs
		current = [a,b,c,d]

		while len(current) < 2*n:
			poss = list(range(SIZE))
			for j in current:
				if j in poss:
					poss.remove(j)
				poss = list(filter(lambda x: not g[j,x], poss))
			if len(poss) < 2:
				raise Exception('Could only get ' + str(len(current)/2) + ' pairs')
			i = random.choice(poss)
			poss.remove(i)
			poss = list(filter(lambda x: g[x,i], poss))
			if len(poss) == 0:
				raise Exception('Could only get ' + str(len(current)/2) + ' pairs')
			j = random.choice(poss)
			current.append(i)
			current.append(j)

		# swap edges in cycle
		for i in range(0, 2*n - 2, 2):
			a = current[i]
			b = current[i+1]
			c = current[i+3]
			g[a,b] = 0
			g[b,a] = 0
			g[a,c] = 1
			g[c,a] = 1

		a = current[-2]
		b = current[-1]
		c = current[1]
		g[a,b] = 0
		g[b,a] = 0
		g[a,c] = 1
		g[c,a] = 1

	else:
		# swap adges
		g[a,b] = 0
		g[b,a] = 0
		g[c,d] = 0
		g[d,c] = 0
		g[a,c] = 1
		g[c,a] = 1
		g[b,d] = 1
		g[d,b] = 1

	return nx.from_numpy_matrix(g)

# run simulated annealing on a single graph g
# T is the initial temperature
# FT is the final temperature
# a is alpha, the cooling ratio
# s is the n parameter for the step function: how many disjoint pairs to pick when stepping
def sim_anneal(g, t, ft, a, s):
	while t >= ft:
		gs = step(g, s)
		d = graph.eval(gs) - graph.eval(g)
		if d < 0:
			g = gs
		else:
			if random.random() < exp(-d / t)
		t = a*t
	return g