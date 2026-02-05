# Week 8 Lab: The OSRM API (Real Routing)

## Lab Overview

In this lab, you'll practice working with the OSRM API to calculate real driving distances, build distance matrices, and compare straight-line vs actual travel distances.

**Time:** 90 minutes

### Prerequisites
- Completed Week 8 lecture
- Understanding of HTTP requests and JSON
- Familiarity with 2D lists (matrices)

### Learning Objectives
1. Make requests to the OSRM routing API
2. Build and manipulate 2D distance matrices
3. Compare Haversine vs driving distances
4. Parse and work with route geometry
5. Create a complete route analysis tool

---

## Setup

Create your working file:

```bash
cd week08/labs
cp week08_starter.py my_solution.py
```

Install required packages (if not already installed):

```bash
pip install requests
```

---

## Exercise 1: Haversine Distance Function (15 minutes)

### Task
Implement the Haversine formula to calculate straight-line distance between two points on Earth.

### Requirements
1. Accept latitude and longitude in degrees
2. Return distance in kilometers
3. Handle edge cases (same point = 0 distance)

### Starter Code

```python
import math

def haversine_distance(lat1: float, lon1: float,
                       lat2: float, lon2: float) -> float:
    """
    Calculate the straight-line distance between two points on Earth.

    The Haversine formula accounts for the Earth's curvature to calculate
    the shortest distance over the Earth's surface.

    Args:
        lat1: Latitude of first point in degrees
        lon1: Longitude of first point in degrees
        lat2: Latitude of second point in degrees
        lon2: Longitude of second point in degrees

    Returns:
        Distance in kilometers

    Examples:
        >>> haversine_distance(25.0330, 121.5654, 25.0478, 121.5170)
        5.21  # Approximately
        >>> haversine_distance(0, 0, 0, 0)
        0.0
    """
    # Earth's radius in kilometers
    R = 6371.0

    # TODO: Implement the Haversine formula
    # 1. Convert all coordinates from degrees to radians
    # 2. Calculate the differences in latitude and longitude
    # 3. Apply the Haversine formula:
    #    a = sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)
    #    c = 2 * arcsin(√a)
    #    distance = R * c

    pass


# Test cases
def test_haversine():
    # Test 1: Same point should be 0
    assert haversine_distance(25.0, 121.0, 25.0, 121.0) == 0.0, "Same point failed"
    print("  Test 1 (same point): PASS")

    # Test 2: Taipei 101 to Main Station (approximately 5.2 km)
    dist = haversine_distance(25.0330, 121.5654, 25.0478, 121.5170)
    assert 5.0 < dist < 5.5, f"Taipei test failed: {dist}"
    print(f"  Test 2 (Taipei 101 → Main Station): {dist:.2f} km - PASS")

    # Test 3: Known distance - equator points 1 degree apart ≈ 111 km
    dist = haversine_distance(0, 0, 0, 1)
    assert 110 < dist < 112, f"Equator test failed: {dist}"
    print(f"  Test 3 (equator 1°): {dist:.2f} km - PASS")

    print("All Haversine tests passed!")


if __name__ == "__main__":
    print("Testing Haversine function...")
    test_haversine()
```

### Expected Output
```
Testing Haversine function...
  Test 1 (same point): PASS
  Test 2 (Taipei 101 → Main Station): 5.21 km - PASS
  Test 3 (equator 1°): 111.19 km - PASS
All Haversine tests passed!
```

---

## Exercise 2: Basic OSRM Route Request (15 minutes)

### Task
Create a function to get driving distance and duration from OSRM.

### Requirements
1. Build correct OSRM URL with coordinates
2. Handle API response parsing
3. Return distance in km and duration in minutes
4. Handle errors gracefully

### Starter Code

