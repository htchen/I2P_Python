# Week 8: OSRM API (Real Routing)

**Phase 2: The API & The Cloud** — "Fetching the World"

---

## Concepts
- 2D Lists (Matrices)
- Cost comparison
- Real-world routing vs straight-line distance

---

## Project Task

Compare "Haversine distance" (straight line) vs "OSRM Distance" (walking time). Fetch route geometry (JSON) from the OSRM public demo server.

### Straight Line vs Real Route

```python
import requests
from math import radians, sin, cos, sqrt, asin

def haversine(coord1, coord2):
    """Straight-line distance in km."""
    R = 6371
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return R * 2 * asin(sqrt(a))


def get_walking_route(coord1, coord2):
    """Get real walking distance and time from OSRM."""
    # IMPORTANT: OSRM uses longitude,latitude order!
    start = f"{coord1[1]},{coord1[0]}"
    end = f"{coord2[1]},{coord2[0]}"

    url = f"https://router.project-osrm.org/route/v1/foot/{start};{end}"

    response = requests.get(url, params={
        "overview": "full",
        "geometries": "geojson"
    })

    data = response.json()
    route = data["routes"][0]

    return {
        "distance_km": route["distance"] / 1000,
        "duration_min": route["duration"] / 60,
        "geometry": route["geometry"]
    }


# Compare!
start = (25.0330, 121.5654)  # Taipei 101
end = (25.0478, 121.5170)    # Taipei Main Station

straight = haversine(start, end)
real = get_walking_route(start, end)

print(f"Straight line: {straight:.2f} km")
print(f"Walking route: {real['distance_km']:.2f} km")
print(f"Walking time:  {real['duration_min']:.1f} minutes")
```

### Building a Distance Matrix

```python
def build_distance_matrix(places):
    """
    Build a matrix of walking times between all places.
    Returns a 2D list where matrix[i][j] is the time from place i to j.
    """
    n = len(places)
    matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                route = get_walking_route(
                    places[i]["coords"],
                    places[j]["coords"]
                )
                matrix[i][j] = route["duration_min"]
                time.sleep(0.5)  # Rate limiting

    return matrix


# Usage
places = [
    {"name": "A", "coords": (25.033, 121.565)},
    {"name": "B", "coords": (25.047, 121.517)},
    {"name": "C", "coords": (25.041, 121.551)},
]

matrix = build_distance_matrix(places)
# matrix[0][1] = walking time from A to B
```

---

## Lab Exercises

See the `lectures/lecture_exercises/` folder for this week's exercises.

## Lecture Materials

See the `lectures/` folder for slides and examples.
