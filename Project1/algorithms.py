import random

import path

def random_path(package_stream):
    return path.Path(package_stream)

def greedy(package_stream): # will find the nearest package each time 
    currLocation = (0,0)
    result = []
    while len(package_stream) != 1:
        min_distance = float('inf')
        nearest = None

        for package in package_stream:
            dist = package.dist(currLocation[0],currLocation[1])
            
            if dist < min_distance:
                min_distance = dist
                nearest = package
        
        result.append(nearest)
        currLocation = (nearest.coordinates_x, nearest.coordinates_y)
        package_stream.remove(nearest)

    return path.Path(result)

def hill_climbing(package_stream):
    current_sequence = greedy(package_stream)
    current_cost = current_sequence.calculateTotalCost()

    while True:
        neighbors = current_sequence.get_neighbors()
        min_cost = current_cost
        min_sequence = current_sequence.package_stream

        for neighbor in neighbors:
            cost = neighbor.calculateTotalCost()

            if cost < min_cost:
                min_cost = cost
                min_sequence = neighbor

        if min_cost < current_cost:
            current_sequence = min_sequence
            current_cost = min_cost
        else:
            break

    return current_sequence

def genetic_algorithm(package_stream, population_size, generations=200):
    population = [random.sample(package_stream, len(package_stream)) for _ in range(population_size)] # Generate initial random population
    best_individual = None
    best_fitness = float('inf')
    
    for _ in range(generations):
        fitnesses = [path.Path(individual).calculateTotalCost() for individual in population]

        current_best_fitness = min(fitnesses)
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_individual = population[fitnesses.index(best_fitness)].copy()

        parents = tournament_selection(population, fitnesses)

        children = []
        for i in range(0, len(parents), 2):
            child1, child2 = crossover(parents[i], parents[i+1])
            child1 = mutate_with_probability(child1)
            child2 = mutate_with_probability(child2)
            children.extend([child1, child2])

        population = replace_worst_individuals(population, children, fitnesses)

        population[0] = best_individual

    return path.Path(best_individual)

def tournament_selection(population, fitnesses, tournament_size=3):
    parents = []
    for _ in range(len(population)):
        participants = random.sample(list(enumerate(fitnesses)), tournament_size)
        winner = min(participants, key=lambda x: x[1])
        parents.append(population[winner[0]])
    return parents

def crossover(parent1, parent2): # ordered crossover
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child1 = [None]*size
    child1[start:end] = parent1[start:end]
    pointer = end
    for gene in parent2:
        if gene not in child1:
            child1[pointer] = gene
            pointer = (pointer + 1) % size 

    child2 = [None]*size
    child2[start:end] = parent2[start:end]
    pointer = end
    for gene in parent1:
        if gene not in child2:
            child2[pointer] = gene
            pointer = (pointer + 1) % size  

    return child1, child2

def mutate(individual): # swap mutation
    idx1, idx2 = random.sample(range(len(individual)), 2)  
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1] 
    return individual

def mutate_with_probability(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        return mutate(individual)
    return individual

def replace_worst_individuals(population, children, fitnesses):
    sorted_population = [x for _, x in sorted(zip(fitnesses, population), key=lambda pair: pair[0])]
    sorted_population[-len(children):] = children
    return sorted_population