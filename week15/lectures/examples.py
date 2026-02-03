#!/usr/bin/env python3
"""
Week 15: Final Integration Sprint
Interactive Examples

This file demonstrates the complete Smart City Navigator integration.
Each demo builds on previous weeks' concepts.

Usage:
    python examples.py              # Run demo selection menu
    python examples.py --demo N     # Run specific demo (1-8)
    python examples.py --app        # Run the complete Flask app
"""

import sys
import os
import time
from functools import wraps

# Check for required packages
MISSING_PACKAGES = []

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    MISSING_PACKAGES.append("requests")

try:
    import folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False
    MISSING_PACKAGES.append("folium")

try:
    from flask import Flask, render_template_string, request, redirect, url_for, flash
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    MISSING_PACKAGES.append("flask")


# =============================================================================
# Rate Limiting Decorator
# =============================================================================

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


# =============================================================================
# Demo 1: Geocoding with Nominatim
# =============================================================================

def demo_geocoding():
    """Demonstrate geocoding with Nominatim API."""
    print("Demo 1: Geocoding with Nominatim")
    print("-" * 40)

    if not REQUESTS_AVAILABLE:
        print("Error: requests package not installed")
        return None

    @rate_limit(1.0)
    def geocode(address):
        """Convert address to coordinates."""
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }
        headers = {"User-Agent": "SmartCityNavigator/1.0 (demo)"}

        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        if not data:
            return None

        result = data[0]
        return {
            "lat": float(result["lat"]),
            "lon": float(result["lon"]),
            "display_name": result["display_name"]
        }

    # Test geocoding
    test_locations = [
        "National Taiwan University, Taipei",
        "Taipei 101",
        "Taipei Main Station"
    ]

    results = []
    for location in test_locations:
        print(f"\nGeocoding: {location}")
        try:
            result = geocode(location)
            if result:
                print(f"  Coordinates: [{result['lat']:.4f}, {result['lon']:.4f}]")
                print(f"  Full name: {result['display_name'][:60]}...")
                results.append({"query": location, **result})
            else:
                print("  Not found")
        except Exception as e:
            print(f"  Error: {e}")

    return results


# =============================================================================
# Demo 2: Nearby Place Search
# =============================================================================

def demo_nearby_search():
    """Demonstrate searching for nearby places."""
    print("Demo 2: Nearby Place Search")
    print("-" * 40)

    if not REQUESTS_AVAILABLE:
        print("Error: requests package not installed")
        return None

    @rate_limit(1.0)
    def search_nearby(lat, lon, query, radius=1000):
        """Search for places near a location."""
        url = "https://nominatim.openstreetmap.org/search"

        # Calculate bounding box (approximate)
        delta = radius / 111000  # ~111km per degree

        params = {
            "q": query,
            "format": "json",
            "limit": 10,
            "viewbox": f"{lon-delta},{lat+delta},{lon+delta},{lat-delta}",
            "bounded": 1
        }
        headers = {"User-Agent": "SmartCityNavigator/1.0 (demo)"}

        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        places = []

        for item in data:
            places.append({
                "name": item.get("name", item.get("display_name", "Unknown")[:30]),
                "lat": float(item["lat"]),
                "lon": float(item["lon"]),
                "type": item.get("type", "place")
            })

        return places

    # Search near NTU
    center = {"lat": 25.0174, "lon": 121.5405, "name": "NTU"}

    print(f"\nSearching for cafes near {center['name']}...")
    print(f"Center: [{center['lat']}, {center['lon']}]")
    print(f"Radius: 1000m")

    try:
        places = search_nearby(center["lat"], center["lon"], "cafe")
        print(f"\nFound {len(places)} places:")

        for i, place in enumerate(places[:5], 1):
            print(f"  {i}. {place['name']}")
            print(f"     Type: {place['type']}")
            print(f"     Location: [{place['lat']:.4f}, {place['lon']:.4f}]")

        return {"center": center, "places": places}

    except Exception as e:
        print(f"Error: {e}")
        return None


# =============================================================================
# Demo 3: Route Calculation with OSRM
# =============================================================================

