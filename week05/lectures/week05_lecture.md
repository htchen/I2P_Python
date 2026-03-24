# Week 5: The Nominatim API (Geocoding)

## Lecture Overview (3 Hours)

**Phase 2: The API & The Cloud** — "Fetching the World"

### Learning Objectives
By the end of this lecture, students will be able to:
1. Understand geocoding and reverse geocoding concepts
2. Parse complex nested JSON responses from real APIs
3. Use Python's error handling system effectively
4. Build a complete CLI geocoding tool
5. Handle edge cases and unexpected data gracefully
6. Implement robust data extraction patterns

### Prerequisites
- Week 4: HTTP Requests & API Keys
- Understanding of the `requests` library
- Basic JSON parsing knowledge

### Why This Matters

In real-world programming, you rarely work with clean, predictable data. APIs return messy, inconsistent responses. Networks fail. Users enter unexpected inputs. This week, we'll learn to write **defensive code** that handles these challenges gracefully.

---

# Hour 1: Deep Dive into Nominatim

## 1.1 What is Geocoding?

**Geocoding** is the process of converting human-readable addresses or place names into geographic coordinates (latitude and longitude).

```
┌─────────────────────────┐     Geocoding       ┌─────────────────────┐
│    "Taipei 101"         │ ──────────────────> │ (25.0339, 121.5645) │
│    (Place Name)         │                     │   (Coordinates)     │
└─────────────────────────┘                     └─────────────────────┘

┌─────────────────────────┐  Reverse Geocoding  ┌─────────────────────┐
│  (25.0339, 121.5645)    │ ──────────────────> │ "Taipei 101, Xinyi  │
│    (Coordinates)        │                     │  Road, Taipei..."   │
└─────────────────────────┘                     └─────────────────────┘
```

### Think of it Like a Dictionary

- **Geocoding** is like looking up a word to find its definition
  - Input: "Taipei 101" (the word)
  - Output: (25.0339, 121.5645) (the definition)

- **Reverse Geocoding** is like looking up a definition to find the word
  - Input: (25.0339, 121.5645) (the definition)
  - Output: "Taipei 101, Xinyi Road..." (the word)

### Why is Geocoding Important?

Geocoding is **everywhere** in modern applications:

1. **Maps & Navigation**
   - When you type "Starbucks near me" in Google Maps
   - The app geocodes "Starbucks" to find coordinates of nearby locations

2. **Food Delivery Apps**
   - You enter "123 Main Street"
   - The app converts it to coordinates to show you on a map and calculate delivery routes

3. **Data Analysis & Visualization**
   - A company has 10,000 customer addresses
   - Geocoding converts them to coordinates for plotting on a heat map

4. **Location-Based Services**
   - "Find hospitals within 5km"
   - First geocode your location, then search for hospitals near those coordinates

5. **Logistics & Shipping**
   - Delivery companies geocode addresses to optimize routes
   - Calculate distances between warehouses and destinations

### The Geocoding Process (Behind the Scenes)

When you geocode "Taipei 101", the service:

1. **Parses** your query to understand what you're looking for
2. **Searches** a massive database of places and addresses
3. **Ranks** results by relevance (importance score)
4. **Returns** the best matches with coordinates

```
User Query: "Taipei 101"
    │
    ▼
┌─────────────────────┐
│  Query Parser       │  → Understands: building name, Taiwan
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Database Search    │  → Finds: 3 possible matches
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Ranking Algorithm  │  → Best match: Taipei 101 Tower (importance: 0.68)
└─────────────────────┘
    │
    ▼
Result: lat=25.0339, lon=121.5645
```

---

## 1.2 Nominatim: OpenStreetMap's Geocoder

**Nominatim** (Latin for "by name") is the search engine for OpenStreetMap data.

### What is OpenStreetMap?

OpenStreetMap (OSM) is like **Wikipedia for maps**:
- **Community-driven**: Volunteers worldwide add and update map data
- **Free and open**: Anyone can use the data
- **Comprehensive**: Contains streets, buildings, parks, businesses, and more
- **Global coverage**: Maps the entire world

### Why Use Nominatim?

| Feature | Description | Why It Matters |
|---------|-------------|----------------|
| **Free** | No cost for reasonable usage | Perfect for learning and small projects |
| **No API Key** | Just needs proper User-Agent | Easy to get started |
| **Global Coverage** | Entire world mapped | Works for any location |
| **Open Data** | Community-contributed | Transparent, improvable |
| **Multiple Formats** | JSON, XML, HTML | Flexible for different needs |

### Nominatim vs Commercial Geocoders

| Aspect | Nominatim | Google/Mapbox |
|--------|-----------|---------------|
| **Cost** | Free | Paid (after free tier) |
| **Setup** | User-Agent only | API key required |
| **Rate Limit** | 1 req/second | Higher limits |
| **Accuracy** | Good (varies by region) | Generally better |
| **Support** | Community | Professional |

**For learning**: Nominatim is perfect—it's free, easy to use, and teaches real-world API concepts.

### Nominatim Endpoints

An **endpoint** is a specific URL path that performs a particular function:

| Endpoint | Purpose | When to Use |
|----------|---------|-------------|
| `/search` | Geocoding (name → coords) | "Where is Taipei 101?" |
| `/reverse` | Reverse geocoding (coords → name) | "What's at 25.03, 121.56?" |
| `/lookup` | Look up by OSM ID | Get details for a specific place |
| `/status` | Check server status | Is the service running? |

We'll focus on `/search` and `/reverse` in this course.

---

## 1.3 The Search Endpoint in Detail

### Basic Request Structure

Let's break down a geocoding request step by step:

```python
import requests

# Step 1: Define the API endpoint URL
url = "https://nominatim.openstreetmap.org/search"

# Step 2: Define what we're searching for (query parameters)
params = {
    "q": "Taipei 101",      # The search query
    "format": "json"        # We want JSON response
}

# Step 3: Identify ourselves (REQUIRED by Nominatim)
headers = {
    "User-Agent": "CS101-Geocoder/1.0 (cs101@university.edu)"
}

# Step 4: Make the request
response = requests.get(url, params=params, headers=headers, timeout=10)

# Step 5: Parse the JSON response
results = response.json()

# Step 6: Use the results
if results:
    place = results[0]
    print(f"Found: {place['display_name']}")
    print(f"Coordinates: ({place['lat']}, {place['lon']})")
```

