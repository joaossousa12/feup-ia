import math
import matplotlib.pyplot as plt
import random
import pandas as pd

def calcDistance(coordinates1, coordinates2):
    return math.sqrt((coordinates2[0] - coordinates1[0])**2 + (coordinates2[1] - coordinates1[1])**2)

def calcDamageChance(distance, breaking_chance):
    return 1 - ((1 - breaking_chance) ** distance)

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

def printPackageDF(package_stream):
    df = pd.DataFrame([(i, package.package_type, package.coordinates_x, package.coordinates_y, 
                        package.breaking_chance if package.package_type == 'fragile' else None, 
                        package.breaking_cost if package.package_type == 'fragile' else None, 
                        package.delivery_time if package.package_type == 'urgent' else None) 
                        for i, package in enumerate(package_stream, start=1)], 
                        columns=["Package", "Type", "CoordinatesX", "CoordinatesY", "Breaking Chance", "Breaking Cost", "Delivery Time"])
    print(df)