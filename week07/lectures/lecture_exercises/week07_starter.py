"""
Week 7 Lab: The OSRM API (Real Routing) - Starter Code

Complete the TODO sections to implement route analysis functionality.

Run tests: python week07_starter.py --test
Run CLI:   python week07_starter.py
"""

import math
import requests
import time
import json
from typing import Optional


# =============================================================================
# Exercise 1: Haversine Distance
# =============================================================================

def haversine_distance(lat1: float, lon1: float,
                       lat2: float, lon2: float) -> float:
    """
    Calculate the straight-line distance between two points on Earth.

    The Haversine formula accounts for the Earth's curvature to calculate
    the shortest distance over the Earth's surface (great-circle distance).

    Args:
        lat1: Latitude of first point in degrees
        lon1: Longitude of first point in degrees
        lat2: Latitude of second point in degrees
        lon2: Longitude of second point in degrees

    Returns:
        Distance in kilometers

    Examples:
        >>> round(haversine_distance(25.0330, 121.5654, 25.0478, 121.5170), 2)
        5.21
        >>> haversine_distance(0, 0, 0, 0)
        0.0
    """
    # Earth's radius in kilometers
    R = 6371.0

    # TODO: Implement the Haversine formula
    # Step 1: Convert degrees to radians using math.radians()
    # Step 2: Calculate differences: delta_lat = lat2 - lat1, delta_lon = lon2 - lon1
    # Step 3: Apply formula:
    #   a = sin²(delta_lat/2) + cos(lat1) * cos(lat2) * sin²(delta_lon/2)
    #   c = 2 * arcsin(sqrt(a))
    #   distance = R * c
    # Step 4: Return the distance

    pass  # Remove this and add your implementation


# =============================================================================
# Exercise 2: Basic OSRM Route
# =============================================================================

