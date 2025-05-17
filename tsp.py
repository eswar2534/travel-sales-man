#!/usr/bin/env python3
import argparse
from csv_reader import read_places_csv
from distance import build_distance_matrix, haversine
from tsp_solver import greedy_solver, two_opt_improve, calculate_tour_distance
from geojson_exporter import create_geojson, save_geojson
from place import Place

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Travelling Salesman Problem Solver')
    parser.add_argument('--csv', required=True, help='Path to CSV file with places')
    parser.add_argument('--start', help='Name of the starting place')
    parser.add_argument('--return', dest='return_to_start', action='store_true', 
                        help='Return to the starting point')
    parser.add_argument('--algo', choices=['greedy', 'two-opt', 'simulated-annealing'], 
                        default='two-opt', help='Algorithm to use')
    args = parser.parse_args()
    
    # Read places from CSV
    places = read_places_csv(args.csv)
    if not places:
        print(f"Error: No places found in {args.csv}")
        return
    
    # Find the starting index
    start_idx = 0
    if args.start:
        for i, place in enumerate(places):
            if place.name == args.start:
                start_idx = i
                break
        else:
            print(f"Warning: Starting place '{args.start}' not found. Using first place instead.")
    
    # Build distance matrix
    dist_matrix = build_distance_matrix(places)
    
    # Solve TSP
    if args.algo == 'greedy':
        tour = greedy_solver(dist_matrix, start_idx)
    elif args.algo == 'two-opt':
        # Start with greedy solution and improve it
        tour = greedy_solver(dist_matrix, start_idx)
        tour = two_opt_improve(tour, dist_matrix)
    elif args.algo == 'simulated-annealing':
        # This would be implemented as an extension
        print("Simulated annealing not implemented yet. Using two-opt instead.")
        tour = greedy_solver(dist_matrix, start_idx)
        tour = two_opt_improve(tour, dist_matrix)
    
    # Calculate total distance
    total_distance = calculate_tour_distance(tour, dist_matrix)
    
    # If return to start is requested, add the distance back to start
    if args.return_to_start:
        total_distance += dist_matrix[tour[-1]][tour[0]]
        # For GeoJSON, we'll add the starting point at the end in create_geojson
    
    # Print the results
    print("Optimal tour:")
    for i, idx in enumerate(tour, 1):
        print(f"{i}) {places[idx].name}")
    
    if args.return_to_start:
        print(f"{len(tour)+1}) {places[tour[0]].name}")
    
    print(f"Total distance: {total_distance:.1f} km")
    
    # Create and save GeoJSON
    geojson = create_geojson(places, tour, args.return_to_start)
    save_geojson(geojson)
    print("Route written to route.geojson")

if __name__ == "__main__":
    main()
