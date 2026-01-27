"""
Week 5 Lab: The Nominatim API (Geocoding)
Starter Code with Test Cases

This file contains starter code for all exercises.
Complete the TODO sections and run the tests to verify your solutions.

Usage:
    python week05_starter.py
    python week05_starter.py --test       # Run all tests
    python week05_starter.py --cli        # Run interactive CLI
    python week05_starter.py "Taipei 101" # Quick geocode
"""

import requests
import time
import json
import sys
from pathlib import Path


# =============================================================================
# Configuration
# =============================================================================

USER_AGENT = "CS101-Lab/1.0 (your-email@university.edu)"
BASE_URL = "https://nominatim.openstreetmap.org"


# =============================================================================
# Custom Exceptions
# =============================================================================

class GeocodingError(Exception):
    """Base exception for geocoding errors."""
    pass


class NetworkError(GeocodingError):
    """Network-related errors."""
    pass


class NotFoundError(GeocodingError):
    """Place not found."""
    pass


class RateLimitError(GeocodingError):
    """Rate limit exceeded."""
    pass


# =============================================================================
# Exercise 1: Safe Dictionary Access
# =============================================================================

def safe_get(data: dict, *keys, default=None):
    """
    Safely get a nested value from a dictionary.

    Args:
        data: The dictionary to search
        *keys: The keys to traverse
        default: Value to return if path doesn't exist

    Returns:
        The value at the path, or default if not found

    Examples:
        >>> d = {"a": {"b": {"c": 1}}}
        >>> safe_get(d, "a", "b", "c")
        1
        >>> safe_get(d, "a", "x", default="N/A")
        'N/A'
    """
    # TODO: Implement this function
    # Hint: Loop through keys, checking if each level exists
    pass


# =============================================================================
# Exercise 2: Parse Nominatim Response
# =============================================================================

def parse_place(result: dict) -> dict:
    """
    Parse a single Nominatim result into a clean structure.

    Args:
        result: Raw result from Nominatim API

    Returns:
        Dictionary with:
        - name: str (the place name)
        - lat: float (latitude)
        - lon: float (longitude)
        - display_name: str (full address)
        - place_type: str (in format "class:type")
        - importance: float (relevance score, default 0.0)
    """
    # TODO: Implement this function
    # Remember: lat/lon are strings in the API response!
    pass


# =============================================================================
# Exercise 3: Format Address
# =============================================================================

def format_address(result: dict) -> str:
    """
    Format an address from a Nominatim result.

    Args:
        result: Nominatim result with 'address' field

    Returns:
        Formatted address string like:
        "7 Section 5 Xinyi Road, Xinyi District, Taipei, Taiwan"

    If address is missing or empty, return "Unknown location"
    """
    # TODO: Implement this function
    # Hint: Try multiple keys for each part (city vs town vs village, etc.)
    pass


# =============================================================================
# Exercise 4: Error Handling
# =============================================================================

def geocode(query: str) -> dict:
    """
    Geocode a place name with comprehensive error handling.

    Args:
        query: Place name to search

    Returns:
        Dictionary with name, lat, lon, display_name

    Raises:
        NotFoundError: If no results found
        RateLimitError: If rate limit exceeded (429)
        NetworkError: For other network/HTTP errors
        GeocodingError: For parsing errors
    """
    url = f"{BASE_URL}/search"
    headers = {"User-Agent": USER_AGENT}
    params = {"q": query, "format": "json", "limit": 1, "addressdetails": 1}

    # TODO: Implement with full error handling
    # Handle: Timeout, ConnectionError, HTTP errors (especially 429), empty results
    pass


# =============================================================================
# Exercise 5: Geocoder Class
# =============================================================================

class Geocoder:
    """A complete geocoding client with forward and reverse geocoding."""

    def __init__(self, user_agent: str):
        """
        Initialize the geocoder.

        Args:
            user_agent: User-Agent string for API requests
        """
        self.headers = {"User-Agent": user_agent}
        self.last_request = 0

    def _rate_limit(self):
        """Ensure at least 1 second between requests."""
        # TODO: Implement rate limiting
        # Hint: Check time.time() - self.last_request
        pass

    def forward(self, query: str) -> dict | None:
        """
        Convert a place name to coordinates.

        Args:
            query: Place name to search

        Returns:
            Dict with name, lat, lon, display_name or None if not found
        """
        # TODO: Implement forward geocoding
        # Remember to call self._rate_limit() first!
        pass

    def reverse(self, lat: float, lon: float) -> dict | None:
        """
        Convert coordinates to an address.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Dict with display_name, address components or None if not found
        """
        # TODO: Implement reverse geocoding
        pass

    def batch_forward(self, queries: list[str]) -> list[dict]:
        """
        Geocode multiple places.

        Args:
            queries: List of place names

        Returns:
            List of results (only successful geocodes)
        """
        # TODO: Implement batch geocoding with rate limiting
        pass


