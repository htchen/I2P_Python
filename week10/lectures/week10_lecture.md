# Week 10: The "Traveling Salesperson" (Graph Theory Lite)

## Lecture Overview (3 Hours)

**Phase 3: Algorithms & Logic** — "Making Smart Decisions"

### Learning Objectives
By the end of this lecture, students will be able to:
1. Understand the Traveling Salesperson Problem (TSP) and its applications
2. Represent locations and distances as graphs and matrices
3. Generate all permutations of a collection using `itertools.permutations`
4. Implement a brute-force algorithm to find optimal routes
5. Analyze algorithm complexity and understand when brute force is appropriate
6. Apply TSP concepts to real-world route optimization
7. Integrate with OSRM API data from previous weeks

### Prerequisites
- Week 8: OSRM API (distance matrices)
- Week 9: Functional Patterns & Sorting
- Understanding of lists, loops, and functions

---

# Hour 1: Introduction to Graph Theory and TSP

## 1.1 What is Graph Theory?

### Graphs in Computer Science

A **graph** is a mathematical structure used to model relationships between objects.

```
       (A)
      / | \
     /  |  \
   (B)-(C)-(D)
        |
       (E)
```

Key terminology:
- **Node (Vertex)**: A point in the graph (A, B, C, D, E above)
- **Edge**: A connection between two nodes
- **Weight**: A value associated with an edge (distance, time, cost)

### Why Graphs Matter for Our Project

Our Smart City Navigator needs to answer: "What's the best order to visit multiple places?"

```
    ┌──────────────────────────────────────────────┐
    │                                              │
    │   🏠 Start ─────5 min────> 🍕 Pizza A       │
    │      │                        │              │
    │      │                        8 min          │
    │   10 min                      │              │
    │      │                        ▼              │
    │      └───────────────────> 🍔 Burger B      │
    │                               │              │
    │                            6 min             │
    │                               │              │
    │                               ▼              │
    │                           🌮 Taco C         │
    │                                              │
    └──────────────────────────────────────────────┘
```

This is a **weighted graph** where:
- Nodes = Locations (Start, Pizza A, Burger B, Taco C)
- Edges = Paths between locations
- Weights = Walking time in minutes

---

## 1.2 The Traveling Salesperson Problem (TSP)

### Problem Statement

> Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?

### Our Version: Restaurant Tour

Given a starting location and N restaurants to visit:
- Visit each restaurant exactly once
- Minimize total walking time
- (Optionally return to start)

### Why TSP is Famous

TSP is one of the most studied problems in computer science and operations research:

| Application | Nodes | Edges |
|-------------|-------|-------|
| Delivery routes | Addresses | Streets |
| Circuit board drilling | Holes | Drill paths |
| DNA sequencing | Gene fragments | Overlap similarity |
| Telescope scheduling | Stars | Angular distance |
| Package sorting | Bins | Conveyor paths |

### TSP Complexity

TSP is **NP-hard**, meaning:
- No known algorithm solves all cases quickly
- As input grows, time grows extremely fast
- For small inputs, brute force works fine

```
Number of possible routes for N cities:
- N = 3:  3! = 6 routes
- N = 5:  5! = 120 routes
- N = 10: 10! = 3,628,800 routes
- N = 15: 15! = 1,307,674,368,000 routes
- N = 20: 20! = 2,432,902,008,176,640,000 routes
```

For our project (3-5 restaurants), brute force is **perfect**!

---

## 1.3 Representing Graphs: Adjacency Matrix

### What is an Adjacency Matrix?

An **adjacency matrix** represents graph connections as a 2D array where:
- `matrix[i][j]` = weight of edge from node i to node j
- `matrix[i][i]` = 0 (distance to self)
- For undirected graphs: `matrix[i][j] == matrix[j][i]`

### Example: 4 Locations

```
Locations:
  0 = Start (Home)
  1 = Pizza Palace
  2 = Burger Barn
  3 = Taco Town

Distance Matrix (walking minutes):
              To:
         0    1    2    3
       ┌────┬────┬────┬────┐
    0  │  0 │  5 │ 10 │ 15 │  From Start
       ├────┼────┼────┼────┤
    1  │  5 │  0 │  8 │  7 │  From Pizza
From:  ├────┼────┼────┼────┤
    2  │ 10 │  8 │  0 │  6 │  From Burger
       ├────┼────┼────┼────┤
    3  │ 15 │  7 │  6 │  0 │  From Taco
       └────┴────┴────┴────┘
```

### Python Representation

