import random
import time

NUM_QUEENS = 8
POPULATION_SIZE = 100
MUTATION_RATE = 0.5
CROSSOVER_RATE = 1
K = 3
MAX_FITNESS = NUM_QUEENS * (NUM_QUEENS-1)/2


def fitness_score(chromosome):
    score = 0

    for row in range(NUM_QUEENS):
        for other_row in range(NUM_QUEENS):
            # queens cannot pair with itself
            if other_row == row:
                continue
            # col attacking
            if chromosome[other_row] == chromosome[row]:
                continue
            # diagonal attacking
            if other_row + chromosome[other_row] == row + chromosome[row]:
                continue
            # diagonal attacking
            if other_row - chromosome[other_row] == row - chromosome[row]:
                continue
            # score++ if every pair of queens are non-attacking.
            score += 1

    # divide by 2 as pairs of queens are commutative
    return score / 2


def k_tournament_selection(pop, s):
    best = []
    best_score = 0
    for j in range(K):
        inx = random.randint(0, len(pop)-1)
        if j == 0 or s[inx] > best_score:
            best = pop[inx]
            best_score = s[inx]
    return best


def crossover(parents):
    if random.random() < MUTATION_RATE:
        cross_point = random.randint(0, NUM_QUEENS-1)
        return [parents[0][:cross_point] + parents[1][cross_point:],
                parents[1][:cross_point] + parents[0][cross_point:]]
    return parents


def mutation(chromosomes):
    for chromosome in chromosomes:
        if random.random() < MUTATION_RATE:
            chromosome[random.randrange(NUM_QUEENS)] = random.randrange(NUM_QUEENS)
    return chromosomes


# initial population
population = []
for _ in range(POPULATION_SIZE):
    population.append([random.randint(0, NUM_QUEENS-1) for _ in range(NUM_QUEENS)])

population = sorted(population, key=lambda ind: fitness_score(ind), reverse=True)
scores = [fitness_score(chromosome) for chromosome in population]
start = time.time()
end = start
generation = 0
while True:
    new_population = []
    for _ in range(POPULATION_SIZE):

        parent1 = k_tournament_selection(population, scores)
        parent2 = k_tournament_selection(population, scores)
        while parent2 == parent1:
            print('j')
            parent2 = k_tournament_selection(population, scores)
        print('parents: ' + str(parent1) + str(parent2))
        offsprings = crossover([parent1, parent2])
        offsprings = mutation(offsprings)
        print('offspring: ' + str(offsprings))
        for i in offsprings:
            if i not in new_population:
                new_population.append(i)

    # natural selection
    population = sorted(new_population, key=lambda ind: fitness_score(ind), reverse=True)[:POPULATION_SIZE]
    generation += 1
    print('population: ' + str(population))
    # calculate fitness score
    scores = [fitness_score(chromosome) for chromosome in population]
    print('scores: ' + str(scores))
    print()
    end = time.time()
    if MAX_FITNESS in scores or end-start > 20:
        break


for i in range(len(population)):
    if scores[i] == MAX_FITNESS:
        print(population[i])

print(generation)
print(end - start)
print(len(population))
