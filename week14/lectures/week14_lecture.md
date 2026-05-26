# Week 14: Interactive Maps with Folium

## Lecture Overview (3 Hours)

**Phase 4: The Web Interface** — "Showing the User"

### Learning Objectives
By the end of this lecture, students will be able to:
1. Understand how Python libraries can generate JavaScript/HTML
2. Create interactive maps using the Folium library
3. Add markers with custom icons, popups, and tooltips
4. Draw routes and shapes on maps
5. Integrate maps with Flask web applications
6. Build a complete map visualization for the Smart City Navigator

### Prerequisites
- Week 13: Flask Web Server (routes, templates)
- Basic understanding of HTML
- Familiarity with coordinates (latitude, longitude)

---

# Hour 1: Introduction to Interactive Maps

## 1.1 The Visualization Challenge

### Why Maps Matter

```
┌─────────────────────────────────────────────────────────────────┐
│                    Location Data Visualization                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Raw Data                        Visual Representation         │
│   ┌───────────────────┐          ┌───────────────────┐         │
│   │ Pizza Palace      │          │    ┌─────────┐    │         │
│   │ (25.033, 121.565) │   ──▶   │  🍕│  MAP    │    │         │
│   │ Rating: 4.5       │          │    │ 📍      │    │         │
│   │                   │          │    │    📍   │    │         │
│   │ Burger Barn       │          │    └─────────┘    │         │
│   │ (25.038, 121.568) │          │                   │         │
│   └───────────────────┘          └───────────────────┘         │
│                                                                 │
│   Problems with raw data:        Benefits of maps:              │
│   • Hard to understand           • Intuitive visualization      │
│   • No spatial context           • Shows relationships          │
│   • Difficult to compare         • Interactive exploration      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### The Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    Map Technology Stack                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────┐                                          │
│   │    Python       │  Your code (easy to write)               │
│   │    Folium       │                                          │
│   └────────┬────────┘                                          │
│            │ generates                                          │
│            ▼                                                    │
│   ┌─────────────────┐                                          │
│   │   HTML + JS     │  Web page with map                       │
│   │   Leaflet.js    │                                          │
│   └────────┬────────┘                                          │
│            │ renders                                            │
│            ▼                                                    │
│   ┌─────────────────┐                                          │
│   │    Browser      │  Interactive map display                 │
│   │    (Chrome,     │                                          │
│   │     Firefox)    │                                          │
│   └─────────────────┘                                          │
│                                                                 │
│   Folium = Python wrapper around Leaflet.js                    │
│   You write Python → Folium generates JavaScript               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 1.2 Introduction to Folium

### What is Folium?

- **Python library** for creating interactive maps
- **Wraps Leaflet.js** - a popular JavaScript mapping library
- **Generates HTML/JS** that runs in any browser
- **No JavaScript knowledge needed** - just Python!

### Installing Folium

```bash
pip install folium
```

### How Folium Works

```python
import folium

# 1. Create a map object (Python)
m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

# 2. Save to HTML file
m.save("map.html")

# 3. Open map.html in browser - it's now interactive!
```

Behind the scenes, Folium generates:
```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="leaflet.css"/>
    <script src="leaflet.js"></script>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([25.0330, 121.5654], 14);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    </script>
</body>
</html>
```

## 1.3 Creating Your First Map

### Basic Map Creation

```python
import folium

# Create a map centered on a location
m = folium.Map(
    location=[25.0330, 121.5654],  # [latitude, longitude]
    zoom_start=14                   # Initial zoom level (1-18)
)

# Save to file
m.save("my_first_map.html")
print("Map saved! Open my_first_map.html in your browser.")
```

### Understanding Coordinates

```
┌─────────────────────────────────────────────────────────────────┐
│                    Latitude and Longitude                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Latitude (緯度): North-South position                         │
│   • Range: -90 (South Pole) to +90 (North Pole)                │
│   • Taipei: ~25° N                                              │
│                                                                 │
│   Longitude (經度): East-West position                          │
│   • Range: -180 (West) to +180 (East)                          │
│   • Taipei: ~121° E                                             │
│                                                                 │
│          90°N                                                   │
│           │                                                     │
│   -180°W ─┼─ 0° ─────── +180°E                                 │
│           │      (Prime Meridian)                               │
│         -90°S                                                   │
│                                                                 │
│   Format in Python: [latitude, longitude]                       │
│   Example: [25.0330, 121.5654] = Taipei 101                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Zoom Levels

| Zoom Level | View |
|------------|------|
| 1-3 | World/Continent |
| 4-6 | Country |
| 7-9 | State/Province |
| 10-12 | City |
| 13-15 | Neighborhood |
| 16-18 | Street/Building |

```python
# Different zoom levels
folium.Map(location=[25.0330, 121.5654], zoom_start=5)   # See Taiwan
folium.Map(location=[25.0330, 121.5654], zoom_start=12)  # See Taipei
folium.Map(location=[25.0330, 121.5654], zoom_start=17)  # See buildings
```

### Exploring Coordinates Interactively

Folium provides plugins that help you explore coordinates directly on the map:

#### MousePosition — See Coordinates on Hover

```python
import folium
from folium.plugins import MousePosition

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

# Show coordinates as the mouse moves
MousePosition(
    position="topright",
    separator=" | ",
    prefix="Coordinates:",
    num_digits=4          # Decimal places
).add_to(m)

m.save("mouse_position.html")
# Move your mouse over the map — the coordinates update in real time!
```

#### LatLngPopup — Click to See Coordinates

```python
import folium
from folium.plugins import LatLngPopup

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

# Click anywhere on the map to see coordinates in a popup
LatLngPopup().add_to(m)

m.save("click_coordinates.html")
# Click on any spot — a popup shows the exact [lat, lon]!
```

```
┌─────────────────────────────────────────────────────────────────┐
│              Interactive Coordinate Tools                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   MousePosition:                                                │
│   ┌─────────────────────────────────────────┐                  │
│   │                     Coordinates: 25.0330 | 121.5654│        │
│   │          🖱️ ← mouse here                           │        │
│   │                                         │                  │
│   │    MAP                                  │                  │
│   └─────────────────────────────────────────┘                  │
│   Coordinates update as you move the mouse                     │
│                                                                 │
│   LatLngPopup:                                                  │
│   ┌─────────────────────────────────────────┐                  │
│   │              ┌──────────────┐           │                  │
│   │              │ Lat: 25.0350 │           │                  │
│   │              │ Lng: 121.5600│           │                  │
│   │              └──────────────┘           │                  │
│   │    MAP            👆 click here         │                  │
│   └─────────────────────────────────────────┘                  │
│   Click anywhere to see its coordinates                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Map Tiles (Base Layers)

```python
import folium

