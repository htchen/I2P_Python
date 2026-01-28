#!/usr/bin/env python3
"""
Week 9: Functional Patterns & Sorting - Interactive Examples

This module demonstrates functional programming concepts in Python:
- Pure functions vs impure functions
- Immutability
- Lambda functions
- map(), filter(), reduce()
- Sorting with custom keys
- Building data pipelines

Run this file to see all examples in action:
    python examples.py

Or import and use individual functions:
    from examples import filter_nearby, sort_by_rating
"""

from functools import reduce
from typing import List, Dict, Any, Callable, Optional
import math

# =============================================================================
# SECTION 1: SAMPLE DATA
# =============================================================================

def get_sample_places() -> List[Dict[str, Any]]:
    """Return sample place data for demonstrations."""
    return [
        {"name": "Pizza Palace", "rating": 4.5, "walk_time": 10, "category": "pizza", "price": 15},
        {"name": "Burger Barn", "rating": 4.2, "walk_time": 5, "category": "burger", "price": 12},
        {"name": "Sushi Supreme", "rating": 4.8, "walk_time": 15, "category": "sushi", "price": 25},
        {"name": "Taco Town", "rating": 3.9, "walk_time": 8, "category": "mexican", "price": 10},
        {"name": "Pasta Paradise", "rating": 4.6, "walk_time": 20, "category": "italian", "price": 18},
        {"name": "Pizza Planet", "rating": 4.1, "walk_time": 7, "category": "pizza", "price": 13},
        {"name": "Noodle Nirvana", "rating": 4.4, "walk_time": 12, "category": "asian", "price": 14},
        {"name": "Salad Station", "rating": 4.0, "walk_time": 3, "category": "healthy", "price": 11},
    ]


# =============================================================================
# SECTION 2: PURE VS IMPURE FUNCTIONS
# =============================================================================

def demo_pure_vs_impure():
    """Demonstrate the difference between pure and impure functions."""
    print("\n" + "=" * 60)
    print("DEMO: Pure vs Impure Functions")
    print("=" * 60)

    # --- Pure Function Example ---
    print("\n--- Pure Function ---")

    def add(a: int, b: int) -> int:
        """Pure function: always returns same result for same input."""
        return a + b

    # Calling multiple times gives consistent results
    print(f"add(2, 3) = {add(2, 3)}")
    print(f"add(2, 3) = {add(2, 3)}")
    print(f"add(2, 3) = {add(2, 3)}")
    print("(Always returns 5 - predictable!)")

    # --- Impure Function Example ---
    print("\n--- Impure Function (with side effect) ---")

    total = 0

    def add_to_total(x: int) -> int:
        """Impure function: modifies external state."""
        nonlocal total
        total += x
        return total

    print(f"total starts at: {total}")
    print(f"add_to_total(5) = {add_to_total(5)}")
    print(f"add_to_total(5) = {add_to_total(5)}")
    print(f"add_to_total(5) = {add_to_total(5)}")
    print("(Different results for same input - unpredictable!)")

    # --- Pure vs Impure with Lists ---
    print("\n--- Pure vs Impure with Lists ---")

    places = [{"name": "A", "rating": 4.0}, {"name": "B", "rating": 4.5}]

    def add_place_impure(places_list, new_place):
        """Impure: modifies the original list."""
        places_list.append(new_place)
        return places_list

    def add_place_pure(places_list, new_place):
        """Pure: creates a new list."""
        return places_list + [new_place]

    # Test impure
    places_copy = [{"name": "A", "rating": 4.0}, {"name": "B", "rating": 4.5}]
    new_place = {"name": "C", "rating": 4.2}

    print(f"Original list length: {len(places_copy)}")
    result_impure = add_place_impure(places_copy, new_place)
    print(f"After impure add - original length: {len(places_copy)} (modified!)")

    # Test pure
    places_copy = [{"name": "A", "rating": 4.0}, {"name": "B", "rating": 4.5}]
    result_pure = add_place_pure(places_copy, new_place)
    print(f"After pure add - original length: {len(places_copy)} (unchanged)")
    print(f"After pure add - result length: {len(result_pure)} (new list)")


# =============================================================================
# SECTION 3: IMMUTABILITY
# =============================================================================

