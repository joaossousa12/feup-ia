import random
import algorithms
import utils

class Package:
    def __init__(self, package_type, coordinates):
        self.package_type = package_type
        self.coordinates_x = coordinates[0]
        self.coordinates_y = coordinates[1]
        self.did_break = False
        self.was_late = False
        
        if package_type == 'fragile':
            self.breaking_chance = random.uniform(0.0001, 0.01) # 0.01-1% chance of breaking per km
            self.breaking_cost = random.uniform(3, 10) # Extra cost in case of breaking
        
        elif package_type == 'urgent':
            self.delivery_time = random.uniform(100, 240) # Delivery time in minutes (100 minutes to 4 hours)

def generate_package_stream(num_packages, map_size):
    package_types = ['fragile', 'normal', 'urgent']

    package_stream = [Package(random.choice(package_types), (random.uniform(0, map_size), random.uniform(0, map_size))) for _ in range(num_packages)]

    return package_stream

num_packages = int(input("Number of packages (example: 15): "))
map_size = int(input("Map size (example: 60): "))
package_stream = generate_package_stream(num_packages, map_size)

print("\nRandom order\n")
randomPackageStream = package_stream
utils.printPackageDF(randomPackageStream)
totalCostRandom = round(utils.calculateTotalCost(package_stream), 2)
print("\nThe total cost in this order is :", totalCostRandom)
utils.graphicInterface(package_stream, totalCostRandom)

print("\nGreedy order\n")
greedyPackageStream = algorithms.greedy(package_stream[:])  # Create a copy of package_stream
utils.printPackageDF(greedyPackageStream)
totalCostGreedy = round(utils.calculateTotalCost(greedyPackageStream), 2)
print("\nThe total cost in this order is :", totalCostGreedy)
utils.graphicInterface(greedyPackageStream, totalCostGreedy)

print("\nHill Climbing\n")
hillClimbingPackageStream = algorithms.hill_climbing(package_stream[:])  # Create a copy of package_stream
utils.printPackageDF(hillClimbingPackageStream)
totalCostHillClimbing = round(utils.calculateTotalCost(hillClimbingPackageStream), 2)
print("\nThe total cost in this order is :", totalCostHillClimbing)
utils.graphicInterface(hillClimbingPackageStream, totalCostHillClimbing)

print("\nGenetic Algorithm\n")
geneticPackageStream = algorithms.genetic_algorithm(package_stream[:], num_packages * 2)  # Create a copy of package_stream
utils.printPackageDF(geneticPackageStream)
totalCostGenetic = round(utils.calculateTotalCost(geneticPackageStream), 2)
print("\nThe total cost in this order is :", totalCostGenetic)
utils.graphicInterface(geneticPackageStream, totalCostGenetic)



if totalCostGreedy < totalCostRandom and totalCostGreedy < totalCostHillClimbing and totalCostGreedy < totalCostGenetic:
    print("\nThe approach with the minimum cost is the greedy one")
elif totalCostRandom < totalCostGreedy and totalCostRandom < totalCostHillClimbing and totalCostRandom < totalCostGenetic:
    print("\nThe approach with the minimum cost is the random one")
elif totalCostHillClimbing < totalCostGreedy and totalCostHillClimbing < totalCostRandom and totalCostHillClimbing < totalCostGenetic:
    print("\nThe approach with the minimum cost is the hill climbing one")
else:
    print("\nThe approach with the minimum cost is the genetic algorithm one")