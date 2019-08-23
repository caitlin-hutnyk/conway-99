import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# evaluate strong regularity (99,14,1,2)
def eval(graph):
	g = nx.to_numpy_matrix(graph)
	fitness = 0
	for i in range(99):
		for j in range(i + 1, 99, 1):
			count = 0
			for c in range(99):
				if c == i or c == j:
					continue
				if g[i,c] and g[j,c]:
					count += 1
			fitness -= abs(count - (1 if g[i,j] else 2))
	return fitness

def reproduce(first, second):
	a = nx.to_numpy_matrix(first)
	b = nx.to_numpy_matrix(second)
	r = np.zeros(shape=(99,99))

	l = list(range(99))
	random.shuffle(l)

	full = [0]*99
	for i in l:
		poss = []
		for j in range(99):
			if a[i,j] or b[i,j]:
				poss.append(j)
		random.shuffle(poss)
		for j in poss:
			if full[i] >= 14:
				break
			if (not r[i,j]) and full[j] < 14:
				r[i,j] = 1
				r[j,i] = 1
				full[i] += 1
				full[j] += 1
	random.shuffle(l)
	for i in l:
		if full[i] < 14:
			poss = list(set(range(99)).difference(set(poss)))
			for j in poss:
				if full[i] >= 14:
					break
				if (not r[i,j]) and full[j] < 14:
					r[i,j] = 1
					r[j,i] = 1
					full[i] += 1
					full[j] += 1
	for i in l:	
		if full[i] < 14:
			raise Exception('Failed to reproduce')
	return nx.from_numpy_matrix(r)

# returns matrix with the number of common neighbours
# for each pair of vertices
def commonNeighbours(graph):
	g = nx.to_numpy_matrix(graph)
	r = np.zeros(shape=(99,99))

	for i in range(99):
		for j in range(i + 1, 99, 1):
			for c in range(99):
				if c == i or c == j:
					continue
				if g[i,c] and g[j,c]:
					r[i,j] += 1
					r[j,i] += 1

	return r


# verify 14-regularity
def verify(g):
	r = nx.degree_histogram(g)
	if len(r) == 15 and r[14] == 99:
		return True
	return False

def test():
	better = 0
	worse = 0
	fail = 0
	for x in range(500):
		a = nx.random_regular_graph(14, 99)
		b = nx.random_regular_graph(14, 99)
		av = eval(a)
		bv = eval(b)

		try:
			r = reproduce(a,b)
			rv = eval(b)
			if rv > av and rv > bv:
				better += 1
			elif rv < av and rv < bv:
				worse += 1
		except:
			fail += 1
	
	print('better ' + str(better))
	print('worse ' + str(worse))
	print('fail ' + str(fail))

if __name__ == "__main__":
	test()
