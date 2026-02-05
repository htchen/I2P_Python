# Week 6: Searching for Places (Lazy Loading)

## Lecture Overview (3 Hours)

**Phase 2: The API & The Cloud** — "Fetching the World"

### Learning Objectives
By the end of this lecture, students will be able to:
1. Understand and use advanced query parameters for API searches
2. Implement pagination to handle large result sets
3. Create Python generators using the `yield` keyword
4. Apply lazy evaluation patterns to conserve memory and API calls
5. Build an efficient place search tool with on-demand data fetching

### Prerequisites
- Week 5: The Nominatim API (Geocoding)
- Understanding of functions and loops
- Basic API request/response concepts

---

# Hour 1: Query Parameters and Pagination

## 1.1 Review: Query Parameters

Query parameters let you customize API requests:

```
https://nominatim.openstreetmap.org/search?q=coffee&format=json&limit=10
                                          └──────────┬──────────────┘
                                              Query Parameters
```

### Anatomy of Query Parameters

```
?key1=value1&key2=value2&key3=value3
│           │
└ Starts    └ Separated by &
  with ?
```

### In Python with `requests`

```python
import requests

# Clean way - let requests handle encoding
params = {
    "q": "coffee shop",      # Spaces become %20 or +
    "format": "json",
    "limit": 10,
    "countrycodes": "tw"
}

response = requests.get(
    "https://nominatim.openstreetmap.org/search",
    params=params,
    headers={"User-Agent": "CS101/1.0 (test@example.com)"}
)

# See the constructed URL
print(response.url)
# https://nominatim.openstreetmap.org/search?q=coffee+shop&format=json&limit=10&countrycodes=tw
```

---

## 1.2 Nominatim Search Parameters Deep Dive

### Basic Search Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `q` | Free-form search query | `"coffee shop"` |
| `format` | Output format | `"json"`, `"jsonv2"`, `"geojson"` |
| `limit` | Max results (1-50) | `10` |
| `addressdetails` | Include address breakdown | `1` |

### Geographic Filtering

| Parameter | Description | Example |
|-----------|-------------|---------|
| `countrycodes` | ISO country codes | `"tw,jp,kr"` |
| `viewbox` | Bounding box (lon1,lat1,lon2,lat2) | `"121.4,24.9,121.7,25.2"` |
| `bounded` | Strict viewbox (0 or 1) | `1` |

### Result Limiting Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `limit` | Max results (1-40) | `10` |
| `exclude_place_ids` | Exclude previous results | `"123,456,789"` |

> **Note:** Nominatim does not support traditional offset-based pagination. To get additional results, use `exclude_place_ids` to exclude previously returned results.

### Example: Search Coffee Shops in Taipei

```python
import requests

def search_coffee_in_taipei():
    """Search for coffee shops within Taipei's bounding box."""
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": "coffee",
        "format": "json",
        "limit": 10,
        "viewbox": "121.45,24.95,121.65,25.15",  # Taipei area
        "bounded": 1,  # Strict - only results in viewbox
        "addressdetails": 1
    }

    headers = {"User-Agent": "CS101/1.0 (test@example.com)"}

    response = requests.get(url, params=params, headers=headers, timeout=10)

    if response.status_code == 200:
        return response.json()
    return []


results = search_coffee_in_taipei()
for place in results[:5]:
    print(f"- {place['display_name'][:60]}...")
```

---

## 1.3 Understanding Result Limiting

### The Problem: Large Result Sets

When you search for something popular like "restaurant taipei", there could be many matching results. Loading all at once:

1. **Slow** - User waits for everything to load
2. **Memory intensive** - All results stored in memory
3. **Wasteful** - User might only need first 10

### How Nominatim Handles Results

Unlike many REST APIs, **Nominatim does not support traditional offset-based pagination**. Instead:

- The `limit` parameter controls how many results to return (max 40)
- To get additional results, use `exclude_place_ids` to exclude previously returned results
- Nominatim returns the **best matching results**, not a complete list

```
Request 1: limit=10                           → Results 1-10
Request 2: limit=10, exclude_place_ids=...    → Results 11-20
Request 3: limit=10, exclude_place_ids=...    → Results 21-30
...
```

