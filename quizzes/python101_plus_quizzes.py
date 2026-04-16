"""
Python Language Essential Plus — Fill-in-the-Code Quizzes
Week 08–10 Intermediate Understanding
Python 進階語言填空測驗（第八至十週）

Instructions / 作答說明:
  Each function has an English + 繁體中文 docstring describing what it must do,
  followed by a Hint with key components masked as ???.
  Replace every `pass` with the correct Python code.
  Do NOT change function signatures, docstrings, or test cases.

Topics / 主題:
  Q01–Q06   2D Lists & Matrices          二維串列與矩陣          (Week 08)
  Q07–Q16   Functional Programming       函數式程式設計          (Week 09)
  Q17–Q24   Permutations & Graph Search  排列與圖形搜尋          (Week 10)
"""

import itertools
import operator
import functools


# ---------------------------------------------------------------------------
# WEEK 08 — 2D Lists & Matrices  （二維串列與矩陣）
# ---------------------------------------------------------------------------

def q01_create_matrix(rows, cols, fill=0):
    """Return an rows×cols 2D list where every cell contains fill.
    回傳一個 rows×cols 的二維串列，每個格子都填入 fill。
    Hint: return [[??? for _ in range(???)] for _ in range(???)]"""
    pass

assert q01_create_matrix(2, 3) == [[0, 0, 0], [0, 0, 0]]
assert q01_create_matrix(3, 2, 9) == [[9, 9], [9, 9], [9, 9]]


def q02_matrix_element(matrix, row, col):
    """Return the element at the given row and column of matrix.
    回傳矩陣中指定列與行位置的元素。
    Hint: return matrix[???][???]"""
    pass

assert q02_matrix_element([[1, 2, 3], [4, 5, 6]], 1, 2) == 6
assert q02_matrix_element([[10, 20], [30, 40], [50, 60]], 2, 0) == 50


def q03_get_column(matrix, col):
    """Return all values in the given column of matrix as a list.
    回傳矩陣中指定行（直行）的所有元素串列。
    Hint: return [row[???] for row in ???]"""
    pass

assert q03_get_column([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1) == [2, 5, 8]
assert q03_get_column([[10, 20], [30, 40]], 0) == [10, 30]


def q04_transpose(matrix):
    """Return the transpose of matrix: swap rows and columns.
    The input is guaranteed to be a non-empty rectangular matrix.
    回傳矩陣的轉置：將列與行互換。輸入保證為非空矩形矩陣。
    Hint: return [[matrix[???][???] for ??? in range(len(matrix))] for ??? in range(len(matrix[0]))]"""
    pass

assert q04_transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
assert q04_transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]


def q05_flatten_matrix(matrix):
    """Return a flat list of all elements in matrix, row by row.
    回傳矩陣所有元素依列順序組成的一維串列。
    Hint: return [x for row in ??? for x in ???]"""
    pass

assert q05_flatten_matrix([[1, 2], [3, 4], [5, 6]]) == [1, 2, 3, 4, 5, 6]
assert q05_flatten_matrix([[9]]) == [9]


def q06_matrix_max(matrix):
    """Return the largest value found anywhere in the 2D matrix.
    回傳二維矩陣中所有元素的最大值。
    Hint: return max(??? for row in matrix for x in ???)"""
    pass

assert q06_matrix_max([[3, 1], [4, 1], [5, 9]]) == 9
assert q06_matrix_max([[7, 2, 8], [1, 6, 0]]) == 8


# ---------------------------------------------------------------------------
# WEEK 09 — Functional Programming  （函數式程式設計）
# ---------------------------------------------------------------------------

def q07_pure_add_item(lst, item):
    """Return a new list with item appended, without modifying the original lst.
    回傳在 lst 末端加上 item 的新串列，不得修改原始串列。
    Hint: return ??? + [???]"""
    pass

original = [1, 2, 3]
assert q07_pure_add_item(original, 4) == [1, 2, 3, 4]
assert original == [1, 2, 3]
assert q07_pure_add_item([], 99) == [99]


