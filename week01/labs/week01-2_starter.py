"""
Week 1-2 Lab: Functions & Distance Logic
Starter Code

Instructions:
1. Complete each TODO section
2. Run the file to test your code
3. All tests should pass when you're done
"""

import math

# ============================================================
# Exercise 1: Basic Functions
# ============================================================

# Task 1.1: Greeting function
def greet(name):
    """Print a greeting message."""
    # TODO: Print "Hello, {name}!"
    pass


# Task 1.2: Temperature conversion
def celsius_to_fahrenheit(celsius):
    """
    Convert temperature from Celsius to Fahrenheit.
    Formula: F = C × 9/5 + 32
    """
    # TODO: Calculate and return Fahrenheit
    return None


# Task 1.3: Coordinate formatter
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
    return None


# ============================================================
# Exercise 2: The Math Module
# ============================================================

# Task 2.1: Math functions
def explore_math():
    """Explore various math functions."""
    # TODO: Complete each calculation

    sqrt_144 = None          # math.sqrt(144)
    two_to_ten = None        # math.pow(2, 10)
    pi_value = None          # math.pi
    e_value = None           # math.e
    floor_3_7 = None         # math.floor(3.7)

    return sqrt_144, two_to_ten, pi_value, e_value, floor_3_7


# Task 2.2: Degrees to radians
def degrees_to_radians(degrees):
    """Convert degrees to radians."""
    # TODO: Use math.radians()
    return None


# Task 2.3: 2D Euclidean distance
def distance_2d(point1, point2):
    """
    Calculate Euclidean distance between two 2D points.
    Formula: d = √((x2-x1)² + (y2-y1)²)
    """
    x1, y1 = point1
    x2, y2 = point2

    # TODO: Implement the Pythagorean theorem
    dx = x2 - x1
    dy = None  # TODO

    distance = None  # TODO: math.sqrt(...)
    return distance


# ============================================================
# Exercise 3: Haversine Formula
# ============================================================

# Task 3.1 & 3.2: Complete Haversine implementation
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

    # Extract coordinates
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # TODO: Convert to radians
    lat1_rad = None
    lat2_rad = None
    lon1_rad = None
    lon2_rad = None

    # TODO: Calculate differences
    dlat = None
    dlon = None

    # TODO: Haversine formula
    # a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
    a = None

    # TODO: c = 2 × asin(√a)
    c = None

    # TODO: distance = R × c
    distance = None

    return distance


# Task 3.3: Haversine with unit conversion
def haversine_with_units(coord1, coord2, unit='km'):
    """
    Calculate distance with unit conversion.

    Args:
        unit: 'km' for kilometers, 'mi' for miles, 'm' for meters
    """
    distance_km = haversine(coord1, coord2)

    if distance_km is None:
        return None

    # TODO: Convert to requested unit
    if unit == 'km':
        return distance_km
    elif unit == 'mi':
        return None  # TODO: km * 0.621371
    elif unit == 'm':
        return None  # TODO: km * 1000
    else:
        raise ValueError(f"Unknown unit: {unit}")


# ============================================================
# Exercise 4: Real-World Application
# ============================================================

# Task 4.1: Find nearest location
def find_nearest(current_location, locations):
    """
    Find the nearest location from a list.

    Args:
        current_location: (latitude, longitude) tuple
        locations: List of (name, latitude, longitude) tuples

    Returns:
        (name, distance) of the nearest location
    """
    nearest_name = None
    nearest_distance = float('inf')

    # TODO: Loop through locations and find the nearest
    for name, lat, lon in locations:
        location_coord = (lat, lon)
        distance = haversine(current_location, location_coord)

        if distance is not None and distance < nearest_distance:
            # TODO: Update nearest_name and nearest_distance
            pass

    return nearest_name, nearest_distance


# Task 4.2: Sort by distance
def sort_by_distance(reference, locations):
    """
    Sort locations by distance from a reference point.

    Args:
        reference: (latitude, longitude) tuple
        locations: List of (name, latitude, longitude) tuples

    Returns:
        Sorted list of (name, distance) tuples
    """
    distances = []

    for name, lat, lon in locations:
        dist = haversine(reference, (lat, lon))
        if dist is not None:
            distances.append((name, dist))

    # TODO: Sort by distance (index 1)
    # distances.sort(key=lambda x: x[?])

    return distances


