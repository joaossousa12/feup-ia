import package
import random

class Path:
    def __init__(self, package_stream):
        self.package_stream = package_stream
        self.cost = self.calculateTotalCost()

    def calculateTotalCost(self): # calculate the total cost of the path
        totalCost = 0
        totalDistance = 0
        currLocation = (0, 0)

        for package in self.package_stream:
            distanceToPackage = package.dist(currLocation[0],currLocation[1])
            totalDistance += distanceToPackage

            totalCost += distanceToPackage * 0.3

            if package.package_type == 'fragile':
                damageChance = package.actualDamageChance(totalDistance)
                #if damageChance > random.uniform(0, 1):
                #    totalCost += package.breaking_cost
                
                totalCost += package.breaking_cost * damageChance
                
                # dantes tinhamos uma função que realmente via se o package tinha sido partido ou não,
                # mas isso fazia com que para diferentes runs do algoritmo, certas vezes o package ia partir,
                # e o totalCost ia aumentar, mas para a mesmo solução, certas vezes não partia e o totalCost não iria aumentar

                # de forma a termos uma função de cálculo de custo mais determinístico (que não dependesse da run em si), atualizamos
                # o totalCost, para ter apenas em conta a damageChange e o breakingCost, e para não depender de uma função Random 

                
                   

            elif package.package_type == 'urgent':
                totalCost += package.actualDelayedCost(totalDistance)

            currLocation = (package.coordinates_x, package.coordinates_y)

        return totalCost
    
    def get_neighbors(self): # get neighbors of the current path
        neighbors = []

        for i in range(len(self.package_stream)):
            for j in range(i + 1, len(self.package_stream)):
                neighbor = self.package_stream.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(Path(neighbor))

        return neighbors

def generate_random_package_stream(num_packages, map_size): # random package stream
        package_types = ['fragile', 'normal', 'urgent']

        package_stream = [package.Package(random.choice(package_types), (random.uniform(0, map_size), random.uniform(0, map_size))) for _ in range(num_packages)]

        return package_stream


def generate_static_package_stream(): # static package stream
    package_stream = [
        package.Package('urgent', (27.578325617764513, 38.566145329029766), delivery_time=114.44385489765162),
        package.Package('urgent', (3.7432942291667914, 4.068831340717898), delivery_time=160.69084169295067),
        package.Package('urgent', (19.154428567901316, 20.47437713709128), delivery_time=212.33365704000317),
        package.Package('normal', (35.595270390666705, 31.979426598785277)),
        package.Package('urgent', (15.518707115391377, 19.7838014654967), delivery_time=119.37543684267742),
        package.Package('normal', (39.19523336854898, 1.572209409665588)),
        package.Package('normal', (44.768768924216594, 18.75556069179625)),
        package.Package('urgent', (42.31398169810582, 30.643075068936543), delivery_time=138.7892011502737),
        package.Package('normal', (14.305560722769727, 49.70566821771891)),
        package.Package('urgent', (28.828561217992153, 56.9417819134509), delivery_time=112.0739703767673),
        package.Package('urgent', (46.059972361900996, 44.5279398920997), delivery_time=214.6684149528738),
        package.Package('urgent', (43.930266789993226, 21.001711989868234), delivery_time=171.8955694442465),
        package.Package('normal', (53.43139099481249, 38.258046754120926)),
        package.Package('fragile', (45.258413136235205, 24.703895162456703), breaking_chance=0.008558069180790018, breaking_cost=4.966180668086315),
        package.Package('urgent', (19.72087656269181, 37.670182228059744), delivery_time=201.82828954896564)
    ]
    return package_stream