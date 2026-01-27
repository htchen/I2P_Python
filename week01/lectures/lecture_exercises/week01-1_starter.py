"""
Week 1-1 Lab: Variables & The Coordinate System
Starter Code

Instructions:
1. Complete each TODO section
2. Run the file to test your code
3. All tests should pass when you're done
"""

# ============================================================
# Exercise 1: Variable Basics
# ============================================================

# Task 1.1: Create variables for your favorite city
# TODO: Fill in the values

city_name = "Taipei"  # Change to your favorite city
population = None     # TODO: Fill in the population (integer)
area_km2 = None       # TODO: Fill in the area (float)
founded_year = None   # TODO: Fill in the year (integer)

# Uncomment when ready:
# print(f"City: {city_name}")
# print(f"Population: {population}")
# print(f"Area: {area_km2} km²")
# print(f"Founded: {founded_year}")


# Task 1.2: Calculate population density
# TODO: Calculate density = population / area

population_density = None  # TODO: Calculate this

# Uncomment when ready:
# print(f"Population density: {population_density:.2f} people/km²")


# Task 1.3: Check variable types
# TODO: Print the type of each variable

# print(f"city_name is type: {type(city_name)}")
# print(f"population is type: {type(population)}")
# Add more...


# ============================================================
# Exercise 2: Working with Floats
# ============================================================

# Task 2.1: Coordinate precision
lat = 25.0329833
lon = 121.5654268

# TODO: Print with different precision levels
# print(f"Full precision: ({lat}, {lon})")
# print(f"4 decimal places: ({lat:.4f}, {lon:.4f})")
# print(f"2 decimal places: ...")
# print(f"0 decimal places: ...")


# Task 2.2: What precision do you need for a restaurant finder?
recommended_precision = None  # TODO: Fill in a number (1-6)

# Explain your answer in a comment:
# Your explanation: ...


# ============================================================
# Exercise 3: Tuples for Coordinates
# ============================================================

# Task 3.1: Create coordinate tuples
# TODO: Search online for the coordinates and fill them in

taipei_101 = (25.0330, 121.5654)  # Given
ntu_main_library = (None, None)   # TODO: Find coordinates
taipei_main_station = (None, None)
shilin_night_market = (None, None)

# International landmarks
eiffel_tower = (None, None)
statue_of_liberty = (None, None)


# Task 3.2: Accessing tuple elements
# TODO: Extract latitude and longitude from taipei_101

latitude = None   # TODO: taipei_101[?]
longitude = None  # TODO: taipei_101[?]

# TODO: Use tuple unpacking
# lat, lon = taipei_101


# Task 3.3: Tuple immutability
# TODO: Uncomment and run to see the error
# taipei_101[0] = 26.0  # This will fail!

# TODO: Create a new tuple with modified latitude
new_location = None  # (new_latitude, taipei_101[1])


# ============================================================
# Exercise 4: Multiple Locations
# ============================================================

# Task 4.1: Create a list of locations
my_taipei_tour = [
    (25.0330, 121.5654),  # Stop 1: Taipei 101
    # TODO: Add 4 more stops
]


# Task 4.2: Named locations
locations = [
    ("Taipei 101", 25.0330, 121.5654),
    # TODO: Add more named locations
]


# Task 4.3: Calculate bounding box
# TODO: Find min/max latitude and longitude

latitudes = [coord[0] for coord in my_taipei_tour]
longitudes = None  # TODO: Extract longitudes similarly

min_lat = None  # TODO: min(latitudes)
max_lat = None
min_lon = None
max_lon = None

# Uncomment when ready:
# print(f"Bounding Box:")
# print(f"  Latitude:  {min_lat} to {max_lat}")
# print(f"  Longitude: {min_lon} to {max_lon}")


# ============================================================
# Exercise 5: Challenge - Coordinate Formatter
# ============================================================

def format_coordinate(coord):
    """Format a coordinate as a readable string."""
    lat, lon = coord

    # Determine N/S and E/W
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"

    # TODO: Return formatted string like "25.0330°N, 121.5654°E"
    return None


def is_valid_coordinate(coord):
    """Check if a coordinate is valid."""
    lat, lon = coord

    # TODO: Check if lat is between -90 and 90
    # TODO: Check if lon is between -180 and 180
    lat_valid = None
    lon_valid = None

    return lat_valid and lon_valid


# ============================================================
# Test your code
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Week 1-1 Lab Tests")
    print("=" * 50)

    # Test Exercise 1
    print("\n[Exercise 1: Variables]")
    if population is not None and area_km2 is not None:
        density = population / area_km2
        print(f"✓ {city_name}: {density:.0f} people/km²")
    else:
        print("✗ Complete Exercise 1 first")

    # Test Exercise 3
    print("\n[Exercise 3: Tuples]")
    if ntu_main_library[0] is not None:
        print(f"✓ NTU Library: {ntu_main_library}")
    else:
        print("✗ Fill in the coordinates for NTU Library")

    # Test Exercise 4
    print("\n[Exercise 4: Multiple Locations]")
    if len(my_taipei_tour) >= 5:
        print(f"✓ Tour has {len(my_taipei_tour)} stops")
    else:
        print(f"✗ Tour needs at least 5 stops (has {len(my_taipei_tour)})")

    # Test Exercise 5
    print("\n[Exercise 5: Formatter]")
    result = format_coordinate((25.0330, 121.5654))
    if result is not None:
        print(f"✓ Formatted: {result}")
    else:
        print("✗ Complete format_coordinate function")

    print("\n" + "=" * 50)
    print("Complete all ✗ items to finish the lab!")
