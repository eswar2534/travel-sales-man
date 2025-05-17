import csv
from place import Place

def read_places_csv(filename):
    """Read places from a CSV file"""
    places = []
    
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            place = Place(
                name=row['Name'],
                lat=float(row['Lat']),
                lon=float(row['Lon'])
            )
            places.append(place)
    
    return places
