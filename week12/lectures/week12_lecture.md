# Week 12: Refactoring with OOP & Decorators

## Lecture Overview (3 Hours)

**Phase 3: Algorithms & Logic** — "Making Smart Decisions"

### Learning Objectives
By the end of this lecture, students will be able to:
1. Understand the principles of Object-Oriented Programming (OOP)
2. Create classes with attributes, methods, and properties
3. Use special methods (`__init__`, `__repr__`, `__str__`, etc.)
4. Understand and create decorators for cross-cutting concerns
5. Refactor procedural code into well-organized classes
6. Implement a `Place` class for our Smart City Navigator
7. Create a `@rate_limit` decorator for API compliance

### Prerequisites
- Week 9: Functional Patterns (functions as first-class objects)
- Week 10: TSP (understanding of place data structures)
- Basic understanding of functions and closures

---

# Hour 1: Introduction to Object-Oriented Programming

## 1.1 Why OOP?

### The Problem with Procedural Code

As programs grow, procedural code becomes hard to manage:

```python
# Procedural approach - data and functions are separate
place1_name = "Pizza Palace"
place1_lat = 25.033
place1_lon = 121.565
place1_rating = 4.5

place2_name = "Burger Barn"
place2_lat = 25.038
place2_lon = 121.568
place2_rating = 4.2

def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula...
    pass

def format_place(name, lat, lon, rating):
    return f"{name} ({rating}★) at ({lat}, {lon})"

# Problem: Easy to mix up arguments!
dist = calculate_distance(place1_lat, place1_lon, place2_lon, place2_lat)  # Bug!
```

### The OOP Solution

OOP bundles data and behavior together:

```python
# OOP approach - data and methods are bundled
class Place:
    def __init__(self, name, lat, lon, rating):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.rating = rating

    def distance_to(self, other):
        # Haversine formula using self.lat, self.lon, etc.
        pass

    def format(self):
        return f"{self.name} ({self.rating}★) at ({self.lat}, {self.lon})"

# Usage - much clearer!
place1 = Place("Pizza Palace", 25.033, 121.565, 4.5)
place2 = Place("Burger Barn", 25.038, 121.568, 4.2)

dist = place1.distance_to(place2)  # Can't mix up arguments!
print(place1.format())
```

### Core OOP Concepts

```
┌─────────────────────────────────────────────────────────────────┐
│                    Object-Oriented Programming                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CLASS: A blueprint/template for creating objects               │
│  ┌─────────────────────────────────────┐                       │
│  │ class Place:                         │                       │
│  │   - attributes (data)                │                       │
│  │   - methods (behavior)               │                       │
│  └─────────────────────────────────────┘                       │
│                    │                                            │
│                    │ creates                                    │
│                    ▼                                            │
│  OBJECTS: Instances of a class                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │ place1   │  │ place2   │  │ place3   │                      │
│  │ Pizza    │  │ Burger   │  │ Taco     │                      │
│  └──────────┘  └──────────┘  └──────────┘                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1.2 Creating Classes

### Basic Class Syntax

```python
class Place:
    """A class representing a location/place."""

    def __init__(self, name, coords, rating=None):
        """
        Initialize a Place.

        Args:
            name: Name of the place
            coords: Tuple of (latitude, longitude)
            rating: Optional rating (0-5 stars)
        """
        self.name = name
        self.coords = coords
        self.rating = rating

# Creating instances (objects)
p1 = Place("Pizza Palace", (25.033, 121.565), 4.5)
p2 = Place("Burger Barn", (25.038, 121.568))  # rating defaults to None

# Accessing attributes
print(p1.name)      # "Pizza Palace"
print(p1.coords)    # (25.033, 121.565)
print(p1.rating)    # 4.5
print(p2.rating)    # None
```

### Understanding `self`

`self` refers to the current instance:

```python
class Place:
    def __init__(self, name):
        self.name = name  # self.name is the INSTANCE attribute

    def greet(self):
        # self refers to the specific instance calling this method
        return f"Welcome to {self.name}!"

p1 = Place("Pizza Palace")
p2 = Place("Burger Barn")

print(p1.greet())  # "Welcome to Pizza Palace!"
print(p2.greet())  # "Welcome to Burger Barn!"

