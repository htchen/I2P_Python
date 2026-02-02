#!/usr/bin/env python3
"""
Week 13: Introduction to Flask (Web Server)
Interactive Examples

This file demonstrates Flask concepts through runnable examples.
Each example can be run independently.

Usage:
    python examples.py              # Run demo selection menu
    python examples.py --demo N     # Run specific demo (1-7)
    python examples.py --all        # Show all code examples (no server)
"""

import sys
import os
import time
import tempfile
import shutil

# =============================================================================
# Demo 1: Minimal Flask App
# =============================================================================

DEMO_1_CODE = '''
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    """Home page."""
    return "Hello, World!"

@app.route("/about")
def about():
    """About page."""
    return "This is the Smart City Navigator!"

@app.route("/greet/<name>")
def greet(name):
    """Greet a user by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    print("Starting minimal Flask app...")
    print("Visit: http://localhost:5000")
    print("Routes available:")
    print("  - http://localhost:5000/")
    print("  - http://localhost:5000/about")
    print("  - http://localhost:5000/greet/Alice")
    print("Press Ctrl+C to stop")
    app.run(debug=True, port=5000)
'''


# =============================================================================
# Demo 2: Route Parameters
# =============================================================================

DEMO_2_CODE = '''
from flask import Flask

app = Flask(__name__)

# String parameter (default)
@app.route("/place/<name>")
def show_place(name):
    """Show place by name."""
    return f"<h1>Place: {name}</h1>"

# Integer parameter
@app.route("/place/id/<int:place_id>")
def show_place_by_id(place_id):
    """Show place by ID."""
    return f"<h1>Place ID: {place_id}</h1><p>Type: {type(place_id).__name__}</p>"

# Float parameters
@app.route("/location/<float:lat>/<float:lon>")
def show_location(lat, lon):
    """Show a location by coordinates."""
    return f"""
    <h1>Location</h1>
    <p>Latitude: {lat}</p>
    <p>Longitude: {lon}</p>
    """

# Multiple parameters
@app.route("/search/<category>/<int:limit>")
def search(category, limit):
    """Search with category and limit."""
    return f"""
    <h1>Search Results</h1>
    <p>Category: {category}</p>
    <p>Limit: {limit} results</p>
    """

if __name__ == "__main__":
    print("Starting route parameters demo...")
    print("Visit: http://localhost:5000")
    print("Try these routes:")
    print("  - http://localhost:5000/place/Pizza_Palace")
    print("  - http://localhost:5000/place/id/42")
    print("  - http://localhost:5000/location/25.033/121.565")
    print("  - http://localhost:5000/search/restaurant/10")
    print("Press Ctrl+C to stop")
    app.run(debug=True, port=5000)
'''


# =============================================================================
# Demo 3: Returning JSON (API Style)
# =============================================================================

DEMO_3_CODE = '''
from flask import Flask, jsonify

app = Flask(__name__)

# Sample data
PLACES = [
    {"id": 1, "name": "Pizza Palace", "rating": 4.5, "category": "restaurant"},
    {"id": 2, "name": "Burger Barn", "rating": 4.2, "category": "restaurant"},
    {"id": 3, "name": "Central Park", "rating": 4.8, "category": "park"},
    {"id": 4, "name": "City Museum", "rating": 4.6, "category": "museum"},
]

@app.route("/")
def home():
    """API documentation."""
    return """
    <h1>Places API</h1>
    <ul>
        <li><a href="/api/places">/api/places</a> - All places</li>
        <li><a href="/api/places/1">/api/places/1</a> - Place by ID</li>
        <li><a href="/api/categories">/api/categories</a> - All categories</li>
    </ul>
    """

@app.route("/api/places")
def get_places():
    """Return all places as JSON."""
    return jsonify(PLACES)

@app.route("/api/places/<int:place_id>")
def get_place(place_id):
    """Return a specific place by ID."""
    for place in PLACES:
        if place["id"] == place_id:
            return jsonify(place)
    return jsonify({"error": "Place not found"}), 404

@app.route("/api/categories")
def get_categories():
    """Return unique categories."""
    categories = list(set(p["category"] for p in PLACES))
    return jsonify(categories)

if __name__ == "__main__":
    print("Starting JSON API demo...")
    print("Visit: http://localhost:5000")
    print("API Endpoints:")
    print("  - http://localhost:5000/api/places")
    print("  - http://localhost:5000/api/places/1")
    print("  - http://localhost:5000/api/categories")
    print("Press Ctrl+C to stop")
    app.run(debug=True, port=5000)
'''


