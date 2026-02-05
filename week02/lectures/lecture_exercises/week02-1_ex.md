# Week 2-1 Lab: Lists, Loops & The Route

## Lab Overview

In this lab, you will practice:
- Creating and manipulating lists
- Using loops to iterate over data
- Working with `range()`, `enumerate()`, and `zip()`
- Applying `map()` and `filter()` to coordinate data
- Calculating route distances

---

## Exercise 1: List Basics (10 minutes)

### Task 1.1: Create and Modify Lists

```python
# TODO: Create a list of 5 cities you want to visit
cities = ["Taipei", ___, ___, ___, ___]

# TODO: Add "Singapore" to the end of the list
cities.___("Singapore")

# TODO: Insert "Hong Kong" at position 2 (index 2)
cities.___(2, "Hong Kong")

# TODO: Remove "Taipei" from the list
cities.___("Taipei")

# TODO: Print the final list and its length
print(f"Cities: {cities}")
print(f"Number of cities: {len(cities)}")
```

### Task 1.2: List Slicing

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# TODO: Get the first 3 elements
first_three = numbers[___]
print(f"First three: {first_three}")  # [0, 1, 2]

# TODO: Get the last 3 elements
last_three = numbers[___]
print(f"Last three: {last_three}")  # [7, 8, 9]

# TODO: Get elements from index 2 to 5 (inclusive of 2, exclusive of 6)
middle = numbers[___]
print(f"Middle: {middle}")  # [2, 3, 4, 5]

# TODO: Get every other element (0, 2, 4, 6, 8)
every_other = numbers[___]
print(f"Every other: {every_other}")

# TODO: Reverse the list using slicing
reversed_list = numbers[___]
print(f"Reversed: {reversed_list}")
```

### Task 1.3: List of Coordinates

```python
# TODO: Create a list of 5 coordinate tuples for a walking route
# Each coordinate should be (latitude, longitude)
route = [
    (25.0330, 121.5654),  # Start: Taipei 101
    (___),                 # Stop 2
    (___),                 # Stop 3
    (___),                 # Stop 4
    (___),                 # End
]

# TODO: Print the first and last coordinates
print(f"Start: {route[___]}")
print(f"End: {route[___]}")

# TODO: Print the number of stops
print(f"Total stops: {___}")
```

---

## Exercise 2: For Loops (15 minutes)

### Task 2.1: Basic Loop

```python
route = [
    (25.0330, 121.5654),
    (25.0339, 121.5645),
    (25.0329, 121.5598),
    (25.0279, 121.5595),
    (25.0174, 121.5405),
]

# TODO: Print each coordinate in the route
for coord in route:
    print(f"Location: {___}")
```

### Task 2.2: Loop with `enumerate()`

```python
route = [
    (25.0330, 121.5654),
    (25.0339, 121.5645),
    (25.0329, 121.5598),
    (25.0279, 121.5595),
    (25.0174, 121.5405),
]

# TODO: Print each coordinate with its stop number (starting from 1)
for index, coord in enumerate(route, start=___):
    print(f"Stop {index}: {coord}")
```

### Task 2.3: Loop with Tuple Unpacking

```python
route = [
    (25.0330, 121.5654),
    (25.0339, 121.5645),
    (25.0329, 121.5598),
]

# TODO: Print latitude and longitude separately
for lat, lon in route:
    print(f"Latitude: {___}, Longitude: {___}")
```

### Task 2.4: Using `range()`

```python
# TODO: Print numbers from 1 to 10
for i in range(___, ___):
    print(i, end=" ")
print()  # New line

# TODO: Print even numbers from 0 to 20
for i in range(___, ___, ___):
    print(i, end=" ")
print()

# TODO: Print countdown from 5 to 1
for i in range(___, ___, ___):
    print(i, end=" ")
print()
```

---

## Exercise 3: Processing Consecutive Pairs (15 minutes)

### Task 3.1: Iterate Over Pairs Using Index

```python
route = ["A", "B", "C", "D", "E"]

# TODO: Print each consecutive pair
# Expected output:
# A → B
# B → C
# C → D
# D → E

for i in range(len(route) - ___):
    start = route[i]
    end = route[i + ___]
    print(f"{start} → {end}")
```

### Task 3.2: Iterate Over Pairs Using `zip()`

```python
route = ["A", "B", "C", "D", "E"]

