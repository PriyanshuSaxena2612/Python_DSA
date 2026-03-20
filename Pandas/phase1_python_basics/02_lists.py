# ============================================================
# PHASE 1 — Python Basics
# File    : 02_lists.py
# Topic   : Lists
# ============================================================


# ── CONCEPT ─────────────────────────────────────────────────
#
# A list is an ordered collection of items.
# You can put anything inside — numbers, strings, booleans,
# even other lists.
#
# Why this matters for Pandas:
#   A Pandas column IS a list underneath — just smarter.
#   You use lists to:
#     - Create a DataFrame column:  {'name': ['Alice', 'Bob']}
#     - Select multiple columns:    df[['name', 'salary']]
#     - Pass column names:          df.groupby(['dept', 'city'])
#     - Filter using a list:        df[df['dept'].isin(['HR', 'IT'])]
#
# Syntax:
#   my_list = [item1, item2, item3]
#   Square brackets. Items separated by commas.


# ── CREATING LISTS ───────────────────────────────────────────

names    = ["Alice", "Bob", "Charlie"]
salaries = [50000, 60000, 75000]
actives  = [True, False, True]
mixed    = ["Alice", 50000, True, None]  # can mix types (but avoid in Pandas)

print(names)      # ['Alice', 'Bob', 'Charlie']
print(salaries)   # [50000, 60000, 75000]


# ── LENGTH ───────────────────────────────────────────────────
#
# len() tells you how many items are in the list.
# In Pandas, len(df) tells you how many rows a table has.

print(len(names))     # 3
print(len(salaries))  # 3


# ── INDEXING — accessing one item ────────────────────────────
#
# Every item has a position called an index.
# IMPORTANT: Python starts counting from 0, not 1.
#
#   names = ["Alice", "Bob", "Charlie"]
#   index:      0       1        2
#
# Access with square brackets: list[index]

print(names[0])   # "Alice"   ← first item
print(names[1])   # "Bob"     ← second item
print(names[2])   # "Charlie" ← third item
print(names[-1])  # "Charlie" ← last item  (-1 always means last)
print(names[-2])  # "Bob"     ← second from last


# ── SLICING — accessing multiple items ───────────────────────
#
# Slicing gives you a portion of the list.
# Syntax: list[start : stop]
#   start → index to begin at (included)
#   stop  → index to stop at  (NOT included)
#
# Think of it as: "give me from position start up to but not including stop"

numbers = [10, 20, 30, 40, 50]
#  index:   0   1   2   3   4

print(numbers[0:3])   # [10, 20, 30]  — positions 0, 1, 2
print(numbers[1:4])   # [20, 30, 40]  — positions 1, 2, 3
print(numbers[2:])    # [30, 40, 50]  — from position 2 to the end
print(numbers[:3])    # [10, 20, 30]  — from start to position 2
print(numbers[:])     # [10, 20, 30, 40, 50]  — everything

# In Pandas, df.head(3) is essentially df[:3] — same idea.


# ── MODIFYING LISTS ──────────────────────────────────────────

fruits = ["apple", "banana", "cherry"]

# Add one item to the end
fruits.append("mango")
print(fruits)   # ['apple', 'banana', 'cherry', 'mango']

# Add multiple items to the end
fruits.extend(["grape", "kiwi"])
print(fruits)   # ['apple', 'banana', 'cherry', 'mango', 'grape', 'kiwi']

# Remove a specific item
fruits.remove("banana")
print(fruits)   # ['apple', 'cherry', 'mango', 'grape', 'kiwi']

# Change an item at a position
fruits[0] = "orange"
print(fruits)   # ['orange', 'cherry', 'mango', 'grape', 'kiwi']


# ── CHECKING IF SOMETHING IS IN A LIST ───────────────────────
#
# The 'in' keyword checks if an item exists in a list.
# Returns True or False.
# In Pandas: df[df['dept'].isin(['HR', 'IT'])] uses this exact idea.

departments = ["HR", "IT", "Finance"]

print("HR" in departments)        # True
print("Marketing" in departments) # False
print("IT" not in departments)    # False