# =============================================================================
# Exercise 6: CLI Functions
# =============================================================================

def print_forward_result(result: dict):
    """Pretty print a forward geocoding result."""
    print()
    print(f"  Name: {result.get('name', 'N/A')}")
    print(f"  Coordinates: ({result['lat']:.6f}, {result['lon']:.6f})")
    print(f"  Address: {result.get('display_name', 'N/A')}")
    print()


def print_reverse_result(result: dict):
    """Pretty print a reverse geocoding result."""
    print()
    print(f"  Address: {result['display_name']}")
    if 'address' in result:
        print("  Components:")
        for key, value in list(result['address'].items())[:8]:
            print(f"    {key}: {value}")
    print()


def run_cli():
    """Run the interactive CLI."""
    print("\n=== Geocoder CLI ===")
    print("Commands:")
    print("  <place name>          - Search for a place")
    print("  reverse <lat> <lon>   - Reverse geocode coordinates")
    print("  help                  - Show this help")
    print("  quit                  - Exit")
    print()

    geocoder = Geocoder(USER_AGENT)

    while True:
        try:
            user_input = input("geocoder> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        # TODO: Implement CLI command handling
        # 1. Handle 'quit' and 'exit'
        # 2. Handle 'help'
        # 3. Handle 'reverse lat lon'
        # 4. Handle forward geocoding (default)
        # 5. Handle errors gracefully

        pass


# =============================================================================
# Test Functions
# =============================================================================

def test_exercise_1():
    """Test safe_get function."""
    print("\n" + "="*60)
    print("Testing Exercise 1: safe_get")
    print("="*60)

    data = {
        "address": {
            "city": "Taipei",
            "district": "Xinyi",
            "details": {"postcode": "110"}
        },
        "name": "Taipei 101"
    }

    tests = [
        (safe_get(data, "name") == "Taipei 101", "Simple access"),
        (safe_get(data, "address", "city") == "Taipei", "Nested access"),
        (safe_get(data, "address", "details", "postcode") == "110", "Deep nested"),
        (safe_get(data, "address", "country", default="Unknown") == "Unknown", "Missing with default"),
        (safe_get(data, "location", "lat", default=0.0) == 0.0, "Missing intermediate"),
    ]

    passed = 0
    for result, description in tests:
        status = "PASS" if result else "FAIL"
        print(f"  {status}: {description}")
        if result:
            passed += 1

    print(f"\n  Result: {passed}/{len(tests)} tests passed")
    return passed == len(tests)


def test_exercise_2():
    """Test parse_place function."""
    print("\n" + "="*60)
    print("Testing Exercise 2: parse_place")
    print("="*60)

    result = {
        "lat": "25.0339639",
        "lon": "121.5644722",
        "name": "台北101",
        "display_name": "台北101, Xinyi Road, Taipei, Taiwan",
        "class": "tourism",
        "type": "attraction",
        "importance": 0.75
    }

    parsed = parse_place(result)

    if parsed is None:
        print("  FAIL: parse_place returned None")
        return False

    tests = [
        (parsed.get("name") == "台北101", "Name extraction"),
        (isinstance(parsed.get("lat"), float), "Lat is float"),
        (isinstance(parsed.get("lon"), float), "Lon is float"),
        (abs(parsed.get("lat", 0) - 25.0339639) < 0.0001, "Lat value correct"),
        (parsed.get("place_type") == "tourism:attraction", "Type extraction"),
    ]

    passed = 0
    for result, description in tests:
        status = "PASS" if result else "FAIL"
        print(f"  {status}: {description}")
        if result:
            passed += 1

    print(f"\n  Result: {passed}/{len(tests)} tests passed")
    return passed == len(tests)


def test_exercise_3():
    """Test format_address function."""
    print("\n" + "="*60)
    print("Testing Exercise 3: format_address")
    print("="*60)

    test_cases = [
        (
            {"address": {"road": "Xinyi Road", "city": "Taipei", "country": "Taiwan"}},
            ["Taipei", "Taiwan"],
            "Basic address"
        ),
        (
            {"address": {"country": "Japan"}},
            ["Japan"],
            "Country only"
        ),
        (
            {"address": {}},
            None,  # Should return non-empty string
            "Empty address"
        ),
        (
            {},
            None,  # Should return non-empty string
            "No address field"
        ),
    ]

    passed = 0
    for test_input, expected_parts, description in test_cases:
        result = format_address(test_input)

        if expected_parts is None:
            # Just check it returns something
            test_passed = result and len(result) > 0
        else:
            test_passed = all(part in result for part in expected_parts)

        status = "PASS" if test_passed else "FAIL"
        print(f"  {status}: {description}")
        print(f"         Got: '{result}'")
        if test_passed:
            passed += 1

    print(f"\n  Result: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_exercise_4():
    """Test geocode error handling."""
    print("\n" + "="*60)
    print("Testing Exercise 4: geocode error handling")
    print("="*60)

    # Test successful geocoding
    print("\n  Testing successful geocoding...")
    try:
        result = geocode("Taipei 101")
        if result and "lat" in result:
            print("  PASS: Successful geocoding works")
            test1 = True
        else:
            print("  FAIL: Geocoding returned invalid result")
            test1 = False
    except Exception as e:
        print(f"  FAIL: Unexpected error: {e}")
        test1 = False

    time.sleep(1)

    # Test not found
    print("\n  Testing NotFoundError...")
    try:
        geocode("xyzzy12345notarealplace")
        print("  FAIL: Should have raised NotFoundError")
        test2 = False
    except NotFoundError:
        print("  PASS: NotFoundError raised correctly")
        test2 = True
    except Exception as e:
        print(f"  FAIL: Wrong exception type: {type(e).__name__}")
        test2 = False

    all_passed = test1 and test2
    print(f"\n  Result: {'2/2' if all_passed else '?/2'} tests passed")
    return all_passed


def test_exercise_5():
    """Test Geocoder class."""
    print("\n" + "="*60)
    print("Testing Exercise 5: Geocoder class")
    print("="*60)

    geocoder = Geocoder(USER_AGENT)

    # Test forward geocoding
    print("\n  Testing forward geocoding...")
    result = geocoder.forward("Taipei Main Station")
    if result and "lat" in result:
        print(f"  PASS: Found {result.get('name', 'place')[:30]}...")
        test1 = True
    else:
        print("  FAIL: Forward geocoding failed")
        test1 = False

    # Test reverse geocoding
    print("\n  Testing reverse geocoding...")
    result = geocoder.reverse(25.0478, 121.5170)
    if result and "display_name" in result:
        print(f"  PASS: Found address")
        test2 = True
    else:
        print("  FAIL: Reverse geocoding failed")
        test2 = False

    # Test batch
    print("\n  Testing batch geocoding...")
    results = geocoder.batch_forward(["Taipei 101", "National Palace Museum"])
    if len(results) >= 1:
        print(f"  PASS: Found {len(results)} places")
        test3 = True
    else:
        print("  FAIL: Batch geocoding failed")
        test3 = False

    all_passed = test1 and test2 and test3
    print(f"\n  Result: {sum([test1, test2, test3])}/3 tests passed")
    return all_passed


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("WEEK 5 LAB - AUTOMATED TESTS")
    print("="*60)

    results = {}

    # Run tests (with rate limiting between API tests)
    results["Exercise 1"] = test_exercise_1()

    results["Exercise 2"] = test_exercise_2()

    results["Exercise 3"] = test_exercise_3()

    print("\n  Pausing for rate limiting...")
    time.sleep(1)

    results["Exercise 4"] = test_exercise_4()

    print("\n  Pausing for rate limiting...")
    time.sleep(1)

    results["Exercise 5"] = test_exercise_5()

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, passed_test in results.items():
        status = "PASS" if passed_test else "FAIL"
        print(f"  {name}: {status}")

    print(f"\nTotal: {passed}/{total} exercises passed")

    if passed == total:
        print("\n*** All tests passed! Ready for Exercise 6 (CLI). ***")
    else:
        print("\n*** Some tests failed. Review and fix before continuing. ***")


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == "--test":
            run_all_tests()
        elif arg == "--cli":
            run_cli()
        elif arg == "--help":
            print(__doc__)
        else:
            # Treat as geocode query
            query = " ".join(sys.argv[1:])
            try:
                result = geocode(query)
                if result:
                    print_forward_result(result)
                else:
                    print("Not found")
            except GeocodingError as e:
                print(f"Error: {e}")
    else:
        print("Week 5 Lab: The Nominatim API (Geocoding)")
        print("="*60)
        print("\nOptions:")
        print("  python week05_starter.py --test        Run all tests")
        print("  python week05_starter.py --cli         Interactive mode")
        print("  python week05_starter.py 'Taipei 101'  Quick geocode")
        print()

        choice = input("Run tests? (y/n): ").strip().lower()
        if choice == 'y':
            run_all_tests()
