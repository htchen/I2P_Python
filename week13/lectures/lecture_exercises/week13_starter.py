#!/usr/bin/env python3
"""
Week 13 Lab: Introduction to Flask (Web Server)
Starter Code with Test Suite

This file contains starter code for Flask exercises and tests
that verify your implementations WITHOUT running a web server.

Run: python week13_starter.py
Run specific test: python week13_starter.py --test ex1
Run Flask app: python week13_starter.py --app
"""

import sys
import os

# =============================================================================
# Exercise 1: Basic Routes
# =============================================================================

def create_basic_app():
    """
    Create a Flask app with basic routes.

    Requirements:
    1. Home route "/" returns "Welcome to Smart City Navigator!"
    2. About route "/about" returns "A Flask app to explore your city."
    3. Greeting route "/hello/<name>" returns "Hello, {name}!"

    Returns:
        Flask app instance
    """
    from flask import Flask

    app = Flask(__name__)

    # TODO: Create the home route
    @app.route("/")
    def home():
        # Return welcome message
        pass

    # TODO: Create the about route
    @app.route("/about")
    def about():
        # Return about message
        pass

    # TODO: Create the greeting route with name parameter
    @app.route("/hello/<name>")
    def greet(name):
        # Return greeting with name
        pass

    return app


# =============================================================================
# Exercise 2: Route Parameters
# =============================================================================

def create_params_app():
    """
    Create a Flask app demonstrating route parameters.

    Requirements:
    1. "/place/<name>" - Return f"Place: {name}"
    2. "/place/id/<int:place_id>" - Return f"Place ID: {place_id}"
    3. "/coords/<float:lat>/<float:lon>" - Return f"Coords: ({lat}, {lon})"

    Returns:
        Flask app instance
    """
    from flask import Flask

    app = Flask(__name__)

    # TODO: String parameter
    @app.route("/place/<name>")
    def show_place(name):
        pass

    # TODO: Integer parameter
    @app.route("/place/id/<int:place_id>")
    def show_place_by_id(place_id):
        pass

    # TODO: Float parameters
    @app.route("/coords/<float:lat>/<float:lon>")
    def show_coords(lat, lon):
        pass

    return app


# =============================================================================
# Exercise 3: JSON API
# =============================================================================

def create_api_app():
    """
    Create a Flask app that returns JSON data.

    Requirements:
    1. "/api/places" - Return all places as JSON
    2. "/api/places/<int:place_id>" - Return single place or 404
    3. "/api/categories" - Return list of unique categories

    The places data:
    [
        {"id": 1, "name": "Pizza Palace", "rating": 4.5, "category": "restaurant"},
        {"id": 2, "name": "Burger Barn", "rating": 4.2, "category": "restaurant"},
        {"id": 3, "name": "Central Park", "rating": 4.8, "category": "park"},
    ]

    Returns:
        Flask app instance
    """
    from flask import Flask, jsonify

    app = Flask(__name__)

    PLACES = [
        {"id": 1, "name": "Pizza Palace", "rating": 4.5, "category": "restaurant"},
        {"id": 2, "name": "Burger Barn", "rating": 4.2, "category": "restaurant"},
        {"id": 3, "name": "Central Park", "rating": 4.8, "category": "park"},
    ]

    # TODO: Return all places as JSON
    @app.route("/api/places")
    def get_places():
        pass

    # TODO: Return single place by ID or 404
    @app.route("/api/places/<int:place_id>")
    def get_place(place_id):
        pass

    # TODO: Return unique categories
    @app.route("/api/categories")
    def get_categories():
        pass

    return app


# =============================================================================
# Exercise 4: Templates
# =============================================================================

