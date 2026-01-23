# Week 2-2 Lecture: Dictionaries & Storing "Places"

## Learning Objectives

By the end of this lecture, students will be able to:
1. Create and manipulate dictionaries
2. Understand key-value pairs
3. Work with nested data structures
4. Store complex place data (name, coordinates, rating, etc.)
5. Query and filter place collections

---

## Part 1: Introduction to Dictionaries

### What is a Dictionary?

A dictionary stores data as **key-value pairs**.

```python
# Creating a dictionary
person = {
    "name": "Alice",
    "age": 25,
    "city": "Taipei"
}

# Keys are unique identifiers
# Values can be any type
```

### Dictionary Syntax

```python
# Empty dictionary
empty = {}
empty = dict()

# Dictionary with data
place = {
    "name": "Taipei 101",
    "latitude": 25.0330,
    "longitude": 121.5654
}

# Keys can be strings or numbers
scores = {
    1: "Gold",
    2: "Silver",
    3: "Bronze"
}
```

### Why Dictionaries?

Compare storing place data:

```python
# Using tuples (Week 1) - position-based
place_tuple = ("Taipei 101", 25.0330, 121.5654, 4.7)
name = place_tuple[0]      # Which index is which?
rating = place_tuple[3]    # Easy to forget!

# Using dictionaries - name-based
place_dict = {
    "name": "Taipei 101",
    "lat": 25.0330,
    "lon": 121.5654,
    "rating": 4.7
}
name = place_dict["name"]     # Clear and readable!
rating = place_dict["rating"]
```

---

## Part 2: Accessing Dictionary Data

### Getting Values

```python
place = {
    "name": "Taipei 101",
    "lat": 25.0330,
    "lon": 121.5654,
    "rating": 4.7
}

# Method 1: Square bracket notation
name = place["name"]
print(name)  # "Taipei 101"

# ⚠️ KeyError if key doesn't exist
# category = place["category"]  # KeyError!

# Method 2: get() - safe access
category = place.get("category")        # Returns None
category = place.get("category", "N/A") # Returns "N/A" (default)
```

### Checking if Key Exists

```python
place = {"name": "Taipei 101", "rating": 4.7}

# Using 'in' operator
if "rating" in place:
    print(f"Rating: {place['rating']}")
else:
    print("No rating available")

# Check for missing key
if "address" not in place:
    print("Address not available")
```

### Getting All Keys and Values

```python
place = {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654}

# All keys
print(place.keys())    # dict_keys(['name', 'lat', 'lon'])
print(list(place.keys()))  # ['name', 'lat', 'lon']

# All values
print(place.values())  # dict_values(['Taipei 101', 25.033, 121.5654])

# All key-value pairs
print(place.items())   # dict_items([('name', 'Taipei 101'), ...])
```

---

## Part 3: Modifying Dictionaries

### Adding and Updating

```python
place = {"name": "Taipei 101"}

# Add new key-value pair
place["rating"] = 4.7
place["category"] = "landmark"

# Update existing value
place["rating"] = 4.8

# Update multiple at once
place.update({
    "address": "No. 7, Section 5, Xinyi Road",
    "hours": "11:00-21:30"
})

print(place)
```

### Removing Items

```python
place = {
    "name": "Taipei 101",
    "rating": 4.7,
    "temp_data": "delete me"
}

# pop() - remove and return value
rating = place.pop("rating")
print(rating)  # 4.7

# pop() with default (no error if missing)
missing = place.pop("nonexistent", "not found")

# del - just remove
del place["temp_data"]

# clear() - remove all
place.clear()
```

---

## Part 4: Iterating Over Dictionaries

### Loop Through Keys

```python
place = {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654}

# Default iteration is over keys
for key in place:
    print(key)  # name, lat, lon

# Explicit
for key in place.keys():
    print(f"{key}: {place[key]}")
```

### Loop Through Values

```python
for value in place.values():
    print(value)  # Taipei 101, 25.033, 121.5654
```

### Loop Through Key-Value Pairs

```python
for key, value in place.items():
    print(f"{key}: {value}")

# Output:
# name: Taipei 101
# lat: 25.033
# lon: 121.5654
```

---

## Part 5: Nested Data Structures

### Dictionary with Tuple Value

```python
place = {
    "name": "Taipei 101",
    "coords": (25.0330, 121.5654),  # Tuple inside dict
    "rating": 4.7
}

# Access nested data
lat = place["coords"][0]
lon = place["coords"][1]

# Or unpack
lat, lon = place["coords"]
```

### Dictionary with List Value

```python
place = {
    "name": "Din Tai Fung",
    "coords": (25.0339, 121.5645),
    "tags": ["restaurant", "dumplings", "michelin"],  # List inside dict
    "ratings": [4.5, 4.8, 4.6, 4.7]
}

# Access list elements
first_tag = place["tags"][0]  # "restaurant"

# List operations still work
place["tags"].append("taiwanese")
average_rating = sum(place["ratings"]) / len(place["ratings"])
```

### Dictionary with Dictionary Value

```python
place = {
    "name": "Taipei 101",
    "coords": {                    # Nested dictionary
        "lat": 25.0330,
        "lon": 121.5654
    },
    "details": {
        "floors": 101,
        "height_m": 508,
        "opened": 2004
    }
}

# Access nested dictionary
lat = place["coords"]["lat"]
floors = place["details"]["floors"]

# Safe nested access
height = place.get("details", {}).get("height_m", "unknown")
```

---

## Part 6: The Complete Place Structure

### Recommended Structure for Our Project

