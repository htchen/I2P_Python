# Week 15: Final Integration Sprint

## Lecture Overview (3 Hours)

**Phase 4: The Web Interface** — "Putting It All Together"

### Learning Objectives
By the end of this lecture, students will be able to:
1. Integrate multiple APIs (Nominatim, OSRM) into a single application
2. Build a complete Flask web application with form handling
3. Connect geocoding, routing, and map visualization components
4. Implement proper error handling for external API calls
5. Create a polished user interface for the Smart City Navigator
6. Apply all concepts learned throughout the course

### Prerequisites
- Week 8: APIs and HTTP Requests (Nominatim, OSRM)
- Week 12: OOP & Decorators (Place class, rate limiting)
- Week 13: Flask Web Server (routes, templates)
- Week 14: Folium Maps (markers, routes, layers)

---

# Hour 1: System Architecture and Project Setup

## 1.1 The Big Picture

### Complete System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Smart City Navigator Flow                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   User                                                          │
│    │                                                            │
│    │ 1. Enters location & preferences                           │
│    ▼                                                            │
│   ┌──────────────┐                                              │
│   │  HTML Form   │  "Find cafes within 10 min walk of NTU"     │
│   └──────┬───────┘                                              │
│          │                                                      │
│          │ 2. Submit form                                       │
│          ▼                                                      │
│   ┌──────────────┐                                              │
│   │    Flask     │  Process request, coordinate components      │
│   │   Server     │                                              │
│   └──────┬───────┘                                              │
│          │                                                      │
│          │ 3. Geocode starting location                         │
│          ▼                                                      │
│   ┌──────────────┐                                              │
│   │  Nominatim   │  "NTU" → [25.0174, 121.5405]                │
│   │     API      │                                              │
│   └──────┬───────┘                                              │
│          │                                                      │
│          │ 4. Search for nearby places                          │
│          ▼                                                      │
│   ┌──────────────┐                                              │
│   │  Nominatim   │  Find cafes near coordinates                │
│   │   Search     │                                              │
│   └──────┬───────┘                                              │
│          │                                                      │
│          │ 5. Get walking times to each place                   │
│          ▼                                                      │
│   ┌──────────────┐                                              │
│   │    OSRM      │  Calculate routes & durations               │
│   │     API      │                                              │
│   └──────┬───────┘                                              │
│          │                                                      │
│          │ 6. Filter & sort results                             │
│          ▼                                                      │
│   ┌──────────────┐                                              │
│   │   Business   │  Keep places ≤ 10 min, sort by rating       │
│   │    Logic     │                                              │
│   └──────┬───────┘                                              │
│          │                                                      │
│          │ 7. Generate interactive map                          │
│          ▼                                                      │
│   ┌──────────────┐                                              │
│   │   Folium     │  Create map with markers & routes           │
│   │     Map      │                                              │
│   └──────┬───────┘                                              │
│          │                                                      │
│          │ 8. Return HTML response                              │
│          ▼                                                      │
│   ┌──────────────┐                                              │
│   │  Results     │  Display map & place list to user           │
│   │    Page      │                                              │
│   └──────────────┘                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Input | Output |
|-----------|---------------|-------|--------|
| **HTML Form** | Collect user preferences | User interaction | Form data |
| **Flask** | Coordinate all components | HTTP request | HTTP response |
| **Nominatim** | Convert addresses to coordinates | Address string | Lat/lon |
| **Nominatim** | Find nearby places | Coordinates + query | List of places |
| **OSRM** | Calculate walking routes | Start/end coords | Route + duration |
| **Business Logic** | Filter and sort places | Places list | Filtered list |
| **Folium** | Generate interactive map | Places + routes | HTML map |

## 1.2 Project Structure

### Recommended Directory Layout

```
smart_city_navigator/
├── app.py                 # Main Flask application
├── requirements.txt       # Dependencies
├── config.py              # Configuration settings
├── templates/
│   ├── base.html         # Base template with common layout
│   ├── index.html        # Home page with search form
│   ├── results.html      # Results page with map
│   └── error.html        # Error page
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── main.js       # Optional JavaScript
└── utils/
    ├── __init__.py
    ├── geocoding.py      # Nominatim API wrapper
    ├── routing.py        # OSRM API wrapper
    ├── places.py         # Place class and helpers
    └── mapping.py        # Folium map generation
```

