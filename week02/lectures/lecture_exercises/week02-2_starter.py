"""
Week 2-2 Lab: Dictionaries & Storing "Places"
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
# Exercise 1: Dictionary Basics
# ============================================================

# Task 1.1: Create a place dictionary
my_favorite = {
    "name": None,       # TODO: Fill in
    "lat": None,        # TODO: Fill in
    "lon": None,        # TODO: Fill in
    "rating": None,     # TODO: Fill in
    "category": "restaurant"
}


# Task 1.2: Access dictionary values
sample_place = {
    "name": "Din Tai Fung",
    "lat": 25.0339,
    "lon": 121.5645,
    "rating": 4.9,
    "category": "restaurant",
    "tags": ["dumplings", "michelin", "taiwanese"]
}

def get_place_info(place):
    """Extract and return place information."""
    # TODO: Get name, rating, and first tag
    name = None
    rating = None
    first_tag = None
    address = None  # TODO: Use .get() with default "N/A"

    return name, rating, first_tag, address


# Task 1.3: Modify dictionary
def add_place_details(place):
    """Add details to a place dictionary."""
    # TODO: Add category, coordinates, and tags
    # Return the modified place
    return place


# ============================================================
# Exercise 2: Iterating Over Dictionaries
# ============================================================

def print_place_details(place):
    """Task 2.1: Print all key-value pairs."""
    # TODO: Loop through items() and print each
    pass


def print_all_names_ratings(places):
    """Task 2.2: Print name and rating for each place."""
    # TODO: Loop through places and print name: rating
    pass


def calculate_average_rating(places):
    """Task 2.3: Calculate average rating of all places."""
    # TODO: Calculate and return average
    return None


# ============================================================
# Exercise 3: Nested Data Structures
# ============================================================

# Task 3.1: Dictionary with tuple coordinates
place_with_coords = {
    "name": "Taipei 101",
    "coords": (25.0330, 121.5654),
    "rating": 4.7
}

def get_coordinates(place):
    """Extract latitude and longitude from a place."""
    # TODO: Return (lat, lon) tuple from coords
    return None, None


# Task 3.2: Dictionary with nested dictionary
nested_place = {
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

def get_nested_info(place):
    """Extract nested information from a place."""
    # TODO: Get lat, floors, and city
    lat = None
    floors = None
    city = None
    return lat, floors, city


# Task 3.3: Build complete place structure
def create_complete_place(name, lat, lon, rating, category, tags, hours_dict):
    """Create a complete place dictionary."""
    # TODO: Build and return the place dict
    return None


# ============================================================
# Exercise 4: Place Database Operations
# ============================================================

# Sample database
PLACES_DB = [
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
    },
    {
        "name": "Elephant Mountain",
        "coords": (25.0271, 121.5576),
        "rating": 4.6,
        "category": "landmark"
    },
    {
        "name": "Raohe Night Market",
        "coords": (25.0504, 121.5775),
        "rating": 4.4,
        "category": "market"
    },
]


def find_by_name(places, name):
    """Task 4.2: Find a place by name."""
    # TODO: Return the place dict or None
    return None


def filter_by_category(places, category):
    """Task 4.3: Get all places in a category."""
    # TODO: Return list of matching places
    return []


def filter_by_rating(places, min_rating):
    """Task 4.4: Get all places with rating >= min_rating."""
    # TODO: Return list of matching places
    return []


def sort_by_rating(places, descending=True):
    """Task 4.5: Sort places by rating."""
    # TODO: Return sorted list (new list, don't modify original)
    return []


# ============================================================
# Exercise 5: Advanced Queries
# ============================================================

def find_nearby(places, center, max_km):
    """
    Task 5.1: Find all places within max_km of center.
    Returns list of (place, distance) tuples, sorted by distance.
    """
    results = []
    # TODO: Calculate distances and filter
    return results


def search_places(places, center=None, max_km=None, min_rating=None, category=None):
    """
    Task 5.2: Search with multiple optional filters.
    """
    results = places.copy()

    # TODO: Apply filters if specified
    # Filter by category
    # Filter by rating
    # Filter by distance

    return results


def get_database_stats(places):
    """
    Task 5.3: Get database statistics.
    Returns dict with: total_places, categories, avg_rating,
                       highest_rated, lowest_rated
    """
    if not places:
        return None

    # TODO: Calculate statistics
    stats = {
        "total_places": None,
        "categories": {},
        "avg_rating": None,
        "highest_rated": None,
        "lowest_rated": None,
    }

    return stats


# ============================================================
# Exercise 6: Dictionary Comprehension
# ============================================================

def create_coords_lookup(places):
    """Task 6.1: Create name -> coords lookup dictionary."""
    # TODO: Use dictionary comprehension
    return {}


def create_rating_lookup(places):
    """Task 6.1: Create name -> rating lookup dictionary."""
    # TODO: Use dictionary comprehension
    return {}


def create_info_lookup(places):
    """Task 6.2: Create name -> formatted info lookup."""
    # Format: "4.7★ at (25.0330, 121.5654)"
    # TODO: Use dictionary comprehension
    return {}


# ============================================================
# Test Code
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 2-2 Lab Tests")
    print("=" * 60)

    # Test Exercise 1
    print("\n[Exercise 1: Dictionary Basics]")
    if my_favorite["name"] and my_favorite["lat"]:
        print(f"✓ my_favorite place: {my_favorite['name']}")
    else:
        print("✗ Complete my_favorite dictionary")

    name, rating, tag, addr = get_place_info(sample_place)
    if name == "Din Tai Fung" and rating == 4.9:
        print(f"✓ get_place_info working: {name}, {rating}★")
    else:
        print("✗ get_place_info not working correctly")

    # Test Exercise 2
    print("\n[Exercise 2: Iteration]")
    avg = calculate_average_rating(PLACES_DB)
    if avg and 4.0 < avg < 5.0:
        print(f"✓ Average rating: {avg:.2f}")
    else:
        print("✗ calculate_average_rating not working")

    # Test Exercise 3
    print("\n[Exercise 3: Nested Data]")
    lat, lon = get_coordinates(place_with_coords)
    if lat == 25.0330 and lon == 121.5654:
        print(f"✓ Coordinates extracted: ({lat}, {lon})")
    else:
        print("✗ get_coordinates not working")

    lat, floors, city = get_nested_info(nested_place)
    if lat == 25.0330 and floors == 101 and city == "Taipei":
        print(f"✓ Nested info: lat={lat}, floors={floors}, city={city}")
    else:
        print("✗ get_nested_info not working")

    # Test Exercise 4
    print("\n[Exercise 4: Database Operations]")

    result = find_by_name(PLACES_DB, "Taipei 101")
    if result and result["name"] == "Taipei 101":
        print(f"✓ find_by_name working")
    else:
        print("✗ find_by_name not working")

    restaurants = filter_by_category(PLACES_DB, "restaurant")
    if len(restaurants) == 1:
        print(f"✓ filter_by_category working: {len(restaurants)} restaurant(s)")
    else:
        print(f"✗ filter_by_category not working (expected 1, got {len(restaurants)})")

    top = filter_by_rating(PLACES_DB, 4.6)
    if len(top) == 3:
        print(f"✓ filter_by_rating working: {len(top)} places >= 4.6")
    else:
        print(f"✗ filter_by_rating not working (expected 3, got {len(top)})")

    sorted_places = sort_by_rating(PLACES_DB)
    if sorted_places and sorted_places[0]["name"] == "Din Tai Fung":
        print(f"✓ sort_by_rating working: top is {sorted_places[0]['name']}")
    else:
        print("✗ sort_by_rating not working")

    # Test Exercise 5
    print("\n[Exercise 5: Advanced Queries]")

    my_loc = (25.0330, 121.5654)  # Taipei 101
    nearby = find_nearby(PLACES_DB, my_loc, 1.0)
    if nearby and len(nearby) >= 2:
        print(f"✓ find_nearby working: {len(nearby)} places within 1km")
    else:
        print("✗ find_nearby not working")

    results = search_places(PLACES_DB, center=my_loc, max_km=5.0, min_rating=4.5)
    if results:
        print(f"✓ search_places working: {len(results)} results")
    else:
        print("✗ search_places not working")

    stats = get_database_stats(PLACES_DB)
    if stats and stats["total_places"] == 5:
        print(f"✓ get_database_stats working: {stats['total_places']} places")
    else:
        print("✗ get_database_stats not working")

    # Test Exercise 6
    print("\n[Exercise 6: Dictionary Comprehension]")

    coords_lookup = create_coords_lookup(PLACES_DB)
    if "Taipei 101" in coords_lookup:
        print(f"✓ coords_lookup working")
    else:
        print("✗ create_coords_lookup not working")

    rating_lookup = create_rating_lookup(PLACES_DB)
    if rating_lookup.get("Din Tai Fung") == 4.9:
        print(f"✓ rating_lookup working")
    else:
        print("✗ create_rating_lookup not working")

    print("\n" + "=" * 60)
    print("Complete all ✗ items to finish the lab!")
