# Week 9: Functional Patterns & Sorting

## Lecture Overview (3 Hours)

**Phase 3: Algorithms & Logic** — "Making Smart Decisions"

### Learning Objectives
By the end of this lecture, students will be able to:
1. Understand the principles of functional programming in Python
2. Use `map`, `filter`, and `reduce` to process collections
3. Write and use lambda functions effectively
4. Understand immutability and why it matters
5. Sort data using custom key functions
6. Chain operations to build data processing pipelines
7. Apply functional patterns to filter and sort places by rating and walk time

### Prerequisites
- Week 2: Lists, Loops & Dictionaries
- Week 3: JSON & File I/O
- Week 8: OSRM API (Real Routing) - understanding of place data structures

---

# Hour 1: Introduction to Functional Programming

## 1.1 What is Functional Programming?

### Programming Paradigms

There are different ways to think about and structure programs:

| Paradigm | Key Idea | Example |
|----------|----------|---------|
| **Imperative** | Step-by-step instructions | "Add 1 to x, then add 1 again" |
| **Object-Oriented** | Objects with state and behavior | "The counter increments itself" |
| **Functional** | Transform data with functions | "Apply increment twice to x" |

Python supports all three paradigms, but this week we focus on **functional programming (FP)**.

### Core Principles of Functional Programming

```
┌─────────────────────────────────────────────────────────────────┐
│                 Functional Programming Principles               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. PURE FUNCTIONS                                              │
│     - Same input always produces same output                    │
│     - No side effects (doesn't modify external state)           │
│                                                                 │
│  2. IMMUTABILITY                                                │
│     - Data is never modified in place                           │
│     - Instead, create new data with changes                     │
│                                                                 │
│  3. FIRST-CLASS FUNCTIONS                                       │
│     - Functions can be passed as arguments                      │
│     - Functions can be returned from other functions            │
│     - Functions can be stored in variables                      │
│                                                                 │
│  4. DECLARATIVE STYLE                                           │
│     - Describe WHAT you want, not HOW to do it                  │
│     - Focus on transformations, not steps                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Why Functional Programming Matters

1. **Easier to Test**: Pure functions are predictable
2. **Easier to Debug**: No hidden state changes
3. **Easier to Parallelize**: No shared mutable state
4. **More Readable**: Describes intent, not mechanics

---

## 1.2 Pure Functions vs Impure Functions

### What is a Pure Function?

A **pure function**:
- Always returns the same output for the same input
- Has no side effects (doesn't modify anything outside itself)

```python
# PURE FUNCTION - Always returns same result for same input
def add(a, b):
    return a + b

# Calling add(2, 3) will ALWAYS return 5
print(add(2, 3))  # 5
print(add(2, 3))  # 5
print(add(2, 3))  # 5
```

### What is an Impure Function?

An **impure function** either:
- Returns different results for the same input, OR
- Modifies something outside itself (side effect)

```python
# IMPURE - Modifies external state (side effect)
total = 0
def add_to_total(x):
    global total
    total += x  # Side effect: modifies global variable
    return total

print(add_to_total(5))  # 5
print(add_to_total(5))  # 10  <- Different result for same input!
print(add_to_total(5))  # 15

# IMPURE - Depends on external state
import random
def add_random(x):
    return x + random.randint(1, 10)  # Different result each time

print(add_random(5))  # Maybe 8
print(add_random(5))  # Maybe 12
```

### Visual Comparison

```
PURE FUNCTION:
                    ┌─────────┐
    Input A ───────>│         │
                    │  Pure   │───────> Output (always same)
    Input B ───────>│Function │
                    └─────────┘

IMPURE FUNCTION:
                    ┌─────────┐
    Input A ───────>│         │───────> Output (may vary)
                    │ Impure  │
    Input B ───────>│Function │───────> Side Effects
                    └─────────┘               │
                         ^                    v
                         └──── Global State ──┘
```

### Real-World Example: Processing Places

```python
places = [
    {"name": "Pizza A", "rating": 4.2},
    {"name": "Pizza B", "rating": 4.8},
]

# IMPURE: Modifies the original list
def add_place_impure(places, new_place):
    places.append(new_place)  # Side effect!
    return places

# PURE: Returns a new list, original unchanged
def add_place_pure(places, new_place):
    return places + [new_place]  # Creates new list

