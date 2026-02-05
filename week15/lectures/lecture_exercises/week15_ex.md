# Week 15 Lab: Final Integration Sprint

## Lab Overview

In this lab, you'll build the complete Smart City Navigator application by integrating all the components you've learned throughout the course. This is the capstone project that brings together APIs, Flask, and Folium maps.

**Time:** 3 hours

**Prerequisites:**
- All required packages installed (`pip install flask folium requests`)
- Understanding of Nominatim API (geocoding)
- Understanding of OSRM API (routing)
- Flask web development basics
- Folium map creation

---

## Setup

```bash
# Install required packages
pip install flask folium requests

# Create project directory
mkdir smart_city_navigator
cd smart_city_navigator

# Create directory structure
mkdir -p templates static/css utils
touch app.py config.py requirements.txt
touch utils/__init__.py utils/geocoding.py utils/routing.py utils/mapping.py
touch templates/base.html templates/index.html templates/results.html
```

---

## Exercise 1: Geocoding Module (20 minutes)

### Objective
Create a reusable geocoding module that wraps the Nominatim API.

### Task
Implement the `Geocoder` class in `utils/geocoding.py`.

### Starter Code

```python
# utils/geocoding.py
"""Nominatim API wrapper for geocoding operations."""

import requests
import time
from functools import wraps


class GeocodingError(Exception):
    """Exception raised for geocoding errors."""
    pass


def rate_limit(min_interval=1.0):
    """
    Decorator to enforce minimum time between API calls.

    Args:
        min_interval: Minimum seconds between calls
    """
    # TODO: Implement rate limiting
    # Hint: Track last call time and sleep if needed
    pass


class Geocoder:
    """Wrapper for Nominatim geocoding API."""

    def __init__(self, user_agent="SmartCityNavigator/1.0"):
        self.base_url = "https://nominatim.openstreetmap.org"
        self.headers = {"User-Agent": user_agent}

    def geocode(self, address):
        """
        Convert address to coordinates.

        Args:
            address: Address string to geocode

        Returns:
            dict with 'lat', 'lon', 'display_name'

        Raises:
            GeocodingError: If geocoding fails
        """
        # TODO: Implement geocoding
        # 1. Make request to Nominatim /search endpoint
        # 2. Parse response and extract coordinates
        # 3. Handle errors appropriately
        pass

    def search_nearby(self, lat, lon, query, radius=1000):
        """
        Search for places near a location.

        Args:
            lat: Latitude
            lon: Longitude
            query: Search query (e.g., "cafe")
            radius: Search radius in meters

        Returns:
            List of place dictionaries
        """
        # TODO: Implement nearby search
        # 1. Calculate bounding box from radius
        # 2. Make request with viewbox parameter
        # 3. Parse and return results
        pass
```

### Requirements

1. Rate limit decorator that sleeps between API calls
2. `geocode()` method that converts addresses to coordinates
3. `search_nearby()` method that finds places within a radius
4. Proper error handling with custom `GeocodingError`
5. Respect Nominatim's usage policy (1 request per second)

### Test Your Implementation

```python
# test_geocoding.py
from utils.geocoding import Geocoder, GeocodingError

geocoder = Geocoder()

# Test 1: Geocode a known location
try:
    result = geocoder.geocode("Taipei 101")
    print(f"Taipei 101: [{result['lat']}, {result['lon']}]")
    assert abs(result['lat'] - 25.033) < 0.01
    print("Test 1 passed!")
except GeocodingError as e:
    print(f"Test 1 failed: {e}")

# Test 2: Search nearby
try:
    places = geocoder.search_nearby(25.033, 121.565, "cafe")
    print(f"Found {len(places)} cafes")
    assert len(places) > 0
    print("Test 2 passed!")
except GeocodingError as e:
    print(f"Test 2 failed: {e}")

# Test 3: Handle non-existent location
try:
    geocoder.geocode("nonexistent_place_xyz123")
    print("Test 3 failed: Should have raised error")
except GeocodingError:
    print("Test 3 passed!")
```

