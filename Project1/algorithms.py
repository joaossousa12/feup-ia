import utils
import random

import path

def random_path(package_stream):
    return path.Path(package_stream)

def greedy(package_stream): # will find the nearest package each time 
    currLocation = (0,0)
    result = []
    while len(package_stream) != 1:
        min_distance = float('inf')
        nearest = None

        for package in package_stream:
            dist = package.dist(currLocation[0],currLocation[1])
            
            if dist < min_distance:
                min_distance = dist
                nearest = package
        
        result.append(nearest)
        currLocation = (nearest.coordinates_x, nearest.coordinates_y)
        package_stream.remove(nearest)

    return path.Path(result)