```python
import requests

def get_osrm_route(start_lat: float, start_lon: float,
                   end_lat: float, end_lon: float) -> dict | None:
    """
    Get driving route information from OSRM.

    IMPORTANT: OSRM uses longitude,latitude order (not lat,lon)!

    Args:
        start_lat: Starting latitude
        start_lon: Starting longitude
        end_lat: Ending latitude
        end_lon: Ending longitude

    Returns:
        Dictionary with:
        - distance_km: Driving distance in kilometers
        - duration_min: Estimated time in minutes
        Or None if the request fails

    Example:
        >>> get_osrm_route(25.0330, 121.5654, 25.0478, 121.5170)
        {'distance_km': 6.23, 'duration_min': 12.5}
    """
    # OSRM demo server URL
    base_url = "https://router.project-osrm.org/route/v1/driving"

    # TODO: Implement the OSRM request
    # 1. Build coordinates string: "lon1,lat1;lon2,lat2"
    #    REMEMBER: longitude comes first!
    # 2. Make GET request to: base_url + "/" + coordinates
    # 3. Check response.status_code == 200
    # 4. Parse JSON and check data["code"] == "Ok"
    # 5. Extract distance (meters) and duration (seconds) from routes[0]
    # 6. Convert to km and minutes, return as dict

    pass


# Test (requires internet connection)
def test_osrm_route():
    print("Testing OSRM route function...")

    # Taipei 101 to Main Station
    result = get_osrm_route(25.0330, 121.5654, 25.0478, 121.5170)

    if result is None:
        print("  ERROR: No result returned (check internet connection)")
        return

    assert "distance_km" in result, "Missing distance_km"
    assert "duration_min" in result, "Missing duration_min"

    print(f"  Distance: {result['distance_km']:.2f} km")
    print(f"  Duration: {result['duration_min']:.1f} min")

    # Sanity check - driving should be longer than straight-line
    straight_line = haversine_distance(25.0330, 121.5654, 25.0478, 121.5170)
    assert result['distance_km'] > straight_line, "Driving should be > straight-line"

    print("  OSRM route test: PASS")


if __name__ == "__main__":
    test_osrm_route()
```

---

## Exercise 3: 2D Distance Matrix (15 minutes)

### Task
Create functions to build and display a distance matrix.

### Requirements
1. Create an NxN matrix for N locations
2. Fill with Haversine distances
3. Pretty-print the matrix with location names

### Starter Code

```python
def create_distance_matrix(locations: list[dict]) -> list[list[float]]:
    """
    Create a distance matrix using Haversine distances.

    Args:
        locations: List of dicts with 'name', 'lat', 'lon'

    Returns:
        2D list where matrix[i][j] is the distance from location i to j

    Example:
        >>> locs = [
        ...     {"name": "A", "lat": 25.0, "lon": 121.0},
        ...     {"name": "B", "lat": 25.1, "lon": 121.1}
        ... ]
        >>> matrix = create_distance_matrix(locs)
        >>> len(matrix)
        2
        >>> matrix[0][0]
        0.0
    """
    # TODO: Implement distance matrix creation
    # 1. Get the number of locations (n)
    # 2. Create an n x n matrix filled with 0.0
    # 3. For each pair (i, j) where i != j:
    #    - Calculate Haversine distance
    #    - Store in matrix[i][j]
    # 4. Return the matrix

    pass


def print_distance_matrix(matrix: list[list[float]], locations: list[dict]) -> None:
    """
    Pretty-print a distance matrix with location names.

    Args:
        matrix: 2D distance matrix
        locations: List of location dicts with 'name'

    Output format:
                 Loc1      Loc2      Loc3
        Loc1     0.00      5.21     10.34
        Loc2     5.21      0.00      6.78
        Loc3    10.34      6.78      0.00
    """
    # TODO: Implement pretty printing
    # 1. Print header row with location names (truncated to 8 chars)
    # 2. For each row:
    #    - Print location name
    #    - Print each distance value formatted to 2 decimal places

    pass


# Test
def test_distance_matrix():
    print("Testing distance matrix...")

    locations = [
        {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
        {"name": "Main Station", "lat": 25.0478, "lon": 121.5170},
        {"name": "Palace Museum", "lat": 25.1024, "lon": 121.5485},
    ]

    matrix = create_distance_matrix(locations)

    # Check dimensions
    assert len(matrix) == 3, "Wrong number of rows"
    assert all(len(row) == 3 for row in matrix), "Wrong number of columns"
    print("  Dimensions: PASS")

    # Check diagonal is zero
    for i in range(len(matrix)):
        assert matrix[i][i] == 0.0, f"Diagonal [{i}][{i}] not zero"
    print("  Diagonal zeros: PASS")

    # Check symmetry (Haversine is symmetric)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            assert abs(matrix[i][j] - matrix[j][i]) < 0.01, "Matrix not symmetric"
    print("  Symmetry: PASS")

    # Display the matrix
    print("\nDistance Matrix (km):")
    print_distance_matrix(matrix, locations)


if __name__ == "__main__":
    test_distance_matrix()
```