# Behind the scenes, Python does:
# Place.greet(p1) -> "Welcome to Pizza Palace!"
# Place.greet(p2) -> "Welcome to Burger Barn!"
```

### Instance vs Class Attributes

```python
class Place:
    # Class attribute - shared by ALL instances
    planet = "Earth"
    instance_count = 0

    def __init__(self, name, coords):
        # Instance attributes - unique to EACH instance
        self.name = name
        self.coords = coords

        # Increment class attribute
        Place.instance_count += 1

# All instances share class attributes
p1 = Place("Pizza", (25.0, 121.0))
p2 = Place("Burger", (25.1, 121.1))

print(p1.planet)          # "Earth"
print(p2.planet)          # "Earth"
print(Place.planet)       # "Earth"
print(Place.instance_count)  # 2

# Instance attributes are unique
print(p1.name)  # "Pizza"
print(p2.name)  # "Burger"
```

---

## 1.3 Methods

### Instance Methods

Regular methods that operate on instance data:

```python
import math

class Place:
    def __init__(self, name, coords, rating=None):
        self.name = name
        self.coords = coords
        self.rating = rating

    def distance_to(self, other):
        """Calculate distance to another Place in km."""
        lat1, lon1 = math.radians(self.coords[0]), math.radians(self.coords[1])
        lat2, lon2 = math.radians(other.coords[0]), math.radians(other.coords[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))

        return 6371 * c  # Earth's radius in km

    def is_highly_rated(self, threshold=4.0):
        """Check if place is highly rated."""
        return self.rating is not None and self.rating >= threshold

# Usage
p1 = Place("Taipei 101", (25.0330, 121.5654), 4.7)
p2 = Place("Main Station", (25.0478, 121.5170), 4.2)

print(f"Distance: {p1.distance_to(p2):.2f} km")
print(f"Highly rated: {p1.is_highly_rated()}")  # True
```

### Class Methods

Methods that operate on the class itself:

```python
class Place:
    all_places = []  # Class attribute to track all instances

    def __init__(self, name, coords, rating=None):
        self.name = name
        self.coords = coords
        self.rating = rating
        Place.all_places.append(self)

    @classmethod
    def from_dict(cls, data):
        """Create a Place from a dictionary."""
        return cls(
            name=data["name"],
            coords=tuple(data["coords"]),
            rating=data.get("rating")
        )

    @classmethod
    def get_all(cls):
        """Get all Place instances."""
        return cls.all_places

    @classmethod
    def clear_all(cls):
        """Clear all Place instances."""
        cls.all_places = []

# Usage
data = {"name": "Pizza Palace", "coords": [25.033, 121.565], "rating": 4.5}
place = Place.from_dict(data)  # Create from dictionary

print(Place.get_all())  # List of all places
```

### Static Methods

Methods that don't need instance or class:

```python
class Place:
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        """Calculate haversine distance between two points."""
        import math
        R = 6371

        lat1, lat2 = math.radians(lat1), math.radians(lat2)
        dlat = lat2 - lat1
        dlon = math.radians(lon2 - lon1)

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))

    def distance_to(self, other):
        """Use static method for calculation."""
        return Place.haversine(
            self.coords[0], self.coords[1],
            other.coords[0], other.coords[1]
        )

