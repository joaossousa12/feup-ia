import random
import math

import path

def random_path(package_stream):
    return path.Path(package_stream)

def greedy(package_stream): # will find the nearest package each time 
    currLocation = (0,0)
    result = []
    while len(package_stream) > 0:
        min_distance = float('inf')
        nearest_packages = [] # fix for cases where there are multiple packages at the same distance

        for package in package_stream:
            dist = package.dist(currLocation[0], currLocation[1])
            if dist < min_distance:
                min_distance = dist
                nearest_packages = [package]
            elif dist == min_distance:
                nearest_packages.append(package)
        
        nearest = random.choice(nearest_packages)

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

# start with a given temperature and a given cooling_rate
def simulated_annealing(package_stream, temperature = 700, cooling_rate = 0.003):
    current_sequence = hill_climbing(package_stream)
    current_cost = current_sequence.calculateTotalCost()
    
    lowest = []
    while temperature > 1:
        neighbors = current_sequence.get_neighbors()
        next_sequence = random.choice(neighbors) 
        next_cost = next_sequence.calculateTotalCost()
        # If the new solution is better, accept it
        if next_cost < current_cost:
            current_sequence = next_sequence
            current_cost = next_cost
            lowest.append(current_sequence)
        # if not, we still have a chance to accept it
        else:
            probability = math.exp((current_cost - next_cost) / temperature)
            if random.random() < probability:
                current_sequence = next_sequence
                current_cost = next_cost
        
        temperature *= 1 - cooling_rate
    for i in lowest:
        if i.calculateTotalCost() < current_cost:
            current_sequence = i
            current_cost = i.calculateTotalCost()
    return current_sequence

def genetic_algorithm(package_stream, population_size, generations=5000):
    elite_size = round(0.05 * population_size)
    population = [random.sample(package_stream, len(package_stream)) for _ in range(population_size)]
    
    hill_climbing_solution = hill_climbing(package_stream)
    population[population_size-1] = hill_climbing_solution.package_stream
    
    best_individual = None
    best_fitness = float('inf')
    
    for generation in range(generations):
        fitnesses = [path.Path(individual).calculateTotalCost() for individual in population]

        # update the best individual found so far
        current_best_fitness = min(fitnesses)
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_individual = population[fitnesses.index(current_best_fitness)].copy()
            # did this just to see how the algorithm is working
            print(f"New better solution found at generation {generation}:")
            print(f"Fitness: {best_fitness}")

        # elite selection carry forward the best performing individuals
        elites = select_elites(population, fitnesses, elite_size)

        parents = tournament_selection(population, fitnesses)
        children = []

        # generating children with crossover and mutation
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents): 
                child1, child2 = crossover(parents[i], parents[i+1])
                child1 = mutate_with_probability(child1)
                child2 = mutate_with_probability(child2)
                children.extend([child1, child2])

        # introduce new random individuals to maintain diversity
        new_individuals = [random.sample(package_stream, len(package_stream)) for _ in range(elite_size)]
        population = replace_worst_individuals(population, children + new_individuals, fitnesses)

        # ensuring the elites are always in the population
        population = ensure_elites(population, elites, fitnesses)

    return path.Path(best_individual)

def select_elites(population, fitnesses, elite_size):
    sorted_by_fitness = sorted(zip(fitnesses, population), key=lambda x: x[0])
    elites = [individual for _, individual in sorted_by_fitness[:elite_size]]
    return elites

def ensure_elites(population, elites, fitnesses):
    sorted_population = sorted(zip(fitnesses, population), key=lambda pair: pair[0])
    sorted_population[:len(elites)] = [(0, elite) for elite in elites]  # assuming fitness of 0 for elites for simplicity
    return [individual for _, individual in sorted_population]

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

def tabu_search(package_stream, tabu_size=10, max_iter=1000):
    current_solution = greedy(package_stream)
    best_solution = current_solution
    tabu_list = []

    for iteration in range(max_iter):
        neighbors = current_solution.get_neighbors()

        non_tabu_neighbors = [neighbor for neighbor in neighbors if neighbor.package_stream not in tabu_list]

        if not non_tabu_neighbors:
            break

        best_neighbor = min(non_tabu_neighbors, key=lambda x: x.calculateTotalCost())

        current_solution = best_neighbor

        tabu_list.append(current_solution.package_stream)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        if current_solution.calculateTotalCost() < best_solution.calculateTotalCost():
            best_solution = current_solution
            print(f"Iteration {iteration+1}: Best solution cost = {best_solution.calculateTotalCost()}")

    return best_solution