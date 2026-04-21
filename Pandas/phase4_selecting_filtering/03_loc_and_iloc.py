# ============================================================
# PHASE 4 — Selecting and Filtering
# File    : 03_loc_and_iloc.py
# Topic   : loc and iloc — precise row and column selection
# ============================================================

import pandas as pd
import numpy as np

df = pd.DataFrame({
    "transaction_id": [1001, 1002, 1003, 1004, 1005],
    "customer":       ["Raj", "Priya", "Amit", "Neha", "Raj"],
    "amount":         [5000.0, 12000.0, 8000.0, 8500.0, 3200.0],
    "category":       ["food", "travel", "food", "electronics", "travel"],
    "status":         ["success", "success", "failed", "success", "success"]
})


# ── CONCEPT ─────────────────────────────────────────────────
#
# So far you've selected either:
#   - All rows, some columns  → df[["col1", "col2"]]
#   - Some rows, all columns  → df[df["amount"] > 5000]
#
# But what if you need BOTH — specific rows AND specific columns?
# That's what loc and iloc are for.
#
#   loc  → select by LABEL  (column names, index labels)
#   iloc → select by POSITION (row number, column number)
#
# Both use this syntax:
#   df.loc[row_selector, column_selector]
#   df.iloc[row_selector, column_selector]
#
# Think of it as a coordinate system:
#   rows first, columns second — always in that order.


# ── iloc — selection by POSITION ────────────────────────────
#
# iloc uses integer positions — like indexing a list.
# Rows and columns are numbered 0, 1, 2, 3...
#
# Syntax: df.iloc[row_position, column_position]

# Single row — returns a Series
print(df.iloc[0])        # first row
print(df.iloc[-1])       # last row

# Single cell — one row, one column
print(df.iloc[0, 0])     # row 0, column 0 → 1001
print(df.iloc[0, 2])     # row 0, column 2 → 5000.0
print(df.iloc[-1, 1])    # last row, column 1 → "Raj"

# Row slice — multiple rows
print(df.iloc[0:3])      # rows 0, 1, 2 (not 3)
print(df.iloc[1:4])      # rows 1, 2, 3

# Column slice — multiple columns
print(df.iloc[:, 0:3])   # all rows, columns 0, 1, 2
print(df.iloc[:, 1])     # all rows, column 1 only

# Both rows and columns
print(df.iloc[0:3, 1:3]) # rows 0-2, columns 1-2

# Specific rows and columns using lists
print(df.iloc[[0, 2, 4], [1, 2]])  # rows 0,2,4 and columns 1,2


# ── loc — selection by LABEL ─────────────────────────────────
#
# loc uses the actual index labels and column names.
# With the default index (0,1,2...) it looks similar to iloc
# but behaves differently with slicing — see below.
#
# Syntax: df.loc[row_label, column_name]

# Single row by index label
print(df.loc[0])     # row with index label 0
print(df.loc[3])     # row with index label 3

# Single cell
print(df.loc[0, "customer"])    # "Raj"
print(df.loc[2, "amount"])      # 8000.0

# Multiple columns for one row
print(df.loc[0, ["customer", "amount"]])

# Multiple rows, one column
print(df.loc[0:3, "amount"])    # rows 0,1,2,3 — note: 3 IS included with loc

# Multiple rows, multiple columns
print(df.loc[0:2, ["customer", "amount", "status"]])

# All rows, specific columns — most common use of loc
print(df.loc[:, ["customer", "amount"]])
# same as df[["customer", "amount"]] — but loc is more explicit


# ── THE KEY DIFFERENCE — loc includes the end, iloc does not ─
#
# This trips up almost everyone coming from Python lists.
#
# iloc — like Python lists — end is EXCLUDED
print(df.iloc[0:3])   # rows 0, 1, 2  (row 3 NOT included)
#
# loc — end is INCLUDED
print(df.loc[0:3])    # rows 0, 1, 2, 3  (row 3 IS included)
#
# Why? Because loc works with labels, not positions.
# If your index were ["a","b","c","d"], you'd write:
#   df.loc["a":"c"]  → includes "a", "b", "c"
# It would be confusing if "c" was excluded — you named it explicitly.


# ── loc WITH A CUSTOM INDEX ───────────────────────────────────
#
# This is where loc becomes really powerful.
# When your index has meaningful labels, loc makes selection intuitive.

df_custom = pd.DataFrame({
    "customer": ["Raj", "Priya", "Amit"],
    "amount":   [5000.0, 12000.0, 8000.0],
    "status":   ["success", "success", "failed"]
}, index=[1001, 1002, 1003])   # transaction IDs as index

# Now select by transaction ID — much more readable
print(df_custom.loc[1001])              # Raj's transaction
print(df_custom.loc[1001, "amount"])    # 5000.0
print(df_custom.loc[1001:1002])         # transactions 1001 and 1002


# ── loc WITH A BOOLEAN MASK ───────────────────────────────────
#
# This is the most important use of loc in real work.
# Combine row filtering with column selection in one step.

# Instead of two steps:
filtered = df[df["amount"] > 5000]
result   = filtered[["customer", "amount"]]