def create_template_app():
    """
    Create a Flask app using templates.

    Requirements:
    1. Home route renders a template with title and places
    2. Template shows places count
    3. Template loops through places

    Returns:
        Flask app instance
    """
    from flask import Flask, render_template_string

    app = Flask(__name__)

    PLACES = [
        {"name": "Pizza Palace", "rating": 4.5, "category": "restaurant"},
        {"name": "Central Park", "rating": 4.8, "category": "park"},
    ]

    # Template for testing
    INDEX_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head><title>{{ title }}</title></head>
    <body>
        <h1>{{ title }}</h1>
        <p>Total: {{ places | length }} places</p>
        <ul>
        {% for place in places %}
            <li>{{ place.name }} - {{ place.rating }}</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """

    # TODO: Render template with title and places
    @app.route("/")
    def home():
        pass

    return app


# =============================================================================
# Exercise 5: Form Handling (GET)
# =============================================================================

def create_search_app():
    """
    Create a Flask app with search functionality using GET.

    Requirements:
    1. "/search" shows search form
    2. "/search?q=pizza" filters places by name
    3. Search is case-insensitive

    Returns:
        Flask app instance
    """
    from flask import Flask, request, render_template_string

    app = Flask(__name__)

    PLACES = [
        {"name": "Pizza Palace", "rating": 4.5},
        {"name": "Pizza Hut", "rating": 4.0},
        {"name": "Burger Barn", "rating": 4.2},
    ]

    SEARCH_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <body>
        <form method="GET" action="/search">
            <input type="text" name="q" value="{{ query }}">
            <button>Search</button>
        </form>
        {% if results is defined %}
        <h2>Results for "{{ query }}"</h2>
        <ul>
        {% for place in results %}
            <li>{{ place.name }}</li>
        {% else %}
            <li>No results found</li>
        {% endfor %}
        </ul>
        {% endif %}
    </body>
    </html>
    """

    # TODO: Handle search with query parameter
    @app.route("/search")
    def search():
        # Get query from request.args
        # Filter places by name (case-insensitive)
        # Return template with results
        pass

    return app


# =============================================================================
# Exercise 6: Form Handling (POST)
# =============================================================================

def create_add_app():
    """
    Create a Flask app with form handling using POST.

    Requirements:
    1. GET "/add" shows empty form
    2. POST "/add" adds place to list
    3. Returns message on success

    Returns:
        Flask app instance
    """
    from flask import Flask, request, render_template_string

    app = Flask(__name__)

    PLACES = []

    ADD_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <body>
        {% if message %}
        <div class="message">{{ message }}</div>
        {% endif %}
        <form method="POST">
            <input type="text" name="name" placeholder="Name" required>
            <input type="number" name="rating" placeholder="Rating" step="0.1" min="0" max="5" required>
            <button>Add</button>
        </form>
        <h2>Places ({{ places | length }})</h2>
        <ul>
        {% for place in places %}
            <li>{{ place.name }} - {{ place.rating }}</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """

    # TODO: Handle GET (show form) and POST (add place)
    @app.route("/add", methods=["GET", "POST"])
    def add_place():
        pass

    return app


# =============================================================================
# Exercise 7: URL Building
# =============================================================================

def create_url_app():
    """
    Create a Flask app demonstrating url_for.

    Requirements:
    1. Navigation links use url_for
    2. Dynamic URLs with parameters work

    Returns:
        Flask app instance
    """
    from flask import Flask, url_for, render_template_string

    app = Flask(__name__)

    NAV_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <body>
        <nav>
            <a href="{{ url_for('home') }}">Home</a>
            <a href="{{ url_for('places') }}">Places</a>
            <a href="{{ url_for('place_detail', place_id=1) }}">Place 1</a>
        </nav>
        <h1>{{ page_name }}</h1>
    </body>
    </html>
    """

    @app.route("/")
    def home():
        return render_template_string(NAV_TEMPLATE, page_name="Home")

    @app.route("/places")
    def places():
        return render_template_string(NAV_TEMPLATE, page_name="Places")

    @app.route("/place/<int:place_id>")
    def place_detail(place_id):
        return render_template_string(NAV_TEMPLATE, page_name=f"Place {place_id}")

    return app


# =============================================================================
# Exercise 8: Complete Application
# =============================================================================

