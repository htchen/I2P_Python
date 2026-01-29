#!/usr/bin/env python3
"""
Week 10: The "Traveling Salesperson" (Graph Theory Lite) - Interactive Examples

This module demonstrates:
- Graph representation with adjacency matrices
- Permutations and factorial growth
- Brute force algorithm for TSP
- Route optimization for restaurant tours
- Integration concepts with real distance calculations

Run this file to see all examples in action:
    python examples.py

Or run with interactive menu:
    python examples.py --interactive
"""

from itertools import permutations
from typing import List, Dict, Any, Tuple, Optional
import math
import time


# =============================================================================
# SECTION 1: SAMPLE DATA
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
        {"name": "🏠 Home", "lat": 25.033, "lon": 121.565},
        {"name": "🍕 Pizza Palace", "lat": 25.038, "lon": 121.568},
        {"name": "🍔 Burger Barn", "lat": 25.030, "lon": 121.560},
        {"name": "🌮 Taco Town", "lat": 25.035, "lon": 121.570},
    ]


def get_larger_distance_matrix() -> List[List[float]]:
    """Return a larger distance matrix for benchmarking."""
    return [
        [0,  5, 10, 15, 20, 12],
        [5,  0,  8,  7, 14, 10],
        [10, 8,  0,  6, 11,  9],
        [15, 7,  6,  0,  5, 13],
        [20, 14, 11, 5,  0,  8],
        [12, 10, 9, 13,  8,  0],
    ]


# =============================================================================
# SECTION 2: BASIC GRAPH OPERATIONS
# =============================================================================

def calculate_route_distance(route: List[int], distance_matrix: List[List[float]]) -> float:
    """
    Calculate total distance for a route.

    Args:
        route: List of node indices representing the path
        distance_matrix: 2D matrix of distances between nodes

    Returns:
        Total distance of the route
    """
    total = 0
    for i in range(len(route) - 1):
        from_node = route[i]
        to_node = route[i + 1]
        total += distance_matrix[from_node][to_node]
    return total


def demo_adjacency_matrix():
    """Demonstrate adjacency matrix representation."""
    print("\n" + "=" * 60)
    print("DEMO: Adjacency Matrix Representation")
    print("=" * 60)

    matrix = get_sample_distance_matrix()
    places = get_sample_places()

    print("\nDistance Matrix (walking time in minutes):")
    print("\n       ", end="")
    for i, p in enumerate(places):
        print(f"{i:>8}", end="")
    print()

    for i, row in enumerate(matrix):
        print(f"  {i} [{places[i]['name'][:6]:>6}]", end="")
        for val in row:
            print(f"{val:>8}", end="")
        print()

    print("\nReading the matrix:")
    print(f"  Home → Pizza:  matrix[0][1] = {matrix[0][1]} min")
    print(f"  Pizza → Burger: matrix[1][2] = {matrix[1][2]} min")
    print(f"  Burger → Taco:  matrix[2][3] = {matrix[2][3]} min")
    print(f"  Taco → Home:    matrix[3][0] = {matrix[3][0]} min")


def demo_route_distance():
    """Demonstrate route distance calculation."""
    print("\n" + "=" * 60)
    print("DEMO: Route Distance Calculation")
    print("=" * 60)

    matrix = get_sample_distance_matrix()
    places = get_sample_places()

    routes = [
        [0, 1, 2, 3],  # Home → Pizza → Burger → Taco
        [0, 1, 3, 2],  # Home → Pizza → Taco → Burger
        [0, 2, 1, 3],  # Home → Burger → Pizza → Taco
        [0, 2, 3, 1],  # Home → Burger → Taco → Pizza
        [0, 3, 1, 2],  # Home → Taco → Pizza → Burger
        [0, 3, 2, 1],  # Home → Taco → Burger → Pizza
    ]

    print("\nAll possible routes from Home visiting all restaurants:")
    print("-" * 60)

    results = []
    for route in routes:
        distance = calculate_route_distance(route, matrix)
        route_str = " → ".join(places[i]["name"] for i in route)
        results.append((distance, route_str, route))

        # Show calculation
        steps = []
        for i in range(len(route) - 1):
            steps.append(f"{route[i]}→{route[i+1]}({matrix[route[i]][route[i+1]]})")
        calc = " + ".join(steps)
        print(f"  {route_str}")
        print(f"    Calculation: {calc} = {distance} min")
        print()

    # Sort and show ranking
    results.sort(key=lambda x: x[0])
    print("\nRoutes Ranked by Distance:")
    print("-" * 60)
    for i, (dist, route_str, _) in enumerate(results, 1):
        marker = " 👑 BEST!" if i == 1 else ""
        print(f"  {i}. {dist:>2} min: {route_str}{marker}")


