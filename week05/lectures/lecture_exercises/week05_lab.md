# Week 5 Lab: The Nominatim API (Geocoding)

## Lab Overview

In this lab, you'll practice parsing complex JSON responses, implementing robust error handling, and building a complete geocoding CLI tool.

**Time:** 90 minutes

### Prerequisites
- Completed Week 5 lecture
- Week 4 lab completed (HTTP requests basics)
- Python environment with `requests` installed

### Learning Objectives
1. Parse complex nested JSON from real APIs
2. Implement comprehensive error handling
3. Build reusable geocoding functions
4. Create a command-line interface
5. Handle edge cases gracefully

---

## Setup

Create your working file:

```bash
cd week05/labs
touch week05_starter.py
```

---

## Exercise 1: Safe Dictionary Access (15 minutes)

### Task
Implement a `safe_get` function that safely extracts nested values from dictionaries.

### Requirements
1. Accept a dictionary and a series of keys
2. Return the value at the nested path, or a default if not found
3. Handle missing keys, None values, and wrong types

### Starter Code

```python
def safe_get(data: dict, *keys, default=None):
    """
    Safely get a nested value from a dictionary.

    Args:
        data: The dictionary to search
        *keys: The keys to traverse
        default: Value to return if path doesn't exist

    Returns:
        The value at the path, or default if not found

    Examples:
        >>> d = {"a": {"b": {"c": 1}}}
        >>> safe_get(d, "a", "b", "c")
        1
        >>> safe_get(d, "a", "x", "c", default="N/A")
        'N/A'
    """
    # TODO: Implement this function
    pass


# Test cases
def test_safe_get():
    data = {
        "address": {
            "city": "Taipei",
            "district": "Xinyi",
            "details": {
                "postcode": "110"
            }
        },
        "name": "Taipei 101"
    }

    # Test 1: Simple access
    assert safe_get(data, "name") == "Taipei 101", "Test 1 failed"

    # Test 2: Nested access
    assert safe_get(data, "address", "city") == "Taipei", "Test 2 failed"

    # Test 3: Deep nested access
    assert safe_get(data, "address", "details", "postcode") == "110", "Test 3 failed"

    # Test 4: Missing key with default
    assert safe_get(data, "address", "country", default="Unknown") == "Unknown", "Test 4 failed"

    # Test 5: Missing intermediate key
    assert safe_get(data, "location", "lat", default=0.0) == 0.0, "Test 5 failed"

    # Test 6: None value
    data_with_none = {"a": {"b": None}}
    assert safe_get(data_with_none, "a", "b", "c", default="default") == "default", "Test 6 failed"

    print("All safe_get tests passed!")


if __name__ == "__main__":
    test_safe_get()
```

### Expected Output
```
All safe_get tests passed!
```

---

## Exercise 2: Parse Nominatim Response (15 minutes)

### Task
Create a function that parses a Nominatim search result into a clean, consistent format.

### Requirements
1. Extract name, coordinates, display_name, and type
2. Convert lat/lon strings to floats
3. Handle missing fields with sensible defaults
4. Return a well-structured dictionary

### Starter Code

```python
def parse_place(result: dict) -> dict:
    """
    Parse a single Nominatim result into a clean structure.

    Args:
        result: Raw result from Nominatim API

    Returns:
        Dictionary with:
        - name: str (the place name)
        - lat: float (latitude)
        - lon: float (longitude)
        - display_name: str (full address)
        - place_type: str (in format "class:type")
        - importance: float (relevance score)

    Example:
        >>> result = {"lat": "25.03", "lon": "121.56", "name": "Taipei 101", ...}
        >>> parse_place(result)
        {'name': 'Taipei 101', 'lat': 25.03, 'lon': 121.56, ...}
    """
    # TODO: Implement this function
    pass


# Test cases
def test_parse_place():
    # Complete result
    result1 = {
        "place_id": 12345,
        "lat": "25.0339639",
        "lon": "121.5644722",
        "name": "台北101",
        "display_name": "台北101, Xinyi Road, Taipei, Taiwan",
        "class": "tourism",
        "type": "attraction",
        "importance": 0.75
    }

    parsed1 = parse_place(result1)
    assert parsed1["name"] == "台北101", "Name extraction failed"
    assert abs(parsed1["lat"] - 25.0339639) < 0.0001, "Lat conversion failed"
    assert abs(parsed1["lon"] - 121.5644722) < 0.0001, "Lon conversion failed"
    assert parsed1["place_type"] == "tourism:attraction", "Type extraction failed"

    # Minimal result (missing some fields)
    result2 = {
        "lat": "25.0",
        "lon": "121.5",
        "display_name": "Some Place, Taiwan"
    }

    parsed2 = parse_place(result2)
    assert parsed2["lat"] == 25.0, "Lat conversion failed"
    assert parsed2["name"] != "", "Name should have fallback"
    assert parsed2["importance"] == 0.0, "Importance should default to 0"

    print("All parse_place tests passed!")


if __name__ == "__main__":
    test_parse_place()
```