```python
# Distance matrix as nested list
distance_matrix = [
    [0,  5, 10, 15],  # From Start (0)
    [5,  0,  8,  7],  # From Pizza Palace (1)
    [10, 8,  0,  6],  # From Burger Barn (2)
    [15, 7,  6,  0],  # From Taco Town (3)
]

# Access: distance_matrix[from][to]
print(f"Start to Pizza: {distance_matrix[0][1]} min")      # 5
print(f"Pizza to Burger: {distance_matrix[1][2]} min")     # 8
print(f"Burger to Taco: {distance_matrix[2][3]} min")      # 6
```

### Building a Matrix from Place Data

```python
def build_distance_matrix(places: list, get_distance_func) -> list:
    """
    Build a distance matrix from a list of places.

    Args:
        places: List of place dictionaries with coordinates
        get_distance_func: Function that takes two places and returns distance

    Returns:
        2D list (matrix) of distances
    """
    n = len(places)
    matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = get_distance_func(places[i], places[j])

    return matrix

# Example usage with Haversine distance
import math

def haversine_distance(place1, place2):
    """Calculate distance in km between two places."""
    lat1, lon1 = place1["lat"], place1["lon"]
    lat2, lon2 = place2["lat"], place2["lon"]

    R = 6371  # Earth's radius in km

    lat1, lat2 = math.radians(lat1), math.radians(lat2)
    dlat = lat2 - lat1
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return round(R * c, 2)

places = [
    {"name": "Start", "lat": 25.033, "lon": 121.565},
    {"name": "Pizza", "lat": 25.038, "lon": 121.568},
    {"name": "Burger", "lat": 25.030, "lon": 121.560},
]

matrix = build_distance_matrix(places, haversine_distance)
```

---

## 1.4 Calculating Route Distance

### Total Route Distance

Given a route (sequence of node indices), calculate total distance:

```python
def calculate_route_distance(route: list, distance_matrix: list) -> float:
    """
    Calculate total distance for a route.

    Args:
        route: List of node indices [start, node1, node2, ...]
        distance_matrix: 2D distance matrix

    Returns:
        Total distance of the route
    """
    total = 0
    for i in range(len(route) - 1):
        from_node = route[i]
        to_node = route[i + 1]
        total += distance_matrix[from_node][to_node]
    return total

# Example
distance_matrix = [
    [0,  5, 10, 15],
    [5,  0,  8,  7],
    [10, 8,  0,  6],
    [15, 7,  6,  0],
]

route1 = [0, 1, 2, 3]  # Start -> Pizza -> Burger -> Taco
route2 = [0, 1, 3, 2]  # Start -> Pizza -> Taco -> Burger
route3 = [0, 3, 2, 1]  # Start -> Taco -> Burger -> Pizza

print(f"Route 1: {calculate_route_distance(route1, distance_matrix)} min")
print(f"Route 2: {calculate_route_distance(route2, distance_matrix)} min")
print(f"Route 3: {calculate_route_distance(route3, distance_matrix)} min")
```

### Visualizing Routes

```
Route 1: Start(0) -> Pizza(1) -> Burger(2) -> Taco(3)
         0 ──5──> 1 ──8──> 2 ──6──> 3
         Total: 5 + 8 + 6 = 19 minutes

Route 2: Start(0) -> Pizza(1) -> Taco(3) -> Burger(2)
         0 ──5──> 1 ──7──> 3 ──6──> 2
         Total: 5 + 7 + 6 = 18 minutes  ← Better!

Route 3: Start(0) -> Taco(3) -> Burger(2) -> Pizza(1)
         0 ──15─> 3 ──6──> 2 ──8──> 1
         Total: 15 + 6 + 8 = 29 minutes  ← Worst!
```

---

# Hour 2: Permutations and Brute Force

## 2.1 Understanding Permutations

### What is a Permutation?

A **permutation** is an arrangement of elements in a specific order.

For 3 items [A, B, C], all permutations are:
1. [A, B, C]
2. [A, C, B]
3. [B, A, C]
4. [B, C, A]
5. [C, A, B]
6. [C, B, A]

Total: 3! = 3 × 2 × 1 = 6 permutations

### Factorial Growth

| n | n! | Calculation |
|---|-----|-------------|
| 1 | 1 | 1 |
| 2 | 2 | 2×1 |
| 3 | 6 | 3×2×1 |
| 4 | 24 | 4×3×2×1 |
| 5 | 120 | 5×4×3×2×1 |
| 6 | 720 | 6! |
| 7 | 5,040 | 7! |
| 8 | 40,320 | 8! |
| 9 | 362,880 | 9! |
| 10 | 3,628,800 | 10! |

### Using itertools.permutations

Python's `itertools` module provides efficient permutation generation:

```python
from itertools import permutations

# Generate all permutations of a list
items = ['A', 'B', 'C']

print("All permutations of [A, B, C]:")
for i, perm in enumerate(permutations(items), 1):
    print(f"  {i}. {perm}")

# Output:
# 1. ('A', 'B', 'C')
# 2. ('A', 'C', 'B')
# 3. ('B', 'A', 'C')
# 4. ('B', 'C', 'A')
# 5. ('C', 'A', 'B')
# 6. ('C', 'B', 'A')
```

### Permutations of Indices

For TSP, we work with node indices:

```python
from itertools import permutations

places_to_visit = [1, 2, 3]  # Indices of places (excluding start)

print("All possible visit orders:")
for perm in permutations(places_to_visit):
    print(f"  Start(0) -> {perm[0]} -> {perm[1]} -> {perm[2]}")

# Output:
# Start(0) -> 1 -> 2 -> 3
# Start(0) -> 1 -> 3 -> 2
# Start(0) -> 2 -> 1 -> 3
# Start(0) -> 2 -> 3 -> 1
# Start(0) -> 3 -> 1 -> 2
# Start(0) -> 3 -> 2 -> 1
```

---

## 2.2 Brute Force Algorithm

### The Algorithm

```
1. Generate ALL possible permutations of places to visit
2. For EACH permutation:
   a. Build the complete route (start + permutation)
   b. Calculate total distance
   c. If this distance < best so far, save it
3. Return the best route found
```

### Implementation

```python
from itertools import permutations
from typing import List, Tuple

def find_optimal_route_brute_force(
    start: int,
    places_to_visit: List[int],
    distance_matrix: List[List[float]]
) -> Tuple[List[int], float]:
    """
    Find the optimal route using brute force.

    Args:
        start: Index of starting location
        places_to_visit: List of indices to visit
        distance_matrix: 2D distance matrix

    Returns:
        Tuple of (best_route, best_distance)
    """
    best_route = None
    best_distance = float('inf')

    # Try all permutations
    for perm in permutations(places_to_visit):
        # Build complete route: start -> perm[0] -> perm[1] -> ...
        route = [start] + list(perm)

        # Calculate total distance
        distance = calculate_route_distance(route, distance_matrix)

        # Update best if this is better
        if distance < best_distance:
            best_distance = distance
            best_route = route

    return best_route, best_distance

# Example usage
distance_matrix = [
    [0,  5, 10, 15],
    [5,  0,  8,  7],
    [10, 8,  0,  6],
    [15, 7,  6,  0],
]

route, distance = find_optimal_route_brute_force(0, [1, 2, 3], distance_matrix)
print(f"Best route: {route}")
print(f"Total distance: {distance} minutes")
```

### Tracing the Algorithm

```
Starting brute force search...
Start: 0, Places to visit: [1, 2, 3]

Permutation 1: (1, 2, 3)
  Route: [0, 1, 2, 3]
  Distance: 0→1(5) + 1→2(8) + 2→3(6) = 19
  Best so far: 19 ✓

Permutation 2: (1, 3, 2)
  Route: [0, 1, 3, 2]
  Distance: 0→1(5) + 1→3(7) + 3→2(6) = 18
  Better! Best so far: 18 ✓

Permutation 3: (2, 1, 3)
  Route: [0, 2, 1, 3]
  Distance: 0→2(10) + 2→1(8) + 1→3(7) = 25
  Not better.

Permutation 4: (2, 3, 1)
  Route: [0, 2, 3, 1]
  Distance: 0→2(10) + 2→3(6) + 3→1(7) = 23
  Not better.

Permutation 5: (3, 1, 2)
  Route: [0, 3, 1, 2]
  Distance: 0→3(15) + 3→1(7) + 1→2(8) = 30
  Not better.

Permutation 6: (3, 2, 1)
  Route: [0, 3, 2, 1]
  Distance: 0→3(15) + 3→2(6) + 2→1(8) = 29
  Not better.

Result: Best route is [0, 1, 3, 2] with distance 18 minutes
```

---

## 2.3 Round-Trip Routes

### Including Return to Start

Sometimes we need to return to the starting point:

```python
def find_optimal_round_trip(
    start: int,
    places_to_visit: List[int],
    distance_matrix: List[List[float]]
) -> Tuple[List[int], float]:
    """
    Find optimal route that returns to start.
    """
    best_route = None
    best_distance = float('inf')

    for perm in permutations(places_to_visit):
        # Build round-trip route: start -> ... -> start
        route = [start] + list(perm) + [start]

        distance = calculate_route_distance(route, distance_matrix)

        if distance < best_distance:
            best_distance = distance
            best_route = route

    return best_route, best_distance

# Example
route, distance = find_optimal_round_trip(0, [1, 2, 3], distance_matrix)
print(f"Round trip: {route}")
print(f"Total distance: {distance} minutes")
# Adds return: ... + 3→0 or similar
```

