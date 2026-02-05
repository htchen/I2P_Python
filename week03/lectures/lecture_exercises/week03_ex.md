# Week 3 Lab: JSON & File I/O

## Lab Overview

In this lab, you will practice:
- Converting between Python objects and JSON
- Reading and writing text files
- Working with JSON files
- Building a persistent place database
- Handling file errors gracefully

---

## Exercise 1: JSON Basics (10 minutes)

### Task 1.1: Python to JSON String

```python
import json

# TODO: Convert this Python dictionary to a JSON string
place = {
    "name": "Taipei 101",
    "coords": (25.0330, 121.5654),  # Note: tuple!
    "rating": 4.7,
    "is_open": True,
    "tags": ["landmark", "shopping"]
}

# Convert to JSON string
json_string = json.___(place)
print(json_string)

# TODO: Convert with pretty printing (indent=2)
json_pretty = json.dumps(place, indent=___)
print(json_pretty)

# Question: What happened to the tuple? Why?
# Answer: ___
```

### Task 1.2: JSON String to Python

```python
import json

# TODO: Parse this JSON string to a Python object
json_string = '''
{
    "name": "Din Tai Fung",
    "coords": [25.0339, 121.5645],
    "rating": 4.9,
    "is_open": true,
    "categories": ["restaurant", "dumplings"]
}
'''

# Parse JSON string
place = json.___(json_string)

# TODO: Access the data
name = place["___"]
rating = place["___"]
first_category = place["categories"][___]

print(f"Name: {name}")
print(f"Rating: {rating}")
print(f"First category: {first_category}")

# TODO: Check the type of is_open
print(f"is_open type: {type(place['is_open'])}")  # Should be <class 'bool'>
```

### Task 1.3: Handling Chinese Characters

```python
import json

place = {
    "name": "鼎泰豐",
    "city": "台北",
    "rating": 4.9
}

# TODO: Convert to JSON with escaped characters (default)
json_escaped = json.dumps(place)
print(f"Escaped: {json_escaped}")

# TODO: Convert to JSON keeping Chinese readable
json_readable = json.dumps(place, ensure_ascii=___)
print(f"Readable: {json_readable}")
```

---

## Exercise 2: File Operations (10 minutes)

### Task 2.1: Write and Read Text File

```python
# TODO: Write a greeting to a file
with open("greeting.txt", "___", encoding="utf-8") as f:
    f.write("Hello, World!\n")
    f.write("Welcome to Week 3!")

print("File written!")

# TODO: Read the file back
with open("greeting.txt", "___", encoding="utf-8") as f:
    content = f.___()

print("File content:")
print(content)
```

### Task 2.2: Append to File

```python
# TODO: Append a new line to the file
with open("greeting.txt", "___", encoding="utf-8") as f:
    f.write("\nThis line was appended!")

# Read and verify
with open("greeting.txt", "r", encoding="utf-8") as f:
    print(f.read())
```

### Task 2.3: Read Lines

```python
# Create a file with multiple lines
with open("cities.txt", "w", encoding="utf-8") as f:
    f.write("Taipei\n")
    f.write("Tokyo\n")
    f.write("Seoul\n")
    f.write("Bangkok\n")

# TODO: Read all lines as a list
with open("cities.txt", "r", encoding="utf-8") as f:
    lines = f.___()  # Returns a list of lines

print(f"Number of lines: {len(lines)}")

# TODO: Print each city (strip removes the \n)
for line in lines:
    city = line.___()  # Remove whitespace/newline
    print(f"City: {city}")
```

---

## Exercise 3: JSON File I/O (15 minutes)

### Task 3.1: Save Places to JSON File

```python
import json

places = [
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

# TODO: Save to JSON file with pretty printing
with open("places.json", "___", encoding="utf-8") as f:
    json.___(places, f, indent=2, ensure_ascii=False)

print("Places saved to places.json")
```

### Task 3.2: Load Places from JSON File

```python
import json

# TODO: Load places from the JSON file
with open("places.json", "___", encoding="utf-8") as f:
    loaded_places = json.___(f)

print(f"Loaded {len(loaded_places)} places:")
for place in loaded_places:
    print(f"  - {place['name']}: {place['rating']}★")
```

