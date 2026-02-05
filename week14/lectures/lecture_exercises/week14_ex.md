# Week 14 Lab: Interactive Maps with Folium

## Lab Overview

In this lab, you'll create interactive maps using the Folium library. You'll practice creating maps, adding markers, drawing routes, and integrating maps with Flask.

**Time:** 2 hours

**Prerequisites:**
- Folium installed (`pip install folium`)
- Flask installed (`pip install flask`)
- Basic understanding of coordinates (latitude, longitude)

---

## Setup

```bash
# Install required packages
pip install folium flask

# Create project folder
mkdir folium_lab
cd folium_lab
```

---

## Exercise 1: Your First Map (10 minutes)

### Objective
Create a basic map and save it as an HTML file.

### Task

Create a map centered on a location of your choice (your city, university, or favorite place).

### Starter Code

```python
# exercise1.py
import folium

# TODO: Create a map centered on your chosen location
# Hint: Use folium.Map(location=[lat, lon], zoom_start=14)


# TODO: Save the map to "my_first_map.html"
# Hint: Use m.save("filename.html")


print("Map saved! Open my_first_map.html in your browser.")
```

### Requirements

1. Center the map on a specific location
2. Set an appropriate zoom level (try 12-15)
3. Save the map as an HTML file
4. Open the file in a browser to verify

### Expected Output

An HTML file that shows an interactive map when opened in a browser.

---

## Exercise 2: Adding Markers (15 minutes)

### Objective
Add multiple markers with popups and tooltips.

### Task

Create a map with at least 5 markers representing places you'd like to visit.

### Starter Code

```python
# exercise2.py
import folium

# Sample data - replace with your own places!
places = [
    {"name": "Place 1", "coords": [25.033, 121.565], "description": "A great spot"},
    {"name": "Place 2", "coords": [25.040, 121.560], "description": "Must visit"},
    # TODO: Add more places
]

# Create map
m = folium.Map(location=[25.035, 121.560], zoom_start=13)

# TODO: Loop through places and add markers
# Each marker should have:
# - popup with name and description
# - tooltip with just the name


# Save the map
m.save("places_map.html")
print("Map saved with markers!")
```

### Requirements

1. At least 5 markers
2. Each marker has a popup (shows on click)
3. Each marker has a tooltip (shows on hover)
4. Popups include HTML formatting (bold names, line breaks)

### Expected Features

- Click a marker → popup with details
- Hover over a marker → tooltip with name

---

## Exercise 3: Custom Icons by Category (20 minutes)

### Objective
Use different icons and colors based on place category.

### Task

Create a map where markers have different icons and colors depending on their category.

### Starter Code

```python
# exercise3.py
import folium

places = [
    {"name": "Best Pizza", "coords": [25.033, 121.565], "category": "restaurant"},
    {"name": "Coffee Corner", "coords": [25.040, 121.560], "category": "cafe"},
    {"name": "Central Park", "coords": [25.045, 121.555], "category": "park"},
    {"name": "Art Museum", "coords": [25.050, 121.545], "category": "museum"},
    {"name": "Shopping Mall", "coords": [25.038, 121.550], "category": "shopping"},
]

# TODO: Define icon styles for each category
# Example:
# styles = {
#     "restaurant": {"color": "red", "icon": "cutlery"},
#     ...
# }


# Create map
m = folium.Map(location=[25.040, 121.555], zoom_start=14)

# TODO: Loop through places and add markers with category-specific icons
# Hint: folium.Icon(color=..., icon=..., prefix='fa')


m.save("categorized_map.html")
```

### Icon Reference

| Category | Suggested Color | Suggested Icon |
|----------|-----------------|----------------|
| restaurant | red | cutlery |
| cafe | orange | coffee |
| park | green | tree |
| museum | blue | university |
| shopping | pink | shopping-cart |

### Expected Output

A map where you can visually distinguish categories by marker color and icon.

---

## Exercise 4: Drawing Routes (20 minutes)

### Objective
Draw a route connecting multiple locations.

### Task

Create a map showing a route between a starting point and destination, with waypoints.

### Starter Code