### Collecting Place IDs for Exclusion

```python
def get_place_ids(results: list) -> str:
    """
    Extract place IDs from results for exclusion in next request.

    Args:
        results: List of place dictionaries from API

    Returns:
        Comma-separated string of place IDs
    """
    return ",".join(str(place["place_id"]) for place in results)


# Example usage:
# first_results = [...from API...]
# place_ids = get_place_ids(first_results)
# Next request: params["exclude_place_ids"] = place_ids
```

---

## 1.4 Implementing Result Fetching with Exclusion

```python
import requests
import time

def fetch_results(query: str, exclude_ids: str = None, limit: int = 10) -> list:
    """
    Fetch search results, optionally excluding previous results.

    Args:
        query: Search query
        exclude_ids: Comma-separated place IDs to exclude
        limit: Max results (1-40)

    Returns:
        List of results
    """
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": query,
        "format": "json",
        "limit": min(limit, 40)  # Nominatim max is 40
    }

    if exclude_ids:
        params["exclude_place_ids"] = exclude_ids

    headers = {"User-Agent": "CS101/1.0 (test@example.com)"}

    response = requests.get(url, params=params, headers=headers, timeout=10)

    if response.status_code == 200:
        return response.json()
    return []


def fetch_multiple_batches(query: str, max_batches: int = 5, batch_size: int = 10) -> list:
    """
    Fetch multiple batches of results using exclude_place_ids.

    Args:
        query: Search query
        max_batches: Maximum batches to fetch
        batch_size: Results per batch

    Returns:
        Combined list of all results
    """
    all_results = []
    exclude_ids = None

    for batch in range(1, max_batches + 1):
        print(f"Fetching batch {batch}...")

        results = fetch_results(query, exclude_ids, batch_size)

        if not results:
            print("No more results")
            break

        all_results.extend(results)
        print(f"  Got {len(results)} results (total: {len(all_results)})")

        # Collect place IDs for exclusion in next request
        new_ids = [str(r["place_id"]) for r in results]
        if exclude_ids:
            exclude_ids = exclude_ids + "," + ",".join(new_ids)
        else:
            exclude_ids = ",".join(new_ids)

        time.sleep(1)  # Rate limiting

    return all_results


# Usage
results = fetch_multiple_batches("cafe taipei", max_batches=3)
print(f"\nTotal results: {len(results)}")
```

### The Problem with This Approach

```python
# This fetches ALL batches upfront, even if we only need a few results
all_results = fetch_multiple_batches("restaurant taipei", max_batches=10)

# But maybe we only wanted the first 3!
for result in all_results[:3]:
    print(result["display_name"])

# We wasted API calls and memory!
```

**Solution: Lazy Evaluation with Generators**

---

## 1.5 Mini-Exercise 1: Understanding Result Exclusion

Answer these questions about Nominatim's result handling:

```python
# Question 1: What's the maximum value for the 'limit' parameter?
max_limit = ?

# Question 2: You made a request and got 10 results with place_ids:
# [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
# What parameter do you add to get the NEXT 10 results?
next_request_param = ?

# Question 3: Why doesn't Nominatim support traditional offset pagination?
# (Think about what Nominatim is designed for)
```

<details>
<summary>Solution</summary>

```python
# Question 1: Maximum limit
max_limit = 40  # Nominatim's maximum is 40 results per request

# Question 2: Exclude previous results
# Add this parameter to your next request:
next_request_param = {"exclude_place_ids": "101,102,103,104,105,106,107,108,109,110"}

# Question 3: Why no offset pagination?
# Nominatim is designed for GEOCODING (finding best matches for a query),
# not for downloading complete datasets. It returns the most relevant
# results first. For bulk data, use the Overpass API instead.
```

</details>

---

# ☕ 5-Minute Break

Stand up, stretch, rest your eyes!

---

# Hour 2: Python Generators and `yield`

## 2.1 What is a Generator?

A **generator** is a special type of function that:
- Returns values one at a time (instead of all at once)
- "Pauses" after each value
- "Resumes" when the next value is requested
- Uses the `yield` keyword instead of `return`

### Regular Function vs Generator

