"""
Python Language 101 — Fill-in-the-Code Quizzes
Week 01–06 Essential Understanding
Python 101 語言填空測驗（第一至六週）

Instructions / 作答說明:
  Each function has an English + 繁體中文 docstring describing what it must do.
  Replace every `pass` with the correct Python code.
  Do NOT change function signatures, docstrings, or test cases.

Topics / 主題:
  Q01–Q08   Variables & Types           變數與型別          (Week 01)
  Q09–Q14   Strings                     字串                (Week 01–02)
  Q15–Q20   Tuples & Math Module        元組與數學模組       (Week 01)
  Q21–Q30   Lists                       串列                (Week 02)
  Q31–Q38   Loops & Iteration           迴圈與迭代          (Week 02)
  Q39–Q46   Dictionaries                字典                (Week 02)
  Q47–Q56   Comprehensions & Lambdas    推導式與匿名函式    (Week 02)
  Q57–Q64   Functions (Advanced)        函式（進階）        (Week 01–02)
  Q65–Q68   Sorting & Built-ins         排序與內建函式      (Week 02)
  Q69–Q72   Generators                  生成器              (Week 06)
"""

import math


# ---------------------------------------------------------------------------
# WEEK 01 — Variables & Types  （變數與型別）
# ---------------------------------------------------------------------------

def q01_swap(a, b):
    """Return (b, a) — the two arguments swapped.
    回傳 (b, a)，即將兩個引數互換後的元組。"""
    pass

assert q01_swap(1, 2) == (2, 1)


def q02_integer_ops(a, b):
    """Return a tuple of (quotient, remainder) when a is divided by b.
    Use integer (floor) division and the modulo operator.
    回傳 a 除以 b 的（商, 餘數）元組，使用整數除法與模運算子。"""
    pass

assert q02_integer_ops(17, 5) == (3, 2)


def q03_power(base, exp):
    """Return base raised to the power of exp.
    回傳 base 的 exp 次方。"""
    pass

assert q03_power(2, 10) == 1024


def q04_type_of(value):
    """Return the type of value.
    回傳 value 的型別。"""
    pass

assert q04_type_of(3.14) == float


def q05_convert_to_int(s):
    """Convert the string s to an integer and return it.
    將字串 s 轉換為整數並回傳。"""
    pass

assert q05_convert_to_int("42") == 42


def q06_convert_to_float(s):
    """Convert the string s to a float and return it.
    將字串 s 轉換為浮點數並回傳。"""
    pass

assert q06_convert_to_float("3.14") == 3.14


def q07_is_even(n):
    """Return True if n is even, False otherwise.
    若 n 為偶數則回傳 True，否則回傳 False。"""
    pass

assert q07_is_even(4) == True
assert q07_is_even(7) == False


def q08_absolute_value(n):
    """Return the absolute value of n without using abs().
    不使用 abs()，回傳 n 的絕對值。"""
    pass

assert q08_absolute_value(-9) == 9
assert q08_absolute_value(5) == 5


# ---------------------------------------------------------------------------
# WEEK 01–02 — Strings  （字串）
# ---------------------------------------------------------------------------

def q09_fstring_format(name, score):
    """Return a formatted string: "<name> scored <score> points"
    Use an f-string.
    使用 f-string 回傳格式化字串："<name> scored <score> points"。"""
    pass

assert q09_fstring_format("Alice", 95) == "Alice scored 95 points"


def q10_fstring_precision(value):
    """Return a string showing value formatted to exactly 2 decimal places.
    Use an f-string with a format spec.
    使用 f-string 格式規格，回傳保留恰好兩位小數的字串。"""
    pass

assert q10_fstring_precision(3.14159) == "3.14"


def q11_string_slicing(s):
    """Return a tuple: (first 3 characters, last 3 characters, reversed string).
    回傳元組：（前 3 個字元、後 3 個字元、反轉後的字串）。"""
    pass

assert q11_string_slicing("abcdefg") == ("abc", "efg", "gfedcba")