### Configuration File

```python
# config.py
"""Application configuration."""

class Config:
    """Base configuration."""
    # API Settings
    NOMINATIM_URL = "https://nominatim.openstreetmap.org"
    OSRM_URL = "http://router.project-osrm.org"
    USER_AGENT = "SmartCityNavigator/1.0 (student@university.edu)"

    # Rate Limiting
    API_DELAY = 1.0  # seconds between API calls

    # Search Defaults
    DEFAULT_RADIUS = 1000  # meters
    DEFAULT_MAX_RESULTS = 10
    DEFAULT_MAX_WALK_TIME = 15  # minutes

    # Map Settings
    DEFAULT_ZOOM = 14
    MAP_TILES = "CartoDB positron"

    # Categories
    CATEGORIES = {
        "cafe": {"icon": "coffee", "color": "orange", "query": "cafe"},
        "restaurant": {"icon": "cutlery", "color": "red", "query": "restaurant"},
        "park": {"icon": "tree", "color": "green", "query": "park"},
        "museum": {"icon": "university", "color": "blue", "query": "museum"},
        "convenience": {"icon": "shopping-cart", "color": "purple", "query": "convenience store"},
    }
```

## 1.3 API Wrapper Modules

### Geocoding Module

```python
# utils/geocoding.py
"""Nominatim API wrapper for geocoding operations."""

import requests
import time
from functools import wraps

# Rate limiting decorator
def rate_limit(min_interval=1.0):
    """Decorator to enforce minimum time between API calls."""
    last_call = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_call[0] = time.time()
            return result
        return wrapper
    return decorator


class GeocodingError(Exception):
    """Exception raised for geocoding errors."""
    pass


class Geocoder:
    """Wrapper for Nominatim geocoding API."""

    def __init__(self, user_agent="SmartCityNavigator/1.0"):
        self.base_url = "https://nominatim.openstreetmap.org"
        self.headers = {"User-Agent": user_agent}

    @rate_limit(1.0)
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
        url = f"{self.base_url}/search"
        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }

        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            if not data:
                raise GeocodingError(f"Location not found: {address}")

            result = data[0]
            return {
                "lat": float(result["lat"]),
                "lon": float(result["lon"]),
                "display_name": result["display_name"]
            }

        except requests.RequestException as e:
            raise GeocodingError(f"API request failed: {e}")

    @rate_limit(1.0)
    def search_nearby(self, lat, lon, query, radius=1000):
        """
        Search for places near a location.

        Args:
            lat: Latitude
            lon: Longitude
            query: Search query (e.g., "cafe", "restaurant")
            radius: Search radius in meters

        Returns:
            List of place dictionaries
        """
        url = f"{self.base_url}/search"

        # Calculate bounding box from radius
        # Approximate: 1 degree latitude = 111km
        delta = radius / 111000

        params = {
            "q": query,
            "format": "json",
            "limit": 20,
            "viewbox": f"{lon-delta},{lat+delta},{lon+delta},{lat-delta}",
            "bounded": 1
        }

        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            places = []

            for item in data:
                places.append({
                    "name": item.get("name", item.get("display_name", "Unknown")),
                    "lat": float(item["lat"]),
                    "lon": float(item["lon"]),
                    "type": item.get("type", "place"),
                    "display_name": item.get("display_name", "")
                })

            return places

        except requests.RequestException as e:
            raise GeocodingError(f"Search failed: {e}")
```

### Routing Module

