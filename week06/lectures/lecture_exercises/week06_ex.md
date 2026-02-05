# Week 6 Lab: Searching for Places (Lazy Loading)

## Lab Overview

In this lab, you'll practice creating Python generators, implementing pagination, and building a lazy-loading place search system.

**Time:** 90 minutes

### Prerequisites
- Completed Week 6 lecture
- Understanding of Nominatim API (Week 4-5)
- Python functions and loops

### Learning Objectives
1. Create generator functions using `yield`
2. Understand and use lazy evaluation
3. Implement API pagination
4. Build memory-efficient data pipelines
5. Create an interactive search application

---

## Setup

Create your working file:

```bash
cd week06/labs
touch week06_starter.py
```

---

## Exercise 1: Basic Generators (15 minutes)

### Task
Create simple generators to understand the `yield` keyword.

### Requirements
1. Create a generator that counts from 1 to n
2. Create a generator that yields squares of numbers
3. Create a generator that yields the Fibonacci sequence

### Starter Code

```python
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
    pass


# Tests
def test_basic_generators():
    print("Testing basic generators...")

    # Test count_to
    assert list(count_to(5)) == [1, 2, 3, 4, 5], "count_to failed"
    print("  count_to: PASS")

    # Test squares
    assert list(squares(5)) == [1, 4, 9, 16, 25], "squares failed"
    print("  squares: PASS")

    # Test fibonacci
    fib_10 = list(fibonacci(10))
    assert fib_10 == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34], f"fibonacci failed: {fib_10}"
    print("  fibonacci: PASS")

    print("All basic generator tests passed!")


if __name__ == "__main__":
    test_basic_generators()
```

---

## Exercise 2: Generator Utilities (15 minutes)

### Task
Implement utility functions that work with generators.

### Requirements
1. `take(n, gen)` - Get first n items from a generator
2. `skip(n, gen)` - Skip first n items, yield the rest
3. `take_while(predicate, gen)` - Yield while condition is true

### Starter Code

```python
from typing import Generator, TypeVar, Callable, Iterable

T = TypeVar('T')


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


# Tests
def test_generator_utilities():
    print("Testing generator utilities...")

    # Test take
    assert take(3, count_to(10)) == [1, 2, 3], "take failed"
    assert take(10, count_to(3)) == [1, 2, 3], "take with overflow failed"
    print("  take: PASS")

    # Test skip
    assert list(skip(3, count_to(6))) == [4, 5, 6], "skip failed"
    assert list(skip(10, count_to(3))) == [], "skip with overflow failed"
    print("  skip: PASS")

    # Test take_while
    result = list(take_while(lambda x: x < 5, count_to(10)))
    assert result == [1, 2, 3, 4], f"take_while failed: {result}"
    print("  take_while: PASS")

    print("All utility tests passed!")


if __name__ == "__main__":
    test_generator_utilities()
```

---

## Exercise 3: API Result Handling (10 minutes)

### Task
Create functions to work with Nominatim's result exclusion pattern.

### Requirements
1. Extract place IDs from results for exclusion
2. Build the exclude_place_ids parameter string
3. Understand Nominatim's limit (max 40)

### Starter Code

```python
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
    pass


# Tests
def test_result_handling():
    print("Testing result handling functions...")

    # Test extract_place_ids
    results = [{"place_id": 101, "name": "A"}, {"place_id": 102, "name": "B"}]
    assert extract_place_ids(results) == [101, 102], "extract_place_ids failed"
    print("  extract_place_ids: PASS")

    # Test build_exclude_param
    assert build_exclude_param([101, 102, 103]) == "101,102,103", "build_exclude_param failed"
    assert build_exclude_param([]) == "", "empty list failed"
    print("  build_exclude_param: PASS")

    # Test get_safe_limit
    assert get_safe_limit(10) == 10, "limit 10 failed"
    assert get_safe_limit(50) == 40, "limit 50 should be 40"
    assert get_safe_limit(40) == 40, "limit 40 failed"
    print("  get_safe_limit: PASS")

    print("All result handling tests passed!")


if __name__ == "__main__":
    test_result_handling()
```

---

## Exercise 4: Lazy API Generator (20 minutes)

### Task
Create a generator that fetches results from Nominatim using `exclude_place_ids`.

### Requirements
1. Fetch results batch by batch
2. Use `exclude_place_ids` to get additional results
3. Yield results one at a time
4. Stop when no more results
5. Implement rate limiting

### Starter Code