def q12_string_methods(s):
    """Return a tuple: (s uppercased, s lowercased, s stripped of whitespace).
    回傳元組：（全大寫、全小寫、去除首尾空白後的字串）。"""
    pass

assert q12_string_methods("  Hello  ") == ("  HELLO  ", "  hello  ", "Hello")


def q13_string_split_join(sentence):
    """Split sentence on spaces into words, then join them with hyphens.
    Return the joined string.
    以空格分割 sentence 為單字串列，再用連字號連接並回傳。"""
    pass

assert q13_string_split_join("one two three") == "one-two-three"


def q14_string_contains_count(s, sub):
    """Return a tuple: (True/False whether sub is in s,
    the number of times sub appears in s).
    回傳元組：（sub 是否存在於 s 的布林值、sub 在 s 中出現的次數）。"""
    pass

assert q14_string_contains_count("banana", "an") == (True, 2)


# ---------------------------------------------------------------------------
# WEEK 01 — Tuples & Math Module  （元組與數學模組）
# ---------------------------------------------------------------------------

def q15_create_tuple(a, b, c):
    """Return a tuple containing a, b, c in that order.
    依序將 a、b、c 包裝為元組並回傳。"""
    pass

assert q15_create_tuple(1, 2, 3) == (1, 2, 3)


def q16_unpack_and_sum(triple):
    """triple is a tuple of three numbers. Unpack it and return their sum.
    triple 是含三個數字的元組，將其拆包後回傳三數之總和。"""
    pass

assert q16_unpack_and_sum((4, 5, 6)) == 15


def q17_single_element_tuple(value):
    """Return a tuple containing exactly one element: value.
    回傳只包含一個元素 value 的元組。"""
    pass

assert q17_single_element_tuple(7) == (7,)
assert type(q17_single_element_tuple(7)) == tuple


def q18_tuple_index(t, i):
    """Return the element at index i of tuple t.
    回傳元組 t 中索引 i 的元素。"""
    pass

assert q18_tuple_index((10, 20, 30), -1) == 30


def q19_math_operations(x):
    """Return a tuple: (square root of x, ceiling of x, floor of x).
    回傳元組：（x 的平方根、無條件進位、無條件捨去）。"""
    pass

assert q19_math_operations(9.0) == (3.0, 9, 9)
assert q19_math_operations(2.3) == (math.sqrt(2.3), 3, 2)


def q20_degrees_radians_round_trip(degrees):
    """Convert degrees to radians, then convert back to degrees and return it.
    將角度轉為弧度，再轉回角度並回傳（浮點數）。"""
    pass

assert abs(q20_degrees_radians_round_trip(180.0) - 180.0) < 1e-9


# ---------------------------------------------------------------------------
# WEEK 02 — Lists  （串列）
# ---------------------------------------------------------------------------

def q21_build_list(n):
    """Return a list of integers from 1 to n inclusive.
    回傳包含 1 到 n（含）的整數串列。"""
    pass

assert q21_build_list(5) == [1, 2, 3, 4, 5]


def q22_list_ops(lst):
    """Return a tuple: (minimum value, maximum value, sum) of the list.
    回傳元組：（最小值、最大值、總和）。"""
    pass

assert q22_list_ops([3, 1, 4, 1, 5]) == (1, 5, 14)


def q23_list_slice_middle(lst):
    """Return a new list with all elements except the first and last.
    回傳去掉第一個與最後一個元素後的新串列。"""
    pass

assert q23_list_slice_middle([1, 2, 3, 4, 5]) == [2, 3, 4]


def q24_list_reverse(lst):
    """Return a new reversed list without modifying the original.
    回傳反轉後的新串列，不得修改原串列。"""
    pass

original = [1, 2, 3]
assert q24_list_reverse(original) == [3, 2, 1]
assert original == [1, 2, 3]


def q25_list_sort_ascending(lst):
    """Return a new list sorted in ascending order without modifying the original.
    回傳升冪排序後的新串列，不得修改原串列。"""
    pass