# Static method can be called without an instance
dist = Place.haversine(25.033, 121.565, 25.038, 121.568)
```

---

## 1.4 Properties

### The `@property` Decorator

Properties provide controlled access to attributes:

```python
class Place:
    def __init__(self, name, coords, rating=None):
        self.name = name
        self.coords = coords
        self._rating = rating  # Private by convention (underscore prefix)

    @property
    def lat(self):
        """Get latitude from coords."""
        return self.coords[0]

    @property
    def lon(self):
        """Get longitude from coords."""
        return self.coords[1]

    @property
    def rating(self):
        """Get rating."""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Set rating with validation."""
        if value is not None and not (0 <= value <= 5):
            raise ValueError("Rating must be between 0 and 5")
        self._rating = value

# Usage
place = Place("Pizza", (25.033, 121.565), 4.5)

# Access like attributes (not method calls!)
print(place.lat)     # 25.033
print(place.lon)     # 121.565
print(place.rating)  # 4.5

# Setter validates input
place.rating = 4.8   # OK
# place.rating = 6.0  # Raises ValueError!
```

### Computed Properties

Properties can compute values on the fly:

```python
class Place:
    def __init__(self, name, coords, rating=None, review_count=0):
        self.name = name
        self.coords = coords
        self.rating = rating
        self.review_count = review_count

    @property
    def popularity_score(self):
        """Compute popularity based on rating and reviews."""
        if self.rating is None:
            return 0
        return self.rating * min(self.review_count / 100, 1.0)

    @property
    def coords_str(self):
        """Format coordinates as string."""
        return f"({self.coords[0]:.4f}, {self.coords[1]:.4f})"

# Usage
place = Place("Pizza", (25.033, 121.565), 4.5, review_count=150)
print(place.popularity_score)  # 4.5 (rating * 1.0)
print(place.coords_str)        # "(25.0330, 121.5650)"
```

---

# Hour 2: Special Methods and Decorators

## 2.1 Special (Dunder) Methods

### Common Special Methods

Python uses special methods (with double underscores) for built-in operations:

```python
class Place:
    def __init__(self, name, coords, rating=None):
        self.name = name
        self.coords = coords
        self.rating = rating

    def __repr__(self):
        """Developer-friendly representation."""
        return f"Place('{self.name}', {self.coords}, rating={self.rating})"

    def __str__(self):
        """User-friendly string."""
        stars = f" ({self.rating}★)" if self.rating else ""
        return f"{self.name}{stars}"

    def __eq__(self, other):
        """Check equality based on name and coords."""
        if not isinstance(other, Place):
            return False
        return self.name == other.name and self.coords == other.coords

    def __hash__(self):
        """Make Place hashable (for use in sets/dicts)."""
        return hash((self.name, self.coords))

    def __lt__(self, other):
        """Less than - for sorting by rating."""
        if self.rating is None:
            return True
        if other.rating is None:
            return False
        return self.rating < other.rating

# Usage
p1 = Place("Pizza", (25.033, 121.565), 4.5)
p2 = Place("Burger", (25.038, 121.568), 4.2)

print(repr(p1))  # Place('Pizza', (25.033, 121.565), rating=4.5)
print(str(p1))   # Pizza (4.5★)

# Equality
p3 = Place("Pizza", (25.033, 121.565), 4.8)  # Same name/coords, diff rating
print(p1 == p3)  # True (based on name and coords)

# Sorting
places = [p1, p2]
sorted_places = sorted(places, reverse=True)  # Uses __lt__
print([str(p) for p in sorted_places])  # ['Pizza (4.5★)', 'Burger (4.2★)']

# Use in sets
place_set = {p1, p2, p3}
print(len(place_set))  # 2 (p1 and p3 are equal)
```

### Container-Like Behavior

```python
class PlaceCollection:
    """A collection of places with list-like behavior."""

    def __init__(self):
        self._places = []

    def add(self, place):
        self._places.append(place)

    def __len__(self):
        """Support len()."""
        return len(self._places)

    def __getitem__(self, index):
        """Support indexing: collection[0]."""
        return self._places[index]

    def __iter__(self):
        """Support iteration: for place in collection."""
        return iter(self._places)

    def __contains__(self, place):
        """Support 'in' operator."""
        return place in self._places

# Usage
collection = PlaceCollection()
collection.add(Place("Pizza", (25.0, 121.0)))
collection.add(Place("Burger", (25.1, 121.1)))

print(len(collection))     # 2
print(collection[0].name)  # "Pizza"

for place in collection:
    print(place.name)

pizza = Place("Pizza", (25.0, 121.0))
print(pizza in collection)  # True (if __eq__ matches)
```

---

## 2.2 Introduction to Decorators

### What is a Decorator?

A **decorator** is a function that wraps another function to extend its behavior:

```
┌─────────────────────────────────────────────────────────────────┐
│                         Decorator Pattern                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Original Function          Decorated Function                 │
│   ┌─────────────┐           ┌─────────────────────────┐        │
│   │             │           │  ┌─────────────────┐    │        │
│   │   func()    │    =>     │  │  Before logic   │    │        │
│   │             │           │  ├─────────────────┤    │        │
│   └─────────────┘           │  │    func()       │    │        │
│                             │  ├─────────────────┤    │        │
│                             │  │  After logic    │    │        │
│                             │  └─────────────────┘    │        │
│                             └─────────────────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Basic Decorator

```python
def my_decorator(func):
    """A simple decorator."""
    def wrapper(*args, **kwargs):
        print(f"Before calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After calling {func.__name__}")
        return result
    return wrapper

# Using the decorator
@my_decorator
def greet(name):
    print(f"Hello, {name}!")
    return f"Greeted {name}"

# When we call greet(), it's actually calling wrapper()
result = greet("Alice")
# Output:
# Before calling greet
# Hello, Alice!
# After calling greet

# The @ syntax is equivalent to:
# greet = my_decorator(greet)
```

### Preserving Function Metadata

Use `functools.wraps` to preserve the original function's metadata:

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # Preserves __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        """Wrapper function."""
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greet someone by name."""
    return f"Hello, {name}!"