---

## Exercise 3: Format Address (15 minutes)

### Task
Create a function that formats an address from a Nominatim result with `addressdetails`.

### Requirements
1. Handle various address structures (urban, rural, international)
2. Skip empty or missing parts
3. Return a clean, comma-separated string
4. Handle completely missing address gracefully

### Starter Code

```python
def format_address(result: dict) -> str:
    """
    Format an address from a Nominatim result.

    Args:
        result: Nominatim result with 'address' field

    Returns:
        Formatted address string

    Examples:
        "7 Section 5 Xinyi Road, Xinyi District, Taipei, Taiwan"
        "Shibuya, Tokyo, Japan"
        "Unknown location" (if no address data)
    """
    # TODO: Implement this function
    pass


# Test cases
def test_format_address():
    # Full Taiwan address
    result1 = {
        "address": {
            "house_number": "7",
            "road": "Section 5 Xinyi Road",
            "suburb": "Xinyi District",
            "city": "Taipei",
            "country": "Taiwan"
        }
    }
    addr1 = format_address(result1)
    assert "Xinyi" in addr1, "Should contain district"
    assert "Taipei" in addr1, "Should contain city"
    assert "Taiwan" in addr1, "Should contain country"

    # Japanese address (no street number)
    result2 = {
        "address": {
            "suburb": "Shibuya",
            "city": "Tokyo",
            "country": "Japan"
        }
    }
    addr2 = format_address(result2)
    assert "Shibuya" in addr2, "Should contain suburb"
    assert "Tokyo" in addr2, "Should contain city"

    # Minimal address
    result3 = {
        "address": {
            "country": "Taiwan"
        }
    }
    addr3 = format_address(result3)
    assert addr3 == "Taiwan" or "Taiwan" in addr3, "Should return country"

    # Empty address
    result4 = {"address": {}}
    addr4 = format_address(result4)
    assert addr4 != "", "Should return something for empty address"

    # No address field
    result5 = {}
    addr5 = format_address(result5)
    assert addr5 != "", "Should handle missing address field"

    print("All format_address tests passed!")


if __name__ == "__main__":
    test_format_address()
```

---

## Exercise 4: Error Handling (20 minutes)

### Task
Create a robust geocoding function with comprehensive error handling.

### Requirements
1. Handle network errors (timeout, connection)
2. Handle HTTP errors (403, 404, 429, 500)
3. Handle parsing errors (invalid JSON, missing fields)
4. Handle empty results
5. Raise appropriate custom exceptions

### Starter Code

```python
import requests

# Custom exceptions
class GeocodingError(Exception):
    """Base exception for geocoding errors."""
    pass

class NetworkError(GeocodingError):
    """Network-related errors."""
    pass

class NotFoundError(GeocodingError):
    """Place not found."""
    pass

class RateLimitError(GeocodingError):
    """Rate limit exceeded."""
    pass


def geocode(query: str) -> dict:
    """
    Geocode a place name with comprehensive error handling.

    Args:
        query: Place name to search

    Returns:
        Dictionary with name, lat, lon, display_name

    Raises:
        NotFoundError: If no results found
        RateLimitError: If rate limit exceeded (429)
        NetworkError: For other network/HTTP errors
        GeocodingError: For parsing errors
    """
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "CS101-Lab/1.0 (student@example.com)"}
    params = {"q": query, "format": "json", "limit": 1}

    # TODO: Implement with full error handling
    pass


# Test error handling
def test_geocode_errors():
    import time

    print("Testing error handling...")

    # Test 1: Successful geocoding
    print("\n1. Testing successful geocoding...")
    try:
        result = geocode("Taipei 101")
        print(f"   Success: Found {result['name']}")
    except GeocodingError as e:
        print(f"   Failed: {e}")

    time.sleep(1)  # Rate limit

    # Test 2: Not found
    print("\n2. Testing not found (gibberish query)...")
    try:
        result = geocode("xyzzy12345notaplace")
        print(f"   Unexpected success: {result}")
    except NotFoundError as e:
        print(f"   Correct: NotFoundError raised - {e}")
    except GeocodingError as e:
        print(f"   Wrong exception type: {type(e).__name__}")

    time.sleep(1)

    # Test 3: Empty query
    print("\n3. Testing empty query...")
    try:
        result = geocode("")
        print(f"   Result: {result}")
    except (NotFoundError, GeocodingError) as e:
        print(f"   Handled: {type(e).__name__} - {e}")

    print("\nError handling tests complete!")


if __name__ == "__main__":
    test_geocode_errors()
```

