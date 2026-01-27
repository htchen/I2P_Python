# Week 8: The OSRM API (Real Routing)

## Lecture Overview (3 Hours)

**Phase 2: The API & The Cloud** — "Fetching the World"

### Learning Objectives
By the end of this lecture, students will be able to:
1. Understand the difference between straight-line distance and actual travel distance
2. Use the OSRM (Open Source Routing Machine) API for route calculations
3. Work with 2D lists (matrices) to store distance/duration data
4. Parse complex route geometry from API responses
5. Build a route comparison tool that shows real vs estimated distances

### Prerequisites
- Week 5: The Nominatim API (Geocoding)
- Week 6: Generators and Lazy Loading
- Understanding of HTTP requests and JSON parsing

---

# Hour 1: Understanding Real-World Routing

## 1.1 The Problem with Straight-Line Distance

### Why "As the Crow Flies" Isn't Enough

When we calculated distances in previous weeks using the Haversine formula, we computed the **straight-line distance** (also called "great-circle distance" or "as the crow flies"). This is the shortest path between two points on Earth's surface.

```
Point A -------- straight line -------- Point B
         \                            /
          \    actual road path     /
           \________________________/
```

**But humans don't fly like crows!** We need to:
- Follow roads, highways, and paths
- Navigate around obstacles (buildings, rivers, mountains)
- Obey traffic rules (one-way streets, no U-turns)
- Consider different travel modes (driving, walking, cycling)

### A Real-World Example

Consider traveling from Taipei Main Station to Taipei 101:

| Measurement Type | Distance | Time |
|-----------------|----------|------|
| Straight-line (Haversine) | ~2.8 km | N/A |
| Driving distance | ~4.5 km | ~15 min |
| Walking distance | ~3.2 km | ~40 min |

The driving distance is **60% longer** than the straight-line distance! This difference matters enormously for:
- Delivery time estimates
- Ride-sharing fare calculations
- Emergency response planning
- Logistics and fleet management

### Why the Difference?

```
                    River (can't cross)
                         ~~~~
    [A] ----------------X---------------- [B]
         \                              /
          \    Bridge                  /
           \_____|____________________/
                 |
           Actual Route (much longer)
```

Real routes must account for:
1. **Physical barriers**: Rivers, mountains, buildings
2. **Infrastructure**: Roads exist only in certain places
3. **Traffic rules**: One-way streets, turn restrictions
4. **Mode of transport**: Cars can't use pedestrian paths; bikes can't use highways

---

## 1.2 Introduction to OSRM

### What is OSRM?

**OSRM** (Open Source Routing Machine) is a high-performance routing engine that calculates:
- **Routes**: The actual path between points
- **Distances**: Real travel distance along roads
- **Durations**: Estimated travel time
- **Geometry**: The shape of the route (for drawing on maps)

### How OSRM Works (Simplified)

```
┌─────────────────────────────────────────────────────────┐
│                    OSRM Server                          │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ OpenStreet  │ -> │   Graph     │ -> │   Routing   │ │
│  │ Map Data    │    │  Database   │    │  Algorithm  │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│                                               │         │
│                                               v         │
│                                        ┌───────────┐   │
│                                        │  Route    │   │
│                                        │  Result   │   │
│                                        └───────────┘   │
└─────────────────────────────────────────────────────────┘
```

1. **OpenStreetMap data** is processed into a graph structure
2. **Nodes** represent intersections and points along roads
3. **Edges** represent road segments with distances and travel times
4. **Routing algorithms** (like Dijkstra or Contraction Hierarchies) find the shortest/fastest path

### OSRM vs Google Maps vs Other Services

| Feature | OSRM | Google Maps | Mapbox |
|---------|------|-------------|--------|
| Cost | Free (self-hosted) or free public demo | Paid after free tier | Paid after free tier |
| Data Source | OpenStreetMap | Google's proprietary data | OpenStreetMap + proprietary |
| Rate Limits | None (self-hosted) | Yes | Yes |
| Traffic Data | No (basic OSRM) | Yes | Yes |
| Best For | Learning, prototypes, high-volume | Production apps | Production apps |

### The Public OSRM Demo Server

For learning and prototyping, OSRM provides a free demo server:

```
https://router.project-osrm.org/
```

**Important Usage Notes:**
- This is a **demo server** for testing only
- Don't use it for production applications
- Be respectful with request rates (add delays between requests)
- For production, host your own OSRM server or use a commercial service

---

## 1.3 OSRM API Basics

### API Endpoint Structure

```
https://router.project-osrm.org/route/v1/{profile}/{coordinates}?{options}
```

Let's break this down:

| Component | Description | Example |
|-----------|-------------|---------|
| `route/v1` | API version and service | Always `route/v1` for routing |
| `{profile}` | Travel mode | `driving`, `walking`, `cycling` |
| `{coordinates}` | Lon,Lat pairs separated by `;` | `121.5,25.0;121.6,25.1` |
| `{options}` | Query parameters | `overview=full&geometries=geojson` |

### Coordinate Format: Longitude First!

**Critical Warning:** OSRM uses **longitude,latitude** order (the opposite of what many people expect):