def q08_apply_by_index(funcs, index, value):
    """funcs is a list of single-argument functions.
    Call the function at position index with value and return the result.
    funcs 是單引數函式的串列，以 index 選取函式並以 value 呼叫，回傳結果。
    Hint: return ???[???](???)"""
    pass

ops = [lambda x: x + 1, lambda x: x * 2, lambda x: x ** 2]
assert q08_apply_by_index(ops, 0, 5) == 6
assert q08_apply_by_index(ops, 2, 4) == 16


def q09_make_multiplier(factor):
    """Return a function that multiplies its argument by factor.
    回傳一個將引數乘以 factor 的函式（閉包）。
    Hint: def ???(x): return x ??? ???; return ???"""
    pass

double = q09_make_multiplier(2)
triple = q09_make_multiplier(3)
assert double(7) == 14
assert triple(5) == 15


def q10_map_transform(numbers, func):
    """Apply func to every element of numbers using map() and return a list.
    使用 map() 將 func 套用至 numbers 的每個元素，回傳串列。
    Hint: return list(???(???, numbers))"""
    pass

assert q10_map_transform([1, 2, 3, 4], lambda x: x ** 2) == [1, 4, 9, 16]
assert q10_map_transform(["hi", "world"], str.upper) == ["HI", "WORLD"]


def q11_filter_items(items, predicate):
    """Return a list of items for which predicate returns True, using filter().
    使用 filter() 回傳 predicate 為 True 的元素串列。
    Hint: return list(???(???, items))"""
    pass

assert q11_filter_items([1, 2, 3, 4, 5, 6], lambda x: x % 2 == 0) == [2, 4, 6]
assert q11_filter_items(["cat", "elephant", "ox"], lambda s: len(s) > 3) == ["elephant"]


def q12_sort_multi_key(records):
    """records is a list of dicts with "name", "rating" (float), and "distance" (float).
    Return records sorted by rating DESCENDING, then distance ASCENDING for ties.
    records 是含 "name"、"rating"（浮點數）、"distance"（浮點數）的字典串列。
    回傳依 rating 降冪、距離同分時升冪排序的新串列。
    Hint: return ???(records, key=lambda r: (-r[???], r[???]))"""
    pass

data = [
    {"name": "A", "rating": 4.5, "distance": 1.0},
    {"name": "B", "rating": 4.8, "distance": 2.0},
    {"name": "C", "rating": 4.5, "distance": 0.5},
]
result = q12_sort_multi_key(data)
assert [r["name"] for r in result] == ["B", "C", "A"]

data2 = [
    {"name": "X", "rating": 3.0, "distance": 5.0},
    {"name": "Y", "rating": 5.0, "distance": 1.0},
]
result2 = q12_sort_multi_key(data2)
assert [r["name"] for r in result2] == ["Y", "X"]


def q13_itemgetter_sort(records, key):
    """Return records sorted in ascending order by the field named key,
    using operator.itemgetter as the sort key.
    使用 operator.itemgetter，依欄位 key 升冪排序 records 並回傳新串列。
    Hint: return ???(records, key=operator.???(???))"""
    pass

people = [{"name": "Charlie", "age": 30}, {"name": "Alice", "age": 25}, {"name": "Bob", "age": 35}]
assert [p["name"] for p in q13_itemgetter_sort(people, "age")] == ["Alice", "Charlie", "Bob"]
assert [p["name"] for p in q13_itemgetter_sort(people, "name")] == ["Alice", "Bob", "Charlie"]


def q14_map_then_filter(numbers, transform, predicate):
    """Apply transform to every element of numbers with map(), then
    keep only those where predicate is True with filter(). Return a list.
    先以 map() 套用 transform，再以 filter() 保留 predicate 為 True 的元素，回傳串列。
    Hint: return list(???(???, ???(???, numbers)))"""
    pass

assert q14_map_then_filter([1, 2, 3, 4, 5], lambda x: x * 2, lambda x: x > 6) == [8, 10]
assert q14_map_then_filter([-2, -1, 0, 1, 2], lambda x: x ** 2, lambda x: x > 0) == [4, 1, 1, 4]


def q15_reduce_accumulate(numbers, func, initial):
    """Use functools.reduce() to accumulate numbers with func, starting from initial.
    使用 functools.reduce() 以 func 累積 numbers，初始值為 initial，回傳結果。
    Hint: return functools.???(???, numbers, ???)"""
    pass

assert q15_reduce_accumulate([1, 2, 3, 4], lambda acc, x: acc + x, 0) == 10
assert q15_reduce_accumulate([1, 2, 3, 4], lambda acc, x: acc * x, 1) == 24


def q16_pipeline(data, *funcs):
    """Apply each function in funcs to data in sequence (output of one is input of next).
    Return the final result.
    依序將 funcs 中的每個函式套用至 data（前一個的輸出為下一個的輸入），回傳最終結果。
    Hint: result = ???; for f in ???: result = ???(result); return result"""
    pass

assert q16_pipeline(
    [3, 1, 4, 1, 5],
    lambda lst: [x for x in lst if x > 1],   # keep > 1  → [3, 4, 5]
    lambda lst: [x * 2 for x in lst],          # double    → [6, 8, 10]
    sum                                         # sum       → 24
) == 24
assert q16_pipeline("  hello  ", str.strip, str.upper) == "HELLO"


# ---------------------------------------------------------------------------
# WEEK 10 — Permutations & Graph Search  （排列與圖形搜尋）
# ---------------------------------------------------------------------------

def q17_all_permutations(items):
    """Return a list of all permutations of items as tuples,
    using itertools.permutations.
    使用 itertools.permutations 回傳 items 所有排列的元組串列。
    Hint: return list(itertools.???(???))"""
    pass

assert sorted(q17_all_permutations([1, 2, 3])) == [(1,2,3),(1,3,2),(2,1,3),(2,3,1),(3,1,2),(3,2,1)]
assert len(q17_all_permutations([1, 2, 3, 4])) == 24


def q18_all_pairs(items):
    """Return a list of all unique unordered pairs (2-combinations) from items,
    using itertools.combinations.
    使用 itertools.combinations 回傳 items 中所有不重複無序配對（2-組合）的串列。
    Hint: return list(itertools.???(???, ???))"""
    pass

assert sorted(q18_all_pairs([1, 2, 3])) == [(1, 2), (1, 3), (2, 3)]
assert len(q18_all_pairs([1, 2, 3, 4])) == 6


def q19_route_distance(matrix, path):
    """matrix is a 2D list where matrix[i][j] is the distance from node i to node j.
    path is an ordered list of node indices to visit.
    Return the total distance of traveling along path (not a round-trip).
    matrix 是二維距離矩陣，path 是依序訪問的節點索引串列。
    回傳沿 path 行走的總距離（非來回）。
    Hint: return sum(matrix[path[???]][path[???]] for i in range(len(path) ??? 1))"""
    pass

m = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
assert q19_route_distance(m, [0, 1, 2]) == 4   # 0→1 (1) + 1→2 (3) = 4
assert q19_route_distance(m, [2, 0, 1]) == 3   # 2→0 (2) + 0→1 (1) = 3


def q20_round_trip_distance(matrix, path):
    """Same as route_distance, but also add the distance from the last node
    back to the first node (making it a round trip).
    與 route_distance 相同，但需額外加上從最後節點回到起點的距離（形成來回路徑）。
    Hint: total = ???(matrix, path); return total ??? matrix[path[???]][path[???]]"""
    pass

m = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
assert q20_round_trip_distance(m, [0, 1, 2]) == 6   # 0→1→2→0: 1+3+2 = 6
assert q20_round_trip_distance(m, [0, 2, 1]) == 6   # 0→2→1→0: 2+3+1 = 6


def q21_build_distance_matrix(points, dist_func):
    """points is a list of n items. dist_func(a, b) returns the distance between two items.
    Return an n×n 2D list where matrix[i][j] = dist_func(points[i], points[j]).
    points 是 n 個元素的串列，dist_func(a, b) 回傳兩元素間的距離。
    回傳 n×n 的二維距離矩陣，matrix[i][j] = dist_func(points[i], points[j])。
    Hint: return [[???(???[???], ???[???]) for j in range(len(???))) for i in range(len(???))]"""
    pass

pts = [0, 1, 3]
m = q21_build_distance_matrix(pts, lambda a, b: abs(a - b))
assert m == [[0, 1, 3], [1, 0, 2], [3, 2, 0]]

pts2 = [10, 20]
m2 = q21_build_distance_matrix(pts2, lambda a, b: abs(a - b))
assert m2 == [[0, 10], [10, 0]]


def q22_brute_force_shortest(matrix):
    """matrix is an n×n distance matrix (n >= 2).
    Fix node 0 as the start. Try every permutation of the remaining nodes as the
    visiting order. Return the permutation (as a tuple) that yields the minimum
    ONE-WAY total distance (do not include return to start).
    matrix 是 n×n 距離矩陣（n >= 2）。固定節點 0 為起點，窮舉其餘節點的所有排列順序，
    回傳使單程總距離最小的排列（tuple）（不含返回起點）。
    Hint: others = list(range(1, len(???))); return min(itertools.???(???), key=lambda p: ???(matrix, [0] + list(p)))"""
    pass

m = [[0, 2, 9, 10],
     [1, 0, 6,  4],
     [15, 7, 0, 8],
     [6, 3, 12, 0]]

def _dist(mat, path):
    return sum(mat[path[i]][path[i+1]] for i in range(len(path)-1))

best = q22_brute_force_shortest(m)
assert isinstance(best, tuple)
all_perms = list(itertools.permutations(range(1, 4)))
assert _dist(m, [0]+list(best)) == min(_dist(m, [0]+list(p)) for p in all_perms)

m2 = [[0, 3, 1], [3, 0, 2], [1, 2, 0]]
best2 = q22_brute_force_shortest(m2)
# [0,1,2]: 3+2=5  [0,2,1]: 1+2=3  → best is (2,1)
assert _dist(m2, [0]+list(best2)) == min(_dist(m2, [0]+list(p)) for p in itertools.permutations(range(1, 3)))


def q23_nearest_neighbor(matrix, start=0):
    """Implement the nearest-neighbor heuristic starting from node start:
    repeatedly visit the closest unvisited node until all nodes are visited.
    Return the resulting path as a list of node indices.
    從 start 節點出發，每次前往最近的未訪問節點，直到所有節點都被訪問。
    回傳訪問順序的節點索引串列。
    Hint:
        visited = {???}; path = [???]; current = ???
        while len(path) < len(???):
            next_node = min((n for n in range(len(???)) if n ??? visited), key=lambda n: ???[current][n])
            path.???(next_node); visited.???(next_node); current = ???
        return path"""
    pass

m = [[0, 2, 9, 10],
     [2, 0, 6,  4],
     [9, 6, 0,  8],
     [10, 4, 8, 0]]
path = q23_nearest_neighbor(m, start=0)
assert path[0] == 0
assert sorted(path) == [0, 1, 2, 3]   # visits all nodes
assert path == [0, 1, 3, 2]           # greedy: 0→1(2), 1→3(4), 3→2(8)

m2 = [[0, 1, 100], [1, 0, 2], [100, 2, 0]]
path2 = q23_nearest_neighbor(m2, start=0)
assert path2 == [0, 1, 2]


def q24_count_permutations_under(matrix, limit):
    """Count how many ONE-WAY routes starting from node 0 (over all permutations
    of the remaining nodes) have a total distance strictly less than limit.
    計算從節點 0 出發（窮舉其餘節點的所有排列），單程總距離嚴格小於 limit 的路徑數量。
    Hint: return sum(1 for p in itertools.???(range(1, len(???))) if ???(matrix, [0]+list(p)) ??? limit)"""
    pass

m = [[0, 1, 2, 3],
     [1, 0, 1, 2],
     [2, 1, 0, 1],
     [3, 2, 1, 0]]
# [0,1,2,3]=1+1+1=3, [0,1,3,2]=1+2+1=4, all others >= 5
assert q24_count_permutations_under(m, 4) == 1   # only distance 3 qualifies
assert q24_count_permutations_under(m, 5) == 2   # distances 3 and 4 qualify
