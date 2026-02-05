# Week 13 Lab: Introduction to Flask (Web Server)

## Lab Overview

In this lab, you'll build a web application using Flask. You'll practice creating routes, using templates, handling forms, and building a complete web interface.

**Time:** 2 hours

**Prerequisites:**
- Flask installed (`pip install flask`)
- Basic HTML knowledge
- Understanding of Python functions and dictionaries

---

## Setup

Create a project folder for this lab:

```bash
mkdir flask_lab
cd flask_lab
mkdir templates static
mkdir static/css
```

---

## Exercise 1: Hello Flask (15 minutes)

### Objective
Create your first Flask application with multiple routes.

### Task

Create `app.py` with the following requirements:

1. A home route (`/`) that returns "Welcome to Smart City Navigator!"
2. An about route (`/about`) that returns information about the app
3. A greeting route (`/hello/<name>`) that greets the user by name

### Starter Code

```python
# app.py
from flask import Flask

app = Flask(__name__)

# TODO: Create the home route
# Route: /
# Return: "Welcome to Smart City Navigator!"

# TODO: Create the about route
# Route: /about
# Return: "A Flask app to explore your city."

# TODO: Create the greeting route
# Route: /hello/<name>
# Return: "Hello, {name}!"

if __name__ == "__main__":
    app.run(debug=True)
```

### Expected Output

```
GET / → "Welcome to Smart City Navigator!"
GET /about → "A Flask app to explore your city."
GET /hello/Alice → "Hello, Alice!"
```

### Test Your Solution

```bash
python app.py
# Visit http://localhost:5000 in your browser
```

---

## Exercise 2: Route Parameters (15 minutes)

### Objective
Work with different types of URL parameters.

### Task

Create routes that handle different parameter types:

1. `/place/<name>` - Display place name (string)
2. `/place/id/<int:place_id>` - Display place by ID (integer)
3. `/coords/<float:lat>/<float:lon>` - Display coordinates (floats)

### Starter Code

```python
from flask import Flask

app = Flask(__name__)

# TODO: String parameter route
@app.route("/place/<name>")
def show_place(name):
    # Return HTML showing the place name
    pass

# TODO: Integer parameter route
@app.route("/place/id/<int:place_id>")
def show_place_by_id(place_id):
    # Return HTML showing the place ID and its type
    pass

# TODO: Float parameters route
@app.route("/coords/<float:lat>/<float:lon>")
def show_coords(lat, lon):
    # Return HTML showing the coordinates
    pass

if __name__ == "__main__":
    app.run(debug=True)
```

### Expected Output

```
GET /place/Pizza_Palace → Shows "Place: Pizza_Palace"
GET /place/id/42 → Shows "Place ID: 42 (type: int)"
GET /coords/25.033/121.565 → Shows latitude and longitude
```

---

## Exercise 3: Basic Templates (20 minutes)

### Objective
Use Jinja2 templates to render dynamic HTML.

### Task

1. Create a template that displays a list of places
2. Pass data from Python to the template
3. Use loops and conditionals in the template

### Starter Code

**app.py:**
```python
from flask import Flask, render_template

app = Flask(__name__)

PLACES = [
    {"name": "Pizza Palace", "rating": 4.5, "category": "restaurant"},
    {"name": "Burger Barn", "rating": 4.2, "category": "restaurant"},
    {"name": "Central Park", "rating": 4.8, "category": "park"},
    {"name": "City Museum", "rating": 4.6, "category": "museum"},
]

@app.route("/")
def home():
    # TODO: Render index.html with:
    # - title: "Smart City Navigator"
    # - places: the PLACES list
    pass

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
        .place-card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; }
        .rating { color: #f5a623; }
        .high-rating { background-color: #d4edda; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>

    <p>Total places: <!-- TODO: Show count using filter --></p>

    <!-- TODO: Loop through places -->
    <!-- For each place, create a div with class "place-card" -->
    <!-- Add class "high-rating" if rating >= 4.5 -->
    <!-- Show: name, rating with stars, category -->

</body>
</html>
```

### Expected Features

- Display total number of places
- Loop through all places
- Show rating as stars (e.g., ★★★★☆ for 4.0)
- Highlight places with rating >= 4.5
- Display category in title case

---

## Exercise 4: Template Filters (15 minutes)

### Objective
Practice using Jinja2 filters to format data.

### Task

Create a page that demonstrates various Jinja2 filters:

**templates/filters.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Jinja2 Filters Demo</title>
</head>
<body>
    <h1>Jinja2 Filters</h1>

    <h2>String Filters</h2>
    <ul>
        <!-- TODO: Apply filters to "hello world" -->
        <li>Upper: <!-- Use upper filter --></li>
        <li>Title: <!-- Use title filter --></li>
        <li>Capitalize: <!-- Use capitalize filter --></li>
    </ul>

    <h2>Number Filters</h2>
    <ul>
        <!-- TODO: Format the number 3.14159 -->
        <li>Rounded to 2 decimals: <!-- Use round filter --></li>
        <li>As integer: <!-- Use int filter --></li>
    </ul>

    <h2>List Filters</h2>
    <ul>
        <!-- TODO: Apply filters to items list -->
        <li>Length: <!-- Use length filter --></li>
        <li>First item: <!-- Use first filter --></li>
        <li>Last item: <!-- Use last filter --></li>
        <li>Joined: <!-- Use join filter --></li>
    </ul>

    <h2>Default Value</h2>
    <ul>
        <!-- TODO: Use default filter -->
        <li>With value: {{ name | default("Anonymous") }}</li>
        <li>Without value: {{ missing | default("N/A") }}</li>
    </ul>
</body>
</html>
```

**app.py addition:**
```python
@app.route("/filters")
def filters_demo():
    return render_template("filters.html",
                          name="Alice",
                          items=["apple", "banana", "cherry"])
```

---

## Exercise 5: Form Handling - GET (15 minutes)

### Objective
Handle form data using GET requests and query parameters.

### Task

Create a search page that:
1. Shows a search form
2. Accepts a search query via GET
3. Filters places by name
4. Shows results on the same page

### Starter Code

**app.py:**
```python
from flask import Flask, render_template, request

app = Flask(__name__)

PLACES = [
    {"name": "Pizza Palace", "rating": 4.5},
    {"name": "Pizza Hut", "rating": 4.0},
    {"name": "Burger Barn", "rating": 4.2},
    {"name": "Park Central", "rating": 4.8},
]

@app.route("/search")
def search():
    # TODO: Get 'q' parameter from request.args
    # TODO: If query exists, filter PLACES by name (case-insensitive)
    # TODO: Pass query and results to template
    query = request.args.get("q", "")

    # Filter logic here...

    return render_template("search.html", query=query, results=results)
```

**templates/search.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Search Places</title>
</head>
<body>
    <h1>Search Places</h1>

    <!-- TODO: Create a GET form -->
    <form method="GET" action="/search">
        <input type="text" name="q" value="{{ query }}" placeholder="Search...">
        <button type="submit">Search</button>
    </form>

    <!-- TODO: Show results if query exists -->
    {% if query %}
        <h2>Results for "{{ query }}"</h2>
        <!-- Loop through results or show "No results" -->
    {% endif %}
</body>
</html>
```

### Expected Behavior

- `/search` shows empty form
- `/search?q=pizza` shows Pizza Palace and Pizza Hut
- `/search?q=burger` shows Burger Barn
- `/search?q=xyz` shows "No results found"

---

## Exercise 6: Form Handling - POST (20 minutes)

### Objective
Handle form submission using POST method.

### Task

Create a page to add new places:

1. Display a form with name, rating, and category fields
2. Handle POST submission
3. Add new place to the list
4. Show success message

### Starter Code

**app.py:**
```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

PLACES = []  # Start empty

@app.route("/add", methods=["GET", "POST"])
def add_place():
    message = None

    if request.method == "POST":
        # TODO: Get form data
        name = request.form.get("name")
        rating = request.form.get("rating")
        category = request.form.get("category")

        # TODO: Validate data
        # TODO: Add to PLACES list
        # TODO: Set success message

    return render_template("add.html", message=message, places=PLACES)
```

