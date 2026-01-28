#!/usr/bin/env python3
"""
Week 9 Lab: Functional Patterns & Sorting - Starter Code

Complete the exercises by implementing the functions marked with
'# YOUR CODE HERE'. Run this file to test your implementations.

Usage:
    python week09_starter.py              # Run all tests
    python week09_starter.py --test ex1   # Run Exercise 1 tests only
    python week09_starter.py --test ex2   # Run Exercise 2 tests only
    ... and so on
"""

import math
from functools import reduce
from typing import List, Dict, Any, Optional, Callable
import sys


# =============================================================================
# SAMPLE DATA
# =============================================================================

def get_sample_places() -> List[Dict[str, Any]]:
    """Return sample place data for exercises."""
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
# EXERCISE 1: PURE FUNCTIONS
# =============================================================================

def calculate_efficiency_score(place: Dict[str, Any]) -> float:
    """
    Calculate efficiency score: rating / sqrt(walk_time)

    Args:
        place: Dictionary with 'rating' and 'walk_time' keys

    Returns:
        Efficiency score rounded to 2 decimal places

    Example:
        >>> place = {"name": "Test", "rating": 4.5, "walk_time": 9}
        >>> calculate_efficiency_score(place)
        1.5
    """
    # YOUR CODE HERE
    return round(place["rating"] / math.sqrt(place["walk_time"]), 2)


