"""
Week 2-1 Lab: Lists, Loops & The Route
Starter Code

Instructions:
1. Complete each TODO section
2. Run the file to test your code
3. All tests should pass when you're done
"""

import math

# ============================================================
# Haversine function (provided - do not modify)
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
# Exercise 1: List Basics
# ============================================================

# Task 1.1: Create and modify a list
cities = ["Taipei"]  # TODO: Add 4 more cities

# TODO: Add "Singapore" to the end


# TODO: Insert "Hong Kong" at index 2


# TODO: Remove "Taipei"


# Task 1.2: List slicing
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

first_three = None      # TODO: Get first 3 elements
last_three = None       # TODO: Get last 3 elements
middle = None           # TODO: Get elements at index 2-5
every_other = None      # TODO: Get every other element
reversed_list = None    # TODO: Reverse using slicing


# Task 1.3: List of coordinates
route = [
    (25.0330, 121.5654),  # Start: Taipei 101
    # TODO: Add 4 more coordinates
]


# ============================================================
# Exercise 2: For Loops
# ============================================================

# Sample route for exercises
sample_route = [
    (25.0330, 121.5654),
    (25.0339, 121.5645),
    (25.0329, 121.5598),
    (25.0279, 121.5595),
    (25.0174, 121.5405),
]


def print_route_basic(route):
    """Task 2.1: Print each coordinate."""
    # TODO: Use a for loop to print each coordinate
    pass


def print_route_numbered(route):
    """Task 2.2: Print each coordinate with stop number."""
    # TODO: Use enumerate() starting from 1
    pass


def print_route_unpacked(route):
    """Task 2.3: Print latitude and longitude separately."""
    # TODO: Unpack tuples in the loop
    pass


def print_range_examples():
    """Task 2.4: Practice with range()."""
    # TODO: Print numbers 1 to 10

    # TODO: Print even numbers 0 to 20

    # TODO: Print countdown 5 to 1
    pass


# ============================================================
# Exercise 3: Processing Consecutive Pairs
# ============================================================

def print_pairs_index(items):
    """Task 3.1: Print consecutive pairs using index."""
    # TODO: Use range(len(items) - 1)
    pass


def print_pairs_zip(items):
    """Task 3.2: Print consecutive pairs using zip()."""
    # TODO: Use zip(items[:-1], items[1:])
    pass


def calculate_segment_distances(route):
    """Task 3.3: Calculate distance of each segment."""
    distances = []
    # TODO: Calculate distance between consecutive points
    # Return list of distances
    return distances


# ============================================================
# Exercise 4: map() and filter()
# ============================================================

# Task 4.1: Temperature conversion
celsius_temps = [0, 10, 20, 25, 30, 35]

def to_fahrenheit(c):
    """Convert Celsius to Fahrenheit."""
    # TODO: Return the converted temperature
    return None

# TODO: Use map() to convert all temperatures
fahrenheit_temps = None


# Task 4.2: Extract data with map()
coords = [
    (25.0330, 121.5654),
    (25.0478, 121.5170),
    (25.0174, 121.5405),
    (25.0878, 121.5241),
]

# TODO: Extract all latitudes using map()
latitudes = None

# TODO: Extract all longitudes using map()
longitudes = None


# Task 4.3: Filter numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20]

# TODO: Filter to get only even numbers
evens = None

# TODO: Filter to get numbers greater than 10
big_numbers = None

# TODO: Filter to get numbers divisible by 3
div_by_3 = None


# Task 4.4: Filter coordinates
all_coords = [
    (25.0330, 121.5654),  # Taiwan
    (35.6586, 139.7454),  # Japan
    (25.0478, 121.5170),  # Taiwan
    (37.5665, 126.9780),  # Korea
    (25.0174, 121.5405),  # Taiwan
]

# TODO: Filter to keep only Taiwan coordinates (lat 22-26, lon 119-122)
taiwan_coords = None


# ============================================================
# Exercise 5: Route Calculator
# ============================================================

def calculate_route_stats(route):
    """
    Task 5.1: Calculate route statistics.

    Returns dict with: total_distance, segment_count, average_segment,
                       longest_segment, shortest_segment
    """
    if len(route) < 2:
        return None

    # TODO: Calculate segment distances
    segment_distances = []

    # TODO: Calculate and return statistics
    stats = {
        "total_distance": None,
        "segment_count": None,
        "average_segment": None,
        "longest_segment": None,
        "shortest_segment": None,
    }
    return stats


def get_bounding_box(route):
    """
    Task 5.2: Get the bounding box of a route.

    Returns dict with: min_lat, max_lat, min_lon, max_lon
    """
    # TODO: Extract latitudes and longitudes
    # TODO: Return min/max values
    return None


# ============================================================
# Test Code
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 2-1 Lab Tests")
    print("=" * 60)

    # Test Exercise 1
    print("\n[Exercise 1: Lists]")
    if len(cities) >= 5:
        print(f"✓ Cities list has {len(cities)} items")
    else:
        print(f"✗ Cities list needs at least 5 items (has {len(cities)})")

    if first_three == [0, 1, 2]:
        print("✓ first_three is correct")
    else:
        print(f"✗ first_three should be [0, 1, 2], got {first_three}")

    # Test Exercise 2
    print("\n[Exercise 2: For Loops]")
    print("Running print_route_numbered:")
    print_route_numbered(sample_route[:3])

    # Test Exercise 3
    print("\n[Exercise 3: Consecutive Pairs]")
    distances = calculate_segment_distances(sample_route)
    if distances and len(distances) == 4:
        total = sum(distances)
        print(f"✓ Segment distances calculated: {[f'{d:.3f}' for d in distances]}")
        print(f"  Total distance: {total:.2f} km")
    else:
        print("✗ calculate_segment_distances not working")

    # Test Exercise 4
    print("\n[Exercise 4: map() and filter()]")
    if fahrenheit_temps and fahrenheit_temps[0] == 32.0:
        print(f"✓ Temperature conversion working: {fahrenheit_temps}")
    else:
        print("✗ Temperature conversion not working")

    if latitudes:
        print(f"✓ Latitudes extracted: {latitudes}")
    else:
        print("✗ Latitude extraction not working")

    if taiwan_coords and len(taiwan_coords) == 3:
        print(f"✓ Taiwan filter working: {len(taiwan_coords)} coords")
    else:
        print("✗ Taiwan coordinate filter not working")

    # Test Exercise 5
    print("\n[Exercise 5: Route Calculator]")
    stats = calculate_route_stats(sample_route)
    if stats and stats["total_distance"]:
        print(f"✓ Route stats calculated:")
        print(f"  Total: {stats['total_distance']:.2f} km")
        print(f"  Segments: {stats['segment_count']}")
        print(f"  Average: {stats['average_segment']:.3f} km")
    else:
        print("✗ Route stats not working")

    bbox = get_bounding_box(sample_route)
    if bbox and "min_lat" in bbox:
        print(f"✓ Bounding box: lat [{bbox['min_lat']:.4f}, {bbox['max_lat']:.4f}]")
    else:
        print("✗ Bounding box not working")

    print("\n" + "=" * 60)
    print("Complete all ✗ items to finish the lab!")
