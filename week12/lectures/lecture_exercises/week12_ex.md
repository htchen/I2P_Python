# Week 12 Lab: Refactoring with OOP & Decorators

## Lab Overview

In this lab, you'll refactor procedural code into clean object-oriented code and create useful decorators. You'll build a complete `Place` class and implement a `@rate_limit` decorator for API compliance.

**Time:** 2 hours
**Difficulty:** Intermediate

### Learning Objectives

By completing this lab, you will:
1. Create classes with attributes, methods, and properties
2. Implement special methods (`__init__`, `__repr__`, `__eq__`, etc.)
3. Use `@property` for controlled attribute access
4. Create and use decorators
5. Implement a rate-limiting decorator
6. Refactor procedural code into OOP

### Prerequisites

- Week 9: Functional Patterns (closures, first-class functions)
- Week 10: TSP (place data structures)
- Basic understanding of functions

---

## Setup

### Starter Code

Open `week12_starter.py` and review the provided code structure.

### Running Tests

```bash
python week12_starter.py              # Run all tests
python week12_starter.py --test ex1   # Run specific exercise
```

---

## Exercise 1: Basic Class Creation (20 minutes)

### Task 1.1: Create a `Place` class

Implement a basic `Place` class:

```python
class Place:
    """
    A class representing a location/place.

    Attributes:
        name: Name of the place
        coords: Tuple of (latitude, longitude)
        rating: Optional rating (0-5)
        category: Optional category string
    """

    def __init__(self, name: str, coords: tuple, rating: float = None, category: str = None):
        """
        Initialize a Place.

        Args:
            name: Name of the place
            coords: (latitude, longitude) tuple
            rating: Rating from 0-5 (optional)
            category: Category like 'restaurant' (optional)
        """
        # YOUR CODE HERE
        pass
```

### Task 1.2: Add `__repr__` method

```python
def __repr__(self) -> str:
    """
    Return developer-friendly string representation.

    Example:
        >>> p = Place("Pizza", (25.0, 121.0), 4.5)
        >>> repr(p)
        "Place('Pizza', (25.0, 121.0), rating=4.5)"
    """
    # YOUR CODE HERE
    pass
```

### Task 1.3: Add `__str__` method

```python
def __str__(self) -> str:
    """
    Return user-friendly string.

    Example:
        >>> p = Place("Pizza", (25.0, 121.0), 4.5, "restaurant")
        >>> str(p)
        "Pizza (4.5★) [restaurant]"
    """
    # YOUR CODE HERE
    pass
```

---

## Exercise 2: Properties (20 minutes)

### Task 2.1: Add `lat` and `lon` properties

```python
@property
def lat(self) -> float:
    """
    Latitude coordinate (read-only).

    Example:
        >>> p = Place("Test", (25.033, 121.565))
        >>> p.lat
        25.033
    """
    # YOUR CODE HERE
    pass

@property
def lon(self) -> float:
    """
    Longitude coordinate (read-only).

    Example:
        >>> p = Place("Test", (25.033, 121.565))
        >>> p.lon
        121.565
    """
    # YOUR CODE HERE
    pass
```

### Task 2.2: Add validated `rating` property

```python
@property
def rating(self) -> float:
    """Get rating."""
    # YOUR CODE HERE
    pass

@rating.setter
def rating(self, value: float) -> None:
    """
    Set rating with validation.

    Raises:
        ValueError: If rating not between 0 and 5
        TypeError: If rating is not a number

    Example:
        >>> p = Place("Test", (25.0, 121.0))
        >>> p.rating = 4.5  # OK
        >>> p.rating = 6.0  # Raises ValueError
    """
    # YOUR CODE HERE
    pass
```

### Task 2.3: Add computed `coords_str` property

```python
@property
def coords_str(self) -> str:
    """
    Return formatted coordinates string.

    Example:
        >>> p = Place("Test", (25.033, 121.565))
        >>> p.coords_str
        "(25.0330, 121.5650)"
    """
    # YOUR CODE HERE
    pass
```

