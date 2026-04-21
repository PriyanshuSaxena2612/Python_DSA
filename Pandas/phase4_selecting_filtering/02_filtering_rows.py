# ============================================================
# PHASE 4 — Selecting and Filtering
# File    : 02_filtering_rows.py
# Topic   : Filtering rows from a DataFrame
# ============================================================

import pandas as pd
import numpy as np

df = pd.DataFrame({
    "transaction_id": [1001, 1002, 1003, 1004, 1005, 1006, 1007],
    "customer":       ["Raj", "Priya", "Amit", "Neha", "Raj", "Priya", "Amit"],
    "amount":         [5000.0, 12000.0, 8000.0, 8500.0, 3200.0, 15000.0, 4500.0],
    "category":       ["food", "travel", "food", "electronics", "travel", "travel", "food"],
    "status":         ["success", "success", "failed", "success", "success", "success", "failed"],
    "city":           ["Delhi", "Mumbai", "Delhi", "Bangalore", "Mumbai", "Delhi", "Bangalore"]
})


# ── CONCEPT ─────────────────────────────────────────────────
#
# Filtering rows means keeping only the rows that meet
# a condition — like SQL's WHERE clause.
#
# SQL:    SELECT * FROM transactions WHERE amount > 5000
# Pandas: df[df["amount"] > 5000]
#
# How it works — two steps happening at once:
#
#   Step 1: df["amount"] > 5000
#           → produces a Series of True/False for each row
#
#   Step 2: df[that True/False Series]
#           → keeps only rows where value is True
#
# This True/False Series is called a BOOLEAN MASK.
# Understanding the mask is the key to all filtering.


# ── THE BOOLEAN MASK ─────────────────────────────────────────

# Step 1 — create the mask
mask = df["amount"] > 5000
print(mask)
# 0    False   ← 5000 is not > 5000
# 1     True   ← 12000 is > 5000
# 2     True   ← 8000 is > 5000
# 3     True   ← 8500 is > 5000
# 4    False   ← 3200 is not > 5000
# 5     True   ← 15000 is > 5000
# 6    False   ← 4500 is not > 5000
print(type(mask))   # Series of bool

# Step 2 — use the mask to filter
result = df[mask]
print(result)
# Only rows where mask was True

# In practice you combine both steps in one line:
result = df[df["amount"] > 5000]
print(result)   # same result


# ── COMPARISON OPERATORS ─────────────────────────────────────

df[df["amount"] > 5000]    # greater than
df[df["amount"] >= 5000]   # greater than or equal
df[df["amount"] < 5000]    # less than
df[df["amount"] <= 5000]   # less than or equal
df[df["amount"] == 5000]   # equal to
df[df["amount"] != 5000]   # not equal to

# String equality
df[df["status"] == "success"]
df[df["city"] != "Delhi"]


# ── COMBINING CONDITIONS ──────────────────────────────────────
#
# Use & for AND, | for OR, ~ for NOT.
# CRITICAL RULE: wrap EACH condition in its own parentheses.
# Without parentheses Python's operator precedence causes bugs.

# AND — both conditions must be True
result = df[(df["amount"] > 5000) & (df["status"] == "success")]
print(result)

# OR — at least one condition must be True
result = df[(df["category"] == "food") | (df["category"] == "travel")]
print(result)

# NOT — flip True to False and vice versa
result = df[~(df["status"] == "failed")]   # same as status == "success"
print(result)

# Combining all three
result = df[
    (df["amount"] > 5000) &
    (df["status"] == "success") &
    ~(df["city"] == "Delhi")
]
print(result)


# ── WHY PARENTHESES ARE REQUIRED ────────────────────────────
#
# This is a very common bug. Here's why it happens:
#
# Python's & operator has higher precedence than ==.
# Without parentheses, Python reads this:
#
#   df[df["amount"] > 5000 & df["status"] == "success"]
#
# As:
#   df[df["amount"] > (5000 & df["status"]) == "success"]
#
# Which makes no sense and raises a ValueError.
#
# Always write:
#   df[(df["amount"] > 5000) & (df["status"] == "success")]


# ── FILTERING WITH isin() ────────────────────────────────────
#
# isin() checks if a value is in a list.
# Cleaner than multiple OR conditions.

# Instead of this:
df[(df["category"] == "food") | (df["category"] == "travel")]

# Write this:
df[df["category"].isin(["food", "travel"])]

# NOT in a list — use ~ to flip
df[~df["category"].isin(["food", "travel"])]   # only electronics

# isin() with a column of IDs — very common in DE work
valid_customers = ["Raj", "Priya"]
df[df["customer"].isin(valid_customers)]


# ── FILTERING WITH between() ─────────────────────────────────
#
# Cleaner than writing two conditions for a range.

# Instead of this:
df[(df["amount"] >= 5000) & (df["amount"] <= 10000)]

# Write this:
df[df["amount"].between(5000, 10000)]
# Both endpoints are included by default.


# ── FILTERING NULL VALUES ────────────────────────────────────

df_with_nulls = pd.DataFrame({
    "customer": ["Raj", "Priya", "Amit"],
    "amount":   [5000.0, None, 8000.0],
    "category": ["food", "travel", None]
})