def demo_routing():
    """Demonstrate route calculation with OSRM API."""
    print("Demo 3: Route Calculation with OSRM")
    print("-" * 40)

    if not REQUESTS_AVAILABLE:
        print("Error: requests package not installed")
        return None

    @rate_limit(0.5)
    def get_route(start, end, mode="foot"):
        """Get walking route between two points."""
        # OSRM expects lon,lat order
        coords = f"{start[1]},{start[0]};{end[1]},{end[0]}"
        url = f"http://router.project-osrm.org/route/v1/{mode}/{coords}"

        params = {
            "overview": "full",
            "geometries": "geojson"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("code") != "Ok":
            return None

        route = data["routes"][0]

        # Convert coordinates for Folium (lat, lon)
        geometry = route["geometry"]["coordinates"]
        route_coords = [[coord[1], coord[0]] for coord in geometry]

        return {
            "distance_m": route["distance"],
            "duration_s": route["duration"],
            "duration_min": route["duration"] / 60,
            "geometry": route_coords
        }

    # Test route from NTU to nearby locations
    start = (25.0174, 121.5405)  # NTU
    destinations = [
        {"name": "Gongguan Station", "coords": (25.0143, 121.5343)},
        {"name": "Taipei 101", "coords": (25.0330, 121.5654)},
    ]

    print(f"\nCalculating walking routes from NTU:")
    results = []

    for dest in destinations:
        print(f"\n  To: {dest['name']}")
        try:
            route = get_route(start, dest["coords"])
            if route:
                print(f"    Distance: {route['distance_m']:.0f} m")
                print(f"    Duration: {route['duration_min']:.1f} min")
                print(f"    Route points: {len(route['geometry'])}")
                results.append({"destination": dest, "route": route})
            else:
                print("    Route not found")
        except Exception as e:
            print(f"    Error: {e}")

    return results


# =============================================================================
# Demo 4: Filter and Sort Places
# =============================================================================

def demo_filter_sort():
    """Demonstrate filtering and sorting places."""
    print("Demo 4: Filter and Sort Places")
    print("-" * 40)

    # Sample places with walking times
    places = [
        {"name": "Cafe A", "duration_min": 5.2, "rating": 4.5},
        {"name": "Cafe B", "duration_min": 12.8, "rating": 4.8},
        {"name": "Cafe C", "duration_min": 3.1, "rating": 4.2},
        {"name": "Cafe D", "duration_min": 18.5, "rating": 4.9},
        {"name": "Cafe E", "duration_min": 8.7, "rating": 4.6},
        {"name": "Cafe F", "duration_min": 15.2, "rating": 4.3},
    ]

    max_time = 10  # minutes

    print(f"\nAll places ({len(places)} total):")
    for p in places:
        print(f"  - {p['name']}: {p['duration_min']:.1f} min, {p['rating']} stars")

    # Filter by walking time
    filtered = [p for p in places if p["duration_min"] <= max_time]

    print(f"\nAfter filtering (max {max_time} min walk): {len(filtered)} places")
    for p in filtered:
        print(f"  - {p['name']}: {p['duration_min']:.1f} min")

    # Sort by duration
    sorted_by_duration = sorted(filtered, key=lambda p: p["duration_min"])

    print("\nSorted by walking time:")
    for i, p in enumerate(sorted_by_duration, 1):
        print(f"  {i}. {p['name']}: {p['duration_min']:.1f} min")

    # Sort by rating
    sorted_by_rating = sorted(filtered, key=lambda p: p["rating"], reverse=True)

    print("\nSorted by rating:")
    for i, p in enumerate(sorted_by_rating, 1):
        print(f"  {i}. {p['name']}: {p['rating']} stars ({p['duration_min']:.1f} min)")

    return {
        "original": places,
        "filtered": filtered,
        "sorted_duration": sorted_by_duration,
        "sorted_rating": sorted_by_rating
    }


# =============================================================================
# Demo 5: Generate Map with Folium
# =============================================================================

def demo_map_generation():
    """Demonstrate map generation with Folium."""
    print("Demo 5: Generate Map with Folium")
    print("-" * 40)

    if not FOLIUM_AVAILABLE:
        print("Error: folium package not installed")
        return None

    # Sample data
    start = {"name": "NTU", "lat": 25.0174, "lon": 121.5405}

    places = [
        {"name": "Cafe A", "lat": 25.0150, "lon": 121.5340, "duration_min": 5.2},
        {"name": "Cafe B", "lat": 25.0200, "lon": 121.5450, "duration_min": 8.7},
        {"name": "Cafe C", "lat": 25.0130, "lon": 121.5380, "duration_min": 3.1},
    ]

    # Create map
    m = folium.Map(
        location=[start["lat"], start["lon"]],
        zoom_start=15,
        tiles="CartoDB positron"
    )

    # Add start marker
    folium.Marker(
        location=[start["lat"], start["lon"]],
        popup=f"<b>Start:</b> {start['name']}",
        tooltip="Your location",
        icon=folium.Icon(color="green", icon="home", prefix="fa")
    ).add_to(m)

    # Add place markers with routes
    for i, place in enumerate(places, 1):
        # Draw route line (simplified - straight line)
        folium.PolyLine(
            locations=[
                [start["lat"], start["lon"]],
                [place["lat"], place["lon"]]
            ],
            color="orange",
            weight=3,
            opacity=0.6,
            dash_array="5, 10"
        ).add_to(m)

        # Add place marker
        popup_html = f"""
        <div style="min-width: 120px;">
            <b>#{i} {place['name']}</b><br>
            Walk: {place['duration_min']:.1f} min
        </div>
        """

        folium.Marker(
            location=[place["lat"], place["lon"]],
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=f"#{i} {place['name']}",
            icon=folium.Icon(color="orange", icon="coffee", prefix="fa")
        ).add_to(m)

    # Fit bounds
    all_coords = [[start["lat"], start["lon"]]] + [[p["lat"], p["lon"]] for p in places]
    m.fit_bounds(all_coords)

    # Save map
    output_file = "demo5_map.html"
    m.save(output_file)
    print(f"\nMap saved to: {output_file}")
    print(f"Open in browser to view")

    return output_file


# =============================================================================
# Demo 6: Complete Integration (without Flask)
# =============================================================================

def demo_complete_integration():
    """Demonstrate complete integration of all components."""
    print("Demo 6: Complete Integration")
    print("-" * 40)

    if not REQUESTS_AVAILABLE or not FOLIUM_AVAILABLE:
        print("Error: Missing required packages")
        return None

    # Configuration
    location = "National Taiwan University, Taipei"
    category = "cafe"
    max_time = 10  # minutes

    print(f"\nSearching for {category}s near: {location}")
    print(f"Max walking time: {max_time} minutes")

    @rate_limit(1.0)
    def geocode(address):
        """Geocode an address."""
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": address, "format": "json", "limit": 1}
        headers = {"User-Agent": "SmartCityNavigator/1.0 (demo)"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        if not data:
            return None
        return {
            "lat": float(data[0]["lat"]),
            "lon": float(data[0]["lon"]),
            "display_name": data[0]["display_name"]
        }

    @rate_limit(1.0)
    def search_nearby(lat, lon, query):
        """Search for nearby places."""
        url = "https://nominatim.openstreetmap.org/search"
        delta = 0.01
        params = {
            "q": query,
            "format": "json",
            "limit": 5,
            "viewbox": f"{lon-delta},{lat+delta},{lon+delta},{lat-delta}",
            "bounded": 1
        }
        headers = {"User-Agent": "SmartCityNavigator/1.0 (demo)"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        return [
            {"name": p.get("name", "Unknown"), "lat": float(p["lat"]), "lon": float(p["lon"])}
            for p in response.json()
        ]

    @rate_limit(0.5)
    def get_route(start, end):
        """Get walking route."""
        coords = f"{start[1]},{start[0]};{end[1]},{end[0]}"
        url = f"http://router.project-osrm.org/route/v1/foot/{coords}"
        response = requests.get(url, params={"overview": "full", "geometries": "geojson"}, timeout=10)
        data = response.json()
        if data.get("code") != "Ok":
            return None
        route = data["routes"][0]
        return {
            "duration_min": route["duration"] / 60,
            "distance_m": route["distance"],
            "geometry": [[c[1], c[0]] for c in route["geometry"]["coordinates"]]
        }

    try:
        # Step 1: Geocode
        print("\n1. Geocoding starting location...")
        start = geocode(location)
        if not start:
            print("   Location not found!")
            return None
        print(f"   Found: [{start['lat']:.4f}, {start['lon']:.4f}]")

        # Step 2: Search nearby
        print("\n2. Searching for nearby places...")
        places = search_nearby(start["lat"], start["lon"], category)
        print(f"   Found {len(places)} places")

        # Step 3: Get routes
        print("\n3. Calculating walking routes...")
        places_with_routes = []
        for place in places:
            route = get_route((start["lat"], start["lon"]), (place["lat"], place["lon"]))
            if route:
                place["duration_min"] = route["duration_min"]
                place["distance_m"] = route["distance_m"]
                place["geometry"] = route["geometry"]
                places_with_routes.append(place)
                print(f"   - {place['name']}: {route['duration_min']:.1f} min")

        # Step 4: Filter
        print(f"\n4. Filtering by max {max_time} min walk...")
        filtered = [p for p in places_with_routes if p["duration_min"] <= max_time]
        print(f"   {len(filtered)} places within time limit")

        # Step 5: Sort
        print("\n5. Sorting by walking time...")
        filtered.sort(key=lambda p: p["duration_min"])

        # Step 6: Generate map
        print("\n6. Generating map...")
        m = folium.Map(
            location=[start["lat"], start["lon"]],
            zoom_start=15,
            tiles="CartoDB positron"
        )

        # Start marker
        folium.Marker(
            [start["lat"], start["lon"]],
            popup=f"<b>Start</b><br>{start['display_name'][:40]}...",
            icon=folium.Icon(color="green", icon="home", prefix="fa")
        ).add_to(m)

        # Place markers and routes
        for i, place in enumerate(filtered, 1):
            if "geometry" in place:
                folium.PolyLine(
                    place["geometry"],
                    color="orange",
                    weight=4,
                    opacity=0.7
                ).add_to(m)

            folium.Marker(
                [place["lat"], place["lon"]],
                popup=f"<b>#{i} {place['name']}</b><br>{place['duration_min']:.1f} min",
                tooltip=f"#{i} {place['name']}",
                icon=folium.Icon(color="orange", icon="coffee", prefix="fa")
            ).add_to(m)

        output_file = "demo6_complete.html"
        m.save(output_file)
        print(f"\nMap saved to: {output_file}")

        # Summary
        print("\n" + "=" * 40)
        print("RESULTS SUMMARY")
        print("=" * 40)
        print(f"Location: {location}")
        print(f"Category: {category}")
        print(f"Max walk time: {max_time} min")
        print(f"Places found: {len(filtered)}")
        print("\nPlaces:")
        for i, p in enumerate(filtered, 1):
            print(f"  {i}. {p['name']} - {p['duration_min']:.1f} min ({p['distance_m']:.0f}m)")

        return {"start": start, "places": filtered, "map_file": output_file}

    except Exception as e:
        print(f"\nError: {e}")
        return None


# =============================================================================
# Demo 7: Flask Web Application
# =============================================================================

def demo_flask_app():
    """Run a simple Flask application."""
    print("Demo 7: Flask Web Application")
    print("-" * 40)

    if not FLASK_AVAILABLE or not FOLIUM_AVAILABLE:
        print("Error: flask and folium packages required")
        return None

    app = Flask(__name__)
    app.secret_key = "demo-secret-key"

    # Sample data (pre-calculated to avoid API calls)
    SAMPLE_PLACES = [
        {"name": "Cafe Artista", "lat": 25.0150, "lon": 121.5340, "duration_min": 3.2, "distance_m": 280},
        {"name": "Louisa Coffee", "lat": 25.0180, "lon": 121.5420, "duration_min": 5.1, "distance_m": 420},
        {"name": "Starbucks", "lat": 25.0160, "lon": 121.5380, "duration_min": 4.5, "distance_m": 380},
        {"name": "Cama Cafe", "lat": 25.0200, "lon": 121.5450, "duration_min": 8.2, "distance_m": 680},
    ]

    TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart City Navigator Demo</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, sans-serif; background: #f5f5f5; }
            header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem 2rem;
            }
            main { max-width: 1000px; margin: 2rem auto; padding: 0 1rem; }
            .card {
                background: white;
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .form-group { margin-bottom: 1rem; }
            label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
            input, select {
                width: 100%;
                padding: 0.75rem;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 1rem;
            }
            button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                cursor: pointer;
                font-size: 1rem;
            }
            button:hover { opacity: 0.9; }
            .results { display: grid; grid-template-columns: 1fr 2fr; gap: 1.5rem; }
            @media (max-width: 768px) { .results { grid-template-columns: 1fr; } }
            .place-list { list-style: none; }
            .place-item {
                padding: 1rem;
                border-bottom: 1px solid #eee;
            }
            .place-item:last-child { border-bottom: none; }
            .place-name { font-weight: 600; color: #333; }
            .place-details { color: #666; font-size: 0.9rem; margin-top: 0.25rem; }
            .map-container { height: 500px; border-radius: 12px; overflow: hidden; }
        </style>
    </head>
    <body>
        <header>
            <h1>Smart City Navigator</h1>
            <p style="opacity: 0.8; margin-top: 0.5rem;">Find places within walking distance</p>
        </header>
        <main>
            {% if not results %}
            <div class="card">
                <h2 style="margin-bottom: 1rem;">Search for Places</h2>
                <form method="POST">
                    <div class="form-group">
                        <label>Starting Location</label>
                        <input type="text" name="location" value="National Taiwan University" required>
                    </div>
                    <div class="form-group">
                        <label>Category</label>
                        <select name="category">
                            <option value="cafe">Cafe</option>
                            <option value="restaurant">Restaurant</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Max Walking Time (minutes)</label>
                        <input type="number" name="max_time" value="10" min="1" max="30">
                    </div>
                    <button type="submit">Find Places</button>
                </form>
            </div>
            {% else %}
            <div class="card">
                <p><a href="/">&larr; New Search</a></p>
            </div>
            <div class="results">
                <div class="card">
                    <h3 style="margin-bottom: 1rem;">Found {{ places|length }} Places</h3>
                    <ul class="place-list">
                    {% for place in places %}
                        <li class="place-item">
                            <div class="place-name">#{{ loop.index }} {{ place.name }}</div>
                            <div class="place-details">
                                {{ "%.1f"|format(place.duration_min) }} min walk
                                ({{ place.distance_m|int }}m)
                            </div>
                        </li>
                    {% endfor %}
                    </ul>
                </div>
                <div class="card">
                    <div class="map-container">
                        {{ map_html|safe }}
                    </div>
                </div>
            </div>
            {% endif %}
        </main>
    </body>
    </html>
    """

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            max_time = request.form.get("max_time", 10, type=int)

            # Filter sample places
            filtered = [p for p in SAMPLE_PLACES if p["duration_min"] <= max_time]
            filtered.sort(key=lambda p: p["duration_min"])

            # Generate map
            start = {"lat": 25.0174, "lon": 121.5405}
            m = folium.Map(
                location=[start["lat"], start["lon"]],
                zoom_start=15,
                tiles="CartoDB positron"
            )

            # Start marker
            folium.Marker(
                [start["lat"], start["lon"]],
                popup="<b>Start</b><br>NTU",
                icon=folium.Icon(color="green", icon="home", prefix="fa")
            ).add_to(m)

            # Place markers
            for i, place in enumerate(filtered, 1):
                folium.PolyLine(
                    [[start["lat"], start["lon"]], [place["lat"], place["lon"]]],
                    color="orange",
                    weight=3,
                    dash_array="5, 10"
                ).add_to(m)

                folium.Marker(
                    [place["lat"], place["lon"]],
                    popup=f"<b>#{i} {place['name']}</b><br>{place['duration_min']:.1f} min",
                    icon=folium.Icon(color="orange", icon="coffee", prefix="fa")
                ).add_to(m)

            return render_template_string(
                TEMPLATE,
                results=True,
                places=filtered,
                map_html=m._repr_html_()
            )

        return render_template_string(TEMPLATE, results=False)

    print("\nStarting Flask server...")
    print("Visit: http://localhost:5000")
    print("Press Ctrl+C to stop\n")

    app.run(debug=False, port=5000)


# =============================================================================
# Demo 8: Error Handling
# =============================================================================

def demo_error_handling():
    """Demonstrate proper error handling."""
    print("Demo 8: Error Handling")
    print("-" * 40)

    class GeocodingError(Exception):
        """Custom exception for geocoding errors."""
        pass

    class RoutingError(Exception):
        """Custom exception for routing errors."""
        pass

    def safe_geocode(address):
        """Geocode with error handling."""
        if not address or not address.strip():
            raise GeocodingError("Address cannot be empty")

        if not REQUESTS_AVAILABLE:
            raise GeocodingError("requests package not available")

        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {"q": address, "format": "json", "limit": 1}
            headers = {"User-Agent": "SmartCityNavigator/1.0 (demo)"}

            response = requests.get(url, params=params, headers=headers, timeout=5)
            response.raise_for_status()

            data = response.json()
            if not data:
                raise GeocodingError(f"Location not found: {address}")

            return {
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"])
            }

        except requests.Timeout:
            raise GeocodingError("Request timed out - try again later")
        except requests.RequestException as e:
            raise GeocodingError(f"Network error: {e}")

    # Test cases
    test_cases = [
        "",                           # Empty
        "   ",                        # Whitespace only
        "nonexistent_place_xyz123",   # Not found
        "Taipei 101",                 # Valid
    ]

    print("\nTesting error handling:")

    for address in test_cases:
        print(f"\n  Input: '{address}'")
        try:
            result = safe_geocode(address)
            print(f"  Result: [{result['lat']:.4f}, {result['lon']:.4f}]")
        except GeocodingError as e:
            print(f"  Error: {e}")
        except Exception as e:
            print(f"  Unexpected error: {e}")

        time.sleep(1)  # Rate limiting

    return True


# =============================================================================
# Demo Runner
# =============================================================================

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def run_demo(demo_num):
    """Run a specific demo."""
    demos = {
        1: ("Geocoding with Nominatim", demo_geocoding),
        2: ("Nearby Place Search", demo_nearby_search),
        3: ("Route Calculation (OSRM)", demo_routing),
        4: ("Filter and Sort Places", demo_filter_sort),
        5: ("Map Generation (Folium)", demo_map_generation),
        6: ("Complete Integration", demo_complete_integration),
        7: ("Flask Web Application", demo_flask_app),
        8: ("Error Handling", demo_error_handling),
    }

    if demo_num not in demos:
        print(f"Invalid demo number: {demo_num}")
        return None

    title, func = demos[demo_num]
    print_header(f"Demo {demo_num}: {title}")

    return func()


def show_menu():
    """Show interactive menu."""
    print_header("Week 15: Final Integration Sprint")

    if MISSING_PACKAGES:
        print(f"\nWarning: Missing packages: {', '.join(MISSING_PACKAGES)}")
        print("Install with: pip install " + " ".join(MISSING_PACKAGES))

    print("""
Available Demos:
  1. Geocoding          - Convert addresses to coordinates
  2. Nearby Search      - Find places near a location
  3. Route Calculation  - Calculate walking routes
  4. Filter & Sort      - Process place data
  5. Map Generation     - Create interactive maps
  6. Complete Integration - Full workflow (no server)
  7. Flask Application  - Web-based interface
  8. Error Handling     - Robust error management

Commands:
  - Enter 1-8 to run a demo
  - Enter 'q' to quit
""")

    while True:
        try:
            choice = input("Select demo (1-8, or 'q'): ").strip().lower()

            if choice == 'q':
                print("Goodbye!")
                break
            elif choice.isdigit():
                num = int(choice)
                if 1 <= num <= 8:
                    run_demo(num)
                else:
                    print("Please enter a number between 1 and 8")
            else:
                print("Invalid input")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            break


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo" and len(sys.argv) > 2:
            try:
                run_demo(int(sys.argv[2]))
            except ValueError:
                print("Usage: python examples.py --demo N")
        elif sys.argv[1] == "--app":
            demo_flask_app()
        elif sys.argv[1] == "--help":
            print(__doc__)
        else:
            print("Unknown argument. Use --help for usage.")
    else:
        show_menu()


if __name__ == "__main__":
    main()