```python
# exercise4.py
import folium

# Route coordinates (start → waypoints → end)
route = [
    {"name": "Start: Home", "coords": [25.033, 121.565]},
    {"name": "Stop 1: Coffee", "coords": [25.038, 121.555]},
    {"name": "Stop 2: Park", "coords": [25.042, 121.545]},
    {"name": "End: Office", "coords": [25.048, 121.530]},
]

# Extract just coordinates for the polyline
route_coords = [point["coords"] for point in route]

# Create map (center between start and end)
center_lat = (route[0]["coords"][0] + route[-1]["coords"][0]) / 2
center_lon = (route[0]["coords"][1] + route[-1]["coords"][1]) / 2
m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

# TODO: Draw the route line
# Hint: folium.PolyLine(locations=route_coords, color="blue", weight=5)


# TODO: Add start marker (green, with play icon)


# TODO: Add end marker (red, with flag icon)


# TODO: Add numbered markers for waypoints


m.save("route_map.html")
```

### Requirements

1. Blue route line connecting all points
2. Green "play" icon at start
3. Red "flag" icon at end
4. Numbered markers at waypoints
5. Popup on route line showing total distance estimate

---

## Exercise 5: Circles and Areas (15 minutes)

### Objective
Use circles to show areas of interest.

### Task

Create a map that shows:
1. A large circle showing "within 1km" of a central point
2. Circle markers sized by rating

### Starter Code

```python
# exercise5.py
import folium

# Central location
center = [25.033, 121.565]

# Places with ratings
places = [
    {"name": "Place A", "coords": [25.035, 121.567], "rating": 4.8},
    {"name": "Place B", "coords": [25.031, 121.563], "rating": 4.2},
    {"name": "Place C", "coords": [25.037, 121.560], "rating": 3.5},
    {"name": "Place D", "coords": [25.030, 121.568], "rating": 4.5},
]

m = folium.Map(location=center, zoom_start=15)

# TODO: Add a Circle showing 500m radius from center
# Hint: folium.Circle(location, radius=500, color="blue", fill=True)


# TODO: Add CircleMarkers for each place
# - Radius based on rating (e.g., rating * 3)
# - Color based on rating (green >= 4.5, orange >= 4.0, red < 4.0)


m.save("circles_map.html")
```

### Expected Output

- A large translucent circle showing the "within 500m" area
- Circle markers where size indicates rating

---

## Exercise 6: Layer Control (20 minutes)

### Objective
Organize markers into toggleable layers.

### Task

Create a map with multiple layers that users can show/hide.

### Starter Code

```python
# exercise6.py
import folium

# Sample data
restaurants = [
    {"name": "Pizza Place", "coords": [25.033, 121.565]},
    {"name": "Sushi Bar", "coords": [25.040, 121.560]},
]

parks = [
    {"name": "Central Park", "coords": [25.045, 121.555]},
    {"name": "Riverside Park", "coords": [25.050, 121.550]},
]

museums = [
    {"name": "Art Museum", "coords": [25.055, 121.545]},
    {"name": "History Museum", "coords": [25.060, 121.540]},
]

m = folium.Map(location=[25.045, 121.555], zoom_start=12)

# TODO: Create feature groups for each category
# restaurant_group = folium.FeatureGroup(name="Restaurants")


# TODO: Add markers to their respective groups


# TODO: Add all groups to the map


# TODO: Add layer control
# Hint: folium.LayerControl().add_to(m)


m.save("layered_map.html")
```

### Expected Output

A map with a layer control panel in the corner. Users can check/uncheck boxes to show/hide different categories.

---

## Exercise 7: Flask Integration (25 minutes)

### Objective
Embed a Folium map in a Flask web application.

### Task

Create a Flask app that displays an interactive map.

### Starter Code

```python
# exercise7.py
from flask import Flask, render_template_string
import folium

app = Flask(__name__)

PLACES = [
    {"id": 1, "name": "Taipei 101", "coords": [25.0330, 121.5654], "rating": 4.7},
    {"id": 2, "name": "Night Market", "coords": [25.0878, 121.5241], "rating": 4.5},
    {"id": 3, "name": "Temple", "coords": [25.0372, 121.4999], "rating": 4.6},
]

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Map App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; }
        header { background: #333; color: white; padding: 1rem; }
        #map-container { height: calc(100vh - 60px); }
    </style>
</head>
<body>
    <header>
        <h1>My Map Application</h1>
    </header>
    <div id="map-container">
        {{ map_html | safe }}
    </div>
</body>
</html>
"""

@app.route("/")
def show_map():
    # TODO: Create a Folium map
    # TODO: Add markers for all places
    # TODO: Get HTML with m._repr_html_()
    # TODO: Return rendered template

    pass  # Replace with your implementation

if __name__ == "__main__":
    app.run(debug=True)
```