# Keep only rows where amount is NOT null
df_with_nulls[df_with_nulls["amount"].notna()]

# Keep only rows where amount IS null
df_with_nulls[df_with_nulls["amount"].isna()]

# Keep rows where ANY column is null
df_with_nulls[df_with_nulls.isna().any(axis=1)]

# Keep rows where ALL columns are non-null
df_with_nulls[df_with_nulls.notna().all(axis=1)]


# ── FILTERING WITH query() ───────────────────────────────────
#
# query() lets you write filter conditions as a readable string.
# Cleaner for multiple conditions.

# Instead of this:
df[(df["amount"] > 5000) & (df["status"] == "success")]

# Write this:
df.query("amount > 5000 and status == 'success'")

# Using a variable inside query — use @ prefix
min_amount = 5000
df.query("amount > @min_amount and status == 'success'")

# OR / NOT in query
df.query("category in ['food', 'travel']")
df.query("category not in ['food', 'travel']")
df.query("amount > 5000 or city == 'Delhi'")


# ── FILTERING WITH str METHODS ───────────────────────────────
#
# For string columns you can filter using string operations.

# Contains a substring
df[df["city"].str.contains("al")]      # Delhi, Bangalore
df[df["customer"].str.startswith("R")] # Raj
df[df["customer"].str.endswith("j")]   # Raj

# Case insensitive contains
df[df["city"].str.contains("delhi", case=False)]

# String length
df[df["customer"].str.len() > 3]   # names longer than 3 chars


# ── FILTERING CHANGES NOTHING IN THE ORIGINAL ───────────────
#
# Filtering returns a NEW DataFrame.
# The original df is always unchanged.

result = df[df["amount"] > 5000]
print(len(df))      # 7   — original unchanged
print(len(result))  # 4   — filtered copy


# ── COMMON MISTAKES ─────────────────────────────────────────

# MISTAKE 1: Missing parentheses around conditions
# df[df["amount"] > 5000 & df["status"] == "success"]  # ValueError
df[(df["amount"] > 5000) & (df["status"] == "success")]  # ✓

# MISTAKE 2: Using 'and' / 'or' instead of & / |
# df[df["amount"] > 5000 and df["status"] == "success"]  # ValueError
df[(df["amount"] > 5000) & (df["status"] == "success")]  # ✓

# MISTAKE 3: Checking equality with a single =
# df[df["status"] = "success"]   # SyntaxError
df[df["status"] == "success"]    # ✓  double equals

# MISTAKE 4: Forgetting that filter result must be assigned
df[df["amount"] > 5000]          # result is thrown away
result = df[df["amount"] > 5000] # ✓ assign it


# ── EXERCISE ─────────────────────────────────────────────────
#
# Use the df defined at the top of this file.
#
# 1. Filter rows where amount is greater than 6000.
#    Print the result and its shape.
#
# 2. Filter rows where status is 'success' AND city is 'Delhi'.
#    Print the result.
#
# 3. Filter rows where category is either 'food' OR 'electronics'.
#    Use isin() — not multiple OR conditions.
#
# 4. Filter rows where amount is between 4000 and 9000 (inclusive).
#    Use between().
#
# 5. Filter rows where status is NOT 'failed'.
#    Do this two ways:
#      a) using != operator
#      b) using ~ with ==
#    Confirm both give the same result using .equals()
#      Hint: result_a.equals(result_b) → True or False
#
# 6. Using query(), filter rows where:
#      amount > 5000 AND status == 'success'
#    Store the minimum amount from this query in a variable
#    called min_amount, then use it inside another query()
#    with @min_amount.
#
# 7. Filter rows where customer name contains the letter 'i'.
#    Use str.contains().
#
# Write your code below this line:
# ─────────────────────────────────────────────────────────────

df = pd.DataFrame({
    "transaction_id": [1001, 1002, 1003, 1004, 1005, 1006, 1007],
    "customer":       ["Raj", "Priya", "Amit", "Neha", "Raj", "Priya", "Amit"],
    "amount":         [5000.0, 12000.0, 8000.0, 8500.0, 3200.0, 15000.0, 4500.0],
    "category":       ["food", "travel", "food", "electronics", "travel", "travel", "food"],
    "status":         ["success", "success", "failed", "success", "success", "success", "failed"],
    "city":           ["Delhi", "Mumbai", "Delhi", "Bangalore", "Mumbai", "Delhi", "Bangalore"]
})

mask_amount = df['amount']>6000
print(df[mask_amount])

mask_status_city = (df['status'] == 'success') & (df['city'] == 'Delhi')
print(df[mask_status_city])

mask_category = df["category"].isin(["food","electronics"])
print(df[mask_category])

mask_amount_between = df['amount'].between(4000,9000)
print(df[mask_amount_between])

mask_status_1 = df['status']!='failed'
mask_status_2 = ~(df['status'] == 'failed')
print(df[mask_status_1])
print(df[mask_status_2])

min_amount = 5000
df_query = (df.query("(amount > @min_amount) and status == 'success'"))
print(df_query)

print(df[df['city'].str.contains('i')])