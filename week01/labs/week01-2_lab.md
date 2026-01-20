# Week 1-2 Lab: Functions & Distance Logic

## Lab Overview

In this lab, you will practice:
- Defining and calling functions
- Working with the `math` module
- Implementing the Haversine formula
- Calculating distances between real-world locations

---

## Exercise 1: Basic Functions (10 minutes)

### Task 1.1: Your First Function

Create a simple function that greets a user:

```python
# TODO: Define a function called 'greet' that takes a name and prints a greeting

def greet(name):
    """Print a greeting message."""
    # Your code here
    print(f"___")  # Fill in the greeting

# Test your function
greet("Alice")    # Should print: Hello, Alice!
greet("Bob")      # Should print: Hello, Bob!
```

### Task 1.2: Function with Return Value

Create a function that converts Celsius to Fahrenheit:

```python
def celsius_to_fahrenheit(celsius):
    """
    Convert temperature from Celsius to Fahrenheit.

    Formula: F = C × 9/5 + 32
    """
    # TODO: Implement the conversion
    fahrenheit = ___
    return fahrenheit

# Test your function
print(celsius_to_fahrenheit(0))    # Should print: 32.0
print(celsius_to_fahrenheit(100))  # Should print: 212.0
print(celsius_to_fahrenheit(25))   # Should print: 77.0
```

### Task 1.3: Function with Multiple Parameters

Create a function that takes a coordinate tuple and returns a formatted string:

```python
def format_coordinate(coord, precision=4):
    """
    Format a coordinate tuple as a readable string.

    Args:
        coord: (latitude, longitude) tuple
        precision: number of decimal places (default 4)

    Returns:
        Formatted string like "25.0330°N, 121.5654°E"
    """
    lat, lon = coord

    # Determine N/S and E/W
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"

    # TODO: Return the formatted string with the specified precision
    # Hint: Use f-string with :.{precision}f format
    return f"___"

# Test your function
taipei = (25.0330, 121.5654)
sydney = (-33.8568, 151.2153)

print(format_coordinate(taipei))           # 25.0330°N, 121.5654°E
print(format_coordinate(sydney))           # 33.8568°S, 151.2153°E
print(format_coordinate(taipei, 2))        # 25.03°N, 121.57°E
```

---

## Exercise 2: The Math Module (10 minutes)

### Task 2.1: Exploring Math Functions

Use the `math` module to perform calculations:

```python
import math

# TODO: Calculate and print the following:

# 1. Square root of 144
sqrt_result = math.sqrt(___)
print(f"√144 = {sqrt_result}")

# 2. 2 raised to the power of 10
power_result = math.pow(___, ___)
print(f"2¹⁰ = {power_result}")

# 3. The value of π (pi)
print(f"π = {math.___}")

# 4. The value of e (Euler's number)
print(f"e = {math.___}")

# 5. Ceiling and floor of 3.7
print(f"ceil(3.7) = {math.ceil(3.7)}")
print(f"floor(3.7) = {math.___}")
```

### Task 2.2: Trigonometry with Radians

Practice converting between degrees and radians:

```python
import math

# TODO: Convert these angles from degrees to radians
angles_degrees = [0, 30, 45, 60, 90, 180, 360]

print("Degrees → Radians conversion:")
for deg in angles_degrees:
    rad = math.radians(___)
    print(f"  {deg}° = {rad:.4f} radians")

# TODO: Calculate sin, cos for each angle
print("\nTrigonometric values:")
for deg in [0, 30, 45, 60, 90]:
    rad = math.radians(deg)
    sin_val = math.sin(___)
    cos_val = math.cos(___)
    print(f"  {deg}°: sin = {sin_val:.4f}, cos = {cos_val:.4f}")
```

### Task 2.3: Distance in 2D (Pythagorean Theorem)

Implement a simple 2D distance function:

