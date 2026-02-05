"""
Week 6 Lab: Searching for Places (Lazy Loading)
Starter Code with Test Cases

This file contains starter code for all exercises.
Complete the TODO sections and run the tests to verify your solutions.

Usage:
    python week06_starter.py              # Run all tests
    python week06_starter.py --cli        # Run food search CLI
    python week06_starter.py --demo       # Run generator demos
"""

import requests
import time
import sys
import math
from typing import Generator, TypeVar, Callable, Iterable, Optional

T = TypeVar('T')

# =============================================================================
# Configuration
# =============================================================================

USER_AGENT = "CS101-Lab/1.0 (your-email@university.edu)"
BASE_URL = "https://nominatim.openstreetmap.org"


# =============================================================================
# Exercise 1: Basic Generators
# =============================================================================

def count_to(n: int):
    """
    Generator that counts from 1 to n.

    Args:
        n: The number to count to

    Yields:
        Integers from 1 to n

    Example:
        >>> list(count_to(5))
        [1, 2, 3, 4, 5]
    """
    # TODO: Implement this generator
    # Hint: Use a for loop with range and yield each number
    pass


def squares(n: int):
    """
    Generator that yields squares from 1^2 to n^2.

    Args:
        n: How many squares to generate

    Yields:
        1, 4, 9, 16, ..., n^2

    Example:
        >>> list(squares(5))
        [1, 4, 9, 16, 25]
    """
    # TODO: Implement this generator
    pass


def fibonacci(max_count: int = None):
    """
    Generator that yields Fibonacci numbers.

    Args:
        max_count: Maximum numbers to yield (None for infinite)

    Yields:
        0, 1, 1, 2, 3, 5, 8, 13, ...

    Example:
        >>> list(fibonacci(8))
        [0, 1, 1, 2, 3, 5, 8, 13]
    """
    # TODO: Implement this generator
    # Hint: Use a, b = b, a + b for Fibonacci logic
    pass


# =============================================================================
# Exercise 2: Generator Utilities
# =============================================================================

def take(n: int, iterable: Iterable[T]) -> list[T]:
    """
    Take the first n items from an iterable.

    Args:
        n: Number of items to take
        iterable: Source iterable

    Returns:
        List of first n items

    Example:
        >>> take(3, count_to(10))
        [1, 2, 3]
    """
    # TODO: Implement this function
    # Hint: Use a for loop and break after n items
    pass


def skip(n: int, iterable: Iterable[T]) -> Generator[T, None, None]:
    """
    Skip the first n items and yield the rest.

    Args:
        n: Number of items to skip
        iterable: Source iterable

    Yields:
        Items after the first n

    Example:
        >>> list(skip(3, count_to(6)))
        [4, 5, 6]
    """
    # TODO: Implement this generator
    pass


