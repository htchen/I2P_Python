"""
Week 4 Lab: HTTP Requests & API Keys
Starter Code with Test Cases

This file contains starter code for all exercises.
Complete the TODO sections and run the tests to verify your solutions.

Usage:
    python week04_starter.py
"""

import requests
import time
import json

# Configuration - Update with your information
USER_AGENT = "CS101-Lab/1.0 (your-email@university.edu)"


# =============================================================================
# Exercise 1: HTTP Basics
# =============================================================================

def explore_response():
    """
    Make a request to httpbin.org and explore the response object.

    TODO:
    1. Make a GET request to https://httpbin.org/get
    2. Print the status code
    3. Print the Content-Type header
    4. Parse JSON and print the 'origin' field (your IP)
    5. Print whether the request was successful (response.ok)

    Returns:
        dict: The parsed JSON response
    """
    url = "https://httpbin.org/get"

    # YOUR CODE HERE
    pass


# =============================================================================
# Exercise 2: Query Parameters
# =============================================================================

def test_query_params() -> dict:
    """
    Send query parameters and verify they were received.

    TODO:
    1. Define params: city="Taipei", country="Taiwan", limit=5
    2. Make GET request to https://httpbin.org/get with params
    3. Parse response and return the 'args' field

    Returns:
        dict: The 'args' field from the response
    """
    url = "https://httpbin.org/get"

    # YOUR CODE HERE
    pass


# =============================================================================
# Exercise 3: Custom Headers
# =============================================================================

def test_headers() -> dict:
    """
    Send custom headers and verify they were received.

    TODO:
    1. Define headers: User-Agent, Accept, X-Custom-Header
    2. Make GET request to https://httpbin.org/headers
    3. Parse response and return the 'headers' field

    Returns:
        dict: The 'headers' field from the response
    """
    url = "https://httpbin.org/headers"

    # YOUR CODE HERE
    pass


# =============================================================================
# Exercise 4: First Nominatim Request
# =============================================================================

def geocode_place(place_name: str) -> dict | None:
    """
    Geocode a place name using Nominatim.

    TODO:
    1. Make GET request to Nominatim search endpoint
    2. Include proper User-Agent header (REQUIRED!)
    3. Use params: q=place_name, format=json, limit=1
    4. Set timeout to 10 seconds
    5. Parse response and return first result

    Args:
        place_name: Name of the place to search

    Returns:
        dict with 'display_name', 'lat', 'lon' or None if not found
    """
    url = "https://nominatim.openstreetmap.org/search"

    # YOUR CODE HERE
    pass


# =============================================================================
# Exercise 5: Error Handling
# =============================================================================

def safe_request(url: str, params: dict = None, headers: dict = None) -> dict | None:
    """
    Make an HTTP request with comprehensive error handling.

    TODO:
    1. Make GET request with 10 second timeout
    2. Handle Timeout exception
    3. Handle ConnectionError exception
    4. Handle HTTP errors (4xx, 5xx status codes)
    5. Return parsed JSON on success, None on failure

    Args:
        url: The URL to request
        params: Optional query parameters
        headers: Optional headers

    Returns:
        Parsed JSON response or None if failed
    """
    try:
        # YOUR CODE HERE
        pass

    except requests.exceptions.Timeout:
        print("Error: Request timed out")
        return None

    except requests.exceptions.ConnectionError:
        print("Error: Connection failed - check URL or network")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed - {e}")
        return None


# =============================================================================
# Exercise 6: Geocoder with Rate Limiting
# =============================================================================

def geocode_multiple(places: list[str]) -> list[dict]:
    """
    Geocode multiple places with rate limiting.

    TODO:
    1. Loop through places
    2. Wait 1 second between requests (rate limiting)
    3. Make Nominatim API request for each place
    4. Collect successful results
    5. Handle errors gracefully

    Args:
        places: List of place names to geocode

    Returns:
        List of dicts with 'name', 'lat', 'lon' for found places
    """
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": USER_AGENT}

    results = []

    for i, place in enumerate(places):
        print(f"[{i+1}/{len(places)}] Geocoding: {place}...")

        # YOUR CODE HERE

        pass

    return results


# =============================================================================
# Bonus: Reverse Geocoder
# =============================================================================

def reverse_geocode(lat: float, lon: float) -> str | None:
    """
    Convert coordinates to an address using Nominatim.

    TODO:
    1. Make GET request to Nominatim reverse endpoint
    2. Include proper User-Agent header
    3. Use params: lat, lon, format=json
    4. Return the 'display_name' field

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        Address string or None if not found
    """
    url = "https://nominatim.openstreetmap.org/reverse"

    # YOUR CODE HERE
    pass


# =============================================================================
# Test Cases
# =============================================================================

def test_exercise_1():
    """Test Exercise 1: HTTP Basics"""
    print("\n" + "="*60)
    print("Testing Exercise 1: HTTP Basics")
    print("="*60)

    result = explore_response()

    if result is None:
        print("FAIL: Function returned None")
        return False

    if 'origin' in result:
        print("PASS: Successfully retrieved response with 'origin' field")
        return True
    else:
        print("FAIL: Response missing 'origin' field")
        return False


def test_exercise_2():
    """Test Exercise 2: Query Parameters"""
    print("\n" + "="*60)
    print("Testing Exercise 2: Query Parameters")
    print("="*60)

    result = test_query_params()

    if result is None:
        print("FAIL: Function returned None")
        return False

    expected = {"city": "Taipei", "country": "Taiwan", "limit": "5"}

    for key, value in expected.items():
        if key not in result:
            print(f"FAIL: Missing parameter '{key}'")
            return False
        if result[key] != value:
            print(f"FAIL: Parameter '{key}' has wrong value")
            return False

    print("PASS: All parameters sent correctly")
    return True


