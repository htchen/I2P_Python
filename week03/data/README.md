# Week 3 Sample Data Files

This folder contains sample JSON files for practicing JSON parsing and file I/O.

## Files

### `sample_places.json`
A simple list of places with basic information:
- name, coords, rating, category, tags, address

**Use case:** Basic JSON loading, filtering, and sorting practice.

```python
import json

with open("data/sample_places.json", "r", encoding="utf-8") as f:
    places = json.load(f)

for place in places:
    print(f"{place['name']}: {place['rating']}★")
```

### `sample_api_response.json`
Simulated API response similar to what Nominatim returns:
- Nested structure with metadata and results
- String lat/lon values (need to convert to float)
- Full display names that need parsing

**Use case:** Practice parsing real-world API responses.

```python
import json

with open("data/sample_api_response.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if data["status"] == "OK":
    for result in data["results"]:
        name = result["display_name"].split(",")[0]
        lat = float(result["lat"])
        lon = float(result["lon"])
        print(f"{name}: ({lat}, {lon})")
```

### `complex_places.json`
Complex nested structure with:
- Metadata section
- Statistics section
- Detailed place objects with nested location, details, hours, contact

**Use case:** Practice navigating deeply nested JSON structures.

```python
import json

with open("data/complex_places.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Access metadata
print(f"Version: {data['meta']['version']}")
print(f"Total places: {data['statistics']['total_places']}")

# Access nested place data
for place in data["places"]:
    name = place["name"]
    lat, lon = place["location"]["coords"]
    rating = place["details"]["rating"]
    print(f"{name} ({lat}, {lon}): {rating}★")
```

## Tips

1. Always use `encoding="utf-8"` when opening files
2. Use `json.dumps(data, indent=2)` to pretty-print JSON for debugging
3. Use `.get()` for safe access to optional fields
4. Remember that JSON doesn't support tuples (they become lists)