### Task 3.3: Create Save/Load Functions

```python
import json

def save_places(places, filename):
    """
    Save a list of places to a JSON file.

    Args:
        places: List of place dictionaries
        filename: Name of the file to save to
    """
    # TODO: Implement save function
    with open(filename, "___", encoding="utf-8") as f:
        json.___(places, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(places)} places to {filename}")


def load_places(filename):
    """
    Load places from a JSON file.

    Args:
        filename: Name of the file to load from

    Returns:
        List of place dictionaries
    """
    # TODO: Implement load function
    with open(filename, "___", encoding="utf-8") as f:
        places = json.___(f)
    print(f"Loaded {len(places)} places from {filename}")
    return places


# Test your functions
test_places = [
    {"name": "Test Place 1", "rating": 4.0},
    {"name": "Test Place 2", "rating": 4.5},
]

save_places(test_places, "test_places.json")
loaded = load_places("test_places.json")

# Verify they match
assert len(loaded) == len(test_places)
print("✓ Save/Load functions working!")
```

---

## Exercise 4: Error Handling (15 minutes)

### Task 4.1: Handle File Not Found

```python
import json

def load_places_safe(filename):
    """
    Safely load places from a JSON file.
    Returns empty list if file doesn't exist.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        print(f"File {filename} not found. Returning empty list.")
        return ___

    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {filename}: {e}")
        return ___


# TODO: Test with existing file
places = load_places_safe("places.json")
print(f"Loaded {len(places)} places")

# TODO: Test with non-existent file
places = load_places_safe("nonexistent.json")
print(f"Loaded {len(places)} places")  # Should be 0
```

### Task 4.2: Handle Invalid JSON

```python
import json

# Create a file with invalid JSON
with open("invalid.json", "w") as f:
    f.write("this is not valid json {{{")

# TODO: Try to load it (should handle error gracefully)
result = load_places_safe("invalid.json")
print(f"Result: {result}")  # Should be []
```

### Task 4.3: Check if File Exists

```python
import os

def load_or_create(filename, default_data=None):
    """
    Load data from file, or create with default data if file doesn't exist.
    """
    if default_data is None:
        default_data = []

    # TODO: Check if file exists
    if os.path.___(filename):
        # File exists, load it
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # File doesn't exist, create it with default data
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=2)
        print(f"Created new file: {filename}")
        return default_data


# Test
places = load_or_create("new_places.json", default_data=[
    {"name": "Default Place", "rating": 4.0}
])
print(f"Places: {places}")
```

---

## Exercise 5: Building a Place Database (20 minutes)

### Task 5.1: Complete the PlaceDatabase Class

```python
import json
import os

class PlaceDatabase:
    """A simple JSON-based place database."""

    def __init__(self, filename="places_db.json"):
        """Initialize database with given filename."""
        self.filename = filename
        self.places = self._load()

    def _load(self):
        """Load places from file (private method)."""
        # TODO: Return empty list if file doesn't exist
        if not os.path.exists(self.___):
            return []

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save(self):
        """Save places to file (private method)."""
        # TODO: Save self.places to self.filename
        with open(self.___, "w", encoding="utf-8") as f:
            json.dump(self.___, f, indent=2, ensure_ascii=False)

    def add(self, place):
        """Add a new place to the database."""
        # TODO: Append place and save
        self.places.___(place)
        self._save()
        print(f"Added: {place.get('name', 'Unknown')}")

    def find_by_name(self, name):
        """Find a place by name. Returns None if not found."""
        # TODO: Search through places
        for place in self.places:
            if place.get("name") == ___:
                return place
        return None

    def update(self, name, updates):
        """Update a place by name."""
        place = self.find_by_name(name)
        if place:
            # TODO: Update the place with new values
            place.___(updates)
            self._save()
            print(f"Updated: {name}")
            return True
        return False

    def delete(self, name):
        """Delete a place by name."""
        # TODO: Remove place with matching name
        original_count = len(self.places)
        self.places = [p for p in self.places if p.get("name") != ___]

        if len(self.places) < original_count:
            self._save()
            print(f"Deleted: {name}")
            return True
        return False

    def all(self):
        """Get all places."""
        return self.places

    def count(self):
        """Get number of places."""
        return len(self.___)

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
```

