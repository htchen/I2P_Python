"""
Week 3 Lecture Examples: JSON & File I/O
Run this file to see all examples in action.
"""

import json
import os

print("=" * 60)
print("WEEK 3: JSON & File I/O")
print("=" * 60)

# ============================================================
# Part 1: JSON Basics
# ============================================================

print("\n--- Part 1: JSON Basics ---")

# Python dictionary
place = {
    "name": "Taipei 101",
    "coords": [25.0330, 121.5654],  # Note: list (tuples become lists)
    "rating": 4.7,
    "is_open": True,
    "tags": ["landmark", "shopping", "observation"]
}

# Convert to JSON string
json_string = json.dumps(place)
print(f"JSON string:\n{json_string}")

# Pretty print
json_pretty = json.dumps(place, indent=2)
print(f"\nPretty JSON:\n{json_pretty}")

# ============================================================
# Part 2: JSON Parsing
# ============================================================

print("\n--- Part 2: JSON Parsing ---")

json_input = '''
{
    "name": "Din Tai Fung",
    "rating": 4.9,
    "is_open": true,
    "categories": ["restaurant", "dumplings"]
}
'''

# Parse JSON string to Python
parsed = json.loads(json_input)
print(f"Parsed type: {type(parsed)}")
print(f"Name: {parsed['name']}")
print(f"Rating: {parsed['rating']}")
print(f"Is open: {parsed['is_open']} (type: {type(parsed['is_open'])})")

# ============================================================
# Part 3: Chinese Characters
# ============================================================

print("\n--- Part 3: Chinese Characters ---")

chinese_place = {
    "name": "鼎泰豐",
    "city": "台北"
}

# Default (escaped)
print(f"Escaped: {json.dumps(chinese_place)}")

# Keep readable
print(f"Readable: {json.dumps(chinese_place, ensure_ascii=False)}")

# ============================================================
# Part 4: File Operations
# ============================================================

print("\n--- Part 4: File Operations ---")

# Write text file
with open("example.txt", "w", encoding="utf-8") as f:
    f.write("Line 1: Hello\n")
    f.write("Line 2: World\n")
    f.write("Line 3: 你好世界\n")
print("Wrote example.txt")

# Read text file
with open("example.txt", "r", encoding="utf-8") as f:
    content = f.read()
print(f"Content:\n{content}")

# Read lines
with open("example.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
print(f"Lines: {[line.strip() for line in lines]}")

# ============================================================
# Part 5: JSON File I/O
# ============================================================

print("\n--- Part 5: JSON File I/O ---")

places = [
    {"name": "Taipei 101", "coords": [25.0330, 121.5654], "rating": 4.7},
    {"name": "Din Tai Fung", "coords": [25.0339, 121.5645], "rating": 4.9},
    {"name": "Shilin Market", "coords": [25.0878, 121.5241], "rating": 4.5},
]

# Save to JSON file
with open("places.json", "w", encoding="utf-8") as f:
    json.dump(places, f, indent=2, ensure_ascii=False)
print("Saved places.json")

# Load from JSON file
with open("places.json", "r", encoding="utf-8") as f:
    loaded_places = json.load(f)

print(f"Loaded {len(loaded_places)} places:")
for p in loaded_places:
    print(f"  - {p['name']}: {p['rating']}★")

# ============================================================
# Part 6: Error Handling
# ============================================================

print("\n--- Part 6: Error Handling ---")

def safe_load(filename):
    """Safely load JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"  File not found: {filename}")
        return []
    except json.JSONDecodeError as e:
        print(f"  Invalid JSON: {e}")
        return []

# Test with valid file
print("Loading places.json:")
data = safe_load("places.json")
print(f"  Loaded {len(data)} items")

# Test with missing file
print("Loading nonexistent.json:")
data = safe_load("nonexistent.json")
print(f"  Loaded {len(data)} items")

# Test with invalid JSON
with open("invalid.json", "w") as f:
    f.write("not valid json {{{")
print("Loading invalid.json:")
data = safe_load("invalid.json")
print(f"  Loaded {len(data)} items")

# ============================================================
# Part 7: Place Database
# ============================================================

print("\n--- Part 7: Place Database ---")

class PlaceDatabase:
    """A simple JSON-based place database."""

    def __init__(self, filename):
        self.filename = filename
        self.places = self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def _save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.places, f, indent=2, ensure_ascii=False)

    def add(self, place):
        self.places.append(place)
        self._save()

    def find(self, name):
        for p in self.places:
            if p.get("name") == name:
                return p
        return None

    def delete(self, name):
        self.places = [p for p in self.places if p.get("name") != name]
        self._save()

    def all(self):
        return self.places

    def count(self):
        return len(self.places)


# Demo
db = PlaceDatabase("demo_db.json")

# Add places
db.add({"name": "Taipei 101", "rating": 4.7})
db.add({"name": "Din Tai Fung", "rating": 4.9})
print(f"Added 2 places. Total: {db.count()}")

# Find
found = db.find("Taipei 101")
print(f"Found: {found}")

# List all
print("All places:")
for p in db.all():
    print(f"  - {p['name']}")

# Persistence test
db2 = PlaceDatabase("demo_db.json")
print(f"Reloaded from file: {db2.count()} places")

# ============================================================
# Part 8: Complex JSON (API-like)
# ============================================================

print("\n--- Part 8: Complex JSON (API-like) ---")

api_response = '''
{
    "status": "OK",
    "total": 2,
    "results": [
        {
            "place_id": 123,
            "display_name": "Taipei 101, Xinyi, Taipei, Taiwan",
            "lat": "25.0329694",
            "lon": "121.5654268"
        },
        {
            "place_id": 456,
            "display_name": "Din Tai Fung, Da'an, Taipei, Taiwan",
            "lat": "25.0339",
            "lon": "121.5645"
        }
    ]
}
'''

data = json.loads(api_response)

if data["status"] == "OK":
    print(f"Found {data['total']} results:")
    for result in data["results"]:
        name = result["display_name"].split(",")[0]
        lat = float(result["lat"])
        lon = float(result["lon"])
        print(f"  - {name}: ({lat:.4f}, {lon:.4f})")

# ============================================================
# Part 9: Tuple Handling
# ============================================================

print("\n--- Part 9: Tuple Handling ---")

# Python with tuple
original = {
    "name": "Test",
    "coords": (25.0330, 121.5654)  # tuple
}

# Save and reload
json_str = json.dumps(original)
reloaded = json.loads(json_str)

print(f"Original coords type: {type(original['coords'])}")
print(f"Reloaded coords type: {type(reloaded['coords'])}")

# Convert back to tuple if needed
reloaded["coords"] = tuple(reloaded["coords"])
print(f"After conversion: {type(reloaded['coords'])}")

# ============================================================
# Cleanup
# ============================================================

print("\n--- Cleanup ---")
for f in ["example.txt", "places.json", "invalid.json", "demo_db.json"]:
    if os.path.exists(f):
        os.remove(f)
        print(f"Removed: {f}")

print("\n" + "=" * 60)
print("End of Week 3 Examples")
print("=" * 60)