```python
# Regular function - returns everything at once
def get_numbers_list():
    result = []
    for i in range(1, 6):
        result.append(i)
    return result

numbers = get_numbers_list()
print(numbers)  # [1, 2, 3, 4, 5] - all computed immediately


# Generator function - yields one at a time
def get_numbers_generator():
    for i in range(1, 6):
        yield i  # Pause and return i

numbers = get_numbers_generator()
print(numbers)  # <generator object at 0x...> - nothing computed yet!

print(next(numbers))  # 1 - computed now
print(next(numbers))  # 2 - computed now
print(next(numbers))  # 3 - computed now
```

---

## 2.2 The `yield` Keyword

`yield` is like `return`, but:
- **Pauses** the function instead of ending it
- **Remembers** where it left off
- **Resumes** from that point when `next()` is called

```python
def simple_generator():
    print("Starting...")
    yield 1
    print("After first yield")
    yield 2
    print("After second yield")
    yield 3
    print("Done!")


gen = simple_generator()

print("Created generator, nothing printed yet")
print()

print("Calling next():")
print(next(gen))  # Prints "Starting..." then yields 1
print()

print("Calling next() again:")
print(next(gen))  # Prints "After first yield" then yields 2
print()

print("Calling next() one more time:")
print(next(gen))  # Prints "After second yield" then yields 3
```

Output:
```
Created generator, nothing printed yet

Calling next():
Starting...
1

Calling next() again:
After first yield
2

Calling next() one more time:
After second yield
3
```

---

## 2.3 Iterating Over Generators

Generators work with `for` loops:

```python
def countdown(n):
    """Count down from n to 1."""
    print(f"Starting countdown from {n}")
    while n > 0:
        yield n
        n -= 1
    print("Blastoff!")


# Using a for loop
for num in countdown(5):
    print(num)

# Output:
# Starting countdown from 5
# 5
# 4
# 3
# 2
# 1
# Blastoff!
```

### Breaking Early

```python
def infinite_counter():
    """Count forever."""
    n = 1
    while True:
        yield n
        n += 1


# We can break early - no infinite loop!
for num in infinite_counter():
    print(num)
    if num >= 5:
        break  # Stop after 5

# Output: 1, 2, 3, 4, 5
# The generator never computed 6, 7, 8, ...
```

---

## 2.4 Why Use Generators?

### 1. Memory Efficiency

```python
# List - stores ALL values in memory
def squares_list(n):
    return [x**2 for x in range(n)]

# Generator - stores only ONE value at a time
def squares_generator(n):
    for x in range(n):
        yield x**2


# Compare memory usage for 1 million numbers
import sys

big_list = squares_list(1_000_000)
print(f"List size: {sys.getsizeof(big_list):,} bytes")  # ~8 MB

big_gen = squares_generator(1_000_000)
print(f"Generator size: {sys.getsizeof(big_gen):,} bytes")  # ~200 bytes!
```

### 2. Lazy Evaluation

Values are computed **only when needed**:

```python
def expensive_computation(n):
    """Simulate expensive API calls."""
    print(f"  Computing item {n}...")
    import time
    time.sleep(0.5)  # Simulate delay
    return n * 10


def lazy_results():
    for i in range(1, 6):
        yield expensive_computation(i)


# Only compute what we need
gen = lazy_results()

print("Getting first result:")
print(next(gen))  # Only computes #1

print("\nGetting second result:")
print(next(gen))  # Only computes #2

print("\nDone! We never computed #3, #4, #5")
```

### 3. Infinite Sequences

```python
def fibonacci():
    """Generate infinite Fibonacci sequence."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# Get first 10 Fibonacci numbers
fib = fibonacci()
for i in range(10):
    print(next(fib), end=" ")
# 0 1 1 2 3 5 8 13 21 34
```

---

## 2.5 Mini-Exercise 2: Create a Generator

Write a generator that yields powers of 2:

```python
def powers_of_two(max_power):
    """
    Generate powers of 2 from 2^0 to 2^max_power.

    Args:
        max_power: The maximum power to generate

    Yields:
        2^0, 2^1, 2^2, ..., 2^max_power

    Example:
        >>> list(powers_of_two(4))
        [1, 2, 4, 8, 16]
    """
    # TODO: Implement this generator
    pass


# Test
for power in powers_of_two(10):
    print(power, end=" ")
# Expected: 1 2 4 8 16 32 64 128 256 512 1024
```

