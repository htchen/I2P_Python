"""
Week 6: Searching for Places (Lazy Loading)
Lecture Examples - Runnable Code

This file contains all the code examples from the Week 6 lecture.
Run this file to see the examples in action!

Usage:
    python examples.py

Note: Some examples make real API calls and require internet connection.
"""

import requests
import time
import sys
from typing import Generator, TypeVar, Callable, Iterable

T = TypeVar('T')

# =============================================================================
# Configuration
# =============================================================================

USER_AGENT = "CS101-Examples/1.0 (cs101@university.edu)"
BASE_URL = "https://nominatim.openstreetmap.org"


# =============================================================================
# Example 1: Regular Function vs Generator
# =============================================================================

def example_function_vs_generator():
    """Compare regular functions and generators."""
    print("\n" + "="*60)
    print("Example 1: Regular Function vs Generator")
    print("="*60)

    # Regular function - returns everything at once
    def get_numbers_list(n):
        result = []
        for i in range(1, n + 1):
            result.append(i)
        return result

    # Generator function - yields one at a time
    def get_numbers_generator(n):
        for i in range(1, n + 1):
            yield i

    print("\nRegular function:")
    numbers_list = get_numbers_list(5)
    print(f"  Type: {type(numbers_list)}")
    print(f"  Value: {numbers_list}")

    print("\nGenerator function:")
    numbers_gen = get_numbers_generator(5)
    print(f"  Type: {type(numbers_gen)}")
    print(f"  Value: {numbers_gen}")
    print("  Getting values one at a time:")
    print(f"    next(): {next(numbers_gen)}")
    print(f"    next(): {next(numbers_gen)}")
    print(f"    next(): {next(numbers_gen)}")
    print("  (remaining values not computed yet!)")


# =============================================================================
# Example 2: How yield Works
# =============================================================================

def example_yield_behavior():
    """Demonstrate how yield pauses and resumes."""
    print("\n" + "="*60)
    print("Example 2: How yield Works")
    print("="*60)

    def simple_generator():
        print("    Starting generator...")
        yield 1
        print("    After yield 1, before yield 2")
        yield 2
        print("    After yield 2, before yield 3")
        yield 3
        print("    Generator finished!")

    print("\nCreating generator (nothing printed yet):")
    gen = simple_generator()

    print("\nCalling next() first time:")
    value = next(gen)
    print(f"  Got: {value}")

    print("\nCalling next() second time:")
    value = next(gen)
    print(f"  Got: {value}")

    print("\nCalling next() third time:")
    value = next(gen)
    print(f"  Got: {value}")


# =============================================================================
# Example 3: Generators with for Loops
# =============================================================================

def example_generator_with_for():
    """Use generators with for loops."""
    print("\n" + "="*60)
    print("Example 3: Generators with for Loops")
    print("="*60)

    def countdown(n):
        print(f"  Starting countdown from {n}")
        while n > 0:
            yield n
            n -= 1
        print("  Blastoff!")

    print("\nUsing for loop with countdown(5):")
    for num in countdown(5):
        print(f"  {num}...")


# =============================================================================
# Example 4: Breaking Early from Generators
# =============================================================================

def example_break_early():
    """Demonstrate breaking early from generators."""
    print("\n" + "="*60)
    print("Example 4: Breaking Early (Lazy Evaluation)")
    print("="*60)

    def infinite_counter():
        n = 1
        while True:
            print(f"    Computing {n}...")
            yield n
            n += 1

    print("\nInfinite counter, but we only take 5:")
    for num in infinite_counter():
        print(f"  Got: {num}")
        if num >= 5:
            print("  Breaking early!")
            break

    print("\n  Numbers 6, 7, 8, ... were never computed!")


# =============================================================================
# Example 5: Memory Efficiency
# =============================================================================

def example_memory_efficiency():
    """Compare memory usage of lists vs generators."""
    print("\n" + "="*60)
    print("Example 5: Memory Efficiency")
    print("="*60)

    import sys

    # List stores all values
    def squares_list(n):
        return [x**2 for x in range(n)]

    # Generator stores only current state
    def squares_generator(n):
        for x in range(n):
            yield x**2

    n = 100_000

    big_list = squares_list(n)
    big_gen = squares_generator(n)

    print(f"\nFor {n:,} squares:")
    print(f"  List size: {sys.getsizeof(big_list):,} bytes")
    print(f"  Generator size: {sys.getsizeof(big_gen):,} bytes")
    print(f"\n  Generator is ~{sys.getsizeof(big_list) // sys.getsizeof(big_gen)}x smaller!")


# =============================================================================
# Example 6: Fibonacci Generator
# =============================================================================