# Test the difference
new_place = {"name": "Pizza C", "rating": 4.5}

# With impure function
result = add_place_impure(places, new_place)
print(len(places))  # 3 - Original was modified!

# Reset
places = [
    {"name": "Pizza A", "rating": 4.2},
    {"name": "Pizza B", "rating": 4.8},
]

# With pure function
result = add_place_pure(places, new_place)
print(len(places))  # 2 - Original unchanged!
print(len(result))  # 3 - New list has the addition
```

---

## 1.3 Immutability

### What is Immutability?

**Immutable** = cannot be changed after creation

```python
# IMMUTABLE types in Python
string = "hello"
number = 42
tuple_data = (1, 2, 3)

# These operations create NEW objects, not modify existing ones
new_string = string.upper()  # "HELLO" - new string
print(string)  # "hello" - original unchanged

# MUTABLE types in Python
list_data = [1, 2, 3]
dict_data = {"a": 1}

# These operations modify IN PLACE
list_data.append(4)  # Modifies original
print(list_data)  # [1, 2, 3, 4]
```

### Why Immutability Matters

```
WITH MUTABLE DATA:

    Function A ──┐                  ┌─────────┐
                 ├──> Shared List ──│ Chaos!  │
    Function B ──┘    [1, 2, 3]     │ Who     │
                         │          │ changed │
                         v          │ what?   │
                      [1, 2, 3, ?]  └─────────┘

WITH IMMUTABLE DATA:

    Function A ──> Original [1, 2, 3] (unchanged)
                        │
                        v
    Function B ──> New List [1, 2, 3, 4] (safe copy)
```

Benefits of immutability:
1. **Predictable**: Data never changes unexpectedly
2. **Safe Sharing**: Multiple functions can use same data
3. **Easy Undo**: Keep old versions easily
4. **Thread Safe**: No race conditions in parallel code

### Applying Immutability to Our Project

```python
places = [
    {"name": "Pizza A", "rating": 4.2, "walk_time": 8},
    {"name": "Pizza B", "rating": 4.8, "walk_time": 12},
    {"name": "Pizza C", "rating": 3.9, "walk_time": 5},
    {"name": "Pizza D", "rating": 4.5, "walk_time": 20},
]

# WRONG WAY (mutable): Modifies original list
def filter_nearby_wrong(places, max_time):
    # This destroys information!
    i = 0
    while i < len(places):
        if places[i]["walk_time"] > max_time:
            places.pop(i)  # Removes from original!
        else:
            i += 1
    return places

# RIGHT WAY (immutable): Creates new list
def filter_nearby_right(places, max_time):
    return [p for p in places if p["walk_time"] <= max_time]

# Test
nearby = filter_nearby_right(places, 15)
print(f"Nearby places: {len(nearby)}")  # 3
print(f"All places: {len(places)}")     # 4 - Original preserved!
```

---

## 1.4 First-Class Functions

### Functions as Values

In Python, functions are **first-class citizens** - they can be:
- Stored in variables
- Passed as arguments
- Returned from other functions

```python
# Store function in variable
def greet(name):
    return f"Hello, {name}!"

say_hello = greet  # Note: no parentheses
print(say_hello("Alice"))  # "Hello, Alice!"

# Functions in a list
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b

operations = [add, subtract, multiply]

for op in operations:
    print(op(10, 5))  # 15, 5, 50
```

### Passing Functions as Arguments

```python
def apply_twice(func, value):
    """Apply a function twice to a value."""
    return func(func(value))

def add_one(x):
    return x + 1

def double(x):
    return x * 2

print(apply_twice(add_one, 5))  # 7 (5 -> 6 -> 7)
print(apply_twice(double, 3))   # 12 (3 -> 6 -> 12)
```

### Returning Functions from Functions

```python
def make_multiplier(n):
    """Return a function that multiplies by n."""
    def multiplier(x):
        return x * n
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

### Why This Matters

First-class functions enable **higher-order functions** like `map`, `filter`, and `sorted` - the workhorses of functional programming.

```python
# We can pass any function to sorted()
places = [
    {"name": "Pizza A", "rating": 4.2},
    {"name": "Pizza B", "rating": 4.8},
]

def get_rating(place):
    return place["rating"]

# Pass our function to sorted()
sorted_places = sorted(places, key=get_rating, reverse=True)
```