```python
import math

def distance_2d(point1, point2):
    """
    Calculate Euclidean distance between two 2D points.

    Formula: d = √((x2-x1)² + (y2-y1)²)
    """
    x1, y1 = point1
    x2, y2 = point2

    # TODO: Implement the Pythagorean theorem
    dx = x2 - x1
    dy = ___

    distance = math.sqrt(___)
    return distance

# Test with simple points
print(distance_2d((0, 0), (3, 4)))    # Should print: 5.0 (3-4-5 triangle)
print(distance_2d((1, 1), (4, 5)))    # Should print: 5.0
print(distance_2d((0, 0), (1, 1)))    # Should print: ~1.414 (√2)
```

---

## Exercise 3: Implementing Haversine (20 minutes)

### Task 3.1: Step-by-Step Haversine

Implement the Haversine formula step by step:

```python
import math

def haversine_step_by_step(coord1, coord2):
    """
    Calculate great-circle distance with detailed steps.
    """
    # Earth's radius in kilometers
    R = 6371

    # Step 1: Extract coordinates
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    print(f"Point 1: ({lat1}, {lon1})")
    print(f"Point 2: ({lat2}, {lon2})")

    # Step 2: Convert to radians
    # TODO: Convert all four values to radians
    lat1_rad = math.radians(___)
    lat2_rad = math.radians(___)
    lon1_rad = math.radians(___)
    lon2_rad = math.radians(___)
    print(f"In radians - lat1: {lat1_rad:.4f}, lon1: {lon1_rad:.4f}")

    # Step 3: Calculate differences
    # TODO: Calculate dlat and dlon
    dlat = lat2_rad - lat1_rad
    dlon = ___
    print(f"Differences - dlat: {dlat:.6f}, dlon: {dlon:.6f}")

    # Step 4: Apply Haversine formula
    # a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
    # TODO: Calculate 'a'
    a = math.sin(dlat/2)**2 + \
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    print(f"Intermediate value a: {a:.6f}")

    # Step 5: Calculate 'c'
    # c = 2 × asin(√a)
    # TODO: Calculate 'c'
    c = 2 * math.asin(math.sqrt(___))
    print(f"Intermediate value c: {c:.6f}")

    # Step 6: Calculate distance
    # d = R × c
    distance = R * c
    print(f"Distance: {distance:.2f} km")

    return distance

# Test with Taipei 101 to Tokyo Tower
taipei = (25.0330, 121.5654)
tokyo = (35.6586, 139.7454)

print("=" * 50)
print("Calculating distance from Taipei 101 to Tokyo Tower")
print("=" * 50)
result = haversine_step_by_step(taipei, tokyo)
print(f"\nFinal Result: {result:.2f} km")
```

### Task 3.2: Clean Haversine Function

Now implement a clean version without the print statements:

```python
import math

def haversine(coord1, coord2):
    """
    Calculate the great-circle distance between two points on Earth.

    Args:
        coord1: (latitude, longitude) tuple for point 1
        coord2: (latitude, longitude) tuple for point 2

    Returns:
        Distance in kilometers
    """
    R = 6371  # Earth's radius in km

    # TODO: Implement the complete Haversine formula
    # Copy your working code from Task 3.1 (without print statements)

    pass  # Replace with your implementation

# Test cases
test_cases = [
    (("Taipei 101", (25.0330, 121.5654)), ("Tokyo Tower", (35.6586, 139.7454))),
    (("Taipei 101", (25.0330, 121.5654)), ("Main Station", (25.0478, 121.5170))),
    (("New York", (40.7128, -74.0060)), ("London", (51.5074, -0.1278))),
    (("Sydney", (-33.8688, 151.2093)), ("Tokyo", (35.6762, 139.6503))),
]

print("Distance Calculations:")
print("-" * 50)
for (name1, coord1), (name2, coord2) in test_cases:
    dist = haversine(coord1, coord2)
    print(f"{name1} → {name2}: {dist:.2f} km")
```

### Task 3.3: Haversine with Unit Conversion

Extend the Haversine function to support different units:

```python
import math

def haversine(coord1, coord2, unit='km'):
    """
    Calculate the great-circle distance between two points.

    Args:
        coord1: (latitude, longitude) tuple for point 1
        coord2: (latitude, longitude) tuple for point 2
        unit: 'km' for kilometers, 'mi' for miles, 'm' for meters

    Returns:
        Distance in the specified unit
    """
    # Earth's radius in km
    R = 6371

    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    distance_km = R * c

    # TODO: Convert to the requested unit
    if unit == 'km':
        return distance_km
    elif unit == 'mi':
        # 1 km = 0.621371 miles
        return distance_km * ___
    elif unit == 'm':
        # 1 km = 1000 meters
        return distance_km * ___
    else:
        raise ValueError(f"Unknown unit: {unit}")

# Test
taipei = (25.0330, 121.5654)
main_station = (25.0478, 121.5170)

print(f"Distance in km: {haversine(taipei, main_station, 'km'):.2f} km")
print(f"Distance in miles: {haversine(taipei, main_station, 'mi'):.2f} mi")
print(f"Distance in meters: {haversine(taipei, main_station, 'm'):.0f} m")
```

---

## Exercise 4: Real-World Application (15 minutes)

### Task 4.1: Find the Nearest Location

Write a function to find the nearest location from a list:

```python
import math

# Use your haversine function from Task 3.2

def find_nearest(current_location, locations):
    """
    Find the nearest location from a list of locations.

    Args:
        current_location: (latitude, longitude) tuple
        locations: List of (name, latitude, longitude) tuples

    Returns:
        (name, distance) of the nearest location
    """
    nearest_name = None
    nearest_distance = float('inf')  # Start with infinity

    # TODO: Loop through locations and find the nearest one
    for name, lat, lon in locations:
        location_coord = (lat, lon)
        distance = haversine(current_location, location_coord)

        if distance < nearest_distance:
            nearest_distance = ___
            nearest_name = ___

    return nearest_name, nearest_distance

# Test: Find nearest MRT station to Taipei 101
taipei_101 = (25.0330, 121.5654)

mrt_stations = [
    ("Taipei 101/World Trade Center", 25.0330, 121.5637),
    ("Xiangshan", 25.0329, 121.5707),
    ("Taipei City Hall", 25.0408, 121.5679),
    ("Yongchun", 25.0403, 121.5762),
    ("Houshanpi", 25.0446, 121.5824),
]

nearest, distance = find_nearest(taipei_101, mrt_stations)
print(f"Nearest MRT station to Taipei 101: {nearest} ({distance*1000:.0f} meters)")
```

### Task 4.2: Sort Locations by Distance

Sort a list of locations by their distance from a reference point:

```python
def sort_by_distance(reference, locations):
    """
    Sort locations by distance from a reference point.

    Args:
        reference: (latitude, longitude) tuple
        locations: List of (name, latitude, longitude) tuples

    Returns:
        Sorted list of (name, distance) tuples
    """
    # TODO: Create a list of (name, distance) and sort it
    distances = []

    for name, lat, lon in locations:
        dist = haversine(reference, (lat, lon))
        distances.append((name, dist))

    # Sort by distance (second element of tuple)
    distances.sort(key=lambda x: x[___])  # Fill in the index

    return distances

# Test: Sort MRT stations by distance from Taipei 101
sorted_stations = sort_by_distance(taipei_101, mrt_stations)

print("MRT stations sorted by distance from Taipei 101:")
for i, (name, dist) in enumerate(sorted_stations, 1):
    print(f"  {i}. {name}: {dist*1000:.0f} m")
```

### Task 4.3: Walking Time Estimate

Estimate walking time based on distance:

```python
def estimate_walking_time(distance_km, speed_kmh=5.0):
    """
    Estimate walking time based on distance.

    Args:
        distance_km: Distance in kilometers
        speed_kmh: Walking speed in km/h (default 5.0)

    Returns:
        (hours, minutes) tuple
    """
    # TODO: Calculate time in hours, then convert to hours and minutes
    time_hours = distance_km / speed_kmh

    hours = int(time_hours)
    minutes = int((time_hours - hours) * 60)

    return hours, minutes

def format_walking_time(hours, minutes):
    """Format walking time as a readable string."""
    if hours == 0:
        return f"{minutes} min"
    elif minutes == 0:
        return f"{hours} hr"
    else:
        return f"{hours} hr {minutes} min"

# Test: Walking times to MRT stations
print("\nWalking time from Taipei 101 to MRT stations:")
for name, dist in sorted_stations:
    hours, minutes = estimate_walking_time(dist)
    time_str = format_walking_time(hours, minutes)
    print(f"  {name}: {time_str}")
```