original = [3, 1, 4, 1, 5]
assert q25_list_sort_ascending(original) == [1, 1, 3, 4, 5]
assert original == [3, 1, 4, 1, 5]


def q26_list_remove_first(lst, value):
    """Remove the first occurrence of value from lst in place and return lst.
    原地移除 lst 中第一個等於 value 的元素，並回傳 lst。"""
    pass

assert q26_list_remove_first([1, 2, 3, 2], 2) == [1, 3, 2]


def q27_list_insert_at(lst, index, value):
    """Insert value at the given index in lst in place and return lst.
    原地在 lst 的指定索引處插入 value，並回傳 lst。"""
    pass

assert q27_list_insert_at([1, 2, 3], 1, 99) == [1, 99, 2, 3]


def q28_list_count_membership(lst, value):
    """Return a tuple: (count of value in lst, True if value is in lst).
    回傳元組：（value 在 lst 中的出現次數、value 是否存在於 lst）。"""
    pass

assert q28_list_count_membership([1, 2, 2, 3], 2) == (2, True)
assert q28_list_count_membership([1, 2, 2, 3], 9) == (0, False)


def q29_flatten_two_lists(lst1, lst2):
    """Return a new list with all elements of lst1 followed by lst2.
    Do not modify either input.
    回傳將 lst1 與 lst2 依序合併的新串列，不得修改原串列。"""
    pass

assert q29_flatten_two_lists([1, 2], [3, 4]) == [1, 2, 3, 4]


def q30_list_unique(lst):
    """Return a list of unique elements from lst, preserving original order.
    回傳 lst 中不重複的元素串列，保留原始順序。"""
    pass

assert q30_list_unique([3, 1, 2, 1, 3]) == [3, 1, 2]


# ---------------------------------------------------------------------------
# WEEK 02 — Loops & Iteration  （迴圈與迭代）
# ---------------------------------------------------------------------------

def q31_sum_with_loop(numbers):
    """Use a for loop to return the sum of numbers. Do not use sum().
    使用 for 迴圈計算並回傳 numbers 的總和，不得使用 sum()。"""
    pass

assert q31_sum_with_loop([1, 2, 3, 4, 5]) == 15


def q32_countdown(n):
    """Use a while loop to return a list counting down from n to 1.
    使用 while 迴圈回傳從 n 倒數至 1 的串列。"""
    pass

assert q32_countdown(5) == [5, 4, 3, 2, 1]


def q33_range_step():
    """Return a list of every third integer from 0 to 30 inclusive.
    回傳從 0 到 30（含）每隔三個數的整數串列。"""
    pass

assert q33_range_step() == [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]


def q34_enumerate_labels(items):
    """Use enumerate() to return a list of "1. item", "2. item", ... (1-based).
    使用 enumerate() 回傳 "1. 項目"、"2. 項目"⋯⋯（從 1 開始）的字串串列。"""
    pass

assert q34_enumerate_labels(["a", "b", "c"]) == ["1. a", "2. b", "3. c"]


def q35_zip_pairs(keys, values):
    """Use zip() to return a dict mapping each key to its corresponding value.
    使用 zip() 回傳將 keys 對應至 values 的字典。"""
    pass

assert q35_zip_pairs(["x", "y"], [10, 20]) == {"x": 10, "y": 20}


def q36_consecutive_pairs(lst):
    """Return a list of overlapping consecutive (a, b) pairs from lst.
    回傳 lst 中相鄰元素組成的 (a, b) 元組串列。"""
    pass

assert q36_consecutive_pairs([1, 2, 3, 4]) == [(1, 2), (2, 3), (3, 4)]


def q37_loop_break(numbers, target):
    """Return the index of the first occurrence of target, or -1 if not found.
    Use a for loop and break.
    使用 for 迴圈與 break，回傳 target 第一次出現的索引，找不到則回傳 -1。"""
    pass

assert q37_loop_break([5, 3, 8, 3], 8) == 2
assert q37_loop_break([5, 3, 8, 3], 9) == -1