```python
import requests
import time

def search_places_lazy(
    query: str,
    batch_size: int = 10,
    max_batches: int = 5
):
    """
    Generator that fetches places batch by batch.

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
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "CS101-Lab/1.0 (student@example.com)"}

    # TODO: Implement the lazy generator
    # 1. Keep track of place_ids we've seen (for exclusion)
    # 2. Loop through batches (up to max_batches)
    # 3. Build params with 'exclude_place_ids' if we have previous results
    # 4. Fetch batch and yield each result one at a time
    # 5. Add each place_id to our exclusion list
    # 6. Stop if no results returned
    # 7. Add rate limiting (1 second between requests)

    pass


# Test the generator
def test_lazy_search():
    print("Testing lazy search...")

    search = search_places_lazy("cafe taipei", batch_size=5, max_batches=2)

    results = []
    for i, place in enumerate(search):
        results.append(place)
        print(f"  {i+1}. {place['name'][:50]}...")
        if i >= 4:  # Stop after 5 results
            break

    assert len(results) > 0, "No results returned"
    assert "name" in results[0], "Missing 'name' field"
    assert "lat" in results[0], "Missing 'lat' field"
    assert isinstance(results[0]["lat"], float), "lat should be float"

    print(f"\n  Got {len(results)} results")
    print("  lazy_search: PASS")


if __name__ == "__main__":
    test_lazy_search()
```

---

## Exercise 5: Lazy Search with Filters (20 minutes)

### Task
Create an advanced search generator with filtering capabilities.

### Requirements
1. Support country filtering
2. Support bounding box filtering
3. Filter results by type
4. Limit total results
5. Use `exclude_place_ids` for fetching more results

### Starter Code

```python
import requests
import time
from typing import Generator, Optional

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
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "CS101-Lab/1.0 (student@example.com)"}

    # TODO: Implement advanced search generator
    # 1. Keep track of exclude_ids for getting more results
    # 2. Build params with optional country filter
    # 3. Use min(batch_size, 40) for limit (Nominatim max is 40)
    # 4. Add exclude_place_ids param if we have previous results
    # 5. Track count of yielded results
    # 6. Filter by place_type if specified
    # 7. Stop when max_results reached
    # 8. Add rate limiting between batches

    pass


def filter_by_type(places: Generator, type_filter: str) -> Generator[dict, None, None]:
    """
    Filter generator results by type.

    Args:
        places: Generator of place dictionaries
        type_filter: Type to filter for (partial match)

    Yields:
        Places matching the type filter
    """
    # TODO: Implement type filtering
    pass


# Tests
def test_advanced_search():
    print("Testing advanced search...")

    # Test with country filter
    print("\n  Testing country filter (Taiwan)...")
    search = search_places_advanced("coffee", country="tw", max_results=3)
    results = list(search)
    print(f"    Found {len(results)} results")
    assert len(results) <= 3, "max_results not respected"

    time.sleep(1)

    # Test with max_results
    print("\n  Testing max_results...")
    search = search_places_advanced("museum", max_results=5)
    results = list(search)
    assert len(results) <= 5, "max_results not working"
    print(f"    Got exactly {len(results)} results")

    print("\n  advanced_search: PASS")


if __name__ == "__main__":
    test_advanced_search()
```

---

## Exercise 6: Food Search CLI (25 minutes)

### Task
Build the complete "What do you want to eat?" CLI application.

### Requirements
1. Ask user for food type and location
2. Display results in batches
3. Allow user to load more or quit
4. Show result count and basic info
5. Handle errors gracefully

### Starter Code

```python
import requests
import time
from typing import Generator


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
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "CS101-FoodSearch/1.0 (student@example.com)"}

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
                print(f"  API error: {response.status_code}")
                return

            results = response.json()

            if not results:
                return

            for place in results:
                address = place.get("address", {})
                exclude_ids.append(place["place_id"])  # Track for exclusion
                yield {
                    "name": place.get("name", "Unknown"),
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
    # TODO: Implement nice display
    # Show: index, name, district/city, coordinates
    pass


def food_search_cli():
    """
    Interactive food search CLI.

    Flow:
    1. Ask for food type
    2. Ask for location
    3. Show results in batches of 3
    4. Ask user: more results, quit, or new search
    """
    print("\n" + "="*50)
    print("     What Do You Want to Eat?")
    print("="*50)

    while True:
        # TODO: Implement the CLI
        # 1. Get food type from user (default: "restaurant")
        # 2. Get location from user (default: "taipei")
        # 3. Create search generator
        # 4. Display results in batches of 3
        # 5. Handle user input:
        #    - Enter: show more results
        #    - 'q': quit
        #    - 'n': new search
        # 6. Handle no more results

        pass


# Simple test
def test_food_search():
    print("Testing food search generator...")

    search = search_food("ramen", "tokyo")

    count = 0
    for place in search:
        print(f"  {count+1}. {place['name'][:40]}...")
        count += 1
        if count >= 3:
            break

    assert count > 0, "No results found"
    print(f"\n  Found {count} results")
    print("  food_search: PASS")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_food_search()
    else:
        food_search_cli()
```

