# Week 13: Introduction to Flask (Web Server)

## Lecture Overview (3 Hours)

**Phase 4: The Web Interface** — "Showing the User"

### Learning Objectives
By the end of this lecture, students will be able to:
1. Understand how web servers work and the HTTP request/response cycle
2. Create a basic Flask web application with routes
3. Use HTML templates with Jinja2 for dynamic content
4. Handle form input and query parameters
5. Organize Flask applications with proper project structure
6. Build a simple web interface for the Smart City Navigator

### Prerequisites
- Week 12: OOP & Decorators (Place class)
- Basic understanding of HTML
- Familiarity with dictionaries and lists

---

# Hour 1: Web Fundamentals and Flask Basics

## 1.1 How the Web Works

### The Client-Server Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    How Web Applications Work                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   CLIENT (Browser)              SERVER (Flask)                  │
│   ┌─────────────┐               ┌─────────────┐                │
│   │             │   REQUEST     │             │                │
│   │  Web        │ ──────────────▶  Flask      │                │
│   │  Browser    │  GET /places  │  App        │                │
│   │             │               │             │                │
│   │             │   RESPONSE    │             │                │
│   │             │ ◀──────────── │             │                │
│   │             │  HTML page    │             │                │
│   └─────────────┘               └─────────────┘                │
│                                                                 │
│   1. User types URL or clicks link                             │
│   2. Browser sends HTTP REQUEST to server                      │
│   3. Server processes request, runs Python code                │
│   4. Server sends HTTP RESPONSE (HTML, JSON, etc.)             │
│   5. Browser displays the response                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### HTTP Request Methods

| Method | Purpose | Example |
|--------|---------|---------|
| GET | Retrieve data | View a page, search results |
| POST | Send data | Submit a form, create a record |
| PUT | Update data | Update user profile |
| DELETE | Remove data | Delete a record |

```
┌─────────────────────────────────────────────────────────────────┐
│                    HTTP Request Structure                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   GET /search?q=pizza HTTP/1.1                                  │
│   ^^^  ^^^^^^^^^^^^^^ ^^^^^^^^                                  │
│   │    │              └── Protocol version                      │
│   │    └── Path + Query string                                  │
│   └── Method                                                    │
│                                                                 │
│   Host: localhost:5000                                          │
│   User-Agent: Mozilla/5.0                                       │
│   Accept: text/html                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### URLs and Routes

```
   https://example.com:5000/search?q=pizza&limit=10
   ^^^^^   ^^^^^^^^^^^^ ^^^^ ^^^^^^ ^^^^^^^^^^^^^^^
   │       │            │    │      └── Query parameters
   │       │            │    └── Path (route)
   │       │            └── Port
   │       └── Host/Domain
   └── Protocol
```

## 1.2 Introduction to Flask

### What is Flask?

Flask is a **micro web framework** for Python:
- **Micro**: Small core, extensible with plugins
- **Web framework**: Tools for building web applications
- **Python**: Write your server logic in Python!

### Why Flask?

```
┌─────────────────────────────────────────────────────────────────┐
│                    Web Framework Comparison                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Flask (Micro Framework)        Django (Full Framework)        │
│   ┌───────────────────┐         ┌───────────────────┐          │
│   │ • Simple, minimal │         │ • Batteries included│          │
│   │ • Easy to learn   │         │ • More features    │          │
│   │ • Flexible        │         │ • More opinionated │          │
│   │ • Great for APIs  │         │ • Great for large  │          │
│   │ • Quick prototypes│         │   applications     │          │
│   └───────────────────┘         └───────────────────┘          │
│                                                                 │
│   We use Flask because it's perfect for learning!              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Installing Flask

```bash
pip install flask
```

## 1.3 Your First Flask Application

### The Minimal App

```python
# app.py - The simplest Flask application
from flask import Flask

# Create the Flask application instance
# __name__ tells Flask where to find resources
app = Flask(__name__)

# Define a route using a decorator
@app.route("/")
def home():
    """Handle requests to the root URL."""
    return "Hello, World!"

# Run the development server
if __name__ == "__main__":
    app.run(debug=True)
```

### Understanding the Code

