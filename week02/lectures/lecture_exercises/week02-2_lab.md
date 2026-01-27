# Week 2-2 Lab: Dictionaries & Storing "Places"

## Lab Overview

In this lab, you will practice:
- Creating and manipulating dictionaries
- Working with nested data structures
- Storing and querying place data
- Building a simple place database

---

## Exercise 1: Dictionary Basics (10 minutes)

### Task 1.1: Create a Place Dictionary

```python
# TODO: Create a dictionary for your favorite restaurant
# Include: name, latitude, longitude, rating, category

my_favorite = {
    "name": "___",
    "lat": ___,
    "lon": ___,
    "rating": ___,
    "category": "restaurant"
}

# Print the dictionary
print(my_favorite)
```

### Task 1.2: Access Dictionary Values

```python
place = {
    "name": "Din Tai Fung",
    "lat": 25.0339,
    "lon": 121.5645,
    "rating": 4.9,
    "category": "restaurant",
    "tags": ["dumplings", "michelin", "taiwanese"]
}

# TODO: Get the name using bracket notation
name = place["___"]
print(f"Name: {name}")

# TODO: Get the rating
rating = place[___]
print(f"Rating: {rating}")

# TODO: Get the first tag
first_tag = place["tags"][___]
print(f"First tag: {first_tag}")

# TODO: Try to get a key that doesn't exist using .get()
# (with a default value of "N/A")
address = place.get("address", ___)
print(f"Address: {address}")
```

### Task 1.3: Modify Dictionary

```python
place = {
    "name": "Test Restaurant",
    "rating": 4.0
}

# TODO: Add a new key "category" with value "restaurant"
place[___] = ___

# TODO: Add coordinates
place["lat"] = 25.0330
place["lon"] = ___

# TODO: Update the rating to 4.5
place["rating"] = ___

# TODO: Add a list of tags
place["tags"] = ["food", "local"]

# TODO: Add another tag to the existing tags list
place["tags"].append("___")

print(place)
```

---

## Exercise 2: Iterating Over Dictionaries (10 minutes)

### Task 2.1: Loop Through Keys and Values

```python
place = {
    "name": "Taipei 101",
    "lat": 25.0330,
    "lon": 121.5654,
    "rating": 4.7,
    "category": "landmark"
}

# TODO: Print all keys
print("Keys:")
for key in place.___():
    print(f"  {key}")

# TODO: Print all values
print("\nValues:")
for value in place.___():
    print(f"  {value}")

# TODO: Print all key-value pairs
print("\nKey-Value Pairs:")
for key, value in place.___():
    print(f"  {key}: {value}")
```

### Task 2.2: Process Multiple Places

```python
places = [
    {"name": "Taipei 101", "rating": 4.7},
    {"name": "Din Tai Fung", "rating": 4.9},
    {"name": "Shilin Market", "rating": 4.5},
    {"name": "Elephant Mountain", "rating": 4.6},
]

# TODO: Print each place's name and rating
for place in places:
    name = place["___"]
    rating = place["___"]
    print(f"{name}: {rating} stars")
```

### Task 2.3: Calculate Average Rating

```python
places = [
    {"name": "Place A", "rating": 4.5},
    {"name": "Place B", "rating": 4.8},
    {"name": "Place C", "rating": 4.2},
    {"name": "Place D", "rating": 4.6},
]

# TODO: Calculate the average rating
total = 0
count = 0

for place in places:
    total += place["___"]
    count += ___

average = total / count
print(f"Average rating: {average:.2f}")

# TODO: Bonus - do it in one line using list comprehension
average_oneline = sum([p["rating"] for p in places]) / len(places)
print(f"Average (one-line): {average_oneline:.2f}")
```

---

## Exercise 3: Nested Data Structures (15 minutes)

### Task 3.1: Dictionary with Tuple Coordinates

```python
# TODO: Create a place with coordinates as a tuple
place = {
    "name": "Taipei 101",
    "coords": (25.0330, 121.5654),  # (lat, lon) tuple
    "rating": 4.7
}

# TODO: Access the latitude from the coords tuple
latitude = place["coords"][___]
print(f"Latitude: {latitude}")

# TODO: Unpack coords into lat and lon variables
lat, lon = place["___"]
print(f"Location: {lat}, {lon}")
```

### Task 3.2: Dictionary with Nested Dictionary