# Task 4.3: Walking time estimate
def estimate_walking_time(distance_km, speed_kmh=5.0):
    """
    Estimate walking time based on distance.

    Returns:
        (hours, minutes) tuple
    """
    if distance_km is None:
        return (0, 0)

    # TODO: Calculate time
    time_hours = distance_km / speed_kmh

    hours = int(time_hours)
    minutes = None  # TODO: remaining minutes

    return hours, minutes


def format_walking_time(hours, minutes):
    """Format walking time as a readable string."""
    if hours == 0:
        return f"{minutes} min"
    elif minutes == 0:
        return f"{hours} hr"
    else:
        return f"{hours} hr {minutes} min"


# ============================================================
# Exercise 5: Route Calculator
# ============================================================

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

    # TODO: Sum distances between consecutive points
    for i in range(len(route) - 1):
        dist = haversine(route[i], route[i + 1])
        if dist is not None:
            total += dist

    return total


# ============================================================
# Test Data
# ============================================================

# Taipei locations
TAIPEI_101 = (25.0330, 121.5654)
TOKYO_TOWER = (35.6586, 139.7454)
MAIN_STATION = (25.0478, 121.5170)

MRT_STATIONS = [
    ("Taipei 101/World Trade Center", 25.0330, 121.5637),
    ("Xiangshan", 25.0329, 121.5707),
    ("Taipei City Hall", 25.0408, 121.5679),
    ("Yongchun", 25.0403, 121.5762),
    ("Houshanpi", 25.0446, 121.5824),
]

WALKING_TOUR = [
    (25.0330, 121.5654),  # Taipei 101
    (25.0339, 121.5645),  # Din Tai Fung
    (25.0329, 121.5598),  # Yongkang Street
    (25.0279, 121.5595),  # Daan Park
    (25.0174, 121.5405),  # NTU
]


# ============================================================
# Test your code
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 1-2 Lab Tests")
    print("=" * 60)

    # Test Exercise 1
    print("\n[Exercise 1: Basic Functions]")

    # Test celsius_to_fahrenheit
    result = celsius_to_fahrenheit(0)
    if result == 32.0:
        print("✓ celsius_to_fahrenheit(0) = 32.0")
    else:
        print(f"✗ celsius_to_fahrenheit(0) should be 32.0, got {result}")

    # Test format_coordinate
    result = format_coordinate(TAIPEI_101)
    if result is not None and "25.0330" in result and "N" in result:
        print(f"✓ format_coordinate: {result}")
    else:
        print("✗ format_coordinate not implemented correctly")

    # Test Exercise 2
    print("\n[Exercise 2: Math Module]")

    # Test distance_2d
    result = distance_2d((0, 0), (3, 4))
    if result == 5.0:
        print("✓ distance_2d((0,0), (3,4)) = 5.0")
    else:
        print(f"✗ distance_2d should be 5.0, got {result}")

    # Test Exercise 3
    print("\n[Exercise 3: Haversine]")

    # Test haversine
    result = haversine(TAIPEI_101, TOKYO_TOWER)
    if result is not None and 2100 < result < 2150:
        print(f"✓ Taipei to Tokyo: {result:.2f} km")
    else:
        print(f"✗ Taipei to Tokyo should be ~2111 km, got {result}")

    result = haversine(TAIPEI_101, MAIN_STATION)
    if result is not None and 5 < result < 6:
        print(f"✓ Taipei 101 to Main Station: {result:.2f} km")
    else:
        print(f"✗ Taipei 101 to Main Station should be ~5.4 km, got {result}")

    # Test Exercise 4
    print("\n[Exercise 4: Applications]")

    # Test find_nearest
    nearest, dist = find_nearest(TAIPEI_101, MRT_STATIONS)
    if nearest is not None:
        print(f"✓ Nearest MRT: {nearest} ({dist*1000:.0f}m)")
    else:
        print("✗ find_nearest not implemented")

    # Test sort_by_distance
    sorted_stations = sort_by_distance(TAIPEI_101, MRT_STATIONS)
    if len(sorted_stations) > 0 and sorted_stations[0][1] < sorted_stations[-1][1]:
        print("✓ Stations sorted by distance")
    else:
        print("✗ sort_by_distance not working correctly")

    # Test Exercise 5
    print("\n[Exercise 5: Route Calculator]")

    total = calculate_route_distance(WALKING_TOUR)
    if total > 0:
        hrs, mins = estimate_walking_time(total)
        print(f"✓ Tour: {total:.2f} km, {format_walking_time(hrs, mins)}")
    else:
        print("✗ calculate_route_distance not working")

    print("\n" + "=" * 60)
    print("Complete all ✗ items to finish the lab!")
