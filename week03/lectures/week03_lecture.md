# Week 3 Lecture: JSON & File I/O

## Learning Objectives

By the end of this lecture, students will be able to:
1. Understand the JSON data format
2. Read and write text files in Python
3. Parse JSON data into Python objects
4. Save Python data structures as JSON files
5. Handle file errors gracefully
6. Build a persistent place database

---

## Part 1: Why File I/O?

### The Problem with In-Memory Data

```python
# Every time you run the program, data is lost!
places = [
    {"name": "Taipei 101", "rating": 4.7},
    {"name": "Din Tai Fung", "rating": 4.9},
]

# Add a new place
places.append({"name": "Shilin Market", "rating": 4.5})

# Program ends... data is gone! 😢
```

### The Solution: File Storage

```python
# Save to file
save_places(places, "places.json")

# Later, load from file
places = load_places("places.json")
# All your data is back! 🎉
```

---

## Part 2: Introduction to JSON

### What is JSON?

**JSON** = **J**ava**S**cript **O**bject **N**otation

- A lightweight data interchange format
- Human-readable text
- Language-independent (works with Python, JavaScript, Java, etc.)
- The standard format for web APIs

### JSON Syntax

```json
{
    "name": "Taipei 101",
    "latitude": 25.0330,
    "longitude": 121.5654,
    "rating": 4.7,
    "is_open": true,
    "tags": ["landmark", "shopping", "observation"],
    "floors": 101,
    "address": null
}
```

### JSON Data Types

| JSON Type | Python Type | Example |
|-----------|-------------|---------|
| object | `dict` | `{"key": "value"}` |
| array | `list` | `[1, 2, 3]` |
| string | `str` | `"hello"` |
| number (int) | `int` | `42` |
| number (float) | `float` | `3.14` |
| true/false | `True/False` | `true` |
| null | `None` | `null` |

### JSON vs Python Syntax

```python
# Python dictionary
python_dict = {
    "name": "Taipei 101",
    "rating": 4.7,
    "is_open": True,      # Python: True (capital T)
    "address": None       # Python: None (capital N)
}

# Equivalent JSON
json_string = '''
{
    "name": "Taipei 101",
    "rating": 4.7,
    "is_open": true,      # JSON: true (lowercase)
    "address": null       # JSON: null (lowercase)
}
'''
```

### ⚠️ JSON Limitations

```python
# JSON does NOT support:
# 1. Tuples (converted to lists)
# 2. Sets (not supported)
# 3. Comments (not allowed in JSON)
# 4. Single quotes (must use double quotes)
# 5. Trailing commas

# Python tuple
coords = (25.0330, 121.5654)

# In JSON, becomes an array (list)
# [25.0330, 121.5654]
```

---

## Part 3: The `json` Module

### Importing the Module

```python
import json
```

### Key Functions

| Function | Purpose | Input → Output |
|----------|---------|----------------|
| `json.dumps()` | Convert to JSON string | Python → String |
| `json.loads()` | Parse JSON string | String → Python |
| `json.dump()` | Write to file | Python → File |
| `json.load()` | Read from file | File → Python |

Memory trick: `s` = string (dumps/loads), no `s` = file (dump/load)

---

## Part 4: Converting Between Python and JSON

### Python to JSON String: `json.dumps()`

```python
import json

place = {
    "name": "Taipei 101",
    "coords": [25.0330, 121.5654],  # Note: list, not tuple
    "rating": 4.7,
    "is_open": True
}

# Convert to JSON string
json_string = json.dumps(place)
print(json_string)
# {"name": "Taipei 101", "coords": [25.033, 121.5654], "rating": 4.7, "is_open": true}
```

### Pretty Printing JSON

```python
# With indentation (human-readable)
json_string = json.dumps(place, indent=2)
print(json_string)
# {
#   "name": "Taipei 101",
#   "coords": [25.033, 121.5654],
#   "rating": 4.7,
#   "is_open": true
# }

# With sorting keys
json_string = json.dumps(place, indent=2, sort_keys=True)
```

### Handling Non-ASCII Characters

```python
place = {"name": "鼎泰豐", "city": "台北"}

# Default: escapes non-ASCII
print(json.dumps(place))
# {"name": "\u9f0e\u6cf0\u8c50", "city": "\u53f0\u5317"}

# Keep Chinese characters readable
print(json.dumps(place, ensure_ascii=False))
# {"name": "鼎泰豐", "city": "台北"}
```

