# Teaching Notes: Unit & Integration Tests

Instructor companion to **§3.2 "Testing the Application"** in
[`week15_lecture.md`](week15_lecture.md). For each test in
`tests/test_geocoding.py` (unit) and `tests/test_app.py` (integration) this
gives you *what it checks*, *the mechanics to walk through*, and *the teaching
point to land*. Teach straight from it.

---

## Framing first (put this on the board before any code)

| | Unit test (`test_geocoding.py`) | Integration test (`test_app.py`) |
|---|---|---|
| **Scope** | One class/function in isolation | Many modules wired together through Flask |
| **External world** | Mocked away (no real network) | Real Flask app, real routing/templates |
| **Question it answers** | "Does *this piece* do its job?" | "Do the pieces *fit together*?" |
| **When it breaks** | Bug is *inside that one unit* | Bug is in *how units connect* |

> **Slogan:** unit tests test the bricks; integration tests test the wall.

---

# Part 1 — Unit Tests (`tests/test_geocoding.py`)

## Shared setup

```python
import unittest
from unittest.mock import patch, Mock
import requests
from utils.geocoding import Geocoder, GeocodingError
from utils.places import Place, filter_by_walk_time, sort_by_duration
```

- **`unittest`** is built in — no install. Tests are *methods* named `test_*`
  inside a class that subclasses `unittest.TestCase`.
- **`patch` / `Mock`** are the mocking tools. Foreshadow: "so we never actually
  call the internet."
- The imports announce *what is under test*: the `Geocoder` wrapper, its
  `GeocodingError`, and the `Place` model + helpers.

```python
class TestGeocoder(unittest.TestCase):
    def setUp(self):
        self.geocoder = Geocoder(user_agent="TestAgent/1.0")
```

- **`setUp()` runs before *every* test method** — avoids repetition and gives
  each test a *fresh* object. Stress "fresh": tests must not leak state into
  each other.

---

## Unit Test 1 — `test_geocode_success` (happy path)

```python
@patch('utils.geocoding.requests.get')
def test_geocode_success(self, mock_get):
    mock_response = Mock()
    mock_response.json.return_value = [{
        "lat": "25.0330", "lon": "121.5654",
        "display_name": "Taipei 101, Xinyi District, Taipei"
    }]
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = self.geocoder.geocode("Taipei 101")

    self.assertEqual(result["lat"], 25.0330)
    self.assertEqual(result["lon"], 121.5654)
    self.assertIn("Taipei 101", result["display_name"])
```

**Checks:** given a normal Nominatim response, `geocode()` returns the right
coordinates.

**Mechanics — go slowly, this is the crux of mocking:**

1. **`@patch('utils.geocoding.requests.get')`** — for this test, replace
   `requests.get` *as seen inside `utils.geocoding`* with a fake, injected as
   `mock_get`.
   - **#1 thing students get wrong:** patch the name *where it is looked up*
     (`utils.geocoding.requests.get`), **not** where it's defined
     (`requests.get`). `geocoding.py` does `import requests` then calls
     `requests.get`, so the lookup is in the `geocoding` namespace.
2. **Build a fake `response`** to match what the real code touches —
   `response.raise_for_status()` then `response.json()`:
   - `mock_response.json.return_value = [...]` → `response.json()` yields our
     canned list.
   - `mock_response.raise_for_status = Mock()` → a do-nothing stand-in.
   - `mock_get.return_value = mock_response` → `requests.get(...)` returns it.
3. `result = self.geocoder.geocode(...)` runs the **real** wrapper logic; only
   the network call is intercepted.
4. **Assertions test real work:** Nominatim returns lat/lon as **strings**
   (`"25.0330"`); asserting `== 25.0330` (float) proves the wrapper did the
   `float()` conversion. `assertIn` = substring check.

**Teaching point:** a good unit test feeds a *known input* and checks the
*transformation* — here "string JSON → typed dict."

---

## Unit Test 2 — `test_geocode_not_found` (empty-result edge case)

```python
@patch('utils.geocoding.requests.get')
def test_geocode_not_found(self, mock_get):
    mock_response = Mock()
    mock_response.json.return_value = []        # Nominatim found nothing
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    with self.assertRaises(GeocodingError):
        self.geocoder.geocode("nonexistent place xyz123")
```

**Checks:** a *successful* response that is an **empty list** → wrapper raises
`GeocodingError`.

**Mechanics:**
- Only change from Test 1: `json.return_value = []`. This is **not** a network
  error — it's a valid HTTP 200 with no matches. Keep that distinction sharp.
- **`with self.assertRaises(GeocodingError):`** — passes *if* the block raises
  that exception, fails if it raises nothing or a different type. New idea for
  most students: "a test can assert that code *blows up* — and that's correct."