```python
# utils/routing.py
"""OSRM API wrapper for routing operations."""

import requests
from functools import wraps
import time


class RoutingError(Exception):
    """Exception raised for routing errors."""
    pass


def rate_limit(min_interval=0.5):
    """Rate limiting decorator."""
    last_call = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_call[0] = time.time()
            return result
        return wrapper
    return decorator


class Router:
    """Wrapper for OSRM routing API."""

    def __init__(self, base_url="http://router.project-osrm.org"):
        self.base_url = base_url

    @rate_limit(0.5)
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
        profile = {
            "foot": "foot",
            "walk": "foot",
            "car": "car",
            "drive": "car",
            "bike": "bike",
            "bicycle": "bike"
        }.get(mode, "foot")

        # OSRM expects lon,lat order
        coords = f"{start[1]},{start[0]};{end[1]},{end[0]}"
        url = f"{self.base_url}/route/v1/{profile}/{coords}"

        params = {
            "overview": "full",
            "geometries": "geojson"
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("code") != "Ok":
                raise RoutingError(f"Routing failed: {data.get('message', 'Unknown error')}")

            route = data["routes"][0]

            # Extract coordinates for the route line
            geometry = route["geometry"]["coordinates"]
            # Convert from [lon, lat] to [lat, lon] for Folium
            route_coords = [[coord[1], coord[0]] for coord in geometry]

            return {
                "distance": route["distance"],  # meters
                "duration": route["duration"],  # seconds
                "geometry": route_coords
            }

        except requests.RequestException as e:
            raise RoutingError(f"API request failed: {e}")

    def get_duration_minutes(self, start, end, mode="foot"):
        """Get walking duration in minutes."""
        route = self.get_route(start, end, mode)
        return route["duration"] / 60

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
        results = []

        for place in places:
            try:
                route = self.get_route(
                    origin,
                    (place["lat"], place["lon"]),
                    mode
                )

                place_with_route = place.copy()
                place_with_route["distance_m"] = route["distance"]
                place_with_route["duration_min"] = route["duration"] / 60
                place_with_route["route_geometry"] = route["geometry"]
                results.append(place_with_route)

            except RoutingError:
                # Skip places we can't route to
                continue

        return results
```

---

# Hour 2: Flask Application Integration

## 2.1 Main Application Structure

### Complete Flask Application