# With @wraps
print(greet.__name__)  # "greet" (not "wrapper")
print(greet.__doc__)   # "Greet someone by name."
```

---

## 2.3 Practical Decorators

### Timing Decorator

```python
import time
from functools import wraps

def timer(func):
    """Measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done!"

result = slow_function()
# Output: slow_function took 1.0012 seconds
```

### Logging Decorator

```python
from functools import wraps
import logging

logging.basicConfig(level=logging.INFO)

def log_calls(func):
    """Log function calls with arguments."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_str = ", ".join(repr(a) for a in args)
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))

        logging.info(f"Calling {func.__name__}({all_args})")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned {result!r}")

        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

result = add(2, 3)
# INFO:root:Calling add(2, 3)
# INFO:root:add returned 5
```

### Retry Decorator

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    """Retry a function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)

            raise last_exception

        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unreliable_api_call():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network error")
    return "Success!"

# Will retry up to 3 times
result = unreliable_api_call()
```

---

## 2.4 The Rate Limit Decorator

### Why Rate Limiting?

APIs like Nominatim require rate limiting to prevent abuse:

```
Without Rate Limiting:
  Request 1 ─────> Server ─────> Response
  Request 2 ─────> Server ─────> 429 Too Many Requests!
  Request 3 ─────> Server ─────> BANNED!

With Rate Limiting:
  Request 1 ─────> Server ─────> Response
       │
       │ wait 1 second
       ▼
  Request 2 ─────> Server ─────> Response
       │
       │ wait 1 second
       ▼
  Request 3 ─────> Server ─────> Response
```

### Implementing Rate Limit

```python
import time
from functools import wraps

def rate_limit(seconds=1.0):
    """
    Decorator that ensures minimum time between function calls.

    Args:
        seconds: Minimum seconds between calls (default 1.0)
    """
    last_call_time = [0.0]  # Use list to allow modification in closure

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Calculate time since last call
            elapsed = time.time() - last_call_time[0]

            # If not enough time has passed, wait
            if elapsed < seconds:
                wait_time = seconds - elapsed
                print(f"Rate limiting: waiting {wait_time:.2f}s...")
                time.sleep(wait_time)

            # Execute the function
            result = func(*args, **kwargs)

            # Record this call time
            last_call_time[0] = time.time()

            return result

        return wrapper
    return decorator


# Example usage
@rate_limit(seconds=1.0)
def search_api(query):
    """Simulated API call."""
    print(f"Searching for: {query}")
    return {"results": [query]}


# These calls are automatically rate-limited
result1 = search_api("pizza")   # Immediate
result2 = search_api("burger")  # Waits ~1 second
result3 = search_api("taco")    # Waits ~1 second
```

### Rate Limit with Instance Tracking