---

## Exercise 2: Routing Module (20 minutes)

### Objective
Create a routing module that wraps the OSRM API.

### Task
Implement the `Router` class in `utils/routing.py`.

### Starter Code

```python
# utils/routing.py
"""OSRM API wrapper for routing operations."""

import requests
import time


class RoutingError(Exception):
    """Exception raised for routing errors."""
    pass


class Router:
    """Wrapper for OSRM routing API."""

    def __init__(self, base_url="http://router.project-osrm.org"):
        self.base_url = base_url

    def get_route(self, start, end, mode="foot"):
        """
        Get route between two points.

        Args:
            start: (lat, lon) tuple for start point
            end: (lat, lon) tuple for end point
            mode: Travel mode ('foot', 'car', 'bike')

        Returns:
            dict with 'distance' (meters), 'duration' (seconds), 'geometry'
        """
        # TODO: Implement route calculation
        # Note: OSRM expects coordinates as lon,lat (not lat,lon!)
        # 1. Build URL with coordinates
        # 2. Request route with overview=full, geometries=geojson
        # 3. Parse response
        # 4. Convert geometry coordinates from [lon,lat] to [lat,lon]
        pass

    def get_routes_to_places(self, origin, places, mode="foot"):
        """
        Get routes from origin to multiple places.

        Args:
            origin: (lat, lon) tuple
            places: List of place dicts with 'lat', 'lon'
            mode: Travel mode

        Returns:
            List of places with added route information
        """
        # TODO: Implement batch routing
        # Add 'duration_min', 'distance_m', 'route_geometry' to each place
        pass
```

### Requirements

1. `get_route()` calculates route between two points
2. Returns distance in meters, duration in seconds, and route geometry
3. Geometry coordinates converted to `[lat, lon]` format for Folium
4. `get_routes_to_places()` adds route info to multiple places
5. Handles routing failures gracefully

### Test Your Implementation

```python
# test_routing.py
from utils.routing import Router, RoutingError

router = Router()

# Test 1: Get single route
try:
    route = router.get_route(
        (25.0174, 121.5405),  # NTU
        (25.0330, 121.5654)   # Taipei 101
    )
    print(f"Distance: {route['distance']:.0f}m")
    print(f"Duration: {route['duration']/60:.1f} min")
    print(f"Geometry points: {len(route['geometry'])}")
    assert route['distance'] > 0
    print("Test 1 passed!")
except RoutingError as e:
    print(f"Test 1 failed: {e}")

# Test 2: Batch routing
places = [
    {"name": "Place A", "lat": 25.020, "lon": 121.540},
    {"name": "Place B", "lat": 25.025, "lon": 121.550},
]

try:
    results = router.get_routes_to_places((25.0174, 121.5405), places)
    for p in results:
        print(f"{p['name']}: {p['duration_min']:.1f} min")
    print("Test 2 passed!")
except Exception as e:
    print(f"Test 2 failed: {e}")
```

---

## Exercise 3: Map Generation Module (20 minutes)

### Objective
Create a module for generating Folium maps with places and routes.

### Task
Implement map generation functions in `utils/mapping.py`.

### Starter Code