# TODO: Use zip() with slicing to get consecutive pairs
# route[:-1] gives all except last: [A, B, C, D]
# route[1:] gives all except first: [B, C, D, E]

for start, end in zip(route[___], route[___]):
    print(f"{start} → {end}")
```

### Task 3.3: Calculate Segment Distances

```python
import math

def haversine(coord1, coord2):
    """Calculate distance in km."""
    R = 6371
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


route = [
    (25.0330, 121.5654),  # Taipei 101
    (25.0339, 121.5645),  # Din Tai Fung
    (25.0329, 121.5598),  # Yongkang Street
    (25.0279, 121.5595),  # Daan Park
    (25.0174, 121.5405),  # NTU
]

# TODO: Calculate and print the distance of each segment
total_distance = 0

for i in range(len(route) - 1):
    dist = haversine(route[i], route[i + 1])
    total_distance += dist
    print(f"Segment {i + 1}: {dist:.3f} km")

print(f"\nTotal distance: {total_distance:.2f} km")
```

---

## Exercise 4: `map()` and `filter()` (15 minutes)

### Task 4.1: Using `map()`

```python
# TODO: Convert a list of Celsius temperatures to Fahrenheit
celsius_temps = [0, 10, 20, 25, 30, 35]

# Using a regular function
def to_fahrenheit(c):
    return c * 9/5 + 32

fahrenheit_temps = list(map(___, celsius_temps))
print(f"Fahrenheit: {fahrenheit_temps}")

# TODO: Using a lambda function
fahrenheit_temps = list(map(lambda c: ___, celsius_temps))
print(f"Fahrenheit: {fahrenheit_temps}")
```

### Task 4.2: Extract Data with `map()`

```python
coords = [
    (25.0330, 121.5654),
    (25.0478, 121.5170),
    (25.0174, 121.5405),
    (25.0878, 121.5241),
]

# TODO: Extract all latitudes using map
latitudes = list(map(lambda c: c[___], coords))
print(f"Latitudes: {latitudes}")

# TODO: Extract all longitudes using map
longitudes = list(map(lambda c: c[___], coords))
print(f"Longitudes: {longitudes}")

# TODO: Format coordinates as strings like "25.0330°N, 121.5654°E"
formatted = list(map(lambda c: f"{c[0]}°N, {c[1]}°E", coords))
print(f"Formatted: {formatted}")
```

### Task 4.3: Using `filter()`

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20]

# TODO: Filter to get only even numbers
evens = list(filter(lambda x: x % 2 == ___, numbers))
print(f"Evens: {evens}")

# TODO: Filter to get numbers greater than 10
big_numbers = list(filter(lambda x: x ___ 10, numbers))
print(f"Greater than 10: {big_numbers}")

# TODO: Filter to get numbers divisible by 3
div_by_3 = list(filter(lambda x: ___, numbers))
print(f"Divisible by 3: {div_by_3}")
```

### Task 4.4: Filter Coordinates

```python
coords = [
    (25.0330, 121.5654),  # Taiwan
    (35.6586, 139.7454),  # Japan
    (25.0478, 121.5170),  # Taiwan
    (37.5665, 126.9780),  # Korea
    (25.0174, 121.5405),  # Taiwan
    (22.3193, 114.1694),  # Hong Kong
]

# TODO: Filter to keep only coordinates in Taiwan
# Taiwan is roughly: latitude 22-26, longitude 119-122
taiwan_coords = list(filter(
    lambda c: 22 <= c[0] <= 26 and ___ <= c[1] <= ___,
    coords
))

print(f"Taiwan coordinates: {taiwan_coords}")
print(f"Count: {len(taiwan_coords)}")
```

---

## Exercise 5: Route Calculator (15 minutes)

### Task 5.1: Complete Route Statistics