def take_while(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Generator[T, None, None]:
    """
    Yield items while predicate returns True.

    Args:
        predicate: Function that returns True/False
        iterable: Source iterable

    Yields:
        Items until predicate returns False

    Example:
        >>> list(take_while(lambda x: x < 5, count_to(10)))
        [1, 2, 3, 4]
    """
    # TODO: Implement this generator
    pass


# =============================================================================
# Exercise 3: API Result Handling
# =============================================================================

def extract_place_ids(results: list) -> list:
    """
    Extract place IDs from API results.

    Args:
        results: List of place dictionaries from Nominatim

    Returns:
        List of place ID integers

    Example:
        >>> results = [{"place_id": 101}, {"place_id": 102}]
        >>> extract_place_ids(results)
        [101, 102]
    """
    # TODO: Implement this function
    pass


def build_exclude_param(place_ids: list) -> str:
    """
    Build the exclude_place_ids parameter string.

    Args:
        place_ids: List of place IDs to exclude

    Returns:
        Comma-separated string of place IDs

    Example:
        >>> build_exclude_param([101, 102, 103])
        '101,102,103'
    """
    # TODO: Implement this function
    pass


def get_safe_limit(requested: int) -> int:
    """
    Return a safe limit value for Nominatim (max 40).

    Args:
        requested: The requested limit

    Returns:
        The safe limit (capped at 40)

    Example:
        >>> get_safe_limit(10)
        10
        >>> get_safe_limit(50)
        40
    """
    # TODO: Implement this function
    # Hint: Use min() to cap the value
    pass


# =============================================================================
# Exercise 4: Lazy API Generator
# =============================================================================

def search_places_paginated(
    query: str,
    batch_size: int = 10,
    max_batches: int = 5
) -> Generator[dict, None, None]:
    """
    Generator that fetches places batch by batch using exclude_place_ids.

    Args:
        query: Search query
        batch_size: Results per batch (max 40 for Nominatim)
        max_batches: Maximum batches to fetch

    Yields:
        Dictionary with place information:
        - name: Display name
        - lat: Latitude (float)
        - lon: Longitude (float)
        - type: Place type
    """
    url = f"{BASE_URL}/search"
    headers = {"User-Agent": USER_AGENT}

    # TODO: Implement the lazy generator
    # 1. Create an empty list to track exclude_ids
    # 2. Loop through batches (0 to max_batches-1)
    # 3. Build params: q, format, limit (use min(batch_size, 40))
    # 4. If exclude_ids is not empty, add exclude_place_ids param
    # 5. Make API request
    # 6. Handle errors (return on failure)
    # 7. If no results, return (stop generator)
    # 8. For each result: add place_id to exclude_ids, then yield dict
    # 9. Add time.sleep(1) between batches for rate limiting

    pass


# =============================================================================
# Exercise 5: Advanced Search with Filters
# =============================================================================

def search_places_advanced(
    query: str,
    country: Optional[str] = None,
    place_type: Optional[str] = None,
    max_results: Optional[int] = None,
    batch_size: int = 10
) -> Generator[dict, None, None]:
    """
    Advanced place search with filtering.

    Args:
        query: Search query
        country: ISO country code (e.g., "tw", "jp")
        place_type: Filter by type (e.g., "cafe", "restaurant")
        max_results: Maximum results to yield
        batch_size: Results per API call (max 40)

    Yields:
        Dictionary with place info
    """
    url = f"{BASE_URL}/search"
    headers = {"User-Agent": USER_AGENT}

    exclude_ids = []
    count = 0

    # TODO: Implement advanced search generator
    # 1. Build params with optional countrycodes filter
    # 2. Use min(batch_size, 40) for limit (Nominatim max is 40)
    # 3. Add exclude_place_ids if we have previous results
    # 4. Loop until no more results or max_results reached
    # 5. For each result:
    #    - Add place_id to exclude_ids
    #    - If place_type specified, check if type matches (partial match)
    #    - If max_results specified, stop when count reaches it
    #    - Yield the place info
    # 6. Add rate limiting between batches

    pass


# =============================================================================
# Exercise 6: Food Search CLI
# =============================================================================

def search_food(food_type: str, location: str) -> Generator[dict, None, None]:
    """
    Search for food places.

    Args:
        food_type: Type of food (pizza, sushi, etc.)
        location: Location to search

    Yields:
        Place information dictionaries
    """
    query = f"{food_type} {location}"
    url = f"{BASE_URL}/search"
    headers = {"User-Agent": USER_AGENT}

    exclude_ids = []
    batch_size = 10

    while True:
        params = {
            "q": query,
            "format": "json",
            "limit": min(batch_size, 40),  # Nominatim max is 40
            "addressdetails": 1
        }

        if exclude_ids:
            params["exclude_place_ids"] = ",".join(map(str, exclude_ids))

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)

            if response.status_code != 200:
                return

            results = response.json()

            if not results:
                return

            for place in results:
                address = place.get("address", {})
                exclude_ids.append(place["place_id"])  # Track for exclusion
                yield {
                    "name": place.get("name", place.get("display_name", "Unknown")),
                    "display_name": place.get("display_name", ""),
                    "lat": float(place.get("lat", 0)),
                    "lon": float(place.get("lon", 0)),
                    "type": place.get("type", "unknown"),
                    "district": address.get("suburb", address.get("district", "")),
                    "city": address.get("city", address.get("town", ""))
                }

            time.sleep(1)

        except requests.RequestException as e:
            print(f"  Network error: {e}")
            return


def display_result(place: dict, index: int):
    """Display a single result nicely."""
    print(f"\n{index}. {place['name']}")
    location_parts = []
    if place.get('district'):
        location_parts.append(place['district'])
    if place.get('city'):
        location_parts.append(place['city'])
    if location_parts:
        print(f"   {', '.join(location_parts)}")
    print(f"   ({place['lat']:.6f}, {place['lon']:.6f})")