```python
# utils/mapping.py
"""Folium map generation utilities."""

import folium


# Category styles for markers
CATEGORY_STYLES = {
    "cafe": {"icon": "coffee", "color": "orange"},
    "restaurant": {"icon": "cutlery", "color": "red"},
    "park": {"icon": "tree", "color": "green"},
    "museum": {"icon": "university", "color": "blue"},
    "default": {"icon": "info", "color": "gray"},
}


def create_map(center, zoom=14, tiles="CartoDB positron"):
    """
    Create a base Folium map.

    Args:
        center: (lat, lon) tuple for map center
        zoom: Initial zoom level
        tiles: Map tile provider

    Returns:
        folium.Map object
    """
    # TODO: Create and return a Folium map
    pass


def add_start_marker(m, location, name="Start"):
    """
    Add a start marker to the map.

    Args:
        m: Folium map object
        location: dict with 'lat', 'lon'
        name: Marker name
    """
    # TODO: Add green home marker for start location
    pass


def add_place_marker(m, place, rank, category="default"):
    """
    Add a place marker with popup and route line.

    Args:
        m: Folium map object
        place: dict with 'name', 'lat', 'lon', 'duration_min'
        rank: Place ranking number
        category: Category for icon style
    """
    # TODO: Add marker with appropriate icon color
    # Include popup with name and walking time
    pass


def add_route_line(m, geometry, color="blue", weight=3):
    """
    Add a route line to the map.

    Args:
        m: Folium map object
        geometry: List of [lat, lon] coordinates
        color: Line color
        weight: Line thickness
    """
    # TODO: Add PolyLine for the route
    pass


def generate_results_map(start, places, category="cafe"):
    """
    Generate complete results map.

    Args:
        start: dict with 'lat', 'lon', 'display_name'
        places: List of place dicts with routes
        category: Category for styling

    Returns:
        HTML string of the map
    """
    # TODO: Create complete map with all elements
    # 1. Create base map
    # 2. Add start marker
    # 3. Add route lines and place markers
    # 4. Fit bounds to show all markers
    # 5. Return HTML string
    pass
```

### Requirements

1. `create_map()` creates base Folium map with specified options
2. `add_start_marker()` adds green home marker
3. `add_place_marker()` adds category-styled marker with popup
4. `add_route_line()` draws route on map
5. `generate_results_map()` combines all elements

### Test Your Implementation

```python
# test_mapping.py
from utils.mapping import generate_results_map

start = {
    "lat": 25.0174,
    "lon": 121.5405,
    "display_name": "National Taiwan University"
}

places = [
    {
        "name": "Cafe A",
        "lat": 25.015,
        "lon": 121.534,
        "duration_min": 5.2,
        "distance_m": 420,
        "route_geometry": [[25.0174, 121.5405], [25.016, 121.537], [25.015, 121.534]]
    },
    {
        "name": "Cafe B",
        "lat": 25.020,
        "lon": 121.542,
        "duration_min": 8.1,
        "distance_m": 680,
        "route_geometry": [[25.0174, 121.5405], [25.018, 121.540], [25.020, 121.542]]
    },
]

# Generate map
html = generate_results_map(start, places, "cafe")

# Save to file
with open("test_map.html", "w") as f:
    f.write(f"<html><body>{html}</body></html>")

print("Map saved to test_map.html - open in browser to verify")
```

---

## Exercise 4: Flask Application (30 minutes)

### Objective
Build the main Flask application that integrates all modules.

### Task
Implement the Flask routes in `app.py`.

### Starter Code

```python
# app.py
"""Smart City Navigator - Main Flask Application."""

from flask import Flask, render_template, request, flash, redirect, url_for

# Import your modules
from utils.geocoding import Geocoder, GeocodingError
from utils.routing import Router, RoutingError
from utils.mapping import generate_results_map

app = Flask(__name__)
app.secret_key = "your-secret-key-change-this"

# Initialize API clients
geocoder = Geocoder(user_agent="SmartCityNavigator/1.0 (student@university.edu)")
router = Router()

# Configuration
CATEGORIES = {
    "cafe": "Cafe",
    "restaurant": "Restaurant",
    "park": "Park",
    "museum": "Museum",
}
MAX_RESULTS = 10


@app.route("/")
def index():
    """
    Home page with search form.
    """
    # TODO: Render index.html with categories
    pass


@app.route("/search", methods=["POST"])
def search():
    """
    Process search and show results.
    """
    # TODO: Implement search flow
    # 1. Get form data (location, category, max_time)
    # 2. Validate input
    # 3. Geocode starting location
    # 4. Search for nearby places
    # 5. Get walking routes to each place
    # 6. Filter by walking time
    # 7. Sort by duration
    # 8. Generate map
    # 9. Render results.html
    pass


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template("error.html", error_code=404, message="Page not found"), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return render_template("error.html", error_code=500, message="Server error"), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

### Template Files

Create the following templates:

**templates/base.html** - Base template with common layout
**templates/index.html** - Search form
**templates/results.html** - Results display with map
**templates/error.html** - Error page

### Requirements

1. Home page displays search form
2. Search route validates input and handles errors
3. Results page shows map and place list
4. Error handling with user-friendly messages
5. Flash messages for validation errors

### Test Your Application

```bash
# Run the application
python app.py