```python
place = {
    "name": "Joe's Pizza",
    "coords": (40.7128, -74.0060),
    "rating": 4.5,
    "category": "restaurant",
    "tags": ["pizza", "italian", "cheap"],
    "price_level": 1,  # 1-4 scale
    "hours": {
        "mon": "11:00-22:00",
        "tue": "11:00-22:00",
        "wed": "11:00-22:00",
        "thu": "11:00-22:00",
        "fri": "11:00-23:00",
        "sat": "11:00-23:00",
        "sun": "12:00-21:00"
    }
}
```

### Creating Multiple Places

```python
places = [
    {
        "name": "Taipei 101",
        "coords": (25.0330, 121.5654),
        "rating": 4.7,
        "category": "landmark"
    },
    {
        "name": "Din Tai Fung",
        "coords": (25.0339, 121.5645),
        "rating": 4.9,
        "category": "restaurant"
    },
    {
        "name": "Shilin Night Market",
        "coords": (25.0878, 121.5241),
        "rating": 4.5,
        "category": "market"
    }
]
```

---

## Part 7: Querying Place Data

### Find Place by Name

```python
def find_place(places, name):
    """Find a place by name."""
    for place in places:
        if place["name"] == name:
            return place
    return None

# Usage
result = find_place(places, "Din Tai Fung")
if result:
    print(f"Found: {result['name']} at {result['coords']}")
```

### Filter by Category

```python
def get_by_category(places, category):
    """Get all places in a category."""
    return [p for p in places if p["category"] == category]

# Usage
restaurants = get_by_category(places, "restaurant")
for r in restaurants:
    print(r["name"])
```

### Filter by Rating

```python
def get_top_rated(places, min_rating=4.5):
    """Get places with rating >= min_rating."""
    return [p for p in places if p.get("rating", 0) >= min_rating]

# Usage
top_places = get_top_rated(places, 4.7)
```

### Sort by Rating

```python
# Sort in place (modifies original list)
places.sort(key=lambda p: p["rating"], reverse=True)

# Create sorted copy
sorted_places = sorted(places, key=lambda p: p["rating"], reverse=True)

# Print top 3
for i, place in enumerate(sorted_places[:3], 1):
    print(f"{i}. {place['name']} - {place['rating']} stars")
```

---

## Part 8: Dictionary Comprehension

### Basic Syntax

```python
# Create dictionary from lists
names = ["a", "b", "c"]
values = [1, 2, 3]

d = {name: value for name, value in zip(names, values)}
print(d)  # {'a': 1, 'b': 2, 'c': 3}
```

### Transform Place Data

```python
places = [
    {"name": "Taipei 101", "rating": 4.7},
    {"name": "Din Tai Fung", "rating": 4.9},
    {"name": "Shilin Market", "rating": 4.5}
]

# Create name -> rating mapping
rating_map = {p["name"]: p["rating"] for p in places}
print(rating_map)
# {'Taipei 101': 4.7, 'Din Tai Fung': 4.9, 'Shilin Market': 4.5}

# Quick lookup
print(rating_map["Din Tai Fung"])  # 4.9
```

### Extract Coordinates

```python
# Create name -> coords mapping
coord_map = {p["name"]: p["coords"] for p in places}

# Get coordinates by name
taipei_101_coords = coord_map["Taipei 101"]
```

---

## Part 9: Combining with Functions

### Complete Example

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


def find_nearby(places, center, max_distance_km):
    """Find all places within max_distance_km of center."""
    nearby = []
    for place in places:
        distance = haversine(center, place["coords"])
        if distance <= max_distance_km:
            # Add distance to the result
            nearby.append({
                **place,  # Copy all existing fields
                "distance_km": round(distance, 2)
            })
    return nearby


def find_best_nearby(places, center, max_distance_km, min_rating=4.0):
    """Find highly-rated places within distance, sorted by rating."""
    nearby = find_nearby(places, center, max_distance_km)
    filtered = [p for p in nearby if p.get("rating", 0) >= min_rating]
    return sorted(filtered, key=lambda p: p["rating"], reverse=True)


# Usage
places = [
    {"name": "Taipei 101", "coords": (25.0330, 121.5654), "rating": 4.7},
    {"name": "Din Tai Fung", "coords": (25.0339, 121.5645), "rating": 4.9},
    {"name": "Eslite Bookstore", "coords": (25.0398, 121.5672), "rating": 4.6},
    {"name": "Shilin Night Market", "coords": (25.0878, 121.5241), "rating": 4.5},
]

my_location = (25.0350, 121.5650)  # Near Taipei 101

results = find_best_nearby(places, my_location, max_distance_km=1.0, min_rating=4.5)

print("Best places within 1km:")
for place in results:
    print(f"  {place['name']}: {place['rating']}★ ({place['distance_km']}km)")
```

---

## Summary

| Concept | Example | Description |
|---------|---------|-------------|
| Dictionary | `{"key": value}` | Key-value pairs |
| Access | `d["key"]` | Get value by key |
| Safe access | `d.get("key", default)` | No error if missing |
| Add/Update | `d["key"] = value` | Set value |
| Iterate | `for k, v in d.items():` | Loop over pairs |
| Nested | `d["a"]["b"]` | Dict in dict |
| Comprehension | `{k: v for ...}` | Create dict inline |

---

## Practice: 99 Problems

Complete **P11–P15 (Run-length encoding)** from *99 Problems in Python*:

```python
# Example: Run-length encoding
# Input:  ['a', 'a', 'a', 'b', 'b', 'c', 'c', 'c', 'c']
# Output: [('a', 3), ('b', 2), ('c', 4)]
```

This teaches you to:
- Group consecutive elements
- Count occurrences
- Transform data structures

These skills are essential for processing API responses in the coming weeks!