# =============================================================================
# Demo 4: Templates with Jinja2
# =============================================================================

DEMO_4_CODE = '''
import os
from flask import Flask, render_template_string

app = Flask(__name__)

# We use render_template_string for this demo (no external files needed)
# In real apps, use render_template with .html files

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .place-card {
            border: 1px solid #ddd;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
        }
        .rating { color: #f5a623; }
        .excellent { background: #d4edda; }
        .good { background: #fff3cd; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>

    <p>Welcome, {{ user_name | default("Guest") }}!</p>

    <h2>Places ({{ places | length }})</h2>

    {% for place in places %}
    <div class="place-card {% if place.rating >= 4.5 %}excellent{% elif place.rating >= 4.0 %}good{% endif %}">
        <h3>{{ loop.index }}. {{ place.name }}</h3>
        <p class="rating">
            Rating: {{ "★" * (place.rating | int) }} {{ place.rating }}
        </p>
        <p>Category: {{ place.category | title }}</p>
    </div>
    {% else %}
    <p>No places found.</p>
    {% endfor %}

    <hr>
    <h2>Template Features Demo</h2>

    <h3>Filters:</h3>
    <ul>
        <li>Upper: {{ "hello" | upper }}</li>
        <li>Title: {{ "hello world" | title }}</li>
        <li>Length: {{ places | length }} places</li>
        <li>First: {{ places | first | attr("name") }}</li>
        <li>Round: {{ 3.14159 | round(2) }}</li>
    </ul>

    <h3>Conditionals:</h3>
    {% if show_secret %}
        <p>Secret message: You found the secret!</p>
    {% else %}
        <p>No secret here.</p>
    {% endif %}

</body>
</html>
"""

# Sample data
PLACES = [
    {"name": "Pizza Palace", "rating": 4.5, "category": "restaurant"},
    {"name": "Burger Barn", "rating": 4.2, "category": "restaurant"},
    {"name": "Central Park", "rating": 4.8, "category": "park"},
]

@app.route("/")
def home():
    """Render the template with data."""
    return render_template_string(
        INDEX_TEMPLATE,
        title="Smart City Navigator",
        user_name="Alice",
        places=PLACES,
        show_secret=True
    )

@app.route("/guest")
def guest():
    """Render without user name (uses default)."""
    return render_template_string(
        INDEX_TEMPLATE,
        title="Guest View",
        places=PLACES,
        show_secret=False
    )

if __name__ == "__main__":
    print("Starting Jinja2 templates demo...")
    print("Visit: http://localhost:5000")
    print("Routes:")
    print("  - http://localhost:5000/ (logged in view)")
    print("  - http://localhost:5000/guest (guest view)")
    print("Press Ctrl+C to stop")
    app.run(debug=True, port=5000)
'''


# =============================================================================
# Demo 5: Forms and User Input
# =============================================================================

DEMO_5_CODE = '''
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Sample place data
PLACES = [
    {"id": 1, "name": "Pizza Palace", "rating": 4.5, "category": "restaurant"},
    {"id": 2, "name": "Pizza Hut", "rating": 4.0, "category": "restaurant"},
    {"id": 3, "name": "Burger Barn", "rating": 4.2, "category": "restaurant"},
    {"id": 4, "name": "Central Park", "rating": 4.8, "category": "park"},
    {"id": 5, "name": "City Museum", "rating": 4.6, "category": "museum"},
]

SEARCH_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Search Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .form-group { margin: 15px 0; }
        input[type="text"] { padding: 10px; width: 300px; font-size: 16px; }
        button { padding: 10px 20px; font-size: 16px; }
        .result { padding: 10px; margin: 5px 0; background: #f0f0f0; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Search Places</h1>

    <h2>Method 1: POST Form</h2>
    <form method="POST" action="/search">
        <div class="form-group">
            <input type="text" name="query" placeholder="Search..." required>
            <button type="submit">Search (POST)</button>
        </div>
    </form>

    <h2>Method 2: GET Form</h2>
    <form method="GET" action="/filter">
        <div class="form-group">
            <input type="text" name="q" placeholder="Search..." required>
            <button type="submit">Search (GET)</button>
        </div>
    </form>
    <p><small>Notice the query appears in the URL with GET</small></p>

    {% if results is defined %}
    <h2>Results for "{{ query }}"</h2>
    {% if results %}
        <p>Found {{ results | length }} place(s):</p>
        {% for place in results %}
        <div class="result">
            <strong>{{ place.name }}</strong> - {{ place.rating }} stars
            ({{ place.category }})
        </div>
        {% endfor %}
    {% else %}
        <p>No places found matching "{{ query }}"</p>
    {% endif %}
    {% endif %}
</body>
</html>
"""

def search_places(query):
    """Search places by name (case-insensitive)."""
    query = query.lower()
    return [p for p in PLACES if query in p["name"].lower()]

@app.route("/")
def home():
    """Show search form."""
    return render_template_string(SEARCH_TEMPLATE)

@app.route("/search", methods=["POST"])
def search_post():
    """Handle POST form submission."""
    query = request.form["query"]
    results = search_places(query)
    return render_template_string(SEARCH_TEMPLATE, query=query, results=results)

@app.route("/filter")
def search_get():
    """Handle GET request with query parameter."""
    query = request.args.get("q", "")
    if query:
        results = search_places(query)
        return render_template_string(SEARCH_TEMPLATE, query=query, results=results)
    return render_template_string(SEARCH_TEMPLATE)

if __name__ == "__main__":
    print("Starting forms demo...")
    print("Visit: http://localhost:5000")
    print("This demo shows:")
    print("  - POST forms (data in request body)")
    print("  - GET forms (data in URL)")
    print("Try searching for 'pizza' or 'park'")
    print("Press Ctrl+C to stop")
    app.run(debug=True, port=5000)
'''