### JSON String to Python: `json.loads()`

```python
import json

json_string = '{"name": "Taipei 101", "rating": 4.7, "is_open": true}'

# Parse JSON string to Python dict
place = json.loads(json_string)

print(place)           # {'name': 'Taipei 101', 'rating': 4.7, 'is_open': True}
print(type(place))     # <class 'dict'>
print(place["name"])   # Taipei 101
print(place["is_open"])  # True (Python boolean)
```

---

## Part 5: Reading and Writing Files

### Basic File Operations

```python
# Writing to a file
with open("hello.txt", "w") as f:
    f.write("Hello, World!")

# Reading from a file
with open("hello.txt", "r") as f:
    content = f.read()
    print(content)  # Hello, World!
```

### The `with` Statement

The `with` statement automatically closes the file when done:

```python
# With 'with' (recommended)
with open("file.txt", "r") as f:
    content = f.read()
# File is automatically closed here

# Without 'with' (not recommended)
f = open("file.txt", "r")
content = f.read()
f.close()  # Easy to forget!
```

### File Modes

| Mode | Description |
|------|-------------|
| `"r"` | Read (default) - file must exist |
| `"w"` | Write - creates new or overwrites existing |
| `"a"` | Append - adds to end of file |
| `"r+"` | Read and write |
| `"x"` | Create - fails if file exists |

### Specifying Encoding

Always specify encoding for text files:

```python
# Recommended: always use UTF-8
with open("places.json", "r", encoding="utf-8") as f:
    content = f.read()

with open("places.json", "w", encoding="utf-8") as f:
    f.write(content)
```

---

## Part 6: JSON File Operations

### Writing JSON to File: `json.dump()`

```python
import json

places = [
    {"name": "Taipei 101", "coords": [25.0330, 121.5654], "rating": 4.7},
    {"name": "Din Tai Fung", "coords": [25.0339, 121.5645], "rating": 4.9},
    {"name": "Shilin Market", "coords": [25.0878, 121.5241], "rating": 4.5},
]

# Write to file
with open("places.json", "w", encoding="utf-8") as f:
    json.dump(places, f, indent=2, ensure_ascii=False)

print("Saved to places.json")
```

### Reading JSON from File: `json.load()`

```python
import json

# Read from file
with open("places.json", "r", encoding="utf-8") as f:
    places = json.load(f)

print(f"Loaded {len(places)} places")
for place in places:
    print(f"  - {place['name']}: {place['rating']}★")
```

### Complete Save/Load Functions

```python
import json

def save_places(places, filename):
    """Save places to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(places, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(places)} places to {filename}")


def load_places(filename):
    """Load places from a JSON file."""
    with open(filename, "r", encoding="utf-8") as f:
        places = json.load(f)
    print(f"Loaded {len(places)} places from {filename}")
    return places


# Usage
places = [
    {"name": "Taipei 101", "rating": 4.7},
    {"name": "Din Tai Fung", "rating": 4.9},
]

save_places(places, "my_places.json")
loaded_places = load_places("my_places.json")
```

---

## Part 7: Error Handling

### Common File Errors

```python
# FileNotFoundError - file doesn't exist
with open("nonexistent.json", "r") as f:
    data = json.load(f)

# PermissionError - no permission to access
with open("/etc/passwd", "w") as f:
    f.write("test")

# json.JSONDecodeError - invalid JSON
json.loads("not valid json")
```

### Handling Errors with try/except

```python
import json

def load_places_safe(filename):
    """Safely load places from a JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        print(f"File {filename} not found. Returning empty list.")
        return []

    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {filename}: {e}")
        return []

    except PermissionError:
        print(f"Permission denied: {filename}")
        return []


# Usage
places = load_places_safe("places.json")
places = load_places_safe("nonexistent.json")  # Returns []
```

### Checking if File Exists

```python
import os

filename = "places.json"

if os.path.exists(filename):
    print(f"{filename} exists")
else:
    print(f"{filename} does not exist")

# Better: use pathlib
from pathlib import Path

if Path(filename).exists():
    print(f"{filename} exists")
```

---

## Part 8: Building a Place Database

### Complete Database Module