def create_complete_app():
    """
    Create a complete Flask application with all features.

    Requirements:
    1. Home page with featured places
    2. Places list with filtering
    3. Place detail page
    4. Search functionality
    5. Add new places

    Returns:
        Flask app instance
    """
    from flask import Flask, request, redirect, url_for, render_template_string

    app = Flask(__name__)

    PLACES = [
        {"id": 1, "name": "Pizza Palace", "rating": 4.5, "category": "restaurant"},
        {"id": 2, "name": "Burger Barn", "rating": 4.2, "category": "restaurant"},
        {"id": 3, "name": "Central Park", "rating": 4.8, "category": "park"},
    ]

    HOME = """
    <!DOCTYPE html>
    <html>
    <head><title>Home - Navigator</title></head>
    <body>
        <nav>
            <a href="/">Home</a>
            <a href="/places">Places</a>
            <a href="/search">Search</a>
        </nav>
        <main>
            <h1>Welcome!</h1>
            <h2>Top Rated</h2>
            {% for place in top_places %}
            <p>{{ place.name }} - {{ place.rating }}</p>
            {% endfor %}
        </main>
    </body>
    </html>
    """

    PLACES_PAGE = """
    <!DOCTYPE html>
    <html>
    <head><title>Places - Navigator</title></head>
    <body>
        <nav>
            <a href="/">Home</a>
            <a href="/places">Places</a>
            <a href="/search">Search</a>
        </nav>
        <main>
            <h1>All Places ({{ places | length }})</h1>
            {% for place in places %}
            <p><a href="/place/{{ place.id }}">{{ place.name }}</a> - {{ place.rating }}</p>
            {% endfor %}
        </main>
    </body>
    </html>
    """

    DETAIL = """
    <!DOCTYPE html>
    <html>
    <head><title>{{ place.name }} - Navigator</title></head>
    <body>
        <nav>
            <a href="/">Home</a>
            <a href="/places">Places</a>
            <a href="/search">Search</a>
        </nav>
        <main>
            <h1>{{ place.name }}</h1>
            <p>Rating: {{ place.rating }}</p>
            <p>Category: {{ place.category }}</p>
        </main>
    </body>
    </html>
    """

    SEARCH_PAGE = """
    <!DOCTYPE html>
    <html>
    <head><title>Search - Navigator</title></head>
    <body>
        <nav>
            <a href="/">Home</a>
            <a href="/places">Places</a>
            <a href="/search">Search</a>
        </nav>
        <main>
            <h1>Search</h1>
            <form method="GET">
                <input name="q" value="{{ query }}">
                <button>Search</button>
            </form>
            {% if results is defined %}
            <h2>Results</h2>
            {% for place in results %}
            <p>{{ place.name }}</p>
            {% else %}
            <p>No results</p>
            {% endfor %}
            {% endif %}
        </main>
    </body>
    </html>
    """

    @app.route("/")
    def home():
        top = sorted(PLACES, key=lambda p: p["rating"], reverse=True)[:3]
        return render_template_string(HOME, top_places=top)

    @app.route("/places")
    def places():
        category = request.args.get("category")
        if category:
            filtered = [p for p in PLACES if p["category"] == category]
        else:
            filtered = PLACES
        return render_template_string(PLACES_PAGE, places=filtered)

    @app.route("/place/<int:place_id>")
    def detail(place_id):
        place = next((p for p in PLACES if p["id"] == place_id), None)
        if not place:
            return "Not found", 404
        return render_template_string(DETAIL, place=place)

    @app.route("/search")
    def search():
        query = request.args.get("q", "")
        if query:
            results = [p for p in PLACES if query.lower() in p["name"].lower()]
            return render_template_string(SEARCH_PAGE, query=query, results=results)
        return render_template_string(SEARCH_PAGE, query="")

    return app


# =============================================================================
# Test Suite
# =============================================================================