# =============================================================================
# SECTION 3: PERMUTATIONS
# =============================================================================

def demo_permutations():
    """Demonstrate permutation generation."""
    print("\n" + "=" * 60)
    print("DEMO: Permutations")
    print("=" * 60)

    # Simple example with letters
    print("\n--- Permutations of ['A', 'B', 'C'] ---")
    items = ['A', 'B', 'C']
    for i, perm in enumerate(permutations(items), 1):
        print(f"  {i}. {perm}")
    print(f"\nTotal: {math.factorial(len(items))} permutations (3! = 3×2×1 = 6)")

    # With numbers (indices)
    print("\n--- Permutations of Places to Visit [1, 2, 3] ---")
    places = get_sample_places()
    places_to_visit = [1, 2, 3]

    for i, perm in enumerate(permutations(places_to_visit), 1):
        route = [0] + list(perm)
        route_str = " → ".join(places[j]["name"] for j in route)
        print(f"  {i}. Indices: {route} → {route_str}")


def demo_factorial_growth():
    """Demonstrate factorial growth."""
    print("\n" + "=" * 60)
    print("DEMO: Factorial Growth")
    print("=" * 60)

    print("\n  N   |        N!        | Time to check all (1μs each)")
    print("-" * 60)

    for n in range(1, 16):
        factorial = math.factorial(n)
        time_us = factorial  # microseconds
        time_s = time_us / 1_000_000
        time_min = time_s / 60
        time_hr = time_min / 60
        time_day = time_hr / 24
        time_yr = time_day / 365

        if time_s < 1:
            time_str = f"{time_us:>12,} μs"
        elif time_s < 60:
            time_str = f"{time_s:>12.2f} sec"
        elif time_min < 60:
            time_str = f"{time_min:>12.2f} min"
        elif time_hr < 24:
            time_str = f"{time_hr:>12.2f} hours"
        elif time_day < 365:
            time_str = f"{time_day:>12.1f} days"
        else:
            time_str = f"{time_yr:>12.1f} years"

        print(f"  {n:>2}  | {factorial:>16,} | {time_str}")

    print("\n📌 For our restaurant finder (3-5 places): Brute force is perfect!")
    print("   3 places = 6 routes, 5 places = 120 routes → instant!")


# =============================================================================
# SECTION 4: BRUTE FORCE TSP
# =============================================================================

def find_optimal_route_brute_force(
    start: int,
    places_to_visit: List[int],
    distance_matrix: List[List[float]],
    verbose: bool = False
) -> Tuple[List[int], float]:
    """
    Find optimal route using brute force.

    Args:
        start: Index of starting location
        places_to_visit: List of indices to visit
        distance_matrix: 2D distance matrix
        verbose: If True, print each permutation checked

    Returns:
        Tuple of (best_route, best_distance)
    """
    best_route = None
    best_distance = float('inf')
    checked = 0

    for perm in permutations(places_to_visit):
        route = [start] + list(perm)
        distance = calculate_route_distance(route, distance_matrix)
        checked += 1

        if verbose:
            status = "✓ NEW BEST" if distance < best_distance else ""
            print(f"  Checking {route}: {distance} min {status}")

        if distance < best_distance:
            best_distance = distance
            best_route = route

    if verbose:
        print(f"\nTotal routes checked: {checked}")

    return best_route, best_distance


def demo_brute_force():
    """Demonstrate brute force TSP algorithm."""
    print("\n" + "=" * 60)
    print("DEMO: Brute Force TSP Algorithm")
    print("=" * 60)

    matrix = get_sample_distance_matrix()
    places = get_sample_places()

    print("\nSearching for optimal route...")
    print("-" * 40)

    route, distance = find_optimal_route_brute_force(
        start=0,
        places_to_visit=[1, 2, 3],
        distance_matrix=matrix,
        verbose=True
    )

    print("\n" + "=" * 40)
    route_str = " → ".join(places[i]["name"] for i in route)
    print(f"🏆 OPTIMAL ROUTE: {route_str}")
    print(f"   Total time: {distance} minutes")


def find_optimal_round_trip(
    start: int,
    places_to_visit: List[int],
    distance_matrix: List[List[float]]
) -> Tuple[List[int], float]:
    """Find optimal route that returns to start."""
    best_route = None
    best_distance = float('inf')

    for perm in permutations(places_to_visit):
        route = [start] + list(perm) + [start]
        distance = calculate_route_distance(route, distance_matrix)

        if distance < best_distance:
            best_distance = distance
            best_route = route

    return best_route, best_distance