def demo_immutability():
    """Demonstrate immutability concepts."""
    print("\n" + "=" * 60)
    print("DEMO: Immutability")
    print("=" * 60)

    # --- Immutable Types ---
    print("\n--- Immutable Types in Python ---")

    # Strings are immutable
    text = "hello"
    upper_text = text.upper()
    print(f"Original string: '{text}'")
    print(f"After upper(): '{upper_text}'")
    print(f"Original unchanged: '{text}'")

    # Tuples are immutable
    coords = (25.033, 121.565)
    print(f"\nTuple: {coords}")
    try:
        coords[0] = 26.0  # This will fail
    except TypeError as e:
        print(f"Cannot modify tuple: {e}")

    # --- Mutable Types ---
    print("\n--- Mutable Types (be careful!) ---")

    # Lists are mutable
    numbers = [1, 2, 3]
    print(f"Original list: {numbers}")
    numbers.append(4)
    print(f"After append: {numbers} (modified in place!)")

    # --- Immutable Approach with Lists ---
    print("\n--- Treating Lists Immutably ---")

    places = get_sample_places()[:3]
    print(f"Original places count: {len(places)}")

    # WRONG: Modifying in place
    # places.pop()  # This would modify the original!

    # RIGHT: Create new list
    filtered = [p for p in places if p["rating"] >= 4.2]
    print(f"Filtered places count: {len(filtered)}")
    print(f"Original still has: {len(places)} places")


# =============================================================================
# SECTION 4: LAMBDA FUNCTIONS
# =============================================================================

def demo_lambda_functions():
    """Demonstrate lambda function usage."""
    print("\n" + "=" * 60)
    print("DEMO: Lambda Functions")
    print("=" * 60)

    # --- Basic Lambda ---
    print("\n--- Basic Lambda Syntax ---")

    # Regular function
    def square_func(x):
        return x ** 2

    # Lambda equivalent
    square_lambda = lambda x: x ** 2

    print(f"square_func(5) = {square_func(5)}")
    print(f"square_lambda(5) = {square_lambda(5)}")

    # --- Lambda with Multiple Arguments ---
    print("\n--- Lambda with Multiple Arguments ---")

    add = lambda a, b: a + b
    multiply = lambda a, b: a * b

    print(f"add(3, 4) = {add(3, 4)}")
    print(f"multiply(3, 4) = {multiply(3, 4)}")

    # --- Lambda with Conditional ---
    print("\n--- Lambda with Conditional Expression ---")

    abs_value = lambda x: x if x >= 0 else -x
    grade = lambda score: "Pass" if score >= 60 else "Fail"

    print(f"abs_value(-5) = {abs_value(-5)}")
    print(f"abs_value(5) = {abs_value(5)}")
    print(f"grade(75) = {grade(75)}")
    print(f"grade(50) = {grade(50)}")

    # --- Lambda in sorted() ---
    print("\n--- Lambda with sorted() ---")

    places = get_sample_places()[:4]
    sorted_by_rating = sorted(places, key=lambda p: p["rating"], reverse=True)

    print("Sorted by rating (highest first):")
    for p in sorted_by_rating:
        print(f"  {p['name']}: {p['rating']} stars")


# =============================================================================
# SECTION 5: MAP FUNCTION
# =============================================================================

def demo_map_function():
    """Demonstrate the map() function."""
    print("\n" + "=" * 60)
    print("DEMO: map() Function")
    print("=" * 60)

    # --- Basic map ---
    print("\n--- Basic map() ---")

    numbers = [1, 2, 3, 4, 5]
    squared = list(map(lambda x: x ** 2, numbers))
    print(f"Original: {numbers}")
    print(f"Squared:  {squared}")

    # --- map with string operations ---
    print("\n--- map() with Strings ---")

    names = ["alice", "bob", "charlie"]
    upper_names = list(map(str.upper, names))
    print(f"Original: {names}")
    print(f"Upper:    {upper_names}")

    # --- map returns iterator ---
    print("\n--- map() Returns Iterator ---")

    result = map(lambda x: x * 2, [1, 2, 3])
    print(f"map() object: {result}")
    print(f"As list: {list(result)}")

    # Note: iterator is exhausted after first list() call
    print(f"Second list() call: {list(result)} (empty - iterator exhausted!)")

    # --- map with multiple iterables ---
    print("\n--- map() with Multiple Iterables ---")

    list1 = [1, 2, 3]
    list2 = [10, 20, 30]
    sums = list(map(lambda a, b: a + b, list1, list2))
    print(f"List 1: {list1}")
    print(f"List 2: {list2}")
    print(f"Sums:   {sums}")

    # --- map with places data ---
    print("\n--- map() with Place Data ---")

    places = get_sample_places()[:4]

    # Extract names
    names = list(map(lambda p: p["name"], places))
    print(f"Place names: {names}")

    # Add calculated field
    def add_score(place):
        return {**place, "score": round(place["rating"] / place["walk_time"], 2)}

    scored_places = list(map(add_score, places))
    print("\nPlaces with scores:")
    for p in scored_places:
        print(f"  {p['name']}: rating={p['rating']}, time={p['walk_time']}min, score={p['score']}")


