#!/usr/bin/env python3
"""
Week 12: Refactoring with OOP & Decorators - Interactive Examples

This module demonstrates:
- Creating classes with attributes and methods
- Properties and validation
- Special methods (__init__, __repr__, __str__, etc.)
- Decorators for cross-cutting concerns
- The Place class for our Smart City Navigator
- Rate limiting decorator for API compliance

Run this file to see all examples in action:
    python examples.py

Or run with interactive menu:
    python examples.py --interactive
"""

import math
import time
from functools import wraps
from typing import Optional, Tuple, Dict, Any, List
from dataclasses import dataclass, field


# =============================================================================
# SECTION 1: BASIC CLASS EXAMPLES
# =============================================================================

class SimplePlace:
    """A simple class demonstrating basic OOP concepts."""

    def __init__(self, name: str, lat: float, lon: float):
        """Initialize a SimplePlace."""
        self.name = name
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return f"SimplePlace('{self.name}', {self.lat}, {self.lon})"

    def __str__(self):
        return f"{self.name} at ({self.lat}, {self.lon})"


def demo_basic_class():
    """Demonstrate basic class creation and usage."""
    print("\n" + "=" * 60)
    print("DEMO: Basic Class")
    print("=" * 60)

    # Creating instances
    p1 = SimplePlace("Pizza Palace", 25.033, 121.565)
    p2 = SimplePlace("Burger Barn", 25.038, 121.568)

    print("\n--- Creating Instances ---")
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")

    print("\n--- Accessing Attributes ---")
    print(f"p1.name = {p1.name}")
    print(f"p1.lat = {p1.lat}")
    print(f"p1.lon = {p1.lon}")

    print("\n--- repr vs str ---")
    print(f"repr(p1) = {repr(p1)}")
    print(f"str(p1) = {str(p1)}")

    print("\n--- Modifying Attributes ---")
    p1.name = "Pizza Palace (Updated)"
    print(f"After update: {p1}")


# =============================================================================
# SECTION 2: PROPERTIES
# =============================================================================

class PlaceWithProperties:
    """Demonstrate properties for controlled access."""

    def __init__(self, name: str, coords: Tuple[float, float], rating: float = None):
        self.name = name
        self.coords = coords
        self._rating = None
        self.rating = rating  # Use setter

    @property
    def lat(self) -> float:
        """Latitude (read-only)."""
        return self.coords[0]

    @property
    def lon(self) -> float:
        """Longitude (read-only)."""
        return self.coords[1]

    @property
    def rating(self) -> Optional[float]:
        """Rating with getter."""
        return self._rating

    @rating.setter
    def rating(self, value: Optional[float]) -> None:
        """Rating with validation."""
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Rating must be a number")
            if not 0 <= value <= 5:
                raise ValueError("Rating must be between 0 and 5")
        self._rating = value

    @property
    def coords_str(self) -> str:
        """Computed property: formatted coordinates."""
        return f"({self.lat:.4f}, {self.lon:.4f})"


def demo_properties():
    """Demonstrate properties."""
    print("\n" + "=" * 60)
    print("DEMO: Properties")
    print("=" * 60)

    place = PlaceWithProperties("Pizza", (25.033, 121.565), 4.5)

    print("\n--- Read-only Properties ---")
    print(f"place.lat = {place.lat}")
    print(f"place.lon = {place.lon}")

    print("\n--- Trying to set read-only property ---")
    try:
        place.lat = 26.0
    except AttributeError as e:
        print(f"Error: {e}")

    print("\n--- Validated Property (rating) ---")
    print(f"Current rating: {place.rating}")

    place.rating = 4.8
    print(f"After setting to 4.8: {place.rating}")

    print("\n--- Validation in Action ---")
    try:
        place.rating = 6.0  # Invalid!
    except ValueError as e:
        print(f"ValueError: {e}")

    try:
        place.rating = "excellent"  # Invalid type!
    except TypeError as e:
        print(f"TypeError: {e}")

    print("\n--- Computed Property ---")
    print(f"place.coords_str = {place.coords_str}")