```python
place = {
    "name": "Taipei 101",
    "location": {
        "lat": 25.0330,
        "lon": 121.5654,
        "city": "Taipei",
        "district": "Xinyi"
    },
    "details": {
        "floors": 101,
        "height_m": 508,
        "opened_year": 2004
    }
}

# TODO: Get the latitude from the nested location dictionary
lat = place["location"]["___"]
print(f"Latitude: {lat}")

# TODO: Get the number of floors
floors = place[___][___]
print(f"Floors: {floors}")

# TODO: Get the city, with a default of "Unknown"
city = place.get("location", {}).get("city", "Unknown")
print(f"City: {city}")
```

### Task 3.3: Build a Complete Place Structure

```python
# TODO: Create a complete place dictionary with:
# - name
# - coords (as tuple)
# - rating
# - category
# - tags (as list)
# - hours (as nested dictionary with days as keys)

complete_place = {
    "name": "Your Favorite Cafe",
    "coords": (___, ___),
    "rating": ___,
    "category": "cafe",
    "tags": ["coffee", "___", "___"],
    "hours": {
        "mon": "08:00-22:00",
        "tue": "08:00-22:00",
        "wed": "___",
        "thu": "___",
        "fri": "___",
        "sat": "09:00-23:00",
        "sun": "09:00-21:00"
    }
}

# Print nicely formatted
print(f"Place: {complete_place['name']}")
print(f"Rating: {complete_place['rating']} stars")
print(f"Tags: {', '.join(complete_place['tags'])}")
print(f"Monday hours: {complete_place['hours']['mon']}")
```

---

## Exercise 4: Place Database Operations (20 minutes)

### Task 4.1: Create a Place Database

```python
# TODO: Create a list of at least 5 places in Taipei
# Each place should have: name, coords (tuple), rating, category

places_db = [
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
    # TODO: Add 3 more places
    {
        "name": "___",
        "coords": (___, ___),
        "rating": ___,
        "category": "___"
    },
    # ... add more
]

print(f"Database has {len(places_db)} places")
```

### Task 4.2: Find Place by Name

```python
def find_by_name(places, name):
    """
    Find a place by its name.
    Returns the place dict or None if not found.
    """
    # TODO: Loop through places and find matching name
    for place in places:
        if place["name"] == ___:
            return place
    return None


# Test
result = find_by_name(places_db, "Taipei 101")
if result:
    print(f"Found: {result['name']} at {result['coords']}")
else:
    print("Not found")

result = find_by_name(places_db, "Nonexistent Place")
print(f"Search for nonexistent: {result}")  # Should be None
```

### Task 4.3: Filter by Category

```python
def filter_by_category(places, category):
    """
    Get all places in a specific category.
    Returns a list of matching places.
    """
    # TODO: Use list comprehension to filter
    return [p for p in places if p["___"] == ___]


# Test
restaurants = filter_by_category(places_db, "restaurant")
print(f"\nRestaurants ({len(restaurants)}):")
for r in restaurants:
    print(f"  - {r['name']}")
```

### Task 4.4: Filter by Rating

```python
def filter_by_rating(places, min_rating):
    """
    Get all places with rating >= min_rating.
    """
    # TODO: Implement the filter
    return [p for p in places if p.get("rating", 0) >= ___]


# Test
top_rated = filter_by_rating(places_db, 4.7)
print(f"\nTop rated (>= 4.7):")
for p in top_rated:
    print(f"  - {p['name']}: {p['rating']} stars")
```

### Task 4.5: Sort Places

```python
def sort_by_rating(places, descending=True):
    """
    Sort places by rating.
    Returns a new sorted list (doesn't modify original).
    """
    # TODO: Use sorted() with a key function
    return sorted(places, key=lambda p: p["___"], reverse=___)


# Test
sorted_places = sort_by_rating(places_db)
print("\nPlaces sorted by rating (highest first):")
for i, p in enumerate(sorted_places, 1):
    print(f"  {i}. {p['name']}: {p['rating']} stars")
```

---

## Exercise 5: Advanced Queries (15 minutes)

### Task 5.1: Find Nearby Places

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


def find_nearby(places, center, max_km):
    """
    Find all places within max_km of center.
    Returns list of (place, distance) tuples.
    """
    results = []

    for place in places:
        # TODO: Calculate distance from center to this place
        distance = haversine(center, place["___"])

        # TODO: If within max_km, add to results
        if distance <= ___:
            results.append((place, distance))

    # Sort by distance
    results.sort(key=lambda x: x[1])
    return results


# Test: Find places within 1km of Taipei 101
my_location = (25.0330, 121.5654)
nearby = find_nearby(places_db, my_location, 1.0)