def add_efficiency_score(place: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a NEW dictionary with efficiency_score added.
    Do NOT modify the original place dictionary.

    Args:
        place: Original place dictionary

    Returns:
        New dictionary with all original fields plus 'efficiency_score'

    Example:
        >>> place = {"name": "Test", "rating": 4.5, "walk_time": 9}
        >>> result = add_efficiency_score(place)
        >>> result['efficiency_score']
        1.5
        >>> 'efficiency_score' in place  # Original unchanged
        False
    """
    # YOUR CODE HERE
    return {**place, "efficiency_score": calculate_efficiency_score(place)}


# =============================================================================
# EXERCISE 2: LAMBDA FUNCTIONS
# =============================================================================

# Task 2.1: Convert these to lambda expressions

# Get rating from a place
get_rating = lambda place: place["rating"]

# Check if place is nearby (walk_time <= max_time)
is_nearby = lambda place, max_time=15: place["walk_time"] <= max_time

# Format place name with rating
format_place_name = lambda place: f"{place['name']} ({place['rating']}*)"


# Task 2.2: Lambdas with conditionals

# Return "Nearby" if walk_time <= 10, else "Far"
distance_category = lambda place: "Nearby" if place["walk_time"] <= 10 else "Far"

# Return rating if >= 4.0, else 0
rating_or_zero = lambda place: place["rating"] if place["rating"] >= 4.0 else 0

# Return the better place (higher rating)
better_place = lambda p1, p2: p1 if p1["rating"] >= p2["rating"] else p2


# =============================================================================
# EXERCISE 3: MAP AND FILTER
# =============================================================================

def extract_names(places: List[Dict]) -> List[str]:
    """
    Extract all place names using map().

    Args:
        places: List of place dictionaries

    Returns:
        List of place names
    """
    # YOUR CODE HERE - use map()
    return list(map(lambda p: p["name"], places))


def extract_ratings(places: List[Dict]) -> List[float]:
    """
    Extract all ratings using map().

    Args:
        places: List of place dictionaries

    Returns:
        List of ratings
    """
    # YOUR CODE HERE - use map()
    return list(map(lambda p: p["rating"], places))


def filter_nearby(places: List[Dict], max_time: int = 10) -> List[Dict]:
    """
    Filter places within max_time minutes walk using filter().

    Args:
        places: List of place dictionaries
        max_time: Maximum walk time in minutes

    Returns:
        List of nearby places
    """
    # YOUR CODE HERE - use filter()
    return list(filter(lambda p: p["walk_time"] <= max_time, places))


def filter_top_rated(places: List[Dict], min_rating: float = 4.5) -> List[Dict]:
    """
    Filter places with rating >= min_rating using filter().

    Args:
        places: List of place dictionaries
        min_rating: Minimum rating threshold

    Returns:
        List of top-rated places
    """
    # YOUR CODE HERE - use filter()
    return list(filter(lambda p: p["rating"] >= min_rating, places))


def filter_by_category(places: List[Dict], category: str) -> List[Dict]:
    """
    Filter places by category using filter().

    Args:
        places: List of place dictionaries
        category: Category to filter by

    Returns:
        List of places in the specified category
    """
    # YOUR CODE HERE - use filter()
    return list(filter(lambda p: p["category"] == category, places))


def get_nearby_names(places: List[Dict], max_time: int = 10) -> List[str]:
    """
    Get names of places within max_time using map() and filter().

    Args:
        places: List of place dictionaries
        max_time: Maximum walk time

    Returns:
        List of names of nearby places
    """
    # YOUR CODE HERE - use map() and filter()
    return list(map(lambda p: p["name"], filter(lambda p: p["walk_time"] <= max_time, places)))


# =============================================================================
# EXERCISE 4: REDUCE
# =============================================================================

def sum_with_reduce(numbers: List[float]) -> float:
    """
    Calculate sum using reduce().

    Args:
        numbers: List of numbers

    Returns:
        Sum of all numbers
    """
    # YOUR CODE HERE - use reduce()
    return reduce(lambda acc, x: acc + x, numbers, 0)


def product_with_reduce(numbers: List[float]) -> float:
    """
    Calculate product using reduce().

    Args:
        numbers: List of numbers

    Returns:
        Product of all numbers
    """
    # YOUR CODE HERE - use reduce()
    return reduce(lambda acc, x: acc * x, numbers, 1)


def find_max_with_reduce(numbers: List[float]) -> float:
    """
    Find maximum using reduce().

    Args:
        numbers: List of numbers

    Returns:
        Maximum value
    """
    # YOUR CODE HERE - use reduce()
    return reduce(lambda acc, x: x if x > acc else acc, numbers)


def total_walk_time(places: List[Dict]) -> int:
    """
    Calculate total walk time using reduce().

    Args:
        places: List of place dictionaries

    Returns:
        Sum of all walk times
    """
    # YOUR CODE HERE - use reduce()
    return reduce(lambda acc, p: acc + p["walk_time"], places, 0)


def find_best_place(places: List[Dict]) -> Dict:
    """
    Find place with highest rating using reduce().

    Args:
        places: List of place dictionaries

    Returns:
        Place dictionary with highest rating
    """
    # YOUR CODE HERE - use reduce()
    return reduce(lambda acc, p: p if p["rating"] > acc["rating"] else acc, places)


def group_by_category(places: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Group places by category using reduce().

    Args:
        places: List of place dictionaries

    Returns:
        Dictionary mapping category to list of places
    """
    # YOUR CODE HERE - use reduce()
    def reducer(acc, place):
        category = place["category"]
        if category not in acc:
            acc[category] = []
        acc[category].append(place)
        return acc

    return reduce(reducer, places, {})


# =============================================================================
# EXERCISE 5: SORTING
# =============================================================================

def sort_by_rating_desc(places: List[Dict]) -> List[Dict]:
    """
    Sort places by rating (highest first).

    Args:
        places: List of place dictionaries

    Returns:
        Sorted list (new list, original unchanged)
    """
    # YOUR CODE HERE
    return sorted(places, key=lambda p: p["rating"], reverse=True)


def sort_by_walk_time_asc(places: List[Dict]) -> List[Dict]:
    """
    Sort places by walk time (shortest first).

    Args:
        places: List of place dictionaries

    Returns:
        Sorted list
    """
    # YOUR CODE HERE
    return sorted(places, key=lambda p: p["walk_time"])


def sort_by_name(places: List[Dict]) -> List[Dict]:
    """
    Sort places by name alphabetically.

    Args:
        places: List of place dictionaries

    Returns:
        Sorted list
    """
    # YOUR CODE HERE
    return sorted(places, key=lambda p: p["name"])


def sort_by_rating_then_time(places: List[Dict]) -> List[Dict]:
    """
    Sort by rating (desc), then by walk_time (asc) for ties.

    Args:
        places: List of place dictionaries

    Returns:
        Sorted list
    """
    # YOUR CODE HERE - hint: use tuple (-rating, walk_time) as key
    return sorted(places, key=lambda p: (-p["rating"], p["walk_time"]))


def sort_by_efficiency(places: List[Dict]) -> List[Dict]:
    """
    Sort by efficiency score (rating / sqrt(walk_time)), highest first.

    Args:
        places: List of place dictionaries

    Returns:
        Sorted list
    """
    # YOUR CODE HERE
    return sorted(places, key=lambda p: p["rating"] / math.sqrt(p["walk_time"]), reverse=True)


# =============================================================================
# EXERCISE 6: DATA PIPELINES
# =============================================================================

def get_top_nearby_places(
    places: List[Dict],
    max_walk_time: int = 12,
    min_rating: float = 4.0,
    top_n: int = 3
) -> List[Dict]:
    """
    Pipeline: Filter by time -> Filter by rating -> Sort by rating -> Take top N

    Args:
        places: List of place dictionaries
        max_walk_time: Maximum walk time filter
        min_rating: Minimum rating filter
        top_n: Number of results to return

    Returns:
        Top N nearby, well-rated places sorted by rating
    """
    # YOUR CODE HERE
    return sorted(
        [p for p in places if p["walk_time"] <= max_walk_time and p["rating"] >= min_rating],
        key=lambda p: p["rating"],
        reverse=True
    )[:top_n]


def get_best_in_category(
    places: List[Dict],
    category: str,
    top_n: int = 3
) -> List[Dict]:
    """
    Get the most efficient places in a category.

    Pipeline:
    1. Filter by category
    2. Add efficiency score
    3. Sort by efficiency score (descending)
    4. Take top N

    Args:
        places: List of place dictionaries
        category: Category to filter by
        top_n: Number of results

    Returns:
        Top N places in category with efficiency scores
    """
    # YOUR CODE HERE
    filtered = [p for p in places if p["category"] == category]
    scored = [add_efficiency_score(p) for p in filtered]
    sorted_places = sorted(scored, key=lambda p: p["efficiency_score"], reverse=True)
    return sorted_places[:top_n]


def recommend_places(
    places: List[Dict],
    category: Optional[str] = None,
    max_walk_time: int = 15,
    min_rating: float = 0.0,
    max_price: float = float('inf'),
    sort_by: str = "efficiency",
    top_n: int = 5
) -> List[Dict]:
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

    Args:
        places: List of place dictionaries
        category: Optional category filter
        max_walk_time: Maximum walk time in minutes
        min_rating: Minimum rating
        max_price: Maximum price
        sort_by: Field to sort by ("efficiency", "rating", "time", "price")
        top_n: Number of results

    Returns:
        List of recommended places with efficiency scores
    """
    # YOUR CODE HERE
    result = places

    # Filter by category
    if category is not None:
        result = [p for p in result if p["category"] == category]

    # Filter by walk time
    result = [p for p in result if p["walk_time"] <= max_walk_time]

    # Filter by rating
    result = [p for p in result if p["rating"] >= min_rating]

    # Filter by price
    result = [p for p in result if p["price"] <= max_price]

    # Add efficiency score
    result = [add_efficiency_score(p) for p in result]

    # Sort
    sort_keys = {
        "efficiency": lambda p: p["efficiency_score"],
        "rating": lambda p: p["rating"],
        "time": lambda p: p["walk_time"],
        "price": lambda p: p["price"],
    }
    reverse = sort_by not in ["time", "price"]  # Descending for efficiency/rating
    result = sorted(result, key=sort_keys.get(sort_by, sort_keys["efficiency"]), reverse=reverse)

    # Take top N
    return result[:top_n]


# =============================================================================
# EXERCISE 7: LIST COMPREHENSIONS VS FUNCTIONAL
# =============================================================================

def ratings_with_comprehension(places: List[Dict]) -> List[float]:
    """Extract ratings using list comprehension."""
    # YOUR CODE HERE
    return [p["rating"] for p in places]


def nearby_with_comprehension(places: List[Dict], max_time: int = 10) -> List[Dict]:
    """Filter nearby places using list comprehension."""
    # YOUR CODE HERE
    return [p for p in places if p["walk_time"] <= max_time]


def top_rated_names_with_comprehension(places: List[Dict], min_rating: float = 4.5) -> List[str]:
    """Get names of top-rated places using list comprehension."""
    # YOUR CODE HERE
    return [p["name"] for p in places if p["rating"] >= min_rating]


# =============================================================================
# BONUS: FUNCTIONAL STATISTICS
# =============================================================================

def functional_statistics(places: List[Dict]) -> Dict[str, Any]:
    """
    Calculate statistics using only functional programming.
    No for loops allowed!

    Args:
        places: List of place dictionaries

    Returns:
        Dictionary with count, sum, min, max, average of ratings
    """
    if not places:
        return {"count": 0, "sum": 0, "min": None, "max": None, "average": None}

    ratings = list(map(lambda p: p["rating"], places))

    return {
        "count": len(ratings),
        "sum": reduce(lambda acc, x: acc + x, ratings, 0),
        "min": reduce(lambda acc, x: x if x < acc else acc, ratings),
        "max": reduce(lambda acc, x: x if x > acc else acc, ratings),
        "average": reduce(lambda acc, x: acc + x, ratings, 0) / len(ratings),
    }


# =============================================================================
# TESTS
# =============================================================================

def test_exercise1():
    """Test Exercise 1: Pure Functions"""
    print("\n" + "=" * 50)
    print("Testing Exercise 1: Pure Functions")
    print("=" * 50)

    # Test calculate_efficiency_score
    place = {"name": "Test", "rating": 4.5, "walk_time": 9}
    score = calculate_efficiency_score(place)
    assert score == 1.5, f"Expected 1.5, got {score}"
    print("  [PASS] calculate_efficiency_score")

    # Test add_efficiency_score (purity)
    original = {"name": "Test", "rating": 4.0, "walk_time": 4}
    original_copy = dict(original)
    result = add_efficiency_score(original)

    assert original == original_copy, "Original was modified!"
    assert "efficiency_score" in result, "Result missing efficiency_score"
    assert result["efficiency_score"] == 2.0, f"Wrong score: {result['efficiency_score']}"
    print("  [PASS] add_efficiency_score (purity verified)")

    print("\nExercise 1: All tests passed!")


def test_exercise2():
    """Test Exercise 2: Lambda Functions"""
    print("\n" + "=" * 50)
    print("Testing Exercise 2: Lambda Functions")
    print("=" * 50)

    place = {"name": "Test Place", "rating": 4.5, "walk_time": 8}

    # Test get_rating
    assert get_rating(place) == 4.5
    print("  [PASS] get_rating")

    # Test is_nearby
    assert is_nearby(place) == True  # 8 <= 15
    assert is_nearby(place, 5) == False  # 8 > 5
    print("  [PASS] is_nearby")

    # Test format_place_name
    assert format_place_name(place) == "Test Place (4.5*)"
    print("  [PASS] format_place_name")

    # Test distance_category
    assert distance_category({"walk_time": 5}) == "Nearby"
    assert distance_category({"walk_time": 15}) == "Far"
    print("  [PASS] distance_category")

    # Test rating_or_zero
    assert rating_or_zero({"rating": 4.5}) == 4.5
    assert rating_or_zero({"rating": 3.5}) == 0
    print("  [PASS] rating_or_zero")

    # Test better_place
    p1 = {"name": "A", "rating": 4.5}
    p2 = {"name": "B", "rating": 4.2}
    assert better_place(p1, p2)["name"] == "A"
    print("  [PASS] better_place")

    print("\nExercise 2: All tests passed!")


def test_exercise3():
    """Test Exercise 3: map() and filter()"""
    print("\n" + "=" * 50)
    print("Testing Exercise 3: map() and filter()")
    print("=" * 50)

    places = get_sample_places()

    # Test extract_names
    names = extract_names(places)
    assert len(names) == 8
    assert "Pizza Palace" in names
    print("  [PASS] extract_names")

    # Test extract_ratings
    ratings = extract_ratings(places)
    assert len(ratings) == 8
    assert 4.5 in ratings
    print("  [PASS] extract_ratings")

    # Test filter_nearby
    nearby = filter_nearby(places, 10)
    assert all(p["walk_time"] <= 10 for p in nearby)
    print("  [PASS] filter_nearby")

    # Test filter_top_rated
    top = filter_top_rated(places, 4.5)
    assert all(p["rating"] >= 4.5 for p in top)
    print("  [PASS] filter_top_rated")

    # Test filter_by_category
    pizza = filter_by_category(places, "pizza")
    assert len(pizza) == 2
    assert all(p["category"] == "pizza" for p in pizza)
    print("  [PASS] filter_by_category")

    # Test get_nearby_names
    nearby_names = get_nearby_names(places, 10)
    assert isinstance(nearby_names, list)
    assert all(isinstance(n, str) for n in nearby_names)
    print("  [PASS] get_nearby_names")

    print("\nExercise 3: All tests passed!")


def test_exercise4():
    """Test Exercise 4: reduce()"""
    print("\n" + "=" * 50)
    print("Testing Exercise 4: reduce()")
    print("=" * 50)

    numbers = [1, 2, 3, 4, 5]

    # Test sum_with_reduce
    assert sum_with_reduce(numbers) == 15
    print("  [PASS] sum_with_reduce")

    # Test product_with_reduce
    assert product_with_reduce(numbers) == 120
    print("  [PASS] product_with_reduce")

    # Test find_max_with_reduce
    assert find_max_with_reduce(numbers) == 5
    print("  [PASS] find_max_with_reduce")

    places = get_sample_places()

    # Test total_walk_time
    total = total_walk_time(places)
    assert total == sum(p["walk_time"] for p in places)
    print("  [PASS] total_walk_time")

    # Test find_best_place
    best = find_best_place(places)
    assert best["name"] == "Sushi Supreme"  # 4.8 rating
    print("  [PASS] find_best_place")

    # Test group_by_category
    grouped = group_by_category(places)
    assert "pizza" in grouped
    assert len(grouped["pizza"]) == 2
    print("  [PASS] group_by_category")

    print("\nExercise 4: All tests passed!")


def test_exercise5():
    """Test Exercise 5: Sorting"""
    print("\n" + "=" * 50)
    print("Testing Exercise 5: Sorting")
    print("=" * 50)

    places = get_sample_places()

    # Test sort_by_rating_desc
    sorted_rating = sort_by_rating_desc(places)
    assert sorted_rating[0]["name"] == "Sushi Supreme"  # 4.8
    print("  [PASS] sort_by_rating_desc")

    # Test sort_by_walk_time_asc
    sorted_time = sort_by_walk_time_asc(places)
    assert sorted_time[0]["name"] == "Salad Station"  # 3 min
    print("  [PASS] sort_by_walk_time_asc")

    # Test sort_by_name
    sorted_name = sort_by_name(places)
    assert sorted_name[0]["name"] == "Burger Barn"  # B comes first
    print("  [PASS] sort_by_name")

    # Test sort_by_rating_then_time
    test_places = [
        {"name": "A", "rating": 4.5, "walk_time": 10},
        {"name": "B", "rating": 4.5, "walk_time": 5},
        {"name": "C", "rating": 4.2, "walk_time": 3},
    ]
    sorted_multi = sort_by_rating_then_time(test_places)
    assert sorted_multi[0]["name"] == "B"  # 4.5, 5min
    assert sorted_multi[1]["name"] == "A"  # 4.5, 10min
    assert sorted_multi[2]["name"] == "C"  # 4.2, 3min
    print("  [PASS] sort_by_rating_then_time")

    # Test sort_by_efficiency
    sorted_eff = sort_by_efficiency(places)
    # Salad Station: 4.0 / sqrt(3) = 2.31 (highest efficiency)
    assert sorted_eff[0]["name"] == "Salad Station"
    print("  [PASS] sort_by_efficiency")

    print("\nExercise 5: All tests passed!")


def test_exercise6():
    """Test Exercise 6: Data Pipelines"""
    print("\n" + "=" * 50)
    print("Testing Exercise 6: Data Pipelines")
    print("=" * 50)

    places = get_sample_places()

    # Test get_top_nearby_places
    top_nearby = get_top_nearby_places(places, max_walk_time=12, min_rating=4.0, top_n=3)
    assert len(top_nearby) <= 3
    assert all(p["walk_time"] <= 12 for p in top_nearby)
    assert all(p["rating"] >= 4.0 for p in top_nearby)
    print("  [PASS] get_top_nearby_places")

    # Test get_best_in_category
    best_pizza = get_best_in_category(places, "pizza", top_n=2)
    assert len(best_pizza) <= 2
    assert all(p["category"] == "pizza" for p in best_pizza)
    assert all("efficiency_score" in p for p in best_pizza)
    print("  [PASS] get_best_in_category")

    # Test recommend_places
    recommendations = recommend_places(
        places,
        max_walk_time=10,
        min_rating=4.0,
        top_n=3
    )
    assert len(recommendations) <= 3
    assert all(p["walk_time"] <= 10 for p in recommendations)
    assert all(p["rating"] >= 4.0 for p in recommendations)
    assert all("efficiency_score" in p for p in recommendations)
    print("  [PASS] recommend_places")

    print("\nExercise 6: All tests passed!")


def test_exercise7():
    """Test Exercise 7: List Comprehensions"""
    print("\n" + "=" * 50)
    print("Testing Exercise 7: List Comprehensions")
    print("=" * 50)

    places = get_sample_places()

    # Test ratings_with_comprehension
    ratings = ratings_with_comprehension(places)
    assert ratings == extract_ratings(places)
    print("  [PASS] ratings_with_comprehension")

    # Test nearby_with_comprehension
    nearby = nearby_with_comprehension(places, 10)
    assert len(nearby) == len(filter_nearby(places, 10))
    print("  [PASS] nearby_with_comprehension")

    # Test top_rated_names_with_comprehension
    names = top_rated_names_with_comprehension(places, 4.5)
    expected = [p["name"] for p in places if p["rating"] >= 4.5]
    assert names == expected
    print("  [PASS] top_rated_names_with_comprehension")

    print("\nExercise 7: All tests passed!")


def test_bonus():
    """Test Bonus: Functional Statistics"""
    print("\n" + "=" * 50)
    print("Testing Bonus: Functional Statistics")
    print("=" * 50)

    places = get_sample_places()
    stats = functional_statistics(places)

    assert stats["count"] == 8
    assert stats["min"] == 3.9
    assert stats["max"] == 4.8
    assert abs(stats["average"] - 4.3125) < 0.001
    print("  [PASS] functional_statistics")

    print("\nBonus: All tests passed!")


def run_all_tests():
    """Run all test functions."""
    test_functions = [
        ("Exercise 1", test_exercise1),
        ("Exercise 2", test_exercise2),
        ("Exercise 3", test_exercise3),
        ("Exercise 4", test_exercise4),
        ("Exercise 5", test_exercise5),
        ("Exercise 6", test_exercise6),
        ("Exercise 7", test_exercise7),
        ("Bonus", test_bonus),
    ]

    print("\n" + "=" * 60)
    print("WEEK 9 LAB: FUNCTIONAL PATTERNS & SORTING")
    print("Running All Tests")
    print("=" * 60)

    passed = 0
    failed = 0

    for name, test_func in test_functions:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n[FAILED] {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"\n[ERROR] {name}: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            if len(sys.argv) > 2:
                test_name = sys.argv[2].lower()
                test_map = {
                    "ex1": test_exercise1,
                    "ex2": test_exercise2,
                    "ex3": test_exercise3,
                    "ex4": test_exercise4,
                    "ex5": test_exercise5,
                    "ex6": test_exercise6,
                    "ex7": test_exercise7,
                    "bonus": test_bonus,
                }
                if test_name in test_map:
                    test_map[test_name]()
                else:
                    print(f"Unknown test: {test_name}")
                    print(f"Available: {', '.join(test_map.keys())}")
            else:
                run_all_tests()
        else:
            print("Usage:")
            print("  python week09_starter.py           # Run all tests")
            print("  python week09_starter.py --test ex1  # Run specific test")
    else:
        run_all_tests()


if __name__ == "__main__":
    main()
