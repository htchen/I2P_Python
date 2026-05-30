# Automated Testing

Moving beyond manual `print()` debugging to write code that tests our code,
ensuring each component works both independently and together.

## Learning Objectives

- Explain why automated tests matter
- Distinguish unit tests from integration tests
- Write tests for API wrappers and the Flask app
- Mock external APIs so tests run fast and offline

## Why We Need Automated Tests

In previous weeks, we verified our code by running it and looking at the
console. In a web application, manual testing—clicking through the app,
entering addresses, checking the map—is too slow and error-prone.

Imagine repeating this after *every* change: open the browser, type a start,
type a destination, submit, inspect the map, then try a bad address... Tedious,
and easy to skip.

Automated tests let us catch bugs instantly, **before deployment**, applying
the exact same rigorous checks every single time.

> Going from "`print()` debugging" to "code that tests our code" is the single
> biggest step from hobby scripts to professional software engineering.

We will use [pytest](https://docs.pytest.org/):

```bash
pip install pytest
```

Run it from the project root—pytest automatically discovers every `test_*`
function inside a `tests/` folder:

```bash
pytest
```

## Unit Tests vs. Integration Tests

We implement two distinct levels of testing:

| Level | What it tests | Goal |
|-------|---------------|------|
| **Unit test** | A single function or module | Confirm each small piece works *on its own* |
| **Integration test** | How modules interact / the full flow | Confirm the pieces work *together* |

## A. Unit Tests (Testing Independently)

**Goal:** Test small, isolated pieces of logic (like a single function or our
new API wrappers) to ensure they work on their own.

### Example 1: Testing the Geocoding Wrapper

Does it correctly return `(40.7128, -74.0060)` when given "New York City"?

```python
# tests/test_geocoding.py
from unittest.mock import patch
from geocoding import GeocodingService


@patch("geocoding.requests.get")
def test_geocode_returns_coordinates(mock_get):
    # Pretend Nominatim responded (no real network call)
    mock_get.return_value.json.return_value = [
        {"lat": "40.7128", "lon": "-74.0060"}
    ]
    mock_get.return_value.raise_for_status.return_value = None

    result = GeocodingService().geocode("New York City")

    assert result == (40.7128, -74.0060)
```

### Example 2: Testing the `Place` Class

Does our `Place` class correctly instantiate and store its attributes?

```python
# tests/test_geocoding.py (continued)
from geocoding import Place


def test_place_stores_attributes():
    place = Place("Statue of Liberty", 40.6892, -74.0445)

    assert place.name == "Statue of Liberty"
    assert place.lat == 40.6892
    assert place.lon == -74.0445
```

## B. Integration Tests (Testing Together)

**Goal:** Test how different modules interact with each other and the complete
system flow.

### Example 1: The Full Flask Web Flow

Does submitting the HTML search form correctly trigger the geocoding wrapper,
pass the data along, and return a `200 OK` response with the results page?

```python
# tests/test_app.py
from unittest.mock import patch
from app import app


def test_index_page_loads():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


@patch("app.geocoder.geocode")
def test_search_returns_results_page(mock_geocode):
    # Mock the wrapper so we test the *flow*, not the network
    mock_geocode.return_value = (40.7128, -74.0060)

    client = app.test_client()
    response = client.post("/search", data={"address": "New York City"})

    assert response.status_code == 200
    assert b"results" in response.data.lower() or response.status_code == 200
```

### Example 2: Graceful Failure Testing

If the geocoding/routing API goes down (or an address isn't found), does the
app show our custom **error page** instead of crashing?

```python
# tests/test_app.py (continued)
@patch("app.geocoder.geocode")
def test_search_shows_error_page_on_failure(mock_geocode):
    # Simulate an API failure / no result
    mock_geocode.return_value = None

    client = app.test_client()
    response = client.post("/search", data={"address": "Nowhere-at-all"})

    # The app should NOT crash with a 500; it should render error.html
    assert response.status_code == 200
    assert b"not found" in response.data.lower()
```

## Best Practices for Testing External APIs

When writing unit tests for our API wrappers, we do **not** want to ping the
real Nominatim or OSRM servers every time we run our tests. Doing so:

- slows tests down,
- violates API rate limits, and
- makes tests fail whenever the external service is down—even if *our* code is
  perfect.

### Mocking

**Mocking** means simulating (faking) the HTTP response so our unit tests run
instantly and offline. We replace `requests.get` with a stand-in that returns
exactly the data we choose:

```python
@patch("geocoding.requests.get")
def test_geocode_returns_coordinates(mock_get):
    mock_get.return_value.json.return_value = [
        {"lat": "40.7128", "lon": "-74.0060"}
    ]
    ...
```

This way our internal code is verified perfectly, **regardless of the external
API's status**.

> **Remember:** unit tests check *our* code, not someone else's server. Mock
> the external dependency so tests stay fast, stable, and repeatable.

## Summary

Automated tests—unit tests for isolated logic and integration tests for the
full flow, with external APIs mocked—let us verify the Smart City Navigator
works correctly and catch bugs before they ever reach a user.
