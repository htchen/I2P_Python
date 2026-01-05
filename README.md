# CS101 - Building Location-Based Systems with Python

**Methodology:** Project-Based Learning (PBL) + Algorithmic Drills

**Capstone Project:** "The Smart City Navigator" — A web app that optimizes routes and finds places based on user constraints.

**Core Tools:** OpenStreetMap Ecosystem (Nominatim API), OSRM (for routing), and Folium (for map rendering).

---

## Grading

| Component | Weight | Notes |
|-----------|--------|-------|
| Midterm Exam | 40% | 有兩次考試機會，只取較高分的那次（電腦教室考試） |
| Labs | 30% | 多次電腦教室實驗加小考 |
| Written Exam | 5% | 筆試，跟期中考一起 |
| Final Project | 25% | 期末專題 |

---

## Final Project Goal

By Week 16, every student (or group) will have a working Python web application where:

1. A user enters a starting location (e.g., "University Dorm")
2. The user selects a category (e.g., "Cheap Pizza") and a constraint (e.g., "Within 10 mins walk")
3. The app uses the **Nominatim API** to find candidates
4. The app uses the **OSRM API** (Open Source Routing Machine) to filter by real walking time
5. The app calculates the optimal route to visit the top-rated spots
6. The result is displayed on an interactive **Leaflet Map** (generated via Folium) embedded in a web page

---

## Weekly Schedule

Every week introduces a new Python concept specifically required to build the next feature of the app.

### Phase 1: Data & Coordinates (Weeks 1-3)

**Theme:** "Where am I?" — Python Basics & Geodata

#### Week 1-1: Variables & The Coordinate System
- **Concept:** Variables, Floats, Tuples (Immutable data)
- **Project Task:** Create a script to store specific locations as `(latitude, longitude)` tuples. Print them out.

#### Week 1-2: Functions & Distance Logic
- **Concept:** Math module, Defining Functions, Arguments
- **Project Task:** Implement the Haversine Formula (calculating distance between two lat/long points on a sphere) as a Python function.
- **CS Concept:** Abstraction (hiding complex math behind a function call)

#### Week 2-1: Lists, Loops & The Route
- **Concept:** Lists, `for` loops, `range`, `zip`, `map`, `filter`
- **Project Task:** Create a list of 5 coordinate tuples. Write a loop that calculates the total distance of the path connecting them sequentially.
- **Drill:** Complete P01–P10 (Lists) from *99 Problems in Python* to master indexing and list manipulation.

#### Week 2-2: Dictionaries & Storing "Places"
- **Concept:** Dictionaries (Key-Value pairs), Nested structures
- **Project Task:** Move from simple tuples to storing complex data:
  ```python
  place = {"name": "Joe's Pizza", "coords": (40.71, -74.00), "rating": 4.5}
  ```
- **Drill:** Complete P11–P15 (Run-length encoding/Data compression). These problems teach students how to process lists and look for patterns.

#### Week 3: JSON & File I/O
- **Concept:** JSON format, Reading/Writing files
- **Project Task:** Save your database of "favorite places" to a `.json` file and write a script to load it back.

---

### Phase 2: The API & The Cloud (Weeks 4-8)

**Theme:** "Fetching the World" — APIs, Network, and Parsing

#### Week 4: HTTP Requests & API Keys
- **Concept:** The Request/Response cycle, Status Codes (200 vs 403), User-Agent Headers
- **Project Task:** Make specific calls to `https://nominatim.openstreetmap.org` using the `requests` library. Learn why OSM requires a valid Email/User-Agent to prevent banning.

#### Week 5: The Nominatim API (Geocoding)
- **Concept:** Parsing complex nested JSON responses, Error Handling (`try/except`)
- **Project Task:** Build a CLI tool: User types "Empire State Building", script returns `(40.748, -73.985)` using the OSM free search endpoint.

#### Week 6: Searching for Places (Lazy Loading)
- **Concept:** Query parameters, Pagination, Lazy Evaluation (Generators)
- **Project Task:** Script that asks "What do you want to eat?". Use a Generator (`yield`) to handle API pagination, fetching results one page at a time to avoid memory overload.

#### Week 7: OSRM API (Real Routing)
- **Concept:** 2D Lists (Matrices), Cost comparison
- **Project Task:** Compare "Haversine distance" (straight line) vs "OSRM Distance" (walking time). Fetch route geometry (JSON) from the OSRM public demo server.

#### Week 8: Midterm Exam 1 (Tue. & Thu.)

---

### Phase 3: Algorithms & Logic (Weeks 9-12)

**Theme:** "Making Smart Decisions" — CS Fundamentals

#### Week 9: Functional Patterns & Sorting
- **Concept:** Functional Programming (`map`, `filter`), Lambda functions, Immutability
- **Project Task:** Sort the downloaded Places by Rating (High→Low). Use `filter()` or List Comprehensions to purely remove any place further than a 15-minute walk without modifying the original list.
- **Drill:** Complete P46–P50 (Logic & Codes) from *99 Problems*. Understanding truth tables helps with writing complex filter conditions.

#### Week 10: The "Traveling Salesperson" (Graph Theory Lite)
- **Concept:** Permutations, Brute Force optimization
- **Project Task:** Given 3 selected restaurants, find the order of visitation that results in the shortest total walking time.
- **Drill:** Review P80–P86 (Graphs) from *99 Problems*. Visualizing nodes and edges is critical for understanding routing logic.

#### Week 11: Midterm Exam 2 (Tue. & Thu.)

#### Week 12: Refactoring: OOP & Decorators
- **Concept:** Classes, Methods, Decorators
- **Project Task:** Refactor the messy code into a `Place` class. Create a `@rate_limit` decorator to ensure your API calls sleep for 1 second between requests (crucial for OSM compliance).

---

### Phase 4: The Web Interface (Weeks 13-16)

**Theme:** "Showing the User" — Web Frameworks & Final Project

#### Week 13: Introduction to Flask (Web Server)
- **Concept:** Routes, Templates, HTML basics
- **Project Task:** "Hello World" web server. Passing Python variables to an HTML page using Jinja2.

#### Week 14: Interactive Maps with Folium
- **Concept:** Python-to-JS transpilation (Folium/Leaflet)
- **Project Task:** Use the `folium` library to generate an interactive map HTML file. Add markers for your found places and draw lines for the calculated route.

#### Week 15: Final Integration Sprint
- **Focus:** Connecting the User Input Form → Flask → Nominatim API → Sorting Logic → Folium Map Display

#### Week 16: Final Demo Day

---

## Tech Stack

### Python Libraries
- `requests` — HTTP client for API calls
- `flask` — Web framework
- `folium` — Interactive map generation

### Open Data APIs
- **Nominatim (OSM):** For Geocoding and Place Search
- **OSRM (Open Source Routing Machine):** For walking/driving duration and paths

---

## Why This Works for CS Freshmen

| Benefit | Description |
|---------|-------------|
| **Instant Visual Feedback** | Students see a pin drop on a map. It feels "real" compared to printing text to a console. |
| **Modern Skillset** | They learn JSON and APIs immediately, which are standard in industry. |
| **Algorithmic Motivation** | They learn sorting because they need to sort restaurants by rating. They learn graphs because they need to find a route. The "Why" is always answered. |