# Default: OpenStreetMap
m1 = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

# CartoDB Positron (light, clean)
m2 = folium.Map(
    location=[25.0330, 121.5654],
    zoom_start=14,
    tiles="CartoDB positron"
)

# CartoDB Dark Matter (dark theme)
m3 = folium.Map(
    location=[25.0330, 121.5654],
    zoom_start=14,
    tiles="CartoDB dark_matter"
)

# Stamen Terrain (shows topography)
m4 = folium.Map(
    location=[25.0330, 121.5654],
    zoom_start=14,
    tiles="Stamen Terrain"
)
```

### Available Tile Providers

| Tiles | Description | Best For |
|-------|-------------|----------|
| `OpenStreetMap` | Default, detailed | General use |
| `CartoDB positron` | Light, minimal | Clean presentations |
| `CartoDB dark_matter` | Dark theme | Night mode, modern look |
| `Stamen Terrain` | Shows elevation | Hiking, geography |
| `Stamen Toner` | Black and white | Printing |

## 1.4 Adding Markers

### Basic Marker

```python
import folium

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

# Add a simple marker
folium.Marker(
    location=[25.0330, 121.5654],
    popup="Taipei 101"
).add_to(m)

m.save("marker_map.html")
```

### Marker Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    Marker Anatomy                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────┐                                      │
│   │  Popup              │  ← Appears when you CLICK            │
│   │  "Taipei 101"       │    Can contain HTML                  │
│   │  Rating: 4.7        │                                      │
│   └─────────────────────┘                                      │
│            │                                                    │
│   ┌────────┴────────┐                                          │
│   │    Tooltip      │  ← Appears when you HOVER                │
│   │   "Taipei 101"  │    Quick preview                         │
│   └────────┬────────┘                                          │
│            │                                                    │
│         📍 Icon          ← Visual marker on map                │
│                            Customizable color/icon              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Popups and Tooltips

```python
import folium

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

# Marker with popup and tooltip
folium.Marker(
    location=[25.0330, 121.5654],
    popup="<b>Taipei 101</b><br>Height: 508m<br>Rating: ⭐⭐⭐⭐⭐",  # HTML!
    tooltip="Click for details"  # Shows on hover
).add_to(m)

m.save("popup_map.html")
```

### HTML in Popups

```python
import folium

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

# Rich HTML popup
popup_html = """
<div style="width: 200px;">
    <h3 style="color: #333;">Taipei 101</h3>
    <p><b>Category:</b> Landmark</p>
    <p><b>Rating:</b> ⭐ 4.7/5.0</p>
    <p><b>Address:</b> No. 7, Section 5, Xinyi Road</p>
    <a href="https://www.taipei-101.com.tw" target="_blank">Website</a>
</div>
"""

folium.Marker(
    location=[25.0330, 121.5654],
    popup=folium.Popup(popup_html, max_width=300),
    tooltip="Taipei 101"
).add_to(m)

m.save("html_popup_map.html")
```

### Custom Marker Icons

```python
import folium

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

# Different colored markers
folium.Marker(
    location=[25.0330, 121.5654],
    popup="Green Marker",
    icon=folium.Icon(color="green")
).add_to(m)

folium.Marker(
    location=[25.0340, 121.5660],
    popup="Red Marker",
    icon=folium.Icon(color="red")
).add_to(m)

folium.Marker(
    location=[25.0320, 121.5640],
    popup="Blue Marker",
    icon=folium.Icon(color="blue")
).add_to(m)

m.save("colored_markers.html")
```

### Available Icon Colors

```python
# Built-in colors
colors = [
    "red", "blue", "green", "purple", "orange",
    "darkred", "lightred", "beige", "darkblue", "darkgreen",
    "cadetblue", "darkpurple", "white", "pink", "lightblue",
    "lightgreen", "gray", "black", "lightgray"
]
```

### Icons with Font Awesome

```python
import folium

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

# Using Font Awesome icons
folium.Marker(
    location=[25.0330, 121.5654],
    popup="Restaurant",
    icon=folium.Icon(color="red", icon="cutlery", prefix="fa")
).add_to(m)

folium.Marker(
    location=[25.0340, 121.5660],
    popup="Coffee Shop",
    icon=folium.Icon(color="brown", icon="coffee", prefix="fa")
).add_to(m)

folium.Marker(
    location=[25.0320, 121.5640],
    popup="Park",
    icon=folium.Icon(color="green", icon="tree", prefix="fa")
).add_to(m)

m.save("icon_markers.html")
```

### Common Font Awesome Icons

| Icon | Name | Use For |
|------|------|---------|
| 🍴 | `cutlery` | Restaurants |
| ☕ | `coffee` | Cafes |
| 🌲 | `tree` | Parks |
| 🏛️ | `university` | Museums |
| 🏨 | `hotel` | Hotels |
| 🛒 | `shopping-cart` | Shopping |
| ⭐ | `star` | Featured |
| 📍 | `map-marker` | Default |
| 🏠 | `home` | Home/Start |
| 🏁 | `flag` | Destination |

---

# Hour 2: Routes, Shapes, and Multiple Markers

## 2.1 Drawing Routes with PolyLine

### Basic Route Line

```python
import folium

m = folium.Map(location=[25.0400, 121.5400], zoom_start=13)

# Route coordinates (list of [lat, lon] points)
route_coords = [
    [25.0330, 121.5654],  # Start: Taipei 101
    [25.0380, 121.5550],  # Waypoint 1
    [25.0420, 121.5450],  # Waypoint 2
    [25.0478, 121.5170],  # End: Main Station
]

# Draw the route
folium.PolyLine(
    locations=route_coords,
    color="blue",
    weight=5,        # Line thickness
    opacity=0.7      # Transparency (0-1)
).add_to(m)

m.save("route_map.html")
```

### Route with Start/End Markers

```python
import folium

m = folium.Map(location=[25.0400, 121.5400], zoom_start=13)