def q38_loop_continue(numbers):
    """Use a for loop with continue to return only the positive numbers.
    使用含 continue 的 for 迴圈，回傳只包含正數的串列。"""
    pass

assert q38_loop_continue([-1, 2, -3, 4, 0]) == [2, 4]


# ---------------------------------------------------------------------------
# WEEK 02 — Dictionaries  （字典）
# ---------------------------------------------------------------------------

def q39_build_dict(keys, values):
    """Return a dict mapping keys[i] to values[i].
    回傳將 keys[i] 對應至 values[i] 的字典。"""
    pass

assert q39_build_dict(["a", "b"], [1, 2]) == {"a": 1, "b": 2}


def q40_safe_get(d, key, default):
    """Return d[key], or default if key is absent.
    回傳 d[key]；若鍵不存在則回傳 default。"""
    pass

assert q40_safe_get({"a": 1}, "a", 0) == 1
assert q40_safe_get({"a": 1}, "b", 0) == 0


def q41_dict_add_update(d, key, value):
    """Add or update key → value in d and return d.
    在 d 中新增或更新 key → value，並回傳 d。"""
    pass

assert q41_dict_add_update({"a": 1}, "b", 2) == {"a": 1, "b": 2}
assert q41_dict_add_update({"a": 1}, "a", 9) == {"a": 9}


def q42_dict_remove_key(d, key):
    """Remove key from d if it exists and return d. No error if absent.
    若 key 存在則從 d 中移除，並回傳 d；鍵不存在時不可報錯。"""
    pass

assert q42_dict_remove_key({"a": 1, "b": 2}, "a") == {"b": 2}
assert q42_dict_remove_key({"a": 1}, "z") == {"a": 1}


def q43_dict_keys_values(d):
    """Return a tuple: (sorted list of keys, list of values in that same order).
    回傳元組：（排序後的鍵串列、對應排序順序的值串列）。"""
    pass

assert q43_dict_keys_values({"b": 2, "a": 1, "c": 3}) == (["a", "b", "c"], [1, 2, 3])


def q44_dict_merge(d1, d2):
    """Return a new dict with all entries from d1 and d2.
    d2 values win on duplicate keys.
    回傳包含 d1 與 d2 所有項目的新字典；重複鍵以 d2 的值為準。"""
    pass

assert q44_dict_merge({"a": 1, "b": 2}, {"b": 9, "c": 3}) == {"a": 1, "b": 9, "c": 3}


def q45_nested_dict_access(d, outer_key, inner_key):
    """Return d[outer_key][inner_key], or None if either key is missing.
    回傳 d[outer_key][inner_key]；任一鍵不存在則回傳 None。"""
    pass

assert q45_nested_dict_access({"a": {"x": 42}}, "a", "x") == 42
assert q45_nested_dict_access({"a": {"x": 42}}, "a", "y") is None
assert q45_nested_dict_access({"a": {"x": 42}}, "z", "x") is None


def q46_count_occurrences(items):
    """Return a dict mapping each unique value to its count in items.
    回傳將 items 中每個不重複值對應至其出現次數的字典。"""
    pass

assert q46_count_occurrences(["a", "b", "a", "c", "b", "a"]) == {"a": 3, "b": 2, "c": 1}


# ---------------------------------------------------------------------------
# WEEK 02 — Comprehensions & Lambdas  （推導式與匿名函式）
# ---------------------------------------------------------------------------

def q47_squares_comprehension(n):
    """Return [1², 2², ..., n²] using a list comprehension.
    使用串列推導式回傳 [1², 2², ..., n²]。"""
    pass

assert q47_squares_comprehension(5) == [1, 4, 9, 16, 25]


def q48_even_filter_comprehension(numbers):
    """Return only the even numbers from numbers using a list comprehension.
    使用串列推導式回傳 numbers 中的所有偶數。"""
    pass

assert q48_even_filter_comprehension([1, 2, 3, 4, 5, 6]) == [2, 4, 6]


