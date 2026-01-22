"""
Week 2 Lecture Examples
Run this file to see all examples in action.
"""

import math

# ============================================================
# Haversine function (from Week 1)
# ============================================================

def haversine(coord1, coord2):
    """Calculate distance between two coordinates in km."""
    R = 6371
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


# ============================================================
# Week 2-1: Lists, Loops & Routes
# ============================================================

print("=" * 60)
print("WEEK 2-1: Lists, Loops & The Route")
print("=" * 60)

# --- Lists vs Tuples ---
print("\n--- Lists vs Tuples ---")

# Tuple (immutable) - good for coordinates
coord = (25.0330, 121.5654)
print(f"Coordinate (tuple): {coord}")

# List (mutable) - good for collections
cities = ["Taipei", "Tokyo", "Seoul"]
cities.append("Bangkok")
print(f"Cities (list): {cities}")

# --- List Operations ---
print("\n--- List Operations ---")

route = [
    (25.0330, 121.5654),  # Taipei 101
    (25.0339, 121.5645),  # Din Tai Fung
    (25.0329, 121.5598),  # Yongkang Street
]

print(f"Route has {len(route)} stops")
print(f"First stop: {route[0]}")
print(f"Last stop: {route[-1]}")
print(f"First two: {route[:2]}")

# --- For Loops ---
print("\n--- For Loops ---")

print("Basic loop:")
for coord in route:
    print(f"  {coord}")

print("\nWith enumerate:")
for i, coord in enumerate(route, start=1):
    print(f"  Stop {i}: {coord}")

print("\nWith unpacking:")
for lat, lon in route:
    print(f"  Lat: {lat:.4f}, Lon: {lon:.4f}")

# --- range() ---
print("\n--- range() Examples ---")

print("range(5):", list(range(5)))
print("range(1, 6):", list(range(1, 6)))
print("range(0, 10, 2):", list(range(0, 10, 2)))
print("range(5, 0, -1):", list(range(5, 0, -1)))

# --- Consecutive Pairs ---
print("\n--- Consecutive Pairs ---")

route_names = ["A", "B", "C", "D"]

print("Using index:")
for i in range(len(route_names) - 1):
    print(f"  {route_names[i]} → {route_names[i + 1]}")

print("\nUsing zip:")
for start, end in zip(route_names[:-1], route_names[1:]):
    print(f"  {start} → {end}")

# --- Route Distance Calculation ---
print("\n--- Route Distance ---")

route = [
    (25.0330, 121.5654),  # Taipei 101
    (25.0339, 121.5645),  # Din Tai Fung
    (25.0329, 121.5598),  # Yongkang Street
    (25.0279, 121.5595),  # Daan Park
    (25.0174, 121.5405),  # NTU
]

total = 0
for i in range(len(route) - 1):
    dist = haversine(route[i], route[i + 1])
    total += dist
    print(f"Segment {i + 1}: {dist:.3f} km")

print(f"Total: {total:.2f} km")

# --- map() and filter() ---
print("\n--- map() and filter() ---")

numbers = [1, 2, 3, 4, 5]

# map: transform each element
doubled = list(map(lambda x: x * 2, numbers))
print(f"Doubled: {doubled}")

# filter: keep matching elements
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Evens: {evens}")

# Extract latitudes from coordinates
latitudes = list(map(lambda c: c[0], route))
print(f"Latitudes: {latitudes}")

# ============================================================
# Week 2-2: Dictionaries & Storing Places
# ============================================================

print("\n" + "=" * 60)
print("WEEK 2-2: Dictionaries & Storing Places")
print("=" * 60)

# --- Dictionary Basics ---
print("\n--- Dictionary Basics ---")

place = {
    "name": "Taipei 101",
    "coords": (25.0330, 121.5654),
    "rating": 4.7,
    "category": "landmark"
}

print(f"Name: {place['name']}")
print(f"Rating: {place['rating']}")
print(f"Coordinates: {place['coords']}")

# Safe access with get()
address = place.get("address", "Not available")
print(f"Address: {address}")

# --- Modifying Dictionaries ---
print("\n--- Modifying Dictionaries ---")