**Teaching point:** *error paths are behavior too.* Beginners test only the
happy case; pros test "what happens when there's no answer."

---

## Unit Test 3 — `test_geocode_api_error` (network failure)

```python
@patch('utils.geocoding.requests.get')
def test_geocode_api_error(self, mock_get):
    # A real failure from `requests` is always a RequestException subclass,
    # which is exactly what the wrapper catches. Mock that, not a bare
    # Exception, or the error would slip past the wrapper.
    mock_get.side_effect = requests.ConnectionError("Connection failed")

    with self.assertRaises(GeocodingError):
        self.geocoder.geocode("Taipei 101")
```

**Checks:** a network failure is caught and re-raised as the friendly
`GeocodingError`.

**Mechanics — `side_effect` vs `return_value`:**
- `return_value` → the mock *returns* a value when called.
- **`side_effect = <exception>`** → the mock *raises* it when called. So
  `requests.get(...)` now throws instead of returning.

**Best real-world moment (we hit this bug live):**
- `requests.ConnectionError` **is a subclass of** `requests.RequestException`.
- The wrapper does `except requests.RequestException`.
- So it's caught → re-raised as `GeocodingError` → test passes.
- Mock a bare `Exception("...")` instead and it is **not** a `RequestException`
  → slips past the `except` → test fails with the raw `Exception`.

**Teaching point:** *mock the exception type your code is actually designed to
handle.* A "wrong" mock gives a misleading failure.

---

## Unit Test 4 — `test_get_route_success` (same pattern, different module)

```python
class TestRouter(unittest.TestCase):
    @patch('utils.routing.requests.get')
    def test_get_route_success(self, mock_get):
        from utils.routing import Router
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "Ok",
            "routes": [{
                "distance": 1000, "duration": 720,
                "geometry": {"coordinates": [[121.565, 25.033], [121.555, 25.040]]}
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        router = Router()
        result = router.get_route((25.033, 121.565), (25.040, 121.555))

        self.assertEqual(result["distance"], 1000)
        self.assertEqual(result["duration"], 720)
```

**Checks:** the OSRM wrapper extracts distance/duration from OSRM's nested shape.

**Reinforce, don't re-teach** — it's the *same recipe* as Test 1:
- Patch the **right namespace** (`utils.routing`, different from `geocoding`).
- The mock JSON mirrors **OSRM's real nested structure** (`routes[0].distance`);
  the wrapper digs through `data["routes"][0]` — the test proves that works.
- A separate `TestRouter` class — **one class per unit** is a clean convention.

**Teaching point:** once students see the pattern reused across two APIs,
mocking stops being magic and becomes routine.

---

## Unit Tests 5–7 — `TestPlace` (the "no mocking needed" contrast)

```python
class TestPlace(unittest.TestCase):
    def test_stores_attributes(self):
        place = Place("Taipei 101", 25.0330, 121.5654, place_type="attraction")
        self.assertEqual(place.name, "Taipei 101")
        self.assertEqual(place.lat, 25.0330)
        self.assertEqual(place.lon, 121.5654)
        self.assertEqual(place.type, "attraction")
```

**Checks:** the constructor stores what it's given. Trivial — *that's the point.*

**Teaching point:** **pure logic needs no mocking.** `Place` has no network, no
files, no clock → the test is just "make one, check attributes." Contrast with
the `Geocoder` tests: *the amount of test scaffolding is a smell test for how
coupled your code is to the outside world.* Pure classes are easiest to test —
an argument for the modular design from Hour 1.

```python
    def test_has_route(self):
        no_route = Place("A", 25.0, 121.0)
        routed = Place("B", 25.1, 121.1, duration_min=5.0, route_geometry=[[25.0, 121.0]])
        self.assertFalse(no_route.has_route())
        self.assertTrue(routed.has_route())
```

**Checks:** `has_route()` is `False` before routing, `True` after.

**Teaching points:** **test both branches** of a boolean method —
`assertFalse` *and* `assertTrue`. A half-step up from attribute checks: this is
*method behavior*.

```python
    def test_helpers_filter_and_sort(self):
        places = [
            Place("Far", 25.0, 121.0, duration_min=20.0),
            Place("Near", 25.1, 121.1, duration_min=3.0),
            Place("Mid", 25.2, 121.2, duration_min=8.0),
        ]
        within_10 = filter_by_walk_time(places, 10)
        self.assertEqual({p.name for p in within_10}, {"Near", "Mid"})

        ordered = sort_by_duration(places)
        self.assertEqual([p.name for p in ordered], ["Near", "Mid", "Far"])
```

**Checks:** the two business-logic helpers filter and order correctly.

