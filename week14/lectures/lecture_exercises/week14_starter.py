#!/usr/bin/env python3
"""
Week 14 Lab: Interactive Maps with Folium
Starter Code with Test Suite

This file contains starter code for Folium exercises and tests.

Run: python week14_starter.py
Run specific test: python week14_starter.py --test ex1
Run Flask app: python week14_starter.py --app
"""

import sys
import os

# Check for required packages
try:
    import folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

try:
    from flask import Flask, render_template_string, request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False


# =============================================================================
# Exercise 1: Basic Map
# =============================================================================

def create_basic_map(center, zoom=14):
    """
    Create a basic Folium map.

    Args:
        center: [latitude, longitude] for map center
        zoom: Initial zoom level (1-18)

    Returns:
        folium.Map object
    """
    # TODO: Create and return a folium.Map
    # Hint: folium.Map(location=center, zoom_start=zoom)
    pass


# =============================================================================
# Exercise 2: Map with Markers
# =============================================================================

def add_markers_to_map(m, places):
    """
    Add markers to a map for a list of places.

    Args:
        m: folium.Map object
        places: List of dicts with 'name', 'coords', and optional 'description'

    Returns:
        The map with markers added
    """
    # TODO: Loop through places and add markers
    # Each marker should have:
    # - popup with name and description
    # - tooltip with name
    pass


# =============================================================================
# Exercise 3: Custom Icons
# =============================================================================

def get_icon_style(category):
    """
    Get icon style (color and icon name) for a category.

    Args:
        category: Category string (restaurant, cafe, park, museum, shopping)

    Returns:
        Dict with 'color' and 'icon' keys
    """
    # TODO: Define and return icon styles based on category
    # Example return: {"color": "red", "icon": "cutlery"}
    styles = {
        "restaurant": {"color": "red", "icon": "cutlery"},
        "cafe": {"color": "orange", "icon": "coffee"},
        "park": {"color": "green", "icon": "tree"},
        "museum": {"color": "blue", "icon": "university"},
        "shopping": {"color": "pink", "icon": "shopping-cart"},
    }
    return styles.get(category, {"color": "gray", "icon": "info"})


def add_categorized_markers(m, places):
    """
    Add markers with category-specific icons.

    Args:
        m: folium.Map object
        places: List of dicts with 'name', 'coords', 'category'

    Returns:
        The map with categorized markers
    """
    # TODO: Loop through places and add markers with custom icons
    # Use get_icon_style() to get the icon for each category
    pass


# =============================================================================
# Exercise 4: Drawing Routes
# =============================================================================

def draw_route(m, route_coords, color="blue", weight=5):
    """
    Draw a route line on the map.

    Args:
        m: folium.Map object
        route_coords: List of [lat, lon] coordinates
        color: Line color
        weight: Line thickness

    Returns:
        The map with route added
    """
    # TODO: Add a PolyLine to the map
    # Hint: folium.PolyLine(locations=route_coords, color=color, weight=weight)
    pass


def add_route_markers(m, start_coords, end_coords, start_name="Start", end_name="End"):
    """
    Add start and end markers for a route.

    Args:
        m: folium.Map object
        start_coords: [lat, lon] of start
        end_coords: [lat, lon] of end
        start_name: Popup text for start
        end_name: Popup text for end

    Returns:
        The map with route markers
    """
    # TODO: Add green marker at start with play icon
    # TODO: Add red marker at end with flag icon
    pass


# =============================================================================
# Exercise 5: Circles and Areas
# =============================================================================

def add_radius_circle(m, center, radius_meters, color="blue"):
    """
    Add a circle showing an area around a point.

    Args:
        m: folium.Map object
        center: [lat, lon] center point
        radius_meters: Radius in meters
        color: Circle color

    Returns:
        The map with circle added
    """
    # TODO: Add a Circle to the map
    # Hint: folium.Circle(location=center, radius=radius_meters, ...)
    pass


def add_rating_circles(m, places):
    """
    Add CircleMarkers sized by rating.

    Args:
        m: folium.Map object
        places: List of dicts with 'name', 'coords', 'rating'

    Returns:
        The map with circle markers
    """
    # TODO: Add CircleMarkers where:
    # - radius = rating * 3
    # - color = green if rating >= 4.5, orange if >= 4.0, else red
    pass


# =============================================================================
# Exercise 6: Layer Control
# =============================================================================

