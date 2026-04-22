# ============================================================
# PHASE 5 — Transforming Data
# File    : 02_apply_and_map.py
# Topic   : apply() and map()
# ============================================================

import pandas as pd
import numpy as np

df = pd.DataFrame({
    "transaction_id": [1001, 1002, 1003, 1004, 1005],
    "customer":       ["Raj", "Priya", "Amit", "Neha", "Raj"],
    "amount":         [5000.0, 12000.0, 8000.0, 8500.0, 3200.0],
    "category":       ["food", "travel", "food", "electronics", "travel"],
    "status":         ["success", "success", "failed", "success", "success"],
    "city":           ["Delhi", "Mumbai", "Delhi", "Bangalore", "Mumbai"]
})


# ── CONCEPT ─────────────────────────────────────────────────
#
# Both apply() and map() let you transform data using a function.
# The difference is WHERE and HOW they apply that function.
#
#   apply() → works on Series AND DataFrames
#             calls your function on each VALUE (Series)
#             or each ROW/COLUMN (DataFrame)
#
#   map()   → works on Series ONLY
#             best for replacing values using a dict
#             or applying a simple function to each value
#
# When to use which:
#   Complex custom logic         → apply()
#   Simple value replacement     → map() with a dict
#   Simple condition             → np.where() (fastest)
#   Everything else              → apply()


# ── apply() on a Series ──────────────────────────────────────
#
# Calls your function on each VALUE in the column.
# x = one single value at a time.

# Using a lambda
result = df["amount"].apply(lambda x: x * 1.1)
print(result)

# Using a named function
def add_gst(amount):
    return amount * 1.18

result = df["amount"].apply(add_gst)
print(result)

# With a condition
result = df["amount"].apply(lambda x: "large" if x > 6000 else "small")
print(result)

# With multiple conditions — nested ternary
result = df["amount"].apply(
    lambda x: "high"   if x > 10000 else
             ("medium" if x > 5000  else "low")
)
print(result)

# Handling nulls inside apply
s = pd.Series([5000.0, None, 8000.0, None, 3200.0])
result = s.apply(lambda x: x * 1.1 if pd.notna(x) else 0.0)
print(result)
# pd.notna(x) checks if x is NOT null — use this inside apply
# Never use x is not None inside apply — it misses np.nan


# ── apply() on a DataFrame — row-wise ───────────────────────
#
# When you call apply() on a DataFrame with axis=1,
# x = one entire ROW as a Series.
# You access individual values with x["column_name"].
#
# Use this when the new column depends on MULTIPLE columns.

# Example: categorise based on both amount AND city
def city_amount_label(row):
    if row["city"] == "Mumbai" and row["amount"] > 5000:
        return "priority_mumbai"
    elif row["amount"] > 8000:
        return "high_value"
    else:
        return "standard"

df["label"] = df.apply(city_amount_label, axis=1)
print(df[["customer", "city", "amount", "label"]])

# Same thing with lambda — x is the whole row
df["label2"] = df.apply(
    lambda x: "priority_mumbai" if x["city"] == "Mumbai" and x["amount"] > 5000
    else ("high_value" if x["amount"] > 8000 else "standard"),
    axis=1
)

# axis=0 → apply function to each COLUMN (less common)
# axis=1 → apply function to each ROW (what you usually want)


# ── apply() on a DataFrame — column-wise ────────────────────
#
# axis=0 means apply the function to each COLUMN as a Series.
# Useful for getting a summary of each column.

# Get the max value of each column
df_numeric = df[["amount"]]
print(df_numeric.apply(lambda x: x.max(), axis=0))

# Get null count per column
print(df.apply(lambda x: x.isna().sum(), axis=0))
# same as df.isna().sum() but shows how axis=0 works


# ── map() on a Series ────────────────────────────────────────
#
# map() is specifically designed for replacing values.
# Best used with a dict — clean, readable, fast.
#
# Syntax:
#   series.map({"old_value": "new_value", ...})

# Replace status labels with numeric codes
df["status_code"] = df["status"].map({
    "success": 1,
    "failed":  0,
    "pending": -1
})
print(df[["status", "status_code"]])

# Replace city names with region labels
df["region"] = df["city"].map({
    "Delhi":     "North",
    "Mumbai":    "West",
    "Bangalore": "South",
    "Chennai":   "South"
})
print(df[["city", "region"]])

# Important: if a value is NOT in the dict, map() returns NaN
# Mumbai is in the dict → "West"
# A city not in the dict → NaN
# Always handle this with fillna() after map()
df["region"] = df["city"].map({
    "Delhi":     "North",
    "Mumbai":    "West",
    "Bangalore": "South"
}).fillna("Other")

# map() with a function — works like apply() for simple cases
df["customer_lower"] = df["customer"].map(lambda x: x.lower())
# For this kind of thing, str.lower() is cleaner:
df["customer_lower"] = df["customer"].str.lower()