---

## Exercise 5: Challenge - Route Calculator (10 minutes)

### Task 5.1: Calculate Total Route Distance

Create a function that calculates the total distance of a route:

```python
def calculate_route_distance(route):
    """
    Calculate the total distance of a route.

    Args:
        route: List of (latitude, longitude) tuples

    Returns:
        Total distance in kilometers
    """
    if len(route) < 2:
        return 0.0

    total = 0.0

    # TODO: Sum up distances between consecutive points
    for i in range(len(route) - 1):
        dist = haversine(route[i], route[i + 1])
        total += ___

    return total

# Test: A walking tour in Taipei
walking_tour = [
    (25.0330, 121.5654),  # Taipei 101
    (25.0339, 121.5645),  # Din Tai Fung
    (25.0329, 121.5598),  # Yongkang Street
    (25.0279, 121.5595),  # Daan Park
    (25.0174, 121.5405),  # NTU
]

total_distance = calculate_route_distance(walking_tour)
hours, minutes = estimate_walking_time(total_distance)

print(f"Walking Tour Statistics:")
print(f"  Total distance: {total_distance:.2f} km")
print(f"  Estimated walking time: {format_walking_time(hours, minutes)}")
print(f"  Number of stops: {len(walking_tour)}")
```

### Task 5.2: Detailed Route Breakdown

Print a detailed breakdown of each segment:

```python
def print_route_details(locations):
    """
    Print detailed information about each segment of a route.

    Args:
        locations: List of (name, latitude, longitude) tuples
    """
    print("Route Details:")
    print("=" * 60)

    total_distance = 0

    for i in range(len(locations) - 1):
        name1, lat1, lon1 = locations[i]
        name2, lat2, lon2 = locations[i + 1]

        dist = haversine((lat1, lon1), (lat2, lon2))
        total_distance += dist

        hours, minutes = estimate_walking_time(dist)
        time_str = format_walking_time(hours, minutes)

        print(f"Segment {i + 1}: {name1} → {name2}")
        print(f"  Distance: {dist:.2f} km ({dist*1000:.0f} m)")
        print(f"  Walking time: {time_str}")
        print()

    total_hours, total_minutes = estimate_walking_time(total_distance)
    print("=" * 60)
    print(f"TOTAL: {total_distance:.2f} km, {format_walking_time(total_hours, total_minutes)}")

# Test with named locations
taipei_tour = [
    ("Taipei 101", 25.0330, 121.5654),
    ("Din Tai Fung", 25.0339, 121.5645),
    ("Yongkang Street", 25.0329, 121.5598),
    ("Daan Park", 25.0279, 121.5595),
    ("NTU Main Gate", 25.0174, 121.5405),
]

print_route_details(taipei_tour)
```

---

## Submission

Save your completed lab as `week01-2_lab_solution.py` and ensure all exercises run without errors.

### Checklist

- [ ] Exercise 1: Basic functions working correctly
- [ ] Exercise 2: Math module exercises completed
- [ ] Exercise 3: Haversine function implemented and tested
- [ ] Exercise 4: Nearest location and sorting functions working
- [ ] Exercise 5: Route calculator completed

---

## Bonus Challenge

Implement a function that finds the **optimal order** to visit a set of locations (minimizing total distance). This is a preview of the Traveling Salesperson Problem we'll cover in Week 10!

```python
from itertools import permutations

def find_shortest_route(start, locations):
    """
    Find the shortest route to visit all locations starting from 'start'.

    Args:
        start: (latitude, longitude) of starting point
        locations: List of (name, latitude, longitude) tuples to visit

    Returns:
        (best_order, total_distance) where best_order is a list of names
    """
    # TODO: Try all permutations and find the one with minimum distance
    # Hint: Use itertools.permutations

    pass  # Your implementation here
```