**Mechanics — a deliberate, subtle detail:**
- Input is intentionally **out of order** (20, 3, 8). Good test data is chosen
  to *expose* bugs; already-sorted data could let a broken sort "pass."
- **Filter → compare as a `set`** (`{"Near", "Mid"}`): we care about
  *membership*, not order.
- **Sort → compare as a `list`** (`["Near", "Mid", "Far"]`): order *is* the
  point.

**Teaching point (a gem):** *choose the assertion's data structure to match
what you care about.* Set = "what's present." List = "in what order."

---

# Part 2 — Integration Tests (`tests/test_app.py`)

```python
import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
```

**The conceptual jump — make it explicit:**
- `from app import app` imports the **whole real application** (which imports
  geocoder, router, places, mapping, config). **No mocking** — we test the
  assembled system.
- **`app.config["TESTING"] = True`** turns on Flask's testing mode.
- **`app.test_client()`** is the star: a fake browser that sends HTTP requests
  to your routes **without starting a server or opening a port** — in-process
  and instant.

**Teaching point:** integration tests exercise the
request → route → logic → template → response pipeline.

---

## Integration Test 1 — `test_index_page`

```python
def test_index_page(self):
    response = self.client.get("/")
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"Smart City Navigator", response.data)
```

**Checks:** `GET /` returns `200` and the HTML contains our title.

**Mechanics:**
- `response.status_code` — `200` = success.
- `response.data` — the **raw body as bytes**, hence the **`b"..."`** literal
  (students forget the `b` and get a type error — flag it).
- `assertIn` confirms the template rendered with real content.

**Teaching point:** one assertion, many moving parts (routing, view function,
Jinja rendering, HTML) — *that breadth* is what makes it integration.

---

## Integration Test 2 — `test_search_without_location`

```python
def test_search_without_location(self):
    response = self.client.post("/search", data={})
    self.assertEqual(response.status_code, 302)  # Redirect
```

**Checks:** posting the form with **no data** doesn't crash — it redirects back
to the form (with a flashed error).

**Mechanics:**
- **`.post("/search", data={})`** — a form submission with an empty payload
  (contrast the earlier GETs).
- **`302`** = redirect. The app's logic: missing location → `flash(...)` +
  `redirect(url_for("index"))`, so 302 is the *designed* behavior, not 200.

**Teaching point:** integration tests verify the app's **contract for bad
input**. Empty input is normal; the app should guide, not 500. Good moment for
HTTP status families: 2xx success, 3xx redirect, 4xx client error, 5xx server.

---

## Integration Test 3 — `test_health_check`

```python
def test_health_check(self):
    response = self.client.get("/health")
    self.assertEqual(response.status_code, 200)
    data = response.get_json()
    self.assertEqual(data["status"], "healthy")
```

**Checks:** the `/health` endpoint returns `200` and JSON `{"status": "healthy"}`.

**Mechanics:**
- **`response.get_json()`** parses the body into a dict — use this for JSON/API
  endpoints; use `response.data` (bytes) for HTML pages.

**Teaching point:** health-check endpoints are real ops practice (load
balancers/monitors ping `/health`). This is also the test that **failed until
`/health` was actually added to `app.py`** — a live example of an integration
test catching a *missing feature*, not a logic bug.

---

## Integration Test 4 — `test_404_page`

```python
def test_404_page(self):
    response = self.client.get("/nonexistent")
    self.assertEqual(response.status_code, 404)
```

**Checks:** an unknown URL returns `404 Not Found`.

**Teaching point:** confirms graceful handling of unknown routes (and, with the
custom handler, would render `error.html`). Contrast: 302 (Test 2) = "understood
but redirected"; 404 = "that page doesn't exist."

---

# Putting it together (the payoff line)

What each layer would and wouldn't catch:

- **A bug in `Geocoder`'s string→float conversion** → caught by the **unit
  test**, pinpointed to one method. (Integration might catch it but couldn't
  tell you *where*.)
- **Forgetting to register the `/health` route** → **all unit tests still
  pass** (the function is fine), but the **integration test fails** — the bug is
  in *wiring*, not in any single unit. (Exactly what happened in class.)

> **The whole lesson in one sentence:** unit tests tell you *which brick* is
> cracked; integration tests tell you *the wall* doesn't stand up. You need
> both.

---

## Suggested classroom flow (optional)

1. Run `pytest -v` once so students see all tests pass (fast — network mocked).
2. **Break something on purpose** and re-run, to feel which layer catches it:
   - Change `float(result["lat"])` → `result["lat"]` in `geocoding.py`
     → `test_geocode_success` fails (unit catches a logic bug).
   - Comment out the `/health` route in `app.py`
     → `test_health_check` fails (integration catches a wiring bug).
3. Fix each, re-run, watch green return. Reinforces: *a failing test is the
   tool doing its job.*