```python
import json
import os

class PlaceDatabase:
    """A simple JSON-based place database."""

    def __init__(self, filename="places.json"):
        self.filename = filename
        self.places = self._load()

    def _load(self):
        """Load places from file."""
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save(self):
        """Save places to file."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.places, f, indent=2, ensure_ascii=False)

    def add(self, place):
        """Add a new place."""
        self.places.append(place)
        self._save()

    def find(self, name):
        """Find a place by name."""
        for place in self.places:
            if place["name"] == name:
                return place
        return None

    def delete(self, name):
        """Delete a place by name."""
        self.places = [p for p in self.places if p["name"] != name]
        self._save()

    def all(self):
        """Get all places."""
        return self.places

    def count(self):
        """Get the number of places."""
        return len(self.places)


# Usage
db = PlaceDatabase("my_places.json")

# Add places
db.add({"name": "Taipei 101", "coords": [25.0330, 121.5654], "rating": 4.7})
db.add({"name": "Din Tai Fung", "coords": [25.0339, 121.5645], "rating": 4.9})

# Find a place
place = db.find("Taipei 101")
print(place)

# List all
print(f"Total places: {db.count()}")
for p in db.all():
    print(f"  - {p['name']}")
```

---

## Part 9: Working with Complex JSON

### Nested JSON Structures

```python
# Complex place data structure
place_data = {
    "meta": {
        "version": "1.0",
        "last_updated": "2024-01-15",
        "total_places": 3
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
                "categories": ["landmark", "shopping"]
            }
        }
    ]
}

# Access nested data
places = place_data["places"]
first_place = places[0]
coords = first_place["location"]["coords"]
rating = first_place["details"]["rating"]
```

### Loading and Processing API-like JSON

```python
# Simulated API response (like what we'll get from Nominatim)
api_response = '''
[
    {
        "place_id": 123456,
        "display_name": "Taipei 101, Xinyi District, Taipei, Taiwan",
        "lat": "25.0329694",
        "lon": "121.5654268",
        "type": "attraction",
        "importance": 0.8
    },
    {
        "place_id": 789012,
        "display_name": "Taipei 101 Mall, Xinyi District, Taipei, Taiwan",
        "lat": "25.0330",
        "lon": "121.5654",
        "type": "mall",
        "importance": 0.6
    }
]
'''

# Parse and process
results = json.loads(api_response)

for result in results:
    name = result["display_name"].split(",")[0]  # Get first part of name
    lat = float(result["lat"])  # Convert string to float
    lon = float(result["lon"])
    print(f"{name}: ({lat}, {lon})")
```

---

## Part 10: Best Practices

### 1. Always Use UTF-8 Encoding

```python
# Good
with open("file.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Bad (may fail with non-ASCII characters)
with open("file.json", "r") as f:
    data = json.load(f)
```

### 2. Use Pretty Printing for Human-Readable Files

```python
# For debugging/manual editing
json.dump(data, f, indent=2, ensure_ascii=False)

# For production/API (compact)
json.dump(data, f, separators=(",", ":"))
```

### 3. Handle Tuples Carefully

```python
# Tuples become lists in JSON
original = {"coords": (25.0330, 121.5654)}
json_str = json.dumps(original)
loaded = json.loads(json_str)

print(type(original["coords"]))  # <class 'tuple'>
print(type(loaded["coords"]))    # <class 'list'>

# Convert back if needed
loaded["coords"] = tuple(loaded["coords"])
```

### 4. Validate Before Saving

```python
def save_place(place, filename):
    """Save a place with validation."""
    required_keys = ["name", "coords", "rating"]

    for key in required_keys:
        if key not in place:
            raise ValueError(f"Missing required key: {key}")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(place, f, indent=2)
```

---

## Summary

| Concept | Function | Example |
|---------|----------|---------|
| Python → JSON string | `json.dumps()` | `json.dumps({"a": 1})` |
| JSON string → Python | `json.loads()` | `json.loads('{"a": 1}')` |
| Python → JSON file | `json.dump()` | `json.dump(data, file)` |
| JSON file → Python | `json.load()` | `json.load(file)` |
| Open file | `open()` | `open("f.json", "r")` |
| Context manager | `with` | `with open(...) as f:` |

---

## What's Next?

In Week 4, we'll use our JSON skills to:
- Make HTTP requests to APIs
- Parse JSON responses from Nominatim
- Build a geocoding tool that saves results to files