def example_fibonacci():
    """Generate Fibonacci sequence lazily."""
    print("\n" + "="*60)
    print("Example 6: Fibonacci Generator")
    print("="*60)

    def fibonacci():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    print("\nFirst 15 Fibonacci numbers:")
    fib = fibonacci()
    for i in range(15):
        print(f"  F({i}) = {next(fib)}")


# =============================================================================
# Example 7: Generator Expressions
# =============================================================================

def example_generator_expressions():
    """Compare list comprehensions and generator expressions."""
    print("\n" + "="*60)
    print("Example 7: Generator Expressions")
    print("="*60)

    # List comprehension - creates list immediately
    squares_list = [x**2 for x in range(10)]

    # Generator expression - creates generator (lazy)
    squares_gen = (x**2 for x in range(10))

    print("\nList comprehension: [x**2 for x in range(10)]")
    print(f"  Type: {type(squares_list)}")
    print(f"  Value: {squares_list}")

    print("\nGenerator expression: (x**2 for x in range(10))")
    print(f"  Type: {type(squares_gen)}")
    print(f"  Value: {squares_gen}")
    print(f"  Consumed: {list(squares_gen)}")


# =============================================================================
# Example 8: Result Exclusion Basics
# =============================================================================

def example_pagination():
    """Demonstrate Nominatim result exclusion concepts."""
    print("\n" + "="*60)
    print("Example 8: Result Exclusion (Nominatim API)")
    print("="*60)

    print("\nNominatim API Key Facts:")
    print("  - Maximum 'limit' value: 40")
    print("  - No 'offset' parameter (doesn't exist!)")
    print("  - Use 'exclude_place_ids' to get more results")

    print("\nHow to get multiple batches:")
    print("  Batch 1: params = {'limit': 10}")
    print("           -> Returns results with place_ids: 101,102,103...")
    print("  Batch 2: params = {'limit': 10, 'exclude_place_ids': '101,102,103...'}")
    print("           -> Returns NEW results, excluding previous ones")

    def get_exclude_param(place_ids: list) -> str:
        """Convert list of place IDs to exclude parameter."""
        return ",".join(map(str, place_ids))

    # Demo
    example_ids = [101, 102, 103, 104, 105]
    print(f"\n  Example place_ids: {example_ids}")
    print(f"  exclude_place_ids param: '{get_exclude_param(example_ids)}'")


# =============================================================================
# Example 9: Lazy API Search with Exclusion
# =============================================================================

def example_paginated_search():
    """Demonstrate lazy API search using exclude_place_ids."""
    print("\n" + "="*60)
    print("Example 9: Lazy API Search (exclude_place_ids)")
    print("="*60)

    def search_places(query: str, batch_size: int = 5, max_batches: int = 2):
        """Generator that fetches places batch by batch."""
        url = f"{BASE_URL}/search"
        headers = {"User-Agent": USER_AGENT}
        exclude_ids = []

        for batch in range(max_batches):
            print(f"  [Fetching batch {batch + 1}...]")

            params = {
                "q": query,
                "format": "json",
                "limit": min(batch_size, 40)  # Nominatim max is 40
            }

            if exclude_ids:
                params["exclude_place_ids"] = ",".join(map(str, exclude_ids))

            try:
                response = requests.get(url, params=params, headers=headers, timeout=10)

                if response.status_code != 200:
                    return

                results = response.json()

                if not results:
                    print("  [No more results]")
                    return

                for place in results:
                    exclude_ids.append(place["place_id"])
                    yield {
                        "name": place.get("display_name", "Unknown")[:50],
                        "type": place.get("type", "unknown")
                    }

                time.sleep(1)  # Rate limiting

            except requests.RequestException as e:
                print(f"  [Error: {e}]")
                return

    print("\nSearching for 'museum taipei' (lazy loading):")
    search = search_places("museum taipei", batch_size=3, max_batches=2)

    print("\nGetting results one at a time:")
    for i, place in enumerate(search):
        print(f"  {i+1}. {place['name']}...")
        if i >= 4:
            print("  [Stopping early - remaining batches not fetched!]")
            break


# =============================================================================
# Example 10: Advanced Search with Filters
# =============================================================================