---

## Exercise 4: OSRM Table Service (20 minutes)

### Task
Use OSRM's table service to get distance/duration matrices efficiently.

### Requirements
1. Build request for multiple locations in one call
2. Parse the response into distance and duration matrices
3. Handle errors appropriately

### Starter Code

```python
import requests

def get_osrm_matrix(locations: list[dict]) -> tuple[list[list[float]], list[list[float]]]:
    """
    Get distance and duration matrices using OSRM table service.

    This is much more efficient than making N² individual route requests!

    Args:
        locations: List of dicts with 'lat' and 'lon'

    Returns:
        Tuple of (distance_matrix_km, duration_matrix_min)
        Both are 2D lists where [i][j] is from location i to j

    Example:
        >>> locs = [{"lat": 25.0, "lon": 121.0}, {"lat": 25.1, "lon": 121.1}]
        >>> dist, dur = get_osrm_matrix(locs)
        >>> dist[0][1]  # Distance from loc 0 to loc 1
        15.23
    """
    base_url = "https://router.project-osrm.org/table/v1/driving"

    # TODO: Implement OSRM table request
    # 1. Build coordinates string: "lon1,lat1;lon2,lat2;lon3,lat3;..."
    # 2. Make GET request with params: {"annotations": "distance,duration"}
    # 3. Check response code and data["code"] == "Ok"
    # 4. Extract "distances" (in meters) and "durations" (in seconds)
    # 5. Convert to km and minutes
    # 6. Return both matrices

    # On error, return empty matrices
    n = len(locations)
    empty = [[0.0] * n for _ in range(n)]
    return empty, empty


# Test
def test_osrm_matrix():
    print("Testing OSRM table service...")

    locations = [
        {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
        {"name": "Main Station", "lat": 25.0478, "lon": 121.5170},
        {"name": "Palace Museum", "lat": 25.1024, "lon": 121.5485},
    ]

    dist_matrix, dur_matrix = get_osrm_matrix(locations)

    # Check dimensions
    assert len(dist_matrix) == 3, "Wrong distance matrix size"
    assert len(dur_matrix) == 3, "Wrong duration matrix size"
    print("  Dimensions: PASS")

    # Check diagonal is approximately zero (OSRM may return small values)
    for i in range(len(dist_matrix)):
        assert dist_matrix[i][i] < 0.1, f"Distance diagonal [{i}][{i}] not near zero"
        assert dur_matrix[i][i] < 0.1, f"Duration diagonal [{i}][{i}] not near zero"
    print("  Diagonal zeros: PASS")

    # Check we got actual distances (not zeros)
    assert dist_matrix[0][1] > 0, "No distance data"
    assert dur_matrix[0][1] > 0, "No duration data"
    print("  Non-zero values: PASS")

    print("\nOSRM Distance Matrix (km):")
    print_distance_matrix(dist_matrix, locations)

    print("\nOSRM Duration Matrix (min):")
    print_distance_matrix(dur_matrix, locations)


if __name__ == "__main__":
    test_osrm_matrix()
```

---

## Exercise 5: Compare Haversine vs OSRM (15 minutes)

### Task
Create a comparison report showing the difference between straight-line and driving distances.

### Requirements
1. Calculate both Haversine and OSRM distances
2. Compute the ratio (driving/straight-line)
3. Display a formatted comparison report

### Starter Code

