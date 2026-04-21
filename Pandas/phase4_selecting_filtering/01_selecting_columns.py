# ============================================================
# PHASE 4 — Selecting and Filtering
# File    : 01_selecting_columns.py
# Topic   : Selecting columns from a DataFrame
# ============================================================

import pandas as pd
import numpy as np

df = pd.DataFrame({
    "transaction_id": [1001, 1002, 1003, 1004, 1005],
    "customer":       ["Raj", "Priya", "Amit", "Neha", "Raj"],
    "amount":         [5000.0, 12000.0, 8000.0, 8500.0, 3200.0],
    "category":       ["food", "travel", "food", "electronics", "travel"],
    "status":         ["success", "success", "failed", "success", "success"],
    "date":           ["2024-01-01", "2024-01-02", "2024-01-02",
                       "2024-01-03", "2024-01-03"]
})


# ── CONCEPT ─────────────────────────────────────────────────
#
# Selecting columns means picking which columns you want
# to work with — like SQL's SELECT.
#
# SQL:    SELECT customer, amount FROM transactions
# Pandas: df[["customer", "amount"]]
#
# Two things to know before anything else:
#
#   Single bracket  df["col"]    → returns a Series
#   Double bracket  df[["col"]]  → returns a DataFrame
#
# This single vs double bracket difference trips up
# almost every beginner. We'll cover it in detail below.


# ── SINGLE BRACKET — returns a Series ───────────────────────
#
# Use when you want ONE column to do calculations on.

amount = df["amount"]
print(type(amount))   # <class 'pandas.core.series.Series'>
print(amount)
# 0     5000.0
# 1    12000.0
# 2     8000.0
# 3     8500.0
# 4     3200.0

# You can do math directly on a Series
print(amount.mean())   # 7340.0
print(amount.sum())    # 36700.0


# ── DOUBLE BRACKET — returns a DataFrame ────────────────────
#
# Use when you want ONE OR MORE columns and need to keep
# the table structure (a DataFrame, not a Series).

subset = df[["customer", "amount"]]
print(type(subset))    # <class 'pandas.core.frame.DataFrame'>
print(subset)
#   customer   amount
# 0      Raj   5000.0
# 1    Priya  12000.0
# 2     Amit   8000.0
# 3     Neha   8500.0
# 4      Raj   3200.0

# Even for a single column — if you want a DataFrame back:
single_as_df = df[["amount"]]
print(type(single_as_df))   # DataFrame — notice the double bracket


# ── WHY DOES THIS MATTER ─────────────────────────────────────
#
# Some operations only work on Series.
# Some operations only work on DataFrames.
# Using the wrong bracket causes confusing errors.

# Series operations — need single bracket
df["amount"].mean()     # ✓ works
df["amount"].sum()      # ✓ works

# DataFrame operations — need double bracket
df[["amount"]].describe()   # ✓ works — returns a formatted table
# df["amount"].describe()   # also works but output is different format

# When you're filtering rows, you need a Series of True/False.
# That only comes from a single bracket:
mask = df["amount"] > 5000    # Series of True/False ✓
# mask = df[["amount"]] > 5000  # DataFrame of True/False — harder to use


# ── SELECTING MULTIPLE COLUMNS ───────────────────────────────

# Pass a list of column names inside the outer brackets
cols = df[["customer", "amount", "status"]]
print(cols)

# You can also build the list separately — cleaner for many columns
wanted_cols = ["customer", "amount", "status"]
cols = df[wanted_cols]
print(cols)

# Reorder columns by selecting in a different order
reordered = df[["status", "customer", "amount"]]
print(reordered.columns.to_list())
# ['status', 'customer', 'amount']


# ── SELECTING COLUMNS BY CONDITION ──────────────────────────
#
# Sometimes you don't know column names upfront.
# You select columns programmatically using list comprehensions.

# Select all numeric columns
numeric_cols = [col for col in df.columns if df[col].dtype in ["int64", "float64"]]
print(numeric_cols)   # ['transaction_id', 'amount']

# Select all string (object) columns
string_cols = [col for col in df.columns if df[col].dtype == "object"]
print(string_cols)    # ['customer', 'category', 'status', 'date']

# Select columns whose name contains a keyword
id_cols = [col for col in df.columns if "id" in col.lower()]
print(id_cols)        # ['transaction_id']

# Then use the result to select
print(df[numeric_cols])


# ── PANDAS BUILT-IN COLUMN TYPE SELECTORS ───────────────────
#
# Cleaner than list comprehensions for type-based selection.

# select_dtypes — select columns by dtype
numeric_df = df.select_dtypes(include=["int64", "float64"])
print(numeric_df.columns.to_list())   # ['transaction_id', 'amount']