route_coords = [
    [25.0330, 121.5654],  # Start
    [25.0380, 121.5550],
    [25.0420, 121.5450],
    [25.0478, 121.5170],  # End
]

# Draw route line
folium.PolyLine(
    locations=route_coords,
    color="blue",
    weight=5,
    opacity=0.8
).add_to(m)

# Start marker (green)
folium.Marker(
    location=route_coords[0],
    popup="Start: Taipei 101",
    icon=folium.Icon(color="green", icon="play", prefix="fa")
).add_to(m)

# End marker (red)
folium.Marker(
    location=route_coords[-1],
    popup="End: Main Station",
    icon=folium.Icon(color="red", icon="stop", prefix="fa")
).add_to(m)

m.save("route_with_markers.html")
```

### PolyLine Options

```python
# Different line styles
folium.PolyLine(
    locations=coords,
    color="blue",        # Line color
    weight=5,            # Line thickness (pixels)
    opacity=0.8,         # Transparency (0-1)
    dash_array="10",     # Dashed line: "10" or "5, 10"
    line_cap="round",    # End style: round, butt, square
    line_join="round"    # Join style: round, miter, bevel
).add_to(m)
```

### Route Colors by Type

```python
import folium

m = folium.Map(location=[25.04, 121.54], zoom_start=13)

# Walking route (blue, dashed)
walking_route = [[25.033, 121.565], [25.038, 121.555], [25.042, 121.545]]
folium.PolyLine(
    walking_route,
    color="blue",
    weight=4,
    dash_array="5, 10",
    popup="Walking: 15 min"
).add_to(m)

# Driving route (green, solid)
driving_route = [[25.033, 121.565], [25.040, 121.550], [25.048, 121.517]]
folium.PolyLine(
    driving_route,
    color="green",
    weight=5,
    popup="Driving: 8 min"
).add_to(m)

m.save("multi_route.html")
```

### Animated Routes with AntPath

The `AntPath` plugin draws animated flowing dashes along a route, making it easy to see the direction of travel:

```python
import folium
from folium.plugins import AntPath

m = folium.Map(location=[25.04, 121.54], zoom_start=13)

route_coords = [
    [25.0330, 121.5654],  # Start: Taipei 101
    [25.0380, 121.5550],  # Waypoint 1
    [25.0420, 121.5450],  # Waypoint 2
    [25.0478, 121.5170],  # End: Main Station
]

# Animated route — dashes flow from start to end
AntPath(
    locations=route_coords,
    color="blue",
    weight=5,
    opacity=0.8,
    delay=1000       # Animation speed (ms between frames)
).add_to(m)

# Start marker
folium.Marker(
    route_coords[0],
    popup="Start: Taipei 101",
    icon=folium.Icon(color="green", icon="play", prefix="fa")
).add_to(m)

# End marker
folium.Marker(
    route_coords[-1],
    popup="End: Main Station",
    icon=folium.Icon(color="red", icon="flag", prefix="fa")
).add_to(m)

m.save("animated_route.html")
```

### AntPath Options

```python
AntPath(
    locations=route_coords,
    color="blue",          # Line color
    weight=5,              # Line thickness
    opacity=0.8,           # Transparency
    delay=1000,            # Animation speed (lower = faster)
    dash_array=[10, 20],   # Dash pattern [dash_length, gap_length]
    pulse_color="#ffffff",  # Color of the animated pulse
    reverse=False          # Set True to reverse animation direction
).add_to(m)
```

### Comparing PolyLine vs AntPath

```
┌─────────────────────────────────────────────────────────────────┐
│              PolyLine vs AntPath                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   PolyLine (static):                                           │
│   ┌─────────────────────────────────────────┐                  │
│   │    A ─────────────────────── B          │                  │
│   │         (solid or dashed line)          │                  │
│   └─────────────────────────────────────────┘                  │
│   Best for: simple connections, multiple routes                │
│                                                                 │
│   AntPath (animated):                                          │
│   ┌─────────────────────────────────────────┐                  │
│   │    A ── ▸ ── ▸ ── ▸ ── ▸ ── B          │                  │
│   │         (flowing dashes show direction)  │                  │
│   └─────────────────────────────────────────┘                  │
│   Best for: showing direction, navigation paths                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 2.2 Drawing Shapes

### Circles

```python
import folium

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

# Circle with fixed radius (meters)
folium.Circle(
    location=[25.0330, 121.5654],
    radius=500,           # 500 meters
    color="blue",         # Border color
    fill=True,
    fill_color="lightblue",
    fill_opacity=0.5,
    popup="500m radius"
).add_to(m)

m.save("circle_map.html")
```

### CircleMarker (Fixed Pixel Size)

```python
import folium

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

# CircleMarker - radius in pixels (stays same size when zooming)
folium.CircleMarker(
    location=[25.0330, 121.5654],
    radius=15,            # 15 pixels
    color="red",
    fill=True,
    fill_color="red",
    fill_opacity=0.7,
    popup="Circle Marker"
).add_to(m)

m.save("circle_marker.html")
```

### Polygons

```python
import folium

m = folium.Map(location=[25.0350, 121.5600], zoom_start=15)

# Define polygon corners
polygon_coords = [
    [25.0330, 121.5600],
    [25.0370, 121.5600],
    [25.0370, 121.5650],
    [25.0330, 121.5650],
]

folium.Polygon(
    locations=polygon_coords,
    color="purple",
    fill=True,
    fill_color="purple",
    fill_opacity=0.3,
    popup="District Area"
).add_to(m)

m.save("polygon_map.html")
```

### Rectangles

```python
import folium

m = folium.Map(location=[25.0350, 121.5600], zoom_start=15)

# Define rectangle by bounds: [[south, west], [north, east]]
bounds = [[25.0300, 121.5600], [25.0400, 121.5700]]

folium.Rectangle(
    bounds=bounds,
    color="orange",
    fill=True,
    fill_color="yellow",
    fill_opacity=0.4,
    popup="Bounded Area"
).add_to(m)

m.save("rectangle_map.html")
```

## 2.3 Multiple Markers from Data

### Adding Markers in a Loop

