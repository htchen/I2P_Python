# Week 10 Lab: The "Traveling Salesperson" (Graph Theory Lite)

## Lab Overview

In this lab, you'll implement route optimization algorithms to find the best order for visiting multiple restaurants. You'll work with graphs, permutations, and brute-force search.

**Time:** 2 hours
**Difficulty:** Intermediate

### Learning Objectives

By completing this lab, you will:
1. Represent distances as adjacency matrices
2. Generate permutations using `itertools.permutations`
3. Implement brute-force TSP algorithm
4. Calculate and compare route distances
5. Build a complete restaurant tour planner
6. Understand algorithm complexity

### Prerequisites

- Week 9: Functional Patterns (map, filter, sorted)
- Understanding of nested lists (2D arrays)
- Basic algorithm concepts

---

## Setup

### Starter Code

Open `week10_starter.py` and review the provided code structure. You'll find:
- Sample distance matrices
- Function stubs to implement
- Test cases to verify your work

### Running Tests

```bash
# Run all tests
python week10_starter.py

# Run specific exercise
python week10_starter.py --test ex1
```

---

## Exercise 1: Distance Matrix Operations (20 minutes)

### Background

An **adjacency matrix** stores distances between all pairs of locations. For N locations, it's an N×N matrix where `matrix[i][j]` is the distance from location i to location j.

### Task 1.1: Read Matrix Values

```python
distance_matrix = [
    [0,   5,  10,  15],  # From location 0
    [5,   0,   8,   7],  # From location 1
    [10,  8,   0,   6],  # From location 2
    [15,  7,   6,   0],  # From location 3
]

# What are these values?
dist_0_to_1 = ???  # Distance from 0 to 1
dist_1_to_2 = ???  # Distance from 1 to 2
dist_2_to_3 = ???  # Distance from 2 to 3
dist_3_to_0 = ???  # Distance from 3 back to 0
```

### Task 1.2: Implement `get_distance`

```python
def get_distance(
    from_node: int,
    to_node: int,
    distance_matrix: list
) -> float:
    """
    Get distance between two nodes from the matrix.

    Args:
        from_node: Starting node index
        to_node: Destination node index
        distance_matrix: 2D distance matrix

    Returns:
        Distance from from_node to to_node

    Example:
        >>> matrix = [[0, 5], [5, 0]]
        >>> get_distance(0, 1, matrix)
        5
    """
    # YOUR CODE HERE
    pass
```

### Task 1.3: Implement `calculate_route_distance`

```python
def calculate_route_distance(
    route: list,
    distance_matrix: list
) -> float:
    """
    Calculate total distance for a route.

    Args:
        route: List of node indices [start, node1, node2, ...]
        distance_matrix: 2D distance matrix

    Returns:
        Total distance of the route

    Example:
        >>> matrix = [[0, 5, 10], [5, 0, 8], [10, 8, 0]]
        >>> calculate_route_distance([0, 1, 2], matrix)
        13  # 0→1 (5) + 1→2 (8) = 13
    """
    # YOUR CODE HERE
    pass
```

---

## Exercise 2: Permutations (20 minutes)

### Background

A **permutation** is a specific ordering of elements. For TSP, we need to try all possible orderings of the places we want to visit.

### Task 2.1: Count Permutations

```python
from math import factorial

# How many permutations for N items?
perm_3 = ???  # 3 items
perm_4 = ???  # 4 items
perm_5 = ???  # 5 items
perm_10 = ???  # 10 items

# Verify with factorial
assert perm_3 == factorial(3)  # Should be 6
assert perm_4 == factorial(4)  # Should be 24
```

### Task 2.2: Generate Permutations

```python
from itertools import permutations

places_to_visit = [1, 2, 3]  # Indices of places (not including start)

# Generate all permutations
all_perms = list(permutations(places_to_visit))

# How many permutations?
num_perms = ???

# What is the 3rd permutation (index 2)?
third_perm = ???

# Print all permutations with route format
for perm in permutations(places_to_visit):
    route = [0] + list(perm)  # Add start (0) to beginning
    print(f"Route: {route}")
```