### Understanding Each Step

**Step 1 - The URL**: This is the "address" of the API endpoint. Think of it like a phone number for a specific service.

**Step 2 - Query Parameters**: These tell the API what you want:
- `q` = "query" = what you're searching for
- `format` = what format you want the response in

**Step 3 - Headers**: Metadata about your request. The User-Agent identifies who you are (required by Nominatim to prevent abuse).

**Step 4 - The Request**: `requests.get()` sends your request to the server and waits for a response. The `timeout=10` means "give up after 10 seconds".

**Step 5 - Parse JSON**: Convert the response text into Python data structures (lists and dictionaries).

**Step 6 - Use Results**: Check if we got results and extract the data we need.

### All Search Parameters

Nominatim accepts many parameters to customize your search:

#### Basic Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `q` | string | Free-form search query | `"Taipei 101"` |
| `format` | string | Output format | `"json"`, `"jsonv2"`, `"xml"` |
| `limit` | int | Maximum results (1-50) | `5` |

#### Detail Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `addressdetails` | 0/1 | Include address breakdown | `1` |
| `extratags` | 0/1 | Include additional OSM tags | `1` |
| `namedetails` | 0/1 | Include all name variants | `1` |

#### Geographic Filtering

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `countrycodes` | string | Limit to countries (ISO codes) | `"tw,jp"` |
| `viewbox` | string | Bounding box preference | `"lon1,lat1,lon2,lat2"` |
| `bounded` | 0/1 | Strict viewbox limit | `1` |

### Example: Search with Multiple Parameters

```python
params = {
    "q": "coffee shop",
    "format": "json",
    "limit": 5,                    # Get up to 5 results
    "countrycodes": "tw",          # Only Taiwan
    "addressdetails": 1,           # Include address breakdown
    "viewbox": "121.5,25.0,121.6,25.1",  # Taipei area
    "bounded": 1                   # Strict - only within viewbox
}
```

**What this does**:
- Searches for "coffee shop"
- Returns up to 5 results
- Only in Taiwan
- Only within the Taipei area bounding box
- Includes detailed address information

### Structured Search (Alternative)

Instead of a free-form query (`q`), you can search by address components:

```python
# Free-form (less precise)
params = {"q": "7 Section 5 Xinyi Road Taipei Taiwan", "format": "json"}

# Structured (more precise)
params = {
    "street": "7 Section 5 Xinyi Road",
    "city": "Taipei",
    "country": "Taiwan",
    "format": "json"
}
```

**When to use structured search**:
- When you have clean, separated address components
- When you need more precise results
- When free-form search gives unexpected results

---

## 1.4 Understanding the Response Structure

When you make a search request, Nominatim returns a **list of place objects**. Let's examine the response in detail:

### Sample Response

```json
[
    {
        "place_id": 424937126,
        "licence": "Data © OpenStreetMap contributors...",
        "osm_type": "way",
        "osm_id": 1159328965,
        "lat": "25.0338352",
        "lon": "121.5644995",
        "class": "building",
        "type": "attraction",
        "place_rank": 30,
        "importance": 0.5453714025007607,
        "addresstype": "building",
        "name": "台北101",
        "display_name": "台北101, 7, 信義路五段, 西村里, 信義區, 信義商圈, 臺北市, 11049, 臺灣",
        "boundingbox": ["25.0332803", "25.0346102", "121.5638583", "121.5652356"]
    }
]
```

### Key Fields Explained

Let's understand what each field means:

#### Identification Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `place_id` | int | Unique ID in Nominatim's database | `424937126` |
| `osm_id` | int | ID in OpenStreetMap database | `1159328965` |
| `osm_type` | string | Type in OSM | `"way"` |

**Understanding `osm_type`**:
- `"node"` = A single point (e.g., a café, ATM)
- `"way"` = A line or polygon (e.g., a road, building outline)
- `"relation"` = A complex structure (e.g., a transit route, administrative boundary)

Taipei 101 is a `"way"` because it's represented as a building outline (polygon).

#### Location Fields

| Field | Type | Description | Note |
|-------|------|-------------|------|
| `lat` | **string** | Latitude | **Must convert to float!** |
| `lon` | **string** | Longitude | **Must convert to float!** |
| `boundingbox` | list | Geographic extent | [south, north, west, east] |

**Critical Warning**: `lat` and `lon` are **strings**, not numbers!

```python
# WRONG - lat is a string!
result["lat"] + 1  # TypeError: can only concatenate str to str

# CORRECT - convert to float first
float(result["lat"]) + 1  # Works: 26.0339639
```

#### Classification Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `class` | string | Broad category | `"tourism"`, `"amenity"`, `"highway"` |
| `type` | string | Specific type | `"attraction"`, `"restaurant"`, `"bus_stop"` |
| `addresstype` | string | How it fits in an address | `"tourism"`, `"road"` |

**Common class/type combinations**:
- `tourism:attraction` - Tourist attractions
- `amenity:restaurant` - Restaurants
- `amenity:cafe` - Cafes
- `highway:bus_stop` - Bus stops
- `building:yes` - Generic buildings

#### Ranking Fields

| Field | Type | Description | Range |
|-------|------|-------------|-------|
| `importance` | float | How notable/famous | 0.0 to 1.0 |
| `place_rank` | int | Granularity level | 1-30 |

**Understanding `importance`**:
- Higher = more famous/notable
- Eiffel Tower: ~0.62
- Taipei 101: ~0.55
- Local coffee shop: ~0.2

**Understanding `place_rank`**:
- Lower = larger/more important administratively
- Country: ~4
- City: ~16
- Building: ~30

#### Display Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Short name |
| `display_name` | string | Full formatted address |

```python
result["name"]         # "台北101"
result["display_name"] # "台北101, 7, 信義路五段, 西村里, 信義區, 信義商圈, 臺北市, 11049, 臺灣"
```

---