# =============================================================================
# Demo 6: Template Inheritance
# =============================================================================

DEMO_6_CODE = '''
from flask import Flask, render_template_string

app = Flask(__name__)

# Base template - defines the common structure
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Smart City Navigator{% endblock %}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; }

        nav {
            background: #2c3e50;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
        }
        nav a { color: white; text-decoration: none; margin-right: 1rem; }
        nav a:hover { color: #3498db; }
        nav .logo { font-weight: bold; font-size: 1.2rem; }

        main {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }

        footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 1rem;
            position: fixed;
            bottom: 0;
            width: 100%;
        }

        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            margin: 5px;
        }

        {% block extra_css %}{% endblock %}
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo">Smart City Navigator</a>
        <div>
            <a href="/">Home</a>
            <a href="/places">Places</a>
            <a href="/about">About</a>
        </div>
    </nav>

    <main>
        {% block content %}
        <!-- Child templates fill this in -->
        {% endblock %}
    </main>

    <footer>
        <p>&copy; 2024 Smart City Navigator</p>
    </footer>
</body>
</html>
"""

# Child templates extend the base
HOME_TEMPLATE = """
{% extends base %}

{% block title %}Home - Smart City Navigator{% endblock %}

{% block extra_css %}
.hero {
    text-align: center;
    padding: 3rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 8px;
    margin-bottom: 2rem;
}
{% endblock %}

{% block content %}
<div class="hero">
    <h1>Welcome to Smart City Navigator</h1>
    <p>Discover amazing places in your city!</p>
</div>

<h2>Quick Links</h2>
<a href="/places" class="btn">View Places</a>
<a href="/about" class="btn">About Us</a>
{% endblock %}
"""

PLACES_TEMPLATE = """
{% extends base %}

{% block title %}Places - Smart City Navigator{% endblock %}

{% block extra_css %}
.place-card {
    border: 1px solid #ddd;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 8px;
}
{% endblock %}

{% block content %}
<h1>All Places</h1>

{% for place in places %}
<div class="place-card">
    <h3>{{ place.name }}</h3>
    <p>Rating: {{ place.rating }} / 5.0</p>
    <p>Category: {{ place.category | title }}</p>
</div>
{% endfor %}
{% endblock %}
"""

ABOUT_TEMPLATE = """
{% extends base %}

{% block title %}About - Smart City Navigator{% endblock %}

{% block content %}
<h1>About Us</h1>
<p>Smart City Navigator helps you discover the best places in your city.</p>
<p>Built with Flask and Python.</p>

<h2>Features</h2>
<ul>
    <li>Search for places</li>
    <li>Filter by category</li>
    <li>View ratings and details</li>
</ul>

<a href="/" class="btn">Back to Home</a>
{% endblock %}
"""

PLACES = [
    {"name": "Pizza Palace", "rating": 4.5, "category": "restaurant"},
    {"name": "Central Park", "rating": 4.8, "category": "park"},
    {"name": "City Museum", "rating": 4.6, "category": "museum"},
]

@app.route("/")
def home():
    return render_template_string(HOME_TEMPLATE, base=BASE_TEMPLATE)

@app.route("/places")
def places():
    return render_template_string(PLACES_TEMPLATE, base=BASE_TEMPLATE, places=PLACES)

@app.route("/about")
def about():
    return render_template_string(ABOUT_TEMPLATE, base=BASE_TEMPLATE)

if __name__ == "__main__":
    print("Starting template inheritance demo...")
    print("Visit: http://localhost:5000")
    print("Navigate between pages to see:")
    print("  - Common header/footer (from base template)")
    print("  - Different content (from child templates)")
    print("Press Ctrl+C to stop")
    app.run(debug=True, port=5000)
'''


