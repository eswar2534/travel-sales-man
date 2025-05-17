import json

def create_geojson(places, tour, return_to_start=False):
    """
    Create a GeoJSON LineString of the tour
    If return_to_start is True, add the starting point at the end to complete the loop
    """
    # Create a list of coordinates for the tour
    coordinates = []
    for idx in tour:
        place = places[idx]
        coordinates.append([place.lon, place.lat])  # GeoJSON uses [lon, lat] order
    
    # If returning to start, add the first point again at the end
    if return_to_start:
        coordinates.append([places[tour[0]].lon, places[tour[0]].lat])
    
    # Create the GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates
                }
            }
        ]
    }
    
    return geojson

def save_geojson(geojson, filename="route.geojson"):
    """Save the GeoJSON to a file"""
    with open(filename, 'w') as f:
        json.dump(geojson, f, indent=2)