---

# Hour 2: Lambda Functions and Higher-Order Functions

## 2.1 Lambda Functions

### What is a Lambda?

A **lambda** is an anonymous (nameless) function defined in a single expression.

```python
# Regular function
def add(a, b):
    return a + b

# Lambda equivalent
add_lambda = lambda a, b: a + b

# Both work the same way
print(add(2, 3))        # 5
print(add_lambda(2, 3)) # 5
```

### Lambda Syntax

```
lambda arguments: expression
       │              │
       │              └── Single expression (returned automatically)
       │
       └── Comma-separated parameters
```

Examples:
```python
# No arguments
say_hello = lambda: "Hello!"

# One argument
square = lambda x: x ** 2

# Multiple arguments
add = lambda a, b: a + b

# With conditional expression
abs_value = lambda x: x if x >= 0 else -x
```

### When to Use Lambdas

Lambdas are perfect for **short, one-time-use functions**:

```python
# GOOD: Lambda as argument to sorted()
places = [{"name": "A", "rating": 4.2}, {"name": "B", "rating": 4.8}]
sorted_places = sorted(places, key=lambda p: p["rating"])

# BAD: Lambda for complex logic (use regular function)
process = lambda x: x.strip().lower().replace(" ", "_") if x else ""  # Hard to read!

# BETTER: Regular function
def process(x):
    """Convert string to snake_case."""
    if not x:
        return ""
    return x.strip().lower().replace(" ", "_")
```

### Lambda Limitations

Lambdas can only contain **expressions**, not **statements**:

```python
# This WON'T work - assignments are statements
# bad = lambda x: y = x + 1  # SyntaxError!

# This WON'T work - print is okay, but multiple statements aren't
# bad = lambda x: print(x); return x  # SyntaxError!

# This WORKS - single expression with conditional
good = lambda x: x + 1 if x > 0 else 0
```

---

## 2.2 The map() Function

### What is map()?

`map()` applies a function to every item in an iterable:

```
map(function, iterable)
         │         │
         │         └── List, tuple, or any iterable
         │
         └── Function to apply to each element

    [a, b, c, d]
         │
         │  map(f, ...)
         v
    [f(a), f(b), f(c), f(d)]
```

### Basic map() Examples

```python
# Square every number
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x ** 2, numbers)
print(list(squared))  # [1, 4, 9, 16, 25]

# Convert to uppercase
names = ["alice", "bob", "charlie"]
upper_names = map(str.upper, names)
print(list(upper_names))  # ["ALICE", "BOB", "CHARLIE"]

# map() returns an iterator, not a list!
result = map(lambda x: x * 2, [1, 2, 3])
print(result)       # <map object at 0x...>
print(list(result)) # [2, 4, 6]
```

### map() with Multiple Iterables

```python
# Add corresponding elements from two lists
list1 = [1, 2, 3]
list2 = [10, 20, 30]

sums = map(lambda a, b: a + b, list1, list2)
print(list(sums))  # [11, 22, 33]

# Combine first and last names
first_names = ["Alice", "Bob", "Charlie"]
last_names = ["Smith", "Jones", "Brown"]

full_names = map(lambda f, l: f"{f} {l}", first_names, last_names)
print(list(full_names))  # ["Alice Smith", "Bob Jones", "Charlie Brown"]
```

### map() for Our Project

```python
places = [
    {"name": "Pizza A", "rating": 4.2, "walk_time": 8},
    {"name": "Pizza B", "rating": 4.8, "walk_time": 12},
    {"name": "Pizza C", "rating": 3.9, "walk_time": 5},
]

# Extract just the names
names = map(lambda p: p["name"], places)
print(list(names))  # ["Pizza A", "Pizza B", "Pizza C"]

# Calculate score (rating / walk_time)
def calculate_score(place):
    return {
        **place,  # Copy all existing fields
        "score": round(place["rating"] / place["walk_time"], 2)
    }

scored_places = list(map(calculate_score, places))
for p in scored_places:
    print(f"{p['name']}: score = {p['score']}")
```

---

## 2.3 The filter() Function

### What is filter()?

`filter()` keeps only items that pass a test (predicate function):

```
filter(predicate, iterable)
          │           │
          │           └── Items to filter
          │
          └── Function returning True/False

    [a, b, c, d]  where predicate(a)=True, predicate(b)=False, etc.
         │
         │  filter(predicate, ...)
         v
    [a, c]  (only items where predicate returned True)
```

