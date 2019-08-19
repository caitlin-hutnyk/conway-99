import random
import networkx as nx
import graph
import pickle

# graphs is a list of tuples (graph, fitness)
def generation(graphs):
	n = []
	for g in graphs[:20]:
		n.append(g)
	temp = graphs[:40]
	for t in range(4):
		random.shuffle(temp)
		for i in range(0,40,2):
			try:
				g = graph.reproduce(temp[i], temp[i+1])
				n.append(g, graph.eval(g))
			except:
				n.append(graphs[t] if graphs[i][1] < graphs[i+1][1] else graphs[i+1])
	n = sorted(n, key = lambda g : - g[1])
	return n

def run(gens):
	pop = []
	for i in range(100):
		g = nx.random_regular_graph(14,99)
		pop.append((g, graph.eval(g)))
	print(pop)
	pop = sorted(pop, key = lambda g : - g[1])
	print(pop)
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
		print('\n \n \n')
		pop = generation(pop)
	print(sorted(pop, key = lambda g : - g[1]))
	
if __name__ == "__main__":
	run(100)