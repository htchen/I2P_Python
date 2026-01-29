#!/usr/bin/env python3
"""
Week 10 Lab: The "Traveling Salesperson" (Graph Theory Lite) - Starter Code

Complete the exercises by implementing the functions marked with
'# YOUR CODE HERE'. Run this file to test your implementations.

Usage:
    python week10_starter.py              # Run all tests
    python week10_starter.py --test ex1   # Run Exercise 1 tests only
"""

import math
from itertools import permutations
from typing import List, Dict, Any, Tuple, Optional
import sys
import time


# =============================================================================
# SAMPLE DATA
# =============================================================================

def get_sample_distance_matrix() -> List[List[float]]:
    """
    Return sample distance matrix (walking time in minutes).

    Locations:
        0 = Home (Start)
        1 = Pizza Palace
        2 = Burger Barn
        3 = Taco Town
    """
    return [
        [0,   5,  10,  15],  # From Home
        [5,   0,   8,   7],  # From Pizza Palace
        [10,  8,   0,   6],  # From Burger Barn
        [15,  7,   6,   0],  # From Taco Town
    ]


def get_sample_places() -> List[Dict[str, Any]]:
    """Return sample place data with coordinates."""
    return [
        {"name": "Home", "lat": 25.033, "lon": 121.565},
        {"name": "Pizza Palace", "lat": 25.038, "lon": 121.568},
        {"name": "Burger Barn", "lat": 25.030, "lon": 121.560},
        {"name": "Taco Town", "lat": 25.035, "lon": 121.570},
    ]


def get_larger_distance_matrix() -> List[List[float]]:
    """Return larger distance matrix for testing."""
    return [
        [0,   5,  10,  15,  20],
        [5,   0,   8,   7,  14],
        [10,  8,   0,   6,  11],
        [15,  7,   6,   0,   5],
        [20, 14,  11,   5,   0],
    ]


# =============================================================================
# EXERCISE 1: DISTANCE MATRIX OPERATIONS
# =============================================================================

def get_distance(from_node: int, to_node: int, distance_matrix: List[List[float]]) -> float:
    """
    Get distance between two nodes from the matrix.

    Args:
        from_node: Starting node index
        to_node: Destination node index
        distance_matrix: 2D distance matrix

    Returns:
        Distance from from_node to to_node
    """
    # YOUR CODE HERE
    return distance_matrix[from_node][to_node]


def calculate_route_distance(route: List[int], distance_matrix: List[List[float]]) -> float:
    """
    Calculate total distance for a route.

    Args:
        route: List of node indices [start, node1, node2, ...]
        distance_matrix: 2D distance matrix

    Returns:
        Total distance of the route
    """
    # YOUR CODE HERE
    total = 0
    for i in range(len(route) - 1):
        total += distance_matrix[route[i]][route[i + 1]]
    return total


# =============================================================================
# EXERCISE 2: PERMUTATIONS
# =============================================================================

def count_permutations(n: int) -> int:
    """
    Count the number of permutations for n items.

    Args:
        n: Number of items

    Returns:
        Number of permutations (n!)
    """
    # YOUR CODE HERE
    return math.factorial(n)


def get_all_routes(start: int, places_to_visit: List[int]) -> List[List[int]]:
    """
    Generate all possible routes from start through all places.

    Args:
        start: Starting node index
        places_to_visit: List of node indices to visit

    Returns:
        List of all possible routes
    """
    # YOUR CODE HERE
    routes = []
    for perm in permutations(places_to_visit):
        route = [start] + list(perm)
        routes.append(route)
    return routes


# =============================================================================
# EXERCISE 3: BRUTE FORCE TSP
# =============================================================================

def find_optimal_route(
    start: int,
    places_to_visit: List[int],
    distance_matrix: List[List[float]]
) -> Tuple[List[int], float]:
    """
    Find the optimal route using brute force.

    Args:
        start: Starting node index
        places_to_visit: List of node indices to visit
        distance_matrix: 2D distance matrix

    Returns:
        Tuple of (best_route, best_distance)
    """
    # YOUR CODE HERE
    best_route = None
    best_distance = float('inf')

    for perm in permutations(places_to_visit):
        route = [start] + list(perm)
        distance = calculate_route_distance(route, distance_matrix)

        if distance < best_distance:
            best_distance = distance
            best_route = route

    return best_route, best_distance


