"""
Python Language 101 — Fill-in-the-Code Quizzes
Week 01–06 Essential Understanding

Instructions:
  Each function contains a docstring describing what the function must do.
  Replace every `pass` with the correct Python code.
  Do NOT change function signatures or remove comments.

Topics:
  Q01–Q08   Variables & Types           (Week 01)
  Q09–Q14   Strings                     (Week 01–02)
  Q15–Q20   Tuples & Math Module        (Week 01)
  Q21–Q30   Lists                       (Week 02)
  Q31–Q38   Loops & Iteration           (Week 02)
  Q39–Q46   Dictionaries                (Week 02)
  Q47–Q56   Comprehensions & Lambdas    (Week 02)
  Q57–Q64   Functions (Advanced)        (Week 01–02)
  Q65–Q68   Sorting & Built-ins         (Week 02)
  Q69–Q72   Generators                  (Week 06)
"""

import math


# ---------------------------------------------------------------------------
# WEEK 01 — Variables & Types
# ---------------------------------------------------------------------------

def q01_swap(a, b):
    """Return (b, a) — the two arguments swapped."""
    pass


def q02_integer_ops(a, b):
    """Return a tuple of (quotient, remainder) when a is divided by b.
    Use integer (floor) division and the modulo operator."""
    pass


def q03_power(base, exp):
    """Return base raised to the power of exp."""
    pass


def q04_type_of(value):
    """Return the type of value."""
    pass


def q05_convert_to_int(s):
    """Convert the string s to an integer and return it."""
    pass


def q06_convert_to_float(s):
    """Convert the string s to a float and return it."""
    pass


def q07_is_even(n):
    """Return True if n is even, False otherwise."""
    pass


def q08_absolute_value(n):
    """Return the absolute value of n without using abs()."""
    pass


# ---------------------------------------------------------------------------
# WEEK 01–02 — Strings
# ---------------------------------------------------------------------------

def q09_fstring_format(name, score):
    """Return a formatted string: "<name> scored <score> points"
    Use an f-string."""
    pass


def q10_fstring_precision(value):
    """Return a string showing value formatted to exactly 2 decimal places.
    Use an f-string with format spec."""
    pass


def q11_string_slicing(s):
    """Return a tuple: (first 3 characters, last 3 characters, reversed string)."""
    pass


def q12_string_methods(s):
    """Return a tuple: (s uppercased, s lowercased, s with leading/trailing
    whitespace removed)."""
    pass


def q13_string_split_join(sentence):
    """Split sentence on spaces into a list of words, then join them back
    together separated by hyphens. Return the joined string."""
    pass


def q14_string_contains_count(s, sub):
    """Return a tuple: (True/False whether sub is in s,
    the number of times sub appears in s)."""
    pass


# ---------------------------------------------------------------------------
# WEEK 01 — Tuples & Math Module
# ---------------------------------------------------------------------------

def q15_create_tuple(a, b, c):
    """Return a tuple containing a, b, c (in that order)."""
    pass


def q16_unpack_and_sum(triple):
    """triple is a tuple of three numbers. Unpack it into three variables
    and return their sum."""
    pass


def q17_single_element_tuple(value):
    """Return a tuple containing exactly one element: value."""
    pass


def q18_tuple_index(t, i):
    """Return the element at index i of tuple t."""
    pass


def q19_math_operations(x):
    """Return a tuple: (square root of x, ceiling of x, floor of x).
    Use math.sqrt, math.ceil, math.floor."""
    pass


def q20_degrees_radians_round_trip(degrees):
    """Convert degrees to radians, then back to degrees.
    Return the final degrees value (a float)."""
    pass


# ---------------------------------------------------------------------------
# WEEK 02 — Lists
# ---------------------------------------------------------------------------

def q21_build_list(n):
    """Return a list of integers from 1 to n inclusive."""
    pass