---

## Exercise 3: Instance Methods (20 minutes)

### Task 3.1: Implement `distance_to`

```python
def distance_to(self, other: 'Place') -> float:
    """
    Calculate Haversine distance to another Place.

    Args:
        other: Another Place object

    Returns:
        Distance in kilometers

    Example:
        >>> p1 = Place("A", (25.033, 121.565))
        >>> p2 = Place("B", (25.038, 121.568))
        >>> p1.distance_to(p2)
        0.62  # approximately
    """
    import math
    R = 6371  # Earth radius in km

    # YOUR CODE HERE
    # Use Haversine formula
    pass
```

### Task 3.2: Implement `walking_time_to`

```python
def walking_time_to(self, other: 'Place', speed_kmh: float = 5.0) -> float:
    """
    Calculate walking time to another Place.

    Args:
        other: Another Place object
        speed_kmh: Walking speed in km/h (default 5.0)

    Returns:
        Walking time in minutes

    Example:
        >>> p1 = Place("A", (25.033, 121.565))
        >>> p2 = Place("B", (25.038, 121.568))
        >>> p1.walking_time_to(p2)
        7.4  # approximately
    """
    # YOUR CODE HERE
    pass
```

### Task 3.3: Implement `to_dict`

```python
def to_dict(self) -> dict:
    """
    Convert Place to dictionary for JSON serialization.

    Returns:
        Dictionary with name, coords, rating, category

    Example:
        >>> p = Place("Pizza", (25.0, 121.0), 4.5, "restaurant")
        >>> p.to_dict()
        {'name': 'Pizza', 'coords': [25.0, 121.0], 'rating': 4.5, 'category': 'restaurant'}
    """
    # YOUR CODE HERE
    pass
```

---

## Exercise 4: Class Methods (15 minutes)

### Task 4.1: Implement `from_dict`

```python
@classmethod
def from_dict(cls, data: dict) -> 'Place':
    """
    Create Place from dictionary.

    Args:
        data: Dictionary with place data

    Returns:
        New Place instance

    Example:
        >>> data = {'name': 'Pizza', 'coords': [25.0, 121.0], 'rating': 4.5}
        >>> p = Place.from_dict(data)
        >>> p.name
        'Pizza'
    """
    # YOUR CODE HERE
    pass
```

### Task 4.2: Implement `from_nominatim`

```python
@classmethod
def from_nominatim(cls, data: dict) -> 'Place':
    """
    Create Place from Nominatim API response.

    Args:
        data: Nominatim search result dictionary

    Returns:
        New Place instance

    Example:
        >>> data = {'display_name': 'Taipei 101', 'lat': '25.033', 'lon': '121.565', 'type': 'building'}
        >>> p = Place.from_nominatim(data)
        >>> p.name
        'Taipei 101'
    """
    # YOUR CODE HERE
    pass
```

---

## Exercise 5: Special Methods for Comparison (15 minutes)

### Task 5.1: Implement `__eq__`

```python
def __eq__(self, other) -> bool:
    """
    Check equality based on name and coordinates.

    Example:
        >>> p1 = Place("Pizza", (25.0, 121.0), 4.5)
        >>> p2 = Place("Pizza", (25.0, 121.0), 4.8)
        >>> p1 == p2
        True  # Same name and coords
    """
    # YOUR CODE HERE
    pass
```

### Task 5.2: Implement `__hash__`

```python
def __hash__(self) -> int:
    """
    Make Place hashable for use in sets and as dict keys.

    Example:
        >>> p = Place("Pizza", (25.0, 121.0))
        >>> {p: "favorite"}  # Can be used as dict key
    """
    # YOUR CODE HERE
    pass
```

### Task 5.3: Implement `__lt__`

