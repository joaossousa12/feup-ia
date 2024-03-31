import random
import math

class Package:
    # made some of the values default to None because of the static package stream
    # so there is actually 0 randomness in the delivery_time, breaking_chance and breaking_cost
    def __init__(self, package_type, coordinates, delivery_time=None, breaking_chance=None, breaking_cost=None):
        self.package_type = package_type
        self.coordinates_x = coordinates[0]
        self.coordinates_y = coordinates[1]
        
        if package_type == 'fragile':
            if breaking_chance is None:
                self.breaking_chance = random.uniform(0.0001, 0.01) # 0.01-1% chance of breaking per km
                self.breaking_cost = random.uniform(3, 10) # Extra cost in case of breaking
            else:
                self.breaking_chance = breaking_chance
                self.breaking_cost = breaking_cost

        elif package_type == 'urgent':
            if delivery_time is None:
                self.delivery_time = random.uniform(100, 240) # Delivery time in minutes (100 minutes to 4 hours)
            else: 
                self.delivery_time = delivery_time

    def dist(self, package): # distance between two packages
        return math.sqrt((self.coordinates_x - package.coordinates_x)**2 + (self.coordinates_y - package.coordinates_y)**2)
    
    def dist(self, coordinates_x, coordinates_y): # distance between a package and a point
        return math.sqrt((self.coordinates_x - coordinates_x)**2 + (self.coordinates_y - coordinates_y)**2)
    
    def actualDamageChance(self, distance): # calculate the actual damage chance for fragile packages
        return 1 - ((1 - self.breaking_chance) ** distance)

    def actualDelayedCost(self, distance): # calculate the actual delayed cost for urgent packages
        return max(0,(distance - self.delivery_time))
    