<details>
<summary>Solution</summary>

```python
def powers_of_two(max_power):
    """Generate powers of 2 from 2^0 to 2^max_power."""
    for n in range(max_power + 1):
        yield 2 ** n


# Or using a while loop:
def powers_of_two_v2(max_power):
    n = 0
    while n <= max_power:
        yield 2 ** n
        n += 1


# Test
for power in powers_of_two(10):
    print(power, end=" ")
# Output: 1 2 4 8 16 32 64 128 256 512 1024
```

</details>

---

## 2.6 Generator Expressions

Like list comprehensions, but lazy:

```python
# List comprehension - creates list immediately
squares_list = [x**2 for x in range(10)]

# Generator expression - creates generator (lazy)
squares_gen = (x**2 for x in range(10))

print(type(squares_list))  # <class 'list'>
print(type(squares_gen))   # <class 'generator'>

# Use the generator
for sq in squares_gen:
    print(sq, end=" ")
# 0 1 4 9 16 25 36 49 64 81
```

### When to Use Each

```python
# Use list comprehension when:
# - You need random access (data[5])
# - You need to iterate multiple times
# - Dataset is small

# Use generator expression when:
# - You only need to iterate once
# - Dataset is large
# - You might stop early
```

---

## 2.7 Converting Generators to Lists

```python
def first_n_squares(n):
    for i in range(n):
        yield i ** 2


# Get as a generator
gen = first_n_squares(5)

# Convert to list if needed
squares_list = list(gen)
print(squares_list)  # [0, 1, 4, 9, 16]

# Warning: Can only convert once!
squares_list_2 = list(gen)
print(squares_list_2)  # [] - generator is exhausted!
```

---

# ☕ 10-Minute Break

Stretch, grab water, check your phone!

---

# Hour 3: Building a Lazy Place Search

## 3.1 The Problem Revisited

We want to search for places, but:
- There might be hundreds of results
- User might only want the first few
- Each API call costs time and is rate-limited

**Solution: Generator that fetches pages on demand**

---

## 3.2 Basic Lazy Search Generator

```python
import requests
import time

def search_places(query: str, batch_size: int = 10):
    """
    Generator that yields places one at a time,
    fetching new batches only when needed.

    Args:
        query: Search query
        batch_size: Results per API call (max 40)

    Yields:
        Dictionary with place info
    """
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "CS101/1.0 (test@example.com)"}

    exclude_ids = []  # Track place IDs we've already seen

    while True:
        # Build parameters
        params = {
            "q": query,
            "format": "json",
            "limit": min(batch_size, 40)  # Nominatim max is 40
        }

        # Exclude previously returned results
        if exclude_ids:
            params["exclude_place_ids"] = ",".join(map(str, exclude_ids))
            print(f"  [Fetching next batch, excluding {len(exclude_ids)} previous results...]")
        else:
            print(f"  [Fetching first batch...]")

        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            return  # Stop on error

        results = response.json()

        if not results:
            return  # No more results

        # Yield each result one at a time
        for place in results:
            exclude_ids.append(place["place_id"])  # Remember this ID
            yield {
                "name": place.get("display_name", "Unknown"),
                "lat": float(place.get("lat", 0)),
                "lon": float(place.get("lon", 0)),
                "type": place.get("type", "unknown")
            }

        time.sleep(1)  # Rate limiting


# Usage - only fetches what we need!
print("Searching for 'cafe taipei'...")
search = search_places("cafe taipei")

print("\nGetting first 3 results:")
for i, place in enumerate(search):
    print(f"{i+1}. {place['name'][:50]}...")
    if i >= 2:
        break  # Stop after 3 - no extra batches fetched!
```

---

## 3.3 Enhanced Search Generator with Options