```python
def __lt__(self, other) -> bool:
    """
    Less than comparison based on rating (for sorting).

    Places with no rating are considered "less than" rated places.

    Example:
        >>> places = [Place("A", (0,0), 4.2), Place("B", (0,0), 4.5)]
        >>> sorted(places, reverse=True)[0].name
        'B'
    """
    # YOUR CODE HERE
    pass
```

---

## Exercise 6: Basic Decorators (20 minutes)

### Task 6.1: Create `timer` decorator

```python
def timer(func):
    """
    Decorator to time function execution.

    Example:
        @timer
        def slow_func():
            time.sleep(1)

        slow_func()  # Prints: "slow_func took 1.0012 seconds"
    """
    from functools import wraps
    import time

    @wraps(func)
    def wrapper(*args, **kwargs):
        # YOUR CODE HERE
        pass

    return wrapper
```

### Task 6.2: Create `log_calls` decorator

```python
def log_calls(func):
    """
    Decorator to log function calls with arguments.

    Example:
        @log_calls
        def add(a, b):
            return a + b

        add(2, 3)
        # Prints: "Calling add(2, 3)"
        # Prints: "add returned 5"
    """
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        # YOUR CODE HERE
        pass

    return wrapper
```

### Task 6.3: Create `retry` decorator

```python
def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator to retry a function on exception.

    Args:
        max_attempts: Maximum number of attempts
        delay: Delay between attempts in seconds

    Example:
        @retry(max_attempts=3, delay=0.5)
        def flaky_function():
            if random.random() < 0.7:
                raise Exception("Random failure")
            return "Success"
    """
    def decorator(func):
        from functools import wraps

        @wraps(func)
        def wrapper(*args, **kwargs):
            # YOUR CODE HERE
            pass

        return wrapper
    return decorator
```

---

## Exercise 7: Rate Limit Decorator (20 minutes)

### Task 7.1: Implement basic `rate_limit`

```python
def rate_limit(seconds: float = 1.0):
    """
    Decorator that ensures minimum time between function calls.

    Args:
        seconds: Minimum seconds between calls

    Example:
        @rate_limit(seconds=1.0)
        def api_call(query):
            return f"Searching: {query}"

        api_call("pizza")   # Immediate
        api_call("burger")  # Waits ~1 second
    """
    last_call_time = [0.0]

    def decorator(func):
        from functools import wraps

        @wraps(func)
        def wrapper(*args, **kwargs):
            # YOUR CODE HERE
            # 1. Calculate elapsed time since last call
            # 2. If not enough time passed, sleep
            # 3. Call the function
            # 4. Update last_call_time
            pass

        return wrapper
    return decorator
```

### Task 7.2: Create `RateLimiter` class

```python
class RateLimiter:
    """
    Rate limiter that can be shared across functions.

    Example:
        limiter = RateLimiter(calls_per_second=1)

        @limiter
        def func1(): pass

        @limiter
        def func2(): pass

        func1()  # Immediate
        func2()  # Waits 1 second (shares rate limit with func1)
    """

    def __init__(self, calls_per_second: float = 1.0):
        # YOUR CODE HERE
        pass

    def wait_if_needed(self):
        """Wait if necessary to respect rate limit."""
        # YOUR CODE HERE
        pass

    def __call__(self, func):
        """Allow use as decorator."""
        from functools import wraps

        @wraps(func)
        def wrapper(*args, **kwargs):
            # YOUR CODE HERE
            pass

        return wrapper
```

---

## Exercise 8: Refactoring Challenge (15 minutes)

### Task: Refactor Procedural Code to OOP

Given this procedural code:

```python
# BEFORE: Procedural code
places = []

def add_place(name, lat, lon, rating=None):
    places.append({"name": name, "lat": lat, "lon": lon, "rating": rating})

def get_distance(p1, p2):
    import math
    # ... haversine calculation using p1["lat"], p1["lon"], etc.
    pass

def filter_by_rating(places_list, min_rating):
    return [p for p in places_list if p.get("rating", 0) >= min_rating]

def sort_by_rating(places_list):
    return sorted(places_list, key=lambda p: p.get("rating", 0), reverse=True)
```

