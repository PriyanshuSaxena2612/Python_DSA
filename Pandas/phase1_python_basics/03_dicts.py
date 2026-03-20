# ============================================================
# PHASE 1 — Python Basics
# File    : 03_dicts.py
# Topic   : Dictionaries
# ============================================================


# ── CONCEPT ─────────────────────────────────────────────────
#
# A dictionary stores data as key-value pairs.
# Instead of accessing items by position (like a list),
# you access them by name (the key).
#
# Think of it like a real dictionary:
#   word  → definition
#   key   → value
#
# Why this matters for Pandas:
#   A DataFrame is built FROM a dictionary.
#   Keys become column names.
#   Values (lists) become the column's data.
#
#   pd.DataFrame({
#       'name':   ['Alice', 'Bob'],   ← key: 'name',   value: a list
#       'salary': [50000, 60000]      ← key: 'salary', value: a list
#   })
#
#   Every time you create a DataFrame from scratch — you use a dict.
#   Every time you rename columns — you use a dict.
#   Every time you map values — you use a dict.
#
# Syntax:
#   my_dict = { key1: value1, key2: value2 }
#   Curly braces. key: value pairs. Separated by commas.
#   Keys are almost always strings.


# ── CREATING A DICT ──────────────────────────────────────────

employee = {
    "name":       "Alice",
    "age":        30,
    "salary":     50000.0,
    "is_active":  True,
    "department": "HR"
}

print(employee)
# {'name': 'Alice', 'age': 30, 'salary': 50000.0, ...}


# ── ACCESSING VALUES ─────────────────────────────────────────
#
# Use square brackets with the key name.
# This is different from a list — you use the KEY, not a number.

print(employee["name"])       # "Alice"
print(employee["salary"])     # 50000.0
print(employee["is_active"])  # True

# If the key doesn't exist, you get a KeyError
# print(employee["bonus"])    # KeyError: 'bonus'

# Safer way — .get() returns None if key doesn't exist
print(employee.get("bonus"))         # None  — no error
print(employee.get("bonus", 0))      # 0     — default value if missing


# ── ADDING AND UPDATING VALUES ───────────────────────────────
#
# Same syntax for both — if the key exists it updates,
# if it doesn't exist it adds it.

employee["bonus"] = 5000.0       # adds new key
print(employee["bonus"])         # 5000.0

employee["salary"] = 55000.0     # updates existing key
print(employee["salary"])        # 55000.0


# ── REMOVING A KEY ───────────────────────────────────────────

employee_copy = employee.copy()   # make a copy so we don't break employee
del employee_copy["bonus"]
print("bonus" in employee_copy)   # False — it's gone


# ── CHECKING IF A KEY EXISTS ─────────────────────────────────
#
# Use 'in' — same as with lists, but checks keys not values.

print("name" in employee)      # True
print("bonus" in employee)     # True  (we added it above)
print("address" in employee)   # False


# ── LOOPING THROUGH A DICT ───────────────────────────────────
#
# Three ways to loop — you'll use all three in Pandas work.

person = {"name": "Bob", "age": 25, "salary": 60000}

# Loop through keys only
for key in person:
    print(key)
# name
# age
# salary

# Loop through values only
for value in person.values():
    print(value)
# Bob
# 25
# 60000

# Loop through both — most useful
for key, value in person.items():
    print(f"{key}: {value}")
# name: Bob
# age: 25
# salary: 60000

# This is exactly the pattern used in schema validation:
#   for col, dtype in expected_schema.items():
#       check df[col] has correct dtype


# ── A DICT OF LISTS — HOW DATAFRAMES ARE BUILT ───────────────
#
# This is the most important pattern in this file.
# A DataFrame is literally just this — a dict where every
# value is a list of the same length.

data = {
    "name":       ["Alice", "Bob",   "Charlie"],
    "department": ["HR",    "IT",    "HR"     ],
    "salary":     [50000,   60000,   55000    ],
    "is_active":  [True,    False,   True     ]
}

# Each key is a column name.
# Each list is the column's data.
# All lists MUST be the same length — otherwise Pandas throws an error.

