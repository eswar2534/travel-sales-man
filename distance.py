import math
from place import Place

def haversine(place1: Place, place2: Place) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1 = math.radians(place1.lat), math.radians(place1.lon)
    lat2, lon2 = math.radians(place2.lat), math.radians(place2.lon)
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def build_distance_matrix(places):
    """Build a distance matrix for all places"""
    n = len(places)
    dist_matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(i+1, n):
            distance = haversine(places[i], places[j])
            dist_matrix[i][j] = distance
            dist_matrix[j][i] = distance  # Matrix is symmetric
            
    return dist_matrix