Refactor to:

```python
# AFTER: OOP code
class PlaceService:
    """Service for managing places."""

    def __init__(self):
        self.places: List[Place] = []

    def add(self, place: Place) -> None:
        """Add a place to the collection."""
        # YOUR CODE HERE
        pass

    def filter_by_rating(self, min_rating: float) -> List[Place]:
        """Return places with rating >= min_rating."""
        # YOUR CODE HERE
        pass

    def filter_by_category(self, category: str) -> List[Place]:
        """Return places matching category."""
        # YOUR CODE HERE
        pass

    def sort_by_rating(self, descending: bool = True) -> List[Place]:
        """Return places sorted by rating."""
        # YOUR CODE HERE
        pass

    def find_nearest(self, reference: Place) -> Optional[Place]:
        """Find the place nearest to reference."""
        # YOUR CODE HERE
        pass
```

---

## Bonus Challenges

### Challenge 1: Caching Decorator

Create a decorator that caches function results:

```python
def cache(max_size: int = 100):
    """
    Decorator that caches function results.

    Args:
        max_size: Maximum cache size

    Example:
        @cache(max_size=100)
        def expensive_calculation(n):
            time.sleep(1)  # Simulate slow operation
            return n * 2

        expensive_calculation(5)  # Slow (1 second)
        expensive_calculation(5)  # Fast (cached)
    """
    # YOUR CODE HERE
    pass
```

### Challenge 2: Validation Decorator

Create a decorator that validates function arguments:

```python
def validate_types(**type_hints):
    """
    Decorator that validates argument types.

    Example:
        @validate_types(name=str, age=int)
        def create_user(name, age):
            return {"name": name, "age": age}

        create_user("Alice", 30)  # OK
        create_user("Alice", "30")  # Raises TypeError
    """
    # YOUR CODE HERE
    pass
```

### Challenge 3: PlaceCollection with Container Protocol

Implement a collection that supports Python's container protocol:

```python
class PlaceCollection:
    """
    Collection of places with list-like behavior.

    Supports:
    - len(collection)
    - collection[0]
    - for place in collection
    - place in collection
    """

    def __init__(self):
        self._places = []

    def __len__(self) -> int:
        # YOUR CODE HERE
        pass

    def __getitem__(self, index: int) -> Place:
        # YOUR CODE HERE
        pass

    def __iter__(self):
        # YOUR CODE HERE
        pass

    def __contains__(self, place: Place) -> bool:
        # YOUR CODE HERE
        pass
```

---

## Submission Checklist

Before submitting, verify:

- [ ] All exercises completed in `week12_starter.py`
- [ ] All test cases pass
- [ ] `Place` class has all required methods
- [ ] Properties validate input correctly
- [ ] Decorators work as expected
- [ ] `rate_limit` properly delays function calls
- [ ] Code follows OOP best practices

---

## Summary

In this lab, you practiced:

| Concept | What You Learned |
|---------|------------------|
| **Classes** | Bundling data and behavior |
| **`__init__`** | Initializing object state |
| **Properties** | Controlled attribute access |
| **Special Methods** | `__repr__`, `__str__`, `__eq__`, `__lt__` |
| **Class Methods** | Factory methods like `from_dict` |
| **Decorators** | Wrapping functions to extend behavior |
| **Rate Limiting** | Controlling API call frequency |

### Key Takeaways

1. **OOP bundles data and behavior** - methods operate on instance data
2. **Properties provide controlled access** - validation, computed values
3. **Special methods enable Python integration** - sorting, equality, hashing
4. **Decorators add cross-cutting concerns** - timing, logging, rate limiting
5. **Class methods are factory methods** - create instances from various sources
6. **Rate limiting is essential for APIs** - respect service policies