## 1.5 Mini-Exercise 1: Parse a Response

Given this response, extract the place name, coordinates, and type:

```python
response_data = [
    {
        "place_id": 123456,
        "lat": "25.0478",
        "lon": "121.5170",
        "display_name": "Taipei Main Station, Zhongzheng District, Taipei, Taiwan",
        "type": "station",
        "class": "railway",
        "importance": 0.75
    }
]

# Extract:
# 1. The display name
# 2. Coordinates as floats in a tuple
# 3. The type and class combined as "class:type"
```

**Think about**:
- What if the list is empty?
- What if `lat` or `lon` is missing?
- What type are `lat` and `lon`?

<details>
<summary>Solution</summary>

```python
response_data = [
    {
        "place_id": 123456,
        "lat": "25.0478",
        "lon": "121.5170",
        "display_name": "Taipei Main Station, Zhongzheng District, Taipei, Taiwan",
        "type": "station",
        "class": "railway",
        "importance": 0.75
    }
]

# First, check if we have any results
if response_data:
    # Get the first result
    place = response_data[0]

    # 1. Display name - simple dictionary access
    name = place["display_name"]
    print(f"Name: {name}")

    # 2. Coordinates - must convert strings to floats!
    lat = float(place["lat"])
    lon = float(place["lon"])
    coords = (lat, lon)
    print(f"Coordinates: {coords}")

    # 3. Class and type combined
    category = f"{place['class']}:{place['type']}"
    print(f"Category: {category}")
else:
    print("No results found!")

# Output:
# Name: Taipei Main Station, Zhongzheng District, Taipei, Taiwan
# Coordinates: (25.0478, 121.517)
# Category: railway:station
```

**Key points**:
1. Always check if `response_data` is not empty before accessing `[0]`
2. Convert `lat` and `lon` from strings to floats
3. Use f-strings to combine values

</details>

---

## 1.6 Address Details Response

When you add `addressdetails=1` to your request:

```python
params = {
    "q": "Taipei 101",
    "format": "json",
    "addressdetails": 1  # Include address breakdown
}
```

The response includes a nested `address` object with structured information:

```json
{
    "lat": "25.0339639",
    "lon": "121.5644722",
    "display_name": "台北101, 7, 信義路五段, 西村里, 信義區, 信義商圈, 臺北市, 11049, 臺灣",
    "address": {
        "tourism": "台北101",
        "house_number": "7",
        "road": "信義路五段",
        "neighbourhood": "西村里",
        "suburb": "信義區",
        "village": "信義商圈",
        "city": "臺北市",
        "ISO3166-2-lvl4": "TW-TPE",
        "postcode": "11049",
        "country": "臺灣",
        "country_code": "tw"
    }
}
```

### Understanding the Address Object

The `address` object contains **components** of the address, but the keys vary depending on the place type:

**For a tourist attraction (Taipei 101)**:
```json
{
    "tourism": "台北101",
    "house_number": "7",
    "road": "信義路五段",
    "neighbourhood": "西村里",
    "suburb": "信義區",
    "village": "信義商圈",
    "city": "臺北市",  // with city, villge, suburb
    "ISO3166-2-lvl4": "TW-TPE",
    "postcode": "11049",
    "country": "臺灣",
    "country_code": "tw"
}
```

**For a small village**:
```json
{
    "village": "Some Village",   // No "city" - uses "village"
    "county": "Some County",
    "country": "Taiwan"
    // No road, no suburb!
}
```

**This inconsistency is a major challenge** we'll address in Hour 2.

### Parsing Nested Address Data

Here's a function that handles the nested structure:

```python
def parse_address(result: dict) -> dict:
    """
    Extract structured address from Nominatim result.

    Args:
        result: A single Nominatim result dictionary

    Returns:
        Dictionary with standardized address fields
    """
    # Step 1: Get the address object (or empty dict if missing)
    address = result.get("address", {})

    # Step 2: Extract each component with fallbacks
    return {
        # Name could be under different keys depending on place type
        "name": result.get("name", address.get("tourism", "Unknown")),

        # Street information
        "street": address.get("road", ""),
        "number": address.get("house_number", ""),

        # Area - try multiple possible keys
        "district": address.get("suburb", address.get("district", "")),

        # City - might be "city", "town", or "village"
        "city": address.get("city", address.get("town", "")),

        # Country info
        "country": address.get("country", ""),
        "postcode": address.get("postcode", "")
    }
```

**Key technique**: Use `.get()` with fallback values to handle missing keys.

---

# ☕ 5-Minute Break

Stand up, stretch, rest your eyes!

---

# Hour 2: Parsing Complex Nested JSON & Recursion

## 2.1 The Challenge of Real-World JSON

In Week 3, we worked with clean, predictable JSON files that we created ourselves. Real API responses are much messier:

### The Problems You'll Encounter

1. **Missing Fields**: Some responses have fields, others don't
2. **Inconsistent Types**: Sometimes a field is a string, sometimes null
3. **Varying Structures**: Different results have different shapes
4. **Deeply Nested Data**: Data buried many levels deep
5. **Empty Responses**: Sometimes the API returns nothing

### Example: Inconsistent Responses

Here are two real Nominatim responses showing how different they can be:

```python
# Response for "Taipei 101" - a major landmark
{
    "name": "台北101",
    "display_name": "台北101, 7, 信義路五段, 西村里, 信義區, 信義商圈, 臺北市, 11049, 臺灣'",
    "address": {
        "tourism": "台北101",
        "house_number": "7",
        "road": "信義路五段",
        "neighbourhood": "西村里",
        "suburb": "信義區",
        "village": "信義商圈",
        "city": "臺北市",
        "ISO3166-2-lvl4": "TW-TPE",
        "postcode": "11049",
        "country": "臺灣",
        "country_code": "tw"
    },
    "importance": 0.55
    ...
}

# Response for a small village - much sparser
{
    "name": "Some Village",
    "display_name": "Some Village, Some County, Taiwan",
    "address": {
        "village": "Some Village",
        "county": "Some County",
        "country": "Taiwan",
        "country_code": "tw"
    }
    # Notice: no road, no city, no postcode, no importance!
}
```

