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

| Week | Lecture | Lab |
|------|---------|-----|
| 1-1 | **Variables & The Coordinate System** — Variables, Floats, Tuples (Immutable data). Create a script to store specific locations as `(latitude, longitude)` tuples. | |
| 1-2 | **Functions & Distance Logic** — Math module, Defining Functions, Arguments. Implement the Haversine Formula as a Python function. | |
| 2-1 | **Lists, Loops & The Route** — Lists, `for` loops, `range`, `zip`, `map`, `filter`. Calculate total distance of a path connecting coordinates sequentially. | |
| 2-2 | **Dictionaries & Storing "Places"** — Dictionaries (Key-Value pairs), Nested structures. Store complex place data with name, coords, and rating. | |
| 3 | **JSON & File I/O** — JSON format, Reading/Writing files. Save and load a database of "favorite places" to/from a `.json` file. | |

---

### Phase 2: The API & The Cloud (Weeks 4-8)

**Theme:** "Fetching the World" — APIs, Network, and Parsing

| Week | Lecture | Lab |
|------|---------|-----|
| 4 | **HTTP Requests & API Keys** — Request/Response cycle, Status Codes (200 vs 403), User-Agent Headers. Make calls to Nominatim API using `requests`. | |
| 5 | **The Nominatim API (Geocoding)** — Parsing nested JSON, Error Handling (`try/except`). Build a CLI geocoding tool. | |
| 6 | **Searching for Places (Lazy Loading)** — Query parameters, Pagination, Generators (`yield`). Handle API pagination efficiently. | |
| 7 | **Midterm Exam 1 (Tue. & Thu.)** | |
| 8 | **OSRM API (Real Routing)** — 2D Lists (Matrices), Cost comparison. Compare Haversine vs OSRM distance, fetch route geometry. | |

---

### Phase 3: Algorithms & Logic (Weeks 9-12)

**Theme:** "Making Smart Decisions" — CS Fundamentals

| Week | Lecture | Lab |
|------|---------|-----|
| 9 | **Functional Patterns & Sorting** — Functional Programming (`map`, `filter`), Lambda functions, Immutability. Sort places by rating, filter by walk time. | |
| 10 | **The "Traveling Salesperson" (Graph Theory Lite)** — Permutations, Brute Force optimization. Find optimal visitation order for shortest walking time. | |
| 11 | **Midterm Exam 2 (Tue. & Thu.)** | |
| 12 | **Refactoring: OOP & Decorators** — Classes, Methods, Decorators. Create a `Place` class and `@rate_limit` decorator. | |

---

### Phase 4: The Web Interface (Weeks 13-16)

**Theme:** "Showing the User" — Web Frameworks & Final Project

| Week | Lecture | Lab |
|------|---------|-----|
| 13 | **Introduction to Flask (Web Server)** — Routes, Templates, HTML basics. Build a "Hello World" web server with Jinja2 templates. | |
| 14 | **Interactive Maps with Folium** — Python-to-JS transpilation (Folium/Leaflet). Generate interactive map HTML with markers and routes. | |
| 15 | **Final Integration Sprint** — Connect User Input Form → Flask → Nominatim API → Sorting Logic → Folium Map Display. | |
| 16 | **Final Demo Day** | |

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