# =============================================================================
# SECTION 6: FILTER FUNCTION
# =============================================================================

def demo_filter_function():
    """Demonstrate the filter() function."""
    print("\n" + "=" * 60)
    print("DEMO: filter() Function")
    print("=" * 60)

    # --- Basic filter ---
    print("\n--- Basic filter() ---")

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Original: {numbers}")
    print(f"Evens:    {evens}")

    # --- filter with None ---
    print("\n--- filter() with None (removes falsy values) ---")

    values = [0, 1, "", "hello", None, [], [1, 2], False, True]
    truthy = list(filter(None, values))
    print(f"Original: {values}")
    print(f"Truthy:   {truthy}")

    # --- filter with places ---
    print("\n--- filter() with Place Data ---")

    places = get_sample_places()

    # Filter nearby
    nearby = list(filter(lambda p: p["walk_time"] <= 10, places))
    print("Places within 10 minutes walk:")
    for p in nearby:
        print(f"  {p['name']}: {p['walk_time']} min")

    # Filter highly rated
    print("\nPlaces with rating >= 4.5:")
    top_rated = list(filter(lambda p: p["rating"] >= 4.5, places))
    for p in top_rated:
        print(f"  {p['name']}: {p['rating']} stars")

    # Combined filter
    print("\nPlaces: nearby AND highly rated:")
    best_nearby = list(filter(
        lambda p: p["walk_time"] <= 12 and p["rating"] >= 4.3,
        places
    ))
    for p in best_nearby:
        print(f"  {p['name']}: {p['rating']} stars, {p['walk_time']} min")


# =============================================================================
# SECTION 7: REDUCE FUNCTION
# =============================================================================

def demo_reduce_function():
    """Demonstrate the reduce() function."""
    print("\n" + "=" * 60)
    print("DEMO: reduce() Function")
    print("=" * 60)

    # --- Basic reduce ---
    print("\n--- Basic reduce() ---")

    numbers = [1, 2, 3, 4, 5]

    # Sum
    total = reduce(lambda acc, x: acc + x, numbers, 0)
    print(f"Numbers: {numbers}")
    print(f"Sum (reduce): {total}")
    print(f"Sum (built-in): {sum(numbers)}")

    # Product
    product = reduce(lambda acc, x: acc * x, numbers, 1)
    print(f"Product: {product}")

    # --- Visualizing reduce ---
    print("\n--- Visualizing reduce() step by step ---")

    def traced_add(acc, x):
        result = acc + x
        print(f"  acc={acc}, x={x} -> {result}")
        return result

    print("reduce(add, [1, 2, 3, 4], 0):")
    result = reduce(traced_add, [1, 2, 3, 4], 0)
    print(f"Final result: {result}")

    # --- reduce with places ---
    print("\n--- reduce() with Place Data ---")

    places = get_sample_places()

    # Total walk time
    total_time = reduce(lambda acc, p: acc + p["walk_time"], places, 0)
    print(f"Total walk time to all places: {total_time} min")

    # Average rating
    total_rating = reduce(lambda acc, p: acc + p["rating"], places, 0)
    avg_rating = total_rating / len(places)
    print(f"Average rating: {avg_rating:.2f} stars")

    # Find best place
    best = reduce(
        lambda acc, p: p if p["rating"] > acc["rating"] else acc,
        places
    )
    print(f"Best rated place: {best['name']} ({best['rating']} stars)")

    # --- Flatten nested lists ---
    print("\n--- reduce() to Flatten Lists ---")

    nested = [[1, 2], [3, 4], [5, 6]]
    flat = reduce(lambda acc, lst: acc + lst, nested, [])
    print(f"Nested: {nested}")
    print(f"Flat:   {flat}")


# =============================================================================
# SECTION 8: SORTING
# =============================================================================