### What Happens If We Don't Handle This?

```python
# Code that assumes all fields exist
def get_city(result):
    return result["address"]["city"]

# Works for Taipei 101
city = get_city(taipei_101_result)  # "Taipei"

# CRASHES for village
city = get_city(village_result)     # KeyError: 'city'
```

**Our goal**: Write code that works for **all** responses, not just the "nice" ones.

---

## 2.2 Safe Dictionary Access

### The Problem with Direct Access

Direct dictionary access (`dict["key"]`) crashes if the key doesn't exist:

```python
result = {"name": "Taipei 101"}

# This works
name = result["name"]  # "Taipei 101"

# This CRASHES
city = result["city"]  # KeyError: 'city'

# Nested access - even more dangerous
city = result["address"]["city"]  # KeyError: 'address'
```

### Solution 1: The `.get()` Method

The `.get()` method returns `None` (or a default value) if the key doesn't exist:

```python
result = {"name": "Taipei 101"}

# Basic .get() - returns None if missing
city = result.get("city")
print(city)  # None

# .get() with default value
city = result.get("city", "Unknown")
print(city)  # "Unknown"

# Chained .get() for nested access
# First get "address" (or empty dict), then get "city" from that
address = result.get("address", {})
city = address.get("city", "Unknown")
print(city)  # "Unknown"
```

**Why `{}` as the default for nested dicts?**

```python
# If we use None as default:
address = result.get("address")  # None
city = address.get("city")       # AttributeError: 'NoneType' has no attribute 'get'

# If we use {} as default:
address = result.get("address", {})  # {}
city = address.get("city", "Unknown")  # "Unknown" - works!
```

### Solution 2: Check Before Access

Use `in` operator or `if` statements to check first:

```python
result = {"name": "Taipei 101", "address": {"city": "Taipei"}}

# Check if key exists
if "address" in result:
    address = result["address"]
    if "city" in address:
        city = address["city"]
    else:
        city = "Unknown"
else:
    city = "Unknown"

# Check if list is not empty
results = []
if results:  # Empty list is "falsy"
    first = results[0]
else:
    first = None
```

**This works but gets verbose** for deeply nested data.

### Solution 3: Try/Except

Wrap risky code in try/except blocks:

```python
result = {"name": "Taipei 101"}

try:
    city = result["address"]["city"]
except KeyError:
    city = "Unknown"
except TypeError:  # Handles case where result["address"] is None
    city = "Unknown"
```

**When to use each approach**:

| Approach | Use When |
|----------|----------|
| `.get()` | Simple, one-level access |
| `if/in` | You need to do different things based on presence |
| `try/except` | Deep nesting or when errors are expected |

---

## 2.3 Building a Safe Data Extractor

Let's create a **utility function** that safely extracts data from nested structures:

```python
def safe_get(data: dict, *keys, default=None):
    """
    Safely get a nested value from a dictionary.

    This function traverses a nested dictionary structure using
    the provided keys, returning a default value if any key
    is missing or if we encounter None.

    Args:
        data: The dictionary to search
        *keys: The keys to traverse (variable number of arguments)
        default: Value to return if path doesn't exist

    Returns:
        The value at the path, or default if not found

    Examples:
        >>> data = {"address": {"city": "Taipei"}}
        >>> safe_get(data, "address", "city")
        'Taipei'
        >>> safe_get(data, "address", "country", default="Unknown")
        'Unknown'
        >>> safe_get(data, "missing", "path")
        None
    """
    current = data  # Start at the root

    # Traverse each key in the path
    for key in keys:
        if isinstance(current, dict):
            # If current is a dict, use .get() to safely access
            current = current.get(key)
        elif isinstance(current, list) and isinstance(key, int):
            # If current is a list and key is an integer, try index access
            try:
                current = current[key]
            except IndexError:
                return default
        else:
            # current is neither dict nor list (or key type mismatch)
            return default

        # If we hit None at any point, return default
        if current is None:
            return default

    return current
```

### How `safe_get` Works (Step by Step)

Let's trace through an example:

```python
data = {
    "result": {
        "address": {
            "city": "Taipei"
        }
    }
}

# Call: safe_get(data, "result", "address", "city")

# Step 1: current = data (the whole dict)
# Step 2: key = "result"
#         current = data.get("result") = {"address": {"city": "Taipei"}}
# Step 3: key = "address"
#         current = current.get("address") = {"city": "Taipei"}
# Step 4: key = "city"
#         current = current.get("city") = "Taipei"
# Step 5: Return "Taipei"
```

Now with a missing key:

```python
# Call: safe_get(data, "result", "address", "country", default="Unknown")

# Step 1: current = data
# Step 2: key = "result"
#         current = {"address": {"city": "Taipei"}}
# Step 3: key = "address"
#         current = {"city": "Taipei"}
# Step 4: key = "country"
#         current = {"city": "Taipei"}.get("country") = None
# Step 5: current is None, so return default = "Unknown"
```

### Using `safe_get` in Practice

```python
# Raw Nominatim response
result = {
    "lat": "25.0338",
    "lon": "121.5645",
    "display_name": "Taipei 101, Taipei, Taiwan",
    "address": {
        "tourism": "台北101",
        "city": "Taipei"
    }
}

# Safe data extraction
name = safe_get(result, "name", default=safe_get(result, "display_name", default="Unknown"))
city = safe_get(result, "address", "city", default="Unknown")
country = safe_get(result, "address", "country", default="Unknown")
postcode = safe_get(result, "address", "postcode", default="N/A")

print(f"Name: {name}")       # "Taipei 101, Taipei, Taiwan" (fell back to display_name)
print(f"City: {city}")       # "Taipei"
print(f"Country: {country}") # "Unknown"
print(f"Postcode: {postcode}") # "N/A"
```

---

## 2.4 Introduction to Recursion

### What is Recursion?

**Recursion** is when a function calls itself to solve a problem. It's a powerful technique for working with nested or hierarchical data structures—exactly what we encounter with complex JSON responses.

