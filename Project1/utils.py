import math
import matplotlib.pyplot as plt
import random
import pandas as pd

def graphicInterface(path, totalCost):
    package_stream = path.package_stream

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

def printPackageDF(path):
    package_stream = path.package_stream
    df = pd.DataFrame([(i, package.package_type, package.coordinates_x, package.coordinates_y, 
                        package.breaking_chance if package.package_type == 'fragile' else None, 
                        package.breaking_cost if package.package_type == 'fragile' else None, 
                        package.delivery_time if package.package_type == 'urgent' else None) 
                        for i, package in enumerate(package_stream, start=1)], 
                        columns=["Package", "Type", "CoordinatesX", "CoordinatesY", "Breaking Chance", "Breaking Cost", "Delivery Time"])
    print(df)