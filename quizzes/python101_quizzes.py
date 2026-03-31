"""
Python Language 101 — Fill-in-the-Code Quizzes
Week 01–06 Essential Understanding

Instructions:
  Each function has a comment describing the code requirement.
  Replace every `pass` with the correct Python code.
  Do NOT change function signatures or remove comments.

Topics:
  Q01–Q08   Variables & Data Types       (Week 01)
  Q09–Q16   Functions & Math Module      (Week 01)
  Q17–Q24   Lists                        (Week 02)
  Q25–Q32   Loops & Iteration            (Week 02)
  Q33–Q40   Dictionaries                 (Week 02)
  Q41–Q48   Comprehensions & Lambda      (Week 02)
  Q49–Q56   JSON & File I/O              (Week 03)
  Q57–Q62   HTTP Requests                (Week 04)
  Q63–Q68   Error Handling & APIs        (Week 05)
  Q69–Q72   Generators & Lazy Loading    (Week 06)
"""

import math
import json
import os

# ---------------------------------------------------------------------------
# WEEK 01 — Variables & Data Types
# ---------------------------------------------------------------------------

def q01_assign_variables():
    # Assign the integer 2024 to a variable named `year`
    # Assign the float 25.0330 to a variable named `latitude`
    # Assign the string "Taipei" to a variable named `city`
    # Return a tuple: (year, latitude, city)
    pass


def q02_integer_arithmetic(a, b):
    # Return a tuple of five results:
    #   (a + b,  a - b,  a * b,  a // b,  a % b)
    # Use integer division (//) and modulo (%) — not regular division
    pass


def q03_float_division(a, b):
    # Return the result of TRUE division of a by b (yields a float)
    # e.g. q03_float_division(10, 3) → 3.3333...
    pass


def q04_exponentiation(base, exp):
    # Return base raised to the power of exp using the ** operator
    pass


def q05_create_coordinate_tuple(lat, lon):
    # Create and return a tuple (lat, lon) representing a coordinate
    pass


def q06_unpack_coordinate(coord):
    # coord is a (latitude, longitude) tuple
    # Unpack it into two variables: lat and lon
    # Return (lat, lon)
    pass


def q07_type_check(value):
    # Return the type of `value` using the built-in type() function
    pass


def q08_string_formatting(name, lat, lon):
    # Return a formatted string using an f-string:
    #   "{name} is at ({lat:.4f}, {lon:.4f})"
    # Example: "Taipei 101 is at (25.0330, 121.5654)"
    pass


# ---------------------------------------------------------------------------
# WEEK 01 — Functions & Math Module
# ---------------------------------------------------------------------------

def q09_import_and_use_sqrt(x):
    # Import the math module (already imported at the top)
    # Return the square root of x using math.sqrt()
    pass


def q10_degrees_to_radians(degrees):
    # Convert degrees to radians using math.radians()
    # Return the result
    pass


def q11_radians_to_degrees(radians):
    # Convert radians to degrees using math.degrees()
    # Return the result
    pass


def q12_trig_functions(angle_degrees):
    # Convert angle_degrees to radians first
    # Return a tuple: (sin, cos) of the angle
    pass


def q13_default_parameter(name, greeting="Hello"):
    # Return the string f"{greeting}, {name}!"
    # The greeting parameter should default to "Hello"
    pass


def q14_return_multiple_values(coord1, coord2):
    # coord1 and coord2 are (lat, lon) tuples
    # Return a tuple: (lat1, lon1, lat2, lon2)
    # where lat1/lon1 come from coord1 and lat2/lon2 from coord2
    pass


def q15_km_to_miles(km):
    # Convert kilometers to miles
    # 1 km = 0.621371 miles
    # Return the result
    pass


def q16_haversine(coord1, coord2):
    # Implement the Haversine formula to calculate great-circle distance in km
    # Earth radius R = 6371 km
    # Steps:
    #   1. Extract lat1, lon1 from coord1 and lat2, lon2 from coord2
    #   2. Convert all four values to radians with math.radians()
    #   3. dlat = lat2_rad - lat1_rad
    #      dlon = lon2_rad - lon1_rad
    #   4. a = sin(dlat/2)**2 + cos(lat1_rad)*cos(lat2_rad)*sin(dlon/2)**2
    #   5. return R * 2 * math.asin(math.sqrt(a))
    pass


# ---------------------------------------------------------------------------
# WEEK 02 — Lists
# ---------------------------------------------------------------------------

def q17_create_and_append():
    # Create an empty list named `cities`
    # Append "Taipei", then "Tokyo", then "Seoul" to it (in that order)
    # Return cities
    pass


def q18_list_indexing(lst):
    # Return a tuple: (first element, last element)
    # Use positive index for first and negative index for last
    pass


def q19_list_slicing(lst):
    # lst has at least 5 elements
    # Return a tuple:
    #   (first 3 elements,  last 2 elements,  reversed list)
    pass


def q20_list_methods(lst, value):
    # Remove the first occurrence of `value` from lst (use .remove())
    # Append the integer 99 to the end
    # Return the modified lst
    pass