### Task 2.3: Implement `get_all_routes`

```python
def get_all_routes(
    start: int,
    places_to_visit: list
) -> list:
    """
    Generate all possible routes from start through all places.

    Args:
        start: Starting node index
        places_to_visit: List of node indices to visit

    Returns:
        List of all possible routes

    Example:
        >>> get_all_routes(0, [1, 2])
        [[0, 1, 2], [0, 2, 1]]
    """
    # YOUR CODE HERE
    pass
```

---

## Exercise 3: Brute Force TSP (25 minutes)

### Background

The brute force algorithm tries ALL possible routes and keeps track of the best one found.

### Task 3.1: Implement `find_optimal_route`

```python
def find_optimal_route(
    start: int,
    places_to_visit: list,
    distance_matrix: list
) -> tuple:
    """
    Find the optimal route using brute force.

    Args:
        start: Starting node index
        places_to_visit: List of node indices to visit
        distance_matrix: 2D distance matrix

    Returns:
        Tuple of (best_route, best_distance)

    Example:
        >>> matrix = [[0, 5, 10], [5, 0, 8], [10, 8, 0]]
        >>> route, dist = find_optimal_route(0, [1, 2], matrix)
        >>> route
        [0, 1, 2]
        >>> dist
        13
    """
    # YOUR CODE HERE
    # 1. Initialize best_route = None, best_distance = infinity
    # 2. For each permutation of places_to_visit:
    #    a. Build route: [start] + list(permutation)
    #    b. Calculate distance
    #    c. If better than best, update best
    # 3. Return (best_route, best_distance)
    pass
```

### Task 3.2: Trace the Algorithm

Given this distance matrix:
```python
matrix = [
    [0,  5, 10, 15],
    [5,  0,  8,  7],
    [10, 8,  0,  6],
    [15, 7,  6,  0],
]
```

Manually trace finding the optimal route from 0 visiting [1, 2, 3]:

```
Permutation 1: (1, 2, 3)
  Route: [0, 1, 2, 3]
  Distance: ??? + ??? + ??? = ???
  Best so far: ???

Permutation 2: (1, 3, 2)
  Route: [0, 1, 3, 2]
  Distance: ??? + ??? + ??? = ???
  Better? ???

... continue for all 6 permutations ...

Final answer: Route = ???, Distance = ???
```

### Task 3.3: Implement `find_optimal_round_trip`

```python
def find_optimal_round_trip(
    start: int,
    places_to_visit: list,
    distance_matrix: list
) -> tuple:
    """
    Find optimal route that returns to start.

    Same as find_optimal_route but route ends at start.

    Example:
        >>> matrix = [[0, 5, 10], [5, 0, 8], [10, 8, 0]]
        >>> route, dist = find_optimal_round_trip(0, [1, 2], matrix)
        >>> route
        [0, 1, 2, 0]
    """
    # YOUR CODE HERE
    pass
```

---

## Exercise 4: Building Distance Matrices (20 minutes)

### Background

In real applications, we build distance matrices from coordinates using formulas like Haversine.

### Task 4.1: Implement `haversine_distance`

```python
import math

def haversine_distance(
    lat1: float, lon1: float,
    lat2: float, lon2: float
) -> float:
    """
    Calculate distance in km between two coordinates.

    Uses the Haversine formula for great-circle distance.

    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates

    Returns:
        Distance in kilometers

    Example:
        >>> haversine_distance(25.033, 121.565, 25.038, 121.568)
        0.62  # approximately
    """
    R = 6371  # Earth's radius in km

    # Convert to radians
    lat1, lat2 = math.radians(lat1), math.radians(lat2)
    dlat = lat2 - lat1
    dlon = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c
```

### Task 4.2: Implement `build_distance_matrix`