def demo_sorting():
    """Demonstrate sorting with custom keys."""
    print("\n" + "=" * 60)
    print("DEMO: Sorting")
    print("=" * 60)

    places = get_sample_places()

    # --- Basic sorting ---
    print("\n--- Basic sorted() ---")

    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"Original:   {numbers}")
    print(f"Ascending:  {sorted(numbers)}")
    print(f"Descending: {sorted(numbers, reverse=True)}")

    # --- Sorting by key ---
    print("\n--- Sorting Places by Rating ---")

    by_rating = sorted(places, key=lambda p: p["rating"], reverse=True)
    print("By rating (highest first):")
    for p in by_rating[:5]:
        print(f"  {p['name']}: {p['rating']} stars")

    # --- Sorting by walk time ---
    print("\n--- Sorting Places by Walk Time ---")

    by_time = sorted(places, key=lambda p: p["walk_time"])
    print("By walk time (shortest first):")
    for p in by_time[:5]:
        print(f"  {p['name']}: {p['walk_time']} min")

    # --- Multi-level sorting ---
    print("\n--- Multi-Level Sorting ---")

    # Add some places with same rating for demo
    test_places = [
        {"name": "A", "rating": 4.5, "walk_time": 10},
        {"name": "B", "rating": 4.5, "walk_time": 5},
        {"name": "C", "rating": 4.2, "walk_time": 3},
        {"name": "D", "rating": 4.5, "walk_time": 8},
    ]

    # Sort by rating (desc), then walk_time (asc)
    sorted_multi = sorted(
        test_places,
        key=lambda p: (-p["rating"], p["walk_time"])
    )

    print("Sorted by rating (desc), then walk time (asc):")
    for p in sorted_multi:
        print(f"  {p['name']}: {p['rating']} stars, {p['walk_time']} min")

    # --- Using operator.itemgetter ---
    print("\n--- Using operator.itemgetter ---")

    from operator import itemgetter

    by_price = sorted(places, key=itemgetter("price"))
    print("By price (cheapest first):")
    for p in by_price[:5]:
        print(f"  {p['name']}: ${p['price']}")


# =============================================================================
# SECTION 9: LIST COMPREHENSIONS VS MAP/FILTER
# =============================================================================

def demo_comprehensions_vs_functional():
    """Compare list comprehensions with map/filter."""
    print("\n" + "=" * 60)
    print("DEMO: List Comprehensions vs map/filter")
    print("=" * 60)

    numbers = [1, 2, 3, 4, 5]
    places = get_sample_places()[:4]

    # --- Transform: map vs comprehension ---
    print("\n--- Transform: Squaring Numbers ---")

    # Using map
    squared_map = list(map(lambda x: x ** 2, numbers))
    # Using comprehension
    squared_comp = [x ** 2 for x in numbers]

    print(f"Using map():           {squared_map}")
    print(f"Using comprehension:   {squared_comp}")

    # --- Filter: filter vs comprehension ---
    print("\n--- Filter: Even Numbers ---")

    # Using filter
    evens_filter = list(filter(lambda x: x % 2 == 0, numbers))
    # Using comprehension
    evens_comp = [x for x in numbers if x % 2 == 0]

    print(f"Using filter():        {evens_filter}")
    print(f"Using comprehension:   {evens_comp}")

    # --- Combined: map + filter vs comprehension ---
    print("\n--- Combined: Square Even Numbers ---")

    # Using map + filter
    result_func = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers)))
    # Using comprehension
    result_comp = [x ** 2 for x in numbers if x % 2 == 0]

    print(f"Using map+filter:      {result_func}")
    print(f"Using comprehension:   {result_comp}")

    # --- With place data ---
    print("\n--- With Place Data ---")

    # Get names of places with rating >= 4.3
    # Using map + filter
    names_func = list(map(
        lambda p: p["name"],
        filter(lambda p: p["rating"] >= 4.3, places)
    ))
    # Using comprehension
    names_comp = [p["name"] for p in places if p["rating"] >= 4.3]

    print(f"Using map+filter:      {names_func}")
    print(f"Using comprehension:   {names_comp}")


# =============================================================================
# SECTION 10: DATA PIPELINES
# =============================================================================