string_df = df.select_dtypes(include="object")
print(string_df.columns.to_list())    # ['customer', 'category', 'status', 'date']

# Exclude instead of include
non_numeric = df.select_dtypes(exclude=["int64", "float64"])
print(non_numeric.columns.to_list())


# ── DROPPING COLUMNS ─────────────────────────────────────────
#
# Sometimes easier to say what you DON'T want
# instead of listing everything you do want.

# Drop one column
df_no_date = df.drop(columns=["date"])
print(df_no_date.columns.to_list())

# Drop multiple columns
df_minimal = df.drop(columns=["date", "transaction_id"])
print(df_minimal.columns.to_list())

# Original df is unchanged
print(df.columns.to_list())   # still has all columns


# ── RENAMING COLUMNS ─────────────────────────────────────────

df_renamed = df.rename(columns={
    "transaction_id": "txn_id",
    "customer":       "customer_name"
})
print(df_renamed.columns.to_list())

# Rename all columns at once using a list
# (list must be same length as number of columns)
df.columns = ["txn_id", "cust", "amt", "cat", "stat", "dt"]
print(df.columns.to_list())

# Reset back to original names for the rest of the file
df.columns = ["transaction_id", "customer", "amount",
              "category", "status", "date"]


# ── COMMON MISTAKES ─────────────────────────────────────────

# MISTAKE 1: Single vs double bracket confusion
print(type(df["amount"]))      # Series
print(type(df[["amount"]]))    # DataFrame
# If you get an AttributeError trying to use a DataFrame method
# on a Series (or vice versa), this is usually why.

# MISTAKE 2: Trying to select a column that doesn't exist
# df["Amount"]   # KeyError — column names are case sensitive
# df["AMOUNT"]   # KeyError
# df["amount"]   # ✓ correct

# MISTAKE 3: Modifying the result without assigning back
df.drop(columns=["date"])        # does nothing — result is thrown away
df = df.drop(columns=["date"])   # correct — assign back
# Then re-add date for the exercise:
df["date"] = ["2024-01-01", "2024-01-02", "2024-01-02",
              "2024-01-03", "2024-01-03"]


# ── EXERCISE ─────────────────────────────────────────────────
#
# Use this DataFrame for all questions:
#
# df = pd.DataFrame({
#     "transaction_id": [1001, 1002, 1003, 1004, 1005],
#     "customer":       ["Raj", "Priya", "Amit", "Neha", "Raj"],
#     "amount":         [5000.0, 12000.0, 8000.0, 8500.0, 3200.0],
#     "category":       ["food", "travel", "food", "electronics", "travel"],
#     "status":         ["success", "success", "failed", "success", "success"],
#     "date":           ["2024-01-01", "2024-01-02", "2024-01-02",
#                        "2024-01-03", "2024-01-03"]
# })
#
# 1. Select just the 'amount' column as a Series.
#    Confirm it's a Series using type().
#    Print its sum and mean.
#
# 2. Select 'customer' and 'amount' as a DataFrame.
#    Confirm it's a DataFrame using type().
#
# 3. Select all columns EXCEPT 'transaction_id' and 'date'.
#    Do this using drop() — not by listing the columns you want.
#
# 4. Using a list comprehension, find all columns whose name
#    contains the letter 'a' (lowercase).
#    Print the list, then select those columns from df.
#
# 5. Select only the numeric columns using select_dtypes().
#    Print the result.
#
# 6. Rename 'transaction_id' to 'txn_id' and
#    'customer' to 'customer_name'.
#    Print the new column names.
#
# Write your code below this line:
# ─────────────────────────────────────────────────────────────

df = pd.DataFrame({
    "transaction_id": [1001, 1002, 1003, 1004, 1005],
    "customer":       ["Raj", "Priya", "Amit", "Neha", "Raj"],
    "amount":         [5000.0, 12000.0, 8000.0, 8500.0, 3200.0],
    "category":       ["food", "travel", "food", "electronics", "travel"],
    "status":         ["success", "success", "failed", "success", "success"],
    "date":           ["2024-01-01", "2024-01-02", "2024-01-02",
                       "2024-01-03", "2024-01-03"]
})

print(
    df["amount"],"\n",
    type(df["amount"]),
    f"\nSum: {df["amount"].sum()} Mean: {df["amount"].mean()}"
)

print(
    df[["customer","amount"]],"\n",
    type(df[["customer","amount"]])
)

dropped_cols = ["transaction_id","date"]
df_dropped_cols = df.drop(columns = dropped_cols)
print(df_dropped_cols)

cols_with_a = [col for col in df.columns if 'a' in col.lower()]
print(cols_with_a)

print(df.select_dtypes(include="int64"))

df_renamed = df.rename(columns = {
        "transaction_id": "txn_id",
        "customer": "customer_name"
    }
)
print(df_renamed)