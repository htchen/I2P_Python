# Week 1-2 Lecture: Functions & Distance Logic

## Learning Objectives

By the end of this lecture, students will be able to:
1. Define and call Python functions
2. Understand function parameters and return values
3. Use the `math` module for mathematical operations
4. Implement the Haversine formula to calculate distances
5. Understand the concept of abstraction

---

## Part 1: Introduction to Functions

### Why Functions?

Without functions, we'd have to repeat code:

```python
# Without functions - repetitive!
lat1, lon1 = 25.0330, 121.5654
lat2, lon2 = 25.0478, 121.5170

# Calculate distance... (many lines of math)
# ... then repeat for every pair of points!
```

With functions, we write once and reuse:

```python
# With functions - clean and reusable!
distance1 = calculate_distance(taipei_101, main_station)
distance2 = calculate_distance(taipei_101, ntu)
distance3 = calculate_distance(main_station, ntu)
```

### Defining a Function

```python
def greet():
    """A simple function that prints a greeting."""
    print("Hello, World!")

# Calling the function
greet()  # Output: Hello, World!
```

### Function Anatomy

```python
def function_name(parameter1, parameter2):
    """
    Docstring: Describes what the function does.

    Args:
        parameter1: Description of first parameter
        parameter2: Description of second parameter

    Returns:
        Description of return value
    """
    # Function body
    result = parameter1 + parameter2
    return result
```

---

## Part 2: Parameters and Arguments

### Parameters vs Arguments

```python
# 'a' and 'b' are PARAMETERS (in the definition)
def add(a, b):
    return a + b

# 5 and 3 are ARGUMENTS (in the call)
result = add(5, 3)
```

### Positional Arguments

```python
def describe_location(name, lat, lon):
    print(f"{name} is at ({lat}, {lon})")

# Arguments match parameters by position
describe_location("Taipei 101", 25.0330, 121.5654)
# Output: Taipei 101 is at (25.033, 121.5654)
```

### Keyword Arguments

```python
# Can specify by name (order doesn't matter)
describe_location(lat=25.0330, name="Taipei 101", lon=121.5654)
# Output: Taipei 101 is at (25.033, 121.5654)
```

### Default Parameters

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")              # Hello, Alice!
greet("Bob", "Good morning")  # Good morning, Bob!
```

### Tuple Parameters

```python
def get_latitude(coord):
    """Extract latitude from a coordinate tuple."""
    return coord[0]

def get_longitude(coord):
    """Extract longitude from a coordinate tuple."""
    return coord[1]

taipei = (25.0330, 121.5654)
print(get_latitude(taipei))   # 25.0330
print(get_longitude(taipei))  # 121.5654
```

---

## Part 3: Return Values

### The `return` Statement

```python
def add(a, b):
    return a + b  # Returns the sum

result = add(5, 3)
print(result)  # 8
```

### Multiple Return Values

```python
def get_bounds(coords):
    """Return min and max of a list of coordinates."""
    latitudes = [c[0] for c in coords]
    longitudes = [c[1] for c in coords]

    return min(latitudes), max(latitudes), min(longitudes), max(longitudes)

places = [(25.0330, 121.5654), (25.0478, 121.5170), (25.0174, 121.5405)]
min_lat, max_lat, min_lon, max_lon = get_bounds(places)
print(f"Latitude range: {min_lat} to {max_lat}")
```

### Functions Without Return

```python
def print_location(coord):
    print(f"Location: ({coord[0]}, {coord[1]})")
    # No return statement

result = print_location((25.0, 121.5))
print(result)  # None (default return value)
```

---

## Part 4: The `math` Module

### Importing the Math Module

```python
import math

# Using functions from math
print(math.sqrt(16))    # 4.0 (square root)
print(math.pow(2, 3))   # 8.0 (2^3)
print(math.pi)          # 3.141592653589793
```

### Essential Math Functions for Geolocation

```python
import math

# Trigonometric functions (input in RADIANS, not degrees!)
print(math.sin(math.pi / 2))  # 1.0 (sin of 90°)
print(math.cos(0))            # 1.0 (cos of 0°)

# Converting degrees to radians
degrees = 90
radians = math.radians(degrees)  # 1.5707... (π/2)
print(radians)

# Converting radians to degrees
print(math.degrees(math.pi))  # 180.0

# Other useful functions
print(math.sqrt(2))      # 1.414... (square root)
print(math.asin(1))      # 1.5707... (arc sine, returns radians)
print(math.acos(0))      # 1.5707... (arc cosine)
```

### ⚠️ Degrees vs Radians

```python
import math

