#!/usr/bin/env python3
"""
Week 14: Interactive Maps with Folium
Interactive Examples

This file demonstrates Folium map concepts through runnable examples.
Each demo generates an HTML map file that opens in your browser.

Usage:
    python examples.py              # Run demo selection menu
    python examples.py --demo N     # Run specific demo (1-8)
    python examples.py --all        # Generate all maps
"""

import sys
import os
import webbrowser
import tempfile

# Check for folium
try:
    import folium
    from folium import plugins
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False
    print("Warning: folium not installed. Install with: pip install folium")


# =============================================================================
# Demo 1: Basic Map
# =============================================================================

def demo_basic_map():
    """Create a basic map centered on Taipei."""
    print("Creating basic map...")

    # Create map centered on Taipei 101
    m = folium.Map(
        location=[25.0330, 121.5654],
        zoom_start=14
    )

    # Save and open
    output_file = "demo1_basic_map.html"
    m.save(output_file)
    print(f"Saved: {output_file}")
    return output_file


# =============================================================================
# Demo 2: Map Tiles
# =============================================================================

def demo_map_tiles():
    """Demonstrate different map tile styles."""
    print("Creating maps with different tiles...")

    center = [25.0330, 121.5654]

    # Create maps with different tiles
    tiles_options = [
        ("OpenStreetMap", "OpenStreetMap"),
        ("CartoDB positron", "CartoDB positron"),
        ("CartoDB dark_matter", "CartoDB dark_matter"),
    ]

    maps_html = []

    for name, tiles in tiles_options:
        m = folium.Map(location=center, zoom_start=14, tiles=tiles)
        folium.Marker(center, popup=f"Taipei 101\nTiles: {name}").add_to(m)
        maps_html.append((name, m._repr_html_()))

    # Create combined HTML
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Map Tiles Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
            h1 { color: #333; }
            .map-container { display: flex; flex-wrap: wrap; gap: 20px; }
            .map-box { flex: 1; min-width: 400px; }
            .map-box h3 { margin-bottom: 10px; }
            .map-frame { height: 300px; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <h1>Map Tiles Comparison</h1>
        <div class="map-container">
    """

    for name, map_html in maps_html:
        html += f"""
            <div class="map-box">
                <h3>{name}</h3>
                <div class="map-frame">{map_html}</div>
            </div>
        """

    html += """
        </div>
    </body>
    </html>
    """

    output_file = "demo2_map_tiles.html"
    with open(output_file, "w") as f:
        f.write(html)
    print(f"Saved: {output_file}")
    return output_file


# =============================================================================
# Demo 3: Markers with Popups
# =============================================================================

def demo_markers():
    """Demonstrate markers with popups and tooltips."""
    print("Creating map with markers...")

    m = folium.Map(location=[25.0500, 121.5400], zoom_start=12)

    # Sample places
    places = [
        {"name": "Taipei 101", "coords": [25.0330, 121.5654], "rating": 4.7,
         "description": "Iconic skyscraper, 508m tall"},
        {"name": "Din Tai Fung", "coords": [25.0339, 121.5645], "rating": 4.9,
         "description": "Famous for xiaolongbao"},
        {"name": "Shilin Night Market", "coords": [25.0878, 121.5241], "rating": 4.5,
         "description": "Largest night market in Taipei"},
        {"name": "National Palace Museum", "coords": [25.1024, 121.5485], "rating": 4.8,
         "description": "World-class collection of Chinese art"},
    ]

    for place in places:
        # Create rich HTML popup
        popup_html = f"""
        <div style="min-width: 200px;">
            <h4 style="margin: 0 0 8px 0; color: #333;">{place['name']}</h4>
            <p style="margin: 0 0 5px 0;">
                <b>Rating:</b> {'⭐' * int(place['rating'])} {place['rating']}
            </p>
            <p style="margin: 0; color: #666; font-size: 0.9em;">
                {place['description']}
            </p>
        </div>
        """

        folium.Marker(
            location=place['coords'],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Click for info about {place['name']}"
        ).add_to(m)

    output_file = "demo3_markers.html"
    m.save(output_file)
    print(f"Saved: {output_file}")
    return output_file


# =============================================================================
# Demo 4: Custom Icons
# =============================================================================

def demo_custom_icons():
    """Demonstrate custom marker icons."""
    print("Creating map with custom icons...")

    m = folium.Map(location=[25.0400, 121.5400], zoom_start=13)

    # Places with categories
    places = [
        {"name": "Pizza Restaurant", "coords": [25.033, 121.565], "category": "restaurant"},
        {"name": "Coffee Shop", "coords": [25.040, 121.560], "category": "cafe"},
        {"name": "City Park", "coords": [25.045, 121.555], "category": "park"},
        {"name": "History Museum", "coords": [25.050, 121.545], "category": "museum"},
        {"name": "Train Station", "coords": [25.048, 121.517], "category": "transport"},
        {"name": "Shopping Mall", "coords": [25.042, 121.508], "category": "shopping"},
    ]

    # Icon styles by category
    styles = {
        "restaurant": {"color": "red", "icon": "cutlery"},
        "cafe": {"color": "orange", "icon": "coffee"},
        "park": {"color": "green", "icon": "tree"},
        "museum": {"color": "blue", "icon": "university"},
        "transport": {"color": "gray", "icon": "train"},
        "shopping": {"color": "pink", "icon": "shopping-cart"},
    }

    for place in places:
        style = styles.get(place['category'], {"color": "gray", "icon": "info"})

        folium.Marker(
            location=place['coords'],
            popup=f"<b>{place['name']}</b><br>Category: {place['category'].title()}",
            tooltip=place['name'],
            icon=folium.Icon(color=style['color'], icon=style['icon'], prefix='fa')
        ).add_to(m)

    # Add legend
    legend_html = """
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000;
                background: white; padding: 15px; border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);">
        <h4 style="margin: 0 0 10px 0;">Legend</h4>
        <p style="margin: 3px 0;"><span style="color: red;">●</span> Restaurant</p>
        <p style="margin: 3px 0;"><span style="color: orange;">●</span> Cafe</p>
        <p style="margin: 3px 0;"><span style="color: green;">●</span> Park</p>
        <p style="margin: 3px 0;"><span style="color: blue;">●</span> Museum</p>
        <p style="margin: 3px 0;"><span style="color: gray;">●</span> Transport</p>
        <p style="margin: 3px 0;"><span style="color: pink;">●</span> Shopping</p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    output_file = "demo4_custom_icons.html"
    m.save(output_file)
    print(f"Saved: {output_file}")
    return output_file


# =============================================================================
# Demo 5: Drawing Routes
# =============================================================================

def demo_routes():
    """Demonstrate drawing routes on a map."""
    print("Creating map with routes...")

    m = folium.Map(location=[25.0400, 121.5350], zoom_start=13)

    # Route from Taipei 101 to Main Station
    route_coords = [
        [25.0330, 121.5654],  # Taipei 101
        [25.0350, 121.5580],  # Waypoint
        [25.0380, 121.5500],  # Waypoint
        [25.0420, 121.5380],  # Waypoint
        [25.0450, 121.5250],  # Waypoint
        [25.0478, 121.5170],  # Main Station
    ]

    # Draw main route
    folium.PolyLine(
        locations=route_coords,
        color="blue",
        weight=5,
        opacity=0.8,
        popup="Route: 5.2 km, ~15 min by car"
    ).add_to(m)

    # Start marker
    folium.Marker(
        location=route_coords[0],
        popup="<b>Start</b><br>Taipei 101",
        icon=folium.Icon(color="green", icon="play", prefix="fa")
    ).add_to(m)

    # End marker
    folium.Marker(
        location=route_coords[-1],
        popup="<b>End</b><br>Taipei Main Station",
        icon=folium.Icon(color="red", icon="flag", prefix="fa")
    ).add_to(m)

    # Add waypoint markers
    for i, coord in enumerate(route_coords[1:-1], 1):
        folium.CircleMarker(
            location=coord,
            radius=5,
            color="blue",
            fill=True,
            popup=f"Waypoint {i}"
        ).add_to(m)

    output_file = "demo5_routes.html"
    m.save(output_file)
    print(f"Saved: {output_file}")
    return output_file


# =============================================================================
# Demo 6: Shapes (Circles, Polygons)
# =============================================================================

def demo_shapes():
    """Demonstrate drawing shapes on a map."""
    print("Creating map with shapes...")

    m = folium.Map(location=[25.0400, 121.5500], zoom_start=13)

    # Circle - 1km radius around Taipei 101
    folium.Circle(
        location=[25.0330, 121.5654],
        radius=1000,  # meters
        color="blue",
        fill=True,
        fill_color="lightblue",
        fill_opacity=0.4,
        popup="1km radius from Taipei 101"
    ).add_to(m)

    # Circle markers (fixed pixel size)
    ratings = [
        {"name": "Place A", "coords": [25.045, 121.540], "rating": 4.8},
        {"name": "Place B", "coords": [25.050, 121.555], "rating": 4.2},
        {"name": "Place C", "coords": [25.038, 121.530], "rating": 3.5},
    ]

    for place in ratings:
        radius = place['rating'] * 4  # Size based on rating
        color = "green" if place['rating'] >= 4.5 else "orange" if place['rating'] >= 4.0 else "red"

        folium.CircleMarker(
            location=place['coords'],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=f"{place['name']}: {place['rating']}⭐"
        ).add_to(m)

    # Polygon - district boundary
    district_coords = [
        [25.030, 121.560],
        [25.030, 121.575],
        [25.045, 121.575],
        [25.045, 121.560],
    ]

    folium.Polygon(
        locations=district_coords,
        color="purple",
        weight=2,
        fill=True,
        fill_color="purple",
        fill_opacity=0.2,
        popup="Xinyi District"
    ).add_to(m)

    output_file = "demo6_shapes.html"
    m.save(output_file)
    print(f"Saved: {output_file}")
    return output_file


# =============================================================================
# Demo 7: Layer Control
# =============================================================================

def demo_layer_control():
    """Demonstrate feature groups and layer control."""
    print("Creating map with layer control...")

    m = folium.Map(location=[25.0450, 121.5400], zoom_start=12)

    # Create feature groups
    restaurants = folium.FeatureGroup(name="Restaurants")
    parks = folium.FeatureGroup(name="Parks")
    museums = folium.FeatureGroup(name="Museums")
    routes = folium.FeatureGroup(name="Routes")

    # Add restaurants
    restaurant_places = [
        {"name": "Din Tai Fung", "coords": [25.0339, 121.5645]},
        {"name": "Addiction Aquatic", "coords": [25.0600, 121.5500]},
        {"name": "RAW", "coords": [25.0580, 121.5620]},
    ]
    for place in restaurant_places:
        folium.Marker(
            place['coords'],
            popup=place['name'],
            icon=folium.Icon(color="red", icon="cutlery", prefix="fa")
        ).add_to(restaurants)

    # Add parks
    park_places = [
        {"name": "Daan Forest Park", "coords": [25.0295, 121.5357]},
        {"name": "Taipei Botanical Garden", "coords": [25.0316, 121.5089]},
    ]
    for place in park_places:
        folium.Marker(
            place['coords'],
            popup=place['name'],
            icon=folium.Icon(color="green", icon="tree", prefix="fa")
        ).add_to(parks)

    # Add museums
    museum_places = [
        {"name": "National Palace Museum", "coords": [25.1024, 121.5485]},
        {"name": "Taipei Fine Arts Museum", "coords": [25.0725, 121.5247]},
    ]
    for place in museum_places:
        folium.Marker(
            place['coords'],
            popup=place['name'],
            icon=folium.Icon(color="blue", icon="university", prefix="fa")
        ).add_to(museums)

    # Add a sample route
    route_coords = [
        [25.0330, 121.5654],
        [25.0450, 121.5400],
        [25.0600, 121.5250],
    ]
    folium.PolyLine(
        route_coords,
        color="purple",
        weight=4,
        popup="Sample Route"
    ).add_to(routes)

    # Add all groups to map
    restaurants.add_to(m)
    parks.add_to(m)
    museums.add_to(m)
    routes.add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    output_file = "demo7_layer_control.html"
    m.save(output_file)
    print(f"Saved: {output_file}")
    return output_file


# =============================================================================
# Demo 8: Complete Smart City Map
# =============================================================================

def demo_complete_map():
    """Create a complete Smart City Navigator map."""
    print("Creating complete Smart City Navigator map...")

    # All places data
    places = [
        {"id": 1, "name": "Taipei 101", "coords": [25.0330, 121.5654],
         "rating": 4.7, "category": "landmark", "description": "Iconic 508m skyscraper"},
        {"id": 2, "name": "Din Tai Fung", "coords": [25.0339, 121.5645],
         "rating": 4.9, "category": "restaurant", "description": "Famous for xiaolongbao"},
        {"id": 3, "name": "Shilin Night Market", "coords": [25.0878, 121.5241],
         "rating": 4.5, "category": "market", "description": "Largest night market"},
        {"id": 4, "name": "National Palace Museum", "coords": [25.1024, 121.5485],
         "rating": 4.8, "category": "museum", "description": "World-class Chinese art"},
        {"id": 5, "name": "Elephant Mountain", "coords": [25.0275, 121.5701],
         "rating": 4.6, "category": "nature", "description": "Hiking with city views"},
        {"id": 6, "name": "Longshan Temple", "coords": [25.0372, 121.4999],
         "rating": 4.6, "category": "temple", "description": "Historic Buddhist temple"},
        {"id": 7, "name": "Taipei Main Station", "coords": [25.0478, 121.5170],
         "rating": 4.2, "category": "transport", "description": "Central transportation hub"},
        {"id": 8, "name": "Ximending", "coords": [25.0423, 121.5081],
         "rating": 4.4, "category": "shopping", "description": "Youth fashion district"},
    ]

    # Category styles
    styles = {
        "landmark": {"color": "purple", "icon": "building"},
        "restaurant": {"color": "red", "icon": "cutlery"},
        "market": {"color": "orange", "icon": "shopping-cart"},
        "museum": {"color": "blue", "icon": "university"},
        "nature": {"color": "green", "icon": "tree"},
        "temple": {"color": "darkred", "icon": "institution"},
        "transport": {"color": "gray", "icon": "train"},
        "shopping": {"color": "pink", "icon": "shopping-bag"},
    }

    # Calculate center
    avg_lat = sum(p['coords'][0] for p in places) / len(places)
    avg_lon = sum(p['coords'][1] for p in places) / len(places)

    # Create map with nice tiles
    m = folium.Map(
        location=[avg_lat, avg_lon],
        zoom_start=12,
        tiles="CartoDB positron"
    )

    # Create feature groups by category
    groups = {}
    for category in styles.keys():
        groups[category] = folium.FeatureGroup(name=category.title())

    # Add markers
    for place in places:
        style = styles.get(place['category'], {"color": "gray", "icon": "info"})

        popup_html = f"""
        <div style="min-width: 180px; font-family: Arial, sans-serif;">
            <h4 style="margin: 0 0 8px 0; color: #333; border-bottom: 1px solid #eee; padding-bottom: 5px;">
                {place['name']}
            </h4>
            <p style="margin: 0 0 5px 0;">
                {'⭐' * int(place['rating'])} <b>{place['rating']}</b>
            </p>
            <p style="margin: 0 0 5px 0; color: #666;">
                <i class="fa fa-{style['icon']}"></i> {place['category'].title()}
            </p>
            <p style="margin: 0; font-size: 0.9em; color: #888;">
                {place['description']}
            </p>
        </div>
        """

        marker = folium.Marker(
            location=place['coords'],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{place['name']} ({place['rating']}⭐)",
            icon=folium.Icon(color=style['color'], icon=style['icon'], prefix='fa')
        )
        marker.add_to(groups[place['category']])

    # Add sample route (Taipei 101 to Main Station)
    route_group = folium.FeatureGroup(name="Sample Route")
    route_coords = [
        [25.0330, 121.5654],
        [25.0380, 121.5500],
        [25.0420, 121.5350],
        [25.0478, 121.5170],
    ]
    folium.PolyLine(
        route_coords,
        color="#667eea",
        weight=5,
        opacity=0.8,
        popup="Taipei 101 → Main Station<br>~5.2 km, 15 min"
    ).add_to(route_group)

    # Add all groups to map
    for group in groups.values():
        group.add_to(m)
    route_group.add_to(m)

    # Add layer control
    folium.LayerControl(collapsed=False).add_to(m)

    # Add title
    title_html = """
    <div style="position: fixed; top: 10px; left: 60px; z-index: 1000;">
        <h2 style="background: white; padding: 10px 20px; border-radius: 8px;
                   box-shadow: 0 2px 10px rgba(0,0,0,0.2); margin: 0;
                   font-family: Arial, sans-serif; color: #667eea;">
            🗺️ Smart City Navigator
        </h2>
    </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    output_file = "demo8_complete_map.html"
    m.save(output_file)
    print(f"Saved: {output_file}")
    return output_file


# =============================================================================
# Demo Runner
# =============================================================================

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def run_demo(demo_num, open_browser=True):
    """Run a specific demo."""
    if not FOLIUM_AVAILABLE:
        print("Error: folium is not installed.")
        print("Install with: pip install folium")
        return None

    demos = {
        1: ("Basic Map", demo_basic_map),
        2: ("Map Tiles", demo_map_tiles),
        3: ("Markers with Popups", demo_markers),
        4: ("Custom Icons", demo_custom_icons),
        5: ("Drawing Routes", demo_routes),
        6: ("Shapes", demo_shapes),
        7: ("Layer Control", demo_layer_control),
        8: ("Complete Smart City Map", demo_complete_map),
    }

    if demo_num not in demos:
        print(f"Invalid demo number: {demo_num}")
        return None

    title, func = demos[demo_num]
    print_header(f"Demo {demo_num}: {title}")

    output_file = func()

    if output_file and open_browser:
        abs_path = os.path.abspath(output_file)
        print(f"Opening in browser: {abs_path}")
        webbrowser.open(f"file://{abs_path}")

    return output_file


def run_all_demos():
    """Run all demos and generate all map files."""
    if not FOLIUM_AVAILABLE:
        print("Error: folium is not installed.")
        print("Install with: pip install folium")
        return

    print_header("Generating All Demo Maps")

    for i in range(1, 9):
        run_demo(i, open_browser=False)

    print("\n" + "=" * 60)
    print("All maps generated!")
    print("=" * 60)
    print("\nGenerated files:")
    for i in range(1, 9):
        demos = {
            1: "demo1_basic_map.html",
            2: "demo2_map_tiles.html",
            3: "demo3_markers.html",
            4: "demo4_custom_icons.html",
            5: "demo5_routes.html",
            6: "demo6_shapes.html",
            7: "demo7_layer_control.html",
            8: "demo8_complete_map.html",
        }
        print(f"  {i}. {demos[i]}")


def show_menu():
    """Show interactive menu."""
    print_header("Week 14: Interactive Maps with Folium")

    if not FOLIUM_AVAILABLE:
        print("\n⚠️  WARNING: folium is not installed!")
        print("Install with: pip install folium")
        print()

    print("""
Available Demos:
  1. Basic Map          - Create a simple map
  2. Map Tiles          - Compare different tile styles
  3. Markers            - Add markers with popups
  4. Custom Icons       - Category-based marker icons
  5. Routes             - Draw routes between locations
  6. Shapes             - Circles, polygons, and more
  7. Layer Control      - Toggle map layers
  8. Complete Map       - Full Smart City Navigator

Commands:
  - Enter a number (1-8) to run that demo
  - Enter 'all' to generate all demo maps
  - Enter 'q' to quit

Each demo generates an HTML file and opens it in your browser.
""")

    while True:
        try:
            choice = input("\nSelect demo (1-8, 'all', or 'q'): ").strip().lower()

            if choice == 'q':
                print("Goodbye!")
                break
            elif choice == 'all':
                run_all_demos()
            elif choice.isdigit():
                num = int(choice)
                if 1 <= num <= 8:
                    run_demo(num)
                else:
                    print("Please enter a number between 1 and 8")
            else:
                print("Invalid input. Try again.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
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
            run_all_demos()
        elif sys.argv[1] == "--help":
            print(__doc__)
        else:
            print("Unknown argument. Use --help for usage.")
    else:
        show_menu()


if __name__ == "__main__":
    main()