```python
# CORRECT - longitude first, then latitude
coordinates = "121.5654,25.0330;121.5170,25.0478"
#             lon      lat     lon      lat

# WRONG - this would put you in the wrong location!
coordinates = "25.0330,121.5654;25.0478,121.5170"
#             lat      lon      lat      lon
```

**Why this order?** It follows the mathematical convention where x (longitude) comes before y (latitude), like (x, y) coordinates.

### Your First OSRM Request

```python
import requests

def get_route(start_lon, start_lat, end_lon, end_lat):
    """
    Get a route between two points using OSRM.

    Args:
        start_lon, start_lat: Starting point coordinates
        end_lon, end_lat: Ending point coordinates

    Returns:
        dict: Route information or None if failed
    """
    # Build the coordinates string (lon,lat;lon,lat)
    coordinates = f"{start_lon},{start_lat};{end_lon},{end_lat}"

    # Build the URL
    url = f"https://router.project-osrm.org/route/v1/driving/{coordinates}"

    # Add parameters
    params = {
        "overview": "full",      # Get the full route geometry
        "geometries": "geojson"  # Return geometry as GeoJSON
    }

    # Make the request
    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


# Example: Taipei 101 to Taipei Main Station
# Taipei 101: 25.0330°N, 121.5654°E
# Taipei Main Station: 25.0478°N, 121.5170°E

result = get_route(
    start_lon=121.5654, start_lat=25.0330,  # Taipei 101
    end_lon=121.5170, end_lat=25.0478       # Taipei Main Station
)

if result:
    route = result["routes"][0]
    distance_km = route["distance"] / 1000
    duration_min = route["duration"] / 60

    print(f"Distance: {distance_km:.2f} km")
    print(f"Duration: {duration_min:.1f} minutes")
```

---

## 1.4 Understanding the OSRM Response

### Response Structure Overview

```json
{
    "code": "Ok",
    "routes": [
        {
            "distance": 4523.5,
            "duration": 892.3,
            "geometry": { ... },
            "legs": [ ... ]
        }
    ],
    "waypoints": [
        {
            "name": "Section 5, Xinyi Road",
            "location": [121.565397, 25.033108]
        },
        {
            "name": "Zhongxiao West Road",
            "location": [121.517032, 25.047798]
        }
    ]
}
```

### Key Fields Explained

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | Status: "Ok" for success |
| `routes` | array | List of possible routes (usually 1) |
| `routes[0].distance` | float | Total distance in **meters** |
| `routes[0].duration` | float | Total time in **seconds** |
| `routes[0].geometry` | object | The route shape for drawing on maps |
| `routes[0].legs` | array | Segments between waypoints |
| `waypoints` | array | Snapped locations on the road network |

### Why "Snapped" Waypoints?

When you provide coordinates, they might not be exactly on a road. OSRM "snaps" them to the nearest road:

```
Your input point: X (in a parking lot)
                   \
                    \
Nearest road: ═══════●═══════
              Snapped point
```

The `waypoints` array shows where your points were snapped to, which helps you understand if the route makes sense.

### Parsing the Response Safely

```python
def parse_route_response(data: dict) -> dict | None:
    """
    Safely parse an OSRM route response.

    Args:
        data: Raw JSON response from OSRM

    Returns:
        Parsed route info or None if invalid
    """
    # Check for success
    if data.get("code") != "Ok":
        print(f"OSRM error: {data.get('code')}")
        return None

    # Get the first route (OSRM usually returns one)
    routes = data.get("routes", [])
    if not routes:
        print("No routes found")
        return None

    route = routes[0]

    # Extract the key information
    return {
        "distance_meters": route.get("distance", 0),
        "distance_km": route.get("distance", 0) / 1000,
        "duration_seconds": route.get("duration", 0),
        "duration_minutes": route.get("duration", 0) / 60,
        "geometry": route.get("geometry"),
        "legs": route.get("legs", [])
    }


# Usage
if result:
    parsed = parse_route_response(result)
    if parsed:
        print(f"Distance: {parsed['distance_km']:.2f} km")
        print(f"Duration: {parsed['duration_minutes']:.1f} minutes")
```

---

## 1.5 Mini-Exercise 1: Your First Route

Calculate the driving route between two landmarks in your city:

```python
import requests

# TODO: Fill in the coordinates for two places you know
# Remember: longitude first, then latitude!

place_a = {
    "name": "Your Starting Point",
    "lon": 0.0,  # Fill in
    "lat": 0.0   # Fill in
}

place_b = {
    "name": "Your Destination",
    "lon": 0.0,  # Fill in
    "lat": 0.0   # Fill in
}

# Make the request
coords = f"{place_a['lon']},{place_a['lat']};{place_b['lon']},{place_b['lat']}"
url = f"https://router.project-osrm.org/route/v1/driving/{coords}"

response = requests.get(url, timeout=10)
data = response.json()

if data.get("code") == "Ok":
    route = data["routes"][0]
    print(f"From: {place_a['name']}")
    print(f"To: {place_b['name']}")
    print(f"Distance: {route['distance']/1000:.2f} km")
    print(f"Duration: {route['duration']/60:.1f} minutes")
```

<details>
<summary>Solution with Taipei landmarks</summary>