def example_advanced_search():
    """Demonstrate advanced search with filters."""
    print("\n" + "="*60)
    print("Example 10: Advanced Search with Filters")
    print("="*60)

    def search_places_advanced(
        query: str,
        country: str = None,
        max_results: int = None
    ):
        """Advanced search with filtering."""
        url = f"{BASE_URL}/search"
        headers = {"User-Agent": USER_AGENT}

        params = {
            "q": query,
            "format": "json",
            "limit": min(max_results or 10, 40)  # Nominatim max is 40
        }

        if country:
            params["countrycodes"] = country

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)

            if response.status_code != 200:
                return

            results = response.json()

            count = 0
            for place in results:
                if max_results and count >= max_results:
                    return

                yield {
                    "name": place.get("name", place.get("display_name", "Unknown")),
                    "lat": float(place.get("lat", 0)),
                    "lon": float(place.get("lon", 0))
                }
                count += 1

        except requests.RequestException:
            return

    print("\nSearching for 'temple' in Taiwan (max 3 results):")
    search = search_places_advanced("temple", country="tw", max_results=3)

    for i, place in enumerate(search, 1):
        print(f"  {i}. {place['name'][:40]}...")
        print(f"     ({place['lat']:.4f}, {place['lon']:.4f})")


# =============================================================================
# Example 11: Generator Utilities
# =============================================================================

def example_generator_utilities():
    """Demonstrate utility functions for generators."""
    print("\n" + "="*60)
    print("Example 11: Generator Utilities")
    print("="*60)

    def count():
        n = 1
        while True:
            yield n
            n += 1

    def take(n, iterable):
        """Take first n items."""
        result = []
        for i, item in enumerate(iterable):
            if i >= n:
                break
            result.append(item)
        return result

    def skip(n, iterable):
        """Skip first n items."""
        it = iter(iterable)
        for _ in range(n):
            try:
                next(it)
            except StopIteration:
                return
        yield from it

    def take_while(predicate, iterable):
        """Take while predicate is true."""
        for item in iterable:
            if not predicate(item):
                return
            yield item

    print("\nUsing take(5, count()):")
    print(f"  {take(5, count())}")

    print("\nUsing take(5, skip(10, count())):")
    print(f"  {take(5, skip(10, count()))}")

    print("\nUsing take_while(lambda x: x < 10, count()):")
    print(f"  {list(take_while(lambda x: x < 10, count()))}")


# =============================================================================
# Example 12: Food Search Preview
# =============================================================================

def example_food_search():
    """Preview of the food search CLI."""
    print("\n" + "="*60)
    print("Example 12: Food Search Preview")
    print("="*60)

    def search_food(food_type: str, location: str):
        """Search for food places (single batch for demo)."""
        query = f"{food_type} {location}"
        url = f"{BASE_URL}/search"
        headers = {"User-Agent": USER_AGENT}

        params = {
            "q": query,
            "format": "json",
            "limit": 5,  # Nominatim max is 40
            "addressdetails": 1
        }

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)

            if response.status_code != 200:
                return

            for place in response.json():
                address = place.get("address", {})
                yield {
                    "name": place.get("name", "Unknown"),
                    "district": address.get("suburb", address.get("district", "")),
                    "city": address.get("city", address.get("town", ""))
                }

        except requests.RequestException:
            return

    print("\nSearching for 'ramen' in 'tokyo':")
    for i, place in enumerate(search_food("ramen", "tokyo"), 1):
        print(f"\n  {i}. {place['name']}")
        if place['district']:
            print(f"     District: {place['district']}")
        if place['city']:
            print(f"     City: {place['city']}")


# =============================================================================
# Main Menu
# =============================================================================

def main():
    """Run selected examples."""
    print("="*60)
    print("Week 6: Searching for Places (Lazy Loading) - Examples")
    print("="*60)

    examples = [
        ("1", "Function vs Generator", example_function_vs_generator),
        ("2", "How yield Works", example_yield_behavior),
        ("3", "Generators with for", example_generator_with_for),
        ("4", "Breaking Early", example_break_early),
        ("5", "Memory Efficiency", example_memory_efficiency),
        ("6", "Fibonacci Generator", example_fibonacci),
        ("7", "Generator Expressions", example_generator_expressions),
        ("8", "Result Exclusion (API)", example_pagination),
        ("9", "Lazy API Search", example_paginated_search),
        ("10", "Advanced Search", example_advanced_search),
        ("11", "Generator Utilities", example_generator_utilities),
        ("12", "Food Search Preview", example_food_search),
    ]

    print("\nAvailable examples:")
    for num, name, _ in examples:
        print(f"  {num}. {name}")
    print("  a. Run all examples")
    print("  q. Quit")

    while True:
        choice = input("\nEnter example number (or 'a' for all, 'q' to quit): ").strip().lower()

        if choice == 'q':
            print("Goodbye!")
            break
        elif choice == 'a':
            for num, name, func in examples:
                func()
                if num in ['9', '10', '12']:  # API examples need rate limiting
                    time.sleep(1)
            break
        else:
            for num, name, func in examples:
                if choice == num:
                    func()
                    break
            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