# Do it in one step with loc:
result = df.loc[df["amount"] > 5000, ["customer", "amount"]]
print(result)
#   customer   amount
# 1    Priya  12000.0
# 2     Amit   8000.0
# 3     Neha   8500.0

# Reading it: "from df, give me rows where amount > 5000,
#              and only the customer and amount columns"
#
# This is the SQL equivalent of:
# SELECT customer, amount FROM df WHERE amount > 5000


# ── UPDATING VALUES WITH loc ─────────────────────────────────
#
# loc is the CORRECT way to update values in a DataFrame.
# Never update values by chaining filters — it causes warnings.

df_copy = df.copy()

# Update a specific cell
df_copy.loc[0, "status"] = "pending"
print(df_copy.loc[0, "status"])   # "pending"

# Update multiple rows matching a condition
df_copy.loc[df_copy["status"] == "failed", "status"] = "reviewed"
print(df_copy["status"])

# Update multiple columns at once
df_copy.loc[0, ["status", "amount"]] = ["success", 9999.0]
print(df_copy.loc[0])


# ── WHEN TO USE WHICH ────────────────────────────────────────
#
#   Use iloc when:
#     - You need rows/columns by position number
#     - You're iterating through positions programmatically
#     - You don't know or care about column names
#
#   Use loc when:
#     - You know the column names (almost always)
#     - You want to filter rows AND select columns together
#     - You want to update values safely
#     - Your index has meaningful labels (IDs, dates)
#
# In practice: loc is used 80% of the time, iloc 20%.


# ── COMMON MISTAKES ─────────────────────────────────────────

# MISTAKE 1: Forgetting loc includes the end of a slice
print(df.iloc[0:3])   # rows 0,1,2 — row 3 excluded
print(df.loc[0:3])    # rows 0,1,2,3 — row 3 INCLUDED

# MISTAKE 2: Using iloc with column names
# df.iloc[0, "amount"]   # TypeError — iloc needs numbers
df.loc[0, "amount"]      # ✓ loc uses names

# MISTAKE 3: Updating via chained indexing — the classic warning
# WRONG:
df[df["status"] == "failed"]["amount"] = 0   # SettingWithCopyWarning
# RIGHT:
df.loc[df["status"] == "failed", "amount"] = 0  # ✓

# MISTAKE 4: Confusing loc and iloc when index isn't 0,1,2...
df_custom = pd.DataFrame(
    {"amount": [5000, 12000, 8000]},
    index=[10, 20, 30]
)
print(df_custom.iloc[0])    # first row — amount = 5000
print(df_custom.loc[10])    # row with label 10 — amount = 5000
# print(df_custom.loc[0])   # KeyError — there is no label 0!


# ── EXERCISE ─────────────────────────────────────────────────
#
# Use the df defined at the top of this file.
#
# 1. Using iloc, select:
#      a) the third row (index position 2)
#      b) the value at row 1, column 2 (zero-based)
#      c) the first 3 rows and first 3 columns
#
# 2. Using loc, select:
#      a) row with index label 2
#      b) the amount for row 3
#      c) columns 'customer' and 'status' for rows 0 to 2
#
# 3. Using loc with a boolean mask in ONE step:
#      Select only 'customer' and 'amount' columns
#      for rows where status is 'success'.
#
# 4. Create a copy of df called df_copy.
#    Using loc, update all 'failed' transactions:
#      - set their status to 'under_review'
#      - set their amount to 0.0
#    Print df_copy to verify.
#
# 5. Create a DataFrame with transaction IDs as the index:
#      index:    [2001, 2002, 2003]
#      customer: ["Kiran", "Sana", "Dev"]
#      amount:   [7500.0, 3200.0, 11000.0]
#    Use loc to select transaction 2002's amount.
#    Use iloc to select the same value by position.
#    Confirm both give the same result.
#
# Write your code below this line:
# ─────────────────────────────────────────────────────────────


df = pd.DataFrame({
    "transaction_id": [1001, 1002, 1003, 1004, 1005],
    "customer":       ["Raj", "Priya", "Amit", "Neha", "Raj"],
    "amount":         [5000.0, 12000.0, 8000.0, 8500.0, 3200.0],
    "category":       ["food", "travel", "food", "electronics", "travel"],
    "status":         ["success", "success", "failed", "success", "success"]
})

# 1st question
print(df.iloc[2])
print(df.iloc[1,2])
print(df.iloc[0:3,0:3])

# 2nd question
print(df.loc[2])
print(df.loc[2,"amount"])
print(df.loc[0:2,["customer","status"]])

# 3rd question
print(df.loc[df["status"] == 'success', ["customer","amount"]])

# 4th question
df_copy = df.copy()
df_copy.loc[df_copy['status'] == 'failed','status'] = 'under_review'
df_copy.loc[df_copy['status'] == 'under_review','amount'] = 0.0
print(df_copy)

# 5th question
df = pd.DataFrame(
    {
        'index':    [2001, 2002, 2003],
        'customer': ["Kiran", "Sana", "Dev"],
        'amount':   [7500.0, 3200.0, 11000.0]
    }
)

#    Use loc to select transaction 2002's amount.
#    Use iloc to select the same value by position.
#    Confirm both give the same result.
print(df)
print(df.loc[df['index'] == 2002, "amount"])
print(df.iloc[df['index'] == 2002, 2])