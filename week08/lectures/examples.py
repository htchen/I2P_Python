"""
Week 8: The OSRM API (Real Routing) - Code Examples

This file contains runnable examples from the Week 8 lecture.
Run with: python examples.py

Note: Some examples require internet access to reach the OSRM API.
"""

import requests
import time
import math
import json
from typing import Optional


# =============================================================================
# Example 1: Haversine Distance Calculation
# =============================================================================

def haversine_distance(lat1: float, lon1: float,
                       lat2: float, lon2: float) -> float:
    """
    Calculate the straight-line distance between two points on Earth.

    Args:
        lat1, lon1: First point coordinates (in degrees)
        lat2, lon2: Second point coordinates (in degrees)

    Returns:
        Distance in kilometers
    """
    R = 6371.0  # Earth's radius in kilometers

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    # Haversine formula
    a = (math.sin(delta_lat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(delta_lon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def example_haversine():
    """Demonstrate Haversine distance calculation."""
    print("\n" + "="*60)
    print("Example 1: Haversine (Straight-Line) Distance")
    print("="*60)

    # Taipei 101 to Taipei Main Station
    taipei_101 = (25.0330, 121.5654)
    taipei_station = (25.0478, 121.5170)

    distance = haversine_distance(
        taipei_101[0], taipei_101[1],
        taipei_station[0], taipei_station[1]
    )

    print(f"From: Taipei 101 ({taipei_101[0]}, {taipei_101[1]})")
    print(f"To: Taipei Main Station ({taipei_station[0]}, {taipei_station[1]})")
    print(f"Straight-line distance: {distance:.2f} km")


# =============================================================================
# Example 2: Basic OSRM Route Request
# =============================================================================

def get_simple_route(start_lon: float, start_lat: float,
                     end_lon: float, end_lat: float) -> Optional[dict]:
    """
    Get a simple route between two points using OSRM.

    Args:
        start_lon, start_lat: Starting point (longitude, latitude)
        end_lon, end_lat: Ending point (longitude, latitude)

    Returns:
        Route information dict or None if failed
    """
    # IMPORTANT: OSRM uses longitude,latitude order!
    coordinates = f"{start_lon},{start_lat};{end_lon},{end_lat}"
    url = f"https://router.project-osrm.org/route/v1/driving/{coordinates}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("code") == "Ok" and data.get("routes"):
            route = data["routes"][0]
            return {
                "distance_m": route["distance"],
                "distance_km": route["distance"] / 1000,
                "duration_s": route["duration"],
                "duration_min": route["duration"] / 60
            }
    except requests.RequestException as e:
        print(f"Request error: {e}")

    return None


def example_basic_route():
    """Demonstrate a basic OSRM route request."""
    print("\n" + "="*60)
    print("Example 2: Basic OSRM Route")
    print("="*60)

    # Taipei 101 to Taipei Main Station
    # Note: longitude first!
    route = get_simple_route(
        start_lon=121.5654, start_lat=25.0330,  # Taipei 101
        end_lon=121.5170, end_lat=25.0478       # Taipei Main Station
    )

    if route:
        print("Route: Taipei 101 → Taipei Main Station")
        print(f"Distance: {route['distance_km']:.2f} km")
        print(f"Duration: {route['duration_min']:.1f} minutes")
    else:
        print("Failed to get route")


# =============================================================================
# Example 3: 2D Lists (Matrices)
# =============================================================================

def example_2d_lists():
    """Demonstrate 2D list operations."""
    print("\n" + "="*60)
    print("Example 3: 2D Lists (Matrices)")
    print("="*60)

    # Creating a 3x3 matrix
    print("\n1. Creating a 3x3 matrix:")
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    for row in matrix:
        print(f"   {row}")

    # Accessing elements
    print(f"\n2. Accessing elements:")
    print(f"   matrix[0][2] = {matrix[0][2]}")  # Row 0, Col 2
    print(f"   matrix[2][0] = {matrix[2][0]}")  # Row 2, Col 0
    print(f"   matrix[1] = {matrix[1]}")        # Entire row 1

    # Creating with list comprehension
    print(f"\n3. Creating a 4x4 matrix of zeros with list comprehension:")
    zeros = [[0 for _ in range(4)] for _ in range(4)]
    for row in zeros:
        print(f"   {row}")

    # Common mistake demonstration
    print(f"\n4. Common mistake - shared references:")
    wrong = [[0] * 3] * 3
    wrong[0][0] = 99
    print(f"   After wrong[0][0] = 99:")
    for row in wrong:
        print(f"   {row}")
    print("   ↑ All rows changed because they share the same list!")

    correct = [[0] * 3 for _ in range(3)]
    correct[0][0] = 99
    print(f"\n   After correct[0][0] = 99 (using list comprehension):")
    for row in correct:
        print(f"   {row}")
    print("   ↑ Only row 0 changed - each row is independent!")


# =============================================================================
# Example 4: Building a Haversine Distance Matrix
# =============================================================================

def build_haversine_matrix(locations: list[dict]) -> list[list[float]]:
    """
    Build a distance matrix using Haversine distances.

    Args:
        locations: List of dicts with 'name', 'lat', 'lon'

    Returns:
        2D matrix of distances in km
    """
    n = len(locations)
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = round(haversine_distance(
                    locations[i]['lat'], locations[i]['lon'],
                    locations[j]['lat'], locations[j]['lon']
                ), 2)

    return matrix


def print_matrix(matrix: list[list[float]], locations: list[dict],
                 title: str = "Distance Matrix"):
    """Pretty print a distance matrix."""
    print(f"\n{title}:")

    # Header
    print("          ", end="")
    for loc in locations:
        print(f"{loc['name'][:8]:>10}", end="")
    print()

    # Rows
    for i, row in enumerate(matrix):
        print(f"{locations[i]['name'][:8]:>10}", end="")
        for val in row:
            print(f"{val:>10.2f}", end="")
        print()


def example_haversine_matrix():
    """Demonstrate building a Haversine distance matrix."""
    print("\n" + "="*60)
    print("Example 4: Haversine Distance Matrix")
    print("="*60)

    locations = [
        {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
        {"name": "Main Station", "lat": 25.0478, "lon": 121.5170},
        {"name": "Palace Museum", "lat": 25.1024, "lon": 121.5485},
    ]

    matrix = build_haversine_matrix(locations)
    print_matrix(matrix, locations, "Haversine Distance Matrix (km)")


# =============================================================================
# Example 5: OSRM Table Service
# =============================================================================

def get_osrm_table(locations: list[dict]) -> tuple[list[list[float]], list[list[float]]]:
    """
    Get distance/duration matrix using OSRM's table service.

    Args:
        locations: List of dicts with 'lat' and 'lon'

    Returns:
        Tuple of (distance_km matrix, duration_min matrix)
    """
    # Build coordinates string (lon,lat;lon,lat;...)
    coords = ";".join(f"{loc['lon']},{loc['lat']}" for loc in locations)
    url = f"https://router.project-osrm.org/table/v1/driving/{coords}"

    try:
        response = requests.get(
            url,
            params={"annotations": "distance,duration"},
            timeout=30
        )
        data = response.json()

        if data.get("code") == "Ok":
            # Convert meters to km
            distances = data.get("distances", [])
            distance_km = [
                [round(d / 1000, 2) if d else 0 for d in row]
                for row in distances
            ]

            # Convert seconds to minutes
            durations = data.get("durations", [])
            duration_min = [
                [round(d / 60, 1) if d else 0 for d in row]
                for row in durations
            ]

            return distance_km, duration_min

    except requests.RequestException as e:
        print(f"Request error: {e}")

    # Return empty matrices on failure
    n = len(locations)
    empty = [[0.0 for _ in range(n)] for _ in range(n)]
    return empty, empty


def example_osrm_table():
    """Demonstrate OSRM table service for matrix calculation."""
    print("\n" + "="*60)
    print("Example 5: OSRM Table Service (Distance Matrix)")
    print("="*60)

    locations = [
        {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
        {"name": "Main Station", "lat": 25.0478, "lon": 121.5170},
        {"name": "Palace Museum", "lat": 25.1024, "lon": 121.5485},
    ]

    print("Fetching from OSRM (this may take a moment)...")
    dist_matrix, dur_matrix = get_osrm_table(locations)

    print_matrix(dist_matrix, locations, "OSRM Driving Distance Matrix (km)")
    print_matrix(dur_matrix, locations, "OSRM Driving Duration Matrix (min)")


# =============================================================================
# Example 6: Comparing Haversine vs OSRM
# =============================================================================

def example_compare_distances():
    """Compare Haversine and OSRM distances."""
    print("\n" + "="*60)
    print("Example 6: Comparing Haversine vs OSRM Distances")
    print("="*60)

    locations = [
        {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
        {"name": "Main Station", "lat": 25.0478, "lon": 121.5170},
        {"name": "Palace Museum", "lat": 25.1024, "lon": 121.5485},
    ]

    print("Building Haversine matrix...")
    haversine = build_haversine_matrix(locations)

    print("Fetching OSRM matrix...")
    osrm_dist, osrm_dur = get_osrm_table(locations)

    print("\nComparison:")
    print("-" * 70)

    n = len(locations)
    for i in range(n):
        for j in range(n):
            if i < j:  # Only show each pair once
                h = haversine[i][j]
                o = osrm_dist[i][j]
                t = osrm_dur[i][j]
                ratio = o / h if h > 0 else 0

                print(f"\n{locations[i]['name']} → {locations[j]['name']}")
                print(f"  Haversine:     {h:>7.2f} km")
                print(f"  OSRM Driving:  {o:>7.2f} km ({t:.0f} min)")
                print(f"  Ratio:         {ratio:>7.2f}x")


# =============================================================================
# Example 7: Route with Geometry
# =============================================================================

def get_route_with_geometry(start: dict, end: dict) -> Optional[dict]:
    """
    Get a route with full geometry from OSRM.

    Args:
        start: Dict with 'lat', 'lon'
        end: Dict with 'lat', 'lon'

    Returns:
        Route dict with geometry, or None if failed
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
                "distance_km": round(route["distance"] / 1000, 2),
                "duration_min": round(route["duration"] / 60, 1),
                "geometry": route["geometry"],
                "coordinates": route["geometry"]["coordinates"],
                "num_points": len(route["geometry"]["coordinates"])
            }

    except requests.RequestException as e:
        print(f"Request error: {e}")

    return None


def example_route_geometry():
    """Demonstrate getting route geometry."""
    print("\n" + "="*60)
    print("Example 7: Route with Geometry")
    print("="*60)

    start = {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654}
    end = {"name": "Main Station", "lat": 25.0478, "lon": 121.5170}

    print(f"Fetching route: {start['name']} → {end['name']}...")
    route = get_route_with_geometry(start, end)

    if route:
        print(f"Distance: {route['distance_km']} km")
        print(f"Duration: {route['duration_min']} min")
        print(f"Geometry points: {route['num_points']}")
        print(f"First 3 coordinates: {route['coordinates'][:3]}")
        print(f"Last 3 coordinates: {route['coordinates'][-3:]}")
    else:
        print("Failed to get route")


# =============================================================================
# Example 8: ASCII Route Visualization
# =============================================================================

def visualize_route_ascii(coordinates: list[list[float]],
                          width: int = 50, height: int = 15) -> str:
    """
    Create ASCII visualization of a route.

    Args:
        coordinates: List of [lon, lat] pairs
        width: Output width in characters
        height: Output height in characters

    Returns:
        ASCII art string
    """
    if not coordinates:
        return "No route data"

    lons = [c[0] for c in coordinates]
    lats = [c[1] for c in coordinates]

    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)

    lon_range = max_lon - min_lon or 0.001
    lat_range = max_lat - min_lat or 0.001

    # Create grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    # Plot points
    for i, (lon, lat) in enumerate(coordinates):
        x = int((lon - min_lon) / lon_range * (width - 1))
        y = int((max_lat - lat) / lat_range * (height - 1))

        x = max(0, min(width - 1, x))
        y = max(0, min(height - 1, y))

        if i == 0:
            grid[y][x] = 'S'
        elif i == len(coordinates) - 1:
            grid[y][x] = 'E'
        elif grid[y][x] == ' ':
            grid[y][x] = '·'

    # Build output
    border = '+' + '-' * width + '+'
    lines = [border]
    lines.extend('|' + ''.join(row) + '|' for row in grid)
    lines.append(border)

    return '\n'.join(lines)


def example_ascii_visualization():
    """Demonstrate ASCII route visualization."""
    print("\n" + "="*60)
    print("Example 8: ASCII Route Visualization")
    print("="*60)

    start = {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654}
    end = {"name": "Palace Museum", "lat": 25.1024, "lon": 121.5485}

    print(f"Fetching route: {start['name']} → {end['name']}...")
    route = get_route_with_geometry(start, end)

    if route:
        print(f"\nDistance: {route['distance_km']} km")
        print(f"Duration: {route['duration_min']} min")
        print(f"\nRoute visualization:")
        print(visualize_route_ascii(route['coordinates']))
        print("S = Start, E = End, · = Route points")
    else:
        print("Failed to get route")


# =============================================================================
# Example 9: Export to GeoJSON
# =============================================================================

def route_to_geojson(route: dict, start_name: str, end_name: str) -> dict:
    """
    Convert route to GeoJSON FeatureCollection.

    Args:
        route: Route dict with 'coordinates'
        start_name: Name for start marker
        end_name: Name for end marker

    Returns:
        GeoJSON FeatureCollection
    """
    coords = route.get("coordinates", [])

    features = [
        {
            "type": "Feature",
            "properties": {
                "name": "Route",
                "distance_km": route.get("distance_km", 0),
                "duration_min": route.get("duration_min", 0)
            },
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            }
        },
        {
            "type": "Feature",
            "properties": {"name": start_name, "marker-color": "#00ff00"},
            "geometry": {"type": "Point", "coordinates": coords[0] if coords else [0, 0]}
        },
        {
            "type": "Feature",
            "properties": {"name": end_name, "marker-color": "#ff0000"},
            "geometry": {"type": "Point", "coordinates": coords[-1] if coords else [0, 0]}
        }
    ]

    return {"type": "FeatureCollection", "features": features}


def example_geojson_export():
    """Demonstrate exporting route to GeoJSON."""
    print("\n" + "="*60)
    print("Example 9: Export to GeoJSON")
    print("="*60)

    start = {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654}
    end = {"name": "Main Station", "lat": 25.0478, "lon": 121.5170}

    print(f"Fetching route: {start['name']} → {end['name']}...")
    route = get_route_with_geometry(start, end)

    if route:
        geojson = route_to_geojson(route, start['name'], end['name'])

        print("\nGeoJSON structure:")
        print(f"  Type: {geojson['type']}")
        print(f"  Features: {len(geojson['features'])}")
        for f in geojson['features']:
            print(f"    - {f['geometry']['type']}: {f['properties'].get('name', 'N/A')}")

        # Save to file
        filename = "example_route.geojson"
        with open(filename, 'w') as f:
            json.dump(geojson, f, indent=2)
        print(f"\nSaved to {filename}")
        print("Open at https://geojson.io to view on a map!")
    else:
        print("Failed to get route")


# =============================================================================
# Example 10: Complete Route Analyzer Class
# =============================================================================

class RouteAnalyzer:
    """Complete route analysis tool."""

    OSRM_BASE = "https://router.project-osrm.org"

    def __init__(self, locations: list[dict]):
        """Initialize with locations."""
        self.locations = locations
        self.haversine_matrix = None
        self.osrm_distance_matrix = None
        self.osrm_duration_matrix = None

    def _haversine(self, lat1: float, lon1: float,
                   lat2: float, lon2: float) -> float:
        """Calculate straight-line distance in km."""
        R = 6371.0
        lat1_r, lat2_r = math.radians(lat1), math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (math.sin(dlat/2)**2 +
             math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon/2)**2)
        return R * 2 * math.asin(math.sqrt(a))

    def build_haversine_matrix(self) -> list[list[float]]:
        """Build straight-line distance matrix."""
        n = len(self.locations)
        self.haversine_matrix = [[0.0]*n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i != j:
                    self.haversine_matrix[i][j] = round(self._haversine(
                        self.locations[i]['lat'], self.locations[i]['lon'],
                        self.locations[j]['lat'], self.locations[j]['lon']
                    ), 2)

        return self.haversine_matrix

    def build_osrm_matrix(self) -> tuple[list[list[float]], list[list[float]]]:
        """Build driving distance/duration matrices."""
        coords = ";".join(f"{loc['lon']},{loc['lat']}" for loc in self.locations)
        url = f"{self.OSRM_BASE}/table/v1/driving/{coords}"

        try:
            response = requests.get(url, params={"annotations": "distance,duration"}, timeout=30)
            data = response.json()

            if data.get("code") == "Ok":
                self.osrm_distance_matrix = [
                    [round(d/1000, 2) if d else 0 for d in row]
                    for row in data.get("distances", [])
                ]
                self.osrm_duration_matrix = [
                    [round(d/60, 1) if d else 0 for d in row]
                    for row in data.get("durations", [])
                ]
            else:
                raise ValueError(f"OSRM error: {data.get('code')}")

        except Exception as e:
            print(f"Error: {e}")
            n = len(self.locations)
            self.osrm_distance_matrix = [[0.0]*n for _ in range(n)]
            self.osrm_duration_matrix = [[0.0]*n for _ in range(n)]

        return self.osrm_distance_matrix, self.osrm_duration_matrix

    def analyze_all(self) -> dict:
        """Run complete analysis."""
        self.build_haversine_matrix()
        self.build_osrm_matrix()

        comparisons = []
        n = len(self.locations)

        for i in range(n):
            for j in range(n):
                if i < j:
                    h = self.haversine_matrix[i][j]
                    d = self.osrm_distance_matrix[i][j]
                    t = self.osrm_duration_matrix[i][j]
                    ratio = round(d / h, 2) if h > 0 else 0

                    comparisons.append({
                        "from": self.locations[i]['name'],
                        "to": self.locations[j]['name'],
                        "haversine_km": h,
                        "driving_km": d,
                        "driving_min": t,
                        "ratio": ratio
                    })

        return {
            "locations": self.locations,
            "haversine_matrix": self.haversine_matrix,
            "osrm_distance_matrix": self.osrm_distance_matrix,
            "osrm_duration_matrix": self.osrm_duration_matrix,
            "comparisons": comparisons
        }

    def print_summary(self) -> None:
        """Print analysis summary."""
        if not self.haversine_matrix:
            print("Run analyze_all() first!")
            return

        print("\n" + "="*70)
        print("ROUTE ANALYSIS SUMMARY")
        print("="*70)

        n = len(self.locations)
        for i in range(n):
            for j in range(n):
                if i < j:
                    h = self.haversine_matrix[i][j]
                    d = self.osrm_distance_matrix[i][j]
                    t = self.osrm_duration_matrix[i][j]
                    ratio = d / h if h > 0 else 0

                    print(f"\n{self.locations[i]['name']} → {self.locations[j]['name']}")
                    print(f"  Straight-line: {h:>7.2f} km")
                    print(f"  Driving:       {d:>7.2f} km ({t:.0f} min)")
                    print(f"  Ratio:         {ratio:>7.2f}x")


def example_route_analyzer():
    """Demonstrate the RouteAnalyzer class."""
    print("\n" + "="*60)
    print("Example 10: Complete Route Analyzer")
    print("="*60)

    locations = [
        {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
        {"name": "Main Station", "lat": 25.0478, "lon": 121.5170},
        {"name": "Palace Museum", "lat": 25.1024, "lon": 121.5485},
        {"name": "Shilin Market", "lat": 25.0881, "lon": 121.5240},
    ]

    analyzer = RouteAnalyzer(locations)

    print("Running analysis...")
    results = analyzer.analyze_all()

    analyzer.print_summary()

    print(f"\nTotal comparisons: {len(results['comparisons'])}")


# =============================================================================
# Main Menu
# =============================================================================

def show_menu():
    """Display the example menu."""
    print("\n" + "="*60)
    print("Week 8: OSRM API Examples")
    print("="*60)
    print("1.  Haversine Distance Calculation")
    print("2.  Basic OSRM Route")
    print("3.  2D Lists (Matrices)")
    print("4.  Haversine Distance Matrix")
    print("5.  OSRM Table Service")
    print("6.  Compare Haversine vs OSRM")
    print("7.  Route with Geometry")
    print("8.  ASCII Route Visualization")
    print("9.  Export to GeoJSON")
    print("10. Complete Route Analyzer")
    print("0.  Run All Examples")
    print("q.  Quit")
    print("-"*60)


def main():
    """Main function to run examples."""
    examples = {
        '1': example_haversine,
        '2': example_basic_route,
        '3': example_2d_lists,
        '4': example_haversine_matrix,
        '5': example_osrm_table,
        '6': example_compare_distances,
        '7': example_route_geometry,
        '8': example_ascii_visualization,
        '9': example_geojson_export,
        '10': example_route_analyzer,
    }

    while True:
        show_menu()
        choice = input("Select an example (0-10, q to quit): ").strip().lower()

        if choice == 'q':
            print("Goodbye!")
            break
        elif choice == '0':
            for func in examples.values():
                func()
                time.sleep(1)  # Rate limiting between API calls
        elif choice in examples:
            examples[choice]()
            if choice in ['2', '5', '6', '7', '8', '9', '10']:
                time.sleep(1)  # Rate limiting for API examples
        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
