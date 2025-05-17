import unittest
from place import Place
from distance import haversine, build_distance_matrix
from tsp_solver import greedy_solver, two_opt_improve, calculate_tour_distance

class TestTSP(unittest.TestCase):
    def setUp(self):
        # Sample places for testing
        self.places = [
            Place("Eiffel Tower", 48.8584, 2.2945),
            Place("Louvre Museum", 48.8606, 2.3376),
            Place("Notre-Dame", 48.8530, 2.3499),
            Place("Arc de Triomphe", 48.8738, 2.2950)
        ]
        self.dist_matrix = build_distance_matrix(self.places)
    
    def test_haversine(self):
        # Test the haversine distance calculation
        distance = haversine(self.places[0], self.places[1])
        self.assertAlmostEqual(distance, 3.0, delta=0.5)  # Roughly 3 km between Eiffel Tower and Louvre
    
    def test_greedy_solver(self):
        # Test the greedy solver
        tour = greedy_solver(self.dist_matrix, 0)
        self.assertEqual(len(tour), len(self.places))
        self.assertEqual(tour[0], 0)  # Should start at the specified index
        
        # Check that all places are visited exactly once
        self.assertEqual(set(tour), set(range(len(self.places))))
    
    def test_two_opt_improve(self):
        # Test the 2-opt improvement
        initial_tour = list(range(len(self.places)))
        improved_tour = two_opt_improve(initial_tour, self.dist_matrix)
        
        # The improved tour should have the same places
        self.assertEqual(set(improved_tour), set(initial_tour))
        
        # The improved tour should be at least as good as the initial tour
        initial_distance = calculate_tour_distance(initial_tour, self.dist_matrix)
        improved_distance = calculate_tour_distance(improved_tour, self.dist_matrix)
        self.assertLessEqual(improved_distance, initial_distance)

if __name__ == '__main__':
    unittest.main()
