"""
Week 3 Lab: JSON & File I/O
Starter Code

Instructions:
1. Complete each TODO section
2. Run the file to test your code
3. All tests should pass when you're done
"""

import json
import os

# ============================================================
# Exercise 1: JSON Basics
# ============================================================

# Task 1.1: Python to JSON String
def python_to_json_demo():
    """Demonstrate converting Python to JSON."""
    place = {
        "name": "Taipei 101",
        "coords": (25.0330, 121.5654),  # Tuple becomes list in JSON
        "rating": 4.7,
        "is_open": True,
        "tags": ["landmark", "shopping"]
    }

    # TODO: Convert to JSON string
    json_string = None  # json.dumps(place)

    # TODO: Convert with pretty printing (indent=2)
    json_pretty = None  # json.dumps(place, indent=2)

    return json_string, json_pretty


# Task 1.2: JSON String to Python
def json_to_python_demo():
    """Demonstrate parsing JSON to Python."""
    json_string = '''
    {
        "name": "Din Tai Fung",
        "coords": [25.0339, 121.5645],
        "rating": 4.9,
        "is_open": true,
        "categories": ["restaurant", "dumplings"]
    }
    '''

    # TODO: Parse JSON string to Python dict
    place = None  # json.loads(json_string)

    if place:
        name = None        # TODO: Get name
        rating = None      # TODO: Get rating
        first_cat = None   # TODO: Get first category

        return name, rating, first_cat
    return None, None, None


# Task 1.3: Handle Chinese Characters
def chinese_json_demo():
    """Demonstrate handling Chinese in JSON."""
    place = {
        "name": "鼎泰豐",
        "city": "台北",
        "rating": 4.9
    }

    # TODO: Convert with escaped characters (default behavior)
    json_escaped = None  # json.dumps(place)

    # TODO: Convert keeping Chinese readable
    json_readable = None  # json.dumps(place, ensure_ascii=False)

    return json_escaped, json_readable


# ============================================================
# Exercise 2: File Operations
# ============================================================

# Task 2.1 & 2.2: Write and Read Text File
def text_file_demo():
    """Demonstrate basic text file operations."""
    # TODO: Write to file
    # with open("greeting.txt", "w", encoding="utf-8") as f:
    #     f.write("Hello, World!\n")
    #     f.write("Welcome to Week 3!")

    # TODO: Read file content
    content = None
    # with open("greeting.txt", "r", encoding="utf-8") as f:
    #     content = f.read()

    return content


# Task 2.3: Read Lines
def read_lines_demo():
    """Demonstrate reading file line by line."""
    # Create test file
    with open("cities.txt", "w", encoding="utf-8") as f:
        f.write("Taipei\nTokyo\nSeoul\nBangkok\n")

    # TODO: Read all lines as a list
    lines = []
    # with open("cities.txt", "r", encoding="utf-8") as f:
    #     lines = f.readlines()

    # TODO: Strip whitespace from each line
    cities = []  # [line.strip() for line in lines]

    return cities


# ============================================================
# Exercise 3: JSON File I/O
# ============================================================

def save_places(places, filename):
    """
    Save a list of places to a JSON file.

    Args:
        places: List of place dictionaries
        filename: Name of the file to save to
    """
    # TODO: Implement save function
    # with open(filename, "w", encoding="utf-8") as f:
    #     json.dump(places, f, indent=2, ensure_ascii=False)
    pass


def load_places(filename):
    """
    Load places from a JSON file.

    Args:
        filename: Name of the file to load from

    Returns:
        List of place dictionaries
    """
    # TODO: Implement load function
    # with open(filename, "r", encoding="utf-8") as f:
    #     return json.load(f)
    return []


# ============================================================
# Exercise 4: Error Handling
# ============================================================

def load_places_safe(filename):
    """
    Safely load places from a JSON file.
    Returns empty list if file doesn't exist or is invalid.
    """
    # TODO: Implement with try/except
    # try:
    #     with open(filename, "r", encoding="utf-8") as f:
    #         return json.load(f)
    # except FileNotFoundError:
    #     return []
    # except json.JSONDecodeError:
    #     return []
    return []


def load_or_create(filename, default_data=None):
    """
    Load data from file, or create with default data if doesn't exist.
    """
    if default_data is None:
        default_data = []

    # TODO: Check if file exists and load, otherwise create
    # if os.path.exists(filename):
    #     with open(filename, "r", encoding="utf-8") as f:
    #         return json.load(f)
    # else:
    #     with open(filename, "w", encoding="utf-8") as f:
    #         json.dump(default_data, f, indent=2)
    #     return default_data

    return default_data


# ============================================================
# Exercise 5: Place Database Class
# ============================================================

class PlaceDatabase:
    """A simple JSON-based place database."""

    def __init__(self, filename="places_db.json"):
        """Initialize database with given filename."""
        self.filename = filename
        self.places = self._load()

    def _load(self):
        """Load places from file (private method)."""
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save(self):
        """Save places to file (private method)."""
        # TODO: Save self.places to self.filename
        pass

    def add(self, place):
        """Add a new place to the database."""
        # TODO: Append place and save
        pass

    def find_by_name(self, name):
        """Find a place by name. Returns None if not found."""
        # TODO: Search through places
        return None

    def update(self, name, updates):
        """Update a place by name."""
        place = self.find_by_name(name)
        if place:
            # TODO: Update the place with new values
            # place.update(updates)
            # self._save()
            return True
        return False

    def delete(self, name):
        """Delete a place by name."""
        # TODO: Remove place with matching name and save
        return False

    def all(self):
        """Get all places."""
        return self.places

    def count(self):
        """Get number of places."""
        return len(self.places)

    def search(self, **criteria):
        """
        Search places by criteria.
        Example: db.search(category="restaurant", min_rating=4.5)
        """
        results = self.places

        if "category" in criteria:
            results = [p for p in results if p.get("category") == criteria["category"]]

        if "min_rating" in criteria:
            results = [p for p in results if p.get("rating", 0) >= criteria["min_rating"]]

        return results