```python
import folium

# Sample place data
places = [
    {"name": "Taipei 101", "coords": [25.0330, 121.5654], "rating": 4.7, "category": "landmark"},
    {"name": "Din Tai Fung", "coords": [25.0339, 121.5645], "rating": 4.9, "category": "restaurant"},
    {"name": "Shilin Night Market", "coords": [25.0878, 121.5241], "rating": 4.5, "category": "market"},
    {"name": "National Palace Museum", "coords": [25.1024, 121.5485], "rating": 4.8, "category": "museum"},
    {"name": "Elephant Mountain", "coords": [25.0275, 121.5701], "rating": 4.6, "category": "nature"},
]

# Create map
m = folium.Map(location=[25.0500, 121.5500], zoom_start=12)

# Add markers for each place
for place in places:
    # Create popup content
    popup_html = f"""
    <b>{place['name']}</b><br>
    Rating: {'⭐' * int(place['rating'])} {place['rating']}<br>
    Category: {place['category'].title()}
    """

    folium.Marker(
        location=place['coords'],
        popup=popup_html,
        tooltip=place['name']
    ).add_to(m)

m.save("multiple_markers.html")
```

### Color-Coded Markers by Category

```python
import folium

places = [
    {"name": "Taipei 101", "coords": [25.0330, 121.5654], "category": "landmark"},
    {"name": "Din Tai Fung", "coords": [25.0339, 121.5645], "category": "restaurant"},
    {"name": "Shilin Night Market", "coords": [25.0878, 121.5241], "category": "market"},
    {"name": "National Palace Museum", "coords": [25.1024, 121.5485], "category": "museum"},
    {"name": "Elephant Mountain", "coords": [25.0275, 121.5701], "category": "nature"},
]

# Color and icon mapping
category_styles = {
    "landmark": {"color": "purple", "icon": "building"},
    "restaurant": {"color": "red", "icon": "cutlery"},
    "market": {"color": "orange", "icon": "shopping-cart"},
    "museum": {"color": "blue", "icon": "university"},
    "nature": {"color": "green", "icon": "tree"},
}

m = folium.Map(location=[25.0500, 121.5500], zoom_start=12)

for place in places:
    style = category_styles.get(place['category'], {"color": "gray", "icon": "info"})

    folium.Marker(
        location=place['coords'],
        popup=place['name'],
        tooltip=f"{place['name']} ({place['category']})",
        icon=folium.Icon(color=style['color'], icon=style['icon'], prefix='fa')
    ).add_to(m)

m.save("categorized_markers.html")
```

### Markers with Rating-Based Size

```python
import folium

places = [
    {"name": "Place A", "coords": [25.033, 121.565], "rating": 4.9},
    {"name": "Place B", "coords": [25.040, 121.560], "rating": 4.5},
    {"name": "Place C", "coords": [25.035, 121.570], "rating": 3.8},
    {"name": "Place D", "coords": [25.045, 121.555], "rating": 4.2},
]

m = folium.Map(location=[25.038, 121.562], zoom_start=14)

for place in places:
    # Size based on rating (bigger = higher rating)
    radius = place['rating'] * 3  # 3.8 → 11.4, 4.9 → 14.7

    # Color based on rating
    if place['rating'] >= 4.5:
        color = "green"
    elif place['rating'] >= 4.0:
        color = "orange"
    else:
        color = "red"

    folium.CircleMarker(
        location=place['coords'],
        radius=radius,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=f"{place['name']}: {place['rating']}⭐"
    ).add_to(m)

m.save("rating_sized_markers.html")
```

### Auto-Fit Map to Show All Markers

When placing multiple markers, instead of manually calculating the center and zoom level, use `fit_bounds()` to automatically adjust the map view:

```python
import folium

places = [
    {"name": "Taipei 101", "coords": [25.0330, 121.5654]},
    {"name": "Shilin Night Market", "coords": [25.0878, 121.5241]},
    {"name": "National Palace Museum", "coords": [25.1024, 121.5485]},
    {"name": "Longshan Temple", "coords": [25.0372, 121.4999]},
]

# Create map (initial location doesn't matter much)
m = folium.Map(location=[25.05, 121.55], zoom_start=12)

# Add markers
for place in places:
    folium.Marker(
        location=place["coords"],
        popup=place["name"],
        tooltip=place["name"]
    ).add_to(m)

# Auto-fit: compute the bounding box of all coordinates
lats = [p["coords"][0] for p in places]
lons = [p["coords"][1] for p in places]

# fit_bounds takes [[south, west], [north, east]]
m.fit_bounds([
    [min(lats), min(lons)],  # Southwest corner
    [max(lats), max(lons)]   # Northeast corner
])

m.save("auto_fit_map.html")
# The map automatically zooms to show ALL markers!
```

### Manual Center vs fit_bounds

```
┌─────────────────────────────────────────────────────────────────┐
│              Manual Center vs fit_bounds                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Manual (what we did before):                                  │
│   avg_lat = sum(lats) / len(lats)                              │
│   avg_lon = sum(lons) / len(lons)                              │
│   → May miss markers if they're spread out                     │
│   → Need to guess the right zoom level                         │
│                                                                 │
│   fit_bounds (better):                                          │
│   m.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])       │
│   → Guarantees ALL markers are visible                         │
│   → Zoom level is calculated automatically                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 2.4 Feature Groups and Layer Control

### Organizing Markers into Groups

```python
import folium

m = folium.Map(location=[25.0500, 121.5500], zoom_start=12)

# Create feature groups for different categories
restaurants = folium.FeatureGroup(name="Restaurants")
parks = folium.FeatureGroup(name="Parks")
museums = folium.FeatureGroup(name="Museums")

# Add markers to respective groups
folium.Marker([25.033, 121.565], popup="Restaurant 1",
              icon=folium.Icon(color="red")).add_to(restaurants)
folium.Marker([25.040, 121.560], popup="Restaurant 2",
              icon=folium.Icon(color="red")).add_to(restaurants)

folium.Marker([25.035, 121.570], popup="Park 1",
              icon=folium.Icon(color="green")).add_to(parks)
folium.Marker([25.045, 121.555], popup="Park 2",
              icon=folium.Icon(color="green")).add_to(parks)

folium.Marker([25.050, 121.550], popup="Museum 1",
              icon=folium.Icon(color="blue")).add_to(museums)

# Add groups to map
restaurants.add_to(m)
parks.add_to(m)
museums.add_to(m)

