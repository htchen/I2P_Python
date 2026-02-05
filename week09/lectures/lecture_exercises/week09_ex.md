# Week 9 Lab: Functional Patterns & Sorting

## Lab Overview

In this lab, you'll practice functional programming concepts by building a **Place Filter & Ranking System**. You'll work with real place data and implement various filtering, sorting, and data transformation functions.

**Time:** 2 hours
**Difficulty:** Intermediate

### Learning Objectives

By completing this lab, you will:
1. Write pure functions that don't modify their inputs
2. Use `lambda` functions for concise transformations
3. Apply `map()`, `filter()`, and `reduce()` to process data
4. Sort data using custom key functions
5. Build data processing pipelines
6. Practice immutable data handling

### Prerequisites

- Understanding of Python lists and dictionaries
- Basic knowledge of functions and arguments
- Week 8: OSRM API (place data structures)

---

## Setup

### Starter Code

Open `week09_starter.py` and review the provided code structure. You'll find:
- Sample place data
- Function stubs to implement
- Test cases to verify your work

### Running Tests

```bash
# Run all tests
python week09_starter.py

# Run specific test
python week09_starter.py --test exercise1
```

---

## Exercise 1: Pure Functions (20 minutes)

### Background

A **pure function** always returns the same output for the same input and has no side effects. This makes functions predictable and easy to test.

### Task 1.1: Implement `calculate_efficiency_score`

Write a pure function that calculates an efficiency score for a place.

```python
def calculate_efficiency_score(place: dict) -> float:
    """
    Calculate efficiency score: rating / sqrt(walk_time)

    Args:
        place: Dictionary with 'rating' and 'walk_time' keys

    Returns:
        Efficiency score rounded to 2 decimal places

    Example:
        >>> place = {"name": "Pizza A", "rating": 4.5, "walk_time": 9}
        >>> calculate_efficiency_score(place)
        1.5
    """
    # YOUR CODE HERE
    pass
```

**Hint:** Use `math.sqrt()` for square root.

### Task 1.2: Implement `add_efficiency_score`

Write a pure function that adds the efficiency score to a place WITHOUT modifying the original.

```python
def add_efficiency_score(place: dict) -> dict:
    """
    Return a NEW dictionary with efficiency_score added.

    Args:
        place: Original place dictionary

    Returns:
        New dictionary with all original fields plus 'efficiency_score'

    Example:
        >>> place = {"name": "Pizza A", "rating": 4.5, "walk_time": 9}
        >>> result = add_efficiency_score(place)
        >>> result['efficiency_score']
        1.5
        >>> 'efficiency_score' in place  # Original unchanged
        False
    """
    # YOUR CODE HERE
    pass
```

**Hint:** Use `{**place, "new_key": value}` to create a copy with a new field.

### Task 1.3: Verify Purity

Write a test that proves your function doesn't modify the original:

```python
def test_purity():
    """Test that add_efficiency_score doesn't modify original."""
    original = {"name": "Test", "rating": 4.0, "walk_time": 4}
    original_copy = dict(original)  # Make a copy to compare

    result = add_efficiency_score(original)

    # Verify original is unchanged
    assert original == original_copy, "Original was modified!"
    # Verify result has new field
    assert "efficiency_score" in result
    # Verify result has all original fields
    assert result["name"] == original["name"]

    print("Purity test passed!")
```

---

## Exercise 2: Lambda Functions (20 minutes)

### Task 2.1: Basic Lambdas

Convert these regular functions to lambda expressions:

```python
# Convert to lambda
def get_rating(place):
    return place["rating"]

# Your lambda:
get_rating_lambda = lambda place: ???

# Convert to lambda
def is_nearby(place, max_time=15):
    return place["walk_time"] <= max_time

# Your lambda (with default):
is_nearby_lambda = lambda place, max_time=15: ???

# Convert to lambda
def format_place_name(place):
    return f"{place['name']} ({place['rating']}*)"

# Your lambda:
format_place_name_lambda = lambda place: ???
```

### Task 2.2: Lambdas with Conditionals

Write lambdas using conditional expressions:

```python
# Return "Nearby" if walk_time <= 10, else "Far"
distance_category = lambda place: ???

# Return rating if >= 4.0, else 0 (for filtering purposes)
rating_or_zero = lambda place: ???

# Return the better place (higher rating)
better_place = lambda p1, p2: ???
```

### Task 2.3: Lambda in sorted()

Use lambdas to sort the places:

```python
places = [
    {"name": "A", "rating": 4.2, "walk_time": 10, "price": 15},
    {"name": "B", "rating": 4.8, "walk_time": 5, "price": 25},
    {"name": "C", "rating": 4.5, "walk_time": 8, "price": 12},
]

# Sort by rating (highest first)
by_rating = sorted(places, key=???, reverse=True)

# Sort by walk_time (shortest first)
by_time = sorted(places, key=???)

# Sort by price (cheapest first)
by_price = sorted(places, key=???)

# Sort by value (rating / price, highest first)
by_value = sorted(places, key=???, reverse=True)
```

---

## Exercise 3: map() and filter() (25 minutes)

### Task 3.1: Using map()

```python
places = get_sample_places()  # From starter code

# Extract all place names using map()
names = list(map(???, places))
# Expected: ["Pizza Palace", "Burger Barn", ...]

# Extract all ratings using map()
ratings = list(map(???, places))
# Expected: [4.5, 4.2, 4.8, ...]

# Create formatted strings using map()
# Format: "Name: X.X stars"
formatted = list(map(???, places))
# Expected: ["Pizza Palace: 4.5 stars", ...]

# Add efficiency scores to all places using map()
scored_places = list(map(???, places))
```

### Task 3.2: Using filter()

```python
# Filter places within 10 minutes walk
nearby = list(filter(???, places))

# Filter places with rating >= 4.5
top_rated = list(filter(???, places))

# Filter pizza places (category == "pizza")
pizza_places = list(filter(???, places))

# Filter affordable places (price <= 15)
affordable = list(filter(???, places))

# Combined: nearby AND top-rated
best_nearby = list(filter(???, places))
```

### Task 3.3: Combining map() and filter()

```python
# Get names of places within 10 minutes walk
nearby_names = list(map(
    ???,  # Extract name
    filter(???, places)  # Filter nearby
))

# Get formatted info for top-rated places
top_rated_info = list(map(
    lambda p: f"{p['name']}: {p['rating']} stars",
    filter(???, places)
))

# Calculate average rating of nearby places
nearby_ratings = list(map(
    ???,
    filter(???, places)
))
avg_nearby_rating = sum(nearby_ratings) / len(nearby_ratings) if nearby_ratings else 0
```

---

## Exercise 4: reduce() (20 minutes)

### Task 4.1: Basic reduce()

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Sum using reduce
total = reduce(???, numbers, 0)
assert total == 15

# Product using reduce
product = reduce(???, numbers, 1)
assert product == 120

# Find maximum using reduce
maximum = reduce(???, numbers)
assert maximum == 5

# Concatenate strings
words = ["Hello", " ", "World", "!"]
sentence = reduce(???, words, "")
assert sentence == "Hello World!"
```

### Task 4.2: reduce() with Places

```python
places = get_sample_places()

# Calculate total walk time to visit all places
total_walk_time = reduce(???, places, 0)

# Calculate total price of all places
total_price = reduce(???, places, 0)

# Find the place with highest rating
best_place = reduce(???, places)

# Find the place with shortest walk time
closest_place = reduce(???, places)

# Build a summary string
# Expected: "Pizza Palace (4.5*), Burger Barn (4.2*), ..."
summary = reduce(
    ???,
    places,
    ""
).strip(", ")
```

### Task 4.3: Grouping with reduce()

```python
# Group places by category
# Expected: {"pizza": [...], "burger": [...], ...}
def group_by_category(places):
    def reducer(acc, place):
        category = place["category"]
        if category not in acc:
            acc[category] = []
        acc[category].append(place)
        return acc

    return reduce(reducer, places, {})

grouped = group_by_category(places)

# Verify
assert "pizza" in grouped
assert len(grouped["pizza"]) == 2  # Two pizza places
```

---

## Exercise 5: Sorting (20 minutes)

### Task 5.1: Basic Sorting

```python
places = get_sample_places()

# Sort by rating (highest first)
by_rating_desc = sorted(places, key=???, reverse=True)
assert by_rating_desc[0]["name"] == "Sushi Supreme"  # 4.8 rating

# Sort by rating (lowest first)
by_rating_asc = sorted(places, key=???)
assert by_rating_asc[0]["rating"] == min(p["rating"] for p in places)

# Sort by name (alphabetically)
by_name = sorted(places, key=???)
assert by_name[0]["name"] == "Burger Barn"  # B comes first

# Sort by walk_time (shortest first)
by_time = sorted(places, key=???)
assert by_time[0]["walk_time"] == min(p["walk_time"] for p in places)
```

### Task 5.2: Multi-Level Sorting

```python
# Places with some same ratings for testing
test_places = [
    {"name": "A", "rating": 4.5, "walk_time": 10},
    {"name": "B", "rating": 4.5, "walk_time": 5},
    {"name": "C", "rating": 4.5, "walk_time": 8},
    {"name": "D", "rating": 4.2, "walk_time": 3},
]

# Sort by rating (desc), then by walk_time (asc) for ties
# Hint: Use tuple (-rating, walk_time) as key
sorted_multi = sorted(test_places, key=???)

# Expected order: B (4.5, 5min), C (4.5, 8min), A (4.5, 10min), D (4.2, 3min)
assert sorted_multi[0]["name"] == "B"
assert sorted_multi[1]["name"] == "C"
assert sorted_multi[2]["name"] == "A"
assert sorted_multi[3]["name"] == "D"
```

### Task 5.3: Sorting with Calculated Values

```python
places = get_sample_places()

# Sort by efficiency score (rating / sqrt(walk_time))
import math
by_efficiency = sorted(
    places,
    key=???,
    reverse=True
)

# Sort by value score (rating / price)
by_value = sorted(
    places,
    key=???,
    reverse=True
)

print("Most efficient places:")
for p in by_efficiency[:3]:
    score = p["rating"] / math.sqrt(p["walk_time"])
    print(f"  {p['name']}: efficiency={score:.2f}")
```

---

## Exercise 6: Data Pipelines (25 minutes)

### Task 6.1: Simple Pipeline

Build a pipeline that:
1. Filters places within 12 minutes walk
2. Filters places with rating >= 4.0
3. Sorts by rating (highest first)
4. Takes top 3

```python
def get_top_nearby_places(places, max_walk_time=12, min_rating=4.0, top_n=3):
    """
    Pipeline: Filter by time -> Filter by rating -> Sort -> Take top N
    """
    # YOUR CODE HERE
    # Hint: You can do this in one statement or break it into steps
    pass

# Test
places = get_sample_places()
result = get_top_nearby_places(places)
assert len(result) <= 3
assert all(p["walk_time"] <= 12 for p in result)
assert all(p["rating"] >= 4.0 for p in result)
```

### Task 6.2: Pipeline with Transformation

Build a pipeline that:
1. Filters places by category
2. Adds efficiency score to each place
3. Sorts by efficiency score
4. Returns top N places

```python
def get_best_in_category(places, category, top_n=3):
    """
    Get the most efficient places in a category.

    Pipeline:
    1. Filter by category
    2. Add efficiency score
    3. Sort by efficiency score (descending)
    4. Take top N
    """
    # YOUR CODE HERE
    pass

# Test
places = get_sample_places()
best_pizza = get_best_in_category(places, "pizza", top_n=2)
assert len(best_pizza) <= 2
assert all(p["category"] == "pizza" for p in best_pizza)
assert all("efficiency_score" in p for p in best_pizza)
```

### Task 6.3: Complete Recommendation Pipeline

Build a complete place recommendation system:

```python
def recommend_places(
    places,
    category=None,        # Optional category filter
    max_walk_time=15,     # Maximum walk time in minutes
    min_rating=0.0,       # Minimum rating
    max_price=float('inf'),  # Maximum price
    sort_by="efficiency", # "efficiency", "rating", "time", "price"
    top_n=5               # Number of results
):
    """
    Recommend places based on multiple criteria.

    Pipeline:
    1. Filter by category (if specified)
    2. Filter by walk time
    3. Filter by rating
    4. Filter by price
    5. Add efficiency score
    6. Sort by specified field
    7. Take top N

    Returns:
        List of recommended places with efficiency scores
    """
    # YOUR CODE HERE
    pass

# Test cases
places = get_sample_places()

# Test 1: Best nearby affordable places
result1 = recommend_places(
    places,
    max_walk_time=10,
    max_price=15,
    sort_by="efficiency",
    top_n=3
)
print("Best nearby affordable places:")
for p in result1:
    print(f"  {p['name']}: {p['rating']}*, {p['walk_time']}min, ${p['price']}")

# Test 2: Best pizza places
result2 = recommend_places(
    places,
    category="pizza",
    sort_by="rating",
    top_n=2
)
print("\nBest pizza places:")
for p in result2:
    print(f"  {p['name']}: {p['rating']}*")

# Test 3: Quick options sorted by time
result3 = recommend_places(
    places,
    max_walk_time=8,
    sort_by="time",
    top_n=3
)
print("\nQuickest options:")
for p in result3:
    print(f"  {p['name']}: {p['walk_time']}min")
```

---

## Exercise 7: List Comprehensions vs Functional (15 minutes)

### Task 7.1: Convert Between Styles

Convert each functional expression to a list comprehension and vice versa:

```python
places = get_sample_places()

# 1. map() to comprehension
ratings_map = list(map(lambda p: p["rating"], places))
ratings_comp = ???  # Convert to list comprehension

# 2. filter() to comprehension
nearby_filter = list(filter(lambda p: p["walk_time"] <= 10, places))
nearby_comp = ???  # Convert to list comprehension

# 3. map() + filter() to comprehension
names_func = list(map(
    lambda p: p["name"],
    filter(lambda p: p["rating"] >= 4.5, places)
))
names_comp = ???  # Convert to list comprehension

# 4. Comprehension to map() + filter()
scored_comp = [
    {**p, "score": p["rating"] / p["walk_time"]}
    for p in places
    if p["walk_time"] > 0
]
scored_func = ???  # Convert to map() + filter()
```

### Task 7.2: When to Use Which?

For each scenario, decide whether to use list comprehension or map/filter:

```python
# Scenario 1: Simple extraction
# Which is better?
names_comp = [p["name"] for p in places]
names_map = list(map(lambda p: p["name"], places))

# Scenario 2: Complex transformation
def complex_transform(place):
    """Multi-line transformation logic."""
    score = place["rating"] / math.sqrt(place["walk_time"])
    category = place["category"].upper()
    return {
        "name": place["name"],
        "score": round(score, 2),
        "category": category,
        "is_recommended": score > 1.5
    }

# Which is better for complex_transform?
# A: [complex_transform(p) for p in places]
# B: list(map(complex_transform, places))

# Scenario 3: Multiple iterables
list1 = [1, 2, 3]
list2 = [10, 20, 30]
# Which is better for combining corresponding elements?
# A: [a + b for a, b in zip(list1, list2)]
# B: list(map(lambda a, b: a + b, list1, list2))
```

---

## Bonus Challenges

### Challenge 1: Functional Statistics

Implement statistics functions using only functional programming (no loops):

```python
def functional_statistics(places):
    """
    Calculate statistics using map, filter, reduce.
    No for loops allowed!
    """
    ratings = list(map(lambda p: p["rating"], places))

    stats = {
        "count": len(ratings),
        "sum": reduce(???, ratings, 0),
        "min": reduce(???, ratings),
        "max": reduce(???, ratings),
        "average": ???,
    }

    # Bonus: Calculate standard deviation functionally
    # stats["std_dev"] = ???

    return stats
```

### Challenge 2: Compose Functions

Implement a `compose` function that combines multiple functions:

```python
def compose(*functions):
    """
    Compose functions right to left.
    compose(f, g, h)(x) == f(g(h(x)))
    """
    # YOUR CODE HERE
    pass

# Test
add_one = lambda x: x + 1
double = lambda x: x * 2
square = lambda x: x ** 2

# Should compute: square(double(add_one(5))) = square(double(6)) = square(12) = 144
composed = compose(square, double, add_one)
assert composed(5) == 144
```

### Challenge 3: Lazy Pipeline

Implement a lazy pipeline using generators:

```python
def lazy_pipeline(data, *operations):
    """
    Apply operations lazily using generators.
    Each operation is a function that takes an iterable and yields items.
    """
    result = data
    for op in operations:
        result = op(result)
    return result

# Usage
def filter_nearby(places):
    for p in places:
        if p["walk_time"] <= 10:
            yield p

def add_scores(places):
    for p in places:
        yield {**p, "score": p["rating"] / p["walk_time"]}

def sort_by_score(places):
    # Note: sorting requires consuming the whole iterator
    yield from sorted(places, key=lambda p: p["score"], reverse=True)

# This should work lazily until sort
result = lazy_pipeline(
    get_sample_places(),
    filter_nearby,
    add_scores,
    sort_by_score
)

# Only now does it execute
for place in result:
    print(f"{place['name']}: {place['score']:.2f}")
```

---

## Submission Checklist

Before submitting, verify:

- [ ] All exercises completed in `week09_starter.py`
- [ ] All test cases pass (`python week09_starter.py`)
- [ ] Code uses functional patterns (pure functions, immutability)
- [ ] No use of `for` loops where functional alternatives exist
- [ ] Code is well-documented with docstrings
- [ ] Bonus challenges attempted (optional)

---

## Summary

In this lab, you practiced:

| Concept | What You Learned |
|---------|------------------|
| **Pure Functions** | Writing functions without side effects |
| **Immutability** | Creating new data instead of modifying |
| **Lambda** | Writing concise anonymous functions |
| **map()** | Transforming every element in a collection |
| **filter()** | Selecting elements that match criteria |
| **reduce()** | Combining elements into a single value |
| **sorted()** | Ordering data with custom keys |
| **Pipelines** | Chaining operations for data processing |

### Key Takeaways

1. **Prefer pure functions** - they're easier to test and debug
2. **Don't modify data** - create new copies instead
3. **Use lambdas for simple operations** - but named functions for complex logic
4. **List comprehensions are often more Pythonic** than map/filter
5. **Pipelines make data processing clear** - break complex operations into stages