# =============================================================================
# SECTION 3: SPECIAL METHODS
# =============================================================================

class ComparablePlace:
    """Demonstrate special methods for comparison and hashing."""

    def __init__(self, name: str, coords: tuple, rating: float = None):
        self.name = name
        self.coords = coords
        self.rating = rating

    def __repr__(self):
        return f"ComparablePlace('{self.name}', {self.coords}, rating={self.rating})"

    def __str__(self):
        rating_str = f" ({self.rating}★)" if self.rating else ""
        return f"{self.name}{rating_str}"

    def __eq__(self, other):
        """Equality based on name and coords."""
        if not isinstance(other, ComparablePlace):
            return NotImplemented
        return self.name == other.name and self.coords == other.coords

    def __hash__(self):
        """Make hashable for use in sets/dicts."""
        return hash((self.name, self.coords))

    def __lt__(self, other):
        """Less than for sorting by rating."""
        if not isinstance(other, ComparablePlace):
            return NotImplemented
        if self.rating is None:
            return True
        if other.rating is None:
            return False
        return self.rating < other.rating


def demo_special_methods():
    """Demonstrate special methods."""
    print("\n" + "=" * 60)
    print("DEMO: Special Methods")
    print("=" * 60)

    p1 = ComparablePlace("Pizza", (25.0, 121.0), 4.5)
    p2 = ComparablePlace("Burger", (25.1, 121.1), 4.2)
    p3 = ComparablePlace("Pizza", (25.0, 121.0), 4.8)  # Same name/coords as p1

    print("\n--- __repr__ and __str__ ---")
    print(f"repr(p1) = {repr(p1)}")
    print(f"str(p1) = {str(p1)}")

    print("\n--- __eq__ (Equality) ---")
    print(f"p1 == p2: {p1 == p2}  (different name/coords)")
    print(f"p1 == p3: {p1 == p3}  (same name/coords, different rating)")

    print("\n--- __hash__ (Hashable) ---")
    place_set = {p1, p2, p3}
    print(f"Set of places: {len(place_set)} unique places")
    print(f"  (p1 and p3 are considered equal)")

    print("\n--- __lt__ (Sorting) ---")
    places = [p1, p2, p3]
    sorted_places = sorted(places, reverse=True)
    print("Sorted by rating (highest first):")
    for p in sorted_places:
        print(f"  {p}")


# =============================================================================
# SECTION 4: CLASS AND STATIC METHODS
# =============================================================================