print(f"\nPlaces within 1km of my location:")
for place, dist in nearby:
    print(f"  - {place['name']}: {dist*1000:.0f}m")
```

### Task 5.2: Combined Query

```python
def search_places(places, center=None, max_km=None, min_rating=None, category=None):
    """
    Search places with multiple filters.
    All filters are optional.
    """
    results = places.copy()

    # TODO: Filter by category if specified
    if category:
        results = [p for p in results if p.get("category") == ___]

    # TODO: Filter by rating if specified
    if min_rating:
        results = [p for p in results if p.get("rating", 0) >= ___]

    # TODO: Filter by distance if center and max_km specified
    if center and max_km:
        results = [
            p for p in results
            if haversine(center, p["coords"]) <= ___
        ]

    return results


# Test: Find restaurants with rating >= 4.5 within 2km
my_location = (25.0330, 121.5654)
results = search_places(
    places_db,
    center=my_location,
    max_km=2.0,
    min_rating=4.5,
    category="restaurant"
)

print(f"\nSearch results:")
for p in results:
    dist = haversine(my_location, p["coords"])
    print(f"  - {p['name']}: {p['rating']} stars, {dist*1000:.0f}m away")
```

### Task 5.3: Create Summary Statistics

```python
def get_database_stats(places):
    """
    Get statistics about the place database.
    """
    if not places:
        return None

    # TODO: Calculate statistics
    stats = {
        "total_places": len(places),
        "categories": {},
        "avg_rating": 0,
        "highest_rated": None,
        "lowest_rated": None,
    }

    # Count places by category
    for place in places:
        cat = place.get("category", "unknown")
        stats["categories"][cat] = stats["categories"].get(cat, 0) + 1

    # TODO: Calculate average rating
    ratings = [p.get("rating", 0) for p in places if p.get("rating")]
    if ratings:
        stats["avg_rating"] = sum(ratings) / len(ratings)

    # TODO: Find highest and lowest rated
    sorted_by_rating = sorted(places, key=lambda p: p.get("rating", 0))
    stats["lowest_rated"] = sorted_by_rating[0]["name"] if sorted_by_rating else None
    stats["highest_rated"] = sorted_by_rating[___]["name"] if sorted_by_rating else None

    return stats


# Test
stats = get_database_stats(places_db)
print("\nDatabase Statistics:")
print(f"  Total places: {stats['total_places']}")
print(f"  Average rating: {stats['avg_rating']:.2f}")
print(f"  Highest rated: {stats['highest_rated']}")
print(f"  Lowest rated: {stats['lowest_rated']}")
print(f"  Categories: {stats['categories']}")
```

---

## Exercise 6: Dictionary Comprehension (5 minutes)

### Task 6.1: Create Lookup Dictionaries

```python
places = [
    {"name": "Taipei 101", "coords": (25.0330, 121.5654), "rating": 4.7},
    {"name": "Din Tai Fung", "coords": (25.0339, 121.5645), "rating": 4.9},
    {"name": "Shilin Market", "coords": (25.0878, 121.5241), "rating": 4.5},
]

# TODO: Create a name -> coords lookup dictionary
# Example: {"Taipei 101": (25.0330, 121.5654), ...}
coords_lookup = {p["name"]: p["coords"] for p in places}
print(f"Coords lookup: {coords_lookup}")

# TODO: Create a name -> rating lookup dictionary
rating_lookup = {p["___"]: p["___"] for p in places}
print(f"Rating lookup: {rating_lookup}")

# TODO: Use the lookup
taipei_coords = coords_lookup["Taipei 101"]
print(f"\nTaipei 101 coordinates: {taipei_coords}")
```

### Task 6.2: Transform Data

```python
# TODO: Create a dictionary with name as key and formatted info as value
# Example: {"Taipei 101": "4.7★ at (25.0330, 121.5654)", ...}

place_info = {
    p["name"]: f"{p['rating']}★ at {p['coords']}"
    for p in places
}

print("\nPlace Info:")
for name, info in place_info.items():
    print(f"  {name}: {info}")
```

---

## Submission

Save your completed lab as `week02-2_lab_solution.py`.

### Checklist

- [ ] Exercise 1: Dictionary creation and modification
- [ ] Exercise 2: Dictionary iteration
- [ ] Exercise 3: Nested data structures
- [ ] Exercise 4: Place database operations
- [ ] Exercise 5: Advanced queries (nearby, combined search)
- [ ] Exercise 6: Dictionary comprehension