def q21_list_insert_and_pop(lst):
    # Insert the string "START" at index 0
    # Pop (remove and discard) the last element
    # Return the modified lst
    pass


def q22_list_length_and_sum(numbers):
    # Return a tuple: (len(numbers), sum(numbers))
    pass


def q23_list_concatenation(list1, list2):
    # Return a new list that is list1 followed by list2
    # Use the + operator (do not modify either input list)
    pass


def q24_list_extend(list1, list2):
    # Extend list1 IN PLACE with the elements of list2 (use .extend())
    # Return list1
    pass


# ---------------------------------------------------------------------------
# WEEK 02 — Loops & Iteration
# ---------------------------------------------------------------------------

def q25_for_loop_sum(numbers):
    # Use a for loop to compute and return the sum of all numbers in the list
    # Do NOT use the built-in sum()
    pass


def q26_range_loop():
    # Use range() to build and return a list of even numbers from 0 to 18 (inclusive)
    # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    pass


def q27_enumerate_loop(items):
    # Use enumerate() to build and return a list of strings:
    #   ["1. item0", "2. item1", ...]  (1-based numbering)
    pass


def q28_zip_loop(names, coords):
    # names is a list of strings; coords is a list of (lat, lon) tuples
    # Use zip() to return a list of strings:
    #   ["{name}: ({lat}, {lon})", ...]
    pass


def q29_consecutive_pairs(lst):
    # Return a list of consecutive (a, b) pairs from lst
    # e.g. [1,2,3,4] → [(1,2), (2,3), (3,4)]
    # Use zip() with slicing: zip(lst[:-1], lst[1:])
    pass


def q30_while_loop_countdown(n):
    # Use a while loop to build and return a list counting down from n to 1
    # e.g. n=5 → [5, 4, 3, 2, 1]
    pass


def q31_map_function(numbers):
    # Use map() with a lambda to return a list where every element is squared
    # e.g. [1, 2, 3] → [1, 4, 9]
    pass


def q32_filter_function(numbers):
    # Use filter() with a lambda to return a list of only the EVEN numbers
    pass


# ---------------------------------------------------------------------------
# WEEK 02 — Dictionaries
# ---------------------------------------------------------------------------

def q33_create_place_dict(name, lat, lon, rating):
    # Create and return a dictionary with keys:
    #   "name", "coords" (tuple of lat,lon), "rating"
    pass


def q34_dict_access(place):
    # place is a dict with keys "name", "coords", "rating"
    # Return the value for "name" using square-bracket notation
    pass


def q35_dict_safe_access(place, key, default="N/A"):
    # Return the value for `key` from `place`
    # If the key does not exist, return `default` (use .get())
    pass


def q36_dict_update(place, new_category):
    # Add or update a key "category" in `place` with the value new_category
    # Return the modified place dict
    pass


def q37_dict_keys_values(place):
    # Return a tuple: (list of keys, list of values)
    # Convert dict_keys / dict_values to plain lists
    pass


def q38_dict_iteration(places):
    # places is a list of dicts, each with "name" and "rating"
    # Use a for loop and .items() on each dict to build and return
    # a list of strings:  ["{name}: {rating}", ...]
    pass


def q39_nested_dict_access(place):
    # place = {"name": "...", "coords": {"lat": ..., "lon": ...}, ...}
    # Return a tuple: (lat, lon) extracted from place["coords"]
    pass


def q40_dict_pop(place, key):
    # Remove `key` from `place` using .pop()
    # If the key does not exist, return the string "missing" as the default
    # Return the removed value (or "missing")
    pass


# ---------------------------------------------------------------------------
# WEEK 02 — Comprehensions & Lambda
# ---------------------------------------------------------------------------

def q41_list_comprehension_squares(n):
    # Use a list comprehension to return a list of squares: [1, 4, 9, ..., n²]
    # for i in range(1, n+1)
    pass


def q42_list_comprehension_filter(numbers):
    # Use a list comprehension to return only the numbers greater than 10
    pass


def q43_list_comprehension_transform(coords):
    # coords is a list of (lat, lon) tuples
    # Return a list of only the latitudes (first element of each tuple)
    pass


def q44_dict_comprehension(names, ratings):
    # names is a list of strings; ratings is a list of floats
    # Use a dict comprehension with zip() to return {name: rating, ...}
    pass


def q45_dict_comprehension_filter(place_list):
    # place_list is a list of dicts, each with "name" and "rating"
    # Return a dict {name: rating} for places with rating >= 4.5 only
    pass


def q46_lambda_sort(places):
    # places is a list of dicts, each with "name" and "rating"
    # Use sorted() with a lambda key to return the list sorted by
    # "rating" in DESCENDING order (highest first)
    pass


def q47_lambda_map(strings):
    # Use map() with a lambda to return a list of all strings converted to UPPERCASE
    pass


def q48_lambda_filter(place_list):
    # place_list is a list of dicts, each with "category"
    # Use filter() with a lambda to return only places where category == "restaurant"
    pass


# ---------------------------------------------------------------------------
# WEEK 03 — JSON & File I/O
# ---------------------------------------------------------------------------