# WRONG: Using degrees directly
angle_degrees = 45
wrong = math.sin(angle_degrees)  # Wrong! This treats 45 as radians
print(f"Wrong: sin(45) = {wrong}")  # ~0.85 (incorrect)

# CORRECT: Convert to radians first
angle_radians = math.radians(angle_degrees)
correct = math.sin(angle_radians)
print(f"Correct: sin(45°) = {correct}")  # ~0.707 (correct)
```

---

## Part 5: The Haversine Formula

### Why Haversine?

The Earth is a sphere (approximately). Straight-line distance on a map doesn't work!

```
     ___________
    /           \
   /   Taipei    \
  |    *---------*| ← Straight line goes THROUGH Earth!
  |      Tokyo    |
   \             /
    \___________/

The Haversine formula calculates distance ALONG the surface.
```

### The Formula (Don't Memorize!)

```
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
c = 2 × atan2(√a, √(1-a))
d = R × c

Where:
- Δlat = lat2 - lat1 (difference in latitude)
- Δlon = lon2 - lon1 (difference in longitude)
- R = Earth's radius (6371 km)
- d = distance in km
```

### Implementing Haversine in Python

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
    # Earth's radius in kilometers
    R = 6371

    # Extract coordinates
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon1_rad = math.radians(lon1)
    lon2_rad = math.radians(lon2)

    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + \
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2

    c = 2 * math.asin(math.sqrt(a))

    # Distance
    distance = R * c

    return distance
```

### Using the Haversine Function

```python
# Define locations
taipei_101 = (25.0330, 121.5654)
tokyo_tower = (35.6586, 139.7454)
main_station = (25.0478, 121.5170)

# Calculate distances
dist1 = haversine(taipei_101, tokyo_tower)
dist2 = haversine(taipei_101, main_station)

print(f"Taipei 101 to Tokyo Tower: {dist1:.2f} km")
# Output: Taipei 101 to Tokyo Tower: 2111.51 km

print(f"Taipei 101 to Main Station: {dist2:.2f} km")
# Output: Taipei 101 to Main Station: 5.37 km
```

---

## Part 6: Abstraction

### What is Abstraction?

Abstraction means hiding complex details behind a simple interface.

```python
# Without abstraction - you need to understand all the math
import math
lat1, lon1 = 25.0330, 121.5654
lat2, lon2 = 35.6586, 139.7454
R = 6371
lat1_rad = math.radians(lat1)
lat2_rad = math.radians(lat2)
lon1_rad = math.radians(lon1)
lon2_rad = math.radians(lon2)
dlat = lat2_rad - lat1_rad
dlon = lon2_rad - lon1_rad
a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
c = 2 * math.asin(math.sqrt(a))
distance = R * c

# With abstraction - simple and clear!
distance = haversine(taipei_101, tokyo_tower)
```

### Benefits of Abstraction

1. **Simplicity**: Users don't need to understand the implementation
2. **Reusability**: Write once, use anywhere
3. **Maintainability**: Fix bugs in one place
4. **Testing**: Test the function once, trust it everywhere

---

## Part 7: Compact Haversine Implementation

Once you understand the formula, you can write it more concisely:

```python
import math

def haversine(coord1, coord2):
    """Calculate distance between two coordinates in km."""
    R = 6371  # Earth's radius in km

    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2

    return R * 2 * math.asin(math.sqrt(a))
```

---

## Summary

| Concept | Example | Key Point |
|---------|---------|-----------|
| Function definition | `def func():` | Reusable code block |
| Parameters | `def add(a, b):` | Inputs to a function |
| Return value | `return result` | Output from a function |
| `math` module | `import math` | Mathematical functions |
| `math.radians()` | `math.radians(90)` | Degrees → Radians |
| Haversine | `haversine(p1, p2)` | Distance on a sphere |
| Abstraction | Hide complexity | Simple interface |

---

## Practice Exercise

Implement a function `km_to_miles(km)` that converts kilometers to miles (1 km ≈ 0.621371 miles), then modify the haversine function to accept an optional `unit` parameter:

```python
def haversine(coord1, coord2, unit='km'):
    """
    Calculate distance between two coordinates.

    Args:
        coord1, coord2: Coordinate tuples
        unit: 'km' or 'miles'

    Returns:
        Distance in the specified unit
    """
    # Your implementation here
    pass
```
