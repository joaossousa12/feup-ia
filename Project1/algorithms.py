import utils

def greedy(package_stream): # will find the nearest package each time 
    currLocation = (0,0)
    result = []
    while len(package_stream) != 1:
        min_distance = float('inf')
        nearest = None

        for package in package_stream:
            dist = utils.calcDistance(currLocation, (package.coordinates_x, package.coordinates_y))
            
            if dist < min_distance:
                min_distance = dist
                nearest = package
        
        result.append(nearest)
        currLocation = (nearest.coordinates_x, nearest.coordinates_y)
        package_stream.remove(nearest)

    return result

def hill_climbing(package_stream):
    current_sequence = package_stream
    current_cost = utils.calculateTotalCost(current_sequence)

    while True:
        neighbors = get_neighbors(current_sequence)

        min_cost = current_cost
        min_sequence = current_sequence

        for neighbor in neighbors:
            cost = utils.calculateTotalCost(neighbor)

            if cost < min_cost:
                min_cost = cost
                min_sequence = neighbor

        if min_cost < current_cost:
            current_sequence = min_sequence
            current_cost = min_cost
        else:
            break

    return current_sequence

def get_neighbors(sequence):
    neighbors = []

    for i in range(len(sequence)):
        for j in range(i + 1, len(sequence)):
            neighbor = sequence.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)

    return neighbors