```python
import requests

place_a = {
    "name": "Taipei 101",
    "lon": 121.5654,
    "lat": 25.0330
}

place_b = {
    "name": "National Palace Museum",
    "lon": 121.5485,
    "lat": 25.1024
}

coords = f"{place_a['lon']},{place_a['lat']};{place_b['lon']},{place_b['lat']}"
url = f"https://router.project-osrm.org/route/v1/driving/{coords}"

response = requests.get(url, timeout=10)
data = response.json()

if data.get("code") == "Ok":
    route = data["routes"][0]
    print(f"From: {place_a['name']}")
    print(f"To: {place_b['name']}")
    print(f"Distance: {route['distance']/1000:.2f} km")
    print(f"Duration: {route['duration']/60:.1f} minutes")

# Expected output (approximately):
# From: Taipei 101
# To: National Palace Museum
# Distance: 10.23 km
# Duration: 18.5 minutes
```

</details>

---

# ☕ 5-Minute Break

Stand up, stretch, rest your eyes!

---

# Hour 2: 2D Lists (Matrices) and Distance Tables

## 2.1 Introduction to 2D Lists

### What is a 2D List?

A **2D list** (or matrix) is a list of lists. Think of it as a table or grid:

```python
# A 3x3 matrix (3 rows, 3 columns)
matrix = [
    [1, 2, 3],    # Row 0
    [4, 5, 6],    # Row 1
    [7, 8, 9]     # Row 2
]
#   ^  ^  ^
#   |  |  |
# Col 0  1  2
```

### Accessing Elements

Use two indices: `matrix[row][column]`

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Access element at row 0, column 2
print(matrix[0][2])  # 3

# Access element at row 2, column 0
print(matrix[2][0])  # 7

# Access the entire row 1
print(matrix[1])     # [4, 5, 6]
```

### Visual Representation

```
         Column
         0   1   2
       ┌───┬───┬───┐
Row 0  │ 1 │ 2 │ 3 │
       ├───┼───┼───┤
Row 1  │ 4 │ 5 │ 6 │
       ├───┼───┼───┤
Row 2  │ 7 │ 8 │ 9 │
       └───┴───┴───┘

matrix[1][2] = 6  (row 1, column 2)
```

---

## 2.2 Creating 2D Lists

### Method 1: Direct Definition

```python
# A 2x3 matrix (2 rows, 3 columns)
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]
```

### Method 2: Using Loops

```python
# Create a 3x4 matrix of zeros
rows = 3
cols = 4

matrix = []
for i in range(rows):
    row = []
    for j in range(cols):
        row.append(0)
    matrix.append(row)

print(matrix)
# [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
```

### Method 3: List Comprehension (Pythonic Way)

```python
# Create a 3x4 matrix of zeros
rows = 3
cols = 4

matrix = [[0 for _ in range(cols)] for _ in range(rows)]
print(matrix)
# [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
```

### ⚠️ Common Mistake: Shared References

```python
# WRONG - all rows share the same list!
matrix = [[0] * 4] * 3
matrix[0][0] = 99
print(matrix)
# [[99, 0, 0, 0], [99, 0, 0, 0], [99, 0, 0, 0]]  # All rows changed!

# CORRECT - each row is independent
matrix = [[0] * 4 for _ in range(3)]
matrix[0][0] = 99
print(matrix)
# [[99, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]  # Only row 0 changed
```

**Why does this happen?**
- `[[0] * 4] * 3` creates ONE list `[0, 0, 0, 0]` and puts 3 references to it
- `[[0] * 4 for _ in range(3)]` creates 3 SEPARATE lists

---

## 2.3 Distance Matrices

### What is a Distance Matrix?

A **distance matrix** stores the distances between all pairs of locations:

```
              To:
           A    B    C    D
       ┌────┬────┬────┬────┐
    A  │  0 │ 10 │ 25 │ 30 │
       ├────┼────┼────┼────┤
From: B │ 10 │  0 │ 15 │ 20 │
       ├────┼────┼────┼────┤
    C  │ 25 │ 15 │  0 │ 12 │
       ├────┼────┼────┼────┤
    D  │ 30 │ 20 │ 12 │  0 │
       └────┴────┴────┴────┘
```

**Properties:**
- `matrix[i][i] = 0` (distance from a place to itself is 0)
- For symmetric distances: `matrix[i][j] == matrix[j][i]`
- For driving, this may not be symmetric (one-way streets!)

### Creating a Distance Matrix Structure

```python
def create_distance_matrix(locations: list[dict]) -> list[list[float]]:
    """
    Create an empty distance matrix for a list of locations.

    Args:
        locations: List of location dictionaries with 'name', 'lat', 'lon'

    Returns:
        2D list initialized with zeros
    """
    n = len(locations)
    return [[0.0 for _ in range(n)] for _ in range(n)]