def demo_round_trip():
    """Demonstrate round-trip route optimization."""
    print("\n" + "=" * 60)
    print("DEMO: Round-Trip Routes")
    print("=" * 60)

    matrix = get_sample_distance_matrix()
    places = get_sample_places()

    # One-way trip
    one_way_route, one_way_dist = find_optimal_route_brute_force(
        0, [1, 2, 3], matrix
    )

    # Round trip
    round_trip_route, round_trip_dist = find_optimal_round_trip(
        0, [1, 2, 3], matrix
    )

    print("\n--- One-Way Trip ---")
    route_str = " → ".join(places[i]["name"] for i in one_way_route)
    print(f"  Route: {route_str}")
    print(f"  Distance: {one_way_dist} minutes")

    print("\n--- Round Trip (return home) ---")
    route_str = " → ".join(places[i]["name"] for i in round_trip_route)
    print(f"  Route: {route_str}")
    print(f"  Distance: {round_trip_dist} minutes")


# =============================================================================
# SECTION 5: BENCHMARKING
# =============================================================================

def demo_benchmark():
    """Benchmark brute force algorithm."""
    print("\n" + "=" * 60)
    print("DEMO: Brute Force Benchmark")
    print("=" * 60)

    print("\nBenchmarking brute force TSP for different N values...")
    print("-" * 60)
    print(f"{'N':>4} | {'Permutations':>12} | {'Time':>12} | {'Per Route':>12}")
    print("-" * 60)

    for n in range(3, 11):
        # Create dummy distance matrix
        matrix = [[abs(i - j) + 1 for j in range(n)] for i in range(n)]
        for i in range(n):
            matrix[i][i] = 0

        places_to_visit = list(range(1, n))

        start_time = time.time()
        route, dist = find_optimal_route_brute_force(0, places_to_visit, matrix)
        elapsed = time.time() - start_time

        num_perms = math.factorial(n - 1)
        per_route = elapsed / num_perms * 1_000_000  # microseconds

        print(f"{n:>4} | {num_perms:>12,} | {elapsed:>10.4f}s | {per_route:>10.2f}μs")

    print("-" * 60)
    print("\n📌 For N ≤ 10, brute force completes in under a second!")


# =============================================================================
# SECTION 6: HAVERSINE DISTANCE
# =============================================================================

def haversine_distance(p1: Dict[str, Any], p2: Dict[str, Any]) -> float:
    """
    Calculate distance in km between two points using Haversine formula.

    Args:
        p1: First place with 'lat' and 'lon' keys
        p2: Second place with 'lat' and 'lon' keys

    Returns:
        Distance in kilometers
    """
    R = 6371  # Earth's radius in km

    lat1 = math.radians(p1["lat"])
    lat2 = math.radians(p2["lat"])
    dlat = lat2 - lat1
    dlon = math.radians(p2["lon"] - p1["lon"])

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def build_distance_matrix_from_places(
    places: List[Dict[str, Any]],
    walking_speed_kmh: float = 5.0
) -> List[List[float]]:
    """
    Build distance matrix from places using Haversine formula.

    Args:
        places: List of places with lat/lon coordinates
        walking_speed_kmh: Walking speed in km/h (default 5 km/h)

    Returns:
        2D matrix of walking times in minutes
    """
    n = len(places)
    matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                dist_km = haversine_distance(places[i], places[j])
                time_min = (dist_km / walking_speed_kmh) * 60
                matrix[i][j] = round(time_min, 1)

    return matrix


def demo_haversine():
    """Demonstrate building distance matrix from coordinates."""
    print("\n" + "=" * 60)
    print("DEMO: Building Distance Matrix from Coordinates")
    print("=" * 60)

    places = get_sample_places()

    print("\nPlaces with coordinates:")
    for i, p in enumerate(places):
        print(f"  {i}. {p['name']}: ({p['lat']}, {p['lon']})")

    matrix = build_distance_matrix_from_places(places)

    print("\nCalculated walking times (minutes, assuming 5 km/h):")
    print("\n       ", end="")
    for i in range(len(places)):
        print(f"{i:>8}", end="")
    print()

    for i, row in enumerate(matrix):
        print(f"  {i}    ", end="")
        for val in row:
            print(f"{val:>8.1f}", end="")
        print()

    # Find optimal route
    route, dist = find_optimal_route_brute_force(0, [1, 2, 3], matrix)
    route_str = " → ".join(places[i]["name"] for i in route)
    print(f"\nOptimal route: {route_str}")
    print(f"Total time: {dist:.1f} minutes")


