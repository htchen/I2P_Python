#!/usr/bin/env python3
"""
Week 15 Lab: Final Integration Sprint
Starter Code with Test Suite

This file contains starter code for the Smart City Navigator project.
Complete the TODO sections to build the full application.

Run: python week15_starter.py
Run specific test: python week15_starter.py --test ex1
Run Flask app: python week15_starter.py --app
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
# Exercise 1: Rate Limiting Decorator
# =============================================================================

def rate_limit(min_interval=1.0):
    """
    Decorator to enforce minimum time between function calls.

    Args:
        min_interval: Minimum seconds between calls

    Returns:
        Decorated function
    """
    last_call = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Implement rate limiting
            # 1. Calculate elapsed time since last call
            # 2. If elapsed < min_interval, sleep for the difference
            # 3. Call the function
            # 4. Update last_call time
            # 5. Return the result

            # Remove this and implement:
            return func(*args, **kwargs)
        return wrapper
    return decorator


# =============================================================================
# Exercise 2: Geocoding Module
# =============================================================================

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
        # TODO: Implement geocoding
        # 1. Validate address is not empty
        # 2. Make GET request to self.base_url + "/search"
        #    with params: q=address, format=json, limit=1
        # 3. Handle request errors
        # 4. Check if results exist
        # 5. Extract and return lat, lon, display_name

        # Remove this and implement:
        pass

    @rate_limit(1.0)
    def search_nearby(self, lat, lon, query, radius=1000):
        """
        Search for places near a location.

        Args:
            lat: Latitude
            lon: Longitude
            query: Search query (e.g., "cafe")
            radius: Search radius in meters

        Returns:
            List of place dictionaries with name, lat, lon
        """
        # TODO: Implement nearby search
        # 1. Calculate bounding box: delta = radius / 111000
        # 2. Make GET request with viewbox parameter
        # 3. Parse results and return list of places

        # Remove this and implement:
        pass


# =============================================================================
# Exercise 3: Routing Module
# =============================================================================

class RoutingError(Exception):
    """Exception raised for routing errors."""
    pass


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
        # TODO: Implement route calculation
        # IMPORTANT: OSRM expects coordinates as lon,lat (not lat,lon!)
        # 1. Build URL: {base_url}/route/v1/{mode}/{start_lon},{start_lat};{end_lon},{end_lat}
        # 2. Add params: overview=full, geometries=geojson
        # 3. Make request and parse response
        # 4. Check response code is "Ok"
        # 5. Extract distance, duration, geometry
        # 6. Convert geometry from [lon,lat] to [lat,lon] for Folium

        # Remove this and implement:
        pass

    def get_routes_to_places(self, origin, places, mode="foot"):
        """
        Get routes from origin to multiple places.

        Args:
            origin: (lat, lon) tuple
            places: List of place dicts with 'lat', 'lon'
            mode: Travel mode

        Returns:
            List of places with added 'duration_min', 'distance_m', 'route_geometry'
        """
        # TODO: Implement batch routing
        # 1. Loop through places
        # 2. Get route to each place
        # 3. Add route info to place dict
        # 4. Handle errors (skip places that fail)
        # 5. Return list of places with routes

        # Remove this and implement:
        pass


# =============================================================================
# Exercise 4: Map Generation
# =============================================================================

# Category styles for markers
CATEGORY_STYLES = {
    "cafe": {"icon": "coffee", "color": "orange"},
    "restaurant": {"icon": "cutlery", "color": "red"},
    "park": {"icon": "tree", "color": "green"},
    "museum": {"icon": "university", "color": "blue"},
    "default": {"icon": "info", "color": "gray"},
}


def generate_map(start, places, category="cafe"):
    """
    Generate Folium map with start location, places, and routes.

    Args:
        start: dict with 'lat', 'lon', 'display_name'
        places: List of place dicts with 'lat', 'lon', 'name', 'duration_min', 'route_geometry'
        category: Category for marker styling

    Returns:
        HTML string of the map
    """
    if not FOLIUM_AVAILABLE:
        return "<p>Folium not available</p>"

    # TODO: Implement map generation
    # 1. Create folium.Map centered on start location
    # 2. Add start marker (green, home icon)
    # 3. Loop through places:
    #    a. Add route line (PolyLine) if geometry exists
    #    b. Add place marker with popup showing name and duration
    # 4. Fit bounds to show all markers
    # 5. Return m._repr_html_()

    # Remove this and implement:
    m = folium.Map(location=[start["lat"], start["lon"]], zoom_start=14)
    return m._repr_html_()


# =============================================================================
# Exercise 5: Flask Application
# =============================================================================

def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.secret_key = "dev-secret-key"

    # Initialize API clients
    geocoder = Geocoder()
    router = Router()

    # Categories
    CATEGORIES = {
        "cafe": "Cafe",
        "restaurant": "Restaurant",
        "park": "Park",
        "museum": "Museum",
    }

    # HTML template
    TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart City Navigator</title>
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
            .flash { padding: 1rem; border-radius: 8px; margin-bottom: 1rem; }
            .flash.error { background: #fee; color: #c00; border: 1px solid #fcc; }
            .flash.warning { background: #ffc; color: #860; }
            .flash.success { background: #efe; color: #060; }
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
            .results { display: grid; grid-template-columns: 300px 1fr; gap: 1.5rem; }
            @media (max-width: 768px) { .results { grid-template-columns: 1fr; } }
            .place-list { list-style: none; }
            .place-item { padding: 0.75rem 0; border-bottom: 1px solid #eee; }
            .place-item:last-child { border-bottom: none; }
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
            .map-container { height: 500px; border-radius: 12px; overflow: hidden; }
            a { color: #667eea; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <header>
            <h1>Smart City Navigator</h1>
        </header>
        <main>
            {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
            {% endwith %}

            {% if not show_results %}
            <div class="card">
                <h2 style="margin-bottom: 1rem;">Find Places Near You</h2>
                <form method="POST" action="/search">
                    <div class="form-group">
                        <label for="location">Starting Location</label>
                        <input type="text" id="location" name="location"
                               placeholder="e.g., National Taiwan University" required>
                    </div>
                    <div class="form-group">
                        <label for="category">What are you looking for?</label>
                        <select id="category" name="category">
                            {% for key, value in categories.items() %}
                            <option value="{{ key }}">{{ value }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="max_time">Maximum walking time (minutes)</label>
                        <input type="number" id="max_time" name="max_time"
                               value="10" min="1" max="30">
                    </div>
                    <button type="submit">Find Places</button>
                </form>
            </div>
            {% else %}
            <div class="card">
                <a href="/">&larr; New Search</a>
            </div>
            <div class="results">
                <div class="card">
                    <h3 style="margin-bottom: 1rem;">Results</h3>
                    <p style="color: #666; margin-bottom: 1rem;">
                        Found {{ places|length }} {{ category }}s within {{ max_time }} min walk
                    </p>
                    <ul class="place-list">
                    {% for place in places %}
                        <li class="place-item">
                            <span class="place-rank">{{ loop.index }}</span>
                            <strong>{{ place.name }}</strong>
                            <div style="color: #666; font-size: 0.9rem; margin-left: 32px;">
                                {{ "%.1f"|format(place.duration_min) }} min
                                ({{ place.distance_m|int }}m)
                            </div>
                        </li>
                    {% else %}
                        <li class="place-item">No places found</li>
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

    @app.route("/")
    def index():
        return render_template_string(
            TEMPLATE,
            show_results=False,
            categories=CATEGORIES
        )

    @app.route("/search", methods=["POST"])
    def search():
        # Get form data
        location = request.form.get("location", "").strip()
        category = request.form.get("category", "cafe")
        max_time = request.form.get("max_time", 10, type=int)

        # TODO: Implement search flow
        # 1. Validate location is not empty
        # 2. Geocode the location
        # 3. Search for nearby places
        # 4. Get walking routes to each place
        # 5. Filter by max_time
        # 6. Sort by duration
        # 7. Generate map
        # 8. Return results template

        # Placeholder implementation - replace with your code:
        if not location:
            flash("Please enter a location", "error")
            return redirect(url_for("index"))

        try:
            # Geocode
            start = geocoder.geocode(location)
            if not start:
                flash(f"Could not find location: {location}", "error")
                return redirect(url_for("index"))

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

            # Filter by time
            filtered = [p for p in places_with_routes if p.get("duration_min", 999) <= max_time]

            # Sort by duration
            filtered.sort(key=lambda p: p.get("duration_min", 999))

            # Limit results
            filtered = filtered[:10]

            # Generate map
            map_html = generate_map(start, filtered, category)

            return render_template_string(
                TEMPLATE,
                show_results=True,
                places=filtered,
                category=category,
                max_time=max_time,
                map_html=map_html,
                categories=CATEGORIES
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

    return app


# =============================================================================
# Test Suite
# =============================================================================

def test_exercise_1():
    """Test rate limiting decorator."""
    print("\n" + "=" * 60)
    print("Testing Exercise 1: Rate Limiting")
    print("=" * 60)

    @rate_limit(0.5)
    def test_func():
        return time.time()

    tests_passed = 0
    tests_total = 2

    # Test 1: First call should be immediate
    start = time.time()
    test_func()
    elapsed = time.time() - start

    if elapsed < 0.1:
        print("  [PASS] First call is immediate")
        tests_passed += 1
    else:
        print(f"  [FAIL] First call took {elapsed:.2f}s (expected < 0.1s)")

    # Test 2: Second call should be delayed
    start = time.time()
    test_func()
    elapsed = time.time() - start

    if elapsed >= 0.4:
        print("  [PASS] Second call is rate limited")
        tests_passed += 1
    else:
        print(f"  [FAIL] Second call took {elapsed:.2f}s (expected >= 0.4s)")

    print(f"\nExercise 1: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_2():
    """Test geocoding module."""
    print("\n" + "=" * 60)
    print("Testing Exercise 2: Geocoding")
    print("=" * 60)

    if not REQUESTS_AVAILABLE:
        print("  [SKIP] requests package not installed")
        return False

    geocoder = Geocoder()
    tests_passed = 0
    tests_total = 3

    # Test 1: Geocode valid location
    try:
        result = geocoder.geocode("Taipei 101")
        if result and "lat" in result and "lon" in result:
            print(f"  [PASS] Geocoded Taipei 101: [{result['lat']:.4f}, {result['lon']:.4f}]")
            tests_passed += 1
        else:
            print("  [FAIL] Geocode returned invalid result")
    except Exception as e:
        print(f"  [FAIL] Geocode error: {e}")

    time.sleep(1)  # Rate limiting

    # Test 2: Geocode non-existent location
    try:
        result = geocoder.geocode("nonexistent_place_xyz123")
        print("  [FAIL] Should raise GeocodingError for non-existent location")
    except GeocodingError:
        print("  [PASS] Raises GeocodingError for non-existent location")
        tests_passed += 1
    except Exception as e:
        print(f"  [FAIL] Wrong exception type: {e}")

    time.sleep(1)

    # Test 3: Search nearby
    try:
        places = geocoder.search_nearby(25.033, 121.565, "cafe")
        if places and len(places) > 0:
            print(f"  [PASS] Found {len(places)} cafes nearby")
            tests_passed += 1
        else:
            print("  [FAIL] No cafes found")
    except Exception as e:
        print(f"  [FAIL] Search nearby error: {e}")

    print(f"\nExercise 2: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_3():
    """Test routing module."""
    print("\n" + "=" * 60)
    print("Testing Exercise 3: Routing")
    print("=" * 60)

    if not REQUESTS_AVAILABLE:
        print("  [SKIP] requests package not installed")
        return False

    router = Router()
    tests_passed = 0
    tests_total = 2

    # Test 1: Get single route
    try:
        route = router.get_route(
            (25.0174, 121.5405),  # NTU
            (25.0330, 121.5654)   # Taipei 101
        )
        if route and "distance" in route and "duration" in route:
            print(f"  [PASS] Route calculated: {route['distance']:.0f}m, {route['duration']/60:.1f}min")
            tests_passed += 1
        else:
            print("  [FAIL] Route returned invalid result")
    except Exception as e:
        print(f"  [FAIL] Route error: {e}")

    time.sleep(0.5)

    # Test 2: Batch routing
    places = [
        {"name": "Place A", "lat": 25.020, "lon": 121.540},
        {"name": "Place B", "lat": 25.025, "lon": 121.550},
    ]

    try:
        results = router.get_routes_to_places((25.0174, 121.5405), places)
        if results and len(results) > 0 and "duration_min" in results[0]:
            print(f"  [PASS] Batch routing: {len(results)} routes calculated")
            tests_passed += 1
        else:
            print("  [FAIL] Batch routing returned invalid results")
    except Exception as e:
        print(f"  [FAIL] Batch routing error: {e}")

    print(f"\nExercise 3: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_4():
    """Test map generation."""
    print("\n" + "=" * 60)
    print("Testing Exercise 4: Map Generation")
    print("=" * 60)

    if not FOLIUM_AVAILABLE:
        print("  [SKIP] folium package not installed")
        return False

    tests_passed = 0
    tests_total = 2

    start = {"lat": 25.0174, "lon": 121.5405, "display_name": "NTU"}
    places = [
        {
            "name": "Cafe A",
            "lat": 25.015,
            "lon": 121.534,
            "duration_min": 5.2,
            "distance_m": 420,
            "route_geometry": [[25.0174, 121.5405], [25.015, 121.534]]
        }
    ]

    # Test 1: Map generates without error
    try:
        html = generate_map(start, places, "cafe")
        if html and len(html) > 100:
            print("  [PASS] Map HTML generated")
            tests_passed += 1
        else:
            print("  [FAIL] Map HTML too short or empty")
    except Exception as e:
        print(f"  [FAIL] Map generation error: {e}")

    # Test 2: Map contains expected elements
    try:
        html = generate_map(start, places, "cafe")
        if "leaflet" in html.lower() or "folium" in html.lower():
            print("  [PASS] Map contains Leaflet/Folium elements")
            tests_passed += 1
        else:
            print("  [FAIL] Map missing expected elements")
    except Exception as e:
        print(f"  [FAIL] Map element check error: {e}")

    print(f"\nExercise 4: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_5():
    """Test Flask application."""
    print("\n" + "=" * 60)
    print("Testing Exercise 5: Flask Application")
    print("=" * 60)

    if not FLASK_AVAILABLE:
        print("  [SKIP] flask package not installed")
        return False

    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    tests_passed = 0
    tests_total = 3

    # Test 1: Index page loads
    try:
        response = client.get("/")
        if response.status_code == 200 and b"Smart City" in response.data:
            print("  [PASS] Index page loads")
            tests_passed += 1
        else:
            print("  [FAIL] Index page error")
    except Exception as e:
        print(f"  [FAIL] Index page error: {e}")

    # Test 2: Search without location redirects
    try:
        response = client.post("/search", data={"location": ""})
        if response.status_code == 302:
            print("  [PASS] Empty search redirects")
            tests_passed += 1
        else:
            print("  [FAIL] Empty search should redirect")
    except Exception as e:
        print(f"  [FAIL] Search redirect error: {e}")

    # Test 3: Search with valid input
    try:
        response = client.post("/search", data={
            "location": "Taipei 101",
            "category": "cafe",
            "max_time": "10"
        })
        if response.status_code in [200, 302]:
            print("  [PASS] Search with valid input accepted")
            tests_passed += 1
        else:
            print(f"  [FAIL] Search returned status {response.status_code}")
    except Exception as e:
        print(f"  [FAIL] Search error: {e}")

    print(f"\nExercise 5: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Week 15 Lab: Final Integration - Test Suite")
    print("=" * 60)

    if MISSING_PACKAGES:
        print(f"\nWarning: Missing packages: {', '.join(MISSING_PACKAGES)}")
        print("Install with: pip install " + " ".join(MISSING_PACKAGES))

    results = {}

    # Run tests that don't require API calls first
    results['ex1'] = test_exercise_1()
    results['ex4'] = test_exercise_4()
    results['ex5'] = test_exercise_5()

    # API tests (slower, require network)
    print("\nNote: Tests 2 and 3 require network access and may take longer...")
    results['ex2'] = test_exercise_2()
    results['ex3'] = test_exercise_3()

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for ex, result in sorted(results.items()):
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {ex}: {status}")

    print(f"\nTotal: {passed}/{total} exercises passed")

    if passed == total:
        print("\nCongratulations! All tests passed!")
    else:
        print(f"\nKeep working! {total - passed} exercise(s) need attention.")

    return passed == total


def run_app():
    """Run the Flask application."""
    if not FLASK_AVAILABLE or not FOLIUM_AVAILABLE:
        print("Error: flask and folium packages required")
        print("Install with: pip install flask folium requests")
        return

    app = create_app()
    print("\nStarting Smart City Navigator...")
    print("Visit: http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, port=5000)


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--app":
            run_app()
        elif sys.argv[1] == "--test" and len(sys.argv) > 2:
            test_name = sys.argv[2]
            test_funcs = {
                'ex1': test_exercise_1,
                'ex2': test_exercise_2,
                'ex3': test_exercise_3,
                'ex4': test_exercise_4,
                'ex5': test_exercise_5,
            }
            if test_name in test_funcs:
                test_funcs[test_name]()
            else:
                print(f"Unknown test: {test_name}")
                print("Available: ex1, ex2, ex3, ex4, ex5")
        elif sys.argv[1] == "--help":
            print(__doc__)
        else:
            print("Unknown argument. Use --help for usage.")
    else:
        run_all_tests()


if __name__ == "__main__":
    main()
