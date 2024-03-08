import package
import random

class Path:
    def __init__(self, package_stream):
        self.package_stream = package_stream
        self.cost = self.calculateTotalCost()

    def calculateTotalCost(self):
        totalCost = 0
        totalDistance = 0
        currLocation = (0, 0)

        for package in self.package_stream:
            distanceToPackage = package.dist(currLocation[0],currLocation[1])
            totalDistance += distanceToPackage

            totalCost += distanceToPackage * 0.3

            if package.package_type == 'fragile':
                damageChance = package.actualDamageChance(totalDistance)

                if damageChance > random.uniform(0, 1):
                    print('Package broken')
                    totalCost += package.breaking_cost

            elif package.package_type == 'urgent':
                totalCost += package.actualDelayedCost(totalDistance)

            currLocation = (package.coordinates_x, package.coordinates_y)

        return totalCost
    
def generate_package_stream(num_packages, map_size):
        package_types = ['fragile', 'normal', 'urgent']

        package_stream = [package.Package(random.choice(package_types), (random.uniform(0, map_size), random.uniform(0, map_size))) for _ in range(num_packages)]

        return package_stream