```
┌──────────────────────────────────────────────────────────┐
│  Recursion: A function that calls itself                 │
│                                                          │
│  solve_problem(data)                                     │
│      │                                                   │
│      ├─── Is this the simple case? → Return answer       │
│      │                                                   │
│      └─── Otherwise → solve_problem(smaller_data)        │
│                              │                           │
│                              └─── ... and so on          │
└──────────────────────────────────────────────────────────┘
```

### The Two Essential Parts of Recursion

Every recursive function needs:

1. **Base Case**: When to stop (prevents infinite recursion)
2. **Recursive Case**: How to break down the problem and call itself

```python
def countdown(n):
    """Count down from n to 1."""
    # Base case: stop when n reaches 0
    if n <= 0:
        print("Done!")
        return

    # Recursive case: print n, then countdown from n-1
    print(n)
    countdown(n - 1)  # Function calls itself with a smaller value


countdown(5)
# Output:
# 5
# 4
# 3
# 2
# 1
# Done!
```

### Classic Example: Factorial

Factorial (n!) is the product of all positive integers up to n:
- 5! = 5 × 4 × 3 × 2 × 1 = 120
- 3! = 3 × 2 × 1 = 6
- 1! = 1
- 0! = 1 (by definition)

**Mathematically**: n! = n × (n-1)!

```python
def factorial(n):
    """
    Calculate n! (n factorial) recursively.

    Base case: 0! = 1
    Recursive case: n! = n × (n-1)!
    """
    # Base case
    if n <= 1:
        return 1

    # Recursive case
    return n * factorial(n - 1)


print(factorial(5))  # 120
print(factorial(0))  # 1
```

**How it works (tracing the calls):**
```
factorial(5)
  = 5 * factorial(4)
  = 5 * (4 * factorial(3))
  = 5 * (4 * (3 * factorial(2)))
  = 5 * (4 * (3 * (2 * factorial(1))))
  = 5 * (4 * (3 * (2 * 1)))         ← Base case reached
  = 5 * (4 * (3 * 2))
  = 5 * (4 * 6)
  = 5 * 24
  = 120
```

### Why Recursion Matters for JSON Parsing

Nested JSON structures are naturally recursive—dictionaries can contain dictionaries, which can contain more dictionaries, to any depth:

```python
data = {
    "level1": {
        "level2": {
            "level3": {
                "value": "deep inside!"
            }
        }
    }
}
```

You don't know in advance how deep the nesting goes. Recursion handles this naturally.

---

## 2.5 Recursive JSON Traversal

### Finding All Values for a Key

Let's write a recursive function that finds all occurrences of a key anywhere in a nested structure:

```python
def find_all_values(data, target_key):
    """
    Recursively find all values for a given key in nested data.

    Args:
        data: A dictionary, list, or value
        target_key: The key to search for

    Returns:
        List of all values found for that key

    Example:
        >>> data = {"a": 1, "nested": {"a": 2, "deep": {"a": 3}}}
        >>> find_all_values(data, "a")
        [1, 2, 3]
    """
    results = []

    if isinstance(data, dict):
        # If it's a dictionary, check each key
        for key, value in data.items():
            if key == target_key:
                results.append(value)
            # Recursively search in the value (could be dict or list)
            results.extend(find_all_values(value, target_key))

    elif isinstance(data, list):
        # If it's a list, search each element
        for item in data:
            results.extend(find_all_values(item, target_key))

    # Base case: if it's neither dict nor list, there's nothing to search
    return results


# Example with Nominatim-like data
sample_response = {
    "place_id": 123,
    "name": "Taipei 101",
    "address": {
        "name": "台北101",
        "road": "Xinyi Road",
        "details": {
            "name": "Taipei World Financial Center"
        }
    },
    "alternates": [
        {"name": "台北金融大樓"},
        {"name": "Taipei Financial Center"}
    ]
}

all_names = find_all_values(sample_response, "name")
print(all_names)
# ['Taipei 101', '台北101', 'Taipei World Financial Center',
#  '台北金融大樓', 'Taipei Financial Center']
```

### Flattening Nested Structures

Sometimes you want to flatten deeply nested JSON into a simple key-value format:

```python
def flatten_dict(data, parent_key="", separator="."):
    """
    Flatten a nested dictionary into a single-level dictionary.

    Args:
        data: Nested dictionary
        parent_key: Prefix for keys (used in recursion)
        separator: Character to join nested keys

    Returns:
        Flattened dictionary with dot-notation keys

    Example:
        >>> nested = {"a": {"b": {"c": 1}}}
        >>> flatten_dict(nested)
        {'a.b.c': 1}
    """
    items = {}

    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}{separator}{key}" if parent_key else key

            if isinstance(value, dict):
                # Recurse into nested dictionary
                items.update(flatten_dict(value, new_key, separator))
    elif isinstance(value, list):
        # Handle lists with index notation
        for i, item in enumerate(value):
            if isinstance(item, dict):
                items.update(flatten_dict(item, f"{new_key}[{i}]", separator))
            else:
                items[f"{new_key}[{i}]"] = item
    else:
        # Base case: simple value
        items[new_key] = value

    return items


# Example
address_data = {
    "address": {
        "road": "Xinyi Road",
        "city": "Taipei",
        "country": "Taiwan",
        "details": {
            "postcode": "110",
            "district": "Xinyi"
        }
    }
}

flat = flatten_dict(address_data)
for key, value in flat.items():
    print(f"{key}: {value}")

# Output:
# address.road: Xinyi Road
# address.city: Taipei
# address.country: Taiwan
# address.details.postcode: 110
# address.details.district: Xinyi
```

### Counting Nesting Depth

How deep is your JSON nested? Recursion makes this easy:

```python
def max_depth(data):
    """
    Find the maximum nesting depth of a data structure.

    Args:
        data: A dictionary, list, or value

    Returns:
        Integer depth (1 for flat dict, higher for nested)
    """
    if isinstance(data, dict):
        if not data:  # Empty dict
            return 1
        # Depth is 1 (for this level) plus max depth of children
        return 1 + max(max_depth(v) for v in data.values())

    elif isinstance(data, list):
        if not data:  # Empty list
            return 1
        return 1 + max(max_depth(item) for item in data)

    else:
        # Base case: simple value has depth 0
        return 0


# Examples
print(max_depth({"a": 1}))                     # 1
print(max_depth({"a": {"b": 2}}))              # 2
print(max_depth({"a": {"b": {"c": 3}}}))       # 3
print(max_depth(sample_response))              # 4
```