class PlaceWithClassMethods:
    """Demonstrate class methods and static methods."""

    _all_places: List['PlaceWithClassMethods'] = []

    def __init__(self, name: str, coords: tuple, rating: float = None):
        self.name = name
        self.coords = coords
        self.rating = rating
        PlaceWithClassMethods._all_places.append(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'PlaceWithClassMethods':
        """Create instance from dictionary."""
        return cls(
            name=data["name"],
            coords=tuple(data["coords"]),
            rating=data.get("rating")
        )

    @classmethod
    def get_all(cls) -> List['PlaceWithClassMethods']:
        """Get all instances."""
        return cls._all_places.copy()

    @classmethod
    def clear_all(cls) -> None:
        """Clear all instances."""
        cls._all_places = []

    @staticmethod
    def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate haversine distance (static utility)."""
        R = 6371
        lat1, lat2 = math.radians(lat1), math.radians(lat2)
        dlat = lat2 - lat1
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))

    def __repr__(self):
        return f"Place('{self.name}')"


def demo_class_methods():
    """Demonstrate class and static methods."""
    print("\n" + "=" * 60)
    print("DEMO: Class and Static Methods")
    print("=" * 60)

    # Clear any previous instances
    PlaceWithClassMethods.clear_all()

    print("\n--- @classmethod: from_dict ---")
    data = {"name": "Pizza Palace", "coords": [25.033, 121.565], "rating": 4.5}
    place = PlaceWithClassMethods.from_dict(data)
    print(f"Created from dict: {place}")

    print("\n--- @classmethod: get_all ---")
    PlaceWithClassMethods("Burger Barn", (25.038, 121.568))
    all_places = PlaceWithClassMethods.get_all()
    print(f"All places: {all_places}")

    print("\n--- @staticmethod: haversine ---")
    dist = PlaceWithClassMethods.haversine(25.033, 121.565, 25.038, 121.568)
    print(f"Distance: {dist:.3f} km")
    print("  (Can be called without an instance)")

    # Cleanup
    PlaceWithClassMethods.clear_all()


# =============================================================================
# SECTION 5: BASIC DECORATORS
# =============================================================================

def demo_basic_decorator():
    """Demonstrate basic decorator pattern."""
    print("\n" + "=" * 60)
    print("DEMO: Basic Decorators")
    print("=" * 60)

    # Simple decorator
    def my_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"  [Before] Calling {func.__name__}")
            result = func(*args, **kwargs)
            print(f"  [After] {func.__name__} returned {result}")
            return result
        return wrapper

    @my_decorator
    def greet(name):
        """Greet someone."""
        return f"Hello, {name}!"

    print("\n--- Decorated Function ---")
    result = greet("Alice")
    print(f"Final result: {result}")

    print("\n--- Metadata Preserved ---")
    print(f"Function name: {greet.__name__}")
    print(f"Docstring: {greet.__doc__}")


def demo_decorator_with_args():
    """Demonstrate decorator with arguments."""
    print("\n" + "=" * 60)
    print("DEMO: Decorator with Arguments")
    print("=" * 60)

    def repeat(times: int):
        """Repeat a function multiple times."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                results = []
                for i in range(times):
                    result = func(*args, **kwargs)
                    results.append(result)
                return results
            return wrapper
        return decorator

    @repeat(times=3)
    def say_hello(name):
        return f"Hello, {name}!"

    print("\n--- @repeat(times=3) ---")
    results = say_hello("Bob")
    for i, r in enumerate(results, 1):
        print(f"  {i}. {r}")


# =============================================================================
# SECTION 6: PRACTICAL DECORATORS
# =============================================================================

def timer(func):
    """Decorator to time function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  {func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper


def log_calls(func):
    """Decorator to log function calls."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"  Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"  {func.__name__} returned {result!r}")
        return result
    return wrapper


def demo_practical_decorators():
    """Demonstrate practical decorators."""
    print("\n" + "=" * 60)
    print("DEMO: Practical Decorators")
    print("=" * 60)

    @timer
    def slow_operation(duration):
        """Simulate slow operation."""
        time.sleep(duration)
        return "Done"

    print("\n--- @timer ---")
    result = slow_operation(0.5)

    @log_calls
    def calculate(a, b, operation="add"):
        if operation == "add":
            return a + b
        return a - b

    print("\n--- @log_calls ---")
    result = calculate(5, 3, operation="add")


# =============================================================================
# SECTION 7: RATE LIMIT DECORATOR
# =============================================================================

def rate_limit(seconds: float = 1.0):
    """
    Decorator that ensures minimum time between function calls.

    Args:
        seconds: Minimum seconds between calls
    """
    last_call_time = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call_time[0]
            if elapsed < seconds:
                wait_time = seconds - elapsed
                print(f"  Rate limit: waiting {wait_time:.2f}s...")
                time.sleep(wait_time)

            result = func(*args, **kwargs)
            last_call_time[0] = time.time()
            return result
        return wrapper
    return decorator


def demo_rate_limit():
    """Demonstrate rate limiting decorator."""
    print("\n" + "=" * 60)
    print("DEMO: Rate Limit Decorator")
    print("=" * 60)

    @rate_limit(seconds=0.5)  # Short delay for demo
    def api_call(query):
        """Simulated API call."""
        print(f"  API: Searching for '{query}'")
        return {"query": query, "results": []}

    print("\n--- Rate Limited API Calls ---")
    print("Making 3 API calls with 0.5s rate limit:")

    start = time.time()
    for query in ["pizza", "burger", "taco"]:
        api_call(query)
    elapsed = time.time() - start

    print(f"\nTotal time: {elapsed:.2f}s (expected ~1.0s with rate limiting)")


