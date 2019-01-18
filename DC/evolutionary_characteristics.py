import random
rand = lambda x : random.randint(0, x-1)

from ThreeCircle import *
from Util import *
from Constants import *

import array
import numpy
import multiprocessing

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

POPULATION_SIZE = 300
NUM_GENERATIONS = 5
CROSS_CHANCE = 0.5
MUTATION_START_CHANCE = 0.3
MUTATION_CHANCE = 2 * 1.0 / (LANES * DIGITS_PER_LANE)

def linear(a):
	a = theta(a)
	a = pi(a)
	a = iota(a)
	a = rho(a)
	return a

creator.create("FitnessHammingWeight", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessHammingWeight)

toolbox = base.Toolbox()

# Attribute generator
#toolbox.register("digit", lambda : random.choice([0,0,0,0,0,0,1,2]))
#toolbox.register("digit", rand, P)
toolbox.register("digit", lambda : 0)

# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, \
	toolbox.digit, LANES * DIGITS_PER_LANE)

# Define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# The function to be maximized
def evalFitness(individual, n=128, print_trail=False, target=-1):
	ROUNDS = 3

	fitnesses = []

	i = 0
	while i < n or print_trail:
		i += 1

		hws = []

		X = [rand(P) for _ in range(LANES * DIGITS_PER_LANE)]
		Y = digitwise_addition(X, individual)

		if X == Y and not print_trail:
			return ROUNDS * 160 + 1,

		sX = to_state(X)
		sY = to_state(Y)

		hws.append(hamming_weight(individual))

		for _ in range(ROUNDS - 1):
			sX = round(sX)
			sY = round(sY)
			hws.append(hamming_weight(difference(from_state(sX), from_state(sY))))

		fitnesses.append(sum(hws))

		if print_trail and sum(hws) <= target:
			#print(i)
			#print(hws)
			break

	if not print_trail:
		return np.min(fitnesses), 


	sX = to_state(X)
	sY = to_state(Y)

	for i in range(ROUNDS):
		#print("Difference chi in round %s" % i)
		#prints(difference(from_state(sX), from_state(sY)))
		#print()
		#print(to_state(difference(from_state(sX), from_state(sY))))

		cX = chi(sX)
		cY = chi(sY)

		sX = linear(cX)
		sY = linear(cY)

	print((individual, difference(from_state(sX), from_state(sY))), ', ')



# Register the fitness function
toolbox.register("evaluate", evalFitness)

# Register the crossover operator
toolbox.register("mate", tools.cxTwoPoint)

# Register the mutation operator
def randomize(individual, p):
	for i in range(len(individual)):
		if random.random() < p:
			individual[i] = random.choice([0, 1, 2])
	return individual,

toolbox.register("mutate", randomize, p=MUTATION_CHANCE)

# Register the individuals for breeding
toolbox.register("select", tools.selTournament, tournsize=3)

# Enable multithreading
pool = multiprocessing.Pool()
toolbox.register("map", pool.map)

def main():
	pop = toolbox.population(n=POPULATION_SIZE)
	hof = tools.HallOfFame(3)

	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("average", numpy.mean)
	stats.register("stdev  ", numpy.std)
	stats.register("min", numpy.min)
	stats.register("max", numpy.max)

	pop, log = algorithms.eaSimple(pop, toolbox, cxpb=CROSS_CHANCE, mutpb=MUTATION_START_CHANCE, \
		ngen=NUM_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

	print("=== Hall of fame ===")
	for i in range(len(hof)):
		print("Rank # %s has a fitness of %s and is individual:" % (i, evalFitness(hof[i], n=2**10)[0]))
		prints(hof[i])

	evalFitness(hof[0], print_trail=True, target=16)

if __name__ == "__main__":
	main()