```python
def build_distance_matrix(
    places: list,
    walking_speed_kmh: float = 5.0
) -> list:
    """
    Build distance matrix from place coordinates.

    Args:
        places: List of dicts with 'lat' and 'lon' keys
        walking_speed_kmh: Walking speed (default 5 km/h)

    Returns:
        2D matrix of walking times in minutes

    Example:
        >>> places = [
        ...     {"lat": 25.0, "lon": 121.5},
        ...     {"lat": 25.1, "lon": 121.6},
        ... ]
        >>> matrix = build_distance_matrix(places)
        >>> matrix[0][0]
        0  # Distance to self
    """
    # YOUR CODE HERE
    # 1. Get number of places (n)
    # 2. Create n×n matrix filled with 0s
    # 3. For each pair (i, j) where i != j:
    #    a. Calculate haversine distance
    #    b. Convert to walking time in minutes
    #    c. Store in matrix[i][j]
    # 4. Return matrix
    pass
```

---

## Exercise 5: Complete Tour Planner (25 minutes)

### Task 5.1: Implement `RestaurantTourPlanner` class

```python
class RestaurantTourPlanner:
    """Plan optimal routes to visit multiple restaurants."""

    def __init__(self, start_location: dict):
        """
        Initialize with starting location.

        Args:
            start_location: Dict with 'name', 'lat', 'lon'
        """
        self.start = start_location
        self.restaurants = []
        self._matrix = None

    def add_restaurant(self, restaurant: dict) -> None:
        """
        Add a restaurant to visit.

        Args:
            restaurant: Dict with 'name', 'lat', 'lon'
        """
        # YOUR CODE HERE
        pass

    def _build_matrix(self) -> list:
        """Build distance matrix from all locations."""
        # YOUR CODE HERE
        # Combine start + restaurants, then build matrix
        pass

    def find_optimal_route(self) -> dict:
        """
        Find optimal route visiting all restaurants.

        Returns:
            Dict with 'route' (list of names), 'time' (total minutes)
        """
        # YOUR CODE HERE
        pass

    def compare_all_routes(self) -> list:
        """
        Get all routes sorted by distance.

        Returns:
            List of dicts with 'route' and 'time', sorted by time
        """
        # YOUR CODE HERE
        pass
```

### Task 5.2: Use the Planner

```python
# Create planner
planner = RestaurantTourPlanner({
    "name": "Home",
    "lat": 25.033,
    "lon": 121.565
})

# Add restaurants
planner.add_restaurant({"name": "Pizza", "lat": 25.038, "lon": 121.568})
planner.add_restaurant({"name": "Burger", "lat": 25.030, "lon": 121.560})
planner.add_restaurant({"name": "Taco", "lat": 25.035, "lon": 121.570})

# Find optimal route
result = planner.find_optimal_route()
print(f"Best route: {' → '.join(result['route'])}")
print(f"Total time: {result['time']:.1f} minutes")

# Compare all routes
all_routes = planner.compare_all_routes()
print("\nAll routes ranked:")
for i, r in enumerate(all_routes, 1):
    print(f"  {i}. {r['time']:.1f} min: {' → '.join(r['route'])}")
```

---

## Exercise 6: Nearest Neighbor Heuristic (15 minutes)

### Background

The **nearest neighbor** algorithm is a greedy approach: always go to the closest unvisited place. It's fast but not guaranteed to find the optimal route.

### Task 6.1: Implement `nearest_neighbor_route`

```python
def nearest_neighbor_route(
    start: int,
    places_to_visit: list,
    distance_matrix: list
) -> tuple:
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

    Example:
        >>> matrix = [[0, 5, 10], [5, 0, 8], [10, 8, 0]]
        >>> route, dist = nearest_neighbor_route(0, [1, 2], matrix)
    """
    # YOUR CODE HERE
    pass
```

### Task 6.2: Compare Algorithms