```python
# app.py
"""Smart City Navigator - Main Flask Application."""

from flask import Flask, render_template, request, flash, redirect, url_for
import folium
from folium import plugins

from utils.geocoding import Geocoder, GeocodingError
from utils.routing import Router, RoutingError
from config import Config

app = Flask(__name__)
app.secret_key = "your-secret-key-here"

# Initialize API clients
geocoder = Geocoder(user_agent=Config.USER_AGENT)
router = Router(base_url=Config.OSRM_URL)


@app.route("/")
def index():
    """Home page with search form."""
    return render_template("index.html", categories=Config.CATEGORIES)


@app.route("/search", methods=["POST"])
def search():
    """Process search and show results."""
    # Get form data
    location = request.form.get("location", "").strip()
    category = request.form.get("category", "cafe")
    max_time = request.form.get("max_time", 15, type=int)

    # Validate input
    if not location:
        flash("Please enter a starting location", "error")
        return redirect(url_for("index"))

    try:
        # Step 1: Geocode the starting location
        start = geocoder.geocode(location)

        # Step 2: Search for nearby places
        query = Config.CATEGORIES.get(category, {}).get("query", category)
        places = geocoder.search_nearby(
            start["lat"],
            start["lon"],
            query,
            radius=Config.DEFAULT_RADIUS
        )

        if not places:
            flash(f"No {category}s found near {location}", "warning")
            return redirect(url_for("index"))

        # Step 3: Get walking routes to each place
        places_with_routes = router.get_routes_to_places(
            (start["lat"], start["lon"]),
            places
        )

        # Step 4: Filter by walking time
        filtered_places = [
            p for p in places_with_routes
            if p["duration_min"] <= max_time
        ]

        # Step 5: Sort by duration (closest first)
        filtered_places.sort(key=lambda p: p["duration_min"])

        # Step 6: Generate map
        map_html = generate_map(start, filtered_places, category)

        return render_template(
            "results.html",
            location=location,
            start=start,
            places=filtered_places[:Config.DEFAULT_MAX_RESULTS],
            category=category,
            max_time=max_time,
            map_html=map_html,
            categories=Config.CATEGORIES
        )

    except GeocodingError as e:
        flash(f"Location error: {e}", "error")
        return redirect(url_for("index"))
    except RoutingError as e:
        flash(f"Routing error: {e}", "error")
        return redirect(url_for("index"))
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for("index"))


def generate_map(start, places, category):
    """Generate Folium map with places and routes."""
    # Create map centered on start location
    m = folium.Map(
        location=[start["lat"], start["lon"]],
        zoom_start=Config.DEFAULT_ZOOM,
        tiles=Config.MAP_TILES
    )

    # Get category style
    style = Config.CATEGORIES.get(category, {"icon": "info", "color": "gray"})

    # Add start marker
    folium.Marker(
        location=[start["lat"], start["lon"]],
        popup=f"<b>Start:</b><br>{start['display_name'][:50]}...",
        tooltip="Your starting point",
        icon=folium.Icon(color="green", icon="home", prefix="fa")
    ).add_to(m)

    # Add place markers and routes
    for i, place in enumerate(places, 1):
        # Add route line
        if "route_geometry" in place:
            folium.PolyLine(
                locations=place["route_geometry"],
                color=style["color"],
                weight=3,
                opacity=0.6,
                popup=f"{place['duration_min']:.1f} min walk"
            ).add_to(m)

        # Add place marker
        popup_html = f"""
        <div style="min-width: 150px;">
            <h4 style="margin: 0 0 5px 0;">#{i} {place['name']}</h4>
            <p style="margin: 0;"><b>Walk:</b> {place['duration_min']:.1f} min</p>
            <p style="margin: 0;"><b>Distance:</b> {place['distance_m']:.0f} m</p>
        </div>
        """

        folium.Marker(
            location=[place["lat"], place["lon"]],
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=f"#{i} {place['name']} ({place['duration_min']:.1f} min)",
            icon=folium.Icon(color=style["color"], icon=style["icon"], prefix="fa")
        ).add_to(m)

    # Fit map to show all markers
    if places:
        all_coords = [[start["lat"], start["lon"]]] + [[p["lat"], p["lon"]] for p in places]
        m.fit_bounds(all_coords)

    return m._repr_html_()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

## 2.2 HTML Templates

### Base Template

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Smart City Navigator{% endblock %}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            min-height: 100vh;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        header h1 {
            font-size: 1.5rem;
            font-weight: 600;
        }

        header a {
            color: white;
            text-decoration: none;
        }

        .nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
        }

        .nav-links a {
            margin-left: 1.5rem;
            opacity: 0.9;
        }

        .nav-links a:hover {
            opacity: 1;
        }

        main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        .flash-messages {
            margin-bottom: 1rem;
        }

        .flash {
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
        }

        .flash.error {
            background: #fee;
            color: #c00;
            border: 1px solid #fcc;
        }

        .flash.warning {
            background: #ffc;
            color: #860;
            border: 1px solid #fc0;
        }

        .flash.success {
            background: #efe;
            color: #060;
            border: 1px solid #afa;
        }

        .card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 2rem;
            margin-bottom: 1.5rem;
        }

        .card h2 {
            margin-bottom: 1rem;
            color: #333;
        }

        .form-group {
            margin-bottom: 1rem;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: #555;
        }

        input[type="text"],
        input[type="number"],
        select {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.2s;
        }

        input:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
        }

        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

        footer {
            text-align: center;
            padding: 2rem;
            color: #888;
            font-size: 0.9rem;
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <nav class="nav">
            <a href="/"><h1>Smart City Navigator</h1></a>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/about">About</a>
            </div>
        </nav>
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
        <p>Smart City Navigator - I2P Python Course Project</p>
    </footer>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Index Page (Search Form)

```html
<!-- templates/index.html -->
{% extends "base.html" %}

{% block title %}Smart City Navigator - Find Places{% endblock %}

{% block content %}
<div class="card">
    <h2>Find Places Near You</h2>
    <p style="color: #666; margin-bottom: 1.5rem;">
        Enter your starting location and find nearby places within walking distance.
    </p>

    <form method="POST" action="/search">
        <div class="form-group">
            <label for="location">Starting Location</label>
            <input type="text"
                   id="location"
                   name="location"
                   placeholder="e.g., National Taiwan University, Taipei"
                   required>
        </div>

        <div class="form-group">
            <label for="category">What are you looking for?</label>
            <select id="category" name="category">
                {% for key, value in categories.items() %}
                <option value="{{ key }}">{{ key | title }}</option>
                {% endfor %}
            </select>
        </div>

        <div class="form-group">
            <label for="max_time">Maximum walking time (minutes)</label>
            <input type="number"
                   id="max_time"
                   name="max_time"
                   value="10"
                   min="1"
                   max="60">
        </div>

        <button type="submit">Find Places</button>
    </form>
</div>