```python
import requests
import time
from typing import Generator

def search_places_advanced(
    query: str,
    country: str = None,
    viewbox: tuple = None,
    batch_size: int = 10,
    max_results: int = None
) -> Generator[dict, None, None]:
    """
    Advanced place search generator with filtering options.

    Args:
        query: Search query
        country: ISO country code (e.g., "tw")
        viewbox: Bounding box as (west, south, east, north)
        batch_size: Results per API call (max 40)
        max_results: Maximum total results (None for unlimited)

    Yields:
        Dictionary with name, lat, lon, type, address
    """
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "CS101/1.0 (test@example.com)"}

    exclude_ids = []
    count = 0

    while True:
        # Check if we've hit max results
        if max_results and count >= max_results:
            return

        # Build parameters
        params = {
            "q": query,
            "format": "json",
            "limit": min(batch_size, 40),  # Nominatim max is 40
            "addressdetails": 1
        }

        # Exclude previously returned results
        if exclude_ids:
            params["exclude_place_ids"] = ",".join(map(str, exclude_ids))

        if country:
            params["countrycodes"] = country

        if viewbox:
            params["viewbox"] = f"{viewbox[0]},{viewbox[1]},{viewbox[2]},{viewbox[3]}"
            params["bounded"] = 1

        # Fetch batch
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)

            if response.status_code == 429:
                print("  Rate limited! Waiting 5 seconds...")
                time.sleep(5)
                continue

            if response.status_code != 200:
                print(f"  Error: HTTP {response.status_code}")
                return

            results = response.json()

        except requests.RequestException as e:
            print(f"  Network error: {e}")
            return

        if not results:
            return  # No more results

        # Yield each result
        for place in results:
            if max_results and count >= max_results:
                return

            exclude_ids.append(place["place_id"])  # Track for exclusion

            yield {
                "name": place.get("display_name", "Unknown"),
                "lat": float(place.get("lat", 0)),
                "lon": float(place.get("lon", 0)),
                "type": f"{place.get('class', '')}:{place.get('type', '')}",
                "address": place.get("address", {})
            }

            count += 1

        time.sleep(1)  # Rate limiting


# Usage examples

# Search with country filter
print("Coffee shops in Taiwan:")
for i, place in enumerate(search_places_advanced("coffee", country="tw", max_results=5)):
    print(f"  {i+1}. {place['name'][:50]}...")

print()

# Search within bounding box (Taipei)
taipei_box = (121.45, 24.95, 121.65, 25.15)  # west, south, east, north
print("Restaurants in Taipei area:")
for i, place in enumerate(search_places_advanced("restaurant", viewbox=taipei_box, max_results=5)):
    print(f"  {i+1}. {place['name'][:50]}...")
```

---

## 3.4 Mini-Exercise 3: Use the Generator

Use the `search_places` generator to:

1. Find the first coffee shop in Tokyo
2. Find 5 museums and print their coordinates
3. Search for "night market" and stop when you find one in a specific district

```python
# TODO: Complete these tasks using the search generator

# Task 1: First coffee shop in Tokyo
search = search_places_advanced("coffee", country="jp", max_results=20)
# Find one that contains "Tokyo" in the name
# ...

# Task 2: 5 museums with coordinates
# ...

# Task 3: Night market in specific district
# ...
```

<details>
<summary>Solution</summary>

```python
import time

# Task 1: First coffee shop in Tokyo
print("Task 1: Coffee shop in Tokyo")
search = search_places_advanced("coffee shop", country="jp", max_results=50)
for place in search:
    if "Tokyo" in place["name"] or "東京" in place["name"]:
        print(f"Found: {place['name'][:60]}...")
        break
else:
    print("No coffee shop found in Tokyo")

time.sleep(1)

# Task 2: 5 museums with coordinates
print("\nTask 2: 5 Museums")
search = search_places_advanced("museum", max_results=5)
for i, place in enumerate(search, 1):
    print(f"{i}. {place['name'][:40]}...")
    print(f"   Coordinates: ({place['lat']:.4f}, {place['lon']:.4f})")

time.sleep(1)

# Task 3: Night market in specific district
print("\nTask 3: Night market in Shilin")
search = search_places_advanced("night market", country="tw", max_results=50)
for place in search:
    if "Shilin" in place["name"] or "士林" in place["name"]:
        print(f"Found: {place['name'][:60]}...")
        break
else:
    print("Shilin night market not found")
```

</details>

---

## 3.5 Building the Food Search CLI