---

## 2.6 Mini-Exercise: Recursive Key Search

Write a recursive function that finds the path to a value in nested JSON:

```python
def find_path(data, target_value, current_path=""):
    """
    Find the path to a target value in nested data.

    Args:
        data: Nested dictionary/list
        target_value: The value to find
        current_path: Path so far (used in recursion)

    Returns:
        Path string like "address.city" or None if not found

    Example:
        >>> data = {"a": {"b": {"c": "found me!"}}}
        >>> find_path(data, "found me!")
        'a.b.c'
    """
    # TODO: Implement this function
    pass


# Test cases
test_data = {
    "name": "Taipei 101",
    "location": {
        "city": "Taipei",
        "coordinates": {
            "lat": 25.0339,
            "lon": 121.5645
        }
    }
}

print(find_path(test_data, "Taipei"))      # Should print: location.city
print(find_path(test_data, 25.0339))       # Should print: location.coordinates.lat
print(find_path(test_data, "Not here"))    # Should print: None
```

<details>
<summary>Solution</summary>

```python
def find_path(data, target_value, current_path=""):
    """Find the path to a target value in nested data."""

    if isinstance(data, dict):
        for key, value in data.items():
            # Build the new path
            new_path = f"{current_path}.{key}" if current_path else key

            # Check if this value matches
            if value == target_value:
                return new_path

            # Recursively search in nested structures
            result = find_path(value, target_value, new_path)
            if result is not None:
                return result

    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{current_path}[{i}]"

            if item == target_value:
                return new_path

            result = find_path(item, target_value, new_path)
            if result is not None:
                return result

    # Base case: value not found in this branch
    return None
```

</details>

---

## 2.7 Parsing Nominatim Results Robustly

Now let's build a complete, robust parser for Nominatim results:

```python
from typing import TypedDict

class GeocodedPlace(TypedDict):
    """
    Type definition for a geocoded place.

    TypedDict provides documentation and IDE hints about
    what fields our parsed result will have.
    """
    name: str
    lat: float
    lon: float
    display_name: str
    place_type: str
    importance: float
    address: dict


def parse_nominatim_result(result: dict) -> GeocodedPlace:
    """
    Parse a single Nominatim result into a clean, consistent structure.

    This function handles:
    - Missing fields (uses sensible defaults)
    - Type conversion (lat/lon strings to floats)
    - Data normalization (consistent field names)

    Args:
        result: Raw result dictionary from Nominatim API

    Returns:
        Cleaned GeocodedPlace dictionary with consistent structure
    """
    # Handle coordinates - they come as strings!
    # Use try/except to handle malformed data
    try:
        lat = float(result.get("lat", 0))
        lon = float(result.get("lon", 0))
    except (ValueError, TypeError):
        # float() failed - use default coordinates
        lat, lon = 0.0, 0.0

    # Handle importance score
    try:
        importance = float(result.get("importance", 0))
    except (ValueError, TypeError):
        importance = 0.0

    # Build the clean result dictionary
    return {
        # Name: prefer "name" field, fall back to display_name
        "name": result.get("name", result.get("display_name", "Unknown")),

        # Coordinates (now as floats)
        "lat": lat,
        "lon": lon,

        # Full address string
        "display_name": result.get("display_name", ""),

        # Classification - combine class and type
        "place_type": f"{result.get('class', '')}:{result.get('type', '')}",

        # Ranking
        "importance": importance,

        # Raw address object for further processing
        "address": result.get("address", {})
    }


def parse_nominatim_response(response_data: list) -> list[GeocodedPlace]:
    """
    Parse a complete Nominatim response (list of results).

    Args:
        response_data: List of results from Nominatim API

    Returns:
        List of cleaned GeocodedPlace dictionaries
    """
    # Handle empty response
    if not response_data:
        return []

    # Parse each result
    return [parse_nominatim_result(r) for r in response_data]
```

### Why This Design?

1. **Separation of concerns**: One function for single results, one for the list
2. **Defensive**: Every field access has a fallback
3. **Type conversion**: Strings become proper floats
4. **Consistent output**: Same fields regardless of input variations
5. **Documented**: TypedDict shows exactly what we return

---

## 2.8 Mini-Exercise: Handle Missing Data

Write a function that formats an address from a Nominatim result, handling all possible missing fields:

```python
def format_address(result: dict) -> str:
    """
    Format an address from Nominatim result.

    Should handle missing fields gracefully.
    Format: "street number, district, city, country"
    Skip empty parts.

    Examples:
        "7 Section 5 Xinyi Road, Xinyi, Taipei, Taiwan"
        "Shibuya, Tokyo, Japan"  (no street)
        "Taiwan"  (only country)
        "Unknown location"  (nothing available)
    """
    # Your code here
    pass
```

**Test cases to handle:**

```python
test_cases = [
    # Complete address
    {
        "address": {
            "house_number": "7",
            "road": "Section 5 Xinyi Road",
            "suburb": "Xinyi District",
            "city": "Taipei",
            "country": "Taiwan"
        }
    },
    # Missing street
    {
        "address": {
            "suburb": "Shibuya",
            "city": "Tokyo",
            "country": "Japan"
        }
    },
    # Only country
    {
        "address": {
            "country": "Taiwan"
        }
    },
    # Empty address
    {
        "address": {}
    },
    # No address field at all
    {}
]
```

<details>
<summary>Solution</summary>