### Comparing One-Way vs Round-Trip

```python
# One-way route
one_way, dist1 = find_optimal_route_brute_force(0, [1, 2, 3], distance_matrix)
print(f"One-way: {one_way}, Distance: {dist1}")

# Round-trip route
round_trip, dist2 = find_optimal_round_trip(0, [1, 2, 3], distance_matrix)
print(f"Round-trip: {round_trip}, Distance: {dist2}")
```

---

## 2.4 Algorithm Complexity Analysis

### Time Complexity

For N places to visit:
- Number of permutations: N!
- Time to calculate each route: O(N)
- Total time complexity: **O(N! × N)**

### Space Complexity

- Distance matrix: O(N²)
- Best route storage: O(N)
- Total space: **O(N²)**

### Practical Limits

```python
import time
from itertools import permutations
from math import factorial

def benchmark_brute_force(n: int):
    """Benchmark brute force for n places."""
    # Create dummy distance matrix
    matrix = [[i + j for j in range(n)] for i in range(n)]

    start_time = time.time()
    count = 0

    for perm in permutations(range(1, n)):
        route = [0] + list(perm)
        # Simulate distance calculation
        total = sum(matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        count += 1

    elapsed = time.time() - start_time
    return count, elapsed

print("Brute Force Benchmarks:")
print("-" * 50)
for n in range(3, 12):
    count, elapsed = benchmark_brute_force(n)
    print(f"N={n:2d}: {count:>10,} permutations, {elapsed:>8.4f} seconds")
```

Typical output:
```
N= 3:          2 permutations,   0.0000 seconds
N= 4:          6 permutations,   0.0000 seconds
N= 5:         24 permutations,   0.0001 seconds
N= 6:        120 permutations,   0.0002 seconds
N= 7:        720 permutations,   0.0010 seconds
N= 8:      5,040 permutations,   0.0067 seconds
N= 9:     40,320 permutations,   0.0543 seconds
N=10:    362,880 permutations,   0.5124 seconds
N=11:  3,628,800 permutations,   5.3847 seconds
```

### When is Brute Force Acceptable?

| Scenario | Max N | Reasoning |
|----------|-------|-----------|
| Interactive app (< 100ms response) | 8-9 | Users won't wait |
| Background processing (< 1s) | 10-11 | Acceptable delay |
| Batch job (< 1 min) | 12-13 | Running overnight is okay |
| Research (hours okay) | 14-15 | One-time computation |

**For our restaurant finder (3-5 places): Brute force is perfect!**

---

## 2.5 Beyond TSP: Other Applications of Permutations

So far we've used permutations to solve TSP — finding the shortest route through a set of locations. But permutations are useful **far beyond routing problems**. Anywhere we ask *"what's the best ordering?"* or *"which arrangements satisfy a rule?"*, permutations show up.

The general pattern is always:
1. **Generate** every possible ordering with `itertools.permutations`
2. **Filter or score** each one with a problem-specific check
3. **Return** the best (or all valid) results

Let's look at three classic examples that have nothing to do with maps.

---

### 2.5.1 Anagrams: Finding Valid Words

An **anagram** is a rearrangement of letters in a word. Given a set of letters, list every permutation and check which ones form real words.

```python
from itertools import permutations

def find_anagrams(letters: str, dictionary: set) -> list:
    """Find every valid word that can be formed from `letters`."""
    valid_words = set()

    # Try every possible length, from 2 letters up to all of them
    for length in range(2, len(letters) + 1):
        for perm in permutations(letters, length):
            word = "".join(perm).lower()
            if word in dictionary:
                valid_words.add(word)

    # Sort: longer words first, then alphabetical
    return sorted(valid_words, key=lambda w: (-len(w), w))


# Example
dictionary = {"eat", "ate", "tea", "at", "ta", "ae", "ea", "et", "te"}
print(find_anagrams("EAT", dictionary))
# Output: ['ate', 'eat', 'tea', 'ae', 'at', 'ea', 'et', 'ta', 'te']
```

**How it works:**
- `permutations(letters, length)` generates orderings of a *specific* length.
- We loop over multiple lengths so we also find shorter sub-words (e.g. "AT" out of "EAT").
- Using a `set` for the dictionary makes each lookup O(1).
- The same letters can form multiple valid words ("EAT", "ATE", "TEA").

**Tracing on "DOG":**
```
Length 2 perms: DO, OD, DG, GD, OG, GO   (6 perms)
Length 3 perms: DOG, DGO, ODG, OGD, GDO, GOD   (6 perms)

Filtered against an English dictionary:
   → "DOG", "GOD"  ✓
```

**Real-world uses:** Scrabble / Wordle helpers, crossword solvers, simple cipher cracking.

---