print(data["name"])       # ['Alice', 'Bob', 'Charlie']
print(data["salary"][1])  # 60000  — Bob's salary (list index inside dict)
print(len(data["name"]))  # 3

# In the next phase we'll pass this exact dict into pd.DataFrame()
# and it becomes a proper table instantly.


# ── DICT COMPREHENSION ───────────────────────────────────────
#
# Just like list comprehensions, you can build dicts in one line.
# Syntax: { key_expr: value_expr for item in iterable }

# Example: build a dict of name → salary mappings
names    = ["Alice", "Bob", "Charlie"]
salaries = [50000,   60000, 55000   ]

salary_map = {name: salary for name, salary in zip(names, salaries)}
print(salary_map)
# {'Alice': 50000, 'Bob': 60000, 'Charlie': 55000}

# zip() pairs up two lists item by item:
# zip(["Alice","Bob"], [50000,60000]) → ("Alice",50000), ("Bob",60000)

# This pattern is used in Pandas when you rename columns:
#   df.rename(columns={"old_name": "new_name", "old_sal": "salary"})
#   That dict passed to rename is exactly this pattern.


# ── NESTED DICTS ─────────────────────────────────────────────
#
# A dict can contain another dict as a value.

employees = {
    101: {"name": "Alice", "salary": 50000},
    102: {"name": "Bob",   "salary": 60000},
}

print(employees[101])             # {'name': 'Alice', 'salary': 50000}
print(employees[101]["name"])     # 'Alice'
print(employees[102]["salary"])   # 60000


# ── COMMON MISTAKES ─────────────────────────────────────────

# MISTAKE 1: Using a key that doesn't exist
d = {"name": "Alice"}
# print(d["salary"])   # KeyError — use .get() when unsure

# MISTAKE 2: Forgetting that dict keys are case-sensitive
d = {"Name": "Alice"}
print(d.get("name"))   # None — "name" ≠ "Name"
print(d.get("Name"))   # "Alice"

# MISTAKE 3: Lists of different lengths in a DataFrame dict
# This will crash when you pass it to pd.DataFrame():
bad_data = {
    "name":   ["Alice", "Bob", "Charlie"],  # 3 items
    "salary": [50000, 60000]                # 2 items ← will cause ValueError
}
# pd.DataFrame(bad_data)  # ValueError: All arrays must be of the same length


# ── EXERCISE ─────────────────────────────────────────────────
#
# Do this yourself.
#
# You are preparing data to load into a Pandas DataFrame.
#
# 1. Create a dictionary called 'transaction' with these keys
#    and values:
#      transaction_id  → 5001
#      customer_name   → "Priya"
#      amount          → 8750.0
#      currency        → "INR"
#      is_successful   → True
#      notes           → None
#
# 2. Print the customer_name and amount using square brackets.
#
# 3. The transaction failed — update is_successful to False.
#    Also add a new key 'failure_reason' with value "Insufficient funds".
#
# 4. Safely check if 'notes' exists in the dict using 'in'.
#    Print True or False.
#
# 5. Loop through the dict using .items() and print each
#    key and value on its own line like:
#      transaction_id: 5001
#      customer_name: Priya
#      ... and so on
#
# 6. Build a dict of lists called 'transactions_table' that
#    could be passed into pd.DataFrame().
#    It should have 3 transactions with columns:
#      transaction_id, customer_name, amount
#    Make up your own values — just ensure all lists
#    are the same length.
#
# Write your code below this line:
# ─────────────────────────────────────────────────────────────
transaction = {
    "transaction_id": 5001,
    "customer_name": "Priya",
    "amount": 8750.0,
    "currency": "INR",
    "is_successful": True,
    "notes": None
}
print(transaction['customer_name'], transaction['amount'])
transaction["is_successful"] = False
transaction['failure_reason'] = 'Insufficient funds'
print('notes' in transaction)
for key, value in transaction.items():
    print(f"{key}:{value}")

transactions_table = {
    "transaction_id" : [123,234,456],
    "customer_name" : ["A","B","C"],
    "amount" : [450,400,250]
}
import pandas as pd
df = pd.DataFrame(transactions_table)
print(df)