```python
import time
from functools import wraps

class RateLimiter:
    """Rate limiter that can be shared across functions."""

    def __init__(self, calls_per_second=1.0):
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0.0

    def wait_if_needed(self):
        """Wait if necessary to respect rate limit."""
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()

    def __call__(self, func):
        """Use as decorator."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.wait_if_needed()
            return func(*args, **kwargs)
        return wrapper


# Create a shared rate limiter for Nominatim
nominatim_limiter = RateLimiter(calls_per_second=1)

@nominatim_limiter
def search_place(query):
    print(f"Searching: {query}")
    return query

@nominatim_limiter
def geocode_address(address):
    print(f"Geocoding: {address}")
    return address

# Both functions share the same rate limiter
search_place("pizza")      # Immediate
geocode_address("taipei")  # Waits 1 second
search_place("burger")     # Waits 1 second
```

---

# Hour 3: Refactoring and Code Organization

## 3.1 The Complete Place Class

### Full Implementation

```python
from math import radians, sin, cos, sqrt, asin
from typing import Optional, Tuple, Dict, Any, List


class Place:
    """
    A class representing a location/place in the Smart City Navigator.

    Attributes:
        name: Name of the place
        coords: Tuple of (latitude, longitude)
        rating: Rating from 0-5 (optional)
        category: Category like 'restaurant', 'cafe' (optional)
    """

    def __init__(
        self,
        name: str,
        coords: Tuple[float, float],
        rating: Optional[float] = None,
        category: Optional[str] = None
    ):
        """
        Initialize a Place.

        Args:
            name: Name of the place
            coords: Tuple of (latitude, longitude)
            rating: Optional rating (0-5)
            category: Optional category string
        """
        self.name = name
        self.coords = coords
        self._rating = None
        self.rating = rating  # Use setter for validation
        self.category = category

    # === Properties ===

    @property
    def lat(self) -> float:
        """Latitude coordinate."""
        return self.coords[0]

    @property
    def lon(self) -> float:
        """Longitude coordinate."""
        return self.coords[1]

    @property
    def rating(self) -> Optional[float]:
        """Place rating (0-5)."""
        return self._rating

    @rating.setter
    def rating(self, value: Optional[float]) -> None:
        """Set rating with validation."""
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Rating must be a number")
            if not 0 <= value <= 5:
                raise ValueError("Rating must be between 0 and 5")
        self._rating = value

    # === Instance Methods ===

    def distance_to(self, other: 'Place') -> float:
        """
        Calculate Haversine distance to another Place.

        Args:
            other: Another Place object

        Returns:
            Distance in kilometers
        """
        R = 6371  # Earth's radius in km

        lat1, lon1 = radians(self.lat), radians(self.lon)
        lat2, lon2 = radians(other.lat), radians(other.lon)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))

        return R * c

    def walking_time_to(self, other: 'Place', speed_kmh: float = 5.0) -> float:
        """
        Calculate walking time to another Place.

        Args:
            other: Another Place object
            speed_kmh: Walking speed in km/h (default 5.0)

        Returns:
            Walking time in minutes
        """
        distance = self.distance_to(other)
        return (distance / speed_kmh) * 60

    def to_dict(self) -> Dict[str, Any]:
        """Convert Place to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "coords": list(self.coords),
            "rating": self.rating,
            "category": self.category
        }

    # === Class Methods ===

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Place':
        """
        Create a Place from a dictionary.

        Args:
            data: Dictionary with place data

        Returns:
            New Place instance
        """
        return cls(
            name=data["name"],
            coords=tuple(data["coords"]),
            rating=data.get("rating"),
            category=data.get("category")
        )

    @classmethod
    def from_nominatim(cls, data: Dict[str, Any]) -> 'Place':
        """
        Create a Place from Nominatim API response.

        Args:
            data: Nominatim search result

        Returns:
            New Place instance
        """
        return cls(
            name=data.get("display_name", "Unknown"),
            coords=(float(data["lat"]), float(data["lon"])),
            category=data.get("type")
        )

    # === Special Methods ===

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Place('{self.name}', {self.coords}, rating={self.rating})"

    def __str__(self) -> str:
        """User-friendly string."""
        parts = [self.name]
        if self.rating is not None:
            parts.append(f"({self.rating}★)")
        if self.category:
            parts.append(f"[{self.category}]")
        return " ".join(parts)

    def __eq__(self, other: object) -> bool:
        """Check equality based on name and coordinates."""
        if not isinstance(other, Place):
            return NotImplemented
        return self.name == other.name and self.coords == other.coords

    def __hash__(self) -> int:
        """Make Place hashable."""
        return hash((self.name, self.coords))

    def __lt__(self, other: 'Place') -> bool:
        """Compare by rating for sorting."""
        if self.rating is None:
            return True
        if other.rating is None:
            return False
        return self.rating < other.rating


# === Usage Examples ===

if __name__ == "__main__":
    # Create places
    taipei101 = Place("Taipei 101", (25.0330, 121.5654), rating=4.7, category="landmark")
    station = Place("Main Station", (25.0478, 121.5170), rating=4.2, category="transport")

    # Use properties
    print(f"Taipei 101 is at ({taipei101.lat}, {taipei101.lon})")

    # Calculate distance
    dist = taipei101.distance_to(station)
    print(f"Distance: {dist:.2f} km")

    # Walking time
    time_min = taipei101.walking_time_to(station)
    print(f"Walking time: {time_min:.1f} minutes")

    # Convert to/from dict
    data = taipei101.to_dict()
    print(f"As dict: {data}")

    restored = Place.from_dict(data)
    print(f"Restored: {restored}")

    # Sorting
    places = [taipei101, station]
    sorted_places = sorted(places, reverse=True)
    print(f"Sorted: {[str(p) for p in sorted_places]}")
```