# Add layer control (checkbox to toggle groups)
folium.LayerControl().add_to(m)

m.save("layer_control.html")
```

### Layer Control Interface

```
┌─────────────────────────────────────────────────────────────────┐
│                    Layer Control                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────────────┐                                     │
│   │ ☑ Restaurants        │  ← Toggle visibility                │
│   │ ☑ Parks              │                                     │
│   │ ☐ Museums            │  ← Unchecked = hidden               │
│   └──────────────────────┘                                     │
│                                                                 │
│   Users can show/hide different layers                         │
│   Great for maps with many markers                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

# Hour 3: Flask Integration and Complete Application

## 3.1 Embedding Maps in Flask

### Basic Flask + Folium Integration

```python
from flask import Flask, render_template_string
import folium

app = Flask(__name__)

@app.route("/map")
def show_map():
    # Create map
    m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)
    folium.Marker([25.0330, 121.5654], popup="Taipei 101").add_to(m)

    # Get HTML representation
    map_html = m._repr_html_()

    # Embed in template
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Map</title>
            <style>
                body { margin: 0; padding: 0; }
                #map-container { height: 100vh; }
            </style>
        </head>
        <body>
            <div id="map-container">
                {{ map_html | safe }}
            </div>
        </body>
        </html>
    """, map_html=map_html)

if __name__ == "__main__":
    app.run(debug=True)
```

### Map with Header and Controls

```python
from flask import Flask, render_template_string, request
import folium

app = Flask(__name__)

PLACES = [
    {"id": 1, "name": "Taipei 101", "coords": [25.0330, 121.5654], "category": "landmark"},
    {"id": 2, "name": "Din Tai Fung", "coords": [25.0339, 121.5645], "category": "restaurant"},
    {"id": 3, "name": "Shilin Night Market", "coords": [25.0878, 121.5241], "category": "market"},
]

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart City Navigator - Map</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; }
        header {
            background: #2c3e50;
            color: white;
            padding: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        header a { color: white; margin-left: 1rem; text-decoration: none; }
        #map-container { height: calc(100vh - 60px); }
        .controls {
            display: flex;
            gap: 1rem;
        }
        select, button {
            padding: 0.5rem;
            border-radius: 4px;
            border: none;
        }
    </style>
</head>
<body>
    <header>
        <h1>Smart City Navigator</h1>
        <div class="controls">
            <form method="GET" style="display: flex; gap: 0.5rem;">
                <select name="category">
                    <option value="">All Categories</option>
                    <option value="landmark" {{ 'selected' if category == 'landmark' else '' }}>Landmarks</option>
                    <option value="restaurant" {{ 'selected' if category == 'restaurant' else '' }}>Restaurants</option>
                    <option value="market" {{ 'selected' if category == 'market' else '' }}>Markets</option>
                </select>
                <button type="submit">Filter</button>
            </form>
            <a href="/">Home</a>
        </div>
    </header>
    <div id="map-container">
        {{ map_html | safe }}
    </div>
</body>
</html>
"""

@app.route("/map")
def show_map():
    category = request.args.get("category", "")

    # Filter places
    if category:
        filtered_places = [p for p in PLACES if p["category"] == category]
    else:
        filtered_places = PLACES

    # Calculate center (average of all coordinates)
    if filtered_places:
        avg_lat = sum(p["coords"][0] for p in filtered_places) / len(filtered_places)
        avg_lon = sum(p["coords"][1] for p in filtered_places) / len(filtered_places)
        center = [avg_lat, avg_lon]
    else:
        center = [25.0500, 121.5500]

    # Create map
    m = folium.Map(location=center, zoom_start=12)

    # Add markers
    for place in filtered_places:
        folium.Marker(
            location=place["coords"],
            popup=place["name"],
            tooltip=place["name"]
        ).add_to(m)

    map_html = m._repr_html_()

    return render_template_string(TEMPLATE, map_html=map_html, category=category)

if __name__ == "__main__":
    app.run(debug=True)
```

## 3.2 Dynamic Route Visualization

### Show Route Between Places

```python
from flask import Flask, render_template_string, request
import folium

app = Flask(__name__)

PLACES = {
    1: {"name": "Taipei 101", "coords": [25.0330, 121.5654]},
    2: {"name": "Main Station", "coords": [25.0478, 121.5170]},
    3: {"name": "Shilin Market", "coords": [25.0878, 121.5241]},
}

# Simplified route data (in real app, use OSRM API)
ROUTES = {
    (1, 2): {
        "coords": [[25.033, 121.565], [25.038, 121.545], [25.043, 121.525], [25.048, 121.517]],
        "distance": 5.2,
        "duration": 15
    },
    (1, 3): {
        "coords": [[25.033, 121.565], [25.050, 121.540], [25.070, 121.530], [25.088, 121.524]],
        "distance": 7.8,
        "duration": 22
    },
}

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Route Map</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; }
        .controls { padding: 1rem; background: #f0f0f0; }
        select, button { padding: 0.5rem; margin-right: 0.5rem; }
        #map-container { height: calc(100vh - 120px); }
        .info { padding: 0.5rem; background: #e0e0e0; }
    </style>
</head>
<body>
    <div class="controls">
        <form method="GET">
            <label>From:</label>
            <select name="start">
                {% for id, place in places.items() %}
                <option value="{{ id }}" {{ 'selected' if start == id else '' }}>{{ place.name }}</option>
                {% endfor %}
            </select>
            <label>To:</label>
            <select name="end">
                {% for id, place in places.items() %}
                <option value="{{ id }}" {{ 'selected' if end == id else '' }}>{{ place.name }}</option>
                {% endfor %}
            </select>
            <button type="submit">Show Route</button>
        </form>
    </div>
    {% if route_info %}
    <div class="info">
        <strong>Distance:</strong> {{ route_info.distance }} km |
        <strong>Duration:</strong> {{ route_info.duration }} min
    </div>
    {% endif %}
    <div id="map-container">
        {{ map_html | safe }}
    </div>
</body>
</html>
"""

@app.route("/route")
def show_route():
    start = request.args.get("start", 1, type=int)
    end = request.args.get("end", 2, type=int)

    # Get route data
    route_key = (start, end)
    route_info = ROUTES.get(route_key) or ROUTES.get((end, start))

    # Create map
    start_place = PLACES[start]
    end_place = PLACES[end]

    # Center between start and end
    center = [
        (start_place["coords"][0] + end_place["coords"][0]) / 2,
        (start_place["coords"][1] + end_place["coords"][1]) / 2
    ]

    m = folium.Map(location=center, zoom_start=12)

    # Add route line if available
    if route_info:
        folium.PolyLine(
            locations=route_info["coords"],
            color="blue",
            weight=5,
            opacity=0.8
        ).add_to(m)

    # Add markers
    folium.Marker(
        start_place["coords"],
        popup=f"Start: {start_place['name']}",
        icon=folium.Icon(color="green", icon="play", prefix="fa")
    ).add_to(m)

    folium.Marker(
        end_place["coords"],
        popup=f"End: {end_place['name']}",
        icon=folium.Icon(color="red", icon="flag", prefix="fa")
    ).add_to(m)

    map_html = m._repr_html_()

    return render_template_string(
        TEMPLATE,
        map_html=map_html,
        places=PLACES,
        start=start,
        end=end,
        route_info=route_info
    )

if __name__ == "__main__":
    app.run(debug=True)
```