<div class="card">
    <h2>How It Works</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-top: 1rem;">
        <div>
            <h3 style="color: #667eea;">1. Enter Location</h3>
            <p style="color: #666; font-size: 0.9rem;">
                Type your starting point - an address, landmark, or place name.
            </p>
        </div>
        <div>
            <h3 style="color: #667eea;">2. Choose Category</h3>
            <p style="color: #666; font-size: 0.9rem;">
                Select what you're looking for: cafes, restaurants, parks, etc.
            </p>
        </div>
        <div>
            <h3 style="color: #667eea;">3. Set Time Limit</h3>
            <p style="color: #666; font-size: 0.9rem;">
                Specify the maximum walking time you're willing to travel.
            </p>
        </div>
        <div>
            <h3 style="color: #667eea;">4. View Results</h3>
            <p style="color: #666; font-size: 0.9rem;">
                See matching places on an interactive map with walking routes.
            </p>
        </div>
    </div>
</div>
{% endblock %}
```

### Results Page

```html
<!-- templates/results.html -->
{% extends "base.html" %}

{% block title %}Results - Smart City Navigator{% endblock %}

{% block extra_css %}
<style>
    .results-layout {
        display: grid;
        grid-template-columns: 350px 1fr;
        gap: 1.5rem;
    }

    @media (max-width: 900px) {
        .results-layout {
            grid-template-columns: 1fr;
        }
    }

    .sidebar {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .search-summary {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    .search-summary h3 {
        margin-bottom: 1rem;
        color: #333;
    }

    .summary-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #eee;
    }

    .summary-item:last-child {
        border-bottom: none;
    }

    .place-list {
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        overflow: hidden;
    }

    .place-list h3 {
        padding: 1rem 1.5rem;
        background: #f8f9fa;
        margin: 0;
        border-bottom: 1px solid #eee;
    }

    .place-item {
        padding: 1rem 1.5rem;
        border-bottom: 1px solid #eee;
        transition: background 0.2s;
    }

    .place-item:hover {
        background: #f8f9fa;
    }

    .place-item:last-child {
        border-bottom: none;
    }

    .place-rank {
        display: inline-block;
        width: 24px;
        height: 24px;
        background: #667eea;
        color: white;
        border-radius: 50%;
        text-align: center;
        line-height: 24px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
    }

    .place-name {
        font-weight: 600;
        color: #333;
    }

    .place-details {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }

    .map-container {
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        overflow: hidden;
        height: calc(100vh - 200px);
        min-height: 500px;
    }

    .map-container iframe {
        width: 100%;
        height: 100%;
        border: none;
    }

    .back-link {
        display: inline-block;
        margin-bottom: 1rem;
        color: #667eea;
        text-decoration: none;
    }

    .back-link:hover {
        text-decoration: underline;
    }
</style>
{% endblock %}

{% block content %}
<a href="/" class="back-link">&larr; New Search</a>

<div class="results-layout">
    <div class="sidebar">
        <div class="search-summary">
            <h3>Search Summary</h3>
            <div class="summary-item">
                <span>Starting from:</span>
                <span><strong>{{ location }}</strong></span>
            </div>
            <div class="summary-item">
                <span>Looking for:</span>
                <span><strong>{{ category | title }}</strong></span>
            </div>
            <div class="summary-item">
                <span>Max walk time:</span>
                <span><strong>{{ max_time }} min</strong></span>
            </div>
            <div class="summary-item">
                <span>Found:</span>
                <span><strong>{{ places | length }} places</strong></span>
            </div>
        </div>

        <div class="place-list">
            <h3>Places Found</h3>
            {% if places %}
                {% for place in places %}
                <div class="place-item">
                    <div>
                        <span class="place-rank">{{ loop.index }}</span>
                        <span class="place-name">{{ place.name }}</span>
                    </div>
                    <div class="place-details">
                        {{ place.duration_min | round(1) }} min walk
                        ({{ place.distance_m | round(0) }}m)
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <div class="place-item">
                    <p style="color: #666;">No places found matching your criteria.</p>
                </div>
            {% endif %}
        </div>
    </div>

    <div class="map-container">
        {{ map_html | safe }}
    </div>
</div>
{% endblock %}
```

---

# Hour 3: Error Handling, Testing, and Deployment

## 3.1 Robust Error Handling

### Graceful API Failure Handling

```python
# utils/api_helpers.py
"""Helper functions for API error handling."""

import logging
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def handle_api_errors(default_return=None):
    """
    Decorator to handle API errors gracefully.

    Args:
        default_return: Value to return if error occurs
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"API error in {func.__name__}: {e}")
                return default_return
        return wrapper
    return decorator


def retry_on_failure(max_retries=3, delay=1.0):
    """
    Decorator to retry failed API calls.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    import time

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))  # Exponential backoff

            raise last_error
        return wrapper
    return decorator