def q49_json_dumps(data):
    # Convert the Python dict `data` to a JSON-formatted string
    # Use indent=2 for pretty-printing
    # Return the string
    pass


def q50_json_loads(json_string):
    # Parse the JSON string `json_string` into a Python object
    # Return the result
    pass


def q51_write_text_file(filepath, content):
    # Open `filepath` for writing (mode "w") with UTF-8 encoding
    # Write `content` (a string) to the file
    # Use a with statement
    pass


def q52_read_text_file(filepath):
    # Open `filepath` for reading (mode "r") with UTF-8 encoding
    # Read and return the entire file contents as a string
    # Use a with statement
    pass


def q53_save_json_file(filepath, data):
    # Save `data` (a Python object) to `filepath` as JSON
    # Use json.dump() with indent=2 inside a with/open block
    pass


def q54_load_json_file(filepath):
    # Open `filepath` for reading and parse it as JSON using json.load()
    # Return the resulting Python object
    pass


def q55_json_type_conversion():
    # JSON does not support Python tuples or sets.
    # Create a dict `original` with key "coords" = (25.03, 121.57)  (a tuple)
    # Convert it to JSON string (json.dumps), then parse it back (json.loads)
    # Return the TYPE of result["coords"]  — show what JSON does to tuples
    pass


def q56_file_exists_check(filepath):
    # Return True if the file at `filepath` exists, False otherwise
    # Use os.path.exists()
    pass


# ---------------------------------------------------------------------------
# WEEK 04 — HTTP Requests
# ---------------------------------------------------------------------------

def q57_make_get_request(url, params, headers):
    # Import requests is assumed available
    # Make a GET request to `url` with `params` and `headers`
    # Set timeout=10
    # Return the response object
    import requests
    pass


def q58_check_status_code(response):
    # Return True if the response status code is 200, False otherwise
    pass


def q59_parse_response_json(response):
    # Parse and return the JSON body of the response
    # Use response.json()
    pass


def q60_build_nominatim_params(query):
    # Build and return a dict of query parameters for a Nominatim /search request:
    #   "q"      → query
    #   "format" → "json"
    #   "limit"  → 5
    pass


def q61_build_user_agent_header(app_name, email):
    # Build and return a dict containing the User-Agent header:
    #   {"User-Agent": "{app_name}/1.0 ({email})"}
    pass


def q62_extract_first_result_coords(results):
    # results is a list of dicts returned by the Nominatim API
    # Each dict has "lat" and "lon" as STRING values
    # Return a tuple: (float(lat), float(lon)) from the FIRST result
    # Return None if results is empty
    pass


# ---------------------------------------------------------------------------
# WEEK 05 — Error Handling & Defensive APIs
# ---------------------------------------------------------------------------

def q63_try_except_basic(risky_function, *args):
    # Call risky_function(*args) inside a try block
    # If ANY exception is raised, return None
    # Otherwise return the result
    pass


def q64_try_except_specific(json_string):
    # Try to parse `json_string` with json.loads()
    # Catch json.JSONDecodeError specifically
    # If parsing fails, return the empty dict {}
    # Otherwise return the parsed object
    pass


def q65_try_except_finally(filepath):
    # Open `filepath`, read its contents, and return them
    # Use try/finally to ensure the file handle `f` is always closed
    # (Manually open with open(), not a with statement)
    pass


def q66_safe_dict_get_nested(data, *keys):
    # Safely retrieve a nested value from `data` using the sequence of `keys`
    # e.g. safe_get(d, "a", "b", "c") → d["a"]["b"]["c"]
    # If any key is missing (KeyError) or the value is not subscriptable
    # (TypeError), return None
    pass


def q67_validate_coordinate(lat, lon):
    # Return True if the coordinate is valid:
    #   -90 <= lat <= 90  AND  -180 <= lon <= 180
    # Return False otherwise
    pass


def q68_retry_request(url, headers, max_retries=3):
    # Make a GET request to `url` with `headers`
    # If the status code is NOT 200, retry up to max_retries times
    # Return the response if successful (status 200)
    # Return None if all retries are exhausted
    import requests
    import time
    pass


# ---------------------------------------------------------------------------
# WEEK 06 — Generators & Lazy Loading
# ---------------------------------------------------------------------------

def q69_simple_generator(n):
    # Write a generator function that YIELDS integers from 0 up to (but not including) n
    # Use the `yield` keyword inside a for/range loop
    pass


def q70_generator_squares(n):
    # Write a generator that yields the squares of integers 1..n
    # e.g. n=4 → yields 1, 4, 9, 16
    pass


def q71_paginated_results(fetch_page, total_pages):
    # `fetch_page(page_number)` is a function that returns a list of items
    #    for the given page number (1-indexed).
    # Write a generator that lazily YIELDS items one by one,
    #    calling fetch_page() for each page from 1 to total_pages.
    pass


def q72_lazy_filter_generator(iterable, predicate):
    # Write a generator that lazily yields only items from `iterable`
    # for which predicate(item) returns True
    # e.g. lazy_filter([1,2,3,4,5], lambda x: x % 2 == 0) → yields 2, 4
    pass
