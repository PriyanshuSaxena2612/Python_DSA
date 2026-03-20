# ============================================================
# PHASE 1 — Python Basics
# File    : 04_functions_and_lambda.py
# Topic   : Functions and lambda
# ============================================================


# ── CONCEPT ─────────────────────────────────────────────────
#
# A function is a reusable block of code that:
#   1. Takes some input (called arguments or parameters)
#   2. Does something with it
#   3. Returns an output
#
# Why this matters for Pandas:
#   Pandas' most powerful tools take a FUNCTION as input.
#   You pass your function to Pandas, and Pandas calls it
#   on every row, every column, or every group.
#
#   df['salary'].apply(my_function)
#   df.groupby('dept')['salary'].transform(my_function)
#   df.assign(new_col=my_function)
#
#   If you don't understand functions deeply,
#   none of those will ever make sense.


# ── DEFINING A FUNCTION ──────────────────────────────────────
#
# Syntax:
#   def function_name(parameter):
#       do something
#       return result
#
# Breaking it down word by word:
#   def          → tells Python "I'm defining a function"
#   function_name → the name you give it (you choose this)
#   (parameter)  → the input the function receives (you name this too)
#   return       → sends the result back to whoever called the function

def double(x):
    return x * 2

# Calling it:
print(double(5))    # 10
print(double(100))  # 200

# x is just a placeholder name — it holds whatever you pass in.
# When you call double(5), x becomes 5 inside the function.
# When you call double(100), x becomes 100.


# ── MULTIPLE PARAMETERS ──────────────────────────────────────

def add(x, y):
    return x + y

print(add(3, 4))     # 7
print(add(10, 20))   # 30

# Parameters are positional by default —
# first argument goes to x, second to y.


# ── DEFAULT PARAMETER VALUES ─────────────────────────────────
#
# You can give a parameter a default value.
# If the caller doesn't provide it, the default is used.

def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))            # "Hello, Alice!"   — uses default
print(greet("Bob", "Welcome"))   # "Welcome, Bob!"   — overrides default

# You'll see this in Pandas constantly:
#   pd.read_csv("file.csv", sep=",")
#   sep="," is a default — you only pass it if your file uses a different separator


# ── RETURN ───────────────────────────────────────────────────
#
# return sends the result back out of the function.
# Without return, the function gives back None.

def add_no_return(x, y):
    result = x + y
    # forgot to return!

def add_with_return(x, y):
    result = x + y
    return result

print(add_no_return(3, 4))    # None  ← common bug
print(add_with_return(3, 4))  # 7    ← correct

# A function can return anything — a number, string,
# list, dict, even another function.

def get_stats(numbers):
    return {
        "min":  min(numbers),
        "max":  max(numbers),
        "sum":  sum(numbers),
        "mean": sum(numbers) / len(numbers)
    }

stats = get_stats([10, 20, 30, 40])
print(stats)          # {'min': 10, 'max': 40, 'sum': 100, 'mean': 25.0}
print(stats["mean"])  # 25.0


# ── FUNCTIONS AS ARGUMENTS ───────────────────────────────────
#
# This is the most important concept in this file.
# In Python, functions are objects — you can pass them
# to other functions as arguments.
#
# This is EXACTLY what Pandas does when you write:
#   df['salary'].apply(some_function)
#
# Pandas takes your function and calls it once per row.
# You don't call the function — Pandas does.

def apply_to_list(my_list, my_function):
    result = []
    for item in my_list:
        result.append(my_function(item))
    return result

# Notice: we pass double without () — we're passing the function itself,
# not calling it. double means "here is the function".
#                   double() means "call the function now".

salaries = [50000, 60000, 75000]

doubled  = apply_to_list(salaries, double)
print(doubled)   # [100000, 120000, 150000]

# This is precisely what .apply() does in Pandas —
# it loops through every item and calls your function on each one.


# ── LAMBDA — a function written in one line ──────────────────
#
# A lambda is a shorthand for a simple function.
# Use it when the function is short and you only need it once.
#
# Regular function:
def square(x):
    return x ** 2

# Same thing as a lambda:
square_lambda = lambda x: x ** 2
#               ↑      ↑   ↑
#             keyword input what to return
#
# Read it as: "given x, return x squared"
#
# You never write 'return' in a lambda.
# Whatever comes after the colon is automatically returned.

print(square(5))        # 25
print(square_lambda(5)) # 25  — identical

# Most of the time you don't even name the lambda.
# You write it directly where it's needed:

salaries = [50000, 60000, 75000]

# Using a named function
doubled = apply_to_list(salaries, double)

# Using a lambda inline — no need to define a separate function
doubled = apply_to_list(salaries, lambda x: x * 2)
print(doubled)   # [100000, 120000, 150000]


# ── LAMBDA WITH CONDITIONS ───────────────────────────────────
#
# A lambda can have an if/else — but only one expression.
# Syntax: lambda x: value_if_true if condition else value_if_false

bucket = lambda x: "high" if x > 55000 else "low"

print(bucket(70000))  # "high"
print(bucket(40000))  # "low"