---

## 3.2 Refactoring Example: Before and After

### Before: Procedural Code

```python
# Before refactoring - messy procedural code
import requests
import time
import json

# Global state
places_data = []
last_api_call = 0

def search_place(query):
    global last_api_call

    # Manual rate limiting
    elapsed = time.time() - last_api_call
    if elapsed < 1:
        time.sleep(1 - elapsed)

    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": query, "format": "json"},
        headers={"User-Agent": "Test/1.0"}
    )
    last_api_call = time.time()

    return response.json()

def add_place(name, lat, lon, rating=None, category=None):
    global places_data
    places_data.append({
        "name": name,
        "lat": lat,
        "lon": lon,
        "rating": rating,
        "category": category
    })

def get_distance(place1, place2):
    # Haversine formula with raw dict access
    import math
    lat1, lon1 = math.radians(place1["lat"]), math.radians(place1["lon"])
    lat2, lon2 = math.radians(place2["lat"]), math.radians(place2["lon"])
    # ... calculation ...
    pass

def filter_by_rating(places, min_rating):
    return [p for p in places if p.get("rating", 0) >= min_rating]

def sort_by_rating(places):
    return sorted(places, key=lambda p: p.get("rating", 0), reverse=True)
```

### After: OOP with Decorators

```python
# After refactoring - clean OOP code
import requests
import time
from functools import wraps
from typing import List, Optional
from dataclasses import dataclass


def rate_limit(seconds: float = 1.0):
    """Rate limiting decorator."""
    last_call = [0.0]

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


class Place:
    """Represents a location."""

    def __init__(self, name: str, coords: tuple, rating: float = None, category: str = None):
        self.name = name
        self.coords = coords
        self.rating = rating
        self.category = category

    @property
    def lat(self): return self.coords[0]

    @property
    def lon(self): return self.coords[1]

    def distance_to(self, other: 'Place') -> float:
        """Calculate distance using Haversine formula."""
        import math
        R = 6371
        lat1, lon1 = math.radians(self.lat), math.radians(self.lon)
        lat2, lon2 = math.radians(other.lat), math.radians(other.lon)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))


class PlaceService:
    """Service for managing places."""

    def __init__(self):
        self.places: List[Place] = []

    def add(self, place: Place) -> None:
        self.places.append(place)

    def filter_by_rating(self, min_rating: float) -> List[Place]:
        return [p for p in self.places if p.rating and p.rating >= min_rating]

    def sort_by_rating(self, descending: bool = True) -> List[Place]:
        return sorted(self.places, reverse=descending)


class NominatimClient:
    """Client for Nominatim API with automatic rate limiting."""

    BASE_URL = "https://nominatim.openstreetmap.org"

    def __init__(self, user_agent: str):
        self.user_agent = user_agent

    @rate_limit(seconds=1.0)
    def search(self, query: str) -> List[Place]:
        """Search for places."""
        response = requests.get(
            f"{self.BASE_URL}/search",
            params={"q": query, "format": "json"},
            headers={"User-Agent": self.user_agent}
        )
        response.raise_for_status()

        return [
            Place(
                name=item.get("display_name", "Unknown"),
                coords=(float(item["lat"]), float(item["lon"])),
                category=item.get("type")
            )
            for item in response.json()
        ]


# Usage is now clean and organized
client = NominatimClient("MyApp/1.0 (email@example.com)")
service = PlaceService()

# Search is automatically rate-limited
results = client.search("taipei pizza")
for place in results[:3]:
    service.add(place)

# Work with places using clean interface
top_places = service.sort_by_rating()
```

