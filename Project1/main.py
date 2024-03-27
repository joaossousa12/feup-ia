import algorithms
import utils

import path

flag = int(input("Do you want a random number of packages and the map size? (1 for yes, 0 for no): "))

if(flag == 1):
    num_packages = int(input("Number of packages (example: 15): "))
    map_size = int(input("Map size (example: 60): "))
    package_stream = path.generate_random_package_stream(num_packages, map_size)
else:
    num_packages = 15
    map_size = 60
    package_stream = path.generate_static_package_stream()

stats = int(input("Display Statistics? (1 for yes, 0 for no): "))

if(stats == 1):
    algorithms.stats_mode = True

print("\nRandom order\n")
randomPath = algorithms.random_path(package_stream[:])
utils.printPackageDF(randomPath)
totalCostRandom = round(randomPath.cost, 2)
print("\nThe total cost in this order is :", totalCostRandom)
utils.graphicInterface(randomPath, totalCostRandom)

print("\nGreedy order\n")
greedyPath = algorithms.greedy(package_stream[:])
utils.printPackageDF(greedyPath)
totalCostGreedy = round(greedyPath.cost, 2)
print("\nThe total cost in this order is :", totalCostGreedy)
utils.graphicInterface(greedyPath, totalCostGreedy)


print("\nHill Climbing\n")
hillClimbingPackageStream = algorithms.hill_climbing(package_stream[:])  # Create a copy of package_stream
utils.printPackageDF(hillClimbingPackageStream)
totalCostHillClimbing = round(hillClimbingPackageStream.calculateTotalCost(), 2)
print("\nThe total cost in this order is :", totalCostHillClimbing)
utils.graphicInterface(hillClimbingPackageStream, totalCostHillClimbing)

print("\nSimulated Anneiling\n")
simulatedAnneilingPath = algorithms.simulated_annealing(package_stream[:])
utils.printPackageDF(simulatedAnneilingPath)
totalCostSimulatedAnneiling = round(simulatedAnneilingPath.cost, 2)
print("\nThe total cost in this order is :", totalCostSimulatedAnneiling)
utils.graphicInterface(simulatedAnneilingPath, totalCostSimulatedAnneiling)

print("\nGenetic Algorithm\n")
geneticPackageStream = algorithms.genetic_algorithm(package_stream[:], 50, 5000)  # Create a copy of package_stream
utils.printPackageDF(geneticPackageStream)
totalCostGenetic = round(geneticPackageStream.calculateTotalCost(), 2)
print("\nThe total cost in this order is :", totalCostGenetic)
utils.graphicInterface(geneticPackageStream, totalCostGenetic)

print("\nTabu Search\n")
tabu_solution = algorithms.tabu_search(package_stream[:], tabu_size=50, max_iter=5000)
utils.printPackageDF(tabu_solution)
total_cost_tabu = round(tabu_solution.calculateTotalCost(), 2)
print("\nThe total cost using Tabu Search is:", total_cost_tabu)
utils.graphicInterface(tabu_solution, total_cost_tabu)