# =============================================================================
# Demo 7: Complete Mini App
# =============================================================================

DEMO_7_CODE = '''
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# In-memory database
PLACES = [
    {"id": 1, "name": "Pizza Palace", "rating": 4.5, "category": "restaurant"},
    {"id": 2, "name": "Burger Barn", "rating": 4.2, "category": "restaurant"},
    {"id": 3, "name": "Central Park", "rating": 4.8, "category": "park"},
    {"id": 4, "name": "City Museum", "rating": 4.6, "category": "museum"},
    {"id": 5, "name": "Coffee Corner", "rating": 4.3, "category": "cafe"},
]

NEXT_ID = 6

# Templates
BASE = """
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Navigator{% endblock %}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #f5f5f5; }
        nav { background: #2c3e50; padding: 1rem 2rem; }
        nav a { color: white; text-decoration: none; margin-right: 1.5rem; }
        nav a:hover { color: #3498db; }
        main { max-width: 900px; margin: 2rem auto; padding: 0 1rem; }
        h1 { margin-bottom: 1.5rem; color: #2c3e50; }
        .card { background: white; border-radius: 8px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .btn { display: inline-block; padding: 8px 16px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; border: none; cursor: pointer; font-size: 14px; }
        .btn:hover { background: #2980b9; }
        .btn-danger { background: #e74c3c; }
        .btn-danger:hover { background: #c0392b; }
        .rating { color: #f39c12; }
        .category { background: #ecf0f1; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
        .form-group { margin: 1rem 0; }
        .form-group label { display: block; margin-bottom: 0.5rem; font-weight: bold; }
        .form-group input, .form-group select { padding: 8px; width: 100%; max-width: 300px; border: 1px solid #ddd; border-radius: 4px; }
        .filters { margin: 1rem 0; }
        .filters a { margin-right: 1rem; color: #666; text-decoration: none; }
        .filters a.active { color: #3498db; font-weight: bold; }
        .message { padding: 1rem; margin: 1rem 0; border-radius: 4px; }
        .message.success { background: #d4edda; color: #155724; }
        .message.error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <nav>
        <a href="/" style="font-weight: bold; font-size: 1.2rem;">Navigator</a>
        <a href="/">Home</a>
        <a href="/places">Places</a>
        <a href="/add">Add Place</a>
        <a href="/search">Search</a>
    </nav>
    <main>
        {% if message %}
        <div class="message {{ message_type }}">{{ message }}</div>
        {% endif %}
        {% block content %}{% endblock %}
    </main>
</body>
</html>
"""

HOME = """
{% extends base %}
{% block title %}Home{% endblock %}
{% block content %}
<h1>Welcome to Smart City Navigator</h1>
<div class="card">
    <p>Discover and manage places in your city!</p>
    <p style="margin-top: 1rem;">
        <a href="/places" class="btn">Browse Places</a>
        <a href="/add" class="btn">Add New Place</a>
    </p>
</div>
<h2 style="margin-top: 2rem;">Top Rated</h2>
{% for place in top_places %}
<div class="card">
    <h3>{{ place.name }} <span class="rating">{{ "★" * (place.rating | int) }}</span></h3>
    <p>{{ place.rating }} / 5.0 &bull; <span class="category">{{ place.category }}</span></p>
</div>
{% endfor %}
{% endblock %}
"""

PLACES_PAGE = """
{% extends base %}
{% block title %}Places{% endblock %}
{% block content %}
<h1>All Places ({{ places | length }})</h1>
<div class="filters">
    <span>Filter:</span>
    <a href="/places" class="{% if not category %}active{% endif %}">All</a>
    {% for cat in categories %}
    <a href="/places?category={{ cat }}" class="{% if category == cat %}active{% endif %}">{{ cat | title }}</a>
    {% endfor %}
</div>
{% for place in places %}
<div class="card">
    <h3>{{ place.name }} <span class="rating">{{ "★" * (place.rating | int) }}</span></h3>
    <p>{{ place.rating }} / 5.0 &bull; <span class="category">{{ place.category }}</span></p>
    <p style="margin-top: 0.5rem;">
        <a href="/place/{{ place.id }}">View Details</a> &bull;
        <a href="/delete/{{ place.id }}" style="color: #e74c3c;">Delete</a>
    </p>
</div>
{% else %}
<p>No places found.</p>
{% endfor %}
{% endblock %}
"""

DETAIL = """
{% extends base %}
{% block title %}{{ place.name }}{% endblock %}
{% block content %}
<h1>{{ place.name }}</h1>
<div class="card">
    <p><strong>Rating:</strong> <span class="rating">{{ "★" * (place.rating | int) }}</span> {{ place.rating }} / 5.0</p>
    <p><strong>Category:</strong> <span class="category">{{ place.category }}</span></p>
    <p><strong>ID:</strong> {{ place.id }}</p>
    <p style="margin-top: 1rem;">
        <a href="/places" class="btn">Back to Places</a>
    </p>
</div>
{% endblock %}
"""

ADD = """
{% extends base %}
{% block title %}Add Place{% endblock %}
{% block content %}
<h1>Add New Place</h1>
<div class="card">
    <form method="POST">
        <div class="form-group">
            <label>Name:</label>
            <input type="text" name="name" required placeholder="e.g., Pizza Palace">
        </div>
        <div class="form-group">
            <label>Rating (0-5):</label>
            <input type="number" name="rating" min="0" max="5" step="0.1" required placeholder="4.5">
        </div>
        <div class="form-group">
            <label>Category:</label>
            <select name="category" required>
                <option value="">Select...</option>
                <option value="restaurant">Restaurant</option>
                <option value="cafe">Cafe</option>
                <option value="park">Park</option>
                <option value="museum">Museum</option>
                <option value="shop">Shop</option>
            </select>
        </div>
        <button type="submit" class="btn">Add Place</button>
    </form>
</div>
{% endblock %}
"""

SEARCH = """
{% extends base %}
{% block title %}Search{% endblock %}
{% block content %}
<h1>Search Places</h1>
<div class="card">
    <form method="POST">
        <div class="form-group">
            <input type="text" name="query" placeholder="Search by name..." value="{{ query or '' }}" required>
            <button type="submit" class="btn">Search</button>
        </div>
    </form>
</div>
{% if results is defined %}
<h2>Results for "{{ query }}" ({{ results | length }})</h2>
{% for place in results %}
<div class="card">
    <h3>{{ place.name }} <span class="rating">{{ "★" * (place.rating | int) }}</span></h3>
    <p>{{ place.rating }} / 5.0 &bull; <span class="category">{{ place.category }}</span></p>
</div>
{% else %}
<p>No places found matching "{{ query }}".</p>
{% endfor %}
{% endif %}
{% endblock %}
"""

def get_categories():
    return list(set(p["category"] for p in PLACES))

@app.route("/")
def home():
    top = sorted(PLACES, key=lambda p: p["rating"], reverse=True)[:3]
    return render_template_string(HOME, base=BASE, top_places=top)

@app.route("/places")
def places():
    category = request.args.get("category")
    if category:
        filtered = [p for p in PLACES if p["category"] == category]
    else:
        filtered = PLACES
    return render_template_string(PLACES_PAGE, base=BASE,
                                  places=filtered,
                                  categories=get_categories(),
                                  category=category)

@app.route("/place/<int:place_id>")
def detail(place_id):
    place = next((p for p in PLACES if p["id"] == place_id), None)
    if not place:
        return redirect(url_for("places"))
    return render_template_string(DETAIL, base=BASE, place=place)

@app.route("/add", methods=["GET", "POST"])
def add():
    global NEXT_ID
    if request.method == "POST":
        name = request.form["name"]
        rating = float(request.form["rating"])
        category = request.form["category"]
        PLACES.append({"id": NEXT_ID, "name": name, "rating": rating, "category": category})
        NEXT_ID += 1
        return render_template_string(ADD, base=BASE, message=f"Added {name}!", message_type="success")
    return render_template_string(ADD, base=BASE)

@app.route("/delete/<int:place_id>")
def delete(place_id):
    global PLACES
    place = next((p for p in PLACES if p["id"] == place_id), None)
    if place:
        PLACES = [p for p in PLACES if p["id"] != place_id]
    return redirect(url_for("places"))

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form["query"].lower()
        results = [p for p in PLACES if query in p["name"].lower()]
        return render_template_string(SEARCH, base=BASE, query=request.form["query"], results=results)
    return render_template_string(SEARCH, base=BASE)

if __name__ == "__main__":
    print("Starting complete mini app demo...")
    print("Visit: http://localhost:5000")
    print("Features:")
    print("  - Browse places with category filter")
    print("  - View place details")
    print("  - Add new places")
    print("  - Delete places")
    print("  - Search places")
    print("Press Ctrl+C to stop")
    app.run(debug=True, port=5000)
'''