def create_layered_map(center, layer_data):
    """
    Create a map with multiple toggleable layers.

    Args:
        center: [lat, lon] for map center
        layer_data: Dict mapping layer name to list of places

    Returns:
        folium.Map with layers and layer control
    """
    # TODO: Create map
    # TODO: Create FeatureGroup for each layer
    # TODO: Add markers to each group
    # TODO: Add groups to map
    # TODO: Add LayerControl
    pass


# =============================================================================
# Exercise 7: Flask Integration
# =============================================================================

def create_flask_map_app():
    """
    Create a Flask app that displays a Folium map.

    Returns:
        Flask app instance
    """
    app = Flask(__name__)

    PLACES = [
        {"id": 1, "name": "Taipei 101", "coords": [25.0330, 121.5654],
         "rating": 4.7, "category": "landmark"},
        {"id": 2, "name": "Din Tai Fung", "coords": [25.0339, 121.5645],
         "rating": 4.9, "category": "restaurant"},
        {"id": 3, "name": "Shilin Night Market", "coords": [25.0878, 121.5241],
         "rating": 4.5, "category": "market"},
        {"id": 4, "name": "National Palace Museum", "coords": [25.1024, 121.5485],
         "rating": 4.8, "category": "museum"},
    ]

    TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Map Application</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; }
            header {
                background: #2c3e50;
                color: white;
                padding: 1rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .controls { display: flex; gap: 1rem; }
            select, button {
                padding: 0.5rem;
                border-radius: 4px;
                border: none;
            }
            button { background: #3498db; color: white; cursor: pointer; }
            #map-container { height: calc(100vh - 60px); }
            .info {
                padding: 0.5rem 1rem;
                background: #ecf0f1;
                font-size: 0.9rem;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Smart City Navigator</h1>
            <div class="controls">
                <form method="GET">
                    <select name="category">
                        <option value="">All Categories</option>
                        <option value="landmark" {{ 'selected' if category == 'landmark' else '' }}>Landmarks</option>
                        <option value="restaurant" {{ 'selected' if category == 'restaurant' else '' }}>Restaurants</option>
                        <option value="market" {{ 'selected' if category == 'market' else '' }}>Markets</option>
                        <option value="museum" {{ 'selected' if category == 'museum' else '' }}>Museums</option>
                    </select>
                    <button type="submit">Filter</button>
                </form>
            </div>
        </header>
        <div class="info">
            Showing {{ place_count }} places
        </div>
        <div id="map-container">
            {{ map_html | safe }}
        </div>
    </body>
    </html>
    """

    @app.route("/")
    def show_map():
        category = request.args.get("category", "")

        # Filter places
        if category:
            filtered = [p for p in PLACES if p["category"] == category]
        else:
            filtered = PLACES

        # Calculate center
        if filtered:
            avg_lat = sum(p["coords"][0] for p in filtered) / len(filtered)
            avg_lon = sum(p["coords"][1] for p in filtered) / len(filtered)
            center = [avg_lat, avg_lon]
        else:
            center = [25.0500, 121.5500]

        # Create map
        m = folium.Map(location=center, zoom_start=12, tiles="CartoDB positron")

        # Category styles
        styles = {
            "landmark": {"color": "purple", "icon": "building"},
            "restaurant": {"color": "red", "icon": "cutlery"},
            "market": {"color": "orange", "icon": "shopping-cart"},
            "museum": {"color": "blue", "icon": "university"},
        }

        # Add markers
        for place in filtered:
            style = styles.get(place["category"], {"color": "gray", "icon": "info"})

            popup_html = f"""
            <div style="min-width: 150px;">
                <h4 style="margin: 0 0 5px 0;">{place['name']}</h4>
                <p style="margin: 0;">Rating: {'⭐' * int(place['rating'])} {place['rating']}</p>
            </div>
            """

            folium.Marker(
                location=place["coords"],
                popup=folium.Popup(popup_html, max_width=200),
                tooltip=place["name"],
                icon=folium.Icon(color=style["color"], icon=style["icon"], prefix="fa")
            ).add_to(m)

        map_html = m._repr_html_()

        return render_template_string(
            TEMPLATE,
            map_html=map_html,
            category=category,
            place_count=len(filtered)
        )

    return app


# =============================================================================
# Exercise 8: Complete Application
# =============================================================================

def create_complete_app():
    """
    Create a complete Smart City Navigator map application.

    Features:
    - Display places with category icons
    - Filter by category
    - Show route between places
    """
    app = Flask(__name__)

    PLACES = [
        {"id": 1, "name": "Taipei 101", "coords": [25.0330, 121.5654],
         "rating": 4.7, "category": "landmark"},
        {"id": 2, "name": "Din Tai Fung", "coords": [25.0339, 121.5645],
         "rating": 4.9, "category": "restaurant"},
        {"id": 3, "name": "Shilin Night Market", "coords": [25.0878, 121.5241],
         "rating": 4.5, "category": "market"},
        {"id": 4, "name": "National Palace Museum", "coords": [25.1024, 121.5485],
         "rating": 4.8, "category": "museum"},
        {"id": 5, "name": "Taipei Main Station", "coords": [25.0478, 121.5170],
         "rating": 4.2, "category": "transport"},
    ]

    # Sample routes (in real app, use OSRM API)
    ROUTES = {
        (1, 5): [[25.033, 121.565], [25.038, 121.545], [25.043, 121.530], [25.048, 121.517]],
        (1, 3): [[25.033, 121.565], [25.050, 121.540], [25.070, 121.530], [25.088, 121.524]],
    }

    TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart City Navigator</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, sans-serif; }
            header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1rem 2rem;
            }
            .toolbar {
                background: #f8f9fa;
                padding: 1rem;
                border-bottom: 1px solid #ddd;
                display: flex;
                gap: 1rem;
                flex-wrap: wrap;
            }
            select, button {
                padding: 0.5rem 1rem;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            button { background: #667eea; color: white; border: none; cursor: pointer; }
            #map-container { height: calc(100vh - 130px); }
        </style>
    </head>
    <body>
        <header>
            <h1>Smart City Navigator</h1>
        </header>
        <div class="toolbar">
            <form method="GET" style="display: flex; gap: 0.5rem;">
                <select name="category">
                    <option value="">All Categories</option>
                    {% for cat in categories %}
                    <option value="{{ cat }}" {{ 'selected' if category == cat else '' }}>{{ cat | title }}</option>
                    {% endfor %}
                </select>
                <select name="start">
                    <option value="">Route Start</option>
                    {% for p in places %}
                    <option value="{{ p.id }}" {{ 'selected' if start == p.id else '' }}>{{ p.name }}</option>
                    {% endfor %}
                </select>
                <select name="end">
                    <option value="">Route End</option>
                    {% for p in places %}
                    <option value="{{ p.id }}" {{ 'selected' if end == p.id else '' }}>{{ p.name }}</option>
                    {% endfor %}
                </select>
                <button type="submit">Apply</button>
            </form>
            <span>{{ place_count }} places</span>
        </div>
        <div id="map-container">
            {{ map_html | safe }}
        </div>
    </body>
    </html>
    """

    @app.route("/")
    def index():
        category = request.args.get("category", "")
        start_id = request.args.get("start", 0, type=int)
        end_id = request.args.get("end", 0, type=int)

        # Filter places
        if category:
            filtered = [p for p in PLACES if p["category"] == category]
        else:
            filtered = PLACES

        # Calculate center
        if filtered:
            avg_lat = sum(p["coords"][0] for p in filtered) / len(filtered)
            avg_lon = sum(p["coords"][1] for p in filtered) / len(filtered)
            center = [avg_lat, avg_lon]
        else:
            center = [25.05, 121.55]

        # Create map
        m = folium.Map(location=center, zoom_start=12, tiles="CartoDB positron")

        # Category styles
        styles = {
            "landmark": {"color": "purple", "icon": "building"},
            "restaurant": {"color": "red", "icon": "cutlery"},
            "market": {"color": "orange", "icon": "shopping-cart"},
            "museum": {"color": "blue", "icon": "university"},
            "transport": {"color": "gray", "icon": "train"},
        }

        # Add markers
        for place in filtered:
            style = styles.get(place["category"], {"color": "gray", "icon": "info"})

            popup_html = f"""
            <b>{place['name']}</b><br>
            {'⭐' * int(place['rating'])} {place['rating']}
            """

            folium.Marker(
                location=place["coords"],
                popup=popup_html,
                tooltip=place["name"],
                icon=folium.Icon(color=style["color"], icon=style["icon"], prefix="fa")
            ).add_to(m)

        # Add route if both start and end are selected
        if start_id and end_id and start_id != end_id:
            route_key = (start_id, end_id)
            route_coords = ROUTES.get(route_key) or ROUTES.get((end_id, start_id))

            if route_coords:
                folium.PolyLine(
                    locations=route_coords,
                    color="#667eea",
                    weight=5,
                    opacity=0.8
                ).add_to(m)

                # Start marker
                start_place = next((p for p in PLACES if p["id"] == start_id), None)
                end_place = next((p for p in PLACES if p["id"] == end_id), None)

                if start_place:
                    folium.Marker(
                        start_place["coords"],
                        popup=f"Start: {start_place['name']}",
                        icon=folium.Icon(color="green", icon="play", prefix="fa")
                    ).add_to(m)

                if end_place:
                    folium.Marker(
                        end_place["coords"],
                        popup=f"End: {end_place['name']}",
                        icon=folium.Icon(color="red", icon="flag", prefix="fa")
                    ).add_to(m)

        map_html = m._repr_html_()
        categories = sorted(set(p["category"] for p in PLACES))

        return render_template_string(
            TEMPLATE,
            map_html=map_html,
            category=category,
            categories=categories,
            places=PLACES,
            place_count=len(filtered),
            start=start_id,
            end=end_id
        )

    return app


# =============================================================================
# Test Suite
# =============================================================================

def test_exercise_1():
    """Test basic map creation."""
    print("\n" + "=" * 60)
    print("Testing Exercise 1: Basic Map")
    print("=" * 60)

    if not FOLIUM_AVAILABLE:
        print("  ✗ Folium not installed")
        return False

    tests_passed = 0
    tests_total = 0

    # Test map creation
    tests_total += 1
    try:
        m = create_basic_map([25.033, 121.565], zoom=14)
        if m is not None and isinstance(m, folium.Map):
            print("  ✓ Basic map created successfully")
            tests_passed += 1
        else:
            print("  ✗ create_basic_map should return a folium.Map")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    print(f"\nExercise 1: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_2():
    """Test markers."""
    print("\n" + "=" * 60)
    print("Testing Exercise 2: Markers")
    print("=" * 60)

    if not FOLIUM_AVAILABLE:
        print("  ✗ Folium not installed")
        return False

    tests_passed = 0
    tests_total = 0

    places = [
        {"name": "Place 1", "coords": [25.033, 121.565], "description": "Test"},
        {"name": "Place 2", "coords": [25.040, 121.560], "description": "Test 2"},
    ]

    tests_total += 1
    try:
        m = folium.Map(location=[25.035, 121.560], zoom_start=13)
        result = add_markers_to_map(m, places)
        if result is not None:
            print("  ✓ Markers added to map")
            tests_passed += 1
        else:
            print("  ✗ add_markers_to_map should return the map")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    print(f"\nExercise 2: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_3():
    """Test custom icons."""
    print("\n" + "=" * 60)
    print("Testing Exercise 3: Custom Icons")
    print("=" * 60)

    tests_passed = 0
    tests_total = 0

    # Test icon styles
    tests_total += 1
    try:
        style = get_icon_style("restaurant")
        if style["color"] == "red" and style["icon"] == "cutlery":
            print("  ✓ Restaurant icon style correct")
            tests_passed += 1
        else:
            print("  ✗ Restaurant should have red color and cutlery icon")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    tests_total += 1
    try:
        style = get_icon_style("park")
        if style["color"] == "green" and style["icon"] == "tree":
            print("  ✓ Park icon style correct")
            tests_passed += 1
        else:
            print("  ✗ Park should have green color and tree icon")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    tests_total += 1
    try:
        style = get_icon_style("unknown")
        if "color" in style and "icon" in style:
            print("  ✓ Unknown category returns default style")
            tests_passed += 1
        else:
            print("  ✗ Unknown category should return default style")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    print(f"\nExercise 3: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_4():
    """Test routes."""
    print("\n" + "=" * 60)
    print("Testing Exercise 4: Routes")
    print("=" * 60)

    if not FOLIUM_AVAILABLE:
        print("  ✗ Folium not installed")
        return False

    tests_passed = 0
    tests_total = 0

    route_coords = [[25.033, 121.565], [25.040, 121.550], [25.048, 121.517]]

    tests_total += 1
    try:
        m = folium.Map(location=[25.040, 121.540], zoom_start=13)
        result = draw_route(m, route_coords)
        if result is not None:
            print("  ✓ Route drawn on map")
            tests_passed += 1
        else:
            print("  ✗ draw_route should return the map")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    print(f"\nExercise 4: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_7():
    """Test Flask integration."""
    print("\n" + "=" * 60)
    print("Testing Exercise 7: Flask Integration")
    print("=" * 60)

    if not FOLIUM_AVAILABLE or not FLASK_AVAILABLE:
        print("  ✗ Folium or Flask not installed")
        return False

    tests_passed = 0
    tests_total = 0

    tests_total += 1
    try:
        app = create_flask_map_app()
        client = app.test_client()
        response = client.get("/")

        if response.status_code == 200:
            print("  ✓ Flask app responds to /")
            tests_passed += 1
        else:
            print(f"  ✗ Flask app returned status {response.status_code}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    tests_total += 1
    try:
        response = client.get("/")
        html = response.data.decode()

        if "leaflet" in html.lower() or "folium" in html.lower():
            print("  ✓ Response contains map")
            tests_passed += 1
        else:
            print("  ✗ Response should contain map HTML")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    tests_total += 1
    try:
        response = client.get("/?category=restaurant")
        if response.status_code == 200:
            print("  ✓ Category filter works")
            tests_passed += 1
        else:
            print("  ✗ Category filter failed")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    print(f"\nExercise 7: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_8():
    """Test complete application."""
    print("\n" + "=" * 60)
    print("Testing Exercise 8: Complete Application")
    print("=" * 60)

    if not FOLIUM_AVAILABLE or not FLASK_AVAILABLE:
        print("  ✗ Folium or Flask not installed")
        return False

    tests_passed = 0
    tests_total = 0

    try:
        app = create_complete_app()
        client = app.test_client()

        # Test home page
        tests_total += 1
        response = client.get("/")
        if response.status_code == 200 and b"Smart City" in response.data:
            print("  ✓ Home page works")
            tests_passed += 1
        else:
            print("  ✗ Home page failed")

        # Test category filter
        tests_total += 1
        response = client.get("/?category=landmark")
        if response.status_code == 200:
            print("  ✓ Category filter works")
            tests_passed += 1
        else:
            print("  ✗ Category filter failed")

        # Test route display
        tests_total += 1
        response = client.get("/?start=1&end=5")
        if response.status_code == 200:
            print("  ✓ Route parameters accepted")
            tests_passed += 1
        else:
            print("  ✗ Route display failed")

    except Exception as e:
        print(f"  ✗ Error: {e}")

    print(f"\nExercise 8: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Week 14 Lab: Folium Maps - Test Suite")
    print("=" * 60)

    if not FOLIUM_AVAILABLE:
        print("Folium is not installed!")
        print("Install with: pip install folium")
        return False

    if not FLASK_AVAILABLE:
        print("Flask is not installed!")
        print("Install with: pip install flask")

    results = {
        'ex1': test_exercise_1(),
        'ex3': test_exercise_3(),  # Icon styles (no folium needed for basic test)
        'ex7': test_exercise_7(),
        'ex8': test_exercise_8(),
    }

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for ex, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {ex}: {status}")

    print(f"\nTotal: {passed}/{total} exercises passed")

    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n💪 Keep working! {total - passed} exercise(s) remaining.")

    return passed == total


def run_app():
    """Run the complete Flask application."""
    if not FOLIUM_AVAILABLE or not FLASK_AVAILABLE:
        print("Error: folium and flask are required")
        print("Install with: pip install folium flask")
        return

    print("Starting Smart City Navigator...")
    print("Visit: http://localhost:5000")
    print("Press Ctrl+C to stop")

    app = create_complete_app()
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--app":
            run_app()
        elif sys.argv[1] == "--test" and len(sys.argv) > 2:
            test_name = sys.argv[2]
            test_funcs = {
                'ex1': test_exercise_1,
                'ex3': test_exercise_3,
                'ex7': test_exercise_7,
                'ex8': test_exercise_8,
            }
            if test_name in test_funcs:
                test_funcs[test_name]()
            else:
                print(f"Unknown test: {test_name}")
                print("Available: ex1, ex3, ex7, ex8")
        elif sys.argv[1] == "--help":
            print(__doc__)
        else:
            print("Unknown argument. Use --help for usage.")
    else:
        run_all_tests()