### Task 5.2: Test the Database

```python
# Create a new database
db = PlaceDatabase("my_database.json")

# Add places
db.add({
    "name": "Taipei 101",
    "coords": [25.0330, 121.5654],
    "rating": 4.7,
    "category": "landmark"
})

db.add({
    "name": "Din Tai Fung",
    "coords": [25.0339, 121.5645],
    "rating": 4.9,
    "category": "restaurant"
})

db.add({
    "name": "Shilin Night Market",
    "coords": [25.0878, 121.5241],
    "rating": 4.5,
    "category": "market"
})

# Find a place
place = db.find_by_name("Taipei 101")
print(f"\nFound: {place}")

# Update a place
db.update("Taipei 101", {"rating": 4.8, "visits": 100})

# Search
print("\nRestaurants:")
for p in db.search(category="restaurant"):
    print(f"  - {p['name']}")

print("\nTop rated (>= 4.6):")
for p in db.search(min_rating=4.6):
    print(f"  - {p['name']}: {p['rating']}★")

# List all
print(f"\nTotal places: {db.count()}")
for p in db.all():
    print(f"  - {p['name']}")

# Delete a place
db.delete("Shilin Night Market")
print(f"\nAfter deletion: {db.count()} places")
```

### Task 5.3: Persistence Test

```python
# Test that data persists
print("\n--- Persistence Test ---")

# Create fresh database instance (simulates restarting program)
db2 = PlaceDatabase("my_database.json")

print(f"Loaded {db2.count()} places from file:")
for p in db2.all():
    print(f"  - {p['name']}: {p.get('rating', 'N/A')}★")
```

---

## Exercise 6: Working with Complex JSON (10 minutes)

### Task 6.1: Nested JSON Structure

```python
import json

# Create a complex data structure
data = {
    "meta": {
        "version": "1.0",
        "last_updated": "2024-01-15",
        "author": "CS101 Student"
    },
    "places": [
        {
            "name": "Taipei 101",
            "location": {
                "coords": [25.0330, 121.5654],
                "city": "Taipei",
                "district": "Xinyi"
            },
            "details": {
                "rating": 4.7,
                "reviews": 15000,
                "tags": ["landmark", "shopping"]
            }
        }
    ]
}

# TODO: Save to file
with open("complex_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# TODO: Load and access nested data
with open("complex_data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

# Access nested values
version = loaded["meta"]["___"]
first_place = loaded["places"][___]
coords = first_place["location"]["___"]
rating = first_place["___"]["rating"]

print(f"Version: {version}")
print(f"First place: {first_place['name']}")
print(f"Coordinates: {coords}")
print(f"Rating: {rating}")
```

### Task 6.2: Process API-like Response

```python
import json

# Simulated API response (similar to what Nominatim returns)
api_response = '''
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

# TODO: Parse the response
data = json.___(api_response)

# TODO: Check status
if data["status"] == "OK":
    print(f"Found {data['total']} results:")

    # TODO: Process each result
    for result in data["results"]:
        # Extract short name (first part before comma)
        short_name = result["display_name"].split(",")[___]

        # Convert lat/lon strings to floats
        lat = ___(result["lat"])
        lon = ___(result["lon"])

        print(f"  - {short_name}: ({lat:.4f}, {lon:.4f})")
```

---

## Submission

Save your completed lab as `week03_lab_solution.py`.

### Checklist

- [ ] Exercise 1: JSON conversion (dumps, loads)
- [ ] Exercise 2: File operations (read, write, append)
- [ ] Exercise 3: JSON file I/O (dump, load)
- [ ] Exercise 4: Error handling (try/except)
- [ ] Exercise 5: PlaceDatabase class complete and tested
- [ ] Exercise 6: Complex/nested JSON processing

### Clean Up

```python
# Optional: Clean up test files
import os

test_files = [
    "greeting.txt", "cities.txt", "places.json",
    "test_places.json", "invalid.json", "new_places.json",
    "my_database.json", "complex_data.json"
]

for f in test_files:
    if os.path.exists(f):
        os.remove(f)
        print(f"Removed: {f}")
```