# =============================================================================
# SECTION 8: THE COMPLETE PLACE CLASS
# =============================================================================

class Place:
    """
    Complete Place class for Smart City Navigator.

    Demonstrates:
    - Properties with validation
    - Instance methods
    - Class methods
    - Static methods
    - Special methods
    """

    def __init__(
        self,
        name: str,
        coords: Tuple[float, float],
        rating: Optional[float] = None,
        category: Optional[str] = None
    ):
        self.name = name
        self.coords = coords
        self._rating = None
        self.rating = rating
        self.category = category

    # === Properties ===

    @property
    def lat(self) -> float:
        return self.coords[0]

    @property
    def lon(self) -> float:
        return self.coords[1]

    @property
    def rating(self) -> Optional[float]:
        return self._rating

    @rating.setter
    def rating(self, value: Optional[float]) -> None:
        if value is not None and not (0 <= value <= 5):
            raise ValueError("Rating must be between 0 and 5")
        self._rating = value

    # === Instance Methods ===

    def distance_to(self, other: 'Place') -> float:
        """Calculate Haversine distance to another Place in km."""
        R = 6371
        lat1, lon1 = math.radians(self.lat), math.radians(self.lon)
        lat2, lon2 = math.radians(other.lat), math.radians(other.lon)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))

    def walking_time_to(self, other: 'Place', speed_kmh: float = 5.0) -> float:
        """Calculate walking time to another Place in minutes."""
        return (self.distance_to(other) / speed_kmh) * 60

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "coords": list(self.coords),
            "rating": self.rating,
            "category": self.category
        }

    # === Class Methods ===

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Place':
        """Create Place from dictionary."""
        return cls(
            name=data["name"],
            coords=tuple(data["coords"]),
            rating=data.get("rating"),
            category=data.get("category")
        )

    # === Special Methods ===

    def __repr__(self) -> str:
        return f"Place('{self.name}', {self.coords}, rating={self.rating})"

    def __str__(self) -> str:
        parts = [self.name]
        if self.rating:
            parts.append(f"({self.rating}★)")
        if self.category:
            parts.append(f"[{self.category}]")
        return " ".join(parts)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Place):
            return NotImplemented
        return self.name == other.name and self.coords == other.coords

    def __hash__(self) -> int:
        return hash((self.name, self.coords))

    def __lt__(self, other) -> bool:
        if not isinstance(other, Place):
            return NotImplemented
        if self.rating is None:
            return True
        if other.rating is None:
            return False
        return self.rating < other.rating


def demo_place_class():
    """Demonstrate the complete Place class."""
    print("\n" + "=" * 60)
    print("DEMO: Complete Place Class")
    print("=" * 60)

    # Create places
    taipei101 = Place("Taipei 101", (25.0330, 121.5654), rating=4.7, category="landmark")
    station = Place("Main Station", (25.0478, 121.5170), rating=4.2, category="transport")
    pizza = Place("Pizza Palace", (25.035, 121.560), rating=4.5, category="restaurant")

    print("\n--- Creating Places ---")
    print(f"taipei101 = {taipei101}")
    print(f"station = {station}")
    print(f"pizza = {pizza}")

    print("\n--- Properties ---")
    print(f"taipei101.lat = {taipei101.lat}")
    print(f"taipei101.lon = {taipei101.lon}")
    print(f"taipei101.rating = {taipei101.rating}")

    print("\n--- Distance Calculation ---")
    dist = taipei101.distance_to(station)
    print(f"Distance Taipei 101 to Station: {dist:.2f} km")

    walk_time = taipei101.walking_time_to(station)
    print(f"Walking time: {walk_time:.1f} minutes")

    print("\n--- Serialization ---")
    data = taipei101.to_dict()
    print(f"to_dict(): {data}")

    restored = Place.from_dict(data)
    print(f"from_dict(): {restored}")
    print(f"Equal? {taipei101 == restored}")

    print("\n--- Sorting ---")
    places = [taipei101, station, pizza]
    sorted_places = sorted(places, reverse=True)
    print("Sorted by rating (highest first):")
    for p in sorted_places:
        print(f"  {p}")