def demo_data_pipelines():
    """Demonstrate building data processing pipelines."""
    print("\n" + "=" * 60)
    print("DEMO: Data Pipelines")
    print("=" * 60)

    places = get_sample_places()

    # --- Simple pipeline ---
    print("\n--- Simple Pipeline: Filter -> Sort -> Take ---")

    # Filter nearby, sort by rating, take top 3
    result = sorted(
        [p for p in places if p["walk_time"] <= 12],
        key=lambda p: p["rating"],
        reverse=True
    )[:3]

    print("Top 3 nearby places (within 12 min):")
    for p in result:
        print(f"  {p['name']}: {p['rating']} stars, {p['walk_time']} min")

    # --- Pipeline with transformation ---
    print("\n--- Pipeline with Score Calculation ---")

    # Filter -> Add Score -> Sort by Score -> Take Top 5
    pipeline_result = sorted(
        [
            {**p, "value_score": round(p["rating"] / math.sqrt(p["walk_time"]), 2)}
            for p in places
            if p["walk_time"] <= 15
        ],
        key=lambda p: p["value_score"],
        reverse=True
    )[:5]

    print("Top 5 by value score (rating / sqrt(walk_time)):")
    for p in pipeline_result:
        print(f"  {p['name']}: score={p['value_score']}, rating={p['rating']}, time={p['walk_time']}min")

    # --- Named pipeline stages ---
    print("\n--- Named Pipeline Stages ---")

    def process_places(
        places: List[Dict],
        max_walk_time: int = 15,
        min_rating: float = 0.0,
        top_n: int = 5
    ) -> List[Dict]:
        """Process places through a multi-stage pipeline."""

        # Stage 1: Filter by walk time
        stage1 = [p for p in places if p["walk_time"] <= max_walk_time]
        print(f"  Stage 1 (filter walk_time <= {max_walk_time}): {len(stage1)} places")

        # Stage 2: Filter by rating
        stage2 = [p for p in stage1 if p["rating"] >= min_rating]
        print(f"  Stage 2 (filter rating >= {min_rating}): {len(stage2)} places")

        # Stage 3: Add value score
        stage3 = [
            {**p, "value_score": round(p["rating"] / math.sqrt(p["walk_time"]), 2)}
            for p in stage2
        ]
        print(f"  Stage 3 (add value_score): {len(stage3)} places")

        # Stage 4: Sort by value score
        stage4 = sorted(stage3, key=lambda p: p["value_score"], reverse=True)
        print(f"  Stage 4 (sort by value_score): {len(stage4)} places")

        # Stage 5: Take top N
        stage5 = stage4[:top_n]
        print(f"  Stage 5 (take top {top_n}): {len(stage5)} places")

        return stage5

    print("\nRunning pipeline:")
    result = process_places(places, max_walk_time=15, min_rating=4.0, top_n=3)
    print("\nFinal result:")
    for p in result:
        print(f"  {p['name']}: value_score={p['value_score']}")


# =============================================================================
# SECTION 11: PRACTICAL EXAMPLE - PLACE RECOMMENDER
# =============================================================================

