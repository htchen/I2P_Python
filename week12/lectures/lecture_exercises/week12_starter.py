#!/usr/bin/env python3
"""
Week 12 Lab: Refactoring with OOP & Decorators
Starter Code with Test Suite

Complete the exercises by implementing the TODO sections.
Run: python week12_starter.py
Run specific test: python week12_starter.py --test ex1
"""

import math
import time
import sys
from typing import List, Tuple, Optional
from functools import wraps


# =============================================================================
# Exercise 1: Basic Class Creation
# =============================================================================

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
        # TODO: Exercise 1.1 - Initialize attributes
        # Store name, coords, category as instance attributes
        # Use the rating setter for validation (set self._rating = None first)
        pass

    def __repr__(self) -> str:
        """
        Return developer-friendly string representation.

        Example:
            >>> p = Place("Pizza", (25.0, 121.0), 4.5)
            >>> repr(p)
            "Place('Pizza', (25.0, 121.0), rating=4.5)"
        """
        # TODO: Exercise 1.2 - Return repr string
        pass

    def __str__(self) -> str:
        """
        Return user-friendly string.

        Example:
            >>> p = Place("Pizza", (25.0, 121.0), 4.5, "restaurant")
            >>> str(p)
            "Pizza (4.5★) [restaurant]"

            >>> p2 = Place("Park", (25.0, 121.0))
            >>> str(p2)
            "Park"
        """
        # TODO: Exercise 1.3 - Return str string
        # Include rating with ★ if present
        # Include category in brackets if present
        pass


# =============================================================================
# Exercise 2: Properties
# =============================================================================

    @property
    def lat(self) -> float:
        """
        Latitude coordinate (read-only).

        Example:
            >>> p = Place("Test", (25.033, 121.565))
            >>> p.lat
            25.033
        """
        # TODO: Exercise 2.1 - Return latitude from coords
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
        # TODO: Exercise 2.1 - Return longitude from coords
        pass

    @property
    def rating(self) -> float:
        """Get rating."""
        # TODO: Exercise 2.2 - Return _rating
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
        # TODO: Exercise 2.2 - Validate and set rating
        # Allow None
        # Check type (must be int or float)
        # Check range (0-5)
        pass

    @property
    def coords_str(self) -> str:
        """
        Return formatted coordinates string.

        Example:
            >>> p = Place("Test", (25.033, 121.565))
            >>> p.coords_str
            "(25.0330, 121.5650)"
        """
        # TODO: Exercise 2.3 - Return formatted coordinates
        pass


# =============================================================================
# Exercise 3: Instance Methods
# =============================================================================

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
            >>> round(p1.distance_to(p2), 2)
            0.62
        """
        # TODO: Exercise 3.1 - Implement Haversine formula
        R = 6371  # Earth radius in km

        # Convert to radians
        # lat1, lon1 = ...
        # lat2, lon2 = ...

        # Calculate differences
        # dlat = lat2 - lat1
        # dlon = lon2 - lon1

        # Haversine formula
        # a = sin(dlat/2)^2 + cos(lat1) * cos(lat2) * sin(dlon/2)^2
        # c = 2 * asin(sqrt(a))
        # distance = R * c

        pass

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
            >>> round(p1.walking_time_to(p2), 1)
            7.4
        """
        # TODO: Exercise 3.2 - Calculate walking time
        # Use distance_to and convert to minutes
        pass

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
        # TODO: Exercise 3.3 - Return dictionary representation
        # Note: coords should be a list, not tuple
        pass


# =============================================================================
# Exercise 4: Class Methods
# =============================================================================

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
        # TODO: Exercise 4.1 - Create Place from dict
        # Handle both list and tuple coords
        pass

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
        # TODO: Exercise 4.2 - Create Place from Nominatim response
        # Note: lat and lon are strings in Nominatim response
        # Use 'type' as category
        pass


