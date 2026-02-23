# CS101 - Building Location-Based Systems with Python

**Methodology:** Project-Based Learning (PBL) + Algorithmic Drills

**Capstone Project:** "The Smart City Navigator" — A web app that optimizes routes and finds places based on user constraints.

**Core Tools:** OpenStreetMap Ecosystem (Nominatim API), OSRM (for routing), and Folium (for map rendering).

---

## Grading Policy

| Component | Weight | Notes |
|------------|--------|-------|
| Midterm Exam | 40% | 兩次期中考，只取較高分的那次（電腦教室考試） |
| Labs | 10% | 四次線上實作測驗 |
| Quizzes | 20% | 兩次電腦教室實體小考 |
| Written Exam | 5% | 筆試，跟期中考同時進行 |
| Final Project | 25% | 期末專題 ||

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

# Weekly Schedule

| Week | Date | Lecture (Tue 18:30–21:20) | TA / Exams (Thu 18:40–) |
|------|------|----------------------------|--------------------------|
| 1 | 2/24, 2/26 | 課程介紹, Variables, Coordinates & Functions | TA 講解 OJ 使用規定以及計分 |
| 2 | 3/3, 3/5 | Lists, Loops & Dictionaries | TA 演習／線上實作測驗 #1 <br> @ 18:40-19:40 線上實作測驗 |
| 3 | 3/10, 3/12 | JSON & File I/O | TA 演習 |
| 4 | 3/17, 3/19 | HTTP Requests & API Keys | TA 演習／線上實作測驗 #2 <br> @ 18:40-19:40 線上實作測驗 |
| 5 | 3/24, 3/26 | The Nominatim API (Geocoding) | 實體小考 #1 <br> @ 資電館電腦室 18:40 開始|
| 6 | 3/31, 4/2 | Searching for Places (Lazy Loading) | 校際活動週 放假 |
| 7 | 4/7, 4/9 | Midterm Exam 1 (Tue.) <br> @ 資電館電腦室 18:40 開始| Midterm Exam 1 (Thu.) <br> @ 資電館電腦室 18:40 開始 |
| 8 | 4/14, 4/16 | OSRM API (Real Routing) | TA 演習 |
| 9 | 4/21, 4/23 | Functional Patterns & Sorting | TA 演習／線上實作測驗 #3 <br> @ 18:40-19:40 線上實作測驗|
| 10 | 4/28, 4/30 | The "Traveling Salesperson" (Graph Theory Lite) | 實體小考 #2 <br> @ 資電館電腦室 18:40 開始|
| 11 | 5/5, 5/7 | Midterm Exam 2 (Tue.) <br> @ 資電館電腦室 18:40 開始| Midterm Exam 2 (Thu.) <br> @ 資電館電腦室 18:40 開始|
| 12 | 5/12, 5/14 | Refactoring: OOP & Decorators | TA 演習 |
| 13 | 5/19, 5/21 | Introduction to Flask (Web Server) | TA 演習／線上實作測驗 #4 <br> @ 18:40-19:40 線上實作測驗|
| 14 | 5/26, 5/28 | Interactive Maps with Folium | TA 演習 |
| 15 | 6/2, 6/4 | Final Integration Sprint | TA 演習 |
| 16 | 6/9, 6/11 | Final Demo Day (Tue.) | Final Demo Day (Thu.) |

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