def demo_place_recommender():
    """Demonstrate a complete place recommendation system."""
    print("\n" + "=" * 60)
    print("DEMO: Smart Place Recommender")
    print("=" * 60)

    places = get_sample_places()

    # --- Helper functions (pure, composable) ---

    def filter_by_category(places: List[Dict], category: Optional[str]) -> List[Dict]:
        """Filter places by category."""
        if category is None:
            return places
        return [p for p in places if p["category"] == category]

    def filter_by_walk_time(places: List[Dict], max_minutes: int) -> List[Dict]:
        """Filter places within walking distance."""
        return [p for p in places if p["walk_time"] <= max_minutes]

    def filter_by_rating(places: List[Dict], min_rating: float) -> List[Dict]:
        """Filter places by minimum rating."""
        return [p for p in places if p["rating"] >= min_rating]

    def filter_by_price(places: List[Dict], max_price: float) -> List[Dict]:
        """Filter places by maximum price."""
        return [p for p in places if p["price"] <= max_price]

    def add_value_score(places: List[Dict]) -> List[Dict]:
        """Add a value score to each place."""
        return [
            {**p, "value_score": round(p["rating"] / math.sqrt(p["walk_time"]), 2)}
            for p in places
        ]

    def sort_by_field(places: List[Dict], field: str, descending: bool = True) -> List[Dict]:
        """Sort places by specified field."""
        return sorted(places, key=lambda p: p.get(field, 0), reverse=descending)

    def take_top(places: List[Dict], n: int) -> List[Dict]:
        """Take top n places."""
        return places[:n]

    def format_place(p: Dict) -> str:
        """Format a place for display."""
        score = f", score={p['value_score']}" if 'value_score' in p else ""
        return f"{p['name']} ({p['category']}): {p['rating']}*, {p['walk_time']}min, ${p['price']}{score}"

    # --- Scenario 1: Best nearby affordable places ---
    print("\n--- Scenario 1: Best Nearby Affordable Places ---")
    print("Criteria: walk_time <= 10min, price <= $15, rating >= 4.0")

    result = places
    result = filter_by_walk_time(result, 10)
    result = filter_by_price(result, 15)
    result = filter_by_rating(result, 4.0)
    result = add_value_score(result)
    result = sort_by_field(result, "value_score")
    result = take_top(result, 3)

    print(f"Found {len(result)} places:")
    for p in result:
        print(f"  {format_place(p)}")

    # --- Scenario 2: Best pizza ---
    print("\n--- Scenario 2: Best Pizza Places ---")
    print("Criteria: category=pizza, sorted by rating")

    result = places
    result = filter_by_category(result, "pizza")
    result = sort_by_field(result, "rating")

    print(f"Found {len(result)} pizza places:")
    for p in result:
        print(f"  {format_place(p)}")

    # --- Scenario 3: Quick options ---
    print("\n--- Scenario 3: Quick Options ---")
    print("Criteria: walk_time <= 5min, any rating")

    result = places
    result = filter_by_walk_time(result, 5)
    result = sort_by_field(result, "walk_time", descending=False)

    print(f"Found {len(result)} quick options:")
    for p in result:
        print(f"  {format_place(p)}")

    # --- Statistics ---
    print("\n--- Statistics for All Places ---")

    ratings = [p["rating"] for p in places]
    times = [p["walk_time"] for p in places]
    prices = [p["price"] for p in places]

    print(f"Total places: {len(places)}")
    print(f"Avg rating: {sum(ratings)/len(ratings):.2f}")
    print(f"Avg walk time: {sum(times)/len(times):.1f} min")
    print(f"Avg price: ${sum(prices)/len(prices):.2f}")
    print(f"Best rated: {max(places, key=lambda p: p['rating'])['name']}")
    print(f"Closest: {min(places, key=lambda p: p['walk_time'])['name']}")
    print(f"Cheapest: {min(places, key=lambda p: p['price'])['name']}")


# =============================================================================
# MAIN - RUN ALL DEMOS
# =============================================================================

def run_all_demos():
    """Run all demonstration functions."""
    demos = [
        ("Pure vs Impure Functions", demo_pure_vs_impure),
        ("Immutability", demo_immutability),
        ("Lambda Functions", demo_lambda_functions),
        ("map() Function", demo_map_function),
        ("filter() Function", demo_filter_function),
        ("reduce() Function", demo_reduce_function),
        ("Sorting", demo_sorting),
        ("Comprehensions vs Functional", demo_comprehensions_vs_functional),
        ("Data Pipelines", demo_data_pipelines),
        ("Place Recommender", demo_place_recommender),
    ]

    print("=" * 60)
    print("WEEK 9: FUNCTIONAL PATTERNS & SORTING")
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
    """Run an interactive menu to select demos."""
    demos = {
        "1": ("Pure vs Impure Functions", demo_pure_vs_impure),
        "2": ("Immutability", demo_immutability),
        "3": ("Lambda Functions", demo_lambda_functions),
        "4": ("map() Function", demo_map_function),
        "5": ("filter() Function", demo_filter_function),
        "6": ("reduce() Function", demo_reduce_function),
        "7": ("Sorting", demo_sorting),
        "8": ("Comprehensions vs Functional", demo_comprehensions_vs_functional),
        "9": ("Data Pipelines", demo_data_pipelines),
        "10": ("Place Recommender", demo_place_recommender),
        "a": ("Run All Demos", run_all_demos),
    }

    while True:
        print("\n" + "=" * 40)
        print("WEEK 9: FUNCTIONAL PATTERNS & SORTING")
        print("=" * 40)
        print("\nSelect a demo to run:")
        for key, (name, _) in demos.items():
            print(f"  {key}. {name}")
        print("  q. Quit")

        choice = input("\nEnter choice: ").strip().lower()

        if choice == 'q':
            print("Goodbye!")
            break
        elif choice in demos:
            name, func = demos[choice]
            print(f"\nRunning: {name}")
            func()
            input("\nPress Enter to continue...")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive_menu()
    else:
        run_all_demos()