```
┌─────────────────────────────────────────────────────────────────┐
│                    Flask App Anatomy                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   from flask import Flask                                       │
│   └── Import the Flask class                                    │
│                                                                 │
│   app = Flask(__name__)                                         │
│   └── Create app instance                                       │
│       └── __name__ = module name for resource location          │
│                                                                 │
│   @app.route("/")                                               │
│   └── Decorator that registers URL rule                         │
│       └── "/" means the root URL (http://localhost:5000/)       │
│                                                                 │
│   def home():                                                   │
│   └── View function - called when route is accessed            │
│                                                                 │
│   return "Hello, World!"                                        │
│   └── Response sent back to the browser                        │
│                                                                 │
│   app.run(debug=True)                                           │
│   └── Start development server                                  │
│       └── debug=True enables auto-reload and error pages       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Running the App

```bash
# Terminal
$ python app.py
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

Now visit `http://localhost:5000` in your browser!

## 1.4 Routes and Endpoints

### Multiple Routes

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Smart City Navigator!"

@app.route("/about")
def about():
    return "This app helps you explore the city."

@app.route("/contact")
def contact():
    return "Email: navigator@example.com"

if __name__ == "__main__":
    app.run(debug=True)
```

### Dynamic Routes with Variables

```python
from flask import Flask

app = Flask(__name__)

# Route with a variable part
@app.route("/place/<name>")
def show_place(name):
    """Display information about a place."""
    return f"Showing details for: {name}"

# Multiple variables
@app.route("/location/<float:lat>/<float:lon>")
def show_location(lat, lon):
    """Display a specific location."""
    return f"Location: ({lat}, {lon})"

# Variable with type converter
@app.route("/place/<int:place_id>")
def get_place_by_id(place_id):
    """Get place by numeric ID."""
    return f"Place ID: {place_id}"

if __name__ == "__main__":
    app.run(debug=True)
```

### URL Variable Converters

| Converter | Description | Example |
|-----------|-------------|---------|
| `string` | Default, any text without slashes | `/user/<name>` |
| `int` | Integer values | `/place/<int:id>` |
| `float` | Floating point values | `/coords/<float:lat>` |
| `path` | Like string but includes slashes | `/file/<path:filepath>` |

### Route Examples

```python
# These URLs will match:
@app.route("/place/<name>")           # /place/Pizza_Palace
@app.route("/place/<int:id>")         # /place/42
@app.route("/coords/<float:lat>/<float:lon>")  # /coords/25.033/121.565
```

## 1.5 Returning Different Response Types

### Returning HTML

```python
@app.route("/")
def home():
    return """
    <html>
    <head><title>Home</title></head>
    <body>
        <h1>Welcome!</h1>
        <p>This is HTML returned from Flask.</p>
    </body>
    </html>
    """
```

### Returning JSON (for APIs)

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/places")
def get_places():
    places = [
        {"name": "Pizza Palace", "rating": 4.5},
        {"name": "Burger Barn", "rating": 4.2},
    ]
    return jsonify(places)

# Response:
# [{"name": "Pizza Palace", "rating": 4.5}, {"name": "Burger Barn", "rating": 4.2}]
```

### Status Codes

```python
from flask import Flask

app = Flask(__name__)

@app.route("/place/<int:id>")
def get_place(id):
    places = {1: "Pizza", 2: "Burger"}

    if id in places:
        return places[id], 200  # OK
    else:
        return "Place not found", 404  # Not Found

@app.route("/create", methods=["POST"])
def create_place():
    # Create the place...
    return "Created!", 201  # Created
```

### Common HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful request |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid input |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Something went wrong |

---

# Hour 2: Templates and Jinja2

## 2.1 Why Templates?

### The Problem with Inline HTML

```python
# This gets messy quickly!
@app.route("/places")
def list_places():
    places = get_all_places()  # Returns list of places

    html = "<html><head><title>Places</title></head><body>"
    html += "<h1>All Places</h1><ul>"

    for place in places:
        html += f"<li>{place['name']} - {place['rating']} stars</li>"

    html += "</ul></body></html>"

    return html  # Hard to read, hard to maintain!
```

### The Solution: Templates

```
┌─────────────────────────────────────────────────────────────────┐
│                    Separation of Concerns                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Python Code (app.py)           HTML Template (index.html)     │
│   ┌───────────────────┐         ┌───────────────────┐          │
│   │ • Business logic  │         │ • Page structure  │          │
│   │ • Data processing │  ────▶  │ • Visual layout   │          │
│   │ • API calls       │  data   │ • User interface  │          │
│   └───────────────────┘         └───────────────────┘          │
│                                                                 │
│   Benefits:                                                     │
│   • Cleaner code                                                │
│   • Designers can work on templates                            │
│   • Reusable layouts                                           │
│   • Easier to maintain                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 2.2 Flask Project Structure

### Basic Structure

```
project/
├── app.py              # Main application
├── templates/          # HTML templates
│   ├── base.html       # Base layout
│   ├── index.html      # Home page
│   └── places.html     # Places list
└── static/             # Static files
    ├── css/
    │   └── style.css
    ├── js/
    │   └── script.js
    └── images/
        └── logo.png