def q49_transform_comprehension(words):
    """Return each word uppercased, using a list comprehension.
    使用串列推導式回傳每個單字的大寫版本。"""
    pass

assert q49_transform_comprehension(["hi", "world"]) == ["HI", "WORLD"]


def q50_nested_comprehension(matrix):
    """Flatten a list-of-lists into a single list using a nested comprehension.
    使用巢狀串列推導式將二維串列攤平為一維串列。"""
    pass

assert q50_nested_comprehension([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]


def q51_dict_comprehension(lst):
    """Return a dict mapping each string to its length, using a dict comprehension.
    使用字典推導式回傳每個字串對應其長度的字典。"""
    pass

assert q51_dict_comprehension(["cat", "elephant", "ox"]) == {"cat": 3, "elephant": 8, "ox": 2}


def q52_dict_comprehension_filter(d):
    """Return a new dict with only entries whose value is positive,
    using a dict comprehension.
    使用字典推導式回傳只包含正數值的新字典。"""
    pass

assert q52_dict_comprehension_filter({"a": 3, "b": -1, "c": 0, "d": 7}) == {"a": 3, "d": 7}


def q53_map_transform(numbers):
    """Use map() with a lambda to return a list where each number is tripled.
    使用 map() 搭配 lambda，回傳每個元素乘以三的串列。"""
    pass

assert q53_map_transform([1, 2, 3]) == [3, 6, 9]


def q54_filter_transform(numbers):
    """Use filter() with a lambda to return numbers greater than 10.
    使用 filter() 搭配 lambda，回傳大於 10 的數字串列。"""
    pass

assert q54_filter_transform([5, 10, 15, 20]) == [15, 20]


def q55_lambda_expression():
    """Return a lambda that takes two numbers and returns the larger one.
    回傳一個接受兩個數字並回傳較大值的 lambda。"""
    pass

f = q55_lambda_expression()
assert f(3, 7) == 7
assert f(10, 2) == 10


def q56_sorted_with_key(words):
    """Return words sorted by length (shortest first) using sorted() with a key.
    使用 sorted() 搭配 key，回傳按字串長度升冪排序的串列。"""
    pass

assert q56_sorted_with_key(["banana", "fig", "apple", "kiwi"]) == ["fig", "kiwi", "apple", "banana"]


# ---------------------------------------------------------------------------
# WEEK 01–02 — Functions (Advanced)  （函式：進階）
# ---------------------------------------------------------------------------

def q57_default_parameter(value, multiplier=2):
    """Return value * multiplier. multiplier defaults to 2.
    回傳 value 乘以 multiplier，multiplier 預設為 2。"""
    pass

assert q57_default_parameter(5) == 10
assert q57_default_parameter(5, 3) == 15


def q58_keyword_call_demo(a, b, c):
    """Return a - b + c.
    回傳 a - b + c。"""
    pass

assert q58_keyword_call_demo(c=3, a=10, b=4) == 9


def q59_multiple_return(numbers):
    """Return a tuple (min_val, max_val, mean) where mean is a float.
    回傳元組 (最小值, 最大值, 平均值)，平均值為浮點數。"""
    pass

assert q59_multiple_return([2, 4, 6]) == (2, 6, 4.0)


def q60_variadic_sum(*args):
    """Accept any number of positional arguments and return their sum.
    接受任意數量的位置引數並回傳其總和。"""
    pass

assert q60_variadic_sum(1, 2, 3, 4) == 10
assert q60_variadic_sum() == 0


def q61_variadic_kwargs(**kwargs):
    """Return a sorted list of "key=value" strings from the keyword arguments.
    回傳由關鍵字引數組成的 "key=value" 字串串列，依鍵名排序。"""
    pass

assert q61_variadic_kwargs(b=2, a=1, c=3) == ["a=1", "b=2", "c=3"]


def q62_inner_function(x):
    """Define an inner function named double that returns its argument times 2,
    then call it with x and return the result.
    定義名為 double 的內部函式（回傳引數乘以 2），以 x 呼叫後回傳結果。"""
    pass

assert q62_inner_function(6) == 12


def q63_function_as_argument(numbers, transform):
    """Apply transform to every element of numbers and return the resulting list.
    Do not use map().
    將 transform 套用至 numbers 每個元素，回傳結果串列（不得使用 map()）。"""
    pass

assert q63_function_as_argument([1, 2, 3], lambda x: x ** 2) == [1, 4, 9]


def q64_recursive_factorial(n):
    """Return n! using recursion. Base case: factorial(0) == 1.
    使用遞迴回傳 n 的階乘，基底情況：factorial(0) == 1。"""
    pass

assert q64_recursive_factorial(0) == 1
assert q64_recursive_factorial(5) == 120


# ---------------------------------------------------------------------------
# WEEK 02 — Sorting & Built-ins  （排序與內建函式）
# ---------------------------------------------------------------------------

def q65_sort_by_second(pairs):
    """Return the list of (a, b) tuples sorted by the second element ascending.
    回傳依每個元組第二個元素升冪排序後的新串列。"""
    pass

assert q65_sort_by_second([(1, 3), (2, 1), (3, 2)]) == [(2, 1), (3, 2), (1, 3)]


def q66_sort_dicts_by_key(records, key):
    """Return records sorted by records[i][key] in descending order.
    回傳依 records[i][key] 降冪排序後的新串列。"""
    pass

data = [{"name": "B", "score": 70}, {"name": "A", "score": 90}, {"name": "C", "score": 80}]
assert q66_sort_dicts_by_key(data, "score") == [
    {"name": "A", "score": 90}, {"name": "C", "score": 80}, {"name": "B", "score": 70}
]


def q67_min_max_with_key(words):
    """Return a tuple: (shortest word, longest word) using min() and max() with a key.
    使用帶 key 的 min() 與 max()，回傳（最短單字, 最長單字）元組。"""
    pass

assert q67_min_max_with_key(["hi", "elephant", "cat"]) == ("hi", "elephant")


def q68_any_all(numbers):
    """Return a tuple: (True if any number > 100, True if all numbers > 0).
    回傳元組：（是否有任一數 > 100、是否所有數均 > 0）。"""
    pass

assert q68_any_all([1, 50, 200]) == (True, True)
assert q68_any_all([1, 50, 80]) == (False, True)
assert q68_any_all([-1, 50, 200]) == (True, False)


# ---------------------------------------------------------------------------
# WEEK 06 — Generators  （生成器）
# ---------------------------------------------------------------------------

def q69_counting_generator(start, stop):
    """A generator that yields integers from start up to (not including) stop.
    生成器函式，從 start 逐一產出整數直到（不含）stop。"""
    pass

assert list(q69_counting_generator(3, 7)) == [3, 4, 5, 6]


def q70_fibonacci_generator(limit):
    """A generator that yields Fibonacci numbers (0, 1, 1, 2, 3, 5, ...)
    as long as the value is <= limit.
    生成器函式，產出不超過 limit 的費氏數列（0, 1, 1, 2, 3, 5, ...）。"""
    pass

assert list(q70_fibonacci_generator(10)) == [0, 1, 1, 2, 3, 5, 8]


def q71_generator_pipeline(iterable, predicate, transform):
    """A generator that yields transform(item) for each item in iterable
    where predicate(item) is True.
    生成器函式，對 iterable 中滿足 predicate(item) 的每個元素產出 transform(item)。"""
    pass

result = list(q71_generator_pipeline(
    range(10),
    lambda x: x % 2 == 0,
    lambda x: x ** 2
))
assert result == [0, 4, 16, 36, 64]


def q72_take(generator, n):
    """Consume at most n values from generator and return them as a list.
    從 generator 最多取出 n 個值並回傳為串列。"""
    pass

assert q72_take(q69_counting_generator(0, 100), 5) == [0, 1, 2, 3, 4]
assert q72_take(q69_counting_generator(0, 3), 10) == [0, 1, 2]