### 2.5.2 Seating Arrangements with Constraints

Five friends sit in a row, but **A and B refuse to sit next to each other**. How many arrangements work?

This is a textbook **"permutations + filter"** problem — and a perfect chance to reuse the list-comprehension / `filter` idea from Week 9.

```python
from itertools import permutations

def are_adjacent(arrangement: tuple, p1: str, p2: str) -> bool:
    """Return True if p1 and p2 sit next to each other."""
    return abs(arrangement.index(p1) - arrangement.index(p2)) == 1

def find_valid_seatings(people: list, forbidden_pairs: list) -> list:
    """Return all seatings where no forbidden pair is adjacent."""
    return [
        arr for arr in permutations(people)
        if all(not are_adjacent(arr, p1, p2) for p1, p2 in forbidden_pairs)
    ]


# Example
people = ["A", "B", "C", "D", "E"]
forbidden = [("A", "B")]   # A and B cannot sit next to each other

valid = find_valid_seatings(people, forbidden)
print(f"Valid arrangements: {len(valid)} out of 120")
for arr in valid[:3]:
    print("  " + " - ".join(arr))
```

Output:
```
Valid arrangements: 72 out of 120
  A - C - B - D - E
  A - C - B - E - D
  A - C - D - B - E
```

**How it works:**
- There are 5! = 120 total seatings.
- For each arrangement, we check every forbidden pair.
- `arrangement.index(p1)` returns the seat number of person `p1`.
- "A and B are adjacent" ⇔ `|index(A) − index(B)| == 1`.

**Math sanity check:** Treat "A and B together" as a single block. There are 4! = 24 ways to arrange the 4 blocks, times 2 (AB or BA) = **48** "bad" arrangements. So valid = 120 − 48 = **72** ✓

**Extending:** Add a second rule like *"C and D must sit together"* — just write a complementary `must_be_adjacent` check and combine them in the comprehension.

---

### 2.5.3 The N-Queens Problem

Place N queens on an N×N chessboard so that **no two queens attack each other** — none share a row, column, or diagonal.

Here's the elegant insight: if every row holds exactly one queen, a solution is just a list `[c₀, c₁, …, c_{N−1}]` where `cᵢ` is the column of the queen in row *i*. Since each column appears at most once, **a solution is exactly a permutation of `[0, 1, …, N−1]`**.

```python
from itertools import permutations

def is_valid_queens(arrangement: tuple) -> bool:
    """Check if a queen placement has no diagonal conflicts."""
    n = len(arrangement)
    for i in range(n):
        for j in range(i + 1, n):
            # |row difference| == |column difference|  →  same diagonal
            if abs(arrangement[i] - arrangement[j]) == abs(i - j):
                return False
    return True

def solve_n_queens(n: int) -> list:
    """Return all solutions to the N-queens problem."""
    return [perm for perm in permutations(range(n)) if is_valid_queens(perm)]

def print_board(arrangement: tuple) -> None:
    """Print a chessboard with the queens placed."""
    n = len(arrangement)
    for row in range(n):
        print(" ".join("Q" if arrangement[row] == col else "."
                       for col in range(n)))
    print()


# Example: 4-queens
solutions = solve_n_queens(4)
print(f"4-Queens has {len(solutions)} solutions\n")
print("First solution:")
print_board(solutions[0])
```

Output:
```
4-Queens has 2 solutions

First solution:
. Q . .
. . . Q
Q . . .
. . Q .
```

**How it works:**
- The permutation `(1, 3, 0, 2)` reads as: row 0 → col 1, row 1 → col 3, row 2 → col 0, row 3 → col 2.
- Because it's a permutation, **no row repeats and no column repeats** — only diagonals can still clash.
- Two queens are on the same diagonal exactly when `|rowᵢ − rowⱼ| == |colᵢ − colⱼ|`.

**Scaling (factorial growth, just like TSP!):**

| N | Permutations checked | Solutions found |
|---|----------------------|-----------------|
| 4 | 24 | 2 |
| 5 | 120 | 10 |
| 6 | 720 | 4 |
| 7 | 5,040 | 40 |
| 8 | 40,320 | 92 |

Brute force via `permutations` works comfortably up to N ≈ 10. Beyond that, smarter techniques (backtracking with pruning) are required — the same lesson we learned with TSP.

---

### 2.5.4 The Common Pattern

Notice that **TSP, anagrams, seating, and N-Queens** all follow the *same* template:

```python
best = None
for perm in permutations(items):
    if is_valid(perm):              # filter (optional)
        if score(perm) < best_score:  # optimize (optional)
            best = perm
```