```python
def format_address(result: dict) -> str:
    """
    Format an address from Nominatim result.
    Handles missing fields gracefully.
    """
    # Step 1: Get the address object (empty dict if missing)
    address = result.get("address", {})

    # Step 2: Build the street part
    street_parts = []
    if address.get("house_number"):
        street_parts.append(address["house_number"])
    if address.get("road"):
        street_parts.append(address["road"])
    street = " ".join(street_parts)  # Combine with space

    # Step 3: Collect all address parts
    parts = []

    # Add street if we have it
    if street:
        parts.append(street)

    # District - try multiple possible keys
    # (Nominatim uses different keys in different regions)
    district = (address.get("suburb") or
                address.get("district") or
                address.get("neighbourhood") or
                address.get("quarter"))
    if district:
        parts.append(district)

    # City - also has multiple possible keys
    city = (address.get("city") or
            address.get("town") or
            address.get("village") or
            address.get("municipality") or
            address.get("county"))
    if city:
        parts.append(city)

    # State/Province (common in US, Australia)
    state = address.get("state")
    if state:
        parts.append(state)

    # Country (almost always present)
    if address.get("country"):
        parts.append(address["country"])

    # Step 4: Join parts or return default
    if parts:
        return ", ".join(parts)
    else:
        return "Unknown location"


# Test
for i, case in enumerate(test_cases):
    print(f"Case {i + 1}: {format_address(case)}")

# Output:
# Case 1: 7 Section 5 Xinyi Road, Xinyi District, Taipei, Taiwan
# Case 2: Shibuya, Tokyo, Japan
# Case 3: Taiwan
# Case 4: Unknown location
# Case 5: Unknown location
```

**Key techniques used:**
1. `result.get("address", {})` - Safe access with empty dict default
2. `address.get("key")` - Returns None if missing
3. `or` chaining - Try multiple keys, use first non-empty
4. Build list then join - Easier than string concatenation

</details>

---

## 2.9 Working with Bounding Boxes

Nominatim returns bounding boxes as a list of strings:

```json
"boundingbox": ["25.0329", "25.0349", "121.5634", "121.5654"]
```

Format: `[south, north, west, east]`

This represents the rectangular area that contains the place:

```
                 North (25.0349)
                    ────────
                    │      │
      West          │      │         East
    (121.5634)      │      │      (121.5654)
                    │      │
                    ────────
                 South (25.0329)
```

### Why Bounding Boxes Matter

1. **Zoom level**: Larger box = zoom out more on the map
2. **Area calculations**: Estimate the size of a place
3. **Containment checks**: Is a point inside this area?

### Parsing Bounding Boxes

```python
def parse_bounding_box(bbox: list) -> dict | None:
    """
    Parse a Nominatim bounding box.

    Args:
        bbox: List of [south, north, west, east] as strings

    Returns:
        Dictionary with float coordinates, or None if invalid
    """
    # Validate input
    if not bbox or len(bbox) != 4:
        return None

    try:
        return {
            "south": float(bbox[0]),
            "north": float(bbox[1]),
            "west": float(bbox[2]),
            "east": float(bbox[3])
        }
    except (ValueError, TypeError):
        return None


def bbox_center(bbox: dict) -> tuple[float, float]:
    """Calculate the center point of a bounding box."""
    lat = (bbox["south"] + bbox["north"]) / 2
    lon = (bbox["west"] + bbox["east"]) / 2
    return (lat, lon)


def bbox_area_km2(bbox: dict) -> float:
    """
    Estimate the area of a bounding box in km².

    Note: This is an approximation. At the equator, 1 degree ≈ 111 km.
    As you move toward the poles, longitude degrees get smaller.
    """
    import math

    lat_diff = bbox["north"] - bbox["south"]
    lon_diff = bbox["east"] - bbox["west"]

    # 1 degree latitude ≈ 111 km everywhere
    lat_km = lat_diff * 111

    # 1 degree longitude ≈ 111 * cos(latitude) km
    mid_lat = (bbox["north"] + bbox["south"]) / 2
    lon_km = lon_diff * 111 * math.cos(math.radians(mid_lat))

    return lat_km * lon_km


# Example usage
result = {
    "boundingbox": ["25.0329", "25.0349", "121.5634", "121.5654"]
}

bbox = parse_bounding_box(result["boundingbox"])
if bbox:
    center = bbox_center(bbox)
    area = bbox_area_km2(bbox)
    print(f"Center: {center}")
    print(f"Area: {area:.4f} km²")
```

---

# ☕ 10-Minute Break

Stretch, grab water, check your phone!

---

# Hour 3: Error Handling and Building a CLI Tool

## 3.1 Error Handling Essentials

When working with APIs, many things can go wrong. Good error handling keeps your program running and gives users helpful feedback.

### The `try/except` Statement

```python
try:
    result = risky_operation()
except SomeError:
    print("Something went wrong")
```

### Catching Multiple Exceptions

```python
try:
    response = requests.get(url, timeout=10)
    data = response.json()
    result = data[0]["lat"]

except requests.exceptions.Timeout:
    print("Request timed out")

except requests.exceptions.ConnectionError:
    print("Connection failed")

except json.JSONDecodeError:
    print("Invalid JSON response")

except (KeyError, IndexError):
    print("Unexpected response format")

except Exception as e:
    print(f"Unexpected error: {e}")
```

**Best practice**: Catch specific exceptions, not just `Exception`.

### The `try/except/else/finally` Structure

```python
try:
    data = json.load(open("data.json"))
except FileNotFoundError:
    data = {}
else:
    # Only runs if NO exception
    print(f"Loaded {len(data)} items")
finally:
    # ALWAYS runs - good for cleanup
    print("Done")
```

---

## 3.2 Common API Errors and How to Handle Them

| Error | Cause | Solution |
|-------|-------|----------|
| `Timeout` | Server too slow | Retry or show message |
| `ConnectionError` | No internet | Check connection |
| `HTTPError 403` | Forbidden | Check User-Agent |
| `HTTPError 429` | Rate limited | Slow down requests |
| `JSONDecodeError` | Invalid response | Handle gracefully |
| `KeyError` | Missing field | Use `.get()` with defaults |

### Complete Error Handling Pattern

```python
import requests
import json

def geocode(query: str) -> dict:
    """Geocode with comprehensive error handling."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json", "limit": 1}
    headers = {"User-Agent": "CS101/1.0 (test@example.com)"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        # Handle HTTP errors
        if response.status_code == 429:
            return {"error": "Rate limited - slow down"}
        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}"}

        data = response.json()
        if not data:
            return {"error": f"No results for: {query}"}

        result = data[0]
        return {
            "name": result.get("name", query),
            "lat": float(result["lat"]),
            "lon": float(result["lon"]),
            "display_name": result.get("display_name", "")
        }

    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection failed"}
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        return {"error": f"Parse error: {e}"}
```