# Equivalent regular function:
def bucket_fn(x):
    if x > 55000:
        return "high"
    else:
        return "low"

print(bucket_fn(70000))  # "high"

# In Pandas you'll write this as:
# df['salary'].apply(lambda x: 'high' if x > 55000 else 'low')
# Pandas calls your lambda once for each value in the column.


# ── LAMBDA WITH MULTIPLE INPUTS ──────────────────────────────

add = lambda x, y: x + y
print(add(3, 4))   # 7

# But in Pandas, lambdas usually only take one input —
# either one cell value (apply) or one group's Series (transform).


# ── THE x IN PANDAS LAMBDAS ──────────────────────────────────
#
# This is where most people get confused.
# The same lambda syntax means different things in different places.
# x is just a name — what it HOLDS depends on context.
#
# Context 1 — inside .apply() on a column
#   x = one single value from the column
#   Pandas loops: x=50000, then x=60000, then x=75000
#
#   df['salary'].apply(lambda x: x * 1.1)
#
# Context 2 — inside .assign()
#   x = the ENTIRE DataFrame at that point
#   You access columns with x['column_name']
#
#   df.assign(salary_k=lambda x: x['salary'] / 1000)
#
# Context 3 — inside .transform()
#   x = one GROUP's Series (all rows for one group)
#   Pandas calls your lambda once per group
#
#   df.groupby('dept')['salary'].transform(lambda x: x - x.mean())
#
# We will practice all three in their own files.
# For now just know: same syntax, different meaning depending on context.


# ── SCOPE — where variables live ─────────────────────────────
#
# Variables created inside a function only exist inside it.
# They disappear when the function ends.

def calculate():
    result = 100    # only exists inside this function
    return result

calculate()
# print(result)   # NameError — result doesn't exist out here

# But variables outside a function can be READ inside it:
tax_rate = 0.18

def calculate_tax(salary):
    return salary * tax_rate   # reads tax_rate from outside

print(calculate_tax(50000))   # 9000.0


# ── COMMON MISTAKES ─────────────────────────────────────────

# MISTAKE 1: Calling the function instead of passing it
salaries = [50000, 60000]

# WRONG — double() calls the function immediately, result (None or a value)
# is passed instead of the function itself
# apply_to_list(salaries, double())

# RIGHT — double without () passes the function object
apply_to_list(salaries, double)   # ✓

# MISTAKE 2: Forgetting return
def add_tax(salary):
    salary * 1.18   # calculated but not returned!

print(add_tax(50000))   # None ← return is missing

# MISTAKE 3: Writing multiple lines in a lambda
# This is not allowed:
# f = lambda x:
#     y = x * 2      # SyntaxError
#     return y
#
# If your logic needs multiple lines, use a regular def function.

# MISTAKE 4: Confusing x as always being a single value
# In .assign(), x is the whole DataFrame — not one value.
# Beginners often write x * 2 thinking it doubles one value,
# but it doubles every value in every column — or crashes.


# ── EXERCISE ─────────────────────────────────────────────────
#
# Do this yourself. This is the most important exercise so far.
#
# 1. Write a regular function called 'clean_salary' that:
#      - Takes one argument: a value
#      - If the value is None, return 0.0
#      - Otherwise convert it to float and return it
#    Test it:
#      clean_salary(None)     → 0.0
#      clean_salary("75000")  → 75000.0
#      clean_salary(50000)    → 50000.0
#
# 2. Write the same function as a lambda called 'clean_salary_lambda'
#    Hint: you can't handle None with a simple lambda —
#    think about what condition to check.
#    Test it with the same inputs.
#
# 3. Write a function called 'categorise' that:
#      - Takes a salary (number)
#      - Returns "junior"  if salary < 40000
#      - Returns "mid"     if 40000 <= salary < 70000
#      - Returns "senior"  if salary >= 70000
#    Test it with: 35000, 55000, 90000
#
# 4. You have this list of raw salaries:
#      raw = [None, "45000", 62000, None, "91000"]
#    Use your apply_to_list function from this file
#    (copy it into your exercise section) with clean_salary
#    to produce a clean list of floats.
#    Print the result.
#
# 5. Now do the same thing using a lambda directly —
#    no named function, just inline lambda.
#
# Write your code below this line:
# ─────────────────────────────────────────────────────────────

def clean_salary(value):
    if value is None:
        return 0.0
    return float(value)
print(clean_salary(None))     
print(clean_salary("75000"))  
print(clean_salary(50000))  

clean_salary = lambda x: 0.0 if x is None else float(x)
print(clean_salary(None))     
print(clean_salary("75000"))  
print(clean_salary(50000))  

categorise = lambda x: "junior" if x < 40000 else ("mid" if x in range(40000,70000) else "senior")
print(categorise(35000))
print(categorise(55000))
print(categorise(90000))

def apply_to_list(my_list, my_function):
    result = []
    for item in my_list:
        result.append(my_function(item))
    return result
raw = [None, "45000", 62000, None, "91000"]
print(apply_to_list(raw, clean_salary))
print(apply_to_list(raw, lambda x: 0.0 if x is None else float(x)))