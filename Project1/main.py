import algorithms
import utils

import path

num_packages = int(input("Number of packages (example: 15): "))
map_size = int(input("Map size (example: 60): "))
package_stream = path.generate_package_stream(num_packages, map_size)

print("\nRandom order\n")
randomPath = algorithms.random_path(package_stream)
utils.printPackageDF(randomPath)
totalCostRandom = round(randomPath.cost, 2)
print("\nThe total cost in this order is :", totalCostRandom)
utils.graphicInterface(randomPath, totalCostRandom)

print("\nGreedy order\n")
greedyPath = algorithms.greedy(package_stream)
utils.printPackageDF(greedyPath)
totalCostGreedy = round(greedyPath.cost, 2)
print("\nThe total cost in this order is :", totalCostGreedy)
utils.graphicInterface(greedyPath, totalCostGreedy)


if totalCostGreedy < totalCostRandom:
    print("\nThe approach with the minimum cost is the greedy one")
else:
    print("\nThe approach with the minimum cost is the random one")