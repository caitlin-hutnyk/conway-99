import random
import networkx as nx
import matplotlib.pyplot as plt
import graph
import pickle
import numpy as np

# graphs is a list of tuples (graph, fitness)
def generation(graphs):
	n = []
	for g in graphs[:10]:
		n.append(g)
		m = graph.mutate(graph.mutate(g[0]))
		n.append((m, graph.eval(m)))
		for t in range(2):
			m = graph.mutate(graph.mutate(g[0]))
			m = graph.mutate(graph.mutate(m))
			n.append((m, graph.eval(m)))
	temp = graphs[:40]
	for t in range(4):
		random.shuffle(temp)
		for i in range(0,30,2):
			a = temp[i][0]
			b = temp[i+1][0]
			fail = 0
			while fail < 9:
				try:
					x = graph.reproduce(a,b)
					n.append((x, graph.eval(x)))
					break
				except:
					fail += 1
					if fail % 3 == 0:
						a = graph.mutate(a)
						b = graph.mutate(b)
			if fail == 9:
				x = a if graph.eval(a) > graph.eval(b) else b
				x = graph.mutate(graph.mutate(x))
				n.append((x, graph.eval(x)))
	n = sorted(n, key = lambda g : - g[1])
	return n

def run(gens):
	pop = []
	for i in range(100):
		g = nx.random_regular_graph(14,99)
		pop.append((g, graph.eval(g)))
	pop = sorted(pop, key = lambda g : - g[1])
	avgFitness = []
	bestFitness = []

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
		
		avgFitness.append(avg)
		bestFitness.append(pop[0][1])

		if gen != gens - 1:
			pop = generation(pop)

	plt.plot(np.arange(gens), bestFitness)
	plt.plot(np.arange(gens), avgFitness)
	plt.legend(['best fitness', 'average fitness'])
	plt.xlabel('Generations')
	plt.ylabel('Fitness')
	plt.savefig('results.png')
	with open('results.pickle', 'wb') as f:
		pickle.dump(pop, f, protocol=pickle.HIGHEST_PROTOCOL)
	plt.show()
	
if __name__ == "__main__":
	run(1000)