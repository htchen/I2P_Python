# ---------------------------------------------------------------------------
# Example of practicing problems `q01` to `q03` in `python101_quizzes.py`.
# 
# This will let you run only the testcases for the first three questions, without needing to implement the later ones.
# ---------------------------------------------------------------------------

def q01_swap(a, b):
    """Return (b, a) — the two arguments swapped.
    回傳 (b, a)，即將兩個引數互換後的元組。
    Hint: return (???, ???)"""
    pass

assert q01_swap(1, 2) == (2, 1)
assert q01_swap("hello", 99) == (99, "hello")


def q02_integer_ops(a, b):
    """Return a tuple of (quotient, remainder) when a is divided by b.
    Use integer (floor) division and the modulo operator.
    回傳 a 除以 b 的（商, 餘數）元組，使用整數除法與模運算子。
    Hint: return (a ??? b, a ??? b)"""
    pass

assert q02_integer_ops(17, 5) == (3, 2)
assert q02_integer_ops(20, 3) == (6, 2)


def q03_power(base, exp):
    """Return base raised to the power of exp.
    回傳 base 的 exp 次方。
    Hint: return base ??? exp"""
    pass

assert q03_power(2, 10) == 1024
assert q03_power(3, 4) == 81