def test_exercise_3():
    """Test Exercise 3: Custom Headers"""
    print("\n" + "="*60)
    print("Testing Exercise 3: Custom Headers")
    print("="*60)

    result = test_headers()

    if result is None:
        print("FAIL: Function returned None")
        return False

    # Check for custom header (case-insensitive check)
    headers_lower = {k.lower(): v for k, v in result.items()}

    if 'x-custom-header' not in headers_lower:
        print("FAIL: Missing X-Custom-Header")
        return False

    if 'user-agent' not in headers_lower:
        print("FAIL: Missing User-Agent")
        return False

    print("PASS: Custom headers sent correctly")
    return True


def test_exercise_4():
    """Test Exercise 4: First Nominatim Request"""
    print("\n" + "="*60)
    print("Testing Exercise 4: Nominatim Geocoding")
    print("="*60)

    result = geocode_place("National Taiwan University")

    if result is None:
        print("FAIL: Function returned None - check User-Agent header!")
        return False

    required_fields = ['display_name', 'lat', 'lon']
    for field in required_fields:
        if field not in result:
            print(f"FAIL: Missing field '{field}'")
            return False

    # Verify coordinates are in Taiwan
    lat = float(result['lat'])
    lon = float(result['lon'])

    if not (24 < lat < 26 and 120 < lon < 122):
        print(f"FAIL: Coordinates ({lat}, {lon}) don't look like Taiwan")
        return False

    print(f"PASS: Found {result['display_name'][:50]}...")
    print(f"       Coordinates: ({lat:.4f}, {lon:.4f})")
    return True


def test_exercise_5():
    """Test Exercise 5: Error Handling"""
    print("\n" + "="*60)
    print("Testing Exercise 5: Error Handling")
    print("="*60)

    # Test 1: Successful request
    print("\nTest 1: Successful request...")
    result1 = safe_request("https://httpbin.org/get")
    test1_pass = result1 is not None
    print(f"  {'PASS' if test1_pass else 'FAIL'}: Successful request handling")

    # Test 2: 404 error
    print("\nTest 2: 404 Not Found...")
    result2 = safe_request("https://httpbin.org/status/404")
    test2_pass = result2 is None
    print(f"  {'PASS' if test2_pass else 'FAIL'}: 404 error handling")

    # Test 3: Invalid URL (connection error)
    print("\nTest 3: Invalid URL...")
    result3 = safe_request("https://invalid.domain.example.com/test")
    test3_pass = result3 is None
    print(f"  {'PASS' if test3_pass else 'FAIL'}: Connection error handling")

    all_pass = test1_pass and test2_pass and test3_pass
    print(f"\nOverall: {'PASS' if all_pass else 'FAIL'}")
    return all_pass


def test_exercise_6():
    """Test Exercise 6: Geocoder with Rate Limiting"""
    print("\n" + "="*60)
    print("Testing Exercise 6: Multiple Geocoding")
    print("="*60)

    places = ["Taipei 101", "Taipei Main Station"]

    start_time = time.time()
    results = geocode_multiple(places)
    elapsed = time.time() - start_time

    if len(results) == 0:
        print("FAIL: No results returned")
        return False

    if elapsed < 1:
        print("FAIL: Rate limiting not implemented (too fast)")
        return False

    print(f"\nFound {len(results)}/{len(places)} places in {elapsed:.1f} seconds")

    for place in results:
        if 'name' not in place or 'lat' not in place or 'lon' not in place:
            print("FAIL: Result missing required fields")
            return False

    print("PASS: Multiple geocoding with rate limiting works")
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("WEEK 4 LAB - AUTOMATED TESTS")
    print("="*60)

    results = {}

    # Run Exercise 1-3 (httpbin.org - no rate limiting needed)
    results['Exercise 1'] = test_exercise_1()
    results['Exercise 2'] = test_exercise_2()
    results['Exercise 3'] = test_exercise_3()

    # Rate limit pause before Nominatim tests
    print("\nPausing 1 second before Nominatim tests...")
    time.sleep(1)

    # Run Exercise 4 (Nominatim)
    results['Exercise 4'] = test_exercise_4()
    time.sleep(1)

    # Run Exercise 5 (mixed)
    results['Exercise 5'] = test_exercise_5()
    time.sleep(1)

    # Run Exercise 6 (Nominatim multiple)
    results['Exercise 6'] = test_exercise_6()

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
        print("\n*** Congratulations! All exercises complete! ***")
    else:
        print("\n*** Keep working on the failed exercises ***")


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    print("Week 4 Lab: HTTP Requests & API Keys")
    print("="*60)
    print(f"User-Agent: {USER_AGENT}")
    print("\nOptions:")
    print("  1. Run all tests")
    print("  2. Run specific exercise test")
    print()

    choice = input("Enter choice (1 or 2), or press Enter to run all: ").strip()

    if choice == "2":
        ex_num = input("Enter exercise number (1-6): ").strip()
        test_funcs = {
            "1": test_exercise_1,
            "2": test_exercise_2,
            "3": test_exercise_3,
            "4": test_exercise_4,
            "5": test_exercise_5,
            "6": test_exercise_6,
        }
        if ex_num in test_funcs:
            test_funcs[ex_num]()
        else:
            print("Invalid exercise number")
    else:
        run_all_tests()