## 3.3 Complete Smart City Navigator Map

### Full Application Example

```python
from flask import Flask, render_template_string, request, jsonify
import folium
from folium.plugins import MarkerCluster

app = Flask(__name__)

# Sample data
PLACES = [
    {"id": 1, "name": "Taipei 101", "coords": [25.0330, 121.5654], "rating": 4.7, "category": "landmark"},
    {"id": 2, "name": "Din Tai Fung", "coords": [25.0339, 121.5645], "rating": 4.9, "category": "restaurant"},
    {"id": 3, "name": "Shilin Night Market", "coords": [25.0878, 121.5241], "rating": 4.5, "category": "market"},
    {"id": 4, "name": "National Palace Museum", "coords": [25.1024, 121.5485], "rating": 4.8, "category": "museum"},
    {"id": 5, "name": "Elephant Mountain", "coords": [25.0275, 121.5701], "rating": 4.6, "category": "nature"},
    {"id": 6, "name": "Longshan Temple", "coords": [25.0372, 121.4999], "rating": 4.6, "category": "temple"},
    {"id": 7, "name": "Taipei Main Station", "coords": [25.0478, 121.5170], "rating": 4.2, "category": "transport"},
    {"id": 8, "name": "Ximending", "coords": [25.0423, 121.5081], "rating": 4.4, "category": "shopping"},
]

CATEGORY_STYLES = {
    "landmark": {"color": "purple", "icon": "building"},
    "restaurant": {"color": "red", "icon": "cutlery"},
    "market": {"color": "orange", "icon": "shopping-cart"},
    "museum": {"color": "blue", "icon": "university"},
    "nature": {"color": "green", "icon": "tree"},
    "temple": {"color": "darkred", "icon": "institution"},
    "transport": {"color": "gray", "icon": "train"},
    "shopping": {"color": "pink", "icon": "shopping-bag"},
}

BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart City Navigator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        header h1 { font-size: 1.5rem; }

        nav a {
            color: white;
            text-decoration: none;
            margin-left: 1.5rem;
            opacity: 0.9;
        }
        nav a:hover { opacity: 1; }

        .toolbar {
            background: #f8f9fa;
            padding: 1rem 2rem;
            border-bottom: 1px solid #ddd;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            align-items: center;
        }

        .toolbar select, .toolbar input, .toolbar button {
            padding: 0.5rem 1rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 0.9rem;
        }

        .toolbar button {
            background: #667eea;
            color: white;
            border: none;
            cursor: pointer;
        }
        .toolbar button:hover { background: #5a6fd6; }

        #map-container {
            height: calc(100vh - 130px);
        }

        .legend {
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
            font-size: 0.85rem;
        }
        .legend h4 { margin-bottom: 0.5rem; }
        .legend-item {
            display: flex;
            align-items: center;
            margin: 0.3rem 0;
        }
        .legend-color {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 0.5rem;
        }
    </style>
</head>
<body>
    <header>
        <h1>🗺️ Smart City Navigator</h1>
        <nav>
            <a href="/">Home</a>
            <a href="/map">Map</a>
            <a href="/places">Places</a>
        </nav>
    </header>

    <div class="toolbar">
        <form method="GET" style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <select name="category">
                <option value="">All Categories</option>
                {% for cat in categories %}
                <option value="{{ cat }}" {{ 'selected' if selected_category == cat else '' }}>
                    {{ cat | title }}
                </option>
                {% endfor %}
            </select>
            <select name="min_rating">
                <option value="">Any Rating</option>
                <option value="4.5" {{ 'selected' if min_rating == 4.5 else '' }}>4.5+ ⭐</option>
                <option value="4.0" {{ 'selected' if min_rating == 4.0 else '' }}>4.0+ ⭐</option>
                <option value="3.5" {{ 'selected' if min_rating == 3.5 else '' }}>3.5+ ⭐</option>
            </select>
            <button type="submit">Apply Filters</button>
        </form>
        <span style="color: #666;">Showing {{ place_count }} places</span>
    </div>

    <div id="map-container">
        {{ map_html | safe }}
    </div>

    <div class="legend">
        <h4>Categories</h4>
        {% for cat, style in category_styles.items() %}
        <div class="legend-item">
            <div class="legend-color" style="background: {{ style.color }};"></div>
            <span>{{ cat | title }}</span>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return """
    <h1>Smart City Navigator</h1>
    <p><a href="/map">View Map</a></p>
    """

@app.route("/map")
def show_map():
    # Get filter parameters
    category = request.args.get("category", "")
    min_rating = request.args.get("min_rating", 0, type=float)

    # Filter places
    filtered = PLACES
    if category:
        filtered = [p for p in filtered if p["category"] == category]
    if min_rating:
        filtered = [p for p in filtered if p["rating"] >= min_rating]

    # Calculate center
    if filtered:
        avg_lat = sum(p["coords"][0] for p in filtered) / len(filtered)
        avg_lon = sum(p["coords"][1] for p in filtered) / len(filtered)
        center = [avg_lat, avg_lon]
        zoom = 12
    else:
        center = [25.0500, 121.5500]
        zoom = 11

    # Create map
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="CartoDB positron"
    )

    # Add markers
    for place in filtered:
        style = CATEGORY_STYLES.get(place["category"], {"color": "gray", "icon": "info"})

        popup_html = f"""
        <div style="min-width: 150px;">
            <h4 style="margin: 0 0 5px 0;">{place['name']}</h4>
            <p style="margin: 0;">{'⭐' * int(place['rating'])} {place['rating']}</p>
            <p style="margin: 5px 0 0 0; color: #666;">{place['category'].title()}</p>
        </div>
        """

        folium.Marker(
            location=place["coords"],
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=place["name"],
            icon=folium.Icon(color=style["color"], icon=style["icon"], prefix="fa")
        ).add_to(m)

    map_html = m._repr_html_()

    # Get unique categories
    categories = sorted(set(p["category"] for p in PLACES))

    return render_template_string(
        BASE_TEMPLATE,
        map_html=map_html,
        categories=categories,
        category_styles=CATEGORY_STYLES,
        selected_category=category,
        min_rating=min_rating,
        place_count=len(filtered)
    )

if __name__ == "__main__":
    app.run(debug=True)
```