# =============================================================================
# SECTION 7: NEAREST NEIGHBOR HEURISTIC
# =============================================================================

def nearest_neighbor_route(
    start: int,
    places_to_visit: List[int],
    distance_matrix: List[List[float]]
) -> Tuple[List[int], float]:
    """
    Find route using nearest neighbor heuristic (greedy approach).

    This is faster but NOT guaranteed to find the optimal solution.

    Args:
        start: Starting node index
        places_to_visit: List of nodes to visit
        distance_matrix: 2D distance matrix

    Returns:
        Tuple of (route, total_distance)
    """
    route = [start]
    unvisited = set(places_to_visit)
    current = start
    total = 0

    while unvisited:
        # Find nearest unvisited node
        nearest = min(unvisited, key=lambda x: distance_matrix[current][x])

        # Move to nearest
        total += distance_matrix[current][nearest]
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    return route, total


def demo_nearest_neighbor():
    """Compare nearest neighbor with brute force."""
    print("\n" + "=" * 60)
    print("DEMO: Nearest Neighbor vs Brute Force")
    print("=" * 60)

    matrix = get_sample_distance_matrix()
    places = get_sample_places()

    print("\n--- Nearest Neighbor (Greedy) ---")
    nn_route, nn_dist = nearest_neighbor_route(0, [1, 2, 3], matrix)
    nn_route_str = " → ".join(places[i]["name"] for i in nn_route)
    print(f"  Route: {nn_route_str}")
    print(f"  Distance: {nn_dist} minutes")
    print("  Time complexity: O(N²)")

    print("\n--- Brute Force (Optimal) ---")
    bf_route, bf_dist = find_optimal_route_brute_force(0, [1, 2, 3], matrix)
    bf_route_str = " → ".join(places[i]["name"] for i in bf_route)
    print(f"  Route: {bf_route_str}")
    print(f"  Distance: {bf_dist} minutes")
    print("  Time complexity: O(N! × N)")

    print("\n--- Comparison ---")
    if nn_dist == bf_dist:
        print("  ✓ Nearest neighbor found the optimal solution!")
    else:
        diff = nn_dist - bf_dist
        pct = (diff / bf_dist) * 100
        print(f"  ⚠ Nearest neighbor is {diff} min ({pct:.1f}%) longer than optimal")

    # Larger example where nearest neighbor might fail
    print("\n--- Larger Example (6 locations) ---")
    large_matrix = get_larger_distance_matrix()
    large_places = [
        {"name": "Start"},
        {"name": "A"},
        {"name": "B"},
        {"name": "C"},
        {"name": "D"},
        {"name": "E"},
    ]

    nn_route2, nn_dist2 = nearest_neighbor_route(0, [1, 2, 3, 4, 5], large_matrix)
    bf_route2, bf_dist2 = find_optimal_route_brute_force(0, [1, 2, 3, 4, 5], large_matrix)

    print(f"  Nearest Neighbor: {nn_route2} = {nn_dist2} min")
    print(f"  Brute Force:      {bf_route2} = {bf_dist2} min")

    if nn_dist2 > bf_dist2:
        diff = nn_dist2 - bf_dist2
        print(f"  ⚠ Nearest neighbor is {diff} min longer!")


# =============================================================================
# SECTION 8: COMPLETE RESTAURANT TOUR PLANNER
# =============================================================================

class RestaurantTourPlanner:
    """Plan optimal routes to visit multiple restaurants."""

    def __init__(self, start_location: Dict[str, Any]):
        self.start = start_location
        self.restaurants: List[Dict[str, Any]] = []
        self._matrix: Optional[List[List[float]]] = None

    def add_restaurant(self, restaurant: Dict[str, Any]) -> None:
        """Add a restaurant to the tour."""
        self.restaurants.append(restaurant)
        self._matrix = None

    def _get_matrix(self) -> List[List[float]]:
        """Build or return cached distance matrix."""
        if self._matrix is None:
            all_places = [self.start] + self.restaurants
            self._matrix = build_distance_matrix_from_places(all_places)
        return self._matrix

    def find_optimal_route(self, return_to_start: bool = False) -> Dict[str, Any]:
        """Find the optimal route to visit all restaurants."""
        if not self.restaurants:
            return {"route": [self.start["name"]], "time": 0}

        matrix = self._get_matrix()
        all_places = [self.start] + self.restaurants
        places_to_visit = list(range(1, len(all_places)))

        if return_to_start:
            route, time = find_optimal_round_trip(0, places_to_visit, matrix)
        else:
            route, time = find_optimal_route_brute_force(0, places_to_visit, matrix)

        return {
            "route_indices": route,
            "route_names": [all_places[i]["name"] for i in route],
            "total_time": round(time, 1),
            "num_checked": math.factorial(len(places_to_visit)),
        }

    def visualize_route(self, route_indices: List[int]) -> str:
        """Create ASCII visualization of route."""
        all_places = [self.start] + self.restaurants
        matrix = self._get_matrix()
        lines = []

        for i in range(len(route_indices) - 1):
            from_idx = route_indices[i]
            to_idx = route_indices[i + 1]
            from_name = all_places[from_idx]["name"]
            to_name = all_places[to_idx]["name"]
            time = matrix[from_idx][to_idx]

            lines.append(f"  {from_name}")
            lines.append(f"    │")
            lines.append(f"    │ {time:.1f} min")
            lines.append(f"    ▼")

        lines.append(f"  {all_places[route_indices[-1]]['name']}")

        return "\n".join(lines)