# =============================================================================
# Demo Runner
# =============================================================================

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def show_demo_code(demo_num):
    """Display the code for a demo without running it."""
    demos = {
        1: ("Minimal Flask App", DEMO_1_CODE),
        2: ("Route Parameters", DEMO_2_CODE),
        3: ("JSON API", DEMO_3_CODE),
        4: ("Templates with Jinja2", DEMO_4_CODE),
        5: ("Forms and User Input", DEMO_5_CODE),
        6: ("Template Inheritance", DEMO_6_CODE),
        7: ("Complete Mini App", DEMO_7_CODE),
    }

    if demo_num in demos:
        title, code = demos[demo_num]
        print_header(f"Demo {demo_num}: {title}")
        print(code)
    else:
        print(f"Invalid demo number: {demo_num}")


def run_demo(demo_num):
    """Run a specific demo."""
    demos = {
        1: ("Minimal Flask App", DEMO_1_CODE),
        2: ("Route Parameters", DEMO_2_CODE),
        3: ("JSON API", DEMO_3_CODE),
        4: ("Templates with Jinja2", DEMO_4_CODE),
        5: ("Forms and User Input", DEMO_5_CODE),
        6: ("Template Inheritance", DEMO_6_CODE),
        7: ("Complete Mini App", DEMO_7_CODE),
    }

    if demo_num not in demos:
        print(f"Invalid demo number: {demo_num}")
        return

    title, code = demos[demo_num]
    print_header(f"Running Demo {demo_num}: {title}")

    # Execute the demo code
    exec(code, {"__name__": "__main__"})