### Basic filter() Examples

```python
# Keep only even numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = filter(lambda x: x % 2 == 0, numbers)
print(list(evens))  # [2, 4, 6, 8, 10]

# Keep only non-empty strings
strings = ["hello", "", "world", "", "python"]
non_empty = filter(lambda s: s != "", strings)
print(list(non_empty))  # ["hello", "world", "python"]

# Shortcut: filter with None removes "falsy" values
values = [0, 1, "", "hello", None, [], [1, 2]]
truthy = filter(None, values)
print(list(truthy))  # [1, "hello", [1, 2]]
```

### filter() for Our Project

```python
places = [
    {"name": "Pizza A", "rating": 4.2, "walk_time": 8},
    {"name": "Pizza B", "rating": 4.8, "walk_time": 12},
    {"name": "Pizza C", "rating": 3.9, "walk_time": 5},
    {"name": "Pizza D", "rating": 4.5, "walk_time": 20},
]

# Filter places within 15 minutes walk
nearby = filter(lambda p: p["walk_time"] <= 15, places)
print("Nearby places:")
for p in nearby:
    print(f"  {p['name']}: {p['walk_time']} min")

# Filter high-rated places (4.0+)
highly_rated = filter(lambda p: p["rating"] >= 4.0, places)
print("\nHighly rated places:")
for p in highly_rated:
    print(f"  {p['name']}: {p['rating']} stars")

# Combined: nearby AND highly rated
good_nearby = filter(
    lambda p: p["walk_time"] <= 15 and p["rating"] >= 4.0,
    places
)
print("\nGood nearby places:")
for p in good_nearby:
    print(f"  {p['name']}: {p['rating']} stars, {p['walk_time']} min")
```

---

## 2.4 The reduce() Function

### What is reduce()?

`reduce()` combines all elements into a single value:

```
from functools import reduce

reduce(function, iterable, initial)
          │          │        │
          │          │        └── Starting value (optional)
          │          │
          │          └── Items to combine
          │
          └── Function taking (accumulator, current_item)

    [a, b, c, d]
         │
         │  reduce(f, ..., init)
         v
    f(f(f(f(init, a), b), c), d)  →  single result
```

### Visual Explanation

```
reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0)

Step 1: acc=0,  x=1  →  0 + 1 = 1
Step 2: acc=1,  x=2  →  1 + 2 = 3
Step 3: acc=3,  x=3  →  3 + 3 = 6
Step 4: acc=6,  x=4  →  6 + 4 = 10

Result: 10
```

### Basic reduce() Examples

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Sum all numbers
total = reduce(lambda acc, x: acc + x, numbers, 0)
print(total)  # 15

# Product of all numbers
product = reduce(lambda acc, x: acc * x, numbers, 1)
print(product)  # 120

# Find maximum
maximum = reduce(lambda acc, x: x if x > acc else acc, numbers)
print(maximum)  # 5

# Concatenate strings
words = ["Hello", " ", "World", "!"]
sentence = reduce(lambda acc, s: acc + s, words, "")
print(sentence)  # "Hello World!"
```

### reduce() for Our Project

```python
from functools import reduce

places = [
    {"name": "Pizza A", "rating": 4.2, "walk_time": 8},
    {"name": "Pizza B", "rating": 4.8, "walk_time": 12},
    {"name": "Pizza C", "rating": 3.9, "walk_time": 5},
    {"name": "Pizza D", "rating": 4.5, "walk_time": 20},
]

# Calculate average rating
total_rating = reduce(lambda acc, p: acc + p["rating"], places, 0)
average_rating = total_rating / len(places)
print(f"Average rating: {average_rating:.2f}")  # 4.35

# Find the best-rated place
best = reduce(
    lambda acc, p: p if p["rating"] > acc["rating"] else acc,
    places
)
print(f"Best place: {best['name']} ({best['rating']} stars)")

# Total walk time to visit all places
total_time = reduce(lambda acc, p: acc + p["walk_time"], places, 0)
print(f"Total walk time: {total_time} min")
```

### When to Use reduce()

`reduce()` is powerful but can be hard to read. Python provides built-in alternatives for common cases:

```python
numbers = [1, 2, 3, 4, 5]

