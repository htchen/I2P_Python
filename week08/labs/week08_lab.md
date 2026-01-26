# Week 8 Lab: Building the Smart City Navigator

## Overview

In this lab, you will build a complete **Smart City Navigator** application that combines geocoding and routing to help users navigate between locations. This capstone project integrates all the concepts you've learned throughout the course.

**Time Required**: 2-3 hours

**Prerequisites**:
- Completed Week 5 (Nominatim API & Geocoding)
- Completed Week 7 (OSRM API & Routing)
- Understanding of classes, dataclasses, and error handling

---

## Learning Objectives

By the end of this lab, you will be able to:
1. Design and implement multi-component applications
2. Integrate multiple APIs into a cohesive system
3. Implement robust error handling
4. Create user-friendly command-line interfaces
5. Apply software design patterns

---

## Setup

### Required Files
- `week08_starter.py` - Contains starter code with TODO placeholders

### Required Libraries
```bash
pip install requests
```

### Testing Your Code
```bash
# Run all tests
python week08_starter.py --test

# Run in interactive mode
python week08_starter.py

# Run with command-line arguments
python week08_starter.py -s "Taipei 101" -e "Taipei Main Station"
```

---

## Exercise 1: Location Data Model (15 minutes)

Create a `Location` dataclass to represent geographic locations.

### Requirements

1. Create a dataclass with the following fields:
   - `name`: The location's name (string)
   - `latitude`: The latitude (float)
   - `longitude`: The longitude (float)
   - `display_name`: Full address from geocoder (string)

2. Add a `coords` property that returns a `(lat, lon)` tuple

3. Implement a `__str__` method for readable output

### Starter Code

```python
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Location:
    """Represents a geographic location."""
    # TODO: Define the fields

    @property
    def coords(self) -> Tuple[float, float]:
        """Return (lat, lon) tuple."""
        # TODO: Implement this property
        pass

    def __str__(self) -> str:
        # TODO: Return a readable string representation
        pass
```

### Expected Output

```python
loc = Location("Taipei 101", 25.0330, 121.5654, "Taipei 101, Xinyi, Taiwan")
print(loc)
# Output: Taipei 101 (25.0330, 121.5654)
print(loc.coords)
# Output: (25.0330, 121.5654)
```

### Hints
- Use `@dataclass` decorator from the `dataclasses` module
- The `@property` decorator creates a computed attribute
- Format floats with `:.4f` for 4 decimal places

---

## Exercise 2: Route Data Model (15 minutes)

Create a `Route` dataclass to represent route information.

### Requirements

1. Create a dataclass with the following fields:
   - `distance`: Total distance in meters (float)
   - `duration`: Total duration in seconds (float)
   - `geometry`: List of (lat, lon) coordinate tuples

2. Add computed properties:
   - `distance_km`: Distance in kilometers
   - `duration_min`: Duration in minutes

3. Add a `summary()` method that returns a human-readable string

### Starter Code

```python
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Route:
    """Represents a complete route between locations."""
    # TODO: Define the fields

    @property
    def distance_km(self) -> float:
        """Total distance in kilometers."""
        # TODO: Implement
        pass

    @property
    def duration_min(self) -> float:
        """Total duration in minutes."""
        # TODO: Implement
        pass

    def summary(self) -> str:
        """Return a human-readable summary."""
        # TODO: Implement
        pass
```

### Expected Output

```python
route = Route(distance=5200, duration=720, geometry=[(25.0, 121.5), (25.1, 121.6)])
print(route.distance_km)  # 5.2
print(route.duration_min)  # 12.0
print(route.summary())  # "5.2 km, ~12 minutes"
```

---

## Exercise 3: GeocodingService (30 minutes)

Implement a service class that converts addresses to coordinates using the Nominatim API.

### Requirements

1. Create a `GeocodingService` class with:
   - Constructor that accepts a `user_agent` parameter
   - Rate limiting (1 second between requests)
   - `geocode(address)` method that returns a `Location` or `None`
   - `reverse_geocode(lat, lon)` method that returns a `Location` or `None`

2. Handle errors gracefully:
   - Network timeouts
   - Connection errors
   - Invalid responses

### API Information

**Nominatim Search Endpoint**:
```
GET https://nominatim.openstreetmap.org/search
Parameters:
  - q: Address to search
  - format: "json"
  - limit: 1
Headers:
  - User-Agent: Your application name
```

**Nominatim Reverse Endpoint**:
```
GET https://nominatim.openstreetmap.org/reverse
Parameters:
  - lat: Latitude
  - lon: Longitude
  - format: "json"
```

### Starter Code

