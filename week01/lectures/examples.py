"""
Week 1 Lecture Examples
Run this file to see all examples in action.
"""

import math

# ============================================================
# Week 1-1: Variables & Coordinates
# ============================================================

print("=" * 60)
print("WEEK 1-1: Variables & The Coordinate System")
print("=" * 60)

# --- Variables ---
print("\n--- Variables ---")

city_name = "Taipei"
population = 2600000
area_km2 = 271.8

print(f"City: {city_name}")
print(f"Population: {population:,}")  # :, adds thousand separators
print(f"Area: {area_km2} km²")
print(f"Density: {population / area_km2:.0f} people/km²")

# --- Numeric Types ---
print("\n--- Numeric Types ---")

# Integers
year = 2024
print(f"Year (int): {year}, type: {type(year)}")

# Floats
latitude = 25.0330
print(f"Latitude (float): {latitude}, type: {type(latitude)}")

# Float precision warning
print(f"\nFloat precision: 0.1 + 0.2 = {0.1 + 0.2}")

# --- Tuples ---
print("\n--- Tuples ---")

# Creating tuples
taipei_101 = (25.0330, 121.5654)
print(f"Taipei 101: {taipei_101}")

# Accessing elements
print(f"Latitude: {taipei_101[0]}")
print(f"Longitude: {taipei_101[1]}")

# Tuple unpacking
lat, lon = taipei_101
print(f"Unpacked: lat={lat}, lon={lon}")

# --- Multiple Locations ---
print("\n--- Multiple Locations ---")

locations = [
    ("Taipei 101", 25.0330, 121.5654),
    ("Tokyo Tower", 35.6586, 139.7454),
    ("Eiffel Tower", 48.8584, 2.2945),
    ("Statue of Liberty", 40.6892, -74.0445),
]

for name, lat, lon in locations:
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"
    print(f"  {name}: {abs(lat):.4f}°{ns}, {abs(lon):.4f}°{ew}")


# ============================================================
# Week 1-2: Functions & Distance Logic
# ============================================================

print("\n" + "=" * 60)
print("WEEK 1-2: Functions & Distance Logic")
print("=" * 60)

# --- Basic Functions ---
print("\n--- Basic Functions ---")


def greet(name):
    """A simple greeting function."""
    return f"Hello, {name}!"


print(greet("Alice"))
print(greet("Bob"))


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32


print(f"0°C = {celsius_to_fahrenheit(0)}°F")
print(f"100°C = {celsius_to_fahrenheit(100)}°F")

# --- Math Module ---
print("\n--- Math Module ---")

print(f"π = {math.pi}")
print(f"e = {math.e}")
print(f"√2 = {math.sqrt(2)}")
print(f"sin(90°) = {math.sin(math.radians(90))}")
print(f"cos(0°) = {math.cos(math.radians(0))}")

# --- Haversine Formula ---
print("\n--- Haversine Formula ---")


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

    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


# Test distances
taipei_101 = (25.0330, 121.5654)
tokyo_tower = (35.6586, 139.7454)
main_station = (25.0478, 121.5170)

print(f"Taipei 101 → Tokyo Tower: {haversine(taipei_101, tokyo_tower):.2f} km")
print(f"Taipei 101 → Main Station: {haversine(taipei_101, main_station):.2f} km")

# --- Distance Comparison ---
print("\n--- Distance Comparisons ---")

city_pairs = [
    (("Taipei", (25.0330, 121.5654)), ("Tokyo", (35.6762, 139.6503))),
    (("New York", (40.7128, -74.0060)), ("London", (51.5074, -0.1278))),
    (("Sydney", (-33.8688, 151.2093)), ("Auckland", (-36.8509, 174.7645))),
    (("Los Angeles", (34.0522, -118.2437)), ("San Francisco", (37.7749, -122.4194))),
]

for (name1, coord1), (name2, coord2) in city_pairs:
    dist = haversine(coord1, coord2)
    print(f"  {name1} → {name2}: {dist:,.0f} km")

# --- Walking Time Estimate ---
print("\n--- Walking Time Estimates ---")


def estimate_walking_time(distance_km, speed_kmh=5.0):
    """Estimate walking time."""
    hours = distance_km / speed_kmh
    h = int(hours)
    m = int((hours - h) * 60)
    return h, m


mrt_stations = [
    ("Taipei 101/WTC MRT", 25.0330, 121.5637),
    ("Xiangshan MRT", 25.0329, 121.5707),
    ("Taipei City Hall MRT", 25.0408, 121.5679),
]

print("Walking time from Taipei 101 to nearby MRT stations:")
for name, lat, lon in mrt_stations:
    dist = haversine(taipei_101, (lat, lon))
    h, m = estimate_walking_time(dist)
    time_str = f"{m} min" if h == 0 else f"{h}h {m}m"
    print(f"  {name}: {dist * 1000:.0f}m ({time_str})")

# --- Route Distance ---
print("\n--- Route Distance ---")

walking_tour = [
    ("Taipei 101", 25.0330, 121.5654),
    ("Din Tai Fung", 25.0339, 121.5645),
    ("Yongkang Street", 25.0329, 121.5598),
    ("Daan Park", 25.0279, 121.5595),
    ("NTU Main Gate", 25.0174, 121.5405),
]

print("Walking Tour Route:")
total_distance = 0

for i in range(len(walking_tour) - 1):
    name1, lat1, lon1 = walking_tour[i]
    name2, lat2, lon2 = walking_tour[i + 1]
    dist = haversine((lat1, lon1), (lat2, lon2))
    total_distance += dist
    print(f"  {i + 1}. {name1} → {name2}: {dist:.2f} km")

print(f"\nTotal distance: {total_distance:.2f} km")
h, m = estimate_walking_time(total_distance)
print(f"Estimated walking time: {h}h {m}m")

print("\n" + "=" * 60)
print("End of Week 1 Examples")
print("=" * 60)
