import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import datetime

SIZE = 99
DEG = 14
A = 1
C = 2

# evaluate strong regularity (99,14,1,2)
def eval(graph):
	g = nx.to_numpy_matrix(graph)
	fitness = 0
	for i in range(SIZE):
		for j in range(SIZE):
			count = 0
			for c in range(SIZE):
				if g[i,c] and g[j,c]:
					count += 1
			# print(str(i) + " " + str(j) + " " + str(count))
			fitness += ((A if g[i,j] else C) - count)**2
	return fitness - (1-DEG)**2 * SIZE

def fast_eval(graph):
	# tr((2J - A - A^2)^2)
	g = nx.to_numpy_matrix(graph)
	j = np.ones((SIZE,SIZE))
	j2 = np.add(j, j)
	g2 = np.matmul(g, g)
	added = np.subtract(np.subtract(j2,g), g2)
	return np.trace(np.matmul(added, added)) - (1-DEG)**2 * SIZE

# evaluate strong reularity (99,14,1,2)
# but using a graph and its commonNeighbours matrix
def evalMatrix(graph, neighbours):
	result = 0
	adj = nx.to_numpy_matrix(graph)
	for i in range(99):
		for j in range(i + 1, 99, 1):
			if adj[i,j]:
				result -= abs(neighbours[i,j] - 1)
			else:
				result -= abs(neighbours[i,j] - 2)
	return result

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
	for i in range(99):	
		if full[i] < 14:
			raise Exception('Failed to reproduce') 
	return nx.from_numpy_matrix(r)

# scale split distrubution by fitness difference fe-se
def split_reproduce(first, second, fe, se):
	a = nx.to_numpy_matrix(first);
	b = nx.to_numpy_matrix(second);
	r = np.zeros(shape=(99,99))
	diff = fe - se

	# scale difference to range 0-33
	diff = -1 * diff / 500 * 33

	# generate random normal number 
	split = int(np.random.normal(49 + diff, 5))
	# print(split)

	# tracks degree of each vertex in r
	full = [0]*99

	# copy the edges from each side of the cut
	for i in range(split):
		for j in range(i + 1, split):
			if r[i,j]:
				continue
			if a[i,j]:
				r[i,j] = 1
				r[j,i] = 1

				full[i] += 1
				full[j] += 1

	for i in range(split,99):
		for j in range(i + 1,99):
			if r[i,j]:
				continue
			if b[i,j]:
				r[i,j] = 1
				r[j,i] = 1
				full[i] += 1
				full[j] += 1

	l = list(range(99))
	random.shuffle(l)

	# populate cut edges from parent cut edges
	for i in l:
		poss = []
		temp_range = range(0,split) if i >= split else range(split,99) 
		for j in temp_range:
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

	# populate with other edges across the cut
	random.shuffle(l)
	l = list(filter(lambda x: full[x] < 14, l))

	for i in l:
		poss = []
		if i < split:
			poss = list(filter(lambda x: full[x] < 14, list(range(split,99))))
		else:
			poss = list(filter(lambda x: full[x] < 14, list(range(split))))
		for j in poss:
			if full[i] >= 14:
				break
			if (not r[i,j]) and full[j] < 14:
				r[i,j] = 1
				r[j,i] = 1
				full[i] += 1
				full[j] += 1

	# populate with edges not across the cut
	left = []
	for i in range(99):
		if full[i] < 14:
			for j in range(14-full[i]):
				left.append(i)

	while(len(left) > 0):
		if len(set(left)) == 1:
			raise Exception('Failed to reproduce')
		i = random.choice(list(set(left)))
		j = random.choice(list(set(left) - {i}))
		if r[i,j]:
			if len(list(set(left))) == 2:
				raise Exception('Failed to reproduce')
			for t in range(len(set(left))):
				j = random.choice(list(set(left) - {i}))
				if r[i,j]:
					continue
				break
			if r[i,j]:
				raise Exception('Failed to reproduce')

		r[i,j] = 1
		r[j,i] = 1
		left.remove(i)
		left.remove(j)

	return nx.from_numpy_matrix(r)

