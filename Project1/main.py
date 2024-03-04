import random
import pandas as pd
import algorithms
import utils

class Package:
    def __init__(self, package_type, coordinates):
        self.package_type = package_type
        self.coordinates_x = coordinates[0]
        self.coordinates_y = coordinates[1]
        
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

print("Random order\n")

df = pd.DataFrame([(i, package.package_type, package.coordinates_x, package.coordinates_y, package.breaking_chance if package.package_type == 'fragile' else None, package.breaking_cost if package.package_type == 'fragile' else None, package.delivery_time if package.package_type == 'urgent' else None) for i, package in enumerate(package_stream, start=1)], columns=["Package", "Type", "CoordinatesX", "CoordinatesY", "Breaking Chance", "Breaking Cost", "Delivery Time"])
print(df)

totalCost = round(utils.calculateTotalCost(package_stream), 2)

print("\nThe total cost in this order is :", totalCost)

utils.graphicInterface(package_stream, totalCost)

print("Greedy order\n")
greedyPackageStream = algorithms.greedy(package_stream)

df = pd.DataFrame([(i, package.package_type, package.coordinates_x, package.coordinates_y, package.breaking_chance if package.package_type == 'fragile' else None, package.breaking_cost if package.package_type == 'fragile' else None, package.delivery_time if package.package_type == 'urgent' else None) for i, package in enumerate(greedyPackageStream, start=1)], columns=["Package", "Type", "CoordinatesX", "CoordinatesY", "Breaking Chance", "Breaking Cost", "Delivery Time"])
print(df)

totalCostGreedy = round(utils.calculateTotalCost(greedyPackageStream), 2)

print("\nThe total cost in this order is :", totalCostGreedy)

utils.graphicInterface(greedyPackageStream, totalCostGreedy)

if totalCostGreedy < totalCost:
    print("\nThe approach with the minimum cost is the greedy one")

else:
    print("\nThe approach with the minimum cost is the random one")