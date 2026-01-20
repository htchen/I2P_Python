# Week 1-1 Lecture: Variables & The Coordinate System

## Learning Objectives

By the end of this lecture, students will be able to:
1. Understand and use Python variables
2. Work with different numeric types (int, float)
3. Create and access tuples
4. Understand the geographic coordinate system (latitude/longitude)
5. Store locations as coordinate tuples

---

## Part 1: Introduction to Variables

### What is a Variable?

A variable is a name that refers to a value stored in memory.

```python
# Creating variables
name = "Taipei"
population = 2600000
area_km2 = 271.8

print(name)        # Taipei
print(population)  # 2600000
print(area_km2)    # 271.8
```

### Variable Naming Rules

```python
# Valid variable names
city_name = "Taipei"
city2 = "Kaohsiung"
_private = "internal"
CamelCase = "works but not recommended"

# Invalid variable names (will cause errors)
# 2city = "error"      # Cannot start with number
# my-city = "error"    # No hyphens allowed
# class = "error"      # Cannot use reserved words
```

### Python Naming Convention (PEP 8)

```python
# Use snake_case for variables and functions
user_name = "Alice"
max_distance = 100

# Use UPPER_CASE for constants
PI = 3.14159
EARTH_RADIUS_KM = 6371
```

---

## Part 2: Numeric Types

### Integers (int)

Whole numbers without decimal points.

```python
population = 2600000
year = 2024
negative_number = -50

# Type checking
print(type(population))  # <class 'int'>

# Integer operations
a = 10
b = 3
print(a + b)   # 13 (addition)
print(a - b)   # 7  (subtraction)
print(a * b)   # 30 (multiplication)
print(a // b)  # 3  (integer division - floor)
print(a % b)   # 1  (modulo - remainder)
print(a ** b)  # 1000 (exponentiation)
```

### Floating Point Numbers (float)

Numbers with decimal points.

```python
latitude = 25.0330
longitude = 121.5654
pi = 3.14159

# Type checking
print(type(latitude))  # <class 'float'>

# Float operations
print(10 / 3)    # 3.3333... (true division)
print(10.0 + 3)  # 13.0 (int + float = float)

# Scientific notation
distance = 1.5e6  # 1,500,000
tiny = 1e-6       # 0.000001
```

### ⚠️ Float Precision Warning

```python
# Floats have limited precision!
print(0.1 + 0.2)  # 0.30000000000000004 (not exactly 0.3!)

# For coordinates, this precision is usually fine
# 6 decimal places ≈ 10cm accuracy
lat = 25.033012  # This is precise enough for our purposes
```

---

## Part 3: The Coordinate System

### Understanding Latitude and Longitude

```
                    North Pole (90°N)
                         │
                         │
    ─────────────────────┼───────────────────── Equator (0°)
                         │
                         │
                    South Pole (90°S)

    180°W ←────────── 0° (Prime Meridian) ──────────→ 180°E
```

### Latitude (緯度)
- Measures North-South position
- Range: -90° (South Pole) to +90° (North Pole)
- 0° is the Equator
- Taiwan is around 22°N to 25°N

### Longitude (經度)
- Measures East-West position
- Range: -180° to +180°
- 0° is the Prime Meridian (Greenwich, London)
- Taiwan is around 120°E to 122°E

### Examples

```python
# Major cities with coordinates (latitude, longitude)
taipei = (25.0330, 121.5654)      # Taipei 101
tokyo = (35.6762, 139.6503)       # Tokyo Tower
new_york = (40.7484, -73.9857)    # Empire State Building
sydney = (-33.8568, 151.2153)     # Sydney Opera House

# Notice:
# - Taipei: positive lat (North), positive lon (East)
# - New York: positive lat (North), negative lon (West)
# - Sydney: negative lat (South), positive lon (East)
```

---

## Part 4: Tuples

### What is a Tuple?

A tuple is an **immutable** (unchangeable) sequence of values.

```python
# Creating tuples
point = (25.0330, 121.5654)
rgb_color = (255, 128, 0)
person = ("Alice", 25, "Engineer")

# Single element tuple (note the comma!)
single = (42,)  # This is a tuple
not_tuple = (42)  # This is just an integer!
```

### Accessing Tuple Elements

```python
taipei = (25.0330, 121.5654)

# Indexing (0-based)
latitude = taipei[0]   # 25.0330
longitude = taipei[1]  # 121.5654

# Negative indexing
last = taipei[-1]      # 121.5654 (last element)

# Length
print(len(taipei))     # 2
```

### Tuple Unpacking

```python
taipei = (25.0330, 121.5654)

# Unpacking into variables
lat, lon = taipei
print(f"Latitude: {lat}")   # Latitude: 25.0330
print(f"Longitude: {lon}")  # Longitude: 121.5654

# Unpacking in loops
locations = [
    ("Taipei", 25.0330, 121.5654),
    ("Tokyo", 35.6762, 139.6503),
    ("Seoul", 37.5665, 126.9780),
]

for name, lat, lon in locations:
    print(f"{name} is at ({lat}, {lon})")
```

### Why Tuples are Immutable

```python
taipei = (25.0330, 121.5654)

# This will cause an error!
# taipei[0] = 26.0  # TypeError: 'tuple' object does not support item assignment

# If you need to change values, create a new tuple
new_taipei = (26.0, taipei[1])
```

### Why Use Tuples for Coordinates?

1. **Immutability**: Coordinates shouldn't change accidentally
2. **Semantic meaning**: A coordinate is a single unit of two values
3. **Memory efficient**: Tuples use less memory than lists
4. **Hashable**: Tuples can be used as dictionary keys

---

## Part 5: Putting It Together

### Storing Locations

```python
# Method 1: Simple tuples
taipei_101 = (25.0330, 121.5654)
ntu_main_gate = (25.0174, 121.5405)
taipei_main_station = (25.0478, 121.5170)

# Method 2: Named locations using variables
TAIPEI_101_LAT = 25.0330
TAIPEI_101_LON = 121.5654
taipei_101 = (TAIPEI_101_LAT, TAIPEI_101_LON)

# Method 3: Multiple locations in a list
my_favorite_places = [
    (25.0330, 121.5654),  # Taipei 101
    (25.0174, 121.5405),  # NTU
    (25.0478, 121.5170),  # Main Station
]
```

### Printing Coordinates Nicely

```python
taipei_101 = (25.0330, 121.5654)

# Basic print
print(taipei_101)  # (25.033, 121.5654)

# Formatted string (f-string)
lat, lon = taipei_101
print(f"Taipei 101 is at latitude {lat}, longitude {lon}")

# With precision control
print(f"Coordinates: ({lat:.4f}, {lon:.4f})")
# Output: Coordinates: (25.0330, 121.5654)

# Degree symbol
print(f"Location: {lat}°N, {lon}°E")
# Output: Location: 25.033°N, 121.5654°E
```

---

## Summary

| Concept | Example | Key Point |
|---------|---------|-----------|
| Variable | `city = "Taipei"` | Names that store values |
| Integer | `year = 2024` | Whole numbers |
| Float | `lat = 25.0330` | Decimal numbers |
| Tuple | `(25.0, 121.5)` | Immutable sequence |
| Latitude | 25.0330 | North-South (-90 to 90) |
| Longitude | 121.5654 | East-West (-180 to 180) |

---

## What's Next?

In the next lecture (Week 1-2), we'll learn:
- How to define functions
- The math module
- Calculating distances between coordinates using the Haversine formula