## 3.4 Advanced Features

### Marker Clustering

When you have many markers, use clustering to improve performance:

```python
from folium.plugins import MarkerCluster

m = folium.Map(location=[25.05, 121.55], zoom_start=11)

# Create marker cluster
marker_cluster = MarkerCluster().add_to(m)

# Add many markers to the cluster
for place in many_places:
    folium.Marker(
        location=place["coords"],
        popup=place["name"]
    ).add_to(marker_cluster)  # Add to cluster, not directly to map

m.save("clustered_map.html")
```

### Heatmaps

```python
from folium.plugins import HeatMap

m = folium.Map(location=[25.05, 121.55], zoom_start=12)

# List of [lat, lon, weight] or just [lat, lon]
heat_data = [
    [25.033, 121.565, 0.8],  # Taipei 101 area (high density)
    [25.035, 121.563, 0.7],
    [25.034, 121.566, 0.6],
    # ... more points
]

HeatMap(heat_data).add_to(m)

m.save("heatmap.html")
```

### Map Enhancement Plugins

Folium includes several one-line plugins that make your maps feel more polished:

#### MiniMap — Overview Navigation

Adds a small overview map in the corner for quick navigation:

```python
import folium
from folium.plugins import MiniMap

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

folium.Marker([25.0330, 121.5654], popup="Taipei 101").add_to(m)

# Add a mini overview map in the bottom-right corner
MiniMap(
    toggle_display=True,   # Allow user to collapse it
    width=150,
    height=150
).add_to(m)

m.save("minimap.html")
```

#### Fullscreen — Fullscreen Toggle Button

```python
import folium
from folium.plugins import Fullscreen

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

folium.Marker([25.0330, 121.5654], popup="Taipei 101").add_to(m)

# Add a fullscreen button to the map
Fullscreen(
    position="topleft",           # Button position
    title="Enter Fullscreen",     # Tooltip when not fullscreen
    title_cancel="Exit Fullscreen"  # Tooltip when fullscreen
).add_to(m)

m.save("fullscreen_map.html")
```

#### LocateControl — "Where Am I?" Button

Uses the browser's geolocation to show the user's current position:

```python
import folium
from folium.plugins import LocateControl

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

folium.Marker([25.0330, 121.5654], popup="Taipei 101").add_to(m)

# Add a "locate me" button
LocateControl(
    position="topleft",
    strings={"title": "Find my location"}
).add_to(m)

m.save("locate_me.html")
# Click the button — the browser asks for location permission,
# then shows your position on the map!
```

#### Combining Multiple Plugins

You can add all these enhancements together for a polished map:

```python
import folium
from folium.plugins import MiniMap, Fullscreen, LocateControl, MousePosition

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

folium.Marker([25.0330, 121.5654], popup="Taipei 101").add_to(m)

# Add all enhancements — one line each!
MiniMap(toggle_display=True).add_to(m)
Fullscreen().add_to(m)
LocateControl().add_to(m)
MousePosition(position="topright", prefix="Coords:").add_to(m)

m.save("enhanced_map.html")
```

```
┌─────────────────────────────────────────────────────────────────┐
│              Enhanced Map Layout                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────┐          │
│   │ [⛶] [📍]              Coords: 25.0330 | 121.5654│          │
│   │ Fullscreen  Locate            MousePosition     │          │
│   │                                                 │          │
│   │                                                 │          │
│   │              MAP CONTENT                        │          │
│   │                                                 │          │
│   │                                                 │          │
│   │                                    ┌───────┐   │          │
│   │                                    │MiniMap│   │          │
│   │                                    └───────┘   │          │
│   └─────────────────────────────────────────────────┘          │
│                                                                 │
│   4 lines of code → professional-looking map                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### MeasureControl — Distance Measurement Tool

Lets users measure distances and areas directly on the map:

```python
import folium
from folium.plugins import MeasureControl

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

folium.Marker([25.0330, 121.5654], popup="Taipei 101").add_to(m)
folium.Marker([25.0478, 121.5170], popup="Main Station").add_to(m)

# Add measurement tool
MeasureControl(
    position="topleft",
    primary_length_unit="kilometers",
    secondary_length_unit="meters",
    primary_area_unit="sqmeters"
).add_to(m)

m.save("measure_map.html")
# Click the ruler icon, then click points on the map to measure distance!
```

### ClickForMarker — Interactive Marker Placement

Lets users click on the map to place new markers:

```python
import folium
from folium.plugins import ClickForMarker

m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

# Existing markers
folium.Marker([25.0330, 121.5654], popup="Taipei 101").add_to(m)

# Enable click-to-add-marker
ClickForMarker(
    popup="New marker at<br>{lat}, {lng}"  # {lat} and {lng} are replaced automatically
).add_to(m)

m.save("click_marker.html")
# Click anywhere on the map to drop a new marker!
```

```
┌─────────────────────────────────────────────────────────────────┐
│              ClickForMarker Demo                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────┐          │
│   │                                                 │          │
│   │    📍 Taipei 101                                │          │
│   │                                                 │          │
│   │              👆 click here                      │          │
│   │               │                                 │          │
│   │              📍 New!                            │          │
│   │         ┌─────────────────┐                     │          │
│   │         │ New marker at   │                     │          │
│   │         │ 25.035, 121.560 │                     │          │
│   │         └─────────────────┘                     │          │
│   └─────────────────────────────────────────────────┘          │
│                                                                 │
│   Users can interactively place markers by clicking             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### DivIcon — Custom HTML Markers

