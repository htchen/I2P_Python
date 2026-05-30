# Modularity and API Wrappers

Separating concerns into distinct modules to keep code organized, maintainable, and clean.

## Learning Objectives

- Recognize the problems caused by "spaghetti code"
- Apply the principle of separation of concerns
- Build dedicated API wrapper modules
- Structure a professional Flask project

## The Problem with "Spaghetti Code"

When building a complex application like the Smart City Navigator, it is
tempting to put everything—HTML routing, API requests, data processing, and
map generation—into a single file.

- **The issue:** This makes the code incredibly difficult to read, debug, and
  scale. Changing one part often accidentally breaks another, because
  everything is tangled together like a plate of spaghetti.
- **The solution (modularity):** Divide the system into separate components
  based on their responsibilities. The Flask application should only
  *coordinate traffic*—it should not handle the messy details of fetching
  coordinates or calculating routes.

This idea of splitting responsibilities is called **separation of concerns**,
and it is the heart of the **Single Responsibility Principle**: each module
should have one, and only one, reason to change.

## Building API Wrappers

To achieve modularity, we build **wrappers**. An API wrapper is a dedicated
Python module whose sole job is to talk to an external service and return
clean, usable data. It *hides* the raw HTTP requests and JSON parsing from the
main application.

### Module A: The Geocoding Wrapper (`geocoding.py`)

- **Responsibility:** Interacting with the Nominatim API.
- **Input:** An address string or a search query.
- **Output:** Clean latitude/longitude coordinates, or a list of specific
  places.

```python
# geocoding.py — the only file that knows how to talk to Nominatim
from geocoding import GeocodingService

geocoder = GeocodingService()
coords = geocoder.geocode("New York City")   # -> (40.7128, -74.0060)
```

Notice how the caller never sees a URL, a query parameter, or a JSON key. If
Nominatim changes its response format tomorrow, we only edit `geocoding.py`—the
rest of the app is untouched.

### Module B: The Routing Wrapper (`routing.py`)

- **Responsibility:** Interacting with the OSRM API.
- **Input:** Start and end coordinates.
- **Output:** The calculated route and travel duration.

```python
# routing.py — the only file that knows how to talk to OSRM
from routing import RoutingService

router = RoutingService()
route = router.get_route((40.7128, -74.0060), (40.7484, -73.9857))
# -> {"distance": ..., "duration": ..., "geometry": ...}
```

### A Clean Data Model

Wrappers often return a tidy object instead of a raw dictionary. A small
`Place` class makes the data self-documenting and easy to test:

```python
# geocoding.py (excerpt)
class Place:
    """A single location returned by the geocoding wrapper."""

    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon
```

## Project Structure

By extracting these API wrappers, our professional directory layout becomes
much cleaner. We separate the logic into three kinds of files:

1. **Configuration files** — store base URLs and settings.
2. **API modules** — our geocoding and routing wrappers.
3. **Main application** — the Flask file that simply *imports* these wrappers
   and uses them to render the final Folium map.

```
smart_city_navigator/
├── config.py          # Base URLs and settings
├── geocoding.py       # API wrapper: Nominatim
├── routing.py         # API wrapper: OSRM
├── app.py             # Flask app: imports wrappers, renders the map
├── templates/
│   ├── index.html
│   ├── results.html
│   └── error.html
└── static/
    └── style.css
```

A minimal `config.py` keeps settings in one place:

```python
# config.py
NOMINATIM_URL = "https://nominatim.openstreetmap.org"
OSRM_URL = "https://router.project-osrm.org"
USER_AGENT = "SmartCityNavigator/1.0"
REQUEST_TIMEOUT = 10
```

And `app.py` stays small—it only coordinates, it does not do the heavy lifting:

```python
# app.py
from flask import Flask, render_template, request
from geocoding import GeocodingService
from routing import RoutingService

app = Flask(__name__)
geocoder = GeocodingService()
router = RoutingService()

@app.route("/search", methods=["POST"])
def search():
    address = request.form.get("address")
    coords = geocoder.geocode(address)        # delegated to the wrapper
    if not coords:
        return render_template("error.html", message="Address not found")
    return render_template("results.html", lat=coords[0], lon=coords[1])
```

## Interactive Activity: Divide and Conquer

Modularity shines when a team can build pieces **in parallel** and snap them
together at the end. Let's experience it:

1. **Split the class into two groups.**
2. **Group 1** writes the **Geocoding Wrapper** using Nominatim
   (`geocode(address)`).
3. **Group 2** writes the **Routing Wrapper** using OSRM
   (`get_route(start, end)`).
4. Agree on the *interface* first (function names, inputs, outputs), then each
   group works independently.
5. **Bring the groups together** and plug both modules into the main Flask
   application to render the final Folium map.

When two independently built modules connect to `app.py` without friction, you
have seen modularity in action—as long as the interface matches, the internals
can be developed completely separately.

## Summary

Splitting an application into focused modules—configuration, API wrappers, and
a thin coordinating Flask app—turns tangled spaghetti code into a clean,
maintainable, and testable project.
