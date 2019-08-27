import random
import networkx as nx
import graph
import pickle

# graphs is a list of tuples (graph, fitness)
def generation(graphs):
	n = []
	for g in graphs[:10]:
		n.append(g)
		m = graph.mutate(g[0])
		n.append((m, graph.eval(m)))
	temp = graphs[:40]
	for t in range(4):
		random.shuffle(temp)
		for i in range(0,40,2):
			a = temp[i][0]
			b = temp[i+1][0]
			fail = 0
			while fail < 10:
				try:
					x = graph.reproduce(a,b)
					n.append((x, graph.eval(x)))
					break
				except:
					fail += 1
					if fail % 2 == 0:
						a = graph.mutate(a)
						b = graph.mutate(b)
			if fail == 10:
				x = a if graph.eval(a) > graph.eval(b) else b
				x = graph.mutate(x)
				n.append((x, graph.eval(x)))
	n = sorted(n, key = lambda g : - g[1])
	return n

def run(gens):
	pop = []
	for i in range(100):
		g = nx.random_regular_graph(14,99)
		pop.append((g, graph.eval(g)))
	pop = sorted(pop, key = lambda g : - g[1])
	for gen in range(gens):
		print('running generation ' + str(gen))
		print('top two: ' + str(pop[0][1]) + ', ' + str(pop[1][1]))
		if (gen % 10 == 0):
			with open('graph' + str(gen) + '.pickle', 'wb') as f:
				pickle.dump(pop[0], f, protocol=pickle.HIGHEST_PROTOCOL)
		avg = 0
		for g in pop:
			avg += g[1] / 100
		print('average fitness: ' + str(avg))
		print('\n \n')
		pop = generation(pop)
	print(sorted(pop, key = lambda g : - g[1]))
	
if __name__ == "__main__":
	run(500)