# Instead of reduce for sum
total = sum(numbers)  # Clearer than reduce!

# Instead of reduce for min/max
minimum = min(numbers)
maximum = max(numbers)

# Instead of reduce for any/all
has_even = any(x % 2 == 0 for x in numbers)
all_positive = all(x > 0 for x in numbers)

# Use reduce when you need custom combination logic
from functools import reduce

# Flatten nested lists
nested = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda acc, lst: acc + lst, nested, [])
print(flat)  # [1, 2, 3, 4, 5, 6]
```

---

# Hour 3: Sorting and Data Pipelines

## 3.1 Sorting with sorted()

### Basic Sorting

```python
# Sort numbers (ascending by default)
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_nums = sorted(numbers)
print(sorted_nums)  # [1, 1, 2, 3, 4, 5, 6, 9]

# Sort in descending order
desc_nums = sorted(numbers, reverse=True)
print(desc_nums)  # [9, 6, 5, 4, 3, 2, 1, 1]

# Note: sorted() returns a NEW list, original unchanged
print(numbers)  # [3, 1, 4, 1, 5, 9, 2, 6] - still original order
```

### Sorting with key Functions

The `key` parameter specifies a function that extracts a comparison key:

```python
# Sort strings by length
words = ["python", "is", "awesome", "and", "fun"]
by_length = sorted(words, key=len)
print(by_length)  # ["is", "and", "fun", "python", "awesome"]

# Sort case-insensitively
names = ["Alice", "bob", "Charlie", "dave"]
by_name = sorted(names, key=str.lower)
print(by_name)  # ["Alice", "bob", "Charlie", "dave"]

# Sort by absolute value
numbers = [-5, 2, -3, 1, -4]
by_abs = sorted(numbers, key=abs)
print(by_abs)  # [1, 2, -3, -4, -5]
```

### Sorting Dictionaries

```python
places = [
    {"name": "Pizza A", "rating": 4.2, "walk_time": 8},
    {"name": "Pizza B", "rating": 4.8, "walk_time": 12},
    {"name": "Pizza C", "rating": 3.9, "walk_time": 5},
    {"name": "Pizza D", "rating": 4.5, "walk_time": 20},
]

# Sort by rating (highest first)
by_rating = sorted(places, key=lambda p: p["rating"], reverse=True)
print("By rating:")
for p in by_rating:
    print(f"  {p['name']}: {p['rating']} stars")

# Sort by walk time (shortest first)
by_time = sorted(places, key=lambda p: p["walk_time"])
print("\nBy walk time:")
for p in by_time:
    print(f"  {p['name']}: {p['walk_time']} min")

# Sort by name alphabetically
by_name = sorted(places, key=lambda p: p["name"])
print("\nBy name:")
for p in by_name:
    print(f"  {p['name']}")
```

### Multi-Level Sorting

Sort by multiple criteria using tuples:

```python
places = [
    {"name": "Pizza A", "rating": 4.2, "walk_time": 8},
    {"name": "Pizza B", "rating": 4.2, "walk_time": 12},  # Same rating as A
    {"name": "Pizza C", "rating": 3.9, "walk_time": 5},
    {"name": "Pizza D", "rating": 4.2, "walk_time": 6},   # Same rating as A, B
]

# Sort by rating (desc), then by walk_time (asc) for ties
# Note: negate rating for descending order
sorted_places = sorted(
    places,
    key=lambda p: (-p["rating"], p["walk_time"])
)

print("By rating (desc), then walk time (asc):")
for p in sorted_places:
    print(f"  {p['name']}: {p['rating']} stars, {p['walk_time']} min")
# Output:
#   Pizza D: 4.2 stars, 6 min   (highest rating, shortest time)
#   Pizza A: 4.2 stars, 8 min   (same rating, longer time)
#   Pizza B: 4.2 stars, 12 min  (same rating, longest time)
#   Pizza C: 3.9 stars, 5 min   (lowest rating)
```

### Using operator.itemgetter

For better performance and readability with dictionaries:

```python
from operator import itemgetter

places = [
    {"name": "Pizza A", "rating": 4.2, "walk_time": 8},
    {"name": "Pizza B", "rating": 4.8, "walk_time": 12},
]

# Using itemgetter instead of lambda
by_rating = sorted(places, key=itemgetter("rating"), reverse=True)