# =============================================================================
# Exercise 5: Special Methods for Comparison
# =============================================================================

    def __eq__(self, other) -> bool:
        """
        Check equality based on name and coordinates.

        Example:
            >>> p1 = Place("Pizza", (25.0, 121.0), 4.5)
            >>> p2 = Place("Pizza", (25.0, 121.0), 4.8)
            >>> p1 == p2
            True
        """
        # TODO: Exercise 5.1 - Implement equality check
        # Check if other is a Place
        # Compare name and coords
        pass

    def __hash__(self) -> int:
        """
        Make Place hashable for use in sets and as dict keys.

        Example:
            >>> p = Place("Pizza", (25.0, 121.0))
            >>> {p: "favorite"}  # Can be used as dict key
        """
        # TODO: Exercise 5.2 - Return hash based on name and coords
        pass

    def __lt__(self, other) -> bool:
        """
        Less than comparison based on rating (for sorting).

        Places with no rating are considered "less than" rated places.

        Example:
            >>> places = [Place("A", (0,0), 4.2), Place("B", (0,0), 4.5)]
            >>> sorted(places, reverse=True)[0].name
            'B'
        """
        # TODO: Exercise 5.3 - Implement less than comparison
        # Handle None ratings (treat as -infinity)
        pass


# =============================================================================
# Exercise 6: Basic Decorators
# =============================================================================

def timer(func):
    """
    Decorator to time function execution.

    Example:
        @timer
        def slow_func():
            time.sleep(0.1)

        slow_func()  # Prints: "slow_func took 0.1xxx seconds"
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: Exercise 6.1 - Implement timer
        # Record start time
        # Call function
        # Record end time
        # Print elapsed time
        # Return result
        pass

    return wrapper


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
    @wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: Exercise 6.2 - Implement log_calls
        # Print function name and arguments
        # Call function
        # Print return value
        # Return result
        pass

    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator to retry a function on exception.

    Args:
        max_attempts: Maximum number of attempts
        delay: Delay between attempts in seconds

    Example:
        @retry(max_attempts=3, delay=0.1)
        def flaky_function():
            import random
            if random.random() < 0.7:
                raise Exception("Random failure")
            return "Success"
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Exercise 6.3 - Implement retry
            # Loop up to max_attempts
            # Try calling function
            # On exception, wait and retry
            # On last attempt, re-raise exception
            pass

        return wrapper
    return decorator


# =============================================================================
# Exercise 7: Rate Limit Decorator
# =============================================================================

def rate_limit(seconds: float = 1.0):
    """
    Decorator that ensures minimum time between function calls.

    Args:
        seconds: Minimum seconds between calls

    Example:
        @rate_limit(seconds=0.5)
        def api_call(query):
            return f"Searching: {query}"

        api_call("pizza")   # Immediate
        api_call("burger")  # Waits ~0.5 seconds
    """
    last_call_time = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Exercise 7.1 - Implement rate_limit
            # 1. Calculate elapsed time since last call
            # 2. If not enough time passed, sleep
            # 3. Call the function
            # 4. Update last_call_time[0]
            # 5. Return result
            pass

        return wrapper
    return decorator


class RateLimiter:
    """
    Rate limiter that can be shared across functions.

    Example:
        limiter = RateLimiter(calls_per_second=2)

        @limiter
        def func1(): pass

        @limiter
        def func2(): pass

        func1()  # Immediate
        func2()  # Waits 0.5 seconds (shares rate limit with func1)
    """

    def __init__(self, calls_per_second: float = 1.0):
        # TODO: Exercise 7.2 - Initialize rate limiter
        # Store minimum interval (1 / calls_per_second)
        # Initialize last_call_time
        pass

    def wait_if_needed(self):
        """Wait if necessary to respect rate limit."""
        # TODO: Exercise 7.2 - Implement wait logic
        pass

    def __call__(self, func):
        """Allow use as decorator."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Exercise 7.2 - Call wait_if_needed then function
            pass

        return wrapper


# =============================================================================
# Exercise 8: Refactoring Challenge
# =============================================================================

class PlaceService:
    """Service for managing places."""

    def __init__(self):
        self.places: List[Place] = []

    def add(self, place: Place) -> None:
        """Add a place to the collection."""
        # TODO: Exercise 8 - Implement add
        pass

    def filter_by_rating(self, min_rating: float) -> List[Place]:
        """Return places with rating >= min_rating."""
        # TODO: Exercise 8 - Implement filter_by_rating
        pass

    def filter_by_category(self, category: str) -> List[Place]:
        """Return places matching category."""
        # TODO: Exercise 8 - Implement filter_by_category
        pass

    def sort_by_rating(self, descending: bool = True) -> List[Place]:
        """Return places sorted by rating."""
        # TODO: Exercise 8 - Implement sort_by_rating
        pass

    def find_nearest(self, reference: Place) -> Optional[Place]:
        """Find the place nearest to reference."""
        # TODO: Exercise 8 - Implement find_nearest
        pass