# ── apply vs map vs np.where — decision guide ────────────────
#
# Ask yourself:
#
# "Is it a simple if/else based on ONE column?"
#    → np.where()   fastest, cleanest
#
# "Am I replacing specific values using a lookup table?"
#    → map() with a dict
#
# "Does the logic need MULTIPLE columns or complex conditions?"
#    → apply(axis=1) with a named function
#
# "Is it a custom transformation on ONE column?"
#    → apply() with a lambda
#
# Example comparison — all doing the same thing:

# np.where — fastest
df["size"] = np.where(df["amount"] > 6000, "large", "small")

# apply — more flexible but slower
df["size"] = df["amount"].apply(lambda x: "large" if x > 6000 else "small")

# map — only works if you list every possible value
df["size"] = df["amount"].map(
    {5000.0: "small", 12000.0: "large", 8000.0: "large",
     8500.0: "large", 3200.0: "small"}
)  # impractical for numeric ranges — use np.where instead


# ── COMMON MISTAKES ─────────────────────────────────────────

# MISTAKE 1: Using == None instead of pd.notna() inside apply
s = pd.Series([1.0, None, 3.0, np.nan])
s.apply(lambda x: x * 2 if x is not None else 0)
# This misses np.nan — np.nan is not None
# Correct:
s.apply(lambda x: x * 2 if pd.notna(x) else 0)  # ✓

# MISTAKE 2: Forgetting axis=1 for row-wise apply
#df.apply(lambda x: x["amount"] * 1.1)         # axis=0 — wrong
df.apply(lambda x: x["amount"] * 1.1, axis=1) # axis=1 — correct ✓

# MISTAKE 3: Using map() when values aren't in the dict
df["status"].map({"success": 1})
# "failed" is not in the dict → becomes NaN silently
# Always add .fillna() after map() as a safety net

# MISTAKE 4: Using apply() when np.where() would work
# apply() is 10-100x slower than np.where() on large data
# If your logic fits np.where() — always prefer it


# ── EXERCISE ─────────────────────────────────────────────────
#
# Use the df defined at the top of this file.
#
# 1. Using apply() with a lambda on the 'amount' column,
#    create a new column 'amount_after_tax' where:
#      - If amount > 8000: apply 20% tax  (amount * 1.20)
#      - Otherwise:        apply 10% tax  (amount * 1.10)
#
# 2. Using apply() with axis=1 (row-wise), create a column
#    'transaction_label' where:
#      - status is 'failed'              → "FAILED"
#      - status is 'success' and
#        amount > 8000                   → "HIGH VALUE"
#      - everything else                 → "NORMAL"
#    Write this as a named function, not a lambda.
#
# 3. Using map() with a dict, create a column 'category_code':
#      food         → "F"
#      travel       → "T"
#      electronics  → "E"
#    Any unknown category should map to "X" (use fillna).
#
# 4. You have this Series of raw status values:
#      raw = pd.Series(["SUCCESS", "Failed", "SUCCESS",
#                       None, "pending"])
#    Using apply(), clean it so that:
#      - All values are lowercased
#      - None becomes "unknown"
#    Hint: use pd.notna() to check for None/NaN inside apply.
#
# 5. Look at questions 1 and the label part of question 2.
#    Could either of them have been done with np.where instead?
#    Rewrite question 1 using np.where.
#    Which version do you prefer and why?
#
# Write your code below this line:
# ─────────────────────────────────────────────────────────────
df = pd.DataFrame({
    "transaction_id": [1001, 1002, 1003, 1004, 1005],
    "customer":       ["Raj", "Priya", "Amit", "Neha", "Raj"],
    "amount":         [5000.0, 12000.0, 8000.0, 8500.0, 3200.0],
    "category":       ["food", "travel", "food", "electronics", "travel"],
    "status":         ["success", "success", "failed", "success", "success"],
    "city":           ["Delhi", "Mumbai", "Delhi", "Bangalore", "Mumbai"]
})

df["amount_after_tax"] = df["amount"].apply(lambda x: x*1.20 if x > 8000 else x*1.10)
print(df[["amount","amount_after_tax"]])


def func_transaction_label(row):
    if row["status"] == 'failed':
        return "FAILED"
    elif row["status"] == 'success' and row["amount"]>8000:
        return "HIGH VALUE"
    return "NORMAL"
df["transaction_label"] = df.apply(func_transaction_label, axis = 1)

df["category_code"] = df["category"].map({
    "food" : "F",
    "travel" : "T",
    "electronics" : "E"
})

raw = pd.Series(["SUCCESS", "Failed", "SUCCESS",None, "pending"])
raw = raw.apply(lambda x: x.lower() if pd.notna(x) else "unknown")
print(raw)

df["amount_after_tax_new"] = np.where(df["amount"]>8000,df["amount"]*1.20,df["amount"]*1.10)
print(df[["amount","amount_after_tax","amount_after_tax_new"]])

# Use np.where where the conditions are easy to apply and vectorized as vectorization works faster