def food_search_cli():
    """
    Interactive food search CLI.
    """
    print("\n" + "="*50)
    print("     What Do You Want to Eat?")
    print("="*50)

    while True:
        # Get food type
        food = input("\nWhat type of food? (Enter for 'restaurant'): ").strip()
        if not food:
            food = "restaurant"

        # Get location
        location = input("Where? (Enter for 'taipei'): ").strip()
        if not location:
            location = "taipei"

        print(f"\nSearching for '{food}' in '{location}'...")
        print("(Results load on demand)")

        # Create search generator
        search = search_food(food, location)

        # Display results in batches
        count = 0
        batch_size = 3

        while True:
            # Show next batch
            print(f"\n--- Results {count + 1} to {count + batch_size} ---")

            found_in_batch = 0
            for i in range(batch_size):
                try:
                    place = next(search)
                    count += 1
                    display_result(place, count)
                    found_in_batch += 1
                except StopIteration:
                    break

            if found_in_batch == 0:
                print("\nNo more results found.")
                break

            # Ask user what to do
            print("\n[Enter] More | [n] New search | [q] Quit")
            action = input(": ").strip().lower()

            if action == 'q':
                print(f"\nShowed {count} results. Goodbye!")
                return
            elif action == 'n':
                break  # Break inner loop, continue outer loop

        # Check if user wants to quit after new search prompt
        if action == 'q':
            return


# =============================================================================
# Test Functions
# =============================================================================

def test_exercise_1():
    """Test basic generators."""
    print("\n" + "="*60)
    print("Testing Exercise 1: Basic Generators")
    print("="*60)

    tests_passed = 0
    total_tests = 3

    # Test count_to
    try:
        result = list(count_to(5))
        if result == [1, 2, 3, 4, 5]:
            print("  count_to: PASS")
            tests_passed += 1
        else:
            print(f"  count_to: FAIL - got {result}")
    except Exception as e:
        print(f"  count_to: FAIL - {e}")

    # Test squares
    try:
        result = list(squares(5))
        if result == [1, 4, 9, 16, 25]:
            print("  squares: PASS")
            tests_passed += 1
        else:
            print(f"  squares: FAIL - got {result}")
    except Exception as e:
        print(f"  squares: FAIL - {e}")

    # Test fibonacci
    try:
        result = list(fibonacci(10))
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        if result == expected:
            print("  fibonacci: PASS")
            tests_passed += 1
        else:
            print(f"  fibonacci: FAIL - got {result}")
    except Exception as e:
        print(f"  fibonacci: FAIL - {e}")

    print(f"\n  Result: {tests_passed}/{total_tests} tests passed")
    return tests_passed == total_tests


def test_exercise_2():
    """Test generator utilities."""
    print("\n" + "="*60)
    print("Testing Exercise 2: Generator Utilities")
    print("="*60)

    tests_passed = 0
    total_tests = 3

    # Test take
    try:
        result = take(3, count_to(10))
        if result == [1, 2, 3]:
            print("  take: PASS")
            tests_passed += 1
        else:
            print(f"  take: FAIL - got {result}")
    except Exception as e:
        print(f"  take: FAIL - {e}")

    # Test skip
    try:
        result = list(skip(3, count_to(6)))
        if result == [4, 5, 6]:
            print("  skip: PASS")
            tests_passed += 1
        else:
            print(f"  skip: FAIL - got {result}")
    except Exception as e:
        print(f"  skip: FAIL - {e}")

    # Test take_while
    try:
        result = list(take_while(lambda x: x < 5, count_to(10)))
        if result == [1, 2, 3, 4]:
            print("  take_while: PASS")
            tests_passed += 1
        else:
            print(f"  take_while: FAIL - got {result}")
    except Exception as e:
        print(f"  take_while: FAIL - {e}")

    print(f"\n  Result: {tests_passed}/{total_tests} tests passed")
    return tests_passed == total_tests


def test_exercise_3():
    """Test result handling functions."""
    print("\n" + "="*60)
    print("Testing Exercise 3: Result Handling")
    print("="*60)

    tests_passed = 0
    total_tests = 3

    # Test extract_place_ids
    try:
        results = [{"place_id": 101, "name": "A"}, {"place_id": 102, "name": "B"}]
        if extract_place_ids(results) == [101, 102]:
            print("  extract_place_ids: PASS")
            tests_passed += 1
        else:
            print("  extract_place_ids: FAIL")
    except Exception as e:
        print(f"  extract_place_ids: FAIL - {e}")

    # Test build_exclude_param
    try:
        if (build_exclude_param([101, 102, 103]) == "101,102,103" and
            build_exclude_param([]) == ""):
            print("  build_exclude_param: PASS")
            tests_passed += 1
        else:
            print("  build_exclude_param: FAIL")
    except Exception as e:
        print(f"  build_exclude_param: FAIL - {e}")

    # Test get_safe_limit
    try:
        if (get_safe_limit(10) == 10 and
            get_safe_limit(50) == 40 and
            get_safe_limit(40) == 40):
            print("  get_safe_limit: PASS")
            tests_passed += 1
        else:
            print("  get_safe_limit: FAIL")
    except Exception as e:
        print(f"  get_safe_limit: FAIL - {e}")

    print(f"\n  Result: {tests_passed}/{total_tests} tests passed")
    return tests_passed == total_tests