def demo_restaurant_planner():
    """Demonstrate complete restaurant tour planner."""
    print("\n" + "=" * 60)
    print("DEMO: Restaurant Tour Planner")
    print("=" * 60)

    # Create planner
    planner = RestaurantTourPlanner({
        "name": "🏠 Home",
        "lat": 25.033,
        "lon": 121.565
    })

    # Add restaurants
    planner.add_restaurant({"name": "🍕 Pizza Palace", "lat": 25.038, "lon": 121.568})
    planner.add_restaurant({"name": "🍔 Burger Barn", "lat": 25.030, "lon": 121.560})
    planner.add_restaurant({"name": "🌮 Taco Town", "lat": 25.035, "lon": 121.570})

    print("\n--- One-Way Trip ---")
    result = planner.find_optimal_route(return_to_start=False)
    print(f"Optimal Route: {' → '.join(result['route_names'])}")
    print(f"Total Time: {result['total_time']} minutes")
    print(f"Routes Checked: {result['num_checked']}")

    print("\nRoute Visualization:")
    print(planner.visualize_route(result['route_indices']))

    print("\n--- Round Trip ---")
    result_rt = planner.find_optimal_route(return_to_start=True)
    print(f"Optimal Route: {' → '.join(result_rt['route_names'])}")
    print(f"Total Time: {result_rt['total_time']} minutes")


# =============================================================================
# MAIN - RUN ALL DEMOS
# =============================================================================

def run_all_demos():
    """Run all demonstration functions."""
    demos = [
        ("Adjacency Matrix", demo_adjacency_matrix),
        ("Route Distance", demo_route_distance),
        ("Permutations", demo_permutations),
        ("Factorial Growth", demo_factorial_growth),
        ("Brute Force TSP", demo_brute_force),
        ("Round Trip", demo_round_trip),
        ("Benchmark", demo_benchmark),
        ("Haversine Distance", demo_haversine),
        ("Nearest Neighbor", demo_nearest_neighbor),
        ("Restaurant Planner", demo_restaurant_planner),
    ]

    print("=" * 60)
    print("WEEK 10: TRAVELING SALESPERSON PROBLEM")
    print("Interactive Examples")
    print("=" * 60)

    for name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"\n[ERROR in {name}]: {e}")

    print("\n" + "=" * 60)
    print("All demos completed!")
    print("=" * 60)


def run_interactive_menu():
    """Run interactive menu for selecting demos."""
    demos = {
        "1": ("Adjacency Matrix", demo_adjacency_matrix),
        "2": ("Route Distance", demo_route_distance),
        "3": ("Permutations", demo_permutations),
        "4": ("Factorial Growth", demo_factorial_growth),
        "5": ("Brute Force TSP", demo_brute_force),
        "6": ("Round Trip", demo_round_trip),
        "7": ("Benchmark", demo_benchmark),
        "8": ("Haversine Distance", demo_haversine),
        "9": ("Nearest Neighbor", demo_nearest_neighbor),
        "10": ("Restaurant Planner", demo_restaurant_planner),
        "a": ("Run All Demos", run_all_demos),
    }

    while True:
        print("\n" + "=" * 40)
        print("WEEK 10: TRAVELING SALESPERSON")
        print("=" * 40)
        print("\nSelect a demo:")
        for key, (name, _) in demos.items():
            print(f"  {key}. {name}")
        print("  q. Quit")

        choice = input("\nChoice: ").strip().lower()

        if choice == 'q':
            print("Goodbye!")
            break
        elif choice in demos:
            demos[choice][1]()
            input("\nPress Enter to continue...")
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive_menu()
    else:
        run_all_demos()