---

## Exercise 5: Build a Geocoding Function Library (20 minutes)

### Task
Create a complete geocoding module with forward and reverse geocoding.

### Requirements
1. Forward geocoding: place name → coordinates
2. Reverse geocoding: coordinates → address
3. Rate limiting between requests
4. Consistent return format
5. Good error handling

### Starter Code

```python
import requests
import time

class Geocoder:
    """A complete geocoding client with forward and reverse geocoding."""

    BASE_URL = "https://nominatim.openstreetmap.org"

    def __init__(self, user_agent: str):
        """
        Initialize the geocoder.

        Args:
            user_agent: User-Agent string for API requests
        """
        self.headers = {"User-Agent": user_agent}
        self.last_request = 0

    def _rate_limit(self):
        """Ensure at least 1 second between requests."""
        # TODO: Implement rate limiting
        pass

    def forward(self, query: str) -> dict | None:
        """
        Convert a place name to coordinates.

        Args:
            query: Place name to search

        Returns:
            Dict with name, lat, lon, display_name or None if not found
        """
        # TODO: Implement forward geocoding
        pass

    def reverse(self, lat: float, lon: float) -> dict | None:
        """
        Convert coordinates to an address.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Dict with display_name, address components or None if not found
        """
        # TODO: Implement reverse geocoding
        pass

    def batch_forward(self, queries: list[str]) -> list[dict]:
        """
        Geocode multiple places.

        Args:
            queries: List of place names

        Returns:
            List of results (only successful geocodes)
        """
        # TODO: Implement batch geocoding with rate limiting
        pass


# Test the Geocoder class
def test_geocoder():
    print("Testing Geocoder class...\n")

    geocoder = Geocoder("CS101-Lab/1.0 (student@example.com)")

    # Test forward geocoding
    print("1. Forward geocoding 'Taipei Main Station'...")
    result = geocoder.forward("Taipei Main Station")
    if result:
        print(f"   Found: {result['name']}")
        print(f"   Coordinates: ({result['lat']:.4f}, {result['lon']:.4f})")
    else:
        print("   Not found")

    # Test reverse geocoding
    print("\n2. Reverse geocoding (25.0478, 121.5170)...")
    result = geocoder.reverse(25.0478, 121.5170)
    if result:
        print(f"   Address: {result['display_name'][:60]}...")
    else:
        print("   Not found")

    # Test batch geocoding
    print("\n3. Batch geocoding...")
    places = ["Taipei 101", "National Palace Museum", "Jiufen"]
    results = geocoder.batch_forward(places)
    print(f"   Found {len(results)}/{len(places)} places")
    for r in results:
        print(f"   - {r['name'][:40]}...")

    print("\nGeocoder tests complete!")


if __name__ == "__main__":
    test_geocoder()
```

---

## Exercise 6: Interactive CLI Geocoder (20 minutes)

### Task
Build a complete interactive command-line geocoder.

### Requirements
1. Interactive prompt for queries
2. Support forward geocoding (default)
3. Support reverse geocoding with `reverse` command
4. Display results nicely formatted
5. Handle all errors gracefully
6. Support `quit` command to exit

### Starter Code