Use HTML and CSS to create custom marker icons, such as numbered step markers for a route:

```python
import folium

m = folium.Map(location=[25.0400, 121.5400], zoom_start=13)

# Route stops with numbered markers
stops = [
    {"name": "Taipei 101", "coords": [25.0330, 121.5654]},
    {"name": "Ximending", "coords": [25.0423, 121.5081]},
    {"name": "Longshan Temple", "coords": [25.0372, 121.4999]},
]

for i, stop in enumerate(stops, start=1):
    # Create a numbered circle using HTML/CSS
    icon_html = f"""
    <div style="
        background-color: #667eea;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 14px;
        border: 2px solid white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    ">{i}</div>
    """

    folium.Marker(
        location=stop["coords"],
        popup=f"Stop {i}: {stop['name']}",
        tooltip=f"Stop {i}: {stop['name']}",
        icon=folium.DivIcon(
            html=icon_html,
            icon_size=(30, 30),
            icon_anchor=(15, 15)   # Center the icon on the coordinate
        )
    ).add_to(m)

m.save("numbered_stops.html")
```

### DivIcon — Label Markers

```python
import folium

m = folium.Map(location=[25.0330, 121.5654], zoom_start=15)

# Marker with a text label underneath
label_html = """
<div style="text-align: center;">
    <div style="font-size: 24px;">📍</div>
    <div style="
        background: white;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: bold;
        white-space: nowrap;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    ">Taipei 101</div>
</div>
"""

folium.Marker(
    location=[25.0330, 121.5654],
    icon=folium.DivIcon(
        html=label_html,
        icon_size=(80, 40),
        icon_anchor=(40, 40)
    )
).add_to(m)

m.save("label_marker.html")
```

```
┌─────────────────────────────────────────────────────────────────┐
│              DivIcon Examples                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Numbered Stops:                Label Marker:                  │
│   ┌───────────────┐             ┌───────────────┐              │
│   │               │             │               │              │
│   │   ① ── ② ── ③│             │      📍       │              │
│   │               │             │  [Taipei 101] │              │
│   └───────────────┘             └───────────────┘              │
│                                                                 │
│   DivIcon lets you use any HTML/CSS as a marker!               │
│   • Numbered route steps                                        │
│   • Text labels                                                 │
│   • Custom shapes and colors                                    │
│   • Emoji markers                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Saving Maps as Files

```python
import folium

m = folium.Map(location=[25.033, 121.565], zoom_start=14)
folium.Marker([25.033, 121.565], popup="Taipei 101").add_to(m)

# Save as HTML file
m.save("output/my_map.html")

# Get HTML string (for embedding)
html_string = m._repr_html_()
```

---

## Summary

### Key Concepts

```
┌─────────────────────────────────────────────────────────────────┐
│                    Folium Map Development                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   MAP CREATION                                                  │
│   folium.Map(location=[lat, lon], zoom_start=14)               │
│   m.fit_bounds([[south, west], [north, east]])                 │
│   m.save("map.html")                                            │
│                                                                 │
│   MARKERS                                                       │
│   folium.Marker(location, popup, tooltip, icon)                │
│   folium.CircleMarker(location, radius, color)                 │
│   folium.Icon(color, icon, prefix)                             │
│   folium.DivIcon(html, icon_size, icon_anchor)                 │
│                                                                 │
│   SHAPES & ROUTES                                               │
│   folium.PolyLine(locations, color, weight)                    │
│   folium.Circle(location, radius, color, fill)                 │
│   folium.Polygon(locations, color, fill)                       │
│   AntPath(locations, color, weight, delay)                     │
│                                                                 │
│   ORGANIZATION                                                  │
│   folium.FeatureGroup(name)                                    │
│   folium.LayerControl()                                         │
│                                                                 │
│   PLUGINS (from folium.plugins)                                 │
│   MousePosition()    — show coordinates on hover               │
│   LatLngPopup()      — click to see coordinates                │
│   MiniMap()          — overview navigation                     │
│   Fullscreen()       — fullscreen toggle                       │
│   LocateControl()    — "where am I?" button                    │
│   MeasureControl()   — distance measurement                    │
│   ClickForMarker()   — click to place markers                  │
│   MarkerCluster()    — group dense markers                     │
│   HeatMap()          — density visualization                   │
│   AntPath()          — animated directional routes             │
│                                                                 │
│   FLASK INTEGRATION                                             │
│   map_html = m._repr_html_()                                   │
│   {{ map_html | safe }}                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Best Practices

1. **Use `fit_bounds()`** instead of manually calculating center and zoom
2. **Choose appropriate zoom level** based on data density
3. **Use consistent marker styles** for categories
4. **Add tooltips** for quick identification
5. **Use layer control** for complex maps
6. **Consider marker clustering** for many points
7. **Add map plugins** (MiniMap, Fullscreen, LocateControl) for polished UX
8. **Test in multiple browsers**

### Quick Reference

```python
import folium
from folium.plugins import MiniMap, Fullscreen, LocateControl, MousePosition, AntPath

# Create map
m = folium.Map(location=[lat, lon], zoom_start=14, tiles="CartoDB positron")

# Add marker
folium.Marker(
    location=[lat, lon],
    popup="<b>Title</b><br>Description",
    tooltip="Hover text",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

# Draw route (static)
folium.PolyLine(
    locations=[[lat1, lon1], [lat2, lon2], ...],
    color="blue",
    weight=5
).add_to(m)

# Draw route (animated)
AntPath(
    locations=[[lat1, lon1], [lat2, lon2], ...],
    color="blue",
    weight=5,
    delay=1000
).add_to(m)

# Custom HTML marker
folium.Marker(
    location=[lat, lon],
    icon=folium.DivIcon(html="<div>①</div>", icon_size=(30, 30))
).add_to(m)

# Auto-fit to show all markers
m.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])

# Add map enhancements (one line each!)
MiniMap().add_to(m)
Fullscreen().add_to(m)
LocateControl().add_to(m)
MousePosition(prefix="Coords:").add_to(m)

# Save or embed
m.save("map.html")
html = m._repr_html_()
```