```python
import math

def haversine(coord1, coord2):
    """Calculate distance in km."""
    R = 6371
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


def calculate_route_stats(route):
    """
    Calculate statistics for a route.

    Returns:
        Dictionary with total_distance, segment_count, average_segment,
        longest_segment, shortest_segment
    """
    if len(route) < 2:
        return None

    # TODO: Calculate all segment distances
    segment_distances = []
    for i in range(len(route) - 1):
        dist = haversine(route[i], route[i + 1])
        segment_distances.append(dist)

    # TODO: Calculate statistics
    stats = {
        "total_distance": sum(___),
        "segment_count": len(___),
        "average_segment": sum(segment_distances) / len(___),
        "longest_segment": max(___),
        "shortest_segment": min(___),
    }

    return stats


# Test
route = [
    (25.0330, 121.5654),  # Taipei 101
    (25.0339, 121.5645),  # Din Tai Fung
    (25.0329, 121.5598),  # Yongkang Street
    (25.0279, 121.5595),  # Daan Park
    (25.0174, 121.5405),  # NTU
]

stats = calculate_route_stats(route)
print("Route Statistics:")
print(f"  Total distance: {stats['total_distance']:.2f} km")
print(f"  Number of segments: {stats['segment_count']}")
print(f"  Average segment: {stats['average_segment']:.3f} km")
print(f"  Longest segment: {stats['longest_segment']:.3f} km")
print(f"  Shortest segment: {stats['shortest_segment']:.3f} km")
```

### Task 5.2: Find Bounding Box

```python
def get_bounding_box(route):
    """
    Get the bounding box (min/max coordinates) of a route.

    Returns:
        Dictionary with min_lat, max_lat, min_lon, max_lon
    """
    # TODO: Extract all latitudes and longitudes
    latitudes = [coord[0] for coord in route]
    longitudes = [coord[___] for coord in route]

    # TODO: Find min and max
    return {
        "min_lat": min(___),
        "max_lat": max(___),
        "min_lon": min(___),
        "max_lon": max(___),
    }


# Test
route = [
    (25.0330, 121.5654),
    (25.0478, 121.5170),
    (25.0174, 121.5405),
]

bbox = get_bounding_box(route)
print(f"\nBounding Box:")
print(f"  Latitude: {bbox['min_lat']:.4f} to {bbox['max_lat']:.4f}")
print(f"  Longitude: {bbox['min_lon']:.4f} to {bbox['max_lon']:.4f}")
```

### Task 5.3: List Comprehension Practice

```python
route = [
    (25.0330, 121.5654),
    (25.0339, 121.5645),
    (25.0329, 121.5598),
    (25.0279, 121.5595),
    (25.0174, 121.5405),
]

# TODO: Calculate all segment distances using list comprehension
segment_distances = [
    haversine(route[i], route[i + 1])
    for i in range(___)
]
print(f"Segment distances: {segment_distances}")

# TODO: Create formatted strings for each coordinate
formatted_coords = [
    f"({coord[0]:.4f}, {coord[1]:.4f})"
    for ___ in ___
]
print(f"Formatted: {formatted_coords}")

# TODO: Filter to keep only coordinates with latitude > 25.03
high_lat_coords = [
    coord for coord in route
    if ___
]
print(f"High latitude coords: {high_lat_coords}")
```

---

## Exercise 6: Challenge - Route Optimizer Preview (5 minutes)

### Task 6.1: Compare Two Routes

```python
import math

def haversine(coord1, coord2):
    R = 6371
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def total_distance(route):
    """Calculate total distance of a route."""
    return sum(haversine(route[i], route[i+1]) for i in range(len(route)-1))


# Two different orderings of the same places
places = {
    "A": (25.0330, 121.5654),  # Taipei 101
    "B": (25.0174, 121.5405),  # NTU
    "C": (25.0878, 121.5241),  # Shilin
    "D": (25.0478, 121.5170),  # Main Station
}

# Route 1: A → B → C → D
route1 = [places["A"], places["B"], places["C"], places["D"]]

# Route 2: A → D → C → B
route2 = [places["A"], places["D"], places["C"], places["B"]]

# TODO: Calculate and compare total distances
dist1 = total_distance(route1)
dist2 = total_distance(route2)

print(f"Route 1 (A→B→C→D): {dist1:.2f} km")
print(f"Route 2 (A→D→C→B): {dist2:.2f} km")
print(f"Difference: {abs(dist1 - dist2):.2f} km")
print(f"Better route: {'Route 1' if dist1 < dist2 else 'Route 2'}")
```

---

## Submission

Save your completed lab as `week02-1_lab_solution.py`.

### Checklist

- [ ] Exercise 1: List creation and modification
- [ ] Exercise 2: For loops with enumerate and range
- [ ] Exercise 3: Processing consecutive pairs
- [ ] Exercise 4: map() and filter() functions
- [ ] Exercise 5: Route calculator with statistics
- [ ] Exercise 6: Route comparison (bonus)
