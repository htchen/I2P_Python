# Week 12: Refactoring: OOP & Decorators

**Phase 3: Algorithms & Logic** — "Making Smart Decisions"

---

## Concepts
- Classes and Objects
- Methods and Attributes
- Decorators
- Code organization

---

## Project Task

Refactor the messy code into a `Place` class. Create a `@rate_limit` decorator to ensure your API calls sleep for 1 second between requests (crucial for OSM compliance).

### The Place Class

```python
class Place:
    def __init__(self, name, coords, rating=None, category=None):
        self.name = name
        self.coords = coords  # (latitude, longitude)
        self.rating = rating
        self.category = category

    @property
    def lat(self):
        return self.coords[0]

    @property
    def lon(self):
        return self.coords[1]

    def distance_to(self, other):
        """Calculate Haversine distance to another Place."""
        from math import radians, sin, cos, sqrt, asin
        R = 6371
        lat1, lon1 = radians(self.lat), radians(self.lon)
        lat2, lon2 = radians(other.lat), radians(other.lon)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        return R * 2 * asin(sqrt(a))

    def __repr__(self):
        return f"Place('{self.name}', {self.coords})"

    def to_dict(self):
        return {
            "name": self.name,
            "coords": list(self.coords),
            "rating": self.rating,
            "category": self.category
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            coords=tuple(data["coords"]),
            rating=data.get("rating"),
            category=data.get("category")
        )


# Usage
p1 = Place("Taipei 101", (25.0330, 121.5654), rating=4.7)
p2 = Place("Main Station", (25.0478, 121.5170))

print(p1.distance_to(p2))  # Distance in km
```

### The Rate Limit Decorator

```python
import time
from functools import wraps

def rate_limit(seconds=1):
    """
    Decorator that ensures a function waits between calls.
    Crucial for API compliance!
    """
    last_call = [0]  # Use list to allow modification in closure

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < seconds:
                time.sleep(seconds - elapsed)

            result = func(*args, **kwargs)
            last_call[0] = time.time()
            return result
        return wrapper
    return decorator


# Usage
@rate_limit(seconds=1)
def search_nominatim(query):
    """This function will automatically wait 1s between calls."""
    import requests
    headers = {"User-Agent": "CS101/1.0 (your-email@university.edu)"}
    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": query, "format": "json"},
        headers=headers
    )
    return response.json()


# These calls are automatically rate-limited
result1 = search_nominatim("taipei")  # Executes immediately
result2 = search_nominatim("tokyo")   # Waits 1 second first
result3 = search_nominatim("seoul")   # Waits 1 second first
```

---

## Lab Exercises

See the `labs/` folder for this week's exercises.

## Lecture Materials

See the `lectures/` folder for slides and examples.
