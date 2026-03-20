# ============================================================
# PHASE 1 — Python Basics
# File    : 01_variables.py
# Topic   : Variables and data types
# ============================================================


# ── CONCEPT ─────────────────────────────────────────────────
#
# A variable is a name that points to a value stored in memory.
# Think of it as a labelled box — the label is the name,
# the contents is the value.
#
# Why this matters for Pandas:
#   Every column in a Pandas table has a data type.
#   If the type is wrong, your calculations break silently.
#   Example: "50000" + 10 crashes. 50000 + 10 = 50010.
#   Knowing types is the first skill of a Data Engineer.
#
# ── THE 5 TYPES YOU WILL USE IN PANDAS ──────────────────────
#
#   int     → whole numbers           → 42, -7, 0
#   float   → decimal numbers         → 3.14, -0.5, 100.0
#   str     → text                    → "Alice", "HR", "2024-01-01"
#   bool    → True or False only      → True, False
#   None    → absence of a value      → None  (like NULL in SQL)


# ── EXAMPLES ────────────────────────────────────────────────

# --- int ---
age = 25
salary = 50000
print(type(age))        # <class 'int'>
print(type(salary))     # <class 'int'>

# --- float ---
price = 99.99
tax_rate = 0.18
print(type(price))      # <class 'float'>

# --- str ---
name = "Alice"
department = "HR"
date = "2024-01-01"     # looks like a date but Python sees it as text
print(type(name))       # <class 'str'>
print(type(date))       # <class 'str'>  ← important — Pandas gotcha

# --- bool ---
is_active = True
is_deleted = False
print(type(is_active))  # <class 'bool'>

# --- None ---
bonus = None            # employee has no bonus yet
print(type(bonus))      # <class 'NoneType'>
print(bonus)            # None


# ── WHY TYPES MATTER — THE PANDAS GOTCHA ────────────────────
#
# This is the single most common bug beginners hit in Pandas.
# Look at these two variables — they look similar but behave
# completely differently:

salary_number = 50000       # int   — can do math on this
salary_string = "50000"     # str   — CANNOT do math on this

print(salary_number + 10)   # 50010  ✓
# print(salary_string + 10) # TypeError: can only concatenate str to str

# When Pandas reads a CSV file, numbers sometimes come in as
# strings. You must check and fix types before doing any math.
# We'll do this properly in Phase 3.


# ── TYPE CONVERSION ─────────────────────────────────────────
#
# You can convert between types using these built-in functions:
#   int()    → converts to integer
#   float()  → converts to decimal
#   str()    → converts to text
#   bool()   → converts to True/False

x = "50000"
print(type(x))          # str

x = int(x)              # convert to int
print(type(x))          # int
print(x + 10)           # 50010  ✓

y = 99
print(float(y))         # 99.0  — int becomes float

z = 0
print(bool(z))          # False — 0 is False in Python
print(bool(1))          # True  — any non-zero number is True
print(bool("Alice"))    # True  — any non-empty string is True
print(bool(""))         # False — empty string is False
print(bool(None))       # False — None is always False


# ── CHECKING TYPES ───────────────────────────────────────────
#
# Two ways to check a variable's type:

salary = 50000

# Way 1 — type() tells you what type it is
print(type(salary))             # <class 'int'>

# Way 2 — isinstance() asks "is this a specific type?" → True/False
print(isinstance(salary, int))       # True
print(isinstance(salary, str))       # False
print(isinstance(salary, (int, float)))  # True — is it int OR float?

# isinstance() is what Pandas uses internally to validate types.
# You'll write similar checks in your own pipelines.


# ── COMMON MISTAKES ─────────────────────────────────────────
#
# MISTAKE 1: Thinking "123" and 123 are the same
a = "123"
b = 123
print(a == b)       # False — different types, never equal

# MISTAKE 2: Adding strings instead of numbers
val1 = "100"
val2 = "200"
print(val1 + val2)  # "100200" ← string concatenation, not math!
print(int(val1) + int(val2))  # 300 ← correct

# MISTAKE 3: Forgetting that None is not zero
val = None
# print(val + 10)   # TypeError — can't add to None
print(val is None)  # True — correct way to check for None


# ── EXERCISE ─────────────────────────────────────────────────
#
# Do this yourself. Don't look at the examples above.
#
# 1. Create these variables with the correct types:
#      - A customer's name         → "Raj"

#      - Their account balance     → 15750.50

#      - Their customer ID         → 1042

#      - Whether they are active   → True

#      - Their middle name         → None (they don't have one)

#
# 2. Print the type of each variable using type()

#
# 3. The balance came in from a CSV as a string "15750.50"
#    Convert it to a float and add 500.0 to it.
#    Print the result.
#

# 4. Check using isinstance() whether customer_id is an int.
#    Print True or False.
#
# Write your code below this line:
# ─────────────────────────────────────────────────────────────
customer_name = "Raj"
customer_account_balance = 15750.50
customer_id = 1042
is_active = True
customer_middle_name = None

print(f"Type of customer_name: {type(customer_name)}")
print(f"Type of customer_account_balance: {type(customer_account_balance)}")
print(f"Type of customer_id: {type(customer_id)}")
print(f"Type of is_active: {type(is_active)}")
print(f"Type of customer_middle_name: {type(customer_middle_name)}")


balance = "15750.50"
print(float(balance)+500.0)

print(isinstance(customer_id, int))