```python
class GeocodingService:
    """Service for converting addresses to coordinates."""

    def __init__(self, user_agent: str = "SmartNavigator/1.0"):
        # TODO: Initialize instance variables
        pass

    def _wait_for_rate_limit(self):
        """Ensure we don't exceed API rate limits."""
        # TODO: Implement rate limiting
        pass

    def geocode(self, address: str) -> Optional[Location]:
        """Convert an address to coordinates."""
        # TODO: Implement geocoding
        pass

    def reverse_geocode(self, lat: float, lon: float) -> Optional[Location]:
        """Convert coordinates to an address."""
        # TODO: Implement reverse geocoding
        pass
```

### Expected Behavior

```python
geocoder = GeocodingService()
loc = geocoder.geocode("Taipei 101")
print(loc)  # Taipei 101 (25.0330, 121.5654)

loc = geocoder.reverse_geocode(25.0330, 121.5654)
print(loc.display_name)  # Full address string
```

### Hints
- Use `time.time()` and `time.sleep()` for rate limiting
- Store the last request time as an instance variable
- Use `requests.get()` with `timeout=10`
- Catch `requests.exceptions.RequestException` for error handling

---

## Exercise 4: RoutingService (30 minutes)

Implement a service class that calculates routes using the OSRM API.

### Requirements

1. Create a `RoutingService` class with:
   - Constructor that accepts a `profile` parameter ("driving", "walking", "cycling")
   - `get_route(waypoints)` method that returns a `Route` or `None`
   - Support for multiple waypoints

2. Handle the coordinate order correctly:
   - OSRM uses **longitude,latitude** order (opposite of typical lat,lon!)

3. Parse the GeoJSON geometry from the response

### API Information

**OSRM Route Endpoint**:
```
GET https://router.project-osrm.org/route/v1/{profile}/{coordinates}

Where:
  - profile: "driving", "foot", or "cycling"
  - coordinates: "lon1,lat1;lon2,lat2;lon3,lat3"

Parameters:
  - overview: "full"
  - geometries: "geojson"
```

### Starter Code

```python
class RoutingService:
    """Service for calculating routes using OSRM."""

    PROFILES = ["driving", "walking", "cycling"]

    def __init__(self, profile: str = "driving"):
        # TODO: Validate profile and initialize
        pass

    def _format_coordinates(self, coords: List[Tuple[float, float]]) -> str:
        """Format coordinates for OSRM (lon,lat order!)."""
        # TODO: Implement coordinate formatting
        pass

    def _parse_geometry(self, geometry: dict) -> List[Tuple[float, float]]:
        """Parse GeoJSON geometry to (lat, lon) tuples."""
        # TODO: Implement geometry parsing
        pass

    def get_route(self, waypoints: List[Tuple[float, float]]) -> Optional[Route]:
        """Calculate a route through the waypoints."""
        # TODO: Implement routing
        pass
```

### Expected Behavior

```python
router = RoutingService(profile="driving")
route = router.get_route([
    (25.0330, 121.5654),  # Taipei 101
    (25.0478, 121.5170)   # Taipei Main Station
])
print(route.summary())  # "5.2 km, ~12 minutes"
```

### Hints
- Remember: OSRM wants `lon,lat` but we store `lat,lon`
- Use `profile = "foot"` when the user selects "walking"
- GeoJSON coordinates are also `[lon, lat]` order
- The route data is in `response["routes"][0]`

---

## Exercise 5: Navigator Class (30 minutes)

Create the main Navigator class that coordinates the geocoding and routing services.

### Requirements

1. Create a `Navigator` class that:
   - Uses `GeocodingService` and `RoutingService` internally
   - Accepts both addresses AND coordinates as input
   - Provides `navigate(start, end)` method
   - Provides `navigate_multi(locations)` for multi-stop routes

2. Parse location input intelligently:
   - Coordinates: "25.0330, 121.5654" or "(25.0330, 121.5654)"
   - Addresses: "Taipei 101, Taiwan"

3. Return a result dictionary with all relevant information

### Starter Code

```python
class Navigator:
    """Combines geocoding and routing for complete navigation."""

    def __init__(self, profile: str = "driving"):
        # TODO: Initialize services
        pass

    def _parse_location(self, location: str) -> Optional[Location]:
        """Parse a location string (coordinates or address)."""
        # TODO: Implement location parsing
        pass

    def navigate(self, start: str, end: str) -> Optional[dict]:
        """Get navigation from start to end."""
        # TODO: Implement navigation
        pass

    def navigate_multi(self, locations: List[str]) -> Optional[dict]:
        """Navigate through multiple waypoints."""
        # TODO: Implement multi-stop navigation
        pass
```

### Expected Behavior

```python
nav = Navigator(profile="driving")

# With addresses
result = nav.navigate("Taipei 101", "Taipei Main Station")
print(result["route"].summary())  # "5.2 km, ~12 minutes"

# With coordinates
result = nav.navigate("25.0330, 121.5654", "National Palace Museum")
print(result["start"].name)  # Coordinates or reverse-geocoded name

# Multi-stop
result = nav.navigate_multi(["Stop A", "Stop B", "Stop C"])
print(len(result["waypoints"]))  # 3
```