# =============================================================================
# SECTION 9: DATACLASSES
# =============================================================================

@dataclass
class DataclassPlace:
    """Place using dataclass for automatic boilerplate."""

    name: str
    coords: Tuple[float, float]
    rating: Optional[float] = None
    category: Optional[str] = None

    @property
    def lat(self) -> float:
        return self.coords[0]

    @property
    def lon(self) -> float:
        return self.coords[1]

    def distance_to(self, other: 'DataclassPlace') -> float:
        R = 6371
        lat1, lon1 = math.radians(self.lat), math.radians(self.lon)
        lat2, lon2 = math.radians(other.lat), math.radians(other.lon)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))


def demo_dataclass():
    """Demonstrate dataclass usage."""
    print("\n" + "=" * 60)
    print("DEMO: Dataclasses")
    print("=" * 60)

    p1 = DataclassPlace("Pizza", (25.0, 121.0), rating=4.5)
    p2 = DataclassPlace("Pizza", (25.0, 121.0), rating=4.5)
    p3 = DataclassPlace("Burger", (25.1, 121.1))

    print("\n--- Auto-generated __repr__ ---")
    print(f"p1 = {p1}")

    print("\n--- Auto-generated __eq__ ---")
    print(f"p1 == p2: {p1 == p2}")
    print(f"p1 == p3: {p1 == p3}")

    print("\n--- Custom Methods Still Work ---")
    dist = p1.distance_to(p3)
    print(f"Distance p1 to p3: {dist:.3f} km")


# =============================================================================
# MAIN
# =============================================================================

def run_all_demos():
    """Run all demonstrations."""
    demos = [
        ("Basic Class", demo_basic_class),
        ("Properties", demo_properties),
        ("Special Methods", demo_special_methods),
        ("Class and Static Methods", demo_class_methods),
        ("Basic Decorator", demo_basic_decorator),
        ("Decorator with Arguments", demo_decorator_with_args),
        ("Practical Decorators", demo_practical_decorators),
        ("Rate Limit Decorator", demo_rate_limit),
        ("Complete Place Class", demo_place_class),
        ("Dataclasses", demo_dataclass),
    ]

    print("=" * 60)
    print("WEEK 12: OOP & DECORATORS")
    print("Interactive Examples")
    print("=" * 60)

    for name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"\n[ERROR in {name}]: {e}")

    print("\n" + "=" * 60)
    print("All demos completed!")
    print("=" * 60)


def run_interactive_menu():
    """Run interactive menu."""
    demos = {
        "1": ("Basic Class", demo_basic_class),
        "2": ("Properties", demo_properties),
        "3": ("Special Methods", demo_special_methods),
        "4": ("Class and Static Methods", demo_class_methods),
        "5": ("Basic Decorator", demo_basic_decorator),
        "6": ("Decorator with Arguments", demo_decorator_with_args),
        "7": ("Practical Decorators", demo_practical_decorators),
        "8": ("Rate Limit Decorator", demo_rate_limit),
        "9": ("Complete Place Class", demo_place_class),
        "10": ("Dataclasses", demo_dataclass),
        "a": ("Run All", run_all_demos),
    }

    while True:
        print("\n" + "=" * 40)
        print("WEEK 12: OOP & DECORATORS")
        print("=" * 40)
        print("\nSelect a demo:")
        for key, (name, _) in demos.items():
            print(f"  {key}. {name}")
        print("  q. Quit")

        choice = input("\nChoice: ").strip().lower()

        if choice == 'q':
            print("Goodbye!")
            break
        elif choice in demos:
            demos[choice][1]()
            input("\nPress Enter to continue...")
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive_menu()
    else:
        run_all_demos()
