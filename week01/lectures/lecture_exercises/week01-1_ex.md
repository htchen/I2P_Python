# Week 1-1 Lab: Variables & The Coordinate System

## Lab Overview

In this lab, you will practice:
- Creating and using variables
- Working with integers and floats
- Creating and accessing tuples
- Storing geographic coordinates

---

## Exercise 1: Variable Basics (10 minutes)

### Task 1.1: Create Variables

Create variables to store information about your favorite city:

```python
# TODO: Create the following variables:
# - city_name (string): The name of the city
# - population (integer): The population of the city
# - area_km2 (float): The area in square kilometers
# - founded_year (integer): The year the city was founded

# Your code here:
city_name = ___
population = ___
area_km2 = ___
founded_year = ___

# Print all variables
print(f"City: {city_name}")
print(f"Population: {population}")
print(f"Area: {area_km2} km²")
print(f"Founded: {founded_year}")
```

### Task 1.2: Calculate Population Density

Using the variables from Task 1.1, calculate the population density:

```python
# TODO: Calculate population density (people per km²)
# Formula: density = population / area

population_density = ___

print(f"Population density: {population_density:.2f} people/km²")
```

### Task 1.3: Variable Types

Check and print the type of each variable:

```python
# TODO: Use the type() function to check each variable's type
print(f"city_name is type: {type(city_name)}")
print(f"population is type: ___")
print(f"area_km2 is type: ___")
print(f"founded_year is type: ___")
print(f"population_density is type: ___")
```

**Question:** Why is `population_density` a different type than `population`?

---

## Exercise 2: Working with Floats (10 minutes)

### Task 2.1: Coordinate Precision

Explore how float precision affects coordinates:

```python
# These are coordinates for Taipei 101
lat = 25.0329833
lon = 121.5654268

# TODO: Print the coordinates with different precision levels
# Use f-strings with format specifiers: {value:.Nf} where N is decimal places

print(f"Full precision: ({lat}, {lon})")
print(f"4 decimal places: ({lat:.4f}, {lon:.___f})")  # Fill in the blank
print(f"2 decimal places: ({___:.2f}, {___:.2f})")   # Fill in the blanks
print(f"0 decimal places: ({___:.0f}, {___:.0f})")   # Fill in the blanks
```

### Task 2.2: Precision and Accuracy

Different decimal places represent different levels of accuracy:

| Decimal Places | Accuracy | Example Use |
|----------------|----------|-------------|
| 0 | ~111 km | Country level |
| 1 | ~11 km | City level |
| 2 | ~1.1 km | Neighborhood |
| 3 | ~110 m | Street level |
| 4 | ~11 m | Building level |
| 5 | ~1.1 m | Tree level |
| 6 | ~0.11 m | Human level |

```python
# TODO: For a restaurant finder app, how many decimal places do you need?
# Explain your answer in a comment.

recommended_precision = ___  # Fill in a number

# Your explanation:
# ___
```

---

## Exercise 3: Tuples for Coordinates (15 minutes)

### Task 3.1: Create Coordinate Tuples

Create tuples for the following locations (search online for coordinates):

```python
# TODO: Fill in the coordinates as (latitude, longitude) tuples
# Use Google Maps or OpenStreetMap to find the coordinates

# Taiwan locations
taipei_101 = (25.0330, 121.5654)  # Example - given
ntu_main_library = (___, ___)     # National Taiwan University Main Library
taipei_main_station = (___, ___)   # Taipei Main Station
shilin_night_market = (___, ___)   # Shilin Night Market

# International landmarks (for comparison)
eiffel_tower = (___, ___)          # Paris, France
statue_of_liberty = (___, ___)     # New York, USA

# Print all locations
print(f"Taipei 101: {taipei_101}")
print(f"NTU Main Library: {ntu_main_library}")
print(f"Taipei Main Station: {taipei_main_station}")
print(f"Shilin Night Market: {shilin_night_market}")
print(f"Eiffel Tower: {eiffel_tower}")
print(f"Statue of Liberty: {statue_of_liberty}")
```

### Task 3.2: Accessing Tuple Elements

Practice accessing elements from coordinate tuples:

```python
taipei_101 = (25.0330, 121.5654)

# TODO: Extract latitude and longitude separately
latitude = taipei_101[___]   # Fill in the index
longitude = taipei_101[___]  # Fill in the index

print(f"Latitude: {latitude}")
print(f"Longitude: {longitude}")

# TODO: Use tuple unpacking
lat, lon = ___  # Unpack taipei_101

print(f"Unpacked - Lat: {lat}, Lon: {lon}")
```

### Task 3.3: Tuple Immutability

Understand why tuples are immutable:

```python
taipei_101 = (25.0330, 121.5654)

# TODO: Try to modify the tuple (this will cause an error!)
# Uncomment the line below and run the code to see the error
# taipei_101[0] = 26.0

# Question: What error message do you get?
# Answer: ___

# TODO: If you need to "change" a coordinate, create a new tuple
# Create a new tuple with latitude increased by 1 degree
new_location = (___, taipei_101[1])  # Fill in the blank

print(f"Original: {taipei_101}")
print(f"New location: {new_location}")
```

---