**templates/add.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Add Place</title>
    <style>
        .message { padding: 10px; background: #d4edda; margin: 10px 0; }
        .form-group { margin: 10px 0; }
    </style>
</head>
<body>
    <h1>Add New Place</h1>

    {% if message %}
    <div class="message">{{ message }}</div>
    {% endif %}

    <!-- TODO: Create POST form -->
    <form method="POST">
        <div class="form-group">
            <label>Name:</label>
            <input type="text" name="name" required>
        </div>
        <!-- TODO: Add rating input (number, 0-5) -->
        <!-- TODO: Add category select (restaurant, park, museum, cafe) -->
        <button type="submit">Add Place</button>
    </form>

    <h2>Current Places ({{ places | length }})</h2>
    <!-- TODO: List all places -->
</body>
</html>
```

---

## Exercise 7: Template Inheritance (20 minutes)

### Objective
Create a base template and extend it in child templates.

### Task

Create a multi-page application with shared layout:

1. Base template with navigation and footer
2. Home page
3. Places page
4. About page

### Starter Code

**templates/base.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Smart City Navigator{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; }
        nav { background: #2c3e50; padding: 1rem; }
        nav a { color: white; margin-right: 1rem; text-decoration: none; }
        main { padding: 2rem; max-width: 800px; margin: 0 auto; }
        footer { background: #2c3e50; color: white; text-align: center; padding: 1rem; }
        {% block extra_css %}{% endblock %}
    </style>
</head>
<body>
    <nav>
        <!-- TODO: Add navigation links using url_for -->
        <a href="{{ url_for('home') }}">Home</a>
        <!-- Add more links -->
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>&copy; 2024 Smart City Navigator</p>
    </footer>
</body>
</html>
```

**templates/home.html:**
```html
{% extends "base.html" %}

{% block title %}Home - Navigator{% endblock %}

{% block content %}
<h1>Welcome!</h1>
<p>Explore the city's best places.</p>
{% endblock %}
```

**templates/places.html:**
```html
{% extends "base.html" %}

{% block title %}Places - Navigator{% endblock %}

{% block extra_css %}
.place-card { border: 1px solid #ddd; padding: 1rem; margin: 1rem 0; }
{% endblock %}

{% block content %}
<h1>All Places</h1>
<!-- TODO: Loop through places -->
{% endblock %}
```

**app.py:**
```python
from flask import Flask, render_template

app = Flask(__name__)

PLACES = [
    {"id": 1, "name": "Pizza Palace", "rating": 4.5},
    {"id": 2, "name": "Central Park", "rating": 4.8},
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/places")
def places():
    return render_template("places.html", places=PLACES)

@app.route("/about")
def about():
    # TODO: Create about.html template
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Exercise 8: Complete Mini Application (30 minutes)

### Objective
Build a complete web application combining all concepts.

### Task

Create a "Place Manager" application with:

1. **Home page** - Welcome message and top-rated places
2. **Places page** - List all places with category filter
3. **Detail page** - Show individual place details
4. **Add page** - Form to add new places
5. **Search** - Search places by name

### Requirements

- Use template inheritance (base.html)
- Handle both GET and POST requests
- Use URL parameters for filtering
- Display appropriate messages
- Style with CSS

### File Structure

```
flask_lab/
├── app.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── places.html
│   ├── detail.html
│   ├── add.html
│   └── search.html
└── static/
    └── css/
        └── style.css
```

### Starter Code

See `week13_starter.py` for complete starter code.

### Checklist

- [ ] Home page shows welcome message
- [ ] Home page shows top 3 rated places
- [ ] Places page lists all places
- [ ] Places page filters by category
- [ ] Detail page shows place information
- [ ] Add page creates new places
- [ ] Search finds places by name
- [ ] Navigation works on all pages
- [ ] Styles are applied consistently

---

## Bonus Challenges

### Bonus 1: Flash Messages

Add flash messages to show success/error notifications:

```python
from flask import flash

app.secret_key = "your-secret-key"

@app.route("/add", methods=["POST"])
def add():
    # ...
    flash("Place added successfully!", "success")
    return redirect(url_for("places"))
```

In base.html:
```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
        <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
{% endwith %}
```

### Bonus 2: Delete Functionality

Add the ability to delete places:

```python
@app.route("/delete/<int:place_id>")
def delete(place_id):
    global PLACES
    PLACES = [p for p in PLACES if p["id"] != place_id]
    flash("Place deleted!", "info")
    return redirect(url_for("places"))
```

### Bonus 3: Edit Functionality

Add the ability to edit existing places:

1. Create an edit form (similar to add)
2. Pre-populate with existing data
3. Handle POST to update the place

---

## Testing Your Application

### Manual Testing Checklist

1. **Routes Work**
   - [ ] Home page loads at `/`
   - [ ] Places page loads at `/places`
   - [ ] Detail page loads at `/place/1`
   - [ ] Add page loads at `/add`
   - [ ] Search page loads at `/search`

2. **Templates Render**
   - [ ] Variables display correctly
   - [ ] Loops show all items
   - [ ] Conditionals work as expected
   - [ ] Filters format data properly

3. **Forms Function**
   - [ ] GET forms include data in URL
   - [ ] POST forms submit correctly
   - [ ] Validation prevents bad data
   - [ ] Success messages appear

4. **Navigation**
   - [ ] All links work
   - [ ] `url_for` generates correct URLs
   - [ ] Base template appears on all pages

---

## Summary

In this lab, you learned:

1. **Routes** - Map URLs to Python functions
2. **Parameters** - Extract data from URLs
3. **Templates** - Render dynamic HTML with Jinja2
4. **Filters** - Format data in templates
5. **Forms** - Handle user input (GET and POST)
6. **Inheritance** - Reuse template structure
7. **Project Structure** - Organize Flask applications

### Key Commands

```bash
# Run Flask application
python app.py

# Install Flask
pip install flask
```

### Key Concepts

```python
# Routes
@app.route("/")
@app.route("/item/<int:id>")

# Templates
render_template("page.html", var=value)

# Forms
request.args.get("key")     # GET
request.form.get("key")     # POST

# Redirects
redirect(url_for("route_name"))
```

### Next Steps

In Week 14, you'll add interactive maps with Leaflet.js to display places visually!