# ── LOOPING THROUGH A LIST ───────────────────────────────────
#
# A for loop goes through each item one at a time.
# Syntax:
#   for variable_name in list:
#       do something with variable_name
#
# The variable_name is created by you — it can be anything.
# It holds one item at a time as the loop runs.

salaries = [50000, 60000, 75000]

for salary in salaries:
    print(salary)
# prints:
# 50000
# 60000
# 75000

# You can do calculations inside the loop
for salary in salaries:
    print(salary * 1.1)   # give everyone a 10% raise
# prints:
# 55000.0
# 66000.0
# 82500.0


# ── LIST COMPREHENSION ───────────────────────────────────────
#
# A list comprehension is a one-line way to build a new list
# by looping through an existing one.
#
# Regular loop version:
raised = []
for salary in salaries:
    raised.append(salary * 1.1)
print(raised)   # [55000.0, 66000.0, 82500.0]

# List comprehension version — same result, one line:
raised = [salary * 1.1 for salary in salaries]
print(raised)   # [55000.0, 66000.0, 82500.0]
#
# Read it as:
# "make a list of (salary * 1.1) for each salary in salaries"
#
# You can also add a condition:
high_salaries = [s for s in salaries if s > 55000]
print(high_salaries)  # [60000, 75000]
#
# Read it as:
# "include s only if s > 55000, for each s in salaries"
#
# Why this matters for Pandas:
# Pandas uses similar ideas internally.
# You'll also use list comprehensions to build column name lists:
#   cols = [c for c in df.columns if c.startswith('sales_')]


# ── USEFUL LIST FUNCTIONS ────────────────────────────────────

numbers = [30, 10, 50, 20, 40]

print(sorted(numbers))        # [10, 20, 30, 40, 50] — sorted copy
print(sorted(numbers, reverse=True))  # [50, 40, 30, 20, 10]
print(min(numbers))           # 10
print(max(numbers))           # 50
print(sum(numbers))           # 150


# ── COMMON MISTAKES ─────────────────────────────────────────

# MISTAKE 1: Off by one — forgetting index starts at 0
items = ["a", "b", "c"]
# print(items[3])   # IndexError — there is no index 3, only 0,1,2

# MISTAKE 2: Confusing append and extend
nums = [1, 2, 3]
nums.append([4, 5])    # adds the whole list as one item
print(nums)            # [1, 2, 3, [4, 5]]  ← probably not what you wanted

nums = [1, 2, 3]
nums.extend([4, 5])    # adds each item individually
print(nums)            # [1, 2, 3, 4, 5]  ← this is usually what you want

# MISTAKE 3: Modifying a list while looping through it
# Never do this — it causes unpredictable behaviour
# Always loop over a copy or build a new list instead


# ── EXERCISE ─────────────────────────────────────────────────
#
# Do this yourself.
#
# You are building a small data pipeline.
# You have this raw list of employee salaries that came
# from a CSV — all as strings:
#
#   raw_salaries = ["45000", "62000", "38000", "91000", "54000"]
#
# 1. Convert raw_salaries into a list of floats called salaries.
#    Use a list comprehension.
#
# 2. Print the highest and lowest salary using max() and min().
#
# 3. Create a new list called high_earners that contains only
#    salaries above 50000. Use a list comprehension with a condition.
#
# 4. You hired a new employee with salary 75000.0.
#    Add it to the salaries list.
#    Print the updated list and its length.
#
# 5. Check if 38000.0 is in the salaries list. Print True or False.
#
# Write your code below this line:
# ─────────────────────────────────────────────────────────────

raw_salaries = ["45000", "62000", "38000", "91000", "54000"]
raw_salaries = [float(x) for x in raw_salaries]
print(raw_salaries)
print(f"Max Salary: {max(raw_salaries)}\nMin Salary: {min(raw_salaries)}")
high_earners = [x for x in raw_salaries if x>50000]
print(high_earners)
raw_salaries.extend([75000.0])
print(raw_salaries, len(raw_salaries))
print(38000.0 in raw_salaries)