# ============================================================
# Exercise 6: Complex JSON
# ============================================================

def process_api_response(api_response):
    """
    Process a simulated API response.

    Args:
        api_response: JSON string containing API response

    Returns:
        List of (name, lat, lon) tuples
    """
    # TODO: Parse and process the response
    # data = json.loads(api_response)
    # results = []
    # for item in data.get("results", []):
    #     name = item["display_name"].split(",")[0]
    #     lat = float(item["lat"])
    #     lon = float(item["lon"])
    #     results.append((name, lat, lon))
    # return results
    return []


# ============================================================
# Test Data
# ============================================================

SAMPLE_PLACES = [
    {
        "name": "Taipei 101",
        "coords": [25.0330, 121.5654],
        "rating": 4.7,
        "category": "landmark"
    },
    {
        "name": "Din Tai Fung",
        "coords": [25.0339, 121.5645],
        "rating": 4.9,
        "category": "restaurant"
    },
    {
        "name": "Shilin Night Market",
        "coords": [25.0878, 121.5241],
        "rating": 4.5,
        "category": "market"
    }
]

SAMPLE_API_RESPONSE = '''
{
    "results": [
        {
            "place_id": 123456,
            "display_name": "Taipei 101, Xinyi District, Taipei City, Taiwan",
            "lat": "25.0329694",
            "lon": "121.5654268",
            "type": "attraction"
        },
        {
            "place_id": 789012,
            "display_name": "Din Tai Fung, Da'an District, Taipei City, Taiwan",
            "lat": "25.0339",
            "lon": "121.5645",
            "type": "restaurant"
        }
    ],
    "status": "OK",
    "total": 2
}
'''


# ============================================================
# Test Code
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 3 Lab Tests")
    print("=" * 60)

    # Test Exercise 1
    print("\n[Exercise 1: JSON Basics]")

    json_str, json_pretty = python_to_json_demo()
    if json_str and "Taipei 101" in json_str:
        print("✓ python_to_json_demo working")
    else:
        print("✗ Complete python_to_json_demo")

    name, rating, cat = json_to_python_demo()
    if name == "Din Tai Fung" and rating == 4.9:
        print("✓ json_to_python_demo working")
    else:
        print("✗ Complete json_to_python_demo")

    escaped, readable = chinese_json_demo()
    if readable and "鼎泰豐" in readable:
        print("✓ chinese_json_demo working")
    else:
        print("✗ Complete chinese_json_demo")

    # Test Exercise 2
    print("\n[Exercise 2: File Operations]")

    content = text_file_demo()
    if content and "Hello" in content:
        print("✓ text_file_demo working")
    else:
        print("✗ Complete text_file_demo")

    cities = read_lines_demo()
    if cities and len(cities) == 4 and cities[0] == "Taipei":
        print(f"✓ read_lines_demo working: {cities}")
    else:
        print("✗ Complete read_lines_demo")

    # Test Exercise 3
    print("\n[Exercise 3: JSON File I/O]")

    save_places(SAMPLE_PLACES, "test_places.json")
    if os.path.exists("test_places.json"):
        loaded = load_places("test_places.json")
        if loaded and len(loaded) == 3:
            print(f"✓ save_places and load_places working")
        else:
            print("✗ Complete load_places")
    else:
        print("✗ Complete save_places")

    # Test Exercise 4
    print("\n[Exercise 4: Error Handling]")

    result = load_places_safe("nonexistent_file.json")
    if result == []:
        print("✓ load_places_safe handles missing file")
    else:
        print("✗ Complete load_places_safe")

    # Test Exercise 5
    print("\n[Exercise 5: PlaceDatabase]")

    # Clean up test database
    if os.path.exists("test_db.json"):
        os.remove("test_db.json")

    db = PlaceDatabase("test_db.json")
    db.add({"name": "Test Place", "rating": 4.0})

    if db.count() == 1:
        print("✓ PlaceDatabase.add working")
    else:
        print("✗ Complete PlaceDatabase.add")

    found = db.find_by_name("Test Place")
    if found and found["name"] == "Test Place":
        print("✓ PlaceDatabase.find_by_name working")
    else:
        print("✗ Complete PlaceDatabase.find_by_name")

    # Test persistence
    db2 = PlaceDatabase("test_db.json")
    if db2.count() == 1:
        print("✓ PlaceDatabase persistence working")
    else:
        print("✗ Complete PlaceDatabase._save")

    # Test Exercise 6
    print("\n[Exercise 6: Complex JSON]")

    results = process_api_response(SAMPLE_API_RESPONSE)
    if results and len(results) == 2:
        print(f"✓ process_api_response working: {results[0][0]}")
    else:
        print("✗ Complete process_api_response")

    # Cleanup
    print("\n[Cleanup]")
    test_files = ["greeting.txt", "cities.txt", "test_places.json", "test_db.json"]
    for f in test_files:
        if os.path.exists(f):
            os.remove(f)
            print(f"  Removed: {f}")

    print("\n" + "=" * 60)
    print("Complete all ✗ items to finish the lab!")