def test_exercise_4():
    """Test lazy search."""
    print("\n" + "="*60)
    print("Testing Exercise 4: Lazy Search")
    print("="*60)

    print("  Making API request (this may take a few seconds)...")

    try:
        search = search_places_paginated("cafe taipei", batch_size=5, max_batches=1)

        results = []
        for i, place in enumerate(search):
            results.append(place)
            print(f"    {i+1}. {place.get('name', 'Unknown')[:40]}...")
            if i >= 2:
                break

        if len(results) > 0 and "name" in results[0] and "lat" in results[0]:
            print(f"\n  lazy_search: PASS ({len(results)} results)")
            return True
        else:
            print("  lazy_search: FAIL - invalid results")
            return False

    except Exception as e:
        print(f"  lazy_search: FAIL - {e}")
        return False


def test_exercise_5():
    """Test advanced search."""
    print("\n" + "="*60)
    print("Testing Exercise 5: Advanced Search")
    print("="*60)

    print("  Testing with max_results=3...")

    try:
        search = search_places_advanced("museum", max_results=3)
        results = list(search)

        if len(results) <= 3 and len(results) > 0:
            print(f"  Got {len(results)} results (max was 3)")
            print("  advanced_search: PASS")
            return True
        else:
            print(f"  advanced_search: FAIL - got {len(results)} results")
            return False

    except Exception as e:
        print(f"  advanced_search: FAIL - {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("WEEK 6 LAB - AUTOMATED TESTS")
    print("="*60)

    results = {}

    results["Exercise 1"] = test_exercise_1()
    results["Exercise 2"] = test_exercise_2()
    results["Exercise 3"] = test_exercise_3()

    print("\n  Pausing for rate limiting...")
    time.sleep(1)

    results["Exercise 4"] = test_exercise_4()

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
        print("\n*** All tests passed! Try --cli for the food search. ***")
    else:
        print("\n*** Some tests failed. Review and fix before continuing. ***")


def demo_generators():
    """Demonstrate generator concepts."""
    print("\n" + "="*60)
    print("Generator Demonstration")
    print("="*60)

    # Demo 1: Basic generator
    print("\n1. Basic count_to generator:")
    print("   Creating generator: gen = count_to(5)")
    gen = count_to(5)
    print(f"   Generator object: {gen}")
    print("   Calling next(gen) three times:")
    for i in range(3):
        try:
            print(f"     next(gen) = {next(gen)}")
        except (StopIteration, TypeError):
            print("     (generator not implemented)")
            break

    # Demo 2: Lazy evaluation
    print("\n2. Lazy evaluation with infinite Fibonacci:")
    print("   fib = fibonacci() creates infinite generator")
    print("   But we only take first 10:")
    fib = fibonacci(10) if fibonacci(10) else []
    print(f"   {list(fib) if fib else '(not implemented)'}")

    # Demo 3: Generator expression
    print("\n3. Generator expression vs list comprehension:")
    print("   List: [x**2 for x in range(5)] = ", end="")
    print([x**2 for x in range(5)])
    print("   Generator: (x**2 for x in range(5)) = ", end="")
    gen_exp = (x**2 for x in range(5))
    print(f"{gen_exp}")
    print("   Consuming generator:", list(gen_exp))


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == "--cli":
            food_search_cli()
        elif arg == "--demo":
            demo_generators()
        elif arg == "--test":
            run_all_tests()
        else:
            print(f"Unknown argument: {arg}")
            print("Usage:")
            print("  python week06_starter.py          # Run tests")
            print("  python week06_starter.py --cli    # Food search CLI")
            print("  python week06_starter.py --demo   # Generator demos")
    else:
        print("Week 6 Lab: Searching for Places (Lazy Loading)")
        print("="*60)
        print("\nOptions:")
        print("  python week06_starter.py --test    Run all tests")
        print("  python week06_starter.py --cli     Food search CLI")
        print("  python week06_starter.py --demo    Generator demos")
        print()

        choice = input("Run tests? (y/n): ").strip().lower()
        if choice == 'y':
            run_all_tests()