```python
matrix = [
    [0,   5,  10,  15,  20],
    [5,   0,   8,   7,  14],
    [10,  8,   0,   6,  11],
    [15,  7,   6,   0,   5],
    [20, 14,  11,   5,   0],
]

places_to_visit = [1, 2, 3, 4]

# Brute force (optimal)
bf_route, bf_dist = find_optimal_route(0, places_to_visit, matrix)
print(f"Brute Force: {bf_route} = {bf_dist} min")

# Nearest neighbor (fast)
nn_route, nn_dist = nearest_neighbor_route(0, places_to_visit, matrix)
print(f"Nearest Neighbor: {nn_route} = {nn_dist} min")

# Compare
if nn_dist == bf_dist:
    print("✓ Nearest neighbor found optimal!")
else:
    diff = nn_dist - bf_dist
    pct = (diff / bf_dist) * 100
    print(f"⚠ Nearest neighbor is {diff} min ({pct:.1f}%) longer")
```

---

## Exercise 7: Performance Analysis (15 minutes)

### Task 7.1: Benchmark Brute Force

```python
import time
from math import factorial

def benchmark_brute_force(max_n: int = 10):
    """Benchmark brute force for different problem sizes."""
    print(f"{'N':>4} | {'Permutations':>12} | {'Time':>10}")
    print("-" * 35)

    for n in range(3, max_n + 1):
        # Create dummy matrix
        matrix = [[abs(i-j) for j in range(n)] for i in range(n)]
        places = list(range(1, n))

        # Time the search
        start = time.time()
        route, dist = find_optimal_route(0, places, matrix)
        elapsed = time.time() - start

        print(f"{n:>4} | {factorial(n-1):>12,} | {elapsed:>8.4f}s")

# Run benchmark
benchmark_brute_force(10)
```

### Task 7.2: Answer These Questions

1. At what N does brute force take more than 1 second?
2. At what N does brute force take more than 10 seconds?
3. For our restaurant finder (N ≤ 5), is brute force acceptable?
4. When would you use nearest neighbor instead of brute force?

---

## Bonus Challenges

### Challenge 1: Route Visualization

Create ASCII art visualization of a route:

```python
def visualize_route(route: list, places: list, matrix: list) -> str:
    """
    Create ASCII visualization of route.

    Output format:
      🏠 Home
        │
        │ 5.2 min
        ▼
      🍕 Pizza
        │
        │ 7.1 min
        ▼
      🍔 Burger
    """
    # YOUR CODE HERE
    pass
```

### Challenge 2: Top-K Routes

Find the K best routes instead of just the best:

```python
def find_top_k_routes(
    start: int,
    places_to_visit: list,
    distance_matrix: list,
    k: int = 3
) -> list:
    """
    Find the K shortest routes.

    Returns:
        List of (route, distance) tuples, sorted by distance
    """
    # YOUR CODE HERE
    pass
```

### Challenge 3: Constrained TSP

Add constraints like "must visit Pizza before Burger":

```python
def find_optimal_route_with_constraints(
    start: int,
    places_to_visit: list,
    distance_matrix: list,
    must_visit_before: list  # [(a, b), ...] means a must come before b
) -> tuple:
    """
    Find optimal route respecting ordering constraints.
    """
    # YOUR CODE HERE
    pass
```

---

## Submission Checklist

Before submitting, verify:

- [ ] All exercises completed in `week10_starter.py`
- [ ] All test cases pass (`python week10_starter.py`)
- [ ] `calculate_route_distance` works correctly
- [ ] `find_optimal_route` finds the true optimal
- [ ] `build_distance_matrix` creates valid matrices
- [ ] `RestaurantTourPlanner` class is complete
- [ ] Bonus challenges attempted (optional)

---

## Summary

In this lab, you practiced:

| Concept | What You Learned |
|---------|------------------|
| **Adjacency Matrix** | 2D array for storing distances |
| **Permutations** | `itertools.permutations` for all orderings |
| **Brute Force** | Try all possibilities, keep best |
| **TSP** | Finding shortest route through all nodes |
| **Haversine** | Calculate real-world distances |
| **Complexity** | O(N! × N) grows very fast |

### Key Takeaways

1. **Brute force is fine for small N** (≤10 places)
2. **Permutations grow factorially** - 10! = 3.6 million
3. **Distance matrices** efficiently store all pairwise distances
4. **Nearest neighbor** is faster but not always optimal
5. **Real applications** need to consider actual travel times