### Requirements

1. Map displays all places with markers
2. Markers have popups with name and rating
3. Page has a header with title
4. Map fills the rest of the page

### Testing

```bash
python exercise7.py
# Visit http://localhost:5000 in your browser
```

---

## Exercise 8: Complete Map Application (30 minutes)

### Objective
Build a complete map application with filtering and routes.

### Task

Create a Flask app that:
1. Displays places on a map
2. Allows filtering by category
3. Shows a route between selected places

### Starter Code

See `week14_starter.py` for the complete starter code.

### Features to Implement

1. **Map Display**
   - Show all places with category-specific icons
   - Center map on filtered places

2. **Category Filter**
   - Dropdown to select category
   - Map updates to show only selected category

3. **Route Display**
   - Select start and end points
   - Draw route line between them
   - Show distance estimate

### Checklist

- [ ] Map loads with all places
- [ ] Markers have correct icons by category
- [ ] Category filter works
- [ ] Route draws between selected points
- [ ] Start/end markers are different colors
- [ ] Page is styled nicely

---

## Bonus Challenges

### Bonus 1: Marker Clustering

When you have many markers, use clustering:

```python
from folium.plugins import MarkerCluster

m = folium.Map(location=[25.05, 121.55], zoom_start=11)
marker_cluster = MarkerCluster().add_to(m)

for place in many_places:
    folium.Marker(place["coords"]).add_to(marker_cluster)
```

### Bonus 2: Heatmap

Show density of places with a heatmap:

```python
from folium.plugins import HeatMap

heat_data = [[p["coords"][0], p["coords"][1]] for p in places]
HeatMap(heat_data).add_to(m)
```

### Bonus 3: Search Box

Add a search box to find places on the map:

```python
from folium.plugins import Search

# Create a GeoJson layer with your places
# Add Search plugin pointing to that layer
```

---

## Testing Your Maps

### Manual Testing Checklist

1. **Basic Map**
   - [ ] Map loads correctly
   - [ ] Can zoom in/out
   - [ ] Can pan around
   - [ ] Tiles load properly

2. **Markers**
   - [ ] All markers appear
   - [ ] Tooltips show on hover
   - [ ] Popups show on click
   - [ ] Icons display correctly

3. **Routes**
   - [ ] Route line is visible
   - [ ] Start marker is green
   - [ ] End marker is red
   - [ ] Route follows waypoints

4. **Layer Control**
   - [ ] Control panel appears
   - [ ] Can toggle layers on/off
   - [ ] Correct markers in each layer

5. **Flask Integration**
   - [ ] Page loads without errors
   - [ ] Map is embedded properly
   - [ ] Filters work correctly

---

## Summary

In this lab, you learned:

1. **Creating Maps** - `folium.Map(location, zoom_start)`
2. **Adding Markers** - `folium.Marker(location, popup, icon)`
3. **Custom Icons** - `folium.Icon(color, icon, prefix)`
4. **Drawing Routes** - `folium.PolyLine(locations, color)`
5. **Shapes** - `folium.Circle`, `folium.CircleMarker`
6. **Layer Control** - `folium.FeatureGroup`, `folium.LayerControl`
7. **Flask Integration** - `m._repr_html()`, `{{ map | safe }}`

### Quick Reference

```python
import folium

# Create map
m = folium.Map(location=[lat, lon], zoom_start=14)

# Add marker
folium.Marker(
    location=[lat, lon],
    popup="Info here",
    tooltip="Hover text",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

# Draw route
folium.PolyLine(
    locations=[[lat1, lon1], [lat2, lon2]],
    color="blue",
    weight=5
).add_to(m)

# Save or get HTML
m.save("map.html")
html = m._repr_html_()
```

### Next Steps

Congratulations on completing the map visualization module! You now have all the pieces to build the complete Smart City Navigator:

- Week 8: OSRM API for routing
- Week 12: Place class for data
- Week 13: Flask web server
- Week 14: Folium maps

Try combining them all into a complete application!