| Problem | Permutation of… | Filter | Optimize |
|---------|------------------|--------|----------|
| TSP | locations | — | minimize total distance |
| Anagrams | letters | in dictionary? | — (collect all) |
| Seating | people | no forbidden pair adjacent | — (collect all) |
| N-Queens | column indices | no diagonal conflict | — (collect all) |

Whenever you see **"find the best ordering"** or **"list all arrangements satisfying X"**, ask yourself: *is this a permutations + filter / score problem?* If so, you already know the toolkit.

---

# Hour 3: Integration and Advanced Topics

## 3.1 Integrating with OSRM API

### Building Real Distance Matrices

In Week 8, we learned to use OSRM for real walking distances. Now let's combine that with TSP:

```python
import requests
from typing import List, Dict, Any

def get_osrm_distance_matrix(
    places: List[Dict[str, Any]],
    profile: str = "foot"
) -> List[List[float]]:
    """
    Get distance matrix from OSRM Table service.

    Args:
        places: List of places with 'lat' and 'lon' keys
        profile: 'foot', 'car', or 'bike'

    Returns:
        2D matrix of durations in minutes
    """
    # Build coordinates string
    coords = ";".join(f"{p['lon']},{p['lat']}" for p in places)

    # OSRM Table API
    url = f"http://router.project-osrm.org/table/v1/{profile}/{coords}"
    params = {"annotations": "duration"}

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if data["code"] != "Ok":
        raise ValueError(f"OSRM error: {data.get('message', 'Unknown')}")

    # Convert seconds to minutes
    durations = data["durations"]
    return [[round(d / 60, 1) if d else 0 for d in row] for row in durations]


def find_optimal_restaurant_tour(
    start_location: Dict[str, Any],
    restaurants: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Find optimal order to visit restaurants.

    Args:
        start_location: Starting point with lat/lon
        restaurants: List of restaurants with lat/lon

    Returns:
        Dictionary with optimal route and details
    """
    # Combine all locations
    all_places = [start_location] + restaurants

    # Get real walking times from OSRM
    distance_matrix = get_osrm_distance_matrix(all_places, profile="foot")

    # Find optimal route
    places_to_visit = list(range(1, len(all_places)))
    best_route, best_time = find_optimal_route_brute_force(
        start=0,
        places_to_visit=places_to_visit,
        distance_matrix=distance_matrix
    )

    # Build result with place names
    route_names = [all_places[i]["name"] for i in best_route]

    return {
        "route_indices": best_route,
        "route_names": route_names,
        "total_time_minutes": best_time,
        "distance_matrix": distance_matrix,
    }


# Example usage
start = {"name": "Home", "lat": 25.033, "lon": 121.565}
restaurants = [
    {"name": "Pizza Palace", "lat": 25.038, "lon": 121.568},
    {"name": "Burger Barn", "lat": 25.030, "lon": 121.560},
    {"name": "Taco Town", "lat": 25.035, "lon": 121.570},
]

result = find_optimal_restaurant_tour(start, restaurants)
print(f"Optimal route: {' -> '.join(result['route_names'])}")
print(f"Total walking time: {result['total_time_minutes']} minutes")
```

---

## 3.2 Visualizing Routes

### Text-Based Visualization

```python
def visualize_route_text(
    route: List[int],
    places: List[Dict[str, Any]],
    distance_matrix: List[List[float]]
) -> str:
    """Create text visualization of route."""
    lines = ["Route Visualization:", "=" * 40]

    total = 0
    for i in range(len(route) - 1):
        from_idx = route[i]
        to_idx = route[i + 1]
        from_name = places[from_idx]["name"]
        to_name = places[to_idx]["name"]
        dist = distance_matrix[from_idx][to_idx]
        total += dist

        lines.append(f"  {from_name}")
        lines.append(f"    │")
        lines.append(f"    │ {dist} min")
        lines.append(f"    ▼")

    lines.append(f"  {places[route[-1]]['name']}")
    lines.append("=" * 40)
    lines.append(f"Total: {total} minutes")

    return "\n".join(lines)

# Example
places = [
    {"name": "🏠 Home"},
    {"name": "🍕 Pizza"},
    {"name": "🍔 Burger"},
    {"name": "🌮 Taco"},
]
print(visualize_route_text([0, 1, 3, 2], places, distance_matrix))
```

Output:
```
Route Visualization:
========================================
  🏠 Home
    │
    │ 5 min
    ▼
  🍕 Pizza
    │
    │ 7 min
    ▼
  🌮 Taco
    │
    │ 6 min
    ▼
  🍔 Burger
========================================
Total: 18 minutes
```

### Comparing All Routes