### Expected CLI Behavior

```
==================================================
     What Do You Want to Eat?
==================================================

What type of food? (press Enter for 'restaurant'): pizza
Where? (press Enter for 'taipei'): new york

Searching for 'pizza' in 'new york'...

--- Results 1-3 ---

1. Joe's Pizza
   Manhattan, New York
   (40.7308, -73.9973)

2. Di Fara Pizza
   Brooklyn, New York
   (40.6250, -73.9614)

3. Lucali
   Brooklyn, New York
   (40.6786, -73.9977)

[Enter] More results | [n] New search | [q] Quit:

--- Results 4-6 ---
...
```

---

## Bonus Challenge: Generator Pipeline

### Task
Create a pipeline of generators that processes data in stages.

### Requirements
1. Search generator -> Filter generator -> Transform generator
2. Each stage processes data lazily
3. Chain them together

### Starter Code

```python
from typing import Generator, Callable


def create_pipeline(*generators) -> Generator:
    """
    Chain multiple generators together.

    Usage:
        pipeline = create_pipeline(
            search_places("cafe"),
            filter_by_country("tw"),
            transform_to_simple()
        )
    """
    # TODO: Implement generator pipeline
    pass


def filter_generator(source: Generator, predicate: Callable) -> Generator:
    """Filter items from source generator."""
    for item in source:
        if predicate(item):
            yield item


def transform_generator(source: Generator, transform: Callable) -> Generator:
    """Transform items from source generator."""
    for item in source:
        yield transform(item)


def limit_generator(source: Generator, max_items: int) -> Generator:
    """Limit number of items from source."""
    count = 0
    for item in source:
        if count >= max_items:
            return
        yield item
        count += 1


# Example usage
def demo_pipeline():
    """Demonstrate the generator pipeline."""

    # Create a search
    search = search_places_lazy("museum", batch_size=10, max_batches=3)

    # Filter to only art museums
    art_museums = filter_generator(
        search,
        lambda p: "art" in p["name"].lower()
    )

    # Transform to simple format
    simple = transform_generator(
        art_museums,
        lambda p: {"name": p["name"][:50], "coords": (p["lat"], p["lon"])}
    )

    # Limit to 5 results
    limited = limit_generator(simple, 5)

    # Consume the pipeline
    print("Art Museums (max 5):")
    for museum in limited:
        print(f"  - {museum['name']}")
        print(f"    {museum['coords']}")


if __name__ == "__main__":
    demo_pipeline()
```

---

## Submission Checklist

Before submitting, verify:

- [ ] All basic generator tests pass
- [ ] Pagination calculations are correct
- [ ] Paginated API search works with rate limiting
- [ ] Advanced search with filters works
- [ ] Food search CLI is interactive and handles errors
- [ ] Code is well-documented

## Grading Rubric

| Exercise | Points | Criteria |
|----------|--------|----------|
| Exercise 1 | 15 | Basic generators work correctly |
| Exercise 2 | 15 | Utility functions work |
| Exercise 3 | 10 | Pagination math is correct |
| Exercise 4 | 20 | Paginated search with rate limiting |
| Exercise 5 | 15 | Advanced search with filters |
| Exercise 6 | 25 | Complete CLI application |
| Bonus | +15 | Generator pipeline works |

**Total: 100 points (+15 bonus)**

---

## Common Issues & Solutions

### Issue: Generator exhausted after one use
```python
# WRONG - generator can only be used once
gen = my_generator()
list1 = list(gen)  # Works
list2 = list(gen)  # Empty!

# RIGHT - create new generator each time
list1 = list(my_generator())
list2 = list(my_generator())
```

### Issue: StopIteration not handled
```python
# WRONG - crashes when generator ends
gen = my_generator()
while True:
    item = next(gen)  # Raises StopIteration eventually

# RIGHT - use for loop or handle exception
for item in gen:
    process(item)

# Or with try/except
try:
    item = next(gen)
except StopIteration:
    print("No more items")
```

### Issue: Rate limiting not working
```python
# Make sure sleep is AFTER the request
response = requests.get(url, ...)
results = response.json()
time.sleep(1)  # Sleep after processing, before next page
```

---

*End of Week 6 Lab*