```

### Enhanced Application with Error Handling

```python
# app.py (enhanced version)
"""Smart City Navigator with comprehensive error handling."""

from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import logging

app = Flask(__name__)
app.secret_key = "your-secret-key-here"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template("error.html",
                         error_code=404,
                         message="Page not found"), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    logger.error(f"Internal error: {e}")
    return render_template("error.html",
                         error_code=500,
                         message="Internal server error"), 500


@app.route("/api/geocode")
def api_geocode():
    """API endpoint for geocoding (for AJAX requests)."""
    address = request.args.get("address", "")

    if not address:
        return jsonify({"error": "Address required"}), 400

    try:
        result = geocoder.geocode(address)
        return jsonify(result)
    except GeocodingError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Geocoding API error: {e}")
        return jsonify({"error": "Service unavailable"}), 503


@app.route("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "version": "1.0.0"
    })
```

### Error Page Template

```html
<!-- templates/error.html -->
{% extends "base.html" %}

{% block title %}Error {{ error_code }} - Smart City Navigator{% endblock %}

{% block content %}
<div class="card" style="text-align: center; padding: 4rem 2rem;">
    <h1 style="font-size: 4rem; color: #667eea; margin-bottom: 1rem;">
        {{ error_code }}
    </h1>
    <h2 style="color: #333; margin-bottom: 1rem;">
        {{ message }}
    </h2>
    <p style="color: #666; margin-bottom: 2rem;">
        {% if error_code == 404 %}
            The page you're looking for doesn't exist.
        {% elif error_code == 500 %}
            Something went wrong on our end. Please try again later.
        {% else %}
            An unexpected error occurred.
        {% endif %}
    </p>
    <a href="/" style="color: #667eea; text-decoration: none;">
        &larr; Back to Home
    </a>
</div>
{% endblock %}
```

## 3.2 Testing the Application

### Unit Tests

```python
# tests/test_geocoding.py
"""Tests for geocoding module."""

import unittest
from unittest.mock import patch, Mock
from utils.geocoding import Geocoder, GeocodingError


class TestGeocoder(unittest.TestCase):
    """Test cases for Geocoder class."""

    def setUp(self):
        """Set up test fixtures."""
        self.geocoder = Geocoder(user_agent="TestAgent/1.0")

    @patch('utils.geocoding.requests.get')
    def test_geocode_success(self, mock_get):
        """Test successful geocoding."""
        mock_response = Mock()
        mock_response.json.return_value = [{
            "lat": "25.0330",
            "lon": "121.5654",
            "display_name": "Taipei 101, Xinyi District, Taipei"
        }]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = self.geocoder.geocode("Taipei 101")

        self.assertEqual(result["lat"], 25.0330)
        self.assertEqual(result["lon"], 121.5654)
        self.assertIn("Taipei 101", result["display_name"])

    @patch('utils.geocoding.requests.get')
    def test_geocode_not_found(self, mock_get):
        """Test geocoding with no results."""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with self.assertRaises(GeocodingError):
            self.geocoder.geocode("nonexistent place xyz123")

    @patch('utils.geocoding.requests.get')
    def test_geocode_api_error(self, mock_get):
        """Test geocoding with API error."""
        mock_get.side_effect = Exception("Connection failed")

        with self.assertRaises(GeocodingError):
            self.geocoder.geocode("Taipei 101")