### Hints
- Use regex to detect coordinate patterns: `r'^\(?\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*\)?$'`
- Validate coordinates are in valid ranges: lat (-90 to 90), lon (-180 to 180)
- Print progress messages so users know what's happening

---

## Exercise 6: Command-Line Interface (30 minutes)

Create a user-friendly CLI for your navigator.

### Requirements

1. Support command-line arguments:
   - `-s, --start`: Starting location
   - `-e, --end`: Destination
   - `-p, --profile`: Travel mode (driving/walking/cycling)
   - `--multi`: Multiple stops
   - `-i, --interactive`: Interactive mode

2. Implement interactive mode with a menu:
   - Navigate between two locations
   - Multi-stop route
   - Change travel mode
   - Exit

3. Format output nicely with:
   - Clear headers and separators
   - Human-readable distances and durations

### Starter Code

```python
import argparse

def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    # TODO: Create and configure parser
    pass

def interactive_mode(navigator: Navigator):
    """Run the navigator in interactive mode."""
    # TODO: Implement interactive loop
    pass

def main():
    """Main entry point."""
    # TODO: Parse arguments and run appropriate mode
    pass

if __name__ == "__main__":
    main()
```

### Expected Usage

```bash
# Direct navigation
python week08_starter.py -s "Taipei 101" -e "Taipei Main Station" -p driving

# Multi-stop
python week08_starter.py --multi "Stop A" "Stop B" "Stop C"

# Interactive mode
python week08_starter.py -i
```

### Hints
- Use `argparse.ArgumentParser()` for argument parsing
- Use `add_mutually_exclusive_group()` for conflicting options
- Handle `KeyboardInterrupt` for graceful exit
- Use f-strings for formatted output

---

## Bonus Challenge: Caching and Performance (Optional)

Add caching to reduce API calls and improve performance.

### Requirements

1. Create a `SimpleCache` class that:
   - Stores results in JSON files
   - Has a configurable TTL (time-to-live)
   - Uses a hash of the input as the cache key

2. Create a `CachedGeocodingService` that:
   - Extends `GeocodingService`
   - Checks cache before making API calls
   - Stores results in cache after API calls

### Starter Code

```python
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

class SimpleCache:
    """File-based cache with TTL."""

    def __init__(self, cache_dir: str = ".cache", ttl_hours: int = 24):
        # TODO: Initialize cache directory and TTL
        pass

    def _get_key(self, *args) -> str:
        """Generate cache key from arguments."""
        # TODO: Create hash of arguments
        pass

    def get(self, *args) -> Optional[Any]:
        """Get cached value if exists and not expired."""
        # TODO: Implement cache retrieval
        pass

    def set(self, value: Any, *args):
        """Store value in cache."""
        # TODO: Implement cache storage
        pass

class CachedGeocodingService(GeocodingService):
    """Geocoding with caching."""

    def geocode(self, address: str) -> Optional[Location]:
        # TODO: Check cache, call API if miss, store result
        pass
```

### Expected Behavior

```python
cache = SimpleCache(ttl_hours=24)
cache.set({"data": "value"}, "key1", "key2")

result = cache.get("key1", "key2")  # Returns {"data": "value"}
result = cache.get("different")     # Returns None
```

---

## Submission Checklist

Before submitting, ensure:

- [ ] All exercises are completed
- [ ] Code passes syntax check (`python -m py_compile week08_starter.py`)
- [ ] Tests pass (`python week08_starter.py --test`)
- [ ] Code handles errors gracefully (no crashes on bad input)
- [ ] Output is formatted and readable
- [ ] Code includes docstrings and comments

---

## Grading Rubric

| Component | Points |
|-----------|--------|
| Exercise 1: Location dataclass | 10 |
| Exercise 2: Route dataclass | 10 |
| Exercise 3: GeocodingService | 20 |
| Exercise 4: RoutingService | 20 |
| Exercise 5: Navigator class | 25 |
| Exercise 6: CLI interface | 15 |
| **Bonus: Caching** | +10 |
| **Total** | 100 (+10) |

---

## Common Issues and Solutions

### Issue: "Connection refused" errors
**Solution**: Check your internet connection. The APIs require network access.

### Issue: "Too many requests" from Nominatim
**Solution**: Ensure your rate limiting is working (1 second between requests).

### Issue: Routes returning None
**Solution**: Check that you're using `lon,lat` order for OSRM, not `lat,lon`.

### Issue: Coordinates not parsing
**Solution**: Check your regex pattern handles optional parentheses and spaces.

---

## Additional Resources

- [OSRM API Documentation](http://project-osrm.org/docs/v5.24.0/api/)
- [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/)
- [Python argparse Tutorial](https://docs.python.org/3/library/argparse.html)
- [Python dataclasses](https://docs.python.org/3/library/dataclasses.html)