place["tags"] = ["observation", "shopping", "dining"]
place["rating"] = 4.8
print(f"Updated place: {place['name']}, {place['rating']}★")
print(f"Tags: {place['tags']}")

# --- Iterating ---
print("\n--- Iterating Over Dictionaries ---")

for key, value in place.items():
    print(f"  {key}: {value}")

# --- Nested Structures ---
print("\n--- Nested Structures ---")

detailed_place = {
    "name": "Taipei 101",
    "location": {
        "coords": (25.0330, 121.5654),
        "city": "Taipei",
        "district": "Xinyi"
    },
    "details": {
        "floors": 101,
        "height_m": 508
    }
}

print(f"City: {detailed_place['location']['city']}")
print(f"Floors: {detailed_place['details']['floors']}")

# --- Place Database ---
print("\n--- Place Database ---")

places = [
    {"name": "Taipei 101", "coords": (25.0330, 121.5654), "rating": 4.7, "category": "landmark"},
    {"name": "Din Tai Fung", "coords": (25.0339, 121.5645), "rating": 4.9, "category": "restaurant"},
    {"name": "Shilin Market", "coords": (25.0878, 121.5241), "rating": 4.5, "category": "market"},
    {"name": "Elephant Mountain", "coords": (25.0271, 121.5576), "rating": 4.6, "category": "landmark"},
]

print("All places:")
for p in places:
    print(f"  {p['name']}: {p['rating']}★ ({p['category']})")

# --- Querying ---
print("\n--- Querying Places ---")

# Filter by category
restaurants = [p for p in places if p["category"] == "restaurant"]
print(f"Restaurants: {[r['name'] for r in restaurants]}")

# Filter by rating
top_rated = [p for p in places if p["rating"] >= 4.6]
print(f"Top rated (>= 4.6): {[p['name'] for p in top_rated]}")

# Sort by rating
sorted_places = sorted(places, key=lambda p: p["rating"], reverse=True)
print("Sorted by rating:")
for i, p in enumerate(sorted_places, 1):
    print(f"  {i}. {p['name']}: {p['rating']}★")

# --- Finding Nearby ---
print("\n--- Finding Nearby Places ---")

my_location = (25.0330, 121.5654)  # Taipei 101

print(f"Places near {my_location}:")
for p in places:
    dist = haversine(my_location, p["coords"])
    print(f"  {p['name']}: {dist:.2f} km")

# Filter to within 1km
nearby = [(p, haversine(my_location, p["coords"])) for p in places]
nearby = [(p, d) for p, d in nearby if d <= 2.0]
nearby.sort(key=lambda x: x[1])

print(f"\nWithin 2km (sorted by distance):")
for p, dist in nearby:
    print(f"  {p['name']}: {dist*1000:.0f}m")

# --- Dictionary Comprehension ---
print("\n--- Dictionary Comprehension ---")

# Create lookup tables
name_to_coords = {p["name"]: p["coords"] for p in places}
name_to_rating = {p["name"]: p["rating"] for p in places}

print(f"Coords lookup: {name_to_coords}")
print(f"\nDin Tai Fung coords: {name_to_coords['Din Tai Fung']}")
print(f"Din Tai Fung rating: {name_to_rating['Din Tai Fung']}")

# --- Combined Example ---
print("\n--- Combined: Find Best Nearby ---")

def find_best_nearby(places, center, max_km, min_rating=4.0):
    """Find highly-rated places within distance."""
    results = []
    for p in places:
        dist = haversine(center, p["coords"])
        if dist <= max_km and p.get("rating", 0) >= min_rating:
            results.append({**p, "distance_km": round(dist, 3)})

    return sorted(results, key=lambda x: x["rating"], reverse=True)


best = find_best_nearby(places, my_location, max_km=3.0, min_rating=4.5)
print(f"Best places within 3km (rating >= 4.5):")
for p in best:
    print(f"  {p['name']}: {p['rating']}★, {p['distance_km']*1000:.0f}m away")

print("\n" + "=" * 60)
print("End of Week 2 Examples")
print("=" * 60)
