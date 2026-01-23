# Week 2-1 Lecture: Lists, Loops & The Route

## Learning Objectives

By the end of this lecture, students will be able to:
1. Create and manipulate lists
2. Use `for` loops to iterate over sequences
3. Understand `range()`, `enumerate()`, and `zip()`
4. Apply `map()` and `filter()` for data transformation
5. Calculate total route distances using loops

---

## Part 1: Introduction to Lists

### What is a List?

A list is a **mutable** (changeable) ordered collection of items.

```python
# Creating lists
numbers = [1, 2, 3, 4, 5]
cities = ["Taipei", "Tokyo", "Seoul"]
mixed = [1, "hello", 3.14, True]
empty = []

# Lists can contain tuples (coordinates!)
route = [
    (25.0330, 121.5654),
    (25.0478, 121.5170),
    (25.0174, 121.5405),
]
```

### Lists vs Tuples

| Feature | List | Tuple |
|---------|------|-------|
| Syntax | `[1, 2, 3]` | `(1, 2, 3)` |
| Mutable | ✓ Yes | ✗ No |
| Use case | Collections that change | Fixed data (coordinates) |

```python
# List - can be modified
cities = ["Taipei", "Tokyo"]
cities.append("Seoul")      # OK!
cities[0] = "Kaohsiung"     # OK!

# Tuple - cannot be modified
coord = (25.0330, 121.5654)
# coord[0] = 26.0           # Error!
```

---

## Part 2: Accessing List Elements

### Indexing

```python
cities = ["Taipei", "Tokyo", "Seoul", "Bangkok", "Singapore"]

# Positive indexing (from start)
print(cities[0])    # "Taipei" (first element)
print(cities[1])    # "Tokyo"
print(cities[4])    # "Singapore" (last element)

# Negative indexing (from end)
print(cities[-1])   # "Singapore" (last)
print(cities[-2])   # "Bangkok" (second to last)
```

### Slicing

```python
cities = ["Taipei", "Tokyo", "Seoul", "Bangkok", "Singapore"]

# Slicing: list[start:end] (end is exclusive)
print(cities[1:3])    # ["Tokyo", "Seoul"]
print(cities[:3])     # ["Taipei", "Tokyo", "Seoul"] (first 3)
print(cities[2:])     # ["Seoul", "Bangkok", "Singapore"] (from index 2)
print(cities[::2])    # ["Taipei", "Seoul", "Singapore"] (every 2nd)
print(cities[::-1])   # Reversed list
```

### Length

```python
cities = ["Taipei", "Tokyo", "Seoul"]
print(len(cities))  # 3
```

---

## Part 3: Modifying Lists

### Adding Elements

```python
cities = ["Taipei", "Tokyo"]

# append() - add to end
cities.append("Seoul")
print(cities)  # ["Taipei", "Tokyo", "Seoul"]

# insert() - add at specific index
cities.insert(1, "Osaka")
print(cities)  # ["Taipei", "Osaka", "Tokyo", "Seoul"]

# extend() - add multiple elements
cities.extend(["Bangkok", "Singapore"])
print(cities)  # ["Taipei", "Osaka", "Tokyo", "Seoul", "Bangkok", "Singapore"]

# + operator - concatenate lists
more_cities = cities + ["Jakarta", "Manila"]
```

### Removing Elements

```python
cities = ["Taipei", "Tokyo", "Seoul", "Bangkok"]

# remove() - remove by value
cities.remove("Tokyo")
print(cities)  # ["Taipei", "Seoul", "Bangkok"]

# pop() - remove by index (returns the removed element)
last = cities.pop()      # Remove last
print(last)              # "Bangkok"
print(cities)            # ["Taipei", "Seoul"]

first = cities.pop(0)    # Remove first
print(first)             # "Taipei"

# del - delete by index
del cities[0]

# clear() - remove all elements
cities.clear()
print(cities)  # []
```

### Modifying Elements

```python
cities = ["Taipei", "Tokyo", "Seoul"]

# Change single element
cities[1] = "Osaka"
print(cities)  # ["Taipei", "Osaka", "Seoul"]

# Change multiple elements
cities[1:3] = ["Kyoto", "Nara"]
print(cities)  # ["Taipei", "Kyoto", "Nara"]
```

---

## Part 4: For Loops

### Basic For Loop

```python
cities = ["Taipei", "Tokyo", "Seoul"]

# Iterate over each element
for city in cities:
    print(f"I want to visit {city}")

# Output:
# I want to visit Taipei
# I want to visit Tokyo
# I want to visit Seoul
```

### Loop with Index using `enumerate()`

```python
cities = ["Taipei", "Tokyo", "Seoul"]

# enumerate() gives both index and value
for index, city in enumerate(cities):
    print(f"{index + 1}. {city}")

# Output:
# 1. Taipei
# 2. Tokyo
# 3. Seoul

# Start from different number
for i, city in enumerate(cities, start=1):
    print(f"{i}. {city}")
```

### The `range()` Function

```python
# range(stop) - 0 to stop-1
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# range(start, stop) - start to stop-1
for i in range(2, 5):
    print(i)  # 2, 3, 4

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Counting backwards
for i in range(5, 0, -1):
    print(i)  # 5, 4, 3, 2, 1
```

### Loop Over Coordinate Pairs

```python
route = [
    (25.0330, 121.5654),  # Taipei 101
    (25.0478, 121.5170),  # Main Station
    (25.0174, 121.5405),  # NTU
]

# Unpack tuples in the loop
for lat, lon in route:
    print(f"Location: ({lat}, {lon})")

# With index
for i, (lat, lon) in enumerate(route):
    print(f"Stop {i + 1}: ({lat}, {lon})")
```