## Exercise 4: Storing Multiple Locations (15 minutes)

### Task 4.1: List of Coordinate Tuples

Create a list containing multiple coordinate tuples:

```python
# TODO: Create a list of 5 locations you'd like to visit in Taipei
# Each location should be a tuple: (latitude, longitude)

my_taipei_tour = [
    (25.0330, 121.5654),  # Stop 1: Taipei 101
    (___, ___),           # Stop 2: Your choice
    (___, ___),           # Stop 3: Your choice
    (___, ___),           # Stop 4: Your choice
    (___, ___),           # Stop 5: Your choice
]

# Print all stops
for i, location in enumerate(my_taipei_tour, 1):
    print(f"Stop {i}: {location}")
```

### Task 4.2: Named Locations with Tuples

Create a more descriptive data structure:

```python
# TODO: Create tuples that include the name with coordinates
# Format: (name, latitude, longitude)

locations = [
    ("Taipei 101", 25.0330, 121.5654),
    ("___", ___, ___),  # Add your own
    ("___", ___, ___),  # Add your own
]

# Print with names
for name, lat, lon in locations:
    print(f"{name}: ({lat}, {lon})")
```

### Task 4.3: Calculate Bounding Box

Find the bounding box (min/max coordinates) of your tour:

```python
my_taipei_tour = [
    (25.0330, 121.5654),
    (25.0478, 121.5170),
    (25.0174, 121.5405),
    (25.0878, 121.5241),
    (25.0329, 121.5598),
]

# TODO: Find the min and max latitude and longitude
# Hint: Use list comprehension to extract all latitudes, then use min()/max()

latitudes = [coord[0] for coord in my_taipei_tour]
longitudes = [___]  # Extract all longitudes

min_lat = min(latitudes)
max_lat = ___(latitudes)
min_lon = ___(longitudes)
max_lon = ___(longitudes)

print(f"Bounding Box:")
print(f"  Latitude:  {min_lat} to {max_lat}")
print(f"  Longitude: {min_lon} to {max_lon}")
```

---

## Exercise 5: Challenge - Location Formatter (10 minutes)

### Task 5.1: Format Coordinates

Create a script that formats coordinates in different styles:

```python
taipei_101 = (25.0330, 121.5654)

# TODO: Print the location in these formats:

# Format 1: Decimal degrees
# Example: 25.0330°N, 121.5654°E
lat, lon = taipei_101
ns = "N" if lat >= 0 else "S"
ew = "E" if lon >= 0 else "W"
print(f"Decimal: {abs(lat)}°{ns}, {abs(lon)}°{ew}")

# Format 2: Degrees and decimal minutes
# Example: 25°1.98'N, 121°33.92'E
# Hint: minutes = (decimal_degrees - degrees) * 60
lat_deg = int(lat)
lat_min = (lat - lat_deg) * 60
lon_deg = int(lon)
lon_min = ___  # Calculate longitude minutes

print(f"DM: {lat_deg}°{lat_min:.2f}'{ns}, {lon_deg}°{lon_min:.2f}'{ew}")

# Format 3: URL for Google Maps
# Example: https://www.google.com/maps?q=25.0330,121.5654
print(f"Google Maps: https://www.google.com/maps?q={lat},{lon}")
```

### Task 5.2: Coordinate Validator

Write code to check if coordinates are valid:

```python
def is_valid_coordinate(coord):
    """
    Check if a coordinate tuple is valid.

    Valid coordinates:
    - Latitude: -90 to 90
    - Longitude: -180 to 180
    """
    lat, lon = coord

    # TODO: Complete the validation logic
    lat_valid = ___ <= lat <= ___
    lon_valid = ___ <= lon <= ___

    return lat_valid and lon_valid

# Test cases
test_coords = [
    (25.0330, 121.5654),   # Valid (Taipei)
    (91.0, 0.0),           # Invalid (latitude > 90)
    (0.0, 181.0),          # Invalid (longitude > 180)
    (-33.8568, 151.2153),  # Valid (Sydney)
    (0.0, 0.0),            # Valid (Gulf of Guinea)
]

for coord in test_coords:
    result = "✓ Valid" if is_valid_coordinate(coord) else "✗ Invalid"
    print(f"{coord}: {result}")
```

---

## Submission

Save your completed lab as `week01-1_lab_solution.py` and ensure all exercises run without errors.

### Checklist

- [ ] Exercise 1: All variables created and printed correctly
- [ ] Exercise 2: Float precision explored
- [ ] Exercise 3: Tuples created and accessed correctly
- [ ] Exercise 4: Multiple locations stored and bounding box calculated
- [ ] Exercise 5: Coordinate formatter working

---

## Bonus Challenge

Create a function `distance_simple(coord1, coord2)` that calculates the straight-line distance between two points using the Pythagorean theorem. Note: This will be inaccurate for large distances, but it's a good warmup for next class!

```python
import math

def distance_simple(coord1, coord2):
    """
    Calculate approximate distance using Pythagorean theorem.
    WARNING: Only accurate for small distances!
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # TODO: Implement using sqrt((lat2-lat1)² + (lon2-lon1)²)
    # Then multiply by 111 to convert degrees to km (approximate)

    pass  # Replace with your implementation
```