# Example locations
locations = [
    {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
    {"name": "Taipei Main Station", "lat": 25.0478, "lon": 121.5170},
    {"name": "National Palace Museum", "lat": 25.1024, "lon": 121.5485},
    {"name": "Shilin Night Market", "lat": 25.0881, "lon": 121.5240}
]

# Create empty matrix
matrix = create_distance_matrix(locations)

# Print dimensions
print(f"Matrix size: {len(matrix)} x {len(matrix[0])}")
# Matrix size: 4 x 4
```

---

## 2.4 Building a Distance Matrix with Haversine

### Review: The Haversine Formula

The Haversine formula calculates the straight-line distance between two points on Earth:

```python
import math

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
    # Earth's radius in kilometers
    R = 6371.0

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


# Example
dist = haversine_distance(25.0330, 121.5654, 25.0478, 121.5170)
print(f"Straight-line distance: {dist:.2f} km")
```

### Filling the Distance Matrix

```python
def build_haversine_matrix(locations: list[dict]) -> list[list[float]]:
    """
    Build a distance matrix using Haversine (straight-line) distances.

    Args:
        locations: List of location dicts with 'lat' and 'lon'

    Returns:
        2D list of distances in kilometers
    """
    n = len(locations)
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:  # Skip diagonal (distance to self = 0)
                dist = haversine_distance(
                    locations[i]["lat"], locations[i]["lon"],
                    locations[j]["lat"], locations[j]["lon"]
                )
                matrix[i][j] = round(dist, 2)

    return matrix


# Build and display the matrix
locations = [
    {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
    {"name": "Taipei Main Station", "lat": 25.0478, "lon": 121.5170},
    {"name": "National Palace Museum", "lat": 25.1024, "lon": 121.5485},
    {"name": "Shilin Night Market", "lat": 25.0881, "lon": 121.5240}
]

haversine_matrix = build_haversine_matrix(locations)

# Pretty print
print("Haversine Distance Matrix (km):")
print("        ", end="")
for loc in locations:
    print(f"{loc['name'][:8]:>10}", end="")
print()

for i, row in enumerate(haversine_matrix):
    print(f"{locations[i]['name'][:8]:>8}", end="")
    for dist in row:
        print(f"{dist:>10.2f}", end="")
    print()
```

---

## 2.5 Building a Distance Matrix with OSRM

### Single Route Request

```python
import requests
import time

def get_osrm_distance(start: dict, end: dict) -> tuple[float, float]:
    """
    Get driving distance and duration between two points using OSRM.

    Args:
        start: Dict with 'lat' and 'lon'
        end: Dict with 'lat' and 'lon'

    Returns:
        Tuple of (distance_km, duration_minutes)
    """
    coords = f"{start['lon']},{start['lat']};{end['lon']},{end['lat']}"
    url = f"https://router.project-osrm.org/route/v1/driving/{coords}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("code") == "Ok" and data.get("routes"):
            route = data["routes"][0]
            distance_km = route["distance"] / 1000
            duration_min = route["duration"] / 60
            return (round(distance_km, 2), round(duration_min, 1))
    except requests.RequestException as e:
        print(f"Request error: {e}")

    return (0.0, 0.0)
```

### Building the Full Matrix (with Rate Limiting)

```python
def build_osrm_matrix(locations: list[dict],
                      delay: float = 1.0) -> tuple[list[list[float]], list[list[float]]]:
    """
    Build distance and duration matrices using OSRM.

    Args:
        locations: List of location dicts with 'lat', 'lon', 'name'
        delay: Seconds to wait between API calls

    Returns:
        Tuple of (distance_matrix, duration_matrix)
    """
    n = len(locations)
    distance_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    duration_matrix = [[0.0 for _ in range(n)] for _ in range(n)]

    total_requests = n * (n - 1)  # Excluding diagonal
    current = 0

    for i in range(n):
        for j in range(n):
            if i != j:
                current += 1
                print(f"Fetching route {current}/{total_requests}: "
                      f"{locations[i]['name']} -> {locations[j]['name']}")

                distance, duration = get_osrm_distance(locations[i], locations[j])
                distance_matrix[i][j] = distance
                duration_matrix[i][j] = duration

                time.sleep(delay)  # Rate limiting

    return distance_matrix, duration_matrix
```

### A More Efficient Approach: OSRM Table Service

OSRM has a special "table" service that can compute all distances at once:

```python
def get_osrm_table(locations: list[dict]) -> tuple[list[list[float]], list[list[float]]]:
    """
    Get distance/duration matrix using OSRM's table service.

    This is much more efficient than making individual route requests!

    Args:
        locations: List of location dicts with 'lat' and 'lon'

    Returns:
        Tuple of (distance_matrix in km, duration_matrix in minutes)
    """
    # Build coordinates string
    coords = ";".join(f"{loc['lon']},{loc['lat']}" for loc in locations)

    url = f"https://router.project-osrm.org/table/v1/driving/{coords}"
    params = {
        "annotations": "distance,duration"  # Get both distance and duration
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()

        if data.get("code") == "Ok":
            # Convert distances from meters to km
            distances = data.get("distances", [])
            distance_km = [[d / 1000 if d else 0 for d in row] for row in distances]

            # Convert durations from seconds to minutes
            durations = data.get("durations", [])
            duration_min = [[d / 60 if d else 0 for d in row] for row in durations]

            return distance_km, duration_min
    except requests.RequestException as e:
        print(f"Request error: {e}")

    # Return empty matrices on failure
    n = len(locations)
    empty = [[0.0 for _ in range(n)] for _ in range(n)]
    return empty, empty


# Usage - ONE request instead of n*(n-1) requests!
locations = [
    {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
    {"name": "Taipei Main Station", "lat": 25.0478, "lon": 121.5170},
    {"name": "National Palace Museum", "lat": 25.1024, "lon": 121.5485},
    {"name": "Shilin Night Market", "lat": 25.0881, "lon": 121.5240}
]

distance_matrix, duration_matrix = get_osrm_table(locations)
```

---

## 2.6 Comparing Haversine vs OSRM Distances

### Building the Comparison

```python
def compare_distances(locations: list[dict]) -> None:
    """
    Compare Haversine (straight-line) vs OSRM (driving) distances.

    Args:
        locations: List of location dicts
    """
    print("Building Haversine matrix...")
    haversine = build_haversine_matrix(locations)

    print("Fetching OSRM matrix...")
    osrm_dist, osrm_dur = get_osrm_table(locations)

    print("\n" + "="*70)
    print("DISTANCE COMPARISON: Haversine (straight-line) vs OSRM (driving)")
    print("="*70)

    for i in range(len(locations)):
        for j in range(len(locations)):
            if i < j:  # Only show each pair once
                h_dist = haversine[i][j]
                o_dist = osrm_dist[i][j]
                o_dur = osrm_dur[i][j]

                if h_dist > 0:
                    ratio = o_dist / h_dist
                else:
                    ratio = 0

                print(f"\n{locations[i]['name']} → {locations[j]['name']}")
                print(f"  Haversine:     {h_dist:>6.2f} km")
                print(f"  OSRM Driving:  {o_dist:>6.2f} km ({o_dur:.0f} min)")
                print(f"  Ratio:         {ratio:>6.2f}x (driving is {ratio:.0%} of straight-line)")


# Run comparison
compare_distances(locations)
```

### Understanding the Ratio

The ratio of driving distance to straight-line distance tells us about road efficiency:

| Ratio | Interpretation |
|-------|----------------|
| 1.0x | Perfect straight road (very rare) |
| 1.2-1.4x | Good direct roads, urban grid |
| 1.5-2.0x | Normal city driving, some detours |
| 2.0-3.0x | Winding roads, geographic obstacles |
| 3.0x+ | Major obstacles (rivers, mountains) |

---

## 2.7 Mini-Exercise 2: Build Your Own Comparison

Create a comparison table for 3-4 locations in your area:

```python
# TODO: Add 3-4 locations you're familiar with
my_locations = [
    {"name": "Location 1", "lat": 0.0, "lon": 0.0},
    {"name": "Location 2", "lat": 0.0, "lon": 0.0},
    {"name": "Location 3", "lat": 0.0, "lon": 0.0},
]

# Build both matrices
haversine = build_haversine_matrix(my_locations)
osrm_dist, osrm_dur = get_osrm_table(my_locations)

# Print comparison
for i in range(len(my_locations)):
    for j in range(len(my_locations)):
        if i < j:
            h = haversine[i][j]
            o = osrm_dist[i][j]
            print(f"{my_locations[i]['name']} -> {my_locations[j]['name']}")
            print(f"  Straight: {h:.2f} km, Driving: {o:.2f} km")
            print(f"  Ratio: {o/h:.2f}x")
```

---

# ☕ 10-Minute Break

Stretch, grab water, check your phone!

---

# Hour 3: Route Geometry and Visualization

## 3.1 Understanding Route Geometry

### What is Route Geometry?

When OSRM returns a route, it includes the **geometry** - the actual shape of the route that can be drawn on a map.

```
Start ●──────┐
             │
             └────●────┐
                       │
                       └──────● End
```

This geometry is represented as a series of coordinates (longitude, latitude pairs) that trace the path.

### Geometry Formats

OSRM supports several geometry formats:

| Format | Parameter | Description |
|--------|-----------|-------------|
| Polyline | `geometries=polyline` | Encoded string (compact) |
| Polyline6 | `geometries=polyline6` | Higher precision encoded |
| GeoJSON | `geometries=geojson` | Standard JSON format |

For learning, we'll use **GeoJSON** because it's human-readable.

### GeoJSON Geometry Structure

```json
{
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [121.5654, 25.0330],  // Point 1: [lon, lat]
            [121.5640, 25.0335],  // Point 2
            [121.5620, 25.0340],  // Point 3
            // ... many more points
            [121.5170, 25.0478]   // Final point
        ]
    }
}
```

**Key Points:**
- `type: "LineString"` means it's a connected series of points
- `coordinates` is an array of `[longitude, latitude]` pairs
- The points are in order from start to end

---

## 3.2 Extracting Route Geometry

### Getting the Full Route Shape

```python
import requests

def get_route_with_geometry(start: dict, end: dict) -> dict | None:
    """
    Get a route with full geometry from OSRM.

    Args:
        start: Dict with 'lat', 'lon', and optionally 'name'
        end: Dict with 'lat', 'lon', and optionally 'name'

    Returns:
        Dict with route info and geometry, or None if failed
    """
    coords = f"{start['lon']},{start['lat']};{end['lon']},{end['lat']}"
    url = f"https://router.project-osrm.org/route/v1/driving/{coords}"

    params = {
        "overview": "full",       # Get complete route shape
        "geometries": "geojson",  # Easy-to-parse format
        "steps": "true"           # Include turn-by-turn directions
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("code") == "Ok" and data.get("routes"):
            route = data["routes"][0]

            return {
                "distance_km": route["distance"] / 1000,
                "duration_min": route["duration"] / 60,
                "geometry": route["geometry"],
                "coordinates": route["geometry"]["coordinates"],
                "num_points": len(route["geometry"]["coordinates"]),
                "legs": route.get("legs", [])
            }
    except requests.RequestException as e:
        print(f"Error: {e}")

    return None


# Example
start = {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654}
end = {"name": "Taipei Main Station", "lat": 25.0478, "lon": 121.5170}

route = get_route_with_geometry(start, end)
if route:
    print(f"Route: {start['name']} → {end['name']}")
    print(f"Distance: {route['distance_km']:.2f} km")
    print(f"Duration: {route['duration_min']:.1f} min")
    print(f"Geometry points: {route['num_points']}")
    print(f"First 3 points: {route['coordinates'][:3]}")
```

---

## 3.3 Working with Route Steps (Turn-by-Turn)

### Understanding Route Steps

Each route leg contains **steps** - individual maneuvers with instructions:

```python
def get_turn_by_turn(start: dict, end: dict) -> list[dict]:
    """
    Get turn-by-turn directions for a route.

    Args:
        start: Starting location
        end: Ending location

    Returns:
        List of step dictionaries with instructions
    """
    coords = f"{start['lon']},{start['lat']};{end['lon']},{end['lat']}"
    url = f"https://router.project-osrm.org/route/v1/driving/{coords}"

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "true"
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if data.get("code") != "Ok":
        return []

    steps = []
    for leg in data["routes"][0].get("legs", []):
        for step in leg.get("steps", []):
            steps.append({
                "instruction": step.get("maneuver", {}).get("type", ""),
                "modifier": step.get("maneuver", {}).get("modifier", ""),
                "name": step.get("name", ""),
                "distance_m": step.get("distance", 0),
                "duration_s": step.get("duration", 0)
            })

    return steps


# Example
directions = get_turn_by_turn(start, end)
print("Turn-by-turn directions:")
for i, step in enumerate(directions[:10], 1):  # First 10 steps
    dist = step['distance_m']
    instr = step['instruction']
    modifier = step['modifier']
    name = step['name'] or "(unnamed road)"

    direction = f"{instr}"
    if modifier:
        direction += f" {modifier}"

    print(f"{i:2}. {direction:20} onto {name:30} ({dist:>5.0f}m)")
```

### Step Maneuver Types

| Type | Description |
|------|-------------|
| `depart` | Start of the route |
| `arrive` | End of the route |
| `turn` | Regular turn (with modifier: left, right, slight left, etc.) |
| `continue` | Continue on the same road |
| `merge` | Merge onto another road |
| `roundabout` | Enter a roundabout |
| `fork` | Road splits |

---

## 3.4 Creating a Simple Text-Based Map

### Visualizing the Route with ASCII

While we can't draw a real map in the terminal, we can create a simple visualization:

```python
def simple_route_visualization(coordinates: list[list[float]],
                               width: int = 60,
                               height: int = 20) -> str:
    """
    Create a simple ASCII visualization of a route.

    Args:
        coordinates: List of [lon, lat] pairs
        width: Character width of output
        height: Character height of output

    Returns:
        ASCII art string representing the route
    """
    if not coordinates:
        return "No route data"

    # Extract lon/lat bounds
    lons = [c[0] for c in coordinates]
    lats = [c[1] for c in coordinates]

    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)

    # Handle edge case of straight line
    lon_range = max_lon - min_lon or 0.001
    lat_range = max_lat - min_lat or 0.001

    # Create empty grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    # Plot each point
    for i, (lon, lat) in enumerate(coordinates):
        # Normalize to grid coordinates
        x = int((lon - min_lon) / lon_range * (width - 1))
        y = int((max_lat - lat) / lat_range * (height - 1))  # Flip y-axis

        # Clamp to grid bounds
        x = max(0, min(width - 1, x))
        y = max(0, min(height - 1, y))

        # Mark the point
        if i == 0:
            grid[y][x] = 'S'  # Start
        elif i == len(coordinates) - 1:
            grid[y][x] = 'E'  # End
        else:
            grid[y][x] = '·'

    # Convert grid to string
    lines = [''.join(row) for row in grid]

    # Add border
    border = '+' + '-' * width + '+'
    lines = [border] + ['|' + line + '|' for line in lines] + [border]

    return '\n'.join(lines)


# Example usage
route = get_route_with_geometry(start, end)
if route:
    print(f"\nRoute from {start['name']} to {end['name']}")
    print(f"Distance: {route['distance_km']:.2f} km")
    print()
    print(simple_route_visualization(route['coordinates']))
    print()
    print("S = Start, E = End, · = Route points")
```

---

## 3.5 Saving Route Data

### Exporting to JSON

```python
import json

def save_route_to_json(route_data: dict, filename: str) -> None:
    """
    Save route data to a JSON file.

    Args:
        route_data: Route dictionary with geometry
        filename: Output file path
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(route_data, f, indent=2, ensure_ascii=False)
    print(f"Route saved to {filename}")


def load_route_from_json(filename: str) -> dict:
    """
    Load route data from a JSON file.

    Args:
        filename: Input file path

    Returns:
        Route dictionary
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
```

### Exporting to GeoJSON (for Maps)

GeoJSON is a standard format that can be opened in many mapping tools:

```python
def route_to_geojson(route_data: dict,
                     start_name: str = "Start",
                     end_name: str = "End") -> dict:
    """
    Convert route data to a full GeoJSON FeatureCollection.

    This can be loaded into tools like geojson.io, QGIS, or Leaflet.

    Args:
        route_data: Route dict with 'coordinates', 'distance_km', 'duration_min'
        start_name: Name for the start point
        end_name: Name for the end point

    Returns:
        GeoJSON FeatureCollection dict
    """
    coords = route_data.get("coordinates", [])

    features = [
        # The route line
        {
            "type": "Feature",
            "properties": {
                "name": "Route",
                "distance_km": route_data.get("distance_km", 0),
                "duration_min": route_data.get("duration_min", 0)
            },
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            }
        },
        # Start point
        {
            "type": "Feature",
            "properties": {"name": start_name, "marker-color": "#00ff00"},
            "geometry": {
                "type": "Point",
                "coordinates": coords[0] if coords else [0, 0]
            }
        },
        # End point
        {
            "type": "Feature",
            "properties": {"name": end_name, "marker-color": "#ff0000"},
            "geometry": {
                "type": "Point",
                "coordinates": coords[-1] if coords else [0, 0]
            }
        }
    ]

    return {
        "type": "FeatureCollection",
        "features": features
    }


# Save as GeoJSON file
route = get_route_with_geometry(start, end)
if route:
    geojson = route_to_geojson(route, start['name'], end['name'])

    with open("my_route.geojson", 'w') as f:
        json.dump(geojson, f, indent=2)

    print("Saved to my_route.geojson")
    print("Open this file at https://geojson.io to see it on a map!")
```

---

## 3.6 Building a Complete Route Comparison Tool

### The Route Analyzer Class

```python
import requests
import time
import math
import json
from typing import Optional

class RouteAnalyzer:
    """
    A tool for analyzing and comparing routes between locations.

    Features:
    - Calculate straight-line (Haversine) distances
    - Get actual driving distances from OSRM
    - Compare and visualize differences
    - Export results to various formats
    """

    OSRM_BASE = "https://router.project-osrm.org"

    def __init__(self, locations: list[dict]):
        """
        Initialize with a list of locations.

        Args:
            locations: List of dicts with 'name', 'lat', 'lon'
        """
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
        """Build matrix of straight-line distances."""
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
        """Build matrices using OSRM table service."""
        coords = ";".join(f"{loc['lon']},{loc['lat']}" for loc in self.locations)
        url = f"{self.OSRM_BASE}/table/v1/driving/{coords}"

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
            n = len(self.locations)
            self.osrm_distance_matrix = [[0.0]*n for _ in range(n)]
            self.osrm_duration_matrix = [[0.0]*n for _ in range(n)]

        return self.osrm_distance_matrix, self.osrm_duration_matrix

    def get_route(self, from_idx: int, to_idx: int) -> Optional[dict]:
        """Get detailed route between two locations by index."""
        start = self.locations[from_idx]
        end = self.locations[to_idx]

        coords = f"{start['lon']},{start['lat']};{end['lon']},{end['lat']}"
        url = f"{self.OSRM_BASE}/route/v1/driving/{coords}"

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
                "distance_km": round(route["distance"]/1000, 2),
                "duration_min": round(route["duration"]/60, 1),
                "geometry": route["geometry"],
                "coordinates": route["geometry"]["coordinates"],
                "steps": route["legs"][0]["steps"] if route.get("legs") else []
            }
        return None

    def analyze_all(self) -> dict:
        """Run full analysis and return comprehensive results."""
        print("Building Haversine matrix...")
        self.build_haversine_matrix()

        print("Fetching OSRM matrix...")
        self.build_osrm_matrix()

        results = {
            "locations": self.locations,
            "haversine_matrix": self.haversine_matrix,
            "osrm_distance_matrix": self.osrm_distance_matrix,
            "osrm_duration_matrix": self.osrm_duration_matrix,
            "comparisons": []
        }

        # Build pair comparisons
        n = len(self.locations)
        for i in range(n):
            for j in range(n):
                if i < j:
                    h_dist = self.haversine_matrix[i][j]
                    o_dist = self.osrm_distance_matrix[i][j]
                    o_dur = self.osrm_duration_matrix[i][j]
                    ratio = o_dist / h_dist if h_dist > 0 else 0

                    results["comparisons"].append({
                        "from": self.locations[i]['name'],
                        "to": self.locations[j]['name'],
                        "haversine_km": h_dist,
                        "driving_km": o_dist,
                        "driving_min": o_dur,
                        "ratio": round(ratio, 2)
                    })

        return results

    def print_comparison_table(self) -> None:
        """Print a formatted comparison table."""
        if not self.haversine_matrix or not self.osrm_distance_matrix:
            print("Run analyze_all() first!")
            return

        print("\n" + "="*80)
        print("ROUTE COMPARISON: Straight-Line vs Driving Distance")
        print("="*80)

        n = len(self.locations)
        for i in range(n):
            for j in range(n):
                if i < j:
                    h = self.haversine_matrix[i][j]
                    d = self.osrm_distance_matrix[i][j]
                    t = self.osrm_duration_matrix[i][j]
                    ratio = d/h if h > 0 else 0

                    print(f"\n{self.locations[i]['name']} → {self.locations[j]['name']}")
                    print(f"  Straight-line: {h:>7.2f} km")
                    print(f"  Driving:       {d:>7.2f} km  ({t:.0f} min)")
                    print(f"  Ratio:         {ratio:>7.2f}x")

    def export_geojson(self, filename: str) -> None:
        """Export all routes as a GeoJSON file."""
        features = []

        # Add location markers
        for loc in self.locations:
            features.append({
                "type": "Feature",
                "properties": {"name": loc['name'], "marker-color": "#0066ff"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [loc['lon'], loc['lat']]
                }
            })

        geojson = {"type": "FeatureCollection", "features": features}

        with open(filename, 'w') as f:
            json.dump(geojson, f, indent=2)

        print(f"Exported to {filename}")