def get_osrm_route(start_lat: float, start_lon: float,
                   end_lat: float, end_lon: float) -> Optional[dict]:
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
        >>> result = get_osrm_route(25.0330, 121.5654, 25.0478, 121.5170)
        >>> result['distance_km'] > 0
        True
    """
    base_url = "https://router.project-osrm.org/route/v1/driving"

    # TODO: Implement OSRM route request
    # Step 1: Build coordinates string "lon1,lat1;lon2,lat2" (longitude first!)
    # Step 2: Construct full URL: base_url + "/" + coordinates
    # Step 3: Make GET request with timeout=10
    # Step 4: Check response.status_code == 200
    # Step 5: Parse JSON response
    # Step 6: Check data["code"] == "Ok"
    # Step 7: Extract distance (meters) and duration (seconds) from data["routes"][0]
    # Step 8: Convert and return: {"distance_km": ..., "duration_min": ...}
    # Step 9: Return None on any error

    pass  # Remove this and add your implementation


# =============================================================================
# Exercise 3: Distance Matrix
# =============================================================================

def create_distance_matrix(locations: list[dict]) -> list[list[float]]:
    """
    Create a distance matrix using Haversine distances.

    Args:
        locations: List of dicts with 'name', 'lat', 'lon'

    Returns:
        2D list where matrix[i][j] is distance from location i to j in km
        Diagonal elements (i == j) should be 0.0

    Example:
        >>> locs = [{"name": "A", "lat": 25.0, "lon": 121.0},
        ...         {"name": "B", "lat": 25.1, "lon": 121.1}]
        >>> matrix = create_distance_matrix(locs)
        >>> matrix[0][0]
        0.0
        >>> matrix[0][1] > 0
        True
    """
    # TODO: Implement distance matrix creation
    # Step 1: Get number of locations: n = len(locations)
    # Step 2: Create n x n matrix filled with 0.0
    #         Use: [[0.0 for _ in range(n)] for _ in range(n)]
    # Step 3: For each pair (i, j) where i != j:
    #         Calculate haversine_distance and store in matrix[i][j]
    # Step 4: Round values to 2 decimal places
    # Step 5: Return the matrix

    pass  # Remove this and add your implementation


def print_distance_matrix(matrix: list[list[float]], locations: list[dict]) -> None:
    """
    Pretty-print a distance matrix with location names.

    Args:
        matrix: 2D distance matrix
        locations: List of location dicts with 'name'
    """
    # TODO: Implement pretty printing
    # Step 1: Print header row with location names (use [:8] to truncate)
    # Step 2: For each row i:
    #         - Print location name (truncated)
    #         - Print each value formatted as f"{val:>8.2f}"
    # Use string formatting like: f"{name[:8]:>10}" for aligned columns

    pass  # Remove this and add your implementation


# =============================================================================
# Exercise 4: OSRM Table Service
# =============================================================================

def get_osrm_matrix(locations: list[dict]) -> tuple[list[list[float]], list[list[float]]]:
    """
    Get distance and duration matrices using OSRM table service.

    This makes ONE API call instead of N² calls!

    Args:
        locations: List of dicts with 'lat' and 'lon'

    Returns:
        Tuple of (distance_matrix_km, duration_matrix_min)
    """
    base_url = "https://router.project-osrm.org/table/v1/driving"

    # TODO: Implement OSRM table request
    # Step 1: Build coordinates string: "lon1,lat1;lon2,lat2;..."
    #         Use: ";".join(f"{loc['lon']},{loc['lat']}" for loc in locations)
    # Step 2: Make GET request with params={"annotations": "distance,duration"}
    # Step 3: Parse response and check data["code"] == "Ok"
    # Step 4: Get data["distances"] (meters) and data["durations"] (seconds)
    # Step 5: Convert to km and minutes
    # Step 6: Return (distance_matrix, duration_matrix)

    # Return empty matrices on error
    n = len(locations)
    empty = [[0.0] * n for _ in range(n)]
    return empty, empty


# =============================================================================
# Exercise 5: Compare Distances
# =============================================================================

def compare_distances(locations: list[dict]) -> list[dict]:
    """
    Compare Haversine and OSRM distances for all location pairs.

    Args:
        locations: List of location dicts

    Returns:
        List of comparison dicts with keys:
        - from_name, to_name
        - haversine_km, driving_km, driving_min
        - ratio (driving / haversine)
    """
    # TODO: Implement distance comparison
    # Step 1: Build Haversine matrix using create_distance_matrix()
    # Step 2: Get OSRM matrix using get_osrm_matrix()
    # Step 3: Create empty results list
    # Step 4: For each unique pair (i < j):
    #         Create dict with comparison data
    #         Calculate ratio = driving_km / haversine_km
    # Step 5: Return results list

    pass  # Remove this and add your implementation


def print_comparison_report(comparisons: list[dict]) -> None:
    """
    Print a formatted comparison report.

    Args:
        comparisons: List of comparison dicts from compare_distances()
    """
    # TODO: Implement formatted report
    # Print header
    # For each comparison:
    #   Print from → to
    #   Print haversine, driving, duration
    #   Print ratio

    pass  # Remove this and add your implementation


# =============================================================================
# Exercise 6: Detailed Route
# =============================================================================

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
                "coordinates": route["geometry"]["coordinates"],
                "num_points": len(route["geometry"]["coordinates"]),
                "steps": len(route["legs"][0]["steps"]) if route.get("legs") else 0
            }
    except Exception as e:
        print(f"Error: {e}")

    return None


# =============================================================================
# CLI Application
# =============================================================================

def route_analysis_cli():
    """
    Interactive CLI for route analysis.
    """
    locations = [
        {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
        {"name": "Main Station", "lat": 25.0478, "lon": 121.5170},
        {"name": "Palace Museum", "lat": 25.1024, "lon": 121.5485},
        {"name": "Shilin Market", "lat": 25.0881, "lon": 121.5240},
    ]

    print("\n" + "=" * 60)
    print("     Route Analysis Tool")
    print("=" * 60)

    # Pre-calculate matrices
    print("\nLoading data...")
    print("  Building Haversine matrix...", end=" ", flush=True)
    haversine_matrix = create_distance_matrix(locations)
    print("done")

    print("  Fetching OSRM matrix...", end=" ", flush=True)
    osrm_dist, osrm_dur = get_osrm_matrix(locations)
    print("done")

    while True:
        print("\nMenu:")
        print("  1. List all locations")
        print("  2. Show distance comparison")
        print("  3. Get detailed route")
        print("  4. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            print("\nLocations:")
            for i, loc in enumerate(locations):
                print(f"  {i}. {loc['name']} ({loc['lat']}, {loc['lon']})")

        elif choice == "2":
            comparisons = compare_distances(locations)
            if comparisons:
                print_comparison_report(comparisons)
            else:
                print("No comparison data available")

        elif choice == "3":
            print("\nLocations:")
            for i, loc in enumerate(locations):
                print(f"  {i}. {loc['name']}")

            try:
                start_idx = int(input("Enter start location index: "))
                end_idx = int(input("Enter end location index: "))

                if 0 <= start_idx < len(locations) and 0 <= end_idx < len(locations):
                    if start_idx != end_idx:
                        print("\nFetching detailed route...")
                        route = get_detailed_route(locations[start_idx], locations[end_idx])
                        if route:
                            print(f"\nDetailed Route: {route['from']} → {route['to']}")
                            print(f"  Distance: {route['distance_km']} km")
                            print(f"  Duration: {route['duration_min']} min")
                            print(f"  Route points: {route['num_points']}")
                            print(f"  Turn-by-turn steps: {route['steps']}")
                        else:
                            print("Failed to get route")
                        time.sleep(1)  # Rate limiting
                    else:
                        print("Start and end must be different")
                else:
                    print("Invalid index")
            except ValueError:
                print("Please enter a valid number")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


# =============================================================================
# Test Functions
# =============================================================================

def test_haversine():
    """Test the Haversine distance function."""
    print("\nTesting Haversine function...")

    # Test 1: Same point
    result = haversine_distance(25.0, 121.0, 25.0, 121.0)
    assert result == 0.0, f"Same point should be 0, got {result}"
    print("  Test 1 (same point): PASS")

    # Test 2: Taipei 101 to Main Station
    result = haversine_distance(25.0330, 121.5654, 25.0478, 121.5170)
    assert 5.0 < result < 5.5, f"Expected ~5.2 km, got {result}"
    print(f"  Test 2 (Taipei): {result:.2f} km - PASS")

    # Test 3: Equator test
    result = haversine_distance(0, 0, 0, 1)
    assert 110 < result < 112, f"Expected ~111 km, got {result}"
    print(f"  Test 3 (equator): {result:.2f} km - PASS")

    print("All Haversine tests passed!")


def test_osrm_route():
    """Test the OSRM route function."""
    print("\nTesting OSRM route function...")

    result = get_osrm_route(25.0330, 121.5654, 25.0478, 121.5170)

    if result is None:
        print("  WARNING: Could not connect to OSRM (check internet)")
        return

    assert "distance_km" in result, "Missing distance_km"
    assert "duration_min" in result, "Missing duration_min"
    assert result["distance_km"] > 0, "Distance should be positive"
    assert result["duration_min"] > 0, "Duration should be positive"

    print(f"  Distance: {result['distance_km']:.2f} km")
    print(f"  Duration: {result['duration_min']:.1f} min")
    print("OSRM route test: PASS")


def test_distance_matrix():
    """Test distance matrix creation."""
    print("\nTesting distance matrix...")

    locations = [
        {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
        {"name": "Main Station", "lat": 25.0478, "lon": 121.5170},
        {"name": "Palace Museum", "lat": 25.1024, "lon": 121.5485},
    ]

    matrix = create_distance_matrix(locations)

    if matrix is None:
        print("  ERROR: create_distance_matrix returned None")
        return

    # Check dimensions
    assert len(matrix) == 3, f"Expected 3 rows, got {len(matrix)}"
    assert all(len(row) == 3 for row in matrix), "All rows should have 3 columns"
    print("  Dimensions: PASS")

    # Check diagonal
    for i in range(3):
        assert matrix[i][i] == 0.0, f"Diagonal [{i}][{i}] should be 0"
    print("  Diagonal: PASS")

    # Check symmetry
    for i in range(3):
        for j in range(3):
            assert abs(matrix[i][j] - matrix[j][i]) < 0.01, "Should be symmetric"
    print("  Symmetry: PASS")

    print("\nDistance Matrix (km):")
    print_distance_matrix(matrix, locations)
    print("Distance matrix test: PASS")


def test_osrm_matrix():
    """Test OSRM table service."""
    print("\nTesting OSRM table service...")

    locations = [
        {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
        {"name": "Main Station", "lat": 25.0478, "lon": 121.5170},
    ]

    dist, dur = get_osrm_matrix(locations)

    # Check we got non-zero values
    if dist[0][1] == 0 and dist[1][0] == 0:
        print("  WARNING: Could not get OSRM data (check internet)")
        return

    assert dist[0][1] > 0, "Distance should be positive"
    assert dur[0][1] > 0, "Duration should be positive"

    print(f"  Distance [0][1]: {dist[0][1]:.2f} km")
    print(f"  Duration [0][1]: {dur[0][1]:.1f} min")
    print("OSRM table test: PASS")


def test_comparison():
    """Test distance comparison."""
    print("\nTesting distance comparison...")

    locations = [
        {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
        {"name": "Main Station", "lat": 25.0478, "lon": 121.5170},
    ]

    comparisons = compare_distances(locations)

    if comparisons is None or len(comparisons) == 0:
        print("  WARNING: No comparison data (check implementation)")
        return

    comp = comparisons[0]
    required = ['from_name', 'to_name', 'haversine_km', 'driving_km', 'driving_min', 'ratio']

    for field in required:
        assert field in comp, f"Missing field: {field}"

    assert comp['ratio'] >= 1.0, "Ratio should be >= 1"

    print(f"  From: {comp['from_name']}")
    print(f"  To: {comp['to_name']}")
    print(f"  Haversine: {comp['haversine_km']:.2f} km")
    print(f"  Driving: {comp['driving_km']:.2f} km")
    print(f"  Ratio: {comp['ratio']:.2f}x")
    print("Comparison test: PASS")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running Week 7 Lab Tests")
    print("=" * 60)

    test_haversine()
    time.sleep(1)

    test_osrm_route()
    time.sleep(1)

    test_distance_matrix()
    time.sleep(1)

    test_osrm_matrix()
    time.sleep(1)

    test_comparison()

    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_all_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # Quick demo without full CLI
        print("Quick Demo:")
        locations = [
            {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
            {"name": "Main Station", "lat": 25.0478, "lon": 121.5170},
        ]

        print("\nHaversine distance:")
        h_dist = haversine_distance(25.0330, 121.5654, 25.0478, 121.5170)
        if h_dist:
            print(f"  {h_dist:.2f} km")

        print("\nOSRM distance:")
        osrm = get_osrm_route(25.0330, 121.5654, 25.0478, 121.5170)
        if osrm:
            print(f"  {osrm['distance_km']:.2f} km ({osrm['duration_min']:.1f} min)")
    else:
        route_analysis_cli()