def q22_list_ops(lst):
    """Return a tuple: (minimum value, maximum value, sum of all values)
    of the list. Use built-in functions."""
    pass


def q23_list_slice_middle(lst):
    """lst has at least 5 elements. Return a new list containing
    all elements except the first and last."""
    pass


def q24_list_reverse(lst):
    """Return a new list that is lst in reverse order.
    Do not modify the original list."""
    pass


def q25_list_sort_ascending(lst):
    """Return a new list with the same elements sorted in ascending order.
    Do not modify the original list."""
    pass


def q26_list_remove_first(lst, value):
    """Remove the first occurrence of value from lst and return lst.
    Modify the list in place."""
    pass


def q27_list_insert_at(lst, index, value):
    """Insert value at the given index in lst and return lst.
    Modify the list in place."""
    pass


def q28_list_count_membership(lst, value):
    """Return a tuple: (number of times value appears in lst,
    True if value is in lst else False)."""
    pass


def q29_flatten_two_lists(lst1, lst2):
    """Return a single list that contains all elements of lst1
    followed by all elements of lst2.
    Do not modify either input list."""
    pass


def q30_list_unique(lst):
    """Return a list of unique elements from lst, preserving original order."""
    pass


# ---------------------------------------------------------------------------
# WEEK 02 — Loops & Iteration
# ---------------------------------------------------------------------------

def q31_sum_with_loop(numbers):
    """Use a for loop to compute and return the sum of numbers.
    Do not use the built-in sum()."""
    pass


def q32_countdown(n):
    """Use a while loop to build and return a list counting down
    from n to 1 (inclusive)."""
    pass


def q33_range_step():
    """Return a list of every third integer from 0 up to and including 30.
    Use range() with a step argument."""
    pass


def q34_enumerate_labels(items):
    """Use enumerate() to return a list of strings "1. item", "2. item", ...
    (1-based numbering)."""
    pass


def q35_zip_pairs(keys, values):
    """Use zip() to return a dict mapping each key to its corresponding value."""
    pass


def q36_consecutive_pairs(lst):
    """Return a list of overlapping consecutive pairs (a, b) from lst.
    Example: [1, 2, 3] → [(1, 2), (2, 3)]"""
    pass


def q37_loop_break(numbers, target):
    """Iterate over numbers. Return the index of the first element equal
    to target. Return -1 if target is not found. Use a for loop and break."""
    pass


def q38_loop_continue(numbers):
    """Use a for loop with continue to build and return a list of only
    the positive numbers from numbers."""
    pass


# ---------------------------------------------------------------------------
# WEEK 02 — Dictionaries
# ---------------------------------------------------------------------------

def q39_build_dict(keys, values):
    """Given two equal-length lists, return a dict mapping keys[i] → values[i]."""
    pass


def q40_safe_get(d, key, default):
    """Return the value for key in dict d.
    If key is absent, return default instead."""
    pass


def q41_dict_add_update(d, key, value):
    """Add or update key → value in d. Return d."""
    pass


def q42_dict_remove_key(d, key):
    """Remove key from d if it exists. Return d.
    Do not raise an error if key is absent."""
    pass


def q43_dict_keys_values(d):
    """Return a tuple: (sorted list of keys, list of values for those sorted keys)."""
    pass


def q44_dict_merge(d1, d2):
    """Return a new dict containing all entries from d1 and d2.
    Entries from d2 should overwrite d1 on duplicate keys."""
    pass


def q45_nested_dict_access(d, outer_key, inner_key):
    """Return d[outer_key][inner_key]. Return None if either key is missing
    (use .get() chaining)."""
    pass


def q46_count_occurrences(items):
    """items is a list of values. Return a dict mapping each unique value
    to the number of times it appears in items."""
    pass


# ---------------------------------------------------------------------------
# WEEK 02 — Comprehensions & Lambdas
# ---------------------------------------------------------------------------

def q47_squares_comprehension(n):
    """Return a list of squares [1, 4, 9, ..., n²] using a list comprehension."""
    pass