def find_optimal_round_trip(
    start: int,
    places_to_visit: List[int],
    distance_matrix: List[List[float]]
) -> Tuple[List[int], float]:
    """
    Find optimal route that returns to start.

    Args:
        start: Starting node index
        places_to_visit: List of node indices to visit
        distance_matrix: 2D distance matrix

    Returns:
        Tuple of (best_route, best_distance)
    """
    # YOUR CODE HERE
    best_route = None
    best_distance = float('inf')

    for perm in permutations(places_to_visit):
        route = [start] + list(perm) + [start]
        distance = calculate_route_distance(route, distance_matrix)

        if distance < best_distance:
            best_distance = distance
            best_route = route

    return best_route, best_distance


# =============================================================================
# EXERCISE 4: BUILDING DISTANCE MATRICES
# =============================================================================

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance in km between two coordinates using Haversine formula.

    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates

    Returns:
        Distance in kilometers
    """
    # YOUR CODE HERE
    R = 6371  # Earth's radius in km

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = lat2_rad - lat1_rad
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def build_distance_matrix(
    places: List[Dict[str, Any]],
    walking_speed_kmh: float = 5.0
) -> List[List[float]]:
    """
    Build distance matrix from place coordinates.

    Args:
        places: List of dicts with 'lat' and 'lon' keys
        walking_speed_kmh: Walking speed (default 5 km/h)

    Returns:
        2D matrix of walking times in minutes
    """
    # YOUR CODE HERE
    n = len(places)
    matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                dist_km = haversine_distance(
                    places[i]["lat"], places[i]["lon"],
                    places[j]["lat"], places[j]["lon"]
                )
                time_min = (dist_km / walking_speed_kmh) * 60
                matrix[i][j] = round(time_min, 1)

    return matrix


# =============================================================================
# EXERCISE 5: RESTAURANT TOUR PLANNER
# =============================================================================

class RestaurantTourPlanner:
    """Plan optimal routes to visit multiple restaurants."""

    def __init__(self, start_location: Dict[str, Any]):
        """
        Initialize with starting location.

        Args:
            start_location: Dict with 'name', 'lat', 'lon'
        """
        self.start = start_location
        self.restaurants: List[Dict[str, Any]] = []
        self._matrix: Optional[List[List[float]]] = None

    def add_restaurant(self, restaurant: Dict[str, Any]) -> None:
        """Add a restaurant to visit."""
        # YOUR CODE HERE
        self.restaurants.append(restaurant)
        self._matrix = None  # Invalidate cache

    def _build_matrix(self) -> List[List[float]]:
        """Build distance matrix from all locations."""
        # YOUR CODE HERE
        all_places = [self.start] + self.restaurants
        return build_distance_matrix(all_places)

    def _get_matrix(self) -> List[List[float]]:
        """Get or build cached distance matrix."""
        if self._matrix is None:
            self._matrix = self._build_matrix()
        return self._matrix

    def find_optimal_route(self) -> Dict[str, Any]:
        """
        Find optimal route visiting all restaurants.

        Returns:
            Dict with 'route' (list of names), 'time' (total minutes)
        """
        # YOUR CODE HERE
        if not self.restaurants:
            return {"route": [self.start["name"]], "time": 0}

        matrix = self._get_matrix()
        all_places = [self.start] + self.restaurants
        places_to_visit = list(range(1, len(all_places)))

        best_route, best_time = find_optimal_route(0, places_to_visit, matrix)

        return {
            "route": [all_places[i]["name"] for i in best_route],
            "time": round(best_time, 1)
        }

    def compare_all_routes(self) -> List[Dict[str, Any]]:
        """
        Get all routes sorted by distance.

        Returns:
            List of dicts with 'route' and 'time', sorted by time
        """
        # YOUR CODE HERE
        if not self.restaurants:
            return [{"route": [self.start["name"]], "time": 0}]

        matrix = self._get_matrix()
        all_places = [self.start] + self.restaurants
        places_to_visit = list(range(1, len(all_places)))

        results = []
        for perm in permutations(places_to_visit):
            route = [0] + list(perm)
            time = calculate_route_distance(route, matrix)
            results.append({
                "route": [all_places[i]["name"] for i in route],
                "time": round(time, 1)
            })

        return sorted(results, key=lambda x: x["time"])


# =============================================================================
# EXERCISE 6: NEAREST NEIGHBOR HEURISTIC
# =============================================================================

def nearest_neighbor_route(
    start: int,
    places_to_visit: List[int],
    distance_matrix: List[List[float]]
) -> Tuple[List[int], float]:
    """
    Find route using nearest neighbor heuristic.

    Algorithm:
    1. Start at 'start'
    2. While there are unvisited places:
       a. Find the nearest unvisited place
       b. Go there
       c. Mark as visited
    3. Return the route

    Args:
        start: Starting node index
        places_to_visit: List of nodes to visit
        distance_matrix: 2D distance matrix

    Returns:
        Tuple of (route, total_distance)
    """
    # YOUR CODE HERE
    route = [start]
    unvisited = set(places_to_visit)
    current = start
    total = 0

    while unvisited:
        # Find nearest unvisited
        nearest = min(unvisited, key=lambda x: distance_matrix[current][x])

        # Move to nearest
        total += distance_matrix[current][nearest]
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    return route, total


# =============================================================================
# EXERCISE 7: PERFORMANCE ANALYSIS
# =============================================================================

def benchmark_brute_force(max_n: int = 9) -> List[Dict[str, Any]]:
    """
    Benchmark brute force for different problem sizes.

    Args:
        max_n: Maximum number of locations to test

    Returns:
        List of benchmark results
    """
    results = []

    for n in range(3, max_n + 1):
        # Create dummy matrix
        matrix = [[abs(i - j) + 1 for j in range(n)] for i in range(n)]
        for i in range(n):
            matrix[i][i] = 0

        places = list(range(1, n))

        # Time the search
        start_time = time.time()
        route, dist = find_optimal_route(0, places, matrix)
        elapsed = time.time() - start_time

        results.append({
            "n": n,
            "permutations": math.factorial(n - 1),
            "time_seconds": elapsed,
            "route": route,
            "distance": dist
        })

    return results


# =============================================================================
# BONUS: ROUTE VISUALIZATION
# =============================================================================

def visualize_route(
    route: List[int],
    places: List[Dict[str, Any]],
    distance_matrix: List[List[float]]
) -> str:
    """
    Create ASCII visualization of route.

    Args:
        route: List of node indices
        places: List of place dictionaries with 'name' key
        distance_matrix: 2D distance matrix

    Returns:
        ASCII art string
    """
    lines = []

    for i in range(len(route) - 1):
        from_idx = route[i]
        to_idx = route[i + 1]
        from_name = places[from_idx]["name"]
        time = distance_matrix[from_idx][to_idx]

        lines.append(f"  {from_name}")
        lines.append("    │")
        lines.append(f"    │ {time} min")
        lines.append("    ▼")

    lines.append(f"  {places[route[-1]]['name']}")

    return "\n".join(lines)


# =============================================================================
# TESTS
# =============================================================================

def test_exercise1():
    """Test Exercise 1: Distance Matrix Operations"""
    print("\n" + "=" * 50)
    print("Testing Exercise 1: Distance Matrix Operations")
    print("=" * 50)

    matrix = get_sample_distance_matrix()

    # Test get_distance
    assert get_distance(0, 1, matrix) == 5
    assert get_distance(1, 2, matrix) == 8
    assert get_distance(2, 3, matrix) == 6
    print("  [PASS] get_distance")

    # Test calculate_route_distance
    assert calculate_route_distance([0, 1, 2, 3], matrix) == 19  # 5 + 8 + 6
    assert calculate_route_distance([0, 1, 3, 2], matrix) == 18  # 5 + 7 + 6
    assert calculate_route_distance([0, 3, 2, 1], matrix) == 29  # 15 + 6 + 8
    print("  [PASS] calculate_route_distance")

    print("\nExercise 1: All tests passed!")


def test_exercise2():
    """Test Exercise 2: Permutations"""
    print("\n" + "=" * 50)
    print("Testing Exercise 2: Permutations")
    print("=" * 50)

    # Test count_permutations
    assert count_permutations(3) == 6
    assert count_permutations(4) == 24
    assert count_permutations(5) == 120
    print("  [PASS] count_permutations")

    # Test get_all_routes
    routes = get_all_routes(0, [1, 2])
    assert len(routes) == 2
    assert [0, 1, 2] in routes
    assert [0, 2, 1] in routes
    print("  [PASS] get_all_routes (2 places)")

    routes = get_all_routes(0, [1, 2, 3])
    assert len(routes) == 6
    print("  [PASS] get_all_routes (3 places)")

    print("\nExercise 2: All tests passed!")


def test_exercise3():
    """Test Exercise 3: Brute Force TSP"""
    print("\n" + "=" * 50)
    print("Testing Exercise 3: Brute Force TSP")
    print("=" * 50)

    matrix = get_sample_distance_matrix()

    # Test find_optimal_route
    route, dist = find_optimal_route(0, [1, 2, 3], matrix)
    assert dist == 18  # Optimal: 0 -> 1 -> 3 -> 2 (5 + 7 + 6 = 18)
    assert route[0] == 0  # Starts at 0
    assert set(route) == {0, 1, 2, 3}  # Visits all
    print("  [PASS] find_optimal_route")

    # Test find_optimal_round_trip
    route_rt, dist_rt = find_optimal_round_trip(0, [1, 2, 3], matrix)
    assert route_rt[0] == 0 and route_rt[-1] == 0  # Starts and ends at 0
    print("  [PASS] find_optimal_round_trip")

    print("\nExercise 3: All tests passed!")


def test_exercise4():
    """Test Exercise 4: Building Distance Matrices"""
    print("\n" + "=" * 50)
    print("Testing Exercise 4: Building Distance Matrices")
    print("=" * 50)

    # Test haversine_distance
    dist = haversine_distance(25.033, 121.565, 25.038, 121.568)
    assert 0.5 < dist < 1.0  # Should be ~0.6 km
    print("  [PASS] haversine_distance")

    # Test build_distance_matrix
    places = get_sample_places()
    matrix = build_distance_matrix(places)
    assert len(matrix) == 4
    assert len(matrix[0]) == 4
    assert matrix[0][0] == 0  # Distance to self
    assert matrix[0][1] > 0  # Distance between places
    assert abs(matrix[0][1] - matrix[1][0]) < 0.01  # Symmetric
    print("  [PASS] build_distance_matrix")

    print("\nExercise 4: All tests passed!")


def test_exercise5():
    """Test Exercise 5: Restaurant Tour Planner"""
    print("\n" + "=" * 50)
    print("Testing Exercise 5: Restaurant Tour Planner")
    print("=" * 50)

    planner = RestaurantTourPlanner({
        "name": "Home",
        "lat": 25.033,
        "lon": 121.565
    })

    # Test empty
    result = planner.find_optimal_route()
    assert result["route"] == ["Home"]
    assert result["time"] == 0
    print("  [PASS] Empty planner")

    # Add restaurants
    planner.add_restaurant({"name": "Pizza", "lat": 25.038, "lon": 121.568})
    planner.add_restaurant({"name": "Burger", "lat": 25.030, "lon": 121.560})

    # Test with restaurants
    result = planner.find_optimal_route()
    assert len(result["route"]) == 3
    assert result["route"][0] == "Home"
    assert result["time"] > 0
    print("  [PASS] find_optimal_route")

    # Test compare_all_routes
    all_routes = planner.compare_all_routes()
    assert len(all_routes) == 2  # 2! = 2 permutations
    assert all_routes[0]["time"] <= all_routes[-1]["time"]  # Sorted
    print("  [PASS] compare_all_routes")

    print("\nExercise 5: All tests passed!")


def test_exercise6():
    """Test Exercise 6: Nearest Neighbor"""
    print("\n" + "=" * 50)
    print("Testing Exercise 6: Nearest Neighbor")
    print("=" * 50)

    matrix = get_sample_distance_matrix()

    # Test nearest_neighbor_route
    route, dist = nearest_neighbor_route(0, [1, 2, 3], matrix)
    assert route[0] == 0
    assert set(route) == {0, 1, 2, 3}
    assert dist > 0
    print("  [PASS] nearest_neighbor_route")

    # Compare with brute force
    bf_route, bf_dist = find_optimal_route(0, [1, 2, 3], matrix)
    print(f"  Nearest Neighbor: {route} = {dist}")
    print(f"  Brute Force:      {bf_route} = {bf_dist}")

    if dist == bf_dist:
        print("  [INFO] Nearest neighbor found optimal!")
    else:
        print(f"  [INFO] Nearest neighbor is {dist - bf_dist} longer")

    print("\nExercise 6: All tests passed!")


def test_exercise7():
    """Test Exercise 7: Performance Analysis"""
    print("\n" + "=" * 50)
    print("Testing Exercise 7: Performance Analysis")
    print("=" * 50)

    results = benchmark_brute_force(7)

    print("\n  Benchmark Results:")
    print(f"  {'N':>4} | {'Perms':>8} | {'Time':>10}")
    print("  " + "-" * 30)

    for r in results:
        print(f"  {r['n']:>4} | {r['permutations']:>8} | {r['time_seconds']:>8.4f}s")

    # Verify results are valid
    for r in results:
        assert r["time_seconds"] >= 0
        assert r["permutations"] == math.factorial(r["n"] - 1)

    print("\n  [PASS] benchmark_brute_force")

    print("\nExercise 7: All tests passed!")


def test_bonus():
    """Test Bonus: Route Visualization"""
    print("\n" + "=" * 50)
    print("Testing Bonus: Route Visualization")
    print("=" * 50)

    matrix = get_sample_distance_matrix()
    places = [
        {"name": "Home"},
        {"name": "Pizza"},
        {"name": "Burger"},
        {"name": "Taco"},
    ]

    viz = visualize_route([0, 1, 3, 2], places, matrix)
    assert "Home" in viz
    assert "Pizza" in viz
    assert "5" in viz  # Distance from Home to Pizza

    print("  Route Visualization:")
    for line in viz.split("\n"):
        print(f"    {line}")

    print("\n  [PASS] visualize_route")

    print("\nBonus: All tests passed!")


def run_all_tests():
    """Run all test functions."""
    test_functions = [
        ("Exercise 1", test_exercise1),
        ("Exercise 2", test_exercise2),
        ("Exercise 3", test_exercise3),
        ("Exercise 4", test_exercise4),
        ("Exercise 5", test_exercise5),
        ("Exercise 6", test_exercise6),
        ("Exercise 7", test_exercise7),
        ("Bonus", test_bonus),
    ]

    print("\n" + "=" * 60)
    print("WEEK 10 LAB: TRAVELING SALESPERSON PROBLEM")
    print("Running All Tests")
    print("=" * 60)

    passed = 0
    failed = 0

    for name, test_func in test_functions:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n[FAILED] {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"\n[ERROR] {name}: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            if len(sys.argv) > 2:
                test_name = sys.argv[2].lower()
                test_map = {
                    "ex1": test_exercise1,
                    "ex2": test_exercise2,
                    "ex3": test_exercise3,
                    "ex4": test_exercise4,
                    "ex5": test_exercise5,
                    "ex6": test_exercise6,
                    "ex7": test_exercise7,
                    "bonus": test_bonus,
                }
                if test_name in test_map:
                    test_map[test_name]()
                else:
                    print(f"Unknown test: {test_name}")
                    print(f"Available: {', '.join(test_map.keys())}")
            else:
                run_all_tests()
        else:
            print("Usage:")
            print("  python week10_starter.py              # Run all tests")
            print("  python week10_starter.py --test ex1   # Run specific test")
    else:
        run_all_tests()


if __name__ == "__main__":
    main()