```python
def compare_all_routes(
    start: int,
    places_to_visit: List[int],
    places: List[Dict[str, Any]],
    distance_matrix: List[List[float]]
) -> None:
    """Display all routes ranked by distance."""
    routes = []

    for perm in permutations(places_to_visit):
        route = [start] + list(perm)
        dist = calculate_route_distance(route, distance_matrix)
        route_str = " -> ".join(places[i]["name"] for i in route)
        routes.append((dist, route_str, route))

    # Sort by distance
    routes.sort(key=lambda x: x[0])

    print("All Routes Ranked:")
    print("=" * 60)
    for i, (dist, route_str, _) in enumerate(routes, 1):
        marker = "👑 BEST" if i == 1 else ""
        print(f"{i}. {dist:>5} min: {route_str} {marker}")

# Example
places = [
    {"name": "Start"},
    {"name": "Pizza"},
    {"name": "Burger"},
    {"name": "Taco"},
]
compare_all_routes(0, [1, 2, 3], places, distance_matrix)
```

---

## 3.3 Handling Edge Cases

### Empty or Single Destination

```python
def find_optimal_route_safe(
    start: int,
    places_to_visit: List[int],
    distance_matrix: List[List[float]]
) -> Tuple[List[int], float]:
    """
    Find optimal route with edge case handling.
    """
    # Edge case: no places to visit
    if not places_to_visit:
        return [start], 0

    # Edge case: single place to visit
    if len(places_to_visit) == 1:
        dest = places_to_visit[0]
        return [start, dest], distance_matrix[start][dest]

    # Normal case: use brute force
    return find_optimal_route_brute_force(start, places_to_visit, distance_matrix)
```

### Handling Unreachable Locations

```python
def find_optimal_route_with_validation(
    start: int,
    places_to_visit: List[int],
    distance_matrix: List[List[float]],
    max_distance: float = float('inf')
) -> Tuple[List[int], float]:
    """
    Find optimal route, excluding unreachable segments.
    """
    # Check for unreachable locations (infinite or very large distances)
    for i in places_to_visit:
        if distance_matrix[start][i] >= max_distance:
            raise ValueError(f"Location {i} is unreachable from start")

    for i in places_to_visit:
        for j in places_to_visit:
            if i != j and distance_matrix[i][j] >= max_distance:
                raise ValueError(f"Cannot travel from location {i} to {j}")

    return find_optimal_route_brute_force(start, places_to_visit, distance_matrix)
```

---

## 3.4 Beyond Brute Force: A Glimpse at Optimizations

### Nearest Neighbor Heuristic

A faster but non-optimal approach:

```python
def nearest_neighbor_route(
    start: int,
    places_to_visit: List[int],
    distance_matrix: List[List[float]]
) -> Tuple[List[int], float]:
    """
    Find a route using nearest neighbor heuristic.
    Fast but not guaranteed optimal.
    """
    route = [start]
    unvisited = set(places_to_visit)
    current = start
    total_distance = 0

    while unvisited:
        # Find nearest unvisited place
        nearest = min(unvisited, key=lambda x: distance_matrix[current][x])

        # Add to route
        total_distance += distance_matrix[current][nearest]
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    return route, total_distance

# Compare with brute force
print("Nearest Neighbor (fast, approximate):")
route_nn, dist_nn = nearest_neighbor_route(0, [1, 2, 3], distance_matrix)
print(f"  Route: {route_nn}, Distance: {dist_nn}")

print("\nBrute Force (slow, optimal):")
route_bf, dist_bf = find_optimal_route_brute_force(0, [1, 2, 3], distance_matrix)
print(f"  Route: {route_bf}, Distance: {dist_bf}")
```

### When to Use Each Approach

| Approach | Time Complexity | Optimality | Use When |
|----------|----------------|------------|----------|
| Brute Force | O(N! × N) | Guaranteed | N ≤ 10 |
| Nearest Neighbor | O(N²) | ~80% optimal | N > 10, need fast result |
| Dynamic Programming | O(N² × 2^N) | Guaranteed | 10 < N ≤ 20 |
| Genetic Algorithm | O(varies) | Near-optimal | N > 20 |

**For our project: Brute force is the right choice!**

---

## 3.5 Complete Application: Restaurant Tour Planner

### Putting It All Together