# Usage example
if __name__ == "__main__":
    locations = [
        {"name": "Taipei 101", "lat": 25.0330, "lon": 121.5654},
        {"name": "Taipei Main Station", "lat": 25.0478, "lon": 121.5170},
        {"name": "National Palace Museum", "lat": 25.1024, "lon": 121.5485},
    ]

    analyzer = RouteAnalyzer(locations)
    results = analyzer.analyze_all()
    analyzer.print_comparison_table()
```

---

## 3.7 Mini-Exercise 3: Build Your Route Analyzer

Complete this exercise to build your own route analyzer:

```python
# TODO: Create a RouteAnalyzer with at least 4 locations from your city

my_locations = [
    # Add your locations here
    {"name": "Place 1", "lat": 0.0, "lon": 0.0},
    {"name": "Place 2", "lat": 0.0, "lon": 0.0},
    {"name": "Place 3", "lat": 0.0, "lon": 0.0},
    {"name": "Place 4", "lat": 0.0, "lon": 0.0},
]

analyzer = RouteAnalyzer(my_locations)
results = analyzer.analyze_all()
analyzer.print_comparison_table()

# Bonus: Get detailed route between two places
route = analyzer.get_route(0, 1)
if route:
    print(f"\nDetailed route: {route['from']} → {route['to']}")
    print(f"Distance: {route['distance_km']} km")
    print(f"Duration: {route['duration_min']} min")
    print(f"Route points: {len(route['coordinates'])}")