# itemgetter can get multiple keys
by_rating_then_time = sorted(places, key=itemgetter("rating", "walk_time"))
```

---

## 3.2 List Comprehensions vs map/filter

### List Comprehensions

A **list comprehension** is a concise way to create lists:

```python
# Basic syntax
[expression for item in iterable]

# With condition
[expression for item in iterable if condition]
```

### Comparing Approaches

```python
numbers = [1, 2, 3, 4, 5]

# Task 1: Square all numbers
# Using map
squared_map = list(map(lambda x: x ** 2, numbers))
# Using comprehension
squared_comp = [x ** 2 for x in numbers]
# Both give: [1, 4, 9, 16, 25]

# Task 2: Keep only even numbers
# Using filter
evens_filter = list(filter(lambda x: x % 2 == 0, numbers))
# Using comprehension
evens_comp = [x for x in numbers if x % 2 == 0]
# Both give: [2, 4]

# Task 3: Square only even numbers
# Using map + filter
result_mapfilter = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers)))
# Using comprehension
result_comp = [x ** 2 for x in numbers if x % 2 == 0]
# Both give: [4, 16]
```

### Which to Use?

| Situation | Recommended | Reason |
|-----------|-------------|--------|
| Simple transform | List comprehension | More readable |
| Simple filter | List comprehension | More Pythonic |
| Transform + filter | List comprehension | Cleaner syntax |
| Complex transform | map() with named function | Function can be tested |
| Lazy evaluation needed | map()/filter() | Returns iterator |
| Multiple iterables | map() | Built-in support |

### Practical Examples for Our Project

```python
places = [
    {"name": "Pizza A", "rating": 4.2, "walk_time": 8},
    {"name": "Pizza B", "rating": 4.8, "walk_time": 12},
    {"name": "Pizza C", "rating": 3.9, "walk_time": 5},
    {"name": "Pizza D", "rating": 4.5, "walk_time": 20},
]

# Filter nearby places (within 15 min)
nearby = [p for p in places if p["walk_time"] <= 15]

# Get names of highly rated places
top_names = [p["name"] for p in places if p["rating"] >= 4.0]

# Calculate efficiency score for each place
scored = [
    {**p, "efficiency": round(p["rating"] / p["walk_time"], 2)}
    for p in places
]

# Get nearby places sorted by rating
best_nearby = sorted(
    [p for p in places if p["walk_time"] <= 15],
    key=lambda p: p["rating"],
    reverse=True
)
```

---

## 3.3 Building Data Pipelines

### What is a Data Pipeline?

A **data pipeline** is a series of transformations applied to data:

```
Raw Data → Filter → Transform → Sort → Output
    │         │          │        │        │
    │         │          │        │        └── Final result
    │         │          │        └── Order the data
    │         │          └── Modify/enrich the data
    │         └── Remove unwanted items
    └── Starting data
```

### Chaining Operations

```python
places = [
    {"name": "Pizza A", "rating": 4.2, "walk_time": 8},
    {"name": "Pizza B", "rating": 4.8, "walk_time": 12},
    {"name": "Pizza C", "rating": 3.9, "walk_time": 5},
    {"name": "Pizza D", "rating": 4.5, "walk_time": 20},
    {"name": "Pizza E", "rating": 4.1, "walk_time": 7},
]

# Pipeline: Filter nearby → Add score → Sort by score → Take top 3
result = sorted(
    [
        {**p, "score": round(p["rating"] / p["walk_time"], 2)}
        for p in places
        if p["walk_time"] <= 15
    ],
    key=lambda p: p["score"],
    reverse=True
)[:3]

print("Top 3 nearby places by efficiency:")
for p in result:
    print(f"  {p['name']}: score={p['score']}")
```

### Breaking Down Complex Pipelines

For readability, break complex pipelines into steps:

```python
def process_places(places, max_walk_time=15, top_n=3):
    """
    Process places to find the best nearby options.

    Pipeline:
    1. Filter by walk time
    2. Add efficiency score
    3. Sort by score
    4. Return top N
    """
    # Step 1: Filter nearby places
    nearby = [p for p in places if p["walk_time"] <= max_walk_time]

    # Step 2: Add efficiency score
    scored = [
        {**p, "score": round(p["rating"] / p["walk_time"], 2)}
        for p in nearby
    ]

    # Step 3: Sort by score (highest first)
    sorted_places = sorted(scored, key=lambda p: p["score"], reverse=True)

    # Step 4: Return top N
    return sorted_places[:top_n]