---

## 3.3 Mini-Exercise: Error Handling Practice

Add error handling to this function:

```python
def get_coordinates(place_name: str) -> tuple[float, float]:
    """Get coordinates for a place name."""
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "CS101/1.0 (test@example.com)"}
    params = {"q": place_name, "format": "json", "limit": 1}

    # No error handling - will crash on any problem!
    response = requests.get(url, params=params, headers=headers, timeout=10)
    data = response.json()
    result = data[0]
    return (float(result["lat"]), float(result["lon"]))
```

Handle: timeout, connection errors, empty results, missing/invalid coordinates.

<details>
<summary>Solution</summary>

```python
def get_coordinates(place_name: str) -> tuple[float, float] | None:
    """Get coordinates with error handling."""
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "CS101/1.0 (test@example.com)"}
    params = {"q": place_name, "format": "json", "limit": 1}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"HTTP error: {response.status_code}")
            return None

        data = response.json()
        if not data:
            print(f"No results for: {place_name}")
            return None

        result = data[0]
        return (float(result["lat"]), float(result["lon"]))

    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.ConnectionError:
        print("Connection failed")
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"Parse error: {e}")

    return None
```

</details>

---

## 3.4 Building a Simple CLI Geocoder

Here's a complete interactive geocoder that puts everything together:

```python
#!/usr/bin/env python3
"""Simple Geocoder CLI - Convert place names to coordinates."""

import requests
import time

def geocode(query: str) -> dict | None:
    """Geocode a place name with error handling."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json", "limit": 1}
    headers = {"User-Agent": "CS101-Geocoder/1.0 (cs101@university.edu)"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"  HTTP error: {response.status_code}")
            return None

        data = response.json()
        if not data:
            print(f"  No results for: {query}")
            return None

        result = data[0]
        return {
            "name": result.get("name", query),
            "lat": float(result["lat"]),
            "lon": float(result["lon"]),
            "display_name": result.get("display_name", "")
        }

    except requests.exceptions.Timeout:
        print("  Request timed out")
    except requests.exceptions.ConnectionError:
        print("  Connection failed")
    except (KeyError, ValueError) as e:
        print(f"  Parse error: {e}")

    return None


def main():
    """Run the interactive geocoder."""
    print("\n=== Geocoder CLI ===")
    print("Enter a place name, or 'quit' to exit.\n")

    last_request = 0

    while True:
        try:
            query = input("geocoder> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not query:
            continue

        if query.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        # Rate limiting
        elapsed = time.time() - last_request
        if elapsed < 1 and last_request > 0:
            time.sleep(1 - elapsed)

        result = geocode(query)
        last_request = time.time()

        if result:
            print(f"\n  Name: {result['name']}")
            print(f"  Coordinates: ({result['lat']:.6f}, {result['lon']:.6f})")
            print(f"  Address: {result['display_name']}\n")


if __name__ == "__main__":
    main()
```

### Example Session
```
=== Geocoder CLI ===
Enter a place name, or 'quit' to exit.

geocoder> Taipei 101

  Name: 台北101
  Coordinates: (25.033835, 121.564499)
  Address: 台北101, 7, 信義路五段, 西村里, 信義區, 信義商圈, 臺北市, 11049, 臺灣

geocoder> xyznotaplace
  No results for: xyznotaplace

geocoder> quit
Goodbye!
```

---

## 3.5 Best Practices Summary

| Category | Practice | Example |
|----------|----------|---------|
| **Errors** | Catch specific exceptions | `except ValueError` not `except Exception` |
| **Errors** | Provide context in messages | `f"No results for: {query}"` |
| **API** | Always set timeouts | `timeout=10` |
| **API** | Respect rate limits | `time.sleep(1)` between requests |
| **Parsing** | Use `.get()` with defaults | `result.get("key", "default")` |
| **Parsing** | Convert string types | `float(result["lat"])` |

---

## 3.6 Homework Assignments

### Assignment 1: Batch Geocoder (Basic)
Create a script that:
1. Reads place names from a text file (one per line)
2. Geocodes each place with rate limiting
3. Writes results to a JSON file
4. Handles errors gracefully (skip failed places, don't crash)
5. Reports summary at the end (X succeeded, Y failed)

### Assignment 2: Address Formatter (Intermediate)
Create a function that formats addresses according to country conventions:
- Taiwan: "District, City, Country"
- USA: "Street, City, State ZIP"
- Japan: "Prefecture City District"

The function should detect the country and format accordingly.

### Assignment 3: Geocoder with Retry (Advanced)
Enhance the geocoder to:
1. Retry failed requests up to 3 times with exponential backoff
2. Try alternative queries if exact match fails:
   - Remove punctuation
   - Try just the first 3 words
3. Cache both successes and failures (to avoid retrying known failures)

---

## Additional Resources

### Documentation
- [Nominatim API Documentation](https://nominatim.org/release-docs/latest/api/Overview/)
- [OpenStreetMap Wiki - Nominatim](https://wiki.openstreetmap.org/wiki/Nominatim)
- [Python Requests - Error Handling](https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions)
- [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)

### Alternative Geocoding Services
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding) (paid)
- [Mapbox Geocoding](https://docs.mapbox.com/api/search/geocoding/) (freemium)
- [HERE Geocoding](https://developer.here.com/documentation/geocoding-search-api/) (freemium)
- [Geopy](https://geopy.readthedocs.io/) (Python library supporting multiple services)

### Practice Resources
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - Practice parsing nested JSON
- [httpbin.org](https://httpbin.org/) - Test error handling with fake errors

---

## Next Week Preview

**Week 6: Searching for Places (Lazy Loading)**
- Query parameters and pagination
- Python generators and the `yield` keyword
- Lazy evaluation for memory efficiency
- Building a paginated search interface

---

*End of Week 5 Lecture*
