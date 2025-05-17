def greedy_solver(dist_matrix, start_idx=0):
    """
    Greedy algorithm for TSP
    Start at the given index and always visit the nearest unvisited place
    """
    n = len(dist_matrix)
    unvisited = set(range(n))
    tour = [start_idx]
    unvisited.remove(start_idx)
    
    while unvisited:
        current = tour[-1]
        # Find the nearest unvisited place
        nearest = min(unvisited, key=lambda x: dist_matrix[current][x])
        tour.append(nearest)
        unvisited.remove(nearest)
    
    return tour

def two_opt_swap(route, i, j):
    """Swap two edges in a route using 2-opt"""
    new_route = route[:i]
    new_route.extend(reversed(route[i:j + 1]))
    new_route.extend(route[j + 1:])
    return new_route

def two_opt_improve(tour, dist_matrix):
    """
    Improve a tour using 2-opt algorithm
    Keep swapping pairs of edges if it improves the tour length
    """
    n = len(tour)
    improved = True
    best_distance = calculate_tour_distance(tour, dist_matrix)
    
    while improved:
        improved = False
        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                # Consider the swap: (tour[i-1], tour[i]) and (tour[j], tour[j+1])
                new_tour = two_opt_swap(tour, i, j)
                new_distance = calculate_tour_distance(new_tour, dist_matrix)
                
                if new_distance < best_distance:
                    tour = new_tour
                    best_distance = new_distance
                    improved = True
                    break  # Break inner loop to restart with the new tour
            if improved:
                break  # Break outer loop to restart with the new tour
    
    return tour

def calculate_tour_distance(tour, dist_matrix):
    """Calculate the total distance of a tour"""
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += dist_matrix[tour[i]][tour[i + 1]]
    return total_distance