# Use the pipeline
best = process_places(places, max_walk_time=15, top_n=3)
for p in best:
    print(f"{p['name']}: {p['rating']} stars, {p['walk_time']} min, score={p['score']}")
```

### Functional Pipeline with Composition

```python
from functools import reduce

def pipe(value, *functions):
    """Apply functions in sequence to a value."""
    return reduce(lambda v, f: f(v), functions, value)

# Define individual transformation functions
def filter_nearby(places, max_time=15):
    return [p for p in places if p["walk_time"] <= max_time]

def add_scores(places):
    return [
        {**p, "score": round(p["rating"] / p["walk_time"], 2)}
        for p in places
    ]

def sort_by_score(places):
    return sorted(places, key=lambda p: p["score"], reverse=True)

def take_top(n):
    return lambda places: places[:n]

# Build and run the pipeline
result = pipe(
    places,
    lambda p: filter_nearby(p, max_time=15),
    add_scores,
    sort_by_score,
    take_top(3)
)

print("Pipeline result:")
for p in result:
    print(f"  {p['name']}: score={p['score']}")
```

---

## 3.4 Practical Application: Smart Place Recommender

### Complete Example

Let's build a place recommendation system using everything we've learned:

```python
from functools import reduce
from typing import List, Dict, Any, Optional

# Type alias for clarity
Place = Dict[str, Any]

def load_sample_places() -> List[Place]:
    """Load sample place data."""
    return [
        {"name": "Pizza Palace", "rating": 4.5, "walk_time": 10, "category": "pizza"},
        {"name": "Burger Barn", "rating": 4.2, "walk_time": 5, "category": "burger"},
        {"name": "Sushi Supreme", "rating": 4.8, "walk_time": 15, "category": "sushi"},
        {"name": "Taco Town", "rating": 3.9, "walk_time": 8, "category": "mexican"},
        {"name": "Pasta Paradise", "rating": 4.6, "walk_time": 20, "category": "italian"},
        {"name": "Pizza Planet", "rating": 4.1, "walk_time": 7, "category": "pizza"},
        {"name": "Noodle Nirvana", "rating": 4.4, "walk_time": 12, "category": "asian"},
        {"name": "Salad Station", "rating": 4.0, "walk_time": 3, "category": "healthy"},
    ]

def filter_by_category(places: List[Place], category: Optional[str]) -> List[Place]:
    """Filter places by category (None means all categories)."""
    if category is None:
        return places
    return [p for p in places if p["category"] == category]

def filter_by_walk_time(places: List[Place], max_minutes: int) -> List[Place]:
    """Filter places within walking distance."""
    return [p for p in places if p["walk_time"] <= max_minutes]

def filter_by_rating(places: List[Place], min_rating: float) -> List[Place]:
    """Filter places by minimum rating."""
    return [p for p in places if p["rating"] >= min_rating]

def add_value_score(places: List[Place]) -> List[Place]:
    """Add a value score (rating / sqrt(walk_time))."""
    import math
    return [
        {**p, "value_score": round(p["rating"] / math.sqrt(p["walk_time"]), 2)}
        for p in places
    ]

def sort_places(places: List[Place], sort_by: str = "rating", descending: bool = True) -> List[Place]:
    """Sort places by specified field."""
    return sorted(places, key=lambda p: p.get(sort_by, 0), reverse=descending)

def format_place(place: Place) -> str:
    """Format a place for display."""
    score_info = f", value={place['value_score']}" if "value_score" in place else ""
    return f"{place['name']} ({place['category']}): {place['rating']}★, {place['walk_time']}min{score_info}"

def recommend_places(
    places: List[Place],
    category: Optional[str] = None,
    max_walk_time: int = 15,
    min_rating: float = 4.0,
    sort_by: str = "value_score",
    top_n: int = 5
) -> List[Place]:
    """
    Recommend places based on criteria.

    Uses a functional pipeline:
    1. Filter by category
    2. Filter by walk time
    3. Filter by rating
    4. Add value scores
    5. Sort by specified field
    6. Take top N
    """
    # Build the pipeline
    result = places
    result = filter_by_category(result, category)
    result = filter_by_walk_time(result, max_walk_time)
    result = filter_by_rating(result, min_rating)
    result = add_value_score(result)
    result = sort_places(result, sort_by)
    result = result[:top_n]

    return result