```python
import requests
import time
import sys


def geocode(query: str) -> dict | None:
    """Forward geocode a place name."""
    # Use your implementation from Exercise 4/5
    pass


def reverse_geocode(lat: float, lon: float) -> dict | None:
    """Reverse geocode coordinates."""
    # Use your implementation from Exercise 5
    pass


def print_forward_result(result: dict):
    """Pretty print a forward geocoding result."""
    print()
    print(f"  Name: {result.get('name', 'N/A')}")
    print(f"  Coordinates: ({result['lat']:.6f}, {result['lon']:.6f})")
    print(f"  Address: {result.get('display_name', 'N/A')}")
    print()


def print_reverse_result(result: dict):
    """Pretty print a reverse geocoding result."""
    print()
    print(f"  Address: {result['display_name']}")
    if 'address' in result:
        print("  Components:")
        for key, value in result['address'].items():
            print(f"    {key}: {value}")
    print()


def run_cli():
    """Run the interactive CLI."""
    print("\n=== Geocoder CLI ===")
    print("Commands:")
    print("  <place name>          - Search for a place")
    print("  reverse <lat> <lon>   - Reverse geocode coordinates")
    print("  help                  - Show this help")
    print("  quit                  - Exit")
    print()

    last_request = 0

    while True:
        # TODO: Implement the CLI loop
        # 1. Read user input
        # 2. Parse commands (reverse, help, quit, or search)
        # 3. Apply rate limiting
        # 4. Execute appropriate function
        # 5. Handle and display errors nicely
        pass


if __name__ == "__main__":
    # Support command-line arguments too
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        result = geocode(query)
        if result:
            print_forward_result(result)
        else:
            print("Not found")
    else:
        run_cli()
```

### Expected Behavior
```
=== Geocoder CLI ===
Commands:
  <place name>          - Search for a place
  reverse <lat> <lon>   - Reverse geocode coordinates
  help                  - Show this help
  quit                  - Exit

geocoder> Taipei 101

  Name: 台北101
  Coordinates: (25.033964, 121.564472)
  Address: 台北101, 7, Section 5, Xinyi Road, Xinyi District, Taipei, 110, Taiwan

geocoder> reverse 25.0478 121.5170

  Address: Taipei Main Station, Zhongzheng District, Taipei, Taiwan
  Components:
    railway: Taipei Main Station
    suburb: Zhongzheng District
    city: Taipei
    country: Taiwan

geocoder> notarealplace
  Error: No results found for 'notarealplace'

geocoder> quit
Goodbye!
```

---

## Bonus Challenge: Geocoding with Caching

### Task
Add file-based caching to your geocoder to avoid repeated API calls.

### Requirements
1. Cache results to a JSON file
2. Check cache before making API calls
3. Cache key should be case-insensitive query
4. Include a `--no-cache` flag to bypass cache

### Hints
```python
import json
from pathlib import Path

class CachedGeocoder:
    def __init__(self, user_agent: str, cache_file: str = ".geocache.json"):
        self.cache_file = Path(cache_file)
        self.cache = self._load_cache()

    def _load_cache(self) -> dict:
        if self.cache_file.exists():
            return json.loads(self.cache_file.read_text())
        return {}

    def _save_cache(self):
        self.cache_file.write_text(json.dumps(self.cache, indent=2))

    def forward(self, query: str, use_cache: bool = True) -> dict | None:
        cache_key = query.lower().strip()

        if use_cache and cache_key in self.cache:
            print("(from cache)")
            return self.cache[cache_key]

        # Make API call...
        result = self._api_call(query)

        if result and use_cache:
            self.cache[cache_key] = result
            self._save_cache()

        return result
```

---

## Submission Checklist

Before submitting, verify:

- [ ] All test cases pass
- [ ] Error handling covers all edge cases
- [ ] Rate limiting is implemented (1 request/second)
- [ ] CLI handles invalid input gracefully
- [ ] Code is well-documented

## Grading Rubric

| Exercise | Points | Criteria |
|----------|--------|----------|
| Exercise 1 | 15 | safe_get handles all cases |
| Exercise 2 | 15 | parse_place extracts all fields correctly |
| Exercise 3 | 15 | format_address handles all variations |
| Exercise 4 | 20 | All error types handled correctly |
| Exercise 5 | 15 | Geocoder class fully functional |
| Exercise 6 | 20 | CLI works correctly |
| Bonus | +15 | Caching implemented correctly |

**Total: 100 points (+15 bonus)**

---

## Common Issues & Solutions

### Issue: KeyError when accessing nested data
**Solution:** Use `.get()` with defaults or the `safe_get` function:
```python
city = result.get("address", {}).get("city", "Unknown")
```

### Issue: TypeError: 'NoneType' object is not subscriptable
**Solution:** Check for None before accessing:
```python
address = result.get("address")
if address:
    city = address.get("city")
```

### Issue: ValueError when converting lat/lon
**Solution:** Use try/except:
```python
try:
    lat = float(result.get("lat", 0))
except (ValueError, TypeError):
    lat = 0.0
```

### Issue: Getting rate limited (429)
**Solution:** Add proper delays:
```python
time.sleep(1)  # Wait 1 second between requests
```

---

*End of Week 5 Lab*