# =============================================================================
# Test Suite
# =============================================================================

def test_exercise_1():
    """Test basic class creation."""
    print("\n" + "="*60)
    print("Testing Exercise 1: Basic Class Creation")
    print("="*60)

    tests_passed = 0
    tests_total = 0

    # Test 1.1: __init__
    tests_total += 1
    try:
        p = Place("Pizza Palace", (25.033, 121.565), 4.5, "restaurant")
        assert p.name == "Pizza Palace", f"Expected name 'Pizza Palace', got '{p.name}'"
        assert p.coords == (25.033, 121.565), f"Expected coords (25.033, 121.565), got {p.coords}"
        assert p._rating == 4.5, f"Expected _rating 4.5, got {p._rating}"
        assert p.category == "restaurant", f"Expected category 'restaurant', got '{p.category}'"
        print("  ✓ Test 1.1: __init__ works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 1.1: __init__ failed - {e}")

    # Test 1.2: __repr__
    tests_total += 1
    try:
        p = Place("Pizza", (25.0, 121.0), 4.5)
        r = repr(p)
        assert "Place(" in r, f"__repr__ should contain 'Place('"
        assert "'Pizza'" in r, f"__repr__ should contain \"'Pizza'\""
        assert "(25.0, 121.0)" in r, f"__repr__ should contain coords"
        assert "rating=4.5" in r, f"__repr__ should contain 'rating=4.5'"
        print("  ✓ Test 1.2: __repr__ works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 1.2: __repr__ failed - {e}")

    # Test 1.3: __str__
    tests_total += 1
    try:
        p1 = Place("Pizza", (25.0, 121.0), 4.5, "restaurant")
        s1 = str(p1)
        assert "Pizza" in s1, f"__str__ should contain name"
        assert "4.5" in s1, f"__str__ should contain rating"
        assert "★" in s1, f"__str__ should contain star symbol"
        assert "restaurant" in s1, f"__str__ should contain category"

        p2 = Place("Park", (25.0, 121.0))
        s2 = str(p2)
        assert s2 == "Park" or s2.strip() == "Park", f"Place without rating/category should just show name"

        print("  ✓ Test 1.3: __str__ works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 1.3: __str__ failed - {e}")

    print(f"\nExercise 1: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_2():
    """Test properties."""
    print("\n" + "="*60)
    print("Testing Exercise 2: Properties")
    print("="*60)

    tests_passed = 0
    tests_total = 0

    # Test 2.1: lat and lon properties
    tests_total += 1
    try:
        p = Place("Test", (25.033, 121.565))
        assert p.lat == 25.033, f"Expected lat 25.033, got {p.lat}"
        assert p.lon == 121.565, f"Expected lon 121.565, got {p.lon}"
        print("  ✓ Test 2.1: lat/lon properties work correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 2.1: lat/lon properties failed - {e}")

    # Test 2.2: rating property with validation
    tests_total += 1
    try:
        p = Place("Test", (25.0, 121.0))
        p.rating = 4.5
        assert p.rating == 4.5, f"Expected rating 4.5, got {p.rating}"

        try:
            p.rating = 6.0
            print(f"  ✗ Test 2.2: rating validation failed - should raise ValueError for 6.0")
            continue_test = False
        except ValueError:
            continue_test = True

        if continue_test:
            try:
                p.rating = -1.0
                print(f"  ✗ Test 2.2: rating validation failed - should raise ValueError for -1.0")
            except ValueError:
                print("  ✓ Test 2.2: rating property validates correctly")
                tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 2.2: rating property failed - {e}")

    # Test 2.3: coords_str property
    tests_total += 1
    try:
        p = Place("Test", (25.033, 121.565))
        cs = p.coords_str
        assert "25.0330" in cs, f"coords_str should format lat with 4 decimals"
        assert "121.5650" in cs, f"coords_str should format lon with 4 decimals"
        print("  ✓ Test 2.3: coords_str property works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 2.3: coords_str property failed - {e}")

    print(f"\nExercise 2: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_3():
    """Test instance methods."""
    print("\n" + "="*60)
    print("Testing Exercise 3: Instance Methods")
    print("="*60)

    tests_passed = 0
    tests_total = 0

    # Test 3.1: distance_to
    tests_total += 1
    try:
        p1 = Place("A", (25.033, 121.565))
        p2 = Place("B", (25.038, 121.568))
        dist = p1.distance_to(p2)
        # Expected ~0.62 km
        assert 0.5 < dist < 0.8, f"Expected distance ~0.62 km, got {dist}"
        print("  ✓ Test 3.1: distance_to works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 3.1: distance_to failed - {e}")

    # Test 3.2: walking_time_to
    tests_total += 1
    try:
        p1 = Place("A", (25.033, 121.565))
        p2 = Place("B", (25.038, 121.568))
        time_min = p1.walking_time_to(p2)
        # Expected ~7.4 minutes at 5 km/h
        assert 6 < time_min < 9, f"Expected walking time ~7.4 min, got {time_min}"
        print("  ✓ Test 3.2: walking_time_to works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 3.2: walking_time_to failed - {e}")

    # Test 3.3: to_dict
    tests_total += 1
    try:
        p = Place("Pizza", (25.0, 121.0), 4.5, "restaurant")
        d = p.to_dict()
        assert d['name'] == 'Pizza', f"Expected name 'Pizza'"
        assert d['coords'] == [25.0, 121.0], f"Expected coords as list [25.0, 121.0]"
        assert d['rating'] == 4.5, f"Expected rating 4.5"
        assert d['category'] == 'restaurant', f"Expected category 'restaurant'"
        print("  ✓ Test 3.3: to_dict works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 3.3: to_dict failed - {e}")

    print(f"\nExercise 3: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_4():
    """Test class methods."""
    print("\n" + "="*60)
    print("Testing Exercise 4: Class Methods")
    print("="*60)

    tests_passed = 0
    tests_total = 0

    # Test 4.1: from_dict
    tests_total += 1
    try:
        data = {'name': 'Pizza', 'coords': [25.0, 121.0], 'rating': 4.5, 'category': 'restaurant'}
        p = Place.from_dict(data)
        assert p.name == 'Pizza', f"Expected name 'Pizza'"
        assert p.coords == (25.0, 121.0), f"Expected coords (25.0, 121.0)"
        assert p.rating == 4.5, f"Expected rating 4.5"
        assert p.category == 'restaurant', f"Expected category 'restaurant'"
        print("  ✓ Test 4.1: from_dict works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 4.1: from_dict failed - {e}")

    # Test 4.2: from_nominatim
    tests_total += 1
    try:
        data = {'display_name': 'Taipei 101', 'lat': '25.033', 'lon': '121.565', 'type': 'building'}
        p = Place.from_nominatim(data)
        assert p.name == 'Taipei 101', f"Expected name 'Taipei 101'"
        assert p.lat == 25.033, f"Expected lat 25.033"
        assert p.lon == 121.565, f"Expected lon 121.565"
        assert p.category == 'building', f"Expected category 'building'"
        print("  ✓ Test 4.2: from_nominatim works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 4.2: from_nominatim failed - {e}")

    print(f"\nExercise 4: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_5():
    """Test special methods for comparison."""
    print("\n" + "="*60)
    print("Testing Exercise 5: Special Methods for Comparison")
    print("="*60)

    tests_passed = 0
    tests_total = 0

    # Test 5.1: __eq__
    tests_total += 1
    try:
        p1 = Place("Pizza", (25.0, 121.0), 4.5)
        p2 = Place("Pizza", (25.0, 121.0), 4.8)  # Different rating
        p3 = Place("Burger", (25.0, 121.0), 4.5)  # Different name

        assert p1 == p2, "Places with same name and coords should be equal"
        assert p1 != p3, "Places with different names should not be equal"
        assert p1 != "Pizza", "Place should not equal a string"
        print("  ✓ Test 5.1: __eq__ works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 5.1: __eq__ failed - {e}")

    # Test 5.2: __hash__
    tests_total += 1
    try:
        p1 = Place("Pizza", (25.0, 121.0))
        p2 = Place("Pizza", (25.0, 121.0))

        # Should be usable in set
        place_set = {p1, p2}
        assert len(place_set) == 1, "Equal places should hash to same value"

        # Should be usable as dict key
        place_dict = {p1: "favorite"}
        assert place_dict[p2] == "favorite", "Equal places should work as dict keys"

        print("  ✓ Test 5.2: __hash__ works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 5.2: __hash__ failed - {e}")

    # Test 5.3: __lt__
    tests_total += 1
    try:
        p1 = Place("A", (0, 0), 4.2)
        p2 = Place("B", (0, 0), 4.5)
        p3 = Place("C", (0, 0))  # No rating

        assert p1 < p2, "Place with lower rating should be less than"
        assert p3 < p1, "Place with no rating should be less than rated place"

        places = [p1, p2, p3]
        sorted_places = sorted(places, reverse=True)
        assert sorted_places[0].name == 'B', "Highest rated should be first"
        assert sorted_places[-1].name == 'C', "Unrated should be last"

        print("  ✓ Test 5.3: __lt__ works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 5.3: __lt__ failed - {e}")

    print(f"\nExercise 5: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_6():
    """Test basic decorators."""
    print("\n" + "="*60)
    print("Testing Exercise 6: Basic Decorators")
    print("="*60)

    tests_passed = 0
    tests_total = 0

    # Test 6.1: timer decorator
    tests_total += 1
    try:
        @timer
        def slow_func():
            time.sleep(0.1)
            return "done"

        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            result = slow_func()

        output = f.getvalue()
        assert result == "done", "Timer should return function result"
        assert "slow_func" in output, "Timer should print function name"
        assert "0.1" in output or "0.10" in output, "Timer should print elapsed time"

        print("  ✓ Test 6.1: timer decorator works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 6.1: timer decorator failed - {e}")

    # Test 6.2: log_calls decorator
    tests_total += 1
    try:
        @log_calls
        def add(a, b):
            return a + b

        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            result = add(2, 3)

        output = f.getvalue()
        assert result == 5, "log_calls should return function result"
        assert "add" in output, "log_calls should print function name"
        assert "2" in output and "3" in output, "log_calls should print arguments"
        assert "5" in output, "log_calls should print return value"

        print("  ✓ Test 6.2: log_calls decorator works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 6.2: log_calls decorator failed - {e}")

    # Test 6.3: retry decorator
    tests_total += 1
    try:
        attempt_count = [0]

        @retry(max_attempts=3, delay=0.01)
        def flaky_func():
            attempt_count[0] += 1
            if attempt_count[0] < 3:
                raise ValueError("Flaky!")
            return "success"

        result = flaky_func()
        assert result == "success", "retry should eventually succeed"
        assert attempt_count[0] == 3, f"Should have taken 3 attempts, took {attempt_count[0]}"

        # Test that it fails after max attempts
        attempt_count[0] = 0

        @retry(max_attempts=2, delay=0.01)
        def always_fail():
            attempt_count[0] += 1
            raise ValueError("Always fails")

        try:
            always_fail()
            print("  ✗ Test 6.3: retry should raise after max attempts")
        except ValueError:
            assert attempt_count[0] == 2, "Should have tried exactly max_attempts times"
            print("  ✓ Test 6.3: retry decorator works correctly")
            tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 6.3: retry decorator failed - {e}")

    print(f"\nExercise 6: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_7():
    """Test rate limit decorator."""
    print("\n" + "="*60)
    print("Testing Exercise 7: Rate Limit Decorator")
    print("="*60)

    tests_passed = 0
    tests_total = 0

    # Test 7.1: rate_limit decorator
    tests_total += 1
    try:
        @rate_limit(seconds=0.2)
        def fast_api():
            return time.time()

        t1 = fast_api()
        t2 = fast_api()

        elapsed = t2 - t1
        assert elapsed >= 0.18, f"Rate limit should enforce minimum delay, got {elapsed:.3f}s"

        print("  ✓ Test 7.1: rate_limit decorator works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 7.1: rate_limit decorator failed - {e}")

    # Test 7.2: RateLimiter class
    tests_total += 1
    try:
        limiter = RateLimiter(calls_per_second=5)  # 0.2 second interval

        @limiter
        def func1():
            return time.time()

        @limiter
        def func2():
            return time.time()

        t1 = func1()
        t2 = func2()  # Should share rate limit

        elapsed = t2 - t1
        assert elapsed >= 0.18, f"RateLimiter should be shared, got {elapsed:.3f}s"

        print("  ✓ Test 7.2: RateLimiter class works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 7.2: RateLimiter class failed - {e}")

    print(f"\nExercise 7: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def test_exercise_8():
    """Test PlaceService."""
    print("\n" + "="*60)
    print("Testing Exercise 8: PlaceService")
    print("="*60)

    tests_passed = 0
    tests_total = 0

    # First we need working Place class - create test places
    try:
        service = PlaceService()
        p1 = Place("Pizza", (25.033, 121.565), 4.5, "restaurant")
        p2 = Place("Burger", (25.034, 121.566), 4.2, "restaurant")
        p3 = Place("Park", (25.035, 121.567), 4.8, "park")
        p4 = Place("Cafe", (25.036, 121.568), None, "cafe")
    except Exception as e:
        print(f"  ✗ Cannot create test places - Exercise 1 must pass first: {e}")
        return False

    # Test add
    tests_total += 1
    try:
        service.add(p1)
        service.add(p2)
        service.add(p3)
        service.add(p4)
        assert len(service.places) == 4, f"Expected 4 places, got {len(service.places)}"
        print("  ✓ Test 8.1: add works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 8.1: add failed - {e}")

    # Test filter_by_rating
    tests_total += 1
    try:
        filtered = service.filter_by_rating(4.3)
        assert len(filtered) == 2, f"Expected 2 places with rating >= 4.3, got {len(filtered)}"
        names = {p.name for p in filtered}
        assert names == {"Pizza", "Park"}, f"Expected Pizza and Park, got {names}"
        print("  ✓ Test 8.2: filter_by_rating works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 8.2: filter_by_rating failed - {e}")

    # Test filter_by_category
    tests_total += 1
    try:
        filtered = service.filter_by_category("restaurant")
        assert len(filtered) == 2, f"Expected 2 restaurants, got {len(filtered)}"
        print("  ✓ Test 8.3: filter_by_category works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 8.3: filter_by_category failed - {e}")

    # Test sort_by_rating
    tests_total += 1
    try:
        sorted_places = service.sort_by_rating(descending=True)
        assert sorted_places[0].name == "Park", f"Expected Park first (4.8), got {sorted_places[0].name}"
        print("  ✓ Test 8.4: sort_by_rating works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 8.4: sort_by_rating failed - {e}")

    # Test find_nearest
    tests_total += 1
    try:
        reference = Place("Ref", (25.033, 121.565))
        nearest = service.find_nearest(reference)
        assert nearest.name == "Pizza", f"Expected Pizza as nearest, got {nearest.name}"
        print("  ✓ Test 8.5: find_nearest works correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Test 8.5: find_nearest failed - {e}")

    print(f"\nExercise 8: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("Week 12 Lab: OOP & Decorators - Test Suite")
    print("="*60)

    results = {
        'ex1': test_exercise_1(),
        'ex2': test_exercise_2(),
        'ex3': test_exercise_3(),
        'ex4': test_exercise_4(),
        'ex5': test_exercise_5(),
        'ex6': test_exercise_6(),
        'ex7': test_exercise_7(),
        'ex8': test_exercise_8(),
    }

    print("\n" + "="*60)
    print("Summary")
    print("="*60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for ex, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {ex}: {status}")

    print(f"\nTotal: {passed}/{total} exercises passed")

    if passed == total:
        print("\n🎉 All tests passed! Great job!")
    else:
        print(f"\n💪 Keep working! {total - passed} exercise(s) remaining.")

    return passed == total


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        if len(sys.argv) > 2:
            test_name = sys.argv[2]
            test_func = {
                'ex1': test_exercise_1,
                'ex2': test_exercise_2,
                'ex3': test_exercise_3,
                'ex4': test_exercise_4,
                'ex5': test_exercise_5,
                'ex6': test_exercise_6,
                'ex7': test_exercise_7,
                'ex8': test_exercise_8,
            }.get(test_name)

            if test_func:
                test_func()
            else:
                print(f"Unknown test: {test_name}")
                print("Available: ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8")
        else:
            print("Usage: python week12_starter.py --test <exercise>")
            print("Available: ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8")
    else:
        run_all_tests()