class TestRouter(unittest.TestCase):
    """Test cases for Router class."""

    @patch('utils.routing.requests.get')
    def test_get_route_success(self, mock_get):
        """Test successful route calculation."""
        from utils.routing import Router

        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "Ok",
            "routes": [{
                "distance": 1000,
                "duration": 720,
                "geometry": {
                    "coordinates": [[121.565, 25.033], [121.555, 25.040]]
                }
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        router = Router()
        result = router.get_route((25.033, 121.565), (25.040, 121.555))

        self.assertEqual(result["distance"], 1000)
        self.assertEqual(result["duration"], 720)


if __name__ == "__main__":
    unittest.main()
```

### Integration Tests

```python
# tests/test_app.py
"""Integration tests for Flask application."""

import unittest
from app import app


class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask application."""

    def setUp(self):
        """Set up test client."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_index_page(self):
        """Test that index page loads."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Smart City Navigator", response.data)

    def test_search_without_location(self):
        """Test search with missing location."""
        response = self.client.post("/search", data={})
        self.assertEqual(response.status_code, 302)  # Redirect

    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")

    def test_404_page(self):
        """Test 404 error page."""
        response = self.client.get("/nonexistent")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
```

## 3.3 Deployment Preparation

### Requirements File

```txt
# requirements.txt
flask>=2.0.0
folium>=0.14.0
requests>=2.28.0
```

### Running the Application

```bash
# Development
python app.py

# Production (with gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Environment Variables

```python
# config.py (production version)
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
    USER_AGENT = os.environ.get("USER_AGENT", "SmartCityNavigator/1.0")
```

---

## Summary

### Integration Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│                    Integration Checklist                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   User Interface                                                │
│   [x] HTML form collects location, category, time               │
│   [x] Results page shows map and place list                     │
│   [x] Error messages display properly                           │
│   [x] Responsive layout works on mobile                         │
│                                                                 │
│   Geocoding (Nominatim)                                         │
│   [x] Address to coordinates conversion                         │
│   [x] Nearby place search                                       │
│   [x] Rate limiting implemented                                 │
│   [x] Error handling for API failures                           │
│                                                                 │
│   Routing (OSRM)                                                │
│   [x] Walking route calculation                                 │
│   [x] Duration and distance extraction                          │
│   [x] Route geometry for map display                            │
│   [x] Batch routing for multiple places                         │
│                                                                 │
│   Business Logic                                                │
│   [x] Filter places by walking time                             │
│   [x] Sort places by duration                                   │
│   [x] Limit results count                                       │
│                                                                 │
│   Map Visualization (Folium)                                    │
│   [x] Start marker with home icon                               │
│   [x] Place markers with category icons                         │
│   [x] Route lines connecting places                             │
│   [x] Interactive popups with details                           │
│   [x] Auto-fit bounds to show all markers                       │
│                                                                 │
│   Quality                                                       │
│   [x] Unit tests for API wrappers                               │
│   [x] Integration tests for Flask app                           │
│   [x] Error pages for 404/500                                   │
│   [x] Logging for debugging                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Course Concepts Applied

| Week | Concept | Application in Project |
|------|---------|----------------------|
| 1-5 | Python Basics | Variables, loops, functions |
| 6-7 | Data Structures | Lists, dicts for places |
| 8 | APIs & HTTP | Nominatim, OSRM integration |
| 9 | Sorting | Sort places by duration |
| 10 | Graph Theory | Route optimization (TSP) |
| 11 | Testing | Unit & integration tests |
| 12 | OOP & Decorators | Place class, rate limiting |
| 13 | Flask | Web server, templates |
| 14 | Folium | Interactive map display |
| 15 | Integration | Complete application |

### Key Takeaways

1. **Modularity**: Separate concerns into distinct modules (geocoding, routing, mapping)
2. **Error Handling**: Always handle API failures gracefully
3. **User Experience**: Provide feedback during long operations
4. **Testing**: Test each component independently and together
5. **Rate Limiting**: Respect API usage policies with decorators

### Quick Reference

```python
# Complete flow in one function
def search_places(location, category, max_time):
    """Search for nearby places."""
    # 1. Geocode starting location
    start = geocoder.geocode(location)

    # 2. Find nearby places
    places = geocoder.search_nearby(start["lat"], start["lon"], category)

    # 3. Get walking routes
    places = router.get_routes_to_places((start["lat"], start["lon"]), places)

    # 4. Filter by time
    places = [p for p in places if p["duration_min"] <= max_time]

    # 5. Sort by duration
    places.sort(key=lambda p: p["duration_min"])

    # 6. Generate map
    map_html = generate_map(start, places)

    return places, map_html
```