# Visit in browser
# http://localhost:5000

# Test search:
# 1. Enter "National Taiwan University"
# 2. Select "Cafe"
# 3. Set max time to 10 minutes
# 4. Click search
# 5. Verify map and results display
```

---

## Exercise 5: HTML Templates (25 minutes)

### Objective
Create the HTML templates for the application.

### Task
Implement the templates in the `templates/` directory.

### base.html

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Smart City Navigator{% endblock %}</title>
    <style>
        /* TODO: Add your CSS styles here */
        /* Requirements:
           - Clean, modern design
           - Responsive layout
           - Header with gradient background
           - Card-style containers
           - Form styling
        */
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <!-- TODO: Add navigation -->
    </header>

    <main>
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
        <div class="flash-messages">
            {% for category, message in messages %}
            <div class="flash {{ category }}">{{ message }}</div>
            {% endfor %}
        </div>
        {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </main>

    <footer>
        <!-- TODO: Add footer -->
    </footer>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

### index.html

```html
<!-- templates/index.html -->
{% extends "base.html" %}

{% block content %}
<div class="card">
    <h2>Find Places Near You</h2>

    <form method="POST" action="/search">
        <!-- TODO: Add form fields -->
        <!-- Requirements:
             - Location input (text)
             - Category select (from categories dict)
             - Max walking time input (number)
             - Submit button
        -->
    </form>
</div>
{% endblock %}
```

### results.html

```html
<!-- templates/results.html -->
{% extends "base.html" %}

{% block content %}
<div class="results-layout">
    <div class="sidebar">
        <!-- TODO: Add search summary -->
        <!-- Show: location, category, max_time, places count -->

        <!-- TODO: Add place list -->
        <!-- Show: ranked list of places with name and walking time -->
    </div>

    <div class="map-container">
        <!-- TODO: Embed the map -->
        <!-- Use: {{ map_html | safe }} -->
    </div>
</div>
{% endblock %}
```

### Requirements

1. Responsive design that works on mobile
2. Clean form styling with proper labels
3. Results layout with sidebar and map
4. Place list with rank numbers and walking times
5. Search summary showing parameters used

---

## Exercise 6: Error Handling (15 minutes)

### Objective
Add comprehensive error handling to the application.

### Task
Improve error handling throughout the application.

### Checklist

- [ ] Validate empty location input
- [ ] Handle geocoding failures (location not found)
- [ ] Handle routing failures (no route available)
- [ ] Handle API timeouts
- [ ] Handle network errors
- [ ] Show user-friendly error messages
- [ ] Log errors for debugging

### Implementation Tips

```python
# In app.py search route:

@app.route("/search", methods=["POST"])
def search():
    location = request.form.get("location", "").strip()

    # Validate input
    if not location:
        flash("Please enter a starting location", "error")
        return redirect(url_for("index"))

    try:
        # Geocode
        start = geocoder.geocode(location)

        # Search nearby
        places = geocoder.search_nearby(start["lat"], start["lon"], category)

        if not places:
            flash(f"No {category}s found near {location}", "warning")
            return redirect(url_for("index"))

        # Get routes
        places_with_routes = router.get_routes_to_places(
            (start["lat"], start["lon"]),
            places
        )

        # ... rest of search logic

    except GeocodingError as e:
        flash(f"Could not find location: {location}", "error")
        return redirect(url_for("index"))

    except RoutingError as e:
        flash("Unable to calculate walking routes. Please try again.", "error")
        return redirect(url_for("index"))

    except Exception as e:
        # Log unexpected errors
        app.logger.error(f"Search error: {e}")
        flash("An unexpected error occurred. Please try again.", "error")
        return redirect(url_for("index"))