```python
def compare_distances(locations: list[dict]) -> list[dict]:
    """
    Compare Haversine and OSRM distances for all location pairs.

    Args:
        locations: List of location dicts

    Returns:
        List of comparison dicts with:
        - from_name: Starting location name
        - to_name: Ending location name
        - haversine_km: Straight-line distance
        - driving_km: OSRM driving distance
        - driving_min: OSRM driving time
        - ratio: driving_km / haversine_km

    Example:
        >>> locs = [{"name": "A", ...}, {"name": "B", ...}]
        >>> comparisons = compare_distances(locs)
        >>> comparisons[0]['ratio']
        1.45
    """
    # TODO: Implement comparison
    # 1. Build Haversine matrix
    # 2. Get OSRM matrix
    # 3. For each unique pair (i < j):
    #    - Calculate ratio
    #    - Add to results list
    # 4. Return results

    pass


def print_comparison_report(comparisons: list[dict]) -> None:
    """
    Print a formatted comparison report.

    Args:
        comparisons: List of comparison dicts from compare_distances()

    Output format:
    ============================================================
    DISTANCE COMPARISON: Straight-Line vs Driving
    ============================================================

    Taipei 101 → Main Station
      Haversine:     5.21 km
      Driving:       6.54 km (12 min)
      Ratio:         1.26x

    ...
    """
    # TODO: Implement formatted output

    pass


# Test
def test_comparison():
    print("Testing distance comparison...")

    locations = [
        {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
        {"name": "Main Station", "lat": 25.0478, "lon": 121.5170},
        {"name": "Palace Museum", "lat": 25.1024, "lon": 121.5485},
    ]

    comparisons = compare_distances(locations)

    # Should have 3 pairs for 3 locations
    assert len(comparisons) == 3, f"Expected 3 pairs, got {len(comparisons)}"
    print("  Number of pairs: PASS")

    # Check all fields present
    required_fields = ['from_name', 'to_name', 'haversine_km', 'driving_km', 'driving_min', 'ratio']
    for comp in comparisons:
        for field in required_fields:
            assert field in comp, f"Missing field: {field}"
    print("  All fields present: PASS")

    # Ratio should be > 1 (driving is always longer)
    for comp in comparisons:
        assert comp['ratio'] >= 1.0, f"Ratio < 1: {comp}"
    print("  Ratios >= 1: PASS")

    print("\n")
    print_comparison_report(comparisons)


if __name__ == "__main__":
    test_comparison()
```

---

## Exercise 6: Route Analysis CLI (20 minutes)

### Task
Build a complete command-line route analysis tool.

### Requirements
1. Accept a list of locations (can be hardcoded or from input)
2. Calculate and display all distance comparisons
3. Allow user to get detailed route between any two locations
4. Handle errors gracefully

### Starter Code

```python
import requests
import time
from typing import Optional

def get_detailed_route(start: dict, end: dict) -> Optional[dict]:
    """
    Get detailed route information including geometry.

    Args:
        start: Dict with 'name', 'lat', 'lon'
        end: Dict with 'name', 'lat', 'lon'

    Returns:
        Dict with route details or None if failed
    """
    coords = f"{start['lon']},{start['lat']};{end['lon']},{end['lat']}"
    url = f"https://router.project-osrm.org/route/v1/driving/{coords}"

    try:
        response = requests.get(url, params={
            "overview": "full",
            "geometries": "geojson",
            "steps": "true"
        }, timeout=10)

        data = response.json()

        if data.get("code") == "Ok" and data.get("routes"):
            route = data["routes"][0]
            return {
                "from": start['name'],
                "to": end['name'],
                "distance_km": round(route["distance"] / 1000, 2),
                "duration_min": round(route["duration"] / 60, 1),
                "num_points": len(route["geometry"]["coordinates"]),
                "steps": len(route["legs"][0]["steps"]) if route.get("legs") else 0
            }
    except Exception as e:
        print(f"Error: {e}")

    return None


def route_analysis_cli():
    """
    Interactive CLI for route analysis.

    Features:
    1. Display all locations
    2. Show distance comparison matrix
    3. Get detailed route between two locations
    4. Exit
    """
    # Sample locations (you can modify these)
    locations = [
        {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
        {"name": "Main Station", "lat": 25.0478, "lon": 121.5170},
        {"name": "Palace Museum", "lat": 25.1024, "lon": 121.5485},
        {"name": "Shilin Market", "lat": 25.0881, "lon": 121.5240},
    ]

    print("\n" + "="*60)
    print("     Route Analysis Tool")
    print("="*60)

    # TODO: Implement the CLI loop
    # 1. Pre-calculate matrices (show progress)
    # 2. Show menu:
    #    1. List all locations
    #    2. Show comparison report
    #    3. Get detailed route (ask for indices)
    #    4. Exit
    # 3. Handle user input
    # 4. Add rate limiting (1 second) between API calls

    pass


# Simple test
def test_detailed_route():
    print("Testing detailed route function...")

    start = {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654}
    end = {"name": "Main Station", "lat": 25.0478, "lon": 121.5170}

    route = get_detailed_route(start, end)

    if route:
        print(f"  From: {route['from']}")
        print(f"  To: {route['to']}")
        print(f"  Distance: {route['distance_km']} km")
        print(f"  Duration: {route['duration_min']} min")
        print(f"  Route points: {route['num_points']}")
        print(f"  Steps: {route['steps']}")
        print("  Detailed route test: PASS")
    else:
        print("  ERROR: Failed to get route")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_detailed_route()
    else:
        route_analysis_cli()
```