```

### Creating the Structure

```bash
mkdir -p project/templates project/static/css project/static/js
cd project
touch app.py
touch templates/index.html
touch static/css/style.css
```

## 2.3 Introduction to Jinja2

### What is Jinja2?

Jinja2 is Flask's template engine:
- Embedded Python-like expressions in HTML
- Variables, loops, conditionals
- Template inheritance
- Filters for formatting

### Basic Syntax

```html
<!-- Variables: {{ }} -->
<h1>{{ title }}</h1>
<p>Hello, {{ user.name }}!</p>

<!-- Statements: {% %} -->
{% if user.is_admin %}
    <p>Welcome, admin!</p>
{% endif %}

<!-- Comments: {# #} -->
{# This won't appear in the output #}
```

### Rendering Templates

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # Pass variables to the template
    return render_template("index.html",
                          title="Smart City Navigator",
                          message="Welcome to our app!")

if __name__ == "__main__":
    app.run(debug=True)
```

**templates/index.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
</body>
</html>
```

## 2.4 Jinja2 Variables and Expressions

### Passing Different Data Types

```python
@app.route("/demo")
def demo():
    return render_template("demo.html",
        # String
        name="Alice",
        # Number
        count=42,
        # List
        colors=["red", "green", "blue"],
        # Dictionary
        place={"name": "Pizza Palace", "rating": 4.5},
        # Object
        user=User("Bob", "bob@example.com")
    )
```

**templates/demo.html:**
```html
<!-- String -->
<p>Name: {{ name }}</p>

<!-- Number (math operations work!) -->
<p>Count: {{ count }}</p>
<p>Double: {{ count * 2 }}</p>

<!-- List -->
<p>First color: {{ colors[0] }}</p>
<p>Colors: {{ colors | join(", ") }}</p>

<!-- Dictionary -->
<p>Place: {{ place.name }} ({{ place["rating"] }} stars)</p>

<!-- Object attributes -->
<p>User: {{ user.name }} - {{ user.email }}</p>
```

### Jinja2 Filters

Filters modify values using the pipe `|` character:

```html
<!-- String filters -->
{{ name | upper }}              <!-- ALICE -->
{{ name | lower }}              <!-- alice -->
{{ name | capitalize }}         <!-- Alice -->
{{ name | title }}              <!-- Alice (title case) -->

<!-- Number filters -->
{{ price | round(2) }}          <!-- 19.99 -->
{{ count | string }}            <!-- "42" -->

<!-- List filters -->
{{ items | length }}            <!-- 5 -->
{{ items | first }}             <!-- first item -->
{{ items | last }}              <!-- last item -->
{{ items | join(", ") }}        <!-- "a, b, c" -->
{{ items | sort }}              <!-- sorted list -->

<!-- Default value -->
{{ rating | default("N/A") }}   <!-- N/A if rating is None -->

<!-- Safe (don't escape HTML) -->
{{ html_content | safe }}       <!-- Render as HTML -->
```

### Common Filters Reference

| Filter | Purpose | Example |
|--------|---------|---------|
| `upper` | Uppercase | `{{ "hi" | upper }}` → HI |
| `lower` | Lowercase | `{{ "HI" | lower }}` → hi |
| `title` | Title Case | `{{ "hello world" | title }}` → Hello World |
| `length` | Count items | `{{ [1,2,3] | length }}` → 3 |
| `default(val)` | Default if None | `{{ x | default("N/A") }}` |
| `round(n)` | Round number | `{{ 3.14159 | round(2) }}` → 3.14 |
| `join(sep)` | Join list | `{{ ["a","b"] | join("-") }}` → a-b |
| `safe` | Don't escape HTML | `{{ "<b>Hi</b>" | safe }}` |

## 2.5 Control Structures

### Conditionals (if/elif/else)

```html
{% if user %}
    <p>Hello, {{ user.name }}!</p>
{% else %}
    <p>Hello, guest!</p>
{% endif %}

{% if place.rating >= 4.5 %}
    <span class="badge excellent">Excellent</span>
{% elif place.rating >= 4.0 %}
    <span class="badge good">Good</span>
{% elif place.rating >= 3.0 %}
    <span class="badge average">Average</span>
{% else %}
    <span class="badge poor">Poor</span>
{% endif %}
```

### Loops (for)

```html
<ul>
{% for place in places %}
    <li>{{ place.name }} - {{ place.rating }} stars</li>
{% endfor %}
</ul>

<!-- With index -->
<ol>
{% for place in places %}
    <li>{{ loop.index }}. {{ place.name }}</li>
{% endfor %}
</ol>

<!-- Empty list handling -->
{% for place in places %}
    <p>{{ place.name }}</p>
{% else %}
    <p>No places found.</p>
{% endfor %}
```

### Loop Variables

| Variable | Description |
|----------|-------------|
| `loop.index` | Current iteration (1-indexed) |
| `loop.index0` | Current iteration (0-indexed) |
| `loop.first` | True if first iteration |
| `loop.last` | True if last iteration |
| `loop.length` | Total number of items |

```html
{% for place in places %}
    <div class="place {% if loop.first %}first{% endif %} {% if loop.last %}last{% endif %}">
        <span class="number">{{ loop.index }} of {{ loop.length }}</span>
        <span class="name">{{ place.name }}</span>
    </div>
{% endfor %}
```

## 2.6 Complete Template Example

**app.py:**
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    places = [
        {"name": "Pizza Palace", "rating": 4.5, "category": "restaurant"},
        {"name": "Burger Barn", "rating": 4.2, "category": "restaurant"},
        {"name": "Central Park", "rating": 4.8, "category": "park"},
        {"name": "City Museum", "rating": 4.6, "category": "museum"},
    ]

    return render_template("index.html",
                          title="Smart City Navigator",
                          places=places,
                          featured=places[2])  # Central Park

if __name__ == "__main__":
    app.run(debug=True)
```

**templates/index.html:**
```html
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
        .category {
            background: #e0e0e0;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8em;
        }
        .featured {
            background: #fffde7;
            border-color: #f5a623;
        }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>

    <!-- Featured place -->
    {% if featured %}
    <div class="place-card featured">
        <h2>Featured: {{ featured.name }}</h2>
        <p class="rating">{{ "★" * (featured.rating | int) }} {{ featured.rating }}</p>
    </div>
    {% endif %}

    <!-- All places -->
    <h2>All Places ({{ places | length }})</h2>

    {% for place in places %}
    <div class="place-card">
        <h3>{{ loop.index }}. {{ place.name }}</h3>
        <p class="rating">Rating: {{ place.rating }} / 5.0</p>
        <span class="category">{{ place.category | title }}</span>
    </div>
    {% else %}
    <p>No places available.</p>
    {% endfor %}

</body>
</html>
```

---

# Hour 3: Forms, Template Inheritance, and Building Our App

## 3.1 Template Inheritance

### The DRY Principle

Don't Repeat Yourself! Base templates let you define common structure once:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Template Inheritance                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   base.html (Parent)                                            │
│   ┌─────────────────────────────────────────┐                  │
│   │ <!DOCTYPE html>                          │                  │
│   │ <html>                                   │                  │
│   │   <head>...</head>                       │                  │
│   │   <body>                                 │                  │
│   │     <nav>...</nav>                       │                  │
│   │     ┌─────────────────────┐             │                  │
│   │     │ {% block content %} │             │                  │
│   │     │ {% endblock %}      │             │                  │
│   │     └─────────────────────┘             │                  │
│   │     <footer>...</footer>                │                  │
│   │   </body>                               │                  │
│   │ </html>                                 │                  │
│   └─────────────────────────────────────────┘                  │
│                      ▲                                          │
│          ┌───────────┼───────────┐                             │
│          │           │           │                             │
│   ┌──────┴─────┐ ┌───┴────┐ ┌───┴────┐                        │
│   │ index.html │ │places. │ │about.  │                        │
│   │            │ │html    │ │html    │                        │
│   │ extends    │ │extends │ │extends │                        │
│   │ base.html  │ │base    │ │base    │                        │
│   └────────────┘ └────────┘ └────────┘                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Base Template

**templates/base.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Smart City Navigator{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav>
        <a href="{{ url_for('home') }}">Home</a>
        <a href="{{ url_for('places') }}">Places</a>
        <a href="{{ url_for('search') }}">Search</a>
        <a href="{{ url_for('about') }}">About</a>
    </nav>

    <main>
        {% block content %}
        <!-- Child templates fill this in -->
        {% endblock %}
    </main>

    <footer>
        <p>&copy; 2024 Smart City Navigator</p>
    </footer>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Child Templates

**templates/index.html:**
```html
{% extends "base.html" %}

{% block title %}Home - Smart City Navigator{% endblock %}

{% block content %}
<h1>Welcome to Smart City Navigator</h1>
<p>Discover amazing places in your city!</p>

<div class="featured-places">
    {% for place in featured_places %}
    <div class="place-card">
        <h3>{{ place.name }}</h3>
        <p>{{ place.rating }} stars</p>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

**templates/about.html:**
```html
{% extends "base.html" %}

{% block title %}About - Smart City Navigator{% endblock %}

{% block content %}
<h1>About Us</h1>
<p>Smart City Navigator helps you explore your city.</p>
<p>Built with Flask and Python.</p>
{% endblock %}
```

### The url_for() Function

`url_for()` generates URLs dynamically:

```html
<!-- Link to a route -->
<a href="{{ url_for('home') }}">Home</a>
<!-- Generates: /  -->

<!-- Link with parameters -->
<a href="{{ url_for('show_place', name='pizza') }}">Pizza</a>
<!-- Generates: /place/pizza -->

<!-- Link to static files -->
<link href="{{ url_for('static', filename='css/style.css') }}">
<!-- Generates: /static/css/style.css -->

<img src="{{ url_for('static', filename='images/logo.png') }}">
<!-- Generates: /static/images/logo.png -->
```

## 3.2 Handling Forms

### HTML Forms Basics

```html
<form method="POST" action="/search">
    <input type="text" name="query" placeholder="Search...">
    <button type="submit">Search</button>
</form>
```

- `method="POST"`: Send data in request body (secure)
- `method="GET"`: Send data in URL (?query=pizza)
- `action="/search"`: URL to submit to
- `name="query"`: Key for accessing the data in Flask

### Processing Form Data

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        # Get data from form
        query = request.form["query"]

        # Process the search
        results = search_places(query)

        return render_template("results.html",
                              query=query,
                              results=results)

    # GET request - show the search form
    return render_template("search.html")

def search_places(query):
    """Search for places matching query."""
    all_places = [
        {"name": "Pizza Palace", "rating": 4.5},
        {"name": "Pizza Hut", "rating": 4.0},
        {"name": "Burger Barn", "rating": 4.2},
    ]

    # Simple search - filter by name containing query
    query_lower = query.lower()
    return [p for p in all_places if query_lower in p["name"].lower()]

if __name__ == "__main__":
    app.run(debug=True)
```

**templates/search.html:**
```html
{% extends "base.html" %}

{% block content %}
<h1>Search Places</h1>

<form method="POST" action="{{ url_for('search') }}">
    <div class="form-group">
        <label for="query">Search for:</label>
        <input type="text" id="query" name="query"
               placeholder="e.g., pizza, burger, park" required>
    </div>
    <button type="submit">Search</button>
</form>
{% endblock %}
```

**templates/results.html:**
```html
{% extends "base.html" %}

{% block content %}
<h1>Search Results for "{{ query }}"</h1>

{% if results %}
    <p>Found {{ results | length }} place(s):</p>
    <ul>
    {% for place in results %}
        <li>{{ place.name }} - {{ place.rating }} stars</li>
    {% endfor %}
    </ul>
{% else %}
    <p>No places found matching "{{ query }}".</p>
{% endif %}

<p><a href="{{ url_for('search') }}">Search again</a></p>
{% endblock %}
```

### Query Parameters (GET)

```python
@app.route("/places")
def list_places():
    # Get query parameters from URL
    # /places?category=restaurant&min_rating=4.0

    category = request.args.get("category")        # "restaurant" or None
    min_rating = request.args.get("min_rating", 0, type=float)  # 4.0 or 0

    places = get_all_places()

    # Filter by category
    if category:
        places = [p for p in places if p["category"] == category]

    # Filter by rating
    places = [p for p in places if p.get("rating", 0) >= min_rating]

    return render_template("places.html",
                          places=places,
                          category=category,
                          min_rating=min_rating)
```

### Form Methods Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│                    GET vs POST                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   GET                              POST                         │
│   ────────────────                 ────────────────             │
│   • Data in URL                    • Data in body               │
│   • Visible in browser             • Hidden from URL            │
│   • Can be bookmarked              • Cannot bookmark             │
│   • Limited data size              • Large data allowed          │
│   • Use for: searches,             • Use for: login,            │
│     filters, navigation            forms, changes               │
│                                                                 │
│   request.args["key"]              request.form["key"]          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 3.3 Flash Messages

Flash messages show one-time notifications:

```python
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Required for flash messages

@app.route("/add", methods=["GET", "POST"])
def add_place():
    if request.method == "POST":
        name = request.form["name"]

        # Add the place...

        flash(f"Successfully added {name}!", "success")
        return redirect(url_for("places"))

    return render_template("add_place.html")
```

**In base.html:**
```html
<main>
    <!-- Show flash messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    {% block content %}{% endblock %}
</main>
```

## 3.4 Building the Smart City Navigator Web Interface

Let's put it all together! Here's a complete mini-application:

### Project Structure

```
smart_city_navigator/
├── app.py
├── places.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── places.html
│   ├── place_detail.html
│   └── search.html
└── static/
    └── css/
        └── style.css
```

### places.py (Data Module)

```python
"""Place data and operations."""

PLACES = [
    {"id": 1, "name": "Pizza Palace", "rating": 4.5,
     "category": "restaurant", "coords": (25.033, 121.565)},
    {"id": 2, "name": "Burger Barn", "rating": 4.2,
     "category": "restaurant", "coords": (25.038, 121.568)},
    {"id": 3, "name": "Central Park", "rating": 4.8,
     "category": "park", "coords": (25.040, 121.570)},
    {"id": 4, "name": "City Museum", "rating": 4.6,
     "category": "museum", "coords": (25.035, 121.562)},
    {"id": 5, "name": "Coffee Corner", "rating": 4.3,
     "category": "cafe", "coords": (25.034, 121.564)},
]

def get_all_places():
    """Return all places."""
    return PLACES

def get_place_by_id(place_id):
    """Get a place by its ID."""
    for place in PLACES:
        if place["id"] == place_id:
            return place
    return None

def search_places(query):
    """Search places by name."""
    query = query.lower()
    return [p for p in PLACES if query in p["name"].lower()]

def filter_by_category(category):
    """Filter places by category."""
    return [p for p in PLACES if p["category"] == category]

def get_categories():
    """Get list of unique categories."""
    return list(set(p["category"] for p in PLACES))
```

### app.py (Main Application)

```python
"""Smart City Navigator - Flask Web Application."""

from flask import Flask, render_template, request, redirect, url_for, flash
from places import (get_all_places, get_place_by_id, search_places,
                   filter_by_category, get_categories)

app = Flask(__name__)
app.secret_key = "smart-city-secret-key"

@app.route("/")
def home():
    """Home page with featured places."""
    places = get_all_places()
    # Feature top 3 rated places
    featured = sorted(places, key=lambda p: p["rating"], reverse=True)[:3]
    return render_template("index.html", featured=featured)

@app.route("/places")
def places():
    """List all places with optional category filter."""
    category = request.args.get("category")

    if category:
        place_list = filter_by_category(category)
    else:
        place_list = get_all_places()

    categories = get_categories()

    return render_template("places.html",
                          places=place_list,
                          categories=categories,
                          selected_category=category)

@app.route("/place/<int:place_id>")
def place_detail(place_id):
    """Show details for a specific place."""
    place = get_place_by_id(place_id)

    if not place:
        flash("Place not found!", "error")
        return redirect(url_for("places"))

    return render_template("place_detail.html", place=place)

@app.route("/search", methods=["GET", "POST"])
def search():
    """Search for places."""
    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if not query:
            flash("Please enter a search term.", "warning")
            return render_template("search.html", results=None, query="")

        results = search_places(query)
        return render_template("search.html", results=results, query=query)

    return render_template("search.html", results=None, query="")

@app.route("/about")
def about():
    """About page."""
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
```

### templates/base.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Smart City Navigator{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <nav>
            <a href="{{ url_for('home') }}" class="logo">Smart City Navigator</a>
            <ul>
                <li><a href="{{ url_for('home') }}">Home</a></li>
                <li><a href="{{ url_for('places') }}">Places</a></li>
                <li><a href="{{ url_for('search') }}">Search</a></li>
                <li><a href="{{ url_for('about') }}">About</a></li>
            </ul>
        </nav>
    </header>

    <main>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>&copy; 2024 Smart City Navigator | Built with Flask</p>
    </footer>
</body>
</html>
```

### templates/index.html

```html
{% extends "base.html" %}

{% block title %}Home - Smart City Navigator{% endblock %}

{% block content %}
<section class="hero">
    <h1>Discover Your City</h1>
    <p>Find the best places to eat, visit, and explore.</p>
    <a href="{{ url_for('search') }}" class="btn">Start Searching</a>
</section>

<section class="featured">
    <h2>Top Rated Places</h2>
    <div class="place-grid">
        {% for place in featured %}
        <div class="place-card">
            <h3>{{ place.name }}</h3>
            <p class="rating">
                {% for i in range(place.rating | int) %}★{% endfor %}
                {{ place.rating }}
            </p>
            <span class="category">{{ place.category | title }}</span>
            <a href="{{ url_for('place_detail', place_id=place.id) }}">View Details</a>
        </div>
        {% endfor %}
    </div>
</section>
{% endblock %}
```

### templates/places.html

```html
{% extends "base.html" %}

{% block title %}Places - Smart City Navigator{% endblock %}

{% block content %}
<h1>All Places</h1>

<!-- Category Filter -->
<div class="filters">
    <span>Filter by category:</span>
    <a href="{{ url_for('places') }}"
       class="{% if not selected_category %}active{% endif %}">All</a>
    {% for cat in categories %}
        <a href="{{ url_for('places', category=cat) }}"
           class="{% if selected_category == cat %}active{% endif %}">
            {{ cat | title }}
        </a>
    {% endfor %}
</div>

<!-- Places List -->
<div class="place-list">
    {% for place in places %}
    <div class="place-card">
        <h3>{{ place.name }}</h3>
        <p class="rating">Rating: {{ place.rating }} / 5.0</p>
        <span class="category">{{ place.category | title }}</span>
        <a href="{{ url_for('place_detail', place_id=place.id) }}">View Details</a>
    </div>
    {% else %}
    <p>No places found in this category.</p>
    {% endfor %}
</div>
{% endblock %}
```

### templates/place_detail.html

```html
{% extends "base.html" %}

{% block title %}{{ place.name }} - Smart City Navigator{% endblock %}

{% block content %}
<article class="place-detail">
    <h1>{{ place.name }}</h1>

    <div class="details">
        <p><strong>Category:</strong> {{ place.category | title }}</p>
        <p><strong>Rating:</strong>
            {% for i in range(place.rating | int) %}★{% endfor %}
            {{ place.rating }} / 5.0
        </p>
        <p><strong>Location:</strong>
            ({{ place.coords[0] }}, {{ place.coords[1] }})
        </p>
    </div>

    <a href="{{ url_for('places') }}" class="btn">Back to Places</a>
</article>
{% endblock %}
```

### templates/search.html

```html
{% extends "base.html" %}

{% block title %}Search - Smart City Navigator{% endblock %}

{% block content %}
<h1>Search Places</h1>

<form method="POST" class="search-form">
    <input type="text" name="query" placeholder="Search for places..."
           value="{{ query }}" required>
    <button type="submit">Search</button>
</form>

{% if results is not none %}
    <div class="search-results">
        <h2>Results for "{{ query }}"</h2>

        {% if results %}
            <p>Found {{ results | length }} place(s):</p>
            <div class="place-list">
                {% for place in results %}
                <div class="place-card">
                    <h3>{{ place.name }}</h3>
                    <p class="rating">Rating: {{ place.rating }}</p>
                    <a href="{{ url_for('place_detail', place_id=place.id) }}">
                        View Details
                    </a>
                </div>
                {% endfor %}
            </div>
        {% else %}
            <p>No places found matching "{{ query }}".</p>
        {% endif %}
    </div>
{% endif %}
{% endblock %}
```

### static/css/style.css

```css
/* Basic Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
}

/* Navigation */
nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background: #2c3e50;
    color: white;
}

nav .logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
    text-decoration: none;
}

nav ul {
    display: flex;
    list-style: none;
    gap: 1.5rem;
}

nav a {
    color: white;
    text-decoration: none;
}

nav a:hover {
    color: #3498db;
}

/* Main Content */
main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    min-height: calc(100vh - 200px);
}

/* Alerts */
.alert {
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 4px;
}

.alert-success { background: #d4edda; color: #155724; }
.alert-error { background: #f8d7da; color: #721c24; }
.alert-warning { background: #fff3cd; color: #856404; }

/* Hero Section */
.hero {
    text-align: center;
    padding: 4rem 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 8px;
    margin-bottom: 2rem;
}

.hero h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background: #3498db;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    border: none;
    cursor: pointer;
}

.btn:hover {
    background: #2980b9;
}

/* Place Cards */
.place-grid, .place-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 1.5rem;
}

.place-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.5rem;
    transition: box-shadow 0.3s;
}

.place-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.place-card h3 {
    margin-bottom: 0.5rem;
}

.rating {
    color: #f5a623;
}

.category {
    display: inline-block;
    background: #e0e0e0;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.85rem;
    margin: 0.5rem 0;
}

/* Filters */
.filters {
    margin: 1rem 0;
}

.filters a {
    margin-right: 1rem;
    text-decoration: none;
    color: #666;
}

.filters a.active {
    color: #3498db;
    font-weight: bold;
}

/* Search Form */
.search-form {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}

.search-form input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

.search-form button {
    padding: 0.75rem 2rem;
}

/* Footer */
footer {
    text-align: center;
    padding: 2rem;
    background: #2c3e50;
    color: white;
}
```

## 3.5 Running and Testing

### Run the Application

```bash
cd smart_city_navigator
python app.py
```

### Test in Browser

1. Visit `http://localhost:5000` - Home page
2. Click "Places" - See all places
3. Click category filters - Filter places
4. Click "Search" - Search for places
5. Click "View Details" - See place details

### Debug Mode Benefits

When `debug=True`:
- Auto-reloads when you change code
- Shows detailed error pages
- Never use in production!

---

## Summary

### Key Concepts

```
┌─────────────────────────────────────────────────────────────────┐
│                    Flask Web Development                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ROUTES                                                        │
│   @app.route("/path")         Define URL endpoints              │
│   @app.route("/item/<id>")    Dynamic URL variables             │
│                                                                 │
│   TEMPLATES (Jinja2)                                            │
│   {{ variable }}              Output variables                  │
│   {% for item in list %}      Control structures                │
│   {% extends "base.html" %}   Template inheritance              │
│                                                                 │
│   FORMS                                                         │
│   request.form["field"]       POST form data                    │
│   request.args.get("param")   GET query parameters              │
│                                                                 │
│   HELPERS                                                       │
│   url_for("route")            Generate URLs                     │
│   render_template("t.html")   Render templates                  │
│   redirect(url_for("route"))  Redirect to another page         │
│   flash("message", "type")    One-time notifications           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Best Practices

1. **Project Structure**: Separate templates, static files, and code
2. **Template Inheritance**: Use base templates for DRY HTML
3. **URL Generation**: Always use `url_for()` for links
4. **Form Handling**: Validate input and provide feedback
5. **Security**: Never trust user input, use `flash()` for messages

### What's Next?

In Week 14, we'll add:
- Interactive maps with Leaflet.js
- JavaScript integration
- Plotting routes on the map
- Displaying place markers

---

## Quick Reference

### Flask Cheat Sheet

```python
# Create app
from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)
app.secret_key = "secret"

# Routes
@app.route("/")                      # GET only (default)
@app.route("/form", methods=["GET", "POST"])  # GET and POST
@app.route("/item/<int:id>")         # URL variable

# Templates
render_template("page.html", var=value)

# Request data
request.method                       # "GET" or "POST"
request.form["field"]                # POST data
request.args.get("param", default)   # GET parameters

# Responses
return "text"                        # Plain text
return render_template("t.html")     # HTML
return jsonify(data)                 # JSON
return redirect(url_for("route"))    # Redirect

# Flash messages
flash("Message", "category")

# Run
app.run(debug=True)
```

### Jinja2 Cheat Sheet

```html
<!-- Variables -->
{{ variable }}
{{ object.attribute }}
{{ dict["key"] }}

<!-- Filters -->
{{ name | upper }}
{{ list | length }}
{{ value | default("N/A") }}

<!-- Control -->
{% if condition %}...{% endif %}
{% for item in list %}...{% endfor %}
{% for item in list %}...{% else %}...{% endfor %}

<!-- Inheritance -->
{% extends "base.html" %}
{% block name %}...{% endblock %}

<!-- URLs -->
{{ url_for('route_name') }}
{{ url_for('route', param=value) }}
{{ url_for('static', filename='css/style.css') }}
```