def q48_even_filter_comprehension(numbers):
    """Return a list of only the even numbers from numbers,
    using a list comprehension with a condition."""
    pass


def q49_transform_comprehension(words):
    """Return a list of each word in words converted to uppercase,
    using a list comprehension."""
    pass


def q50_nested_comprehension(matrix):
    """matrix is a list of lists of numbers.
    Return a flat list of all numbers using a nested list comprehension."""
    pass


def q51_dict_comprehension(lst):
    """lst is a list of strings.
    Return a dict mapping each string to its length, using a dict comprehension."""
    pass


def q52_dict_comprehension_filter(d):
    """d maps strings to numbers.
    Return a new dict containing only entries where the value is positive,
    using a dict comprehension."""
    pass


def q53_map_transform(numbers):
    """Use map() with a lambda to return a list where each number is tripled."""
    pass


def q54_filter_transform(numbers):
    """Use filter() with a lambda to return a list of numbers greater than 10."""
    pass


def q55_lambda_expression():
    """Define and return a lambda that takes two numbers and returns
    the larger of the two."""
    pass


def q56_sorted_with_key(words):
    """Return a new list with the strings in words sorted by their length
    (shortest first), using sorted() with a key argument."""
    pass


# ---------------------------------------------------------------------------
# WEEK 01–02 — Functions (Advanced)
# ---------------------------------------------------------------------------

def q57_default_parameter(value, multiplier=2):
    """Return value multiplied by multiplier.
    multiplier should default to 2."""
    pass


def q58_keyword_call_demo(a, b, c):
    """Return a - b + c."""
    pass


def q59_multiple_return(numbers):
    """Return a tuple (min_val, max_val, mean) of the list.
    mean should be a float."""
    pass


def q60_variadic_sum(*args):
    """Accept any number of positional arguments and return their sum."""
    pass


def q61_variadic_kwargs(**kwargs):
    """Accept any number of keyword arguments.
    Return a list of strings "key=value" for each pair, sorted by key."""
    pass


def q62_inner_function(x):
    """Define an inner function double(n) that returns n * 2.
    Call it with x and return the result."""
    pass


def q63_function_as_argument(numbers, transform):
    """Apply the transform function to every element of numbers and
    return the resulting list. Do not use map()."""
    pass


def q64_recursive_factorial(n):
    """Return n! (factorial) using recursion.
    Base case: factorial(0) = 1."""
    pass


# ---------------------------------------------------------------------------
# WEEK 02 — Sorting & Built-ins
# ---------------------------------------------------------------------------

def q65_sort_by_second(pairs):
    """pairs is a list of (a, b) tuples.
    Return a new list sorted by the second element of each tuple (ascending)."""
    pass


def q66_sort_dicts_by_key(records, key):
    """records is a list of dicts that all contain key.
    Return a new list sorted by records[i][key] in descending order."""
    pass


def q67_min_max_with_key(words):
    """Return a tuple: (shortest word, longest word) from words.
    Use min() and max() with a key argument."""
    pass


def q68_any_all(numbers):
    """Return a tuple: (any(n > 100 for n in numbers),
                        all(n > 0 for n in numbers))"""
    pass


# ---------------------------------------------------------------------------
# WEEK 06 — Generators
# ---------------------------------------------------------------------------

def q69_counting_generator(start, stop):
    """A generator function that yields integers from start up to
    (but not including) stop."""
    pass


def q70_fibonacci_generator(limit):
    """A generator function that yields Fibonacci numbers (0, 1, 1, 2, 3, 5, ...)
    as long as the value is less than or equal to limit."""
    pass


def q71_generator_pipeline(iterable, predicate, transform):
    """A generator function that yields transform(item) for each item in
    iterable where predicate(item) is True."""
    pass


def q72_take(generator, n):
    """Consume at most n values from generator and return them as a list."""
    pass