```

---

## 3.8 Summary: Key Takeaways

### Routing Concepts

1. **Straight-line distance** (Haversine) is always shorter than actual travel distance
2. **OSRM** provides free, open-source routing based on OpenStreetMap
3. **Driving distance** accounts for roads, one-way streets, and geography
4. **Travel time** depends on road types, speed limits, and conditions

### OSRM API

| Service | Endpoint | Use Case |
|---------|----------|----------|
| Route | `/route/v1/{profile}/{coords}` | Single route with geometry |
| Table | `/table/v1/{profile}/{coords}` | Distance/duration matrix |

### Key Parameters

```python
# Route request with full options
params = {
    "overview": "full",        # full, simplified, or false
    "geometries": "geojson",   # geojson, polyline, or polyline6
    "steps": "true",           # Include turn-by-turn
    "annotations": "true"      # Include speed, duration per segment
}
```

### 2D Lists (Matrices)

```python
# Create safely
matrix = [[0 for _ in range(cols)] for _ in range(rows)]

# Access
value = matrix[row][col]

# Distance matrix: matrix[i][j] = distance from location i to j
```

### Best Practices

1. **Rate limiting**: Add delays between requests to the public OSRM server
2. **Use the table service** for multiple locations (1 request vs N²)
3. **Cache results** to avoid repeated API calls
4. **Handle errors** - network requests can fail
5. **Validate coordinates** - longitude first!

---

## 3.9 Homework Assignments

### Assignment 1: Delivery Route Analyzer (Basic)
Create a tool that takes a list of delivery addresses and:
1. Calculates straight-line distances between all pairs
2. Fetches actual driving distances using OSRM
3. Identifies which routes have the biggest difference

### Assignment 2: Walking vs Driving Comparison (Intermediate)
Modify the RouteAnalyzer to compare walking and driving:
- Use `walking` and `driving` profiles
- Calculate when walking might be faster (short distances in traffic)
- Present the comparison in a clear table

### Assignment 3: Route Visualization (Advanced)
Export routes to GeoJSON and:
1. Include multiple routes in one file
2. Color-code routes by efficiency (ratio of driving to straight-line)
3. Add popup information for each segment
4. Open in geojson.io to verify

---

## Additional Resources

### Documentation
- [OSRM API Documentation](http://project-osrm.org/docs/v5.24.0/api/)
- [OSRM GitHub Repository](https://github.com/Project-OSRM/osrm-backend)
- [GeoJSON Specification](https://geojson.org/)

### Tools
- [geojson.io](https://geojson.io) - View GeoJSON on a map
- [OSRM Demo](https://map.project-osrm.org) - Interactive routing demo

### Further Reading
- [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Contraction Hierarchies](https://en.wikipedia.org/wiki/Contraction_hierarchies)

---

## Next Week Preview

**Week 9: Advanced Topics**
- Building on routing and geocoding knowledge
- Performance optimization
- Caching strategies
- Production considerations

---

*End of Week 8 Lecture*