---

## Part 5: Processing Pairs with `zip()`

### The `zip()` Function

`zip()` combines multiple sequences element by element.

```python
names = ["Taipei 101", "Main Station", "NTU"]
coords = [(25.0330, 121.5654), (25.0478, 121.5170), (25.0174, 121.5405)]

# Combine names and coordinates
for name, coord in zip(names, coords):
    print(f"{name}: {coord}")

# Output:
# Taipei 101: (25.033, 121.5654)
# Main Station: (25.0478, 121.517)
# NTU: (25.0174, 121.5405)
```

### Iterating Over Consecutive Pairs

This is crucial for calculating route distances!

```python
route = [
    (25.0330, 121.5654),  # A
    (25.0478, 121.5170),  # B
    (25.0174, 121.5405),  # C
]

# Method 1: Using index
for i in range(len(route) - 1):
    start = route[i]
    end = route[i + 1]
    print(f"Segment {i + 1}: {start} → {end}")

# Method 2: Using zip with slicing
for start, end in zip(route[:-1], route[1:]):
    print(f"{start} → {end}")

# Explanation:
# route[:-1] = [A, B]     (all except last)
# route[1:]  = [B, C]     (all except first)
# zip gives:   (A,B), (B,C)
```

---

## Part 6: `map()` and `filter()`

### The `map()` Function

Apply a function to every element.

```python
# Convert all temperatures from Celsius to Fahrenheit
celsius = [0, 10, 20, 30, 40]

def to_fahrenheit(c):
    return c * 9/5 + 32

fahrenheit = list(map(to_fahrenheit, celsius))
print(fahrenheit)  # [32.0, 50.0, 68.0, 86.0, 104.0]

# Using lambda (anonymous function)
fahrenheit = list(map(lambda c: c * 9/5 + 32, celsius))
```

### `map()` with Coordinates

```python
coords = [(25.0330, 121.5654), (25.0478, 121.5170), (25.0174, 121.5405)]

# Extract all latitudes
latitudes = list(map(lambda c: c[0], coords))
print(latitudes)  # [25.033, 25.0478, 25.0174]

# Format all coordinates
formatted = list(map(lambda c: f"({c[0]:.2f}, {c[1]:.2f})", coords))
print(formatted)  # ['(25.03, 121.57)', '(25.05, 121.52)', '(25.02, 121.54)']
```

### The `filter()` Function

Keep only elements that pass a test.

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Keep only even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]

# Keep numbers greater than 5
big = list(filter(lambda x: x > 5, numbers))
print(big)  # [6, 7, 8, 9, 10]
```

### `filter()` with Coordinates

```python
coords = [
    (25.0330, 121.5654),  # Taipei 101
    (35.6586, 139.7454),  # Tokyo Tower (far!)
    (25.0478, 121.5170),  # Main Station
    (37.5665, 126.9780),  # Seoul (far!)
    (25.0174, 121.5405),  # NTU
]

# Keep only coordinates in Taiwan (roughly lat 22-26, lon 120-122)
taiwan_coords = list(filter(
    lambda c: 22 <= c[0] <= 26 and 120 <= c[1] <= 122,
    coords
))
print(taiwan_coords)
# [(25.033, 121.5654), (25.0478, 121.517), (25.0174, 121.5405)]
```

---

## Part 7: Calculating Route Distance

### Complete Example

```python
import math

def haversine(coord1, coord2):
    """Calculate distance between two coordinates in km."""
    R = 6371
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


# Our route
route = [
    (25.0330, 121.5654),  # Taipei 101
    (25.0339, 121.5645),  # Din Tai Fung
    (25.0329, 121.5598),  # Yongkang Street
    (25.0279, 121.5595),  # Daan Park
    (25.0174, 121.5405),  # NTU
]

# Calculate total distance
total_distance = 0
segment_distances = []

for i in range(len(route) - 1):
    dist = haversine(route[i], route[i + 1])
    segment_distances.append(dist)
    total_distance += dist
    print(f"Segment {i + 1}: {dist:.3f} km")

print(f"\nTotal route distance: {total_distance:.2f} km")
print(f"Average segment: {total_distance / len(segment_distances):.3f} km")
```

### Using List Comprehension

```python
# Calculate all segment distances in one line
segment_distances = [
    haversine(route[i], route[i + 1])
    for i in range(len(route) - 1)
]

total_distance = sum(segment_distances)
print(f"Total: {total_distance:.2f} km")
```

---

## Summary

| Concept | Example | Description |
|---------|---------|-------------|
| List | `[1, 2, 3]` | Mutable ordered collection |
| Index | `lst[0]`, `lst[-1]` | Access by position |
| Slice | `lst[1:3]` | Get a portion |
| `for` loop | `for x in lst:` | Iterate over elements |
| `enumerate()` | `for i, x in enumerate(lst):` | Index + value |
| `range()` | `range(5)` | Generate numbers |
| `zip()` | `zip(a, b)` | Combine sequences |
| `map()` | `map(func, lst)` | Transform all elements |
| `filter()` | `filter(func, lst)` | Keep matching elements |

---

## Practice: 99 Problems

Complete **P01–P10 (Lists)** from *99 Problems in Python* to master:
- Finding the last element
- Reversing a list
- Checking if palindrome
- Flattening nested lists
- Removing duplicates

These skills are essential for processing route data!
