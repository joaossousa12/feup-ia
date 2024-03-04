import random
import pandas as pd
import math
import matplotlib.pyplot as plt

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

def calcDistance(coordinates1, coordinates2):
    return math.sqrt((coordinates2[0] - coordinates1[0])**2 + (coordinates2[1] - coordinates1[1])**2)

def calcDamageChance(distance, breaking_chance):
    return 1 - ((1 - breaking_chance) ** distance)
    
def graphicInterface(package_stream, totalCost):
    plt.figure(figsize=(8, 8))
    plt.title("Package Delivery Route with a total cost of " + str(totalCost))
    plt.xlabel("X")
    plt.ylabel("Y")

    x_coords = [0] + [package.coordinates_x for package in package_stream]
    y_coords = [0] + [package.coordinates_y for package in package_stream]
    
    plt.scatter(0, 0, color='red', label='Origin')
    plt.text(0, 0, '  Origin', verticalalignment='bottom', color='red')

    for i, (x, y) in enumerate(zip(x_coords[1:], y_coords[1:]), start=1):
        plt.scatter(x, y, label=f'Package {i-1}')
        plt.text(x, y, f'  {i-1}', verticalalignment='bottom')
    
    plt.plot(x_coords, y_coords, marker='o')

    plt.legend()
    plt.grid(True)
    plt.show()

def calculateTotalCost(package_stream):
    totalCost = 0
    totalDistance = 0
    currLocation = (0, 0)

    for package in package_stream:
        distanceToPackage = calcDistance(currLocation, (package.coordinates_x, package.coordinates_y))
        totalDistance += distanceToPackage

        totalCost += distanceToPackage * 0.3

        if package.package_type == 'fragile':
            damageChance = calcDamageChance(totalDistance, package.breaking_chance)
            
            if damageChance > random.uniform(0, 1):
                print('Package broken')
                totalCost += package.breaking_cost
            
        elif package.package_type == 'urgent':
            deliveryTime = totalDistance # vai ser igual porque tamos a calcular em minutos para 60kmh (x * 60 / 60)

            if deliveryTime > package.delivery_time:
                print('After scheduled')
                totalCost += (deliveryTime - package.delivery_time) * 0.3
        
        currLocation = (package.coordinates_x, package.coordinates_y)
    
    return totalCost
            

# Example: Generate a stream of 15 packages in a map of size 60x60

num_packages = 15
map_size = 60
package_stream = generate_package_stream(num_packages, map_size)

df = pd.DataFrame([(i, package.package_type, package.coordinates_x, package.coordinates_y, package.breaking_chance if package.package_type == 'fragile' else None, package.breaking_cost if package.package_type == 'fragile' else None, package.delivery_time if package.package_type == 'urgent' else None) for i, package in enumerate(package_stream, start=1)], columns=["Package", "Type", "CoordinatesX", "CoordinatesY", "Breaking Chance", "Breaking Cost", "Delivery Time"])
print(df)

totalCost = round(calculateTotalCost(package_stream), 2)

print("\nThe total cost in this order is :", totalCost)

graphicInterface(package_stream, totalCost)