```python
from itertools import permutations
from typing import List, Dict, Any, Tuple, Optional
import math

class RestaurantTourPlanner:
    """Plan optimal routes to visit multiple restaurants."""

    def __init__(self, start_location: Dict[str, Any]):
        """
        Initialize planner with starting location.

        Args:
            start_location: Dict with 'name', 'lat', 'lon'
        """
        self.start = start_location
        self.restaurants: List[Dict[str, Any]] = []
        self.distance_matrix: Optional[List[List[float]]] = None

    def add_restaurant(self, restaurant: Dict[str, Any]) -> None:
        """Add a restaurant to visit."""
        self.restaurants.append(restaurant)
        self.distance_matrix = None  # Invalidate cache

    def _build_distance_matrix(self) -> List[List[float]]:
        """Build distance matrix using Haversine formula."""
        all_places = [self.start] + self.restaurants
        n = len(all_places)
        matrix = [[0.0] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i != j:
                    # Calculate walking time (assume 5 km/h walking speed)
                    dist_km = self._haversine(all_places[i], all_places[j])
                    time_min = (dist_km / 5) * 60  # Convert to minutes
                    matrix[i][j] = round(time_min, 1)

        return matrix

    def _haversine(self, p1: Dict, p2: Dict) -> float:
        """Calculate distance in km between two points."""
        R = 6371
        lat1, lat2 = math.radians(p1["lat"]), math.radians(p2["lat"])
        dlat = lat2 - lat1
        dlon = math.radians(p2["lon"] - p1["lon"])

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        return 2 * R * math.asin(math.sqrt(a))

    def _calculate_route_distance(self, route: List[int]) -> float:
        """Calculate total distance for a route."""
        return sum(
            self.distance_matrix[route[i]][route[i+1]]
            for i in range(len(route) - 1)
        )

    def find_optimal_route(self, return_to_start: bool = False) -> Dict[str, Any]:
        """
        Find the optimal route to visit all restaurants.

        Args:
            return_to_start: Whether to return to starting location

        Returns:
            Dict with route details
        """
        if not self.restaurants:
            return {
                "route": [self.start["name"]],
                "total_time": 0,
                "message": "No restaurants to visit"
            }

        # Build distance matrix if needed
        if self.distance_matrix is None:
            self.distance_matrix = self._build_distance_matrix()

        all_places = [self.start] + self.restaurants
        places_to_visit = list(range(1, len(all_places)))

        best_route = None
        best_distance = float('inf')

        for perm in permutations(places_to_visit):
            route = [0] + list(perm)
            if return_to_start:
                route.append(0)

            distance = self._calculate_route_distance(route)

            if distance < best_distance:
                best_distance = distance
                best_route = route

        return {
            "route_indices": best_route,
            "route_names": [all_places[i]["name"] for i in best_route],
            "total_time_minutes": round(best_distance, 1),
            "num_permutations_checked": math.factorial(len(places_to_visit)),
            "return_to_start": return_to_start
        }

    def get_route_details(self, route_indices: List[int]) -> List[Dict[str, Any]]:
        """Get detailed leg-by-leg information for a route."""
        all_places = [self.start] + self.restaurants
        legs = []

        for i in range(len(route_indices) - 1):
            from_idx = route_indices[i]
            to_idx = route_indices[i + 1]

            legs.append({
                "from": all_places[from_idx]["name"],
                "to": all_places[to_idx]["name"],
                "time_minutes": self.distance_matrix[from_idx][to_idx]
            })

        return legs


# Demo
if __name__ == "__main__":
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

    # Find optimal route
    result = planner.find_optimal_route(return_to_start=False)

    print("=" * 50)
    print("RESTAURANT TOUR PLANNER")
    print("=" * 50)
    print(f"\nOptimal Route: {' → '.join(result['route_names'])}")
    print(f"Total Time: {result['total_time_minutes']} minutes")
    print(f"Routes Checked: {result['num_permutations_checked']}")

    # Show leg details
    print("\nRoute Details:")
    legs = planner.get_route_details(result['route_indices'])
    for i, leg in enumerate(legs, 1):
        print(f"  {i}. {leg['from']} → {leg['to']}: {leg['time_minutes']} min")
```

---

## 3.6 Summary

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Graph** | Nodes (locations) connected by edges (paths) |
| **Adjacency Matrix** | 2D array storing distances between all pairs |
| **Permutation** | Specific arrangement/ordering of elements |
| **TSP** | Finding shortest route visiting all nodes |
| **Brute Force** | Trying all possibilities to find optimal |
| **Factorial Growth** | N! grows extremely fast |

### When to Use Brute Force

```
✅ USE brute force when:
   - N ≤ 10 places
   - You need the guaranteed optimal solution
   - Running time of seconds is acceptable

❌ DON'T use brute force when:
   - N > 12 places
   - You need sub-second response
   - Approximate solution is acceptable
```

### Code Patterns

```python
# Generate permutations
from itertools import permutations
for perm in permutations(items):
    process(perm)

# Calculate route distance
total = sum(matrix[route[i]][route[i+1]] for i in range(len(route)-1))

# Track best solution
best_value = float('inf')
for candidate in candidates:
    if score(candidate) < best_value:
        best_value = score(candidate)
        best_solution = candidate
```

---

## Next Week Preview

**Week 11: Midterm Exam 2**
- Review of Weeks 8-10
- Practice problems
- Exam preparation tips