def show_menu():
    """Show interactive menu."""
    print_header("Week 13: Flask Web Server Demos")
    print("""
Available Demos:
  1. Minimal Flask App      - Basic "Hello World" application
  2. Route Parameters       - Dynamic URLs with variables
  3. JSON API               - Building REST-style APIs
  4. Templates with Jinja2  - Dynamic HTML rendering
  5. Forms and User Input   - GET and POST forms
  6. Template Inheritance   - Reusable base templates
  7. Complete Mini App      - Full CRUD application

Commands:
  - Enter a number (1-7) to run that demo
  - Enter 'code N' to view source code for demo N
  - Enter 'all' to show all demo code
  - Enter 'q' to quit

Note: Each demo starts a web server on http://localhost:5000
      Press Ctrl+C to stop the server and return to menu.
""")

    while True:
        try:
            choice = input("\nSelect demo (1-7, 'code N', 'all', or 'q'): ").strip().lower()

            if choice == 'q':
                print("Goodbye!")
                break
            elif choice == 'all':
                for i in range(1, 8):
                    show_demo_code(i)
            elif choice.startswith('code '):
                try:
                    num = int(choice.split()[1])
                    show_demo_code(num)
                except (ValueError, IndexError):
                    print("Usage: code N (where N is 1-7)")
            elif choice.isdigit():
                num = int(choice)
                if 1 <= num <= 7:
                    run_demo(num)
                else:
                    print("Please enter a number between 1 and 7")
            else:
                print("Invalid input. Try again.")

        except KeyboardInterrupt:
            print("\n\nServer stopped. Returning to menu...")
            continue
        except EOFError:
            print("\nGoodbye!")
            break


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo" and len(sys.argv) > 2:
            try:
                demo_num = int(sys.argv[2])
                run_demo(demo_num)
            except ValueError:
                print("Usage: python examples.py --demo N")
        elif sys.argv[1] == "--all":
            for i in range(1, 8):
                show_demo_code(i)
        elif sys.argv[1] == "--help":
            print(__doc__)
        else:
            print("Unknown argument. Use --help for usage.")
    else:
        show_menu()


if __name__ == "__main__":
    main()