def ordered_split_reproduce(first, second, fe, se):
	a = nx.to_numpy_matrix(first)
	b = nx.to_numpy_matrix(second)
	r = nx.Graph()
	r.add_nodes_from(list(range(SIZE)))

	diff = fe - se

	# scale difference to range 0-33
	diff = -1 * diff / 1500 * 33
	# print('d: ' + str(diff))

	# generate random normal number 
	split = int(np.random.normal(49 + diff, 3))
	# print('s: ' + str(split))

	# if the split is not in the range, reset it
	while(split < 5 or split > 95):
		split = int(np.random.normal(49 + diff, 3))

	# copy the edges from each side of the cut
	for i in range(split):
		for j in range(i + 1, split):
			if (i,j) in r.edges:
				continue
			if a[i,j]:
				r.add_edge(i,j)

	for i in range(split,SIZE):
		for j in range(i + 1,SIZE):
			if (i,j) in r.edges:
				continue
			if b[i,j]:
				r.add_edge(i,j)

	# list(set()) to remove duplicates
	poss = list(set(list(first.edges) + list(second.edges)))

	# extract edges crossing the cut from both parents
	# bools x != y is just x xor y
	poss = list(filter(lambda x: (x[0] < split) != (x[1] < split), poss))

	random.shuffle(poss)

	for x,y in poss:
		e = (x,y)
		if e in r.edges:
			continue
		if r.degree[x] >= 14 or r.degree[y] >= 14:
			continue
		r.add_edge(x,y)

	# add other edges that are crossing the cut
	rest = []
	for i in range(SIZE):
		for j in range(i + 1, SIZE):
			rest.append((i,j))
	
	# find all possible edges that cross the cut
	# and remove all the ones we've already tried
	rest = list(filter(lambda x: (x[0] < split) != (x[1] < split), rest))
	rest = list(set(rest) - set(poss))

	for x,y in rest:
		e = (x,y)
		if e in r.edges:
			continue
		if r.degree[x] >= 14 or r.degree[y] >= 14:
			continue
		r.add_edge(x,y)

	# populate using other edges
	# this part is ordered so as to fail less
	# order by how many edges are missing
	# then get first from list, and add an edge from that to some random edge
	# (vertex number, edges needed)

	need = []
	for v in range(SIZE):
		if r.degree[v] == 14:
			continue
		need.append((v, 14-r.degree[v]))
	need = list(sorted(need, key = lambda g: -g[1]))

	while len(need) > 0:
		# print(need)
		v1 = need[0]
		poss = list(filter(lambda g: (v1[0],g[0]) not in r.edges and v1[0] != g[0], need))
		# print(poss)
		if len(poss) == 0:
			return -1 # failed :(
		v2 = random.choice(poss)
		r.add_edge(v1[0],v2[0])
		need.remove(v1)
		need.remove(v2)
		if v1[1] > 1:
			need.append((v1[0], v1[1] - 1))
		if v2[1] > 1:
			need.append((v2[0], v2[1] - 1))
		need = list(sorted(need, key = lambda g: -g[1]))

	return r

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

# find four vertices and swap the connection between them
def mutate(graph):
	g = nx.to_numpy_matrix(graph)
	a = random.randint(0,98)
	adj = list(filter(lambda j: g.item((a,j)) != 0, range(g.shape[0])))
	b = random.choice(adj)
	adj = list(filter(
		lambda i: i not in [a,b] and not g.item(a,i), 
		range(g.shape[0])))
	c = random.choice(adj)
	adj = [j for j in range(0,99) if g[c,j] and not g[j,b]]
	d = random.choice(adj)
	g[a,b] = 0
	g[b,a] = 0
	g[c,d] = 0
	g[d,c] = 0
	g[a,c] = 1
	g[c,a] = 1
	g[b,d] = 1
	g[d,b] = 1
	return nx.from_numpy_matrix(g)

# verify 14-regularity
def verify(g):
	r = nx.degree_histogram(g)
	# print(r)
	if len(r) == 15 and r[14] == 99:
		return True
	return False

# randomly populate the rest of the edges of a partial graph
# while keeping the regularity condition
def populate(g):
	left = 693 - len(g.edges)

	while left > 0:
		poss = list(filter(lambda x: g.degree[x] < 14, list(range(99))))
		[i,j] = random.sample(poss, 2)
		if g.has_edge(i,j):
			if len(poss) == 2:
				raise Exception("Failed to populate")
			continue
		g.add_edge(i,j)
		left -= 1

	return g

def test():
	better = 0
	worse = 0
	for i in range(100):
		a = nx.random_regular_graph(14,99)
		b = mutate(a)
		av = eval(a)
		bv = eval(b)
		if av < bv:
			better += 1
		elif bv < av:
			worse += 1
		
	print(better)
	print(worse)

if __name__ == "__main__":
	g = nx.random_regular_graph(14,99)
	h = nx.random_regular_graph(14,99)
	ordered_split_reproduce(g,h, fast_eval(g), fast_eval(h))