---

## 3.3 Dataclasses (Python 3.7+)

### Simplifying Class Definitions

```python
from dataclasses import dataclass, field
from typing import Optional, Tuple
import math


@dataclass
class Place:
    """A place using dataclass for automatic boilerplate."""

    name: str
    coords: Tuple[float, float]
    rating: Optional[float] = None
    category: Optional[str] = None

    # __init__, __repr__, __eq__ are auto-generated!

    @property
    def lat(self) -> float:
        return self.coords[0]

    @property
    def lon(self) -> float:
        return self.coords[1]

    def distance_to(self, other: 'Place') -> float:
        R = 6371
        lat1, lon1 = math.radians(self.lat), math.radians(self.lon)
        lat2, lon2 = math.radians(other.lat), math.radians(other.lon)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))


# Usage
p1 = Place("Pizza", (25.0, 121.0), rating=4.5)
p2 = Place("Pizza", (25.0, 121.0), rating=4.5)

print(p1)          # Place(name='Pizza', coords=(25.0, 121.0), rating=4.5, category=None)
print(p1 == p2)    # True (auto-generated __eq__)
```

### Dataclass Options

```python
from dataclasses import dataclass, field


@dataclass(frozen=True)  # Immutable
class ImmutablePlace:
    name: str
    coords: tuple


@dataclass(order=True)  # Auto-generate comparison methods
class RankedPlace:
    rating: float  # First field is used for comparison
    name: str = field(compare=False)  # Exclude from comparison
    coords: tuple = field(compare=False)


# Frozen dataclass can be used as dict key
place = ImmutablePlace("Pizza", (25.0, 121.0))
place_dict = {place: "favorite"}

# Ranked places can be sorted
places = [
    RankedPlace(4.5, "Pizza", (25.0, 121.0)),
    RankedPlace(4.8, "Burger", (25.1, 121.1)),
    RankedPlace(4.2, "Taco", (25.2, 121.2)),
]
sorted_places = sorted(places, reverse=True)
```

---

## 3.4 Summary

### Key Concepts

| Concept | Description | Example |
|---------|-------------|---------|
| **Class** | Blueprint for objects | `class Place:` |
| **`__init__`** | Constructor/initializer | `def __init__(self, name):` |
| **Instance Attribute** | Data unique to each object | `self.name = name` |
| **Instance Method** | Function operating on instance | `def distance_to(self, other):` |
| **Property** | Computed/validated attribute | `@property def lat(self):` |
| **Class Method** | Method on the class itself | `@classmethod def from_dict(cls, data):` |
| **Static Method** | Utility method | `@staticmethod def haversine(...):` |
| **Decorator** | Function wrapper | `@rate_limit(seconds=1)` |

### OOP Benefits

```
✓ Encapsulation: Data and behavior together
✓ Abstraction: Hide implementation details
✓ Reusability: Classes can be reused
✓ Organization: Clear code structure
✓ Type Safety: Better IDE support and documentation
```

### Decorator Use Cases

```python
# Timing
@timer
def slow_function(): ...

# Logging
@log_calls
def api_function(): ...

# Rate Limiting
@rate_limit(seconds=1)
def nominatim_search(): ...

# Caching
@lru_cache(maxsize=100)
def expensive_calculation(): ...

# Retry
@retry(max_attempts=3)
def flaky_network_call(): ...
```

---

## Next Week Preview

**Week 13: Introduction to Flask (Web Server)**
- Creating web servers with Flask
- Routes and URL handling
- Templates with Jinja2
- Serving our Smart City Navigator as a web application