def test_exercise_1():
    """Test basic routes."""
    print("\n" + "=" * 60)
    print("Testing Exercise 1: Basic Routes")
    print("=" * 60)

    tests_passed = 0
    tests_total = 0

    try:
        app = create_basic_app()
        client = app.test_client()

        # Test home route
        tests_total += 1
        response = client.get("/")
        if response.status_code == 200 and b"Welcome" in response.data:
            print("  ✓ Home route works")
            tests_passed += 1
        else:
            print(f"  ✗ Home route failed - got: {response.data[:50]}")

        # Test about route
        tests_total += 1
        response = client.get("/about")
        if response.status_code == 200 and b"Flask app" in response.data:
            print("  ✓ About route works")
            tests_passed += 1
        else:
            print(f"  ✗ About route failed")

        # Test greeting route
        tests_total += 1
        response = client.get("/hello/Alice")
        if response.status_code == 200 and b"Alice" in response.data:
            print("  ✓ Greeting route works")
            tests_passed += 1
        else:
            print(f"  ✗ Greeting route failed")

    except Exception as e:
        print(f"  ✗ Error: {e}")

    print(f"\nExercise 1: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_2():
    """Test route parameters."""
    print("\n" + "=" * 60)
    print("Testing Exercise 2: Route Parameters")
    print("=" * 60)

    tests_passed = 0
    tests_total = 0

    try:
        app = create_params_app()
        client = app.test_client()

        # Test string parameter
        tests_total += 1
        response = client.get("/place/Pizza_Palace")
        if response.status_code == 200 and b"Pizza_Palace" in response.data:
            print("  ✓ String parameter works")
            tests_passed += 1
        else:
            print(f"  ✗ String parameter failed")

        # Test integer parameter
        tests_total += 1
        response = client.get("/place/id/42")
        if response.status_code == 200 and b"42" in response.data:
            print("  ✓ Integer parameter works")
            tests_passed += 1
        else:
            print(f"  ✗ Integer parameter failed")

        # Test float parameters
        tests_total += 1
        response = client.get("/coords/25.033/121.565")
        if response.status_code == 200 and b"25.033" in response.data and b"121.565" in response.data:
            print("  ✓ Float parameters work")
            tests_passed += 1
        else:
            print(f"  ✗ Float parameters failed")

    except Exception as e:
        print(f"  ✗ Error: {e}")

    print(f"\nExercise 2: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_3():
    """Test JSON API."""
    print("\n" + "=" * 60)
    print("Testing Exercise 3: JSON API")
    print("=" * 60)

    tests_passed = 0
    tests_total = 0

    try:
        app = create_api_app()
        client = app.test_client()

        # Test get all places
        tests_total += 1
        response = client.get("/api/places")
        if response.status_code == 200:
            data = response.get_json()
            if isinstance(data, list) and len(data) == 3:
                print("  ✓ Get all places works")
                tests_passed += 1
            else:
                print(f"  ✗ Get all places returned wrong data")
        else:
            print(f"  ✗ Get all places failed")

        # Test get single place
        tests_total += 1
        response = client.get("/api/places/1")
        if response.status_code == 200:
            data = response.get_json()
            if data.get("name") == "Pizza Palace":
                print("  ✓ Get single place works")
                tests_passed += 1
            else:
                print(f"  ✗ Get single place returned wrong data")
        else:
            print(f"  ✗ Get single place failed")

        # Test 404 for missing place
        tests_total += 1
        response = client.get("/api/places/999")
        if response.status_code == 404:
            print("  ✓ 404 for missing place works")
            tests_passed += 1
        else:
            print(f"  ✗ Should return 404 for missing place")

        # Test get categories
        tests_total += 1
        response = client.get("/api/categories")
        if response.status_code == 200:
            data = response.get_json()
            if isinstance(data, list) and "restaurant" in data and "park" in data:
                print("  ✓ Get categories works")
                tests_passed += 1
            else:
                print(f"  ✗ Get categories returned wrong data")
        else:
            print(f"  ✗ Get categories failed")

    except Exception as e:
        print(f"  ✗ Error: {e}")

    print(f"\nExercise 3: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_4():
    """Test templates."""
    print("\n" + "=" * 60)
    print("Testing Exercise 4: Templates")
    print("=" * 60)

    tests_passed = 0
    tests_total = 0

    try:
        app = create_template_app()
        client = app.test_client()

        tests_total += 1
        response = client.get("/")
        if response.status_code == 200:
            html = response.data.decode()
            if "Pizza Palace" in html and "Central Park" in html and "2 places" in html:
                print("  ✓ Template renders correctly")
                tests_passed += 1
            else:
                print(f"  ✗ Template missing expected content")
        else:
            print(f"  ✗ Template route failed")

    except Exception as e:
        print(f"  ✗ Error: {e}")

    print(f"\nExercise 4: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_5():
    """Test search (GET)."""
    print("\n" + "=" * 60)
    print("Testing Exercise 5: Search (GET)")
    print("=" * 60)

    tests_passed = 0
    tests_total = 0

    try:
        app = create_search_app()
        client = app.test_client()

        # Test search form
        tests_total += 1
        response = client.get("/search")
        if response.status_code == 200 and b"form" in response.data:
            print("  ✓ Search form displays")
            tests_passed += 1
        else:
            print(f"  ✗ Search form failed")

        # Test search with results
        tests_total += 1
        response = client.get("/search?q=pizza")
        html = response.data.decode().lower()
        if "pizza palace" in html and "pizza hut" in html:
            print("  ✓ Search returns results")
            tests_passed += 1
        else:
            print(f"  ✗ Search results failed")

        # Test search case insensitive
        tests_total += 1
        response = client.get("/search?q=PIZZA")
        html = response.data.decode().lower()
        if "pizza palace" in html:
            print("  ✓ Search is case-insensitive")
            tests_passed += 1
        else:
            print(f"  ✗ Case-insensitive search failed")

    except Exception as e:
        print(f"  ✗ Error: {e}")

    print(f"\nExercise 5: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_6():
    """Test add form (POST)."""
    print("\n" + "=" * 60)
    print("Testing Exercise 6: Add Form (POST)")
    print("=" * 60)

    tests_passed = 0
    tests_total = 0

    try:
        app = create_add_app()
        client = app.test_client()

        # Test GET shows form
        tests_total += 1
        response = client.get("/add")
        if response.status_code == 200 and b"form" in response.data:
            print("  ✓ Add form displays")
            tests_passed += 1
        else:
            print(f"  ✗ Add form failed")

        # Test POST adds place
        tests_total += 1
        response = client.post("/add", data={"name": "Test Place", "rating": "4.5"})
        if response.status_code == 200 and b"Test Place" in response.data:
            print("  ✓ POST adds place")
            tests_passed += 1
        else:
            print(f"  ✗ POST add failed")

    except Exception as e:
        print(f"  ✗ Error: {e}")

    print(f"\nExercise 6: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_7():
    """Test URL building."""
    print("\n" + "=" * 60)
    print("Testing Exercise 7: URL Building")
    print("=" * 60)

    tests_passed = 0
    tests_total = 0

    try:
        app = create_url_app()
        client = app.test_client()

        # Test navigation links
        tests_total += 1
        response = client.get("/")
        html = response.data.decode()
        if 'href="/"' in html and 'href="/places"' in html and 'href="/place/1"' in html:
            print("  ✓ Navigation links work")
            tests_passed += 1
        else:
            print(f"  ✗ Navigation links failed")

        # Test all routes accessible
        tests_total += 1
        r1 = client.get("/")
        r2 = client.get("/places")
        r3 = client.get("/place/1")
        if r1.status_code == 200 and r2.status_code == 200 and r3.status_code == 200:
            print("  ✓ All routes accessible")
            tests_passed += 1
        else:
            print(f"  ✗ Some routes not accessible")

    except Exception as e:
        print(f"  ✗ Error: {e}")

    print(f"\nExercise 7: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_8():
    """Test complete application."""
    print("\n" + "=" * 60)
    print("Testing Exercise 8: Complete Application")
    print("=" * 60)

    tests_passed = 0
    tests_total = 0

    try:
        app = create_complete_app()
        client = app.test_client()

        # Test home
        tests_total += 1
        response = client.get("/")
        if response.status_code == 200 and b"Welcome" in response.data:
            print("  ✓ Home page works")
            tests_passed += 1
        else:
            print(f"  ✗ Home page failed")

        # Test places
        tests_total += 1
        response = client.get("/places")
        if response.status_code == 200 and b"Pizza Palace" in response.data:
            print("  ✓ Places page works")
            tests_passed += 1
        else:
            print(f"  ✗ Places page failed")

        # Test filter
        tests_total += 1
        response = client.get("/places?category=park")
        html = response.data.decode()
        if "Central Park" in html and "Pizza" not in html:
            print("  ✓ Category filter works")
            tests_passed += 1
        else:
            print(f"  ✗ Category filter failed")

        # Test detail
        tests_total += 1
        response = client.get("/place/1")
        if response.status_code == 200 and b"Pizza Palace" in response.data:
            print("  ✓ Detail page works")
            tests_passed += 1
        else:
            print(f"  ✗ Detail page failed")

        # Test search
        tests_total += 1
        response = client.get("/search?q=burger")
        if response.status_code == 200 and b"Burger Barn" in response.data:
            print("  ✓ Search works")
            tests_passed += 1
        else:
            print(f"  ✗ Search failed")

    except Exception as e:
        print(f"  ✗ Error: {e}")

    print(f"\nExercise 8: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Week 13 Lab: Flask Web Server - Test Suite")
    print("=" * 60)

    # Check if Flask is installed
    try:
        import flask
        print(f"Flask version: {flask.__version__}")
    except ImportError:
        print("Flask is not installed!")
        print("Install with: pip install flask")
        return False

    results = {
        'ex1': test_exercise_1(),
        'ex2': test_exercise_2(),
        'ex3': test_exercise_3(),
        'ex4': test_exercise_4(),
        'ex5': test_exercise_5(),
        'ex6': test_exercise_6(),
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
        print("\n🎉 All tests passed! Great job!")
    else:
        print(f"\n💪 Keep working! {total - passed} exercise(s) remaining.")

    return passed == total


def run_app():
    """Run the complete application."""
    print("Starting Flask application...")
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
            test_func = {
                'ex1': test_exercise_1,
                'ex2': test_exercise_2,
                'ex3': test_exercise_3,
                'ex4': test_exercise_4,
                'ex5': test_exercise_5,
                'ex6': test_exercise_6,
                'ex7': test_exercise_7,
                'ex8': test_exercise_8,
            }.get(test_name)

            if test_func:
                # Need Flask for tests
                try:
                    import flask
                    test_func()
                except ImportError:
                    print("Flask is required. Install with: pip install flask")
            else:
                print(f"Unknown test: {test_name}")
                print("Available: ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8")
        elif sys.argv[1] == "--help":
            print(__doc__)
        else:
            print("Unknown argument. Use --help for usage.")
    else:
        run_all_tests()