### Expected CLI Behavior

```
============================================================
     Route Analysis Tool
============================================================

Loading data...
  Building Haversine matrix... done
  Fetching OSRM matrix... done

Menu:
  1. List all locations
  2. Show distance comparison
  3. Get detailed route
  4. Exit

Choice: 1

Locations:
  0. Taipei 101 (25.0330, 121.5654)
  1. Main Station (25.0478, 121.5170)
  2. Palace Museum (25.1024, 121.5485)
  3. Shilin Market (25.0881, 121.5240)

Choice: 3

Enter start location index: 0
Enter end location index: 2

Detailed Route: Taipei 101 → Palace Museum
  Distance: 10.45 km
  Duration: 18.2 min
  Route points: 234
  Turn-by-turn steps: 15

Choice: 4
Goodbye!
```

---

## Bonus Challenge: GeoJSON Export

### Task
Add the ability to export routes as GeoJSON files that can be viewed on a map.

### Requirements
1. Export single route as GeoJSON
2. Include start and end markers
3. Save to file
4. Provide instructions for viewing

### Hints

```python
import json

def export_route_geojson(route_data: dict, start: dict, end: dict,
                         filename: str) -> None:
    """
    Export a route to GeoJSON format.

    Args:
        route_data: Dict with 'coordinates' from OSRM
        start: Start location dict
        end: End location dict
        filename: Output filename (e.g., "route.geojson")
    """
    # Get route coordinates from OSRM response
    # You'll need to modify get_detailed_route to also return coordinates

    geojson = {
        "type": "FeatureCollection",
        "features": [
            # Route line
            {
                "type": "Feature",
                "properties": {"name": "Route"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": route_data.get("coordinates", [])
                }
            },
            # Start marker
            {
                "type": "Feature",
                "properties": {"name": start["name"], "marker-color": "#00ff00"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [start["lon"], start["lat"]]
                }
            },
            # End marker
            {
                "type": "Feature",
                "properties": {"name": end["name"], "marker-color": "#ff0000"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [end["lon"], end["lat"]]
                }
            }
        ]
    }

    with open(filename, 'w') as f:
        json.dump(geojson, f, indent=2)

    print(f"Saved to {filename}")
    print("View at: https://geojson.io")
```

---

## Submission Checklist

Before submitting, verify:

- [ ] Haversine function passes all tests
- [ ] OSRM route function works correctly
- [ ] Distance matrix is correctly built and displayed
- [ ] OSRM table service returns valid matrices
- [ ] Comparison report is clear and accurate
- [ ] CLI is interactive and handles errors
- [ ] Code is well-documented

## Grading Rubric

| Exercise | Points | Criteria |
|----------|--------|----------|
| Exercise 1 | 15 | Haversine formula correct |
| Exercise 2 | 15 | OSRM route request works |
| Exercise 3 | 15 | Matrix creation and display |
| Exercise 4 | 20 | OSRM table service works |
| Exercise 5 | 15 | Comparison report complete |
| Exercise 6 | 20 | CLI fully functional |
| Bonus | +15 | GeoJSON export works |

**Total: 100 points (+15 bonus)**

---

## Common Issues & Solutions

### Issue: "Connection refused" or timeout
**Solution:** Check your internet connection. The OSRM demo server may be slow.
```python
# Increase timeout
response = requests.get(url, timeout=30)
```

### Issue: Coordinates in wrong order
**Solution:** OSRM uses longitude,latitude (not lat,lon)!
```python
# CORRECT
coords = f"{lon},{lat};{lon2},{lat2}"

# WRONG
coords = f"{lat},{lon};{lat2},{lon2}"
```

### Issue: Matrix rows share the same list
**Solution:** Use list comprehension, not multiplication
```python
# WRONG
matrix = [[0] * n] * n

# CORRECT
matrix = [[0 for _ in range(n)] for _ in range(n)]
```

### Issue: Rate limiting (429 errors)
**Solution:** Add delays between requests
```python
import time
time.sleep(1)  # Wait 1 second between requests
```

---

*End of Week 8 Lab*