Now let's build the complete project: "What do you want to eat?"

```python
import requests
import time
from typing import Generator


def search_food(
    food_type: str,
    location: str,
    batch_size: int = 10
) -> Generator[dict, None, None]:
    """
    Search for food/restaurants lazily.

    Args:
        food_type: Type of food (pizza, sushi, etc.)
        location: Location to search in
        batch_size: Results per API call (max 40)

    Yields:
        Restaurant/food place information
    """
    query = f"{food_type} {location}"
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "CS101-FoodSearch/1.0 (cs101@example.com)"}

    exclude_ids = []

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
                # Extract useful info
                address = place.get("address", {})
                exclude_ids.append(place["place_id"])  # Track for exclusion

                yield {
                    "name": place.get("name", place.get("display_name", "Unknown")),
                    "full_address": place.get("display_name", ""),
                    "lat": float(place.get("lat", 0)),
                    "lon": float(place.get("lon", 0)),
                    "type": place.get("type", "unknown"),
                    "city": address.get("city", address.get("town", "")),
                    "district": address.get("suburb", address.get("district", ""))
                }

            time.sleep(1)

        except requests.RequestException:
            return


def display_place(place: dict, index: int):
    """Display a place nicely."""
    print(f"\n{index}. {place['name']}")
    if place['district']:
        print(f"   District: {place['district']}")
    if place['city']:
        print(f"   City: {place['city']}")
    print(f"   Coordinates: ({place['lat']:.6f}, {place['lon']:.6f})")


def food_search_cli():
    """Interactive food search CLI."""
    print("\n" + "="*50)
    print("  What Do You Want to Eat?")
    print("="*50)

    # Get user input
    food = input("\nWhat type of food? (e.g., pizza, ramen, tacos): ").strip()
    if not food:
        food = "restaurant"

    location = input("Where? (e.g., taipei, tokyo, new york): ").strip()
    if not location:
        location = "taipei"

    print(f"\nSearching for '{food}' in '{location}'...")
    print("(Results load on demand - press Enter for more, 'q' to quit)")

    # Create generator
    search = search_food(food, location)

    count = 0
    batch_size = 3

    while True:
        # Show next batch
        print(f"\n--- Results {count + 1} to {count + batch_size} ---")

        found_any = False
        for i in range(batch_size):
            try:
                place = next(search)
                count += 1
                display_place(place, count)
                found_any = True
            except StopIteration:
                if not found_any:
                    print("\nNo more results found.")
                return

        # Ask user
        action = input("\nPress Enter for more, or 'q' to quit: ").strip().lower()
        if action == 'q':
            print(f"\nShowed {count} results. Goodbye!")
            return


if __name__ == "__main__":
    food_search_cli()
```

---

## 3.6 Generator Utilities

Useful functions for working with generators:

```python
from typing import Generator, TypeVar, Iterable
from itertools import islice

T = TypeVar('T')


def take(n: int, iterable: Iterable[T]) -> list[T]:
    """Take first n items from an iterable."""
    return list(islice(iterable, n))


def skip(n: int, iterable: Iterable[T]) -> Generator[T, None, None]:
    """Skip first n items from an iterable."""
    it = iter(iterable)
    for _ in range(n):
        try:
            next(it)
        except StopIteration:
            return
    yield from it


def take_while(predicate, iterable: Iterable[T]) -> Generator[T, None, None]:
    """Take items while predicate is True."""
    for item in iterable:
        if predicate(item):
            yield item
        else:
            return


def filter_gen(predicate, iterable: Iterable[T]) -> Generator[T, None, None]:
    """Filter items from generator."""
    for item in iterable:
        if predicate(item):
            yield item


# Usage examples
search = search_places_advanced("cafe", country="tw")

# Get first 5
first_five = take(5, search)

# Skip 10, get next 5
search = search_places_advanced("cafe", country="tw")
next_five = take(5, skip(10, search))

# Filter by type
search = search_places_advanced("museum")
art_museums = filter_gen(
    lambda p: "art" in p["name"].lower(),
    search
)
```

---

## 3.7 Mini-Exercise 4: Extend the Food Search

Add these features to the food search CLI:

1. Filter by minimum rating (if available in data)
2. Show distance from a reference point
3. Save results to a file

```python
# Hint for distance calculation
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in km."""
    R = 6371  # Earth's radius in km

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


# TODO: Modify display_place to show distance from user's location
# TODO: Add option to save results to JSON file
```

<details>
<summary>Solution Hints</summary>

```python
def display_place_with_distance(place: dict, index: int, user_lat: float, user_lon: float):
    """Display a place with distance from user."""
    distance = haversine_distance(
        user_lat, user_lon,
        place['lat'], place['lon']
    )

    print(f"\n{index}. {place['name']}")
    print(f"   Distance: {distance:.2f} km")
    print(f"   Coordinates: ({place['lat']:.6f}, {place['lon']:.6f})")


def save_results(results: list, filename: str):
    """Save results to JSON file."""
    import json
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(results)} results to {filename}")


# In the CLI, collect results and offer to save:
collected_results = []
for place in search:
    collected_results.append(place)
    display_place(place, len(collected_results))
    # ...

# At the end:
if collected_results:
    save = input("Save results? (y/n): ")
    if save.lower() == 'y':
        save_results(collected_results, "food_search_results.json")
```

</details>

---

## 3.8 Summary: Key Takeaways

### Fetching More Results (Nominatim)
- Use `limit` parameter (max 40) to control batch size
- Use `exclude_place_ids` to get additional results
- Track returned place IDs and exclude them in next request
- Note: Nominatim does NOT support traditional offset pagination

### Generators
- Use `yield` instead of `return`
- Values are computed on demand (lazy)
- Memory efficient for large/infinite sequences
- Can stop early without wasting computation

### Generator Patterns
```python
# Basic generator
def my_generator():
    yield value

# Generator with lazy fetching
def lazy_search(query, batch_size=10):
    exclude_ids = []
    while has_more:
        results = fetch_batch(exclude_ids)
        for item in results:
            exclude_ids.append(item["id"])
            yield item

# Generator expression
gen = (x**2 for x in range(10))

# Using generators
for item in generator:
    process(item)
    if done:
        break  # No wasted computation
```

### Best Practices
1. Use generators for lazy data fetching
2. Implement rate limiting inside the generator
3. Handle errors gracefully (don't crash mid-iteration)
4. Provide clear stopping conditions
5. Document what the generator yields
6. For Nominatim: use `exclude_place_ids`, not offset (which doesn't exist)

---

## 3.9 Homework Assignments

### Assignment 1: Infinite Number Generator (Basic)
Create a generator that yields prime numbers infinitely. Use it to print the first 20 primes.

### Assignment 2: Multi-Source Search (Intermediate)
Modify the food search to search multiple locations and merge results:
```python
def multi_location_search(food: str, locations: list[str]):
    """Search for food across multiple locations."""
    # Yield results from each location in round-robin fashion
    pass
```

### Assignment 3: Cached Generator (Advanced)
Create a generator wrapper that caches results so they can be iterated multiple times without re-fetching:
```python
class CachedGenerator:
    """Wrapper that caches generator results."""

    def __init__(self, generator):
        self.generator = generator
        self.cache = []

    def __iter__(self):
        # First, yield cached results
        # Then, continue from generator and cache new results
        pass
```

---

## Additional Resources

### Python Documentation
- [Generators](https://docs.python.org/3/tutorial/classes.html#generators)
- [Generator Expressions](https://docs.python.org/3/reference/expressions.html#generator-expressions)
- [itertools module](https://docs.python.org/3/library/itertools.html)

### Nominatim
- [Search API Documentation](https://nominatim.org/release-docs/latest/api/Search/)
- [Usage Policy](https://operations.osmfoundation.org/policies/nominatim/)

### Further Reading
- [Python Generators Tutorial](https://realpython.com/introduction-to-python-generators/)
- [Lazy Evaluation in Python](https://en.wikipedia.org/wiki/Lazy_evaluation)

---

## Next Week Preview

**Week 7: OSRM API (Real Routing)**
- 2D Lists (Matrices)
- Cost comparison algorithms
- Comparing Haversine distance vs OSRM (real) distance
- Fetching and parsing route geometry

---

*End of Week 6 Lecture*