```

---

## Exercise 7: Testing (20 minutes)

### Objective
Write tests for your application.

### Task
Create test files for each module.

### Test Structure

```python
# tests/test_app.py
"""Integration tests for Flask application."""

import unittest
from app import app


class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask application."""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_index_page_loads(self):
        """Test that index page loads successfully."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Smart City Navigator", response.data)

    def test_search_without_location(self):
        """Test that search validates empty location."""
        response = self.client.post("/search", data={"location": ""})
        self.assertEqual(response.status_code, 302)  # Redirect

    def test_search_with_valid_input(self):
        """Test search with valid input."""
        response = self.client.post("/search", data={
            "location": "Taipei 101",
            "category": "cafe",
            "max_time": "10"
        })
        # Should return results or redirect with message
        self.assertIn(response.status_code, [200, 302])

    def test_404_page(self):
        """Test 404 error page."""
        response = self.client.get("/nonexistent")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
```

### Run Tests

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_app.py -v
```

---

## Exercise 8: Final Polish (20 minutes)

### Objective
Add finishing touches to make the application production-ready.

### Checklist

- [ ] Add loading indicator for API calls
- [ ] Improve map styling (fit bounds, tooltips)
- [ ] Add "back to search" link on results page
- [ ] Create requirements.txt
- [ ] Add configuration file
- [ ] Write README with setup instructions

### requirements.txt

```txt
flask>=2.0.0
folium>=0.14.0
requests>=2.28.0
```

### Configuration

```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key")
    NOMINATIM_USER_AGENT = os.environ.get(
        "NOMINATIM_USER_AGENT",
        "SmartCityNavigator/1.0"
    )
    MAX_WALK_TIME = 30
    MAX_RESULTS = 10
    DEFAULT_RADIUS = 1000
```

---

## Final Integration Checklist

Before submitting, verify all components work together:

### User Interface
- [ ] Home page loads with search form
- [ ] Form has all required fields
- [ ] Submit button triggers search
- [ ] Error messages display properly
- [ ] Results page shows map and list

### Geocoding
- [ ] Location converts to coordinates
- [ ] Invalid locations show error
- [ ] Nearby search returns results
- [ ] Rate limiting works

### Routing
- [ ] Routes calculate correctly
- [ ] Duration shows in minutes
- [ ] Route geometry displays on map
- [ ] Handles routing failures

### Map
- [ ] Start marker shows (green)
- [ ] Place markers show (category color)
- [ ] Route lines connect places
- [ ] Map fits all markers
- [ ] Popups show details

### Integration
- [ ] Full search flow works
- [ ] Filter by walking time works
- [ ] Sort by duration works
- [ ] Results limited to max count

---

## Summary

Congratulations on completing the Smart City Navigator! You've integrated:

| Week | Component | What You Built |
|------|-----------|----------------|
| 8 | APIs | Nominatim geocoding, OSRM routing |
| 12 | OOP | Geocoder class, Router class |
| 12 | Decorators | Rate limiting |
| 13 | Flask | Web server, routes, templates |
| 14 | Folium | Interactive map visualization |
| 15 | Integration | Complete application |

### Key Skills Demonstrated

1. **API Integration** - Working with external web services
2. **Modular Design** - Separating concerns into reusable modules
3. **Error Handling** - Graceful failure and user feedback
4. **Web Development** - Flask routes, templates, forms
5. **Data Visualization** - Interactive maps with Folium
6. **Testing** - Unit and integration tests

### Next Steps

- Add user authentication
- Store search history
- Implement favorites/bookmarks
- Add more categories
- Optimize for performance
- Deploy to cloud hosting

Great work completing the course project!
