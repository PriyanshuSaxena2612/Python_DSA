# ============================================================
# PHASE 5 — Transforming Data
# File    : 01_adding_columns.py
# Topic   : Adding and modifying columns
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
# Adding a column means creating a new attribute for every row.
# Modifying a column means changing existing values.
#
# There are three ways to do this in Pandas:
#
#   1. Direct assignment    df["new"] = expression
#   2. assign()             df.assign(new=expression)
#   3. np.where()           for conditional columns
#
# We cover all three here — and when to use which.


# ── WAY 1 — Direct assignment ────────────────────────────────
#
# Simplest way. Modifies df in place.
# Use this when you're not chaining operations.

df["amount_usd"] = df["amount"] / 83
print(df["amount_usd"])

# Modify an existing column
df["amount"] = df["amount"].round(2)

# Based on another column
df["amount_doubled"] = df["amount"] * 2

# Based on multiple columns
df["amount_with_tax"] = df["amount"] * 1.18

# String operation
df["customer_upper"] = df["customer"].str.upper()

# From a fixed value — same value for every row
df["currency"] = "INR"
df["version"]  = 1

print(df.head())


# ── WAY 2 — assign() ─────────────────────────────────────────
#
# assign() returns a NEW DataFrame — original is unchanged.
# Use this when you want to keep the original safe,
# or when you're building a pipeline.
#
# Syntax:
#   df.assign(new_column_name = expression)
#
# With lambda:
#   df.assign(new_column_name = lambda x: x["col"] * 2)
#   Here x = the entire DataFrame at that point

df2 = df.assign(amount_usd=lambda x: x["amount"] / 83)
print("original df still unchanged:", "amount_usd" in df.columns)  # depends on way 1 above
print(df2["amount_usd"])

# Multiple columns in one assign — only when they're INDEPENDENT
df2 = df.assign(
    amount_usd  = lambda x: x["amount"] / 83,
    amount_gbp  = lambda x: x["amount"] / 105,
    currency    = "INR"
)

# When second column depends on first — use TWO assigns
df2 = (
    df
    .assign(amount_usd=lambda x: x["amount"] / 83)
    .assign(amount_usd_rounded=lambda x: x["amount_usd"].round(2))
)
# In a single assign, amount_usd_rounded can't reference amount_usd
# because both are evaluated against the ORIGINAL df simultaneously.


# ── WAY 3 — np.where() for conditional columns ──────────────
#
# np.where is the fastest way to create a column based on a condition.
# Think of it as a vectorized if/else.
#
# Syntax:
#   np.where(condition, value_if_true, value_if_false)

df["size"] = np.where(df["amount"] > 6000, "large", "small")
print(df[["amount", "size"]])
# amount > 6000 → "large", otherwise → "small"

# Multiple conditions — nested np.where
# Like SQL: CASE WHEN ... WHEN ... ELSE ...
df["amount_tier"] = np.where(
    df["amount"] > 10000, "platinum",
    np.where(
        df["amount"] > 6000, "gold",
        np.where(
            df["amount"] > 3000, "silver",
            "bronze"
        )
    )
)
print(df[["amount", "amount_tier"]])


# ── WHEN TO USE WHICH ────────────────────────────────────────
#
#   Direct assignment  → simple, modifies in place, easy to read
#   assign()           → safe (doesn't modify original), good for pipelines
#   np.where()         → fast conditional columns, prefer over apply()
#
# Performance order (fastest to slowest):
#   Pure math      df["col"] * 2           → fastest
#   np.where()     conditional             → fast
#   apply(lambda)  custom logic per row    → slowest


# ── MODIFYING EXISTING COLUMNS ───────────────────────────────

df_mod = df.copy()

# Overwrite with cleaned version
df_mod["category"] = df_mod["category"].str.lower().str.strip()

# Round numeric column
df_mod["amount"] = df_mod["amount"].round(0)

# Cast type
df_mod["transaction_id"] = df_mod["transaction_id"].astype(str)

# Fill nulls
df_mod["amount"] = df_mod["amount"].fillna(0.0)


# ── DROPPING COLUMNS ─────────────────────────────────────────

# Drop helper columns you added during processing
df_clean = df.drop(columns=["amount_doubled", "customer_upper", "version"])
print(df_clean.columns.to_list())


# ── COMMON MISTAKES ─────────────────────────────────────────

# MISTAKE 1: Forgetting assign() doesn't modify original
df.assign(new_col=df["amount"] * 2)   # result thrown away
df2 = df.assign(new_col=df["amount"] * 2)  # ✓ assign back

# MISTAKE 2: Two dependent columns in one assign
df.assign(
    col_a = lambda x: x["amount"] * 2,
    col_b = lambda x: x["col_a"] + 1   # KeyError — col_a doesn't exist yet
)
# Fix: use two separate assigns

# MISTAKE 3: Using apply for simple conditions
df["size"] = df["amount"].apply(lambda x: "large" if x > 6000 else "small")
# Works but slow. Use np.where instead:
df["size"] = np.where(df["amount"] > 6000, "large", "small")  # ✓ faster


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
#     "city":           ["Delhi", "Mumbai", "Delhi", "Bangalore", "Mumbai"]
# })
#
# 1. Using direct assignment, add these columns:
#      - 'amount_usd'  → amount divided by 83, rounded to 2 decimal places
#      - 'is_large'    → True if amount > 7000, else False
#                        (do this with a simple vectorized comparison,
#                         no np.where needed — think about what
#                         df["amount"] > 7000 returns on its own)
#
# 2. Using np.where, add a column 'priority':
#      - 'high'    if amount > 10000
#      - 'medium'  if amount > 5000
#      - 'low'     otherwise
#
# 3. Using assign() with a lambda, create df2 that adds:
#      - 'customer_lower' → customer name in lowercase
#      - 'amount_inr_str' → amount as a string with " INR" appended
#        e.g. 5000.0 → "5000.0 INR"
#    Do both in a single assign() call.
#    Confirm original df is unchanged.
#
# 4. The 'category' column has inconsistent casing in real data.
#    Standardise it to lowercase in place using direct assignment.
#
# 5. Drop 'is_large' and 'priority' from df.
#    Print remaining column names.
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

df["amount_usd"] = df["amount"]/83
df["is_large"] = df["amount"]>7000

df['priority'] = np.where(df['amount']>10000,'high',
                          np.where(df['amount']>5000,'medium','low'))

df2 = df.assign(
    customer_lower = lambda x: x['customer'].str.lower(),
    amount_inr_str = lambda x: x['amount'].astype(str) + ' INR'
)

print(df2['amount_inr_str'])

df['category'] = df['category'].str.lower()
df = df.drop(columns = ['is_large','priority'])
print(df.columns)