def get_statistics(places: List[Place]) -> Dict[str, Any]:
    """Calculate statistics for a list of places."""
    if not places:
        return {"count": 0}

    ratings = [p["rating"] for p in places]
    walk_times = [p["walk_time"] for p in places]

    return {
        "count": len(places),
        "avg_rating": round(sum(ratings) / len(ratings), 2),
        "min_rating": min(ratings),
        "max_rating": max(ratings),
        "avg_walk_time": round(sum(walk_times) / len(walk_times), 1),
        "total_walk_time": sum(walk_times),
    }

# Demo
if __name__ == "__main__":
    places = load_sample_places()

    print("=" * 50)
    print("SMART PLACE RECOMMENDER")
    print("=" * 50)

    # Scenario 1: Find best nearby places
    print("\n📍 Best places within 15 minutes (rating 4.0+):")
    recommendations = recommend_places(places, max_walk_time=15, min_rating=4.0)
    for p in recommendations:
        print(f"  • {format_place(p)}")

    # Scenario 2: Find pizza places
    print("\n🍕 Best pizza places:")
    pizza_places = recommend_places(places, category="pizza", max_walk_time=30)
    for p in pizza_places:
        print(f"  • {format_place(p)}")

    # Scenario 3: Quick options (under 10 min)
    print("\n⚡ Quick options (under 10 minutes):")
    quick = recommend_places(places, max_walk_time=10, min_rating=3.5, sort_by="walk_time")
    # Re-sort by walk time ascending for "quick" options
    quick = sorted(quick, key=lambda p: p["walk_time"])
    for p in quick:
        print(f"  • {format_place(p)}")

    # Statistics
    print("\n📊 Statistics for all places:")
    stats = get_statistics(places)
    print(f"  Total places: {stats['count']}")
    print(f"  Average rating: {stats['avg_rating']}★")
    print(f"  Rating range: {stats['min_rating']} - {stats['max_rating']}")
    print(f"  Average walk time: {stats['avg_walk_time']} min")
```

---

## 3.5 Summary

### Key Concepts

| Concept | Description | Example |
|---------|-------------|---------|
| **Pure Function** | Same output for same input, no side effects | `lambda x: x * 2` |
| **Immutability** | Don't modify data, create new copies | `new_list = old_list + [item]` |
| **Lambda** | Anonymous single-expression function | `lambda p: p["rating"]` |
| **map()** | Apply function to each item | `map(str.upper, names)` |
| **filter()** | Keep items that pass test | `filter(lambda x: x > 0, nums)` |
| **reduce()** | Combine items into single value | `reduce(lambda a, b: a + b, nums)` |
| **sorted()** | Sort with custom key | `sorted(places, key=lambda p: p["rating"])` |

### Common Patterns

```python
# Filter then sort
result = sorted(
    [p for p in places if p["walk_time"] <= 15],
    key=lambda p: p["rating"],
    reverse=True
)

# Transform all items
scored = [{**p, "score": p["rating"] / p["walk_time"]} for p in places]

# Get single value from list
best = max(places, key=lambda p: p["rating"])
total = sum(p["walk_time"] for p in places)
```

### Functional vs Imperative

```python
# IMPERATIVE (step by step)
result = []
for place in places:
    if place["walk_time"] <= 15:
        if place["rating"] >= 4.0:
            result.append(place)
result.sort(key=lambda p: p["rating"], reverse=True)

# FUNCTIONAL (transformations)
result = sorted(
    filter(lambda p: p["rating"] >= 4.0,
           filter(lambda p: p["walk_time"] <= 15, places)),
    key=lambda p: p["rating"],
    reverse=True
)

# PYTHONIC (list comprehension + sorted)
result = sorted(
    [p for p in places if p["walk_time"] <= 15 and p["rating"] >= 4.0],
    key=lambda p: p["rating"],
    reverse=True
)
```

---

## Next Week Preview

**Week 10: The "Traveling Salesperson" (Graph Theory Lite)**
- Permutations and combinations
- Brute force optimization
- Finding the optimal order to visit multiple places
- Introduction to graph algorithms
