# ============================================================
# PHASE 5 — Transforming Data
# File    : 03_string_methods.py
# Topic   : String methods — .str accessor
# ============================================================

import pandas as pd
import numpy as np

df = pd.DataFrame({
    "transaction_id": [1001, 1002, 1003, 1004, 1005],
    "customer":       ["  Raj  ", "PRIYA", "amit", "Neha R.", "RAJ"],
    "email":          ["raj@gmail.com", "priya@yahoo.com", "amit@gmail.com",
                       "neha@outlook.com", "raj2@gmail.com"],
    "amount":         [5000.0, 12000.0, 8000.0, 8500.0, 3200.0],
    "category":       ["FOOD", "Travel", "food", "ELECTRONICS", "travel"],
    "description":    ["Food order - Delhi", "Flight Mumbai-Goa",
                       "Grocery Delhi store", "Phone purchase",
                       "Train ticket booking"]
})


# ── CONCEPT ─────────────────────────────────────────────────
#
# String columns in Pandas are dtype 'object'.
# To apply string operations on them you use the .str accessor.
#
# .str gives you access to all Python string methods
# but applies them to every row at once — no loop needed.
#
# Without .str — you'd need apply():
#   df["customer"].apply(lambda x: x.lower())   # slow
#
# With .str — vectorized, much faster:
#   df["customer"].str.lower()                   # fast


# ── CASE METHODS ─────────────────────────────────────────────

print(df["customer"].str.lower())    # all lowercase
print(df["customer"].str.upper())    # all uppercase
print(df["customer"].str.title())    # Title Case — first letter of each word
print(df["customer"].str.capitalize()) # Only first letter of whole string


# ── WHITESPACE ───────────────────────────────────────────────
#
# Real data often has leading/trailing spaces.
# Always strip when cleaning string columns.

print(df["customer"].str.strip())    # remove both sides
print(df["customer"].str.lstrip())   # remove left only
print(df["customer"].str.rstrip())   # remove right only

# Standardise in one step — strip then lowercase
df["customer_clean"] = df["customer"].str.strip().str.lower()
print(df["customer_clean"])
# "  Raj  " → "raj"
# "PRIYA"   → "priya"


# ── CONTAINS, STARTSWITH, ENDSWITH ───────────────────────────
#
# These return a Series of True/False — use for filtering.

print(df["email"].str.contains("gmail"))
# True, False, True, False, True

print(df["customer"].str.startswith("R"))
print(df["customer"].str.endswith("."))

# Case insensitive
print(df["description"].str.contains("delhi", case=False))

# Use directly in filtering
gmail_users = df[df["email"].str.contains("gmail")]
print(gmail_users[["customer", "email"]])


# ── REPLACE ──────────────────────────────────────────────────

# Simple replacement
df["description_clean"] = df["description"].str.replace("-", "to")
print(df["description_clean"])

# Replace multiple characters
df["customer_clean"] = df["customer"].str.strip().str.replace(".", "").str.lower()

# regex=True — use regular expression patterns (advanced)
# Remove all non-alphanumeric characters
df["customer_alphanum"] = df["customer"].str.replace(r"[^a-zA-Z0-9 ]", "", regex=True)
print(df["customer_alphanum"])


# ── SPLIT ────────────────────────────────────────────────────
#
# Split a string into parts.
# Returns a Series of lists.

# Split email into username and domain
parts = df["email"].str.split("@")
print(parts)
# 0    [raj, gmail.com]
# 1    [priya, yahoo.com]
# ...

# Access specific part with .str[index]
df["email_domain"] = df["email"].str.split("@").str[1]
print(df["email_domain"])
# gmail.com, yahoo.com, gmail.com...

df["email_user"] = df["email"].str.split("@").str[0]
print(df["email_user"])

# Split description into first word
df["first_word"] = df["description"].str.split(" ").str[0]
print(df["first_word"])
# Food, Flight, Grocery, Phone, Train


# ── SLICE ────────────────────────────────────────────────────
#
# Extract characters by position — like Python string slicing.

df["email_first3"] = df["email"].str[0:3]
print(df["email_first3"])
# raj, pri, ami, neh, raj

# Last 4 characters
df["email_last4"] = df["email"].str[-4:]
print(df["email_last4"])


# ── LENGTH ───────────────────────────────────────────────────

df["name_length"] = df["customer"].str.strip().str.len()
print(df[["customer", "name_length"]])

# Filter by string length
long_descriptions = df[df["description"].str.len() > 15]
print(long_descriptions["description"])


# ── EXTRACT PATTERNS — str.extract() ────────────────────────
#
# Extract specific parts of a string using a pattern.
# Uses regex groups — the part in () is what gets extracted.

# Extract numbers from description
df["desc_numbers"] = df["description"].str.extract(r"(\d+)")
print(df[["description", "desc_numbers"]])

# Extract domain extension from email
df["domain_ext"] = df["email"].str.extract(r"\.(\w+)$")
print(df[["email", "domain_ext"]])
# gmail.com → com, yahoo.com → com, outlook.com → com


# ── str METHODS RETURN NEW SERIES ────────────────────────────
#
# Just like everything else in Pandas — str methods don't
# modify the original. You must assign the result.

df["category"].str.lower()              # result thrown away
df["category"] = df["category"].str.lower()  # ✓ saved


# ── CHAINING str METHODS ─────────────────────────────────────
#
# You can chain multiple str operations together.

df["customer_final"] = (
    df["customer"]
    .str.strip()           # remove whitespace
    .str.lower()           # lowercase
    .str.replace(".", "", regex=False)  # remove dots
    .str.replace(" ", "_")  # replace spaces with underscore
)
print(df["customer_final"])


# ── HANDLING NULLS IN str METHODS ────────────────────────────
#
# str methods automatically skip NaN values and return NaN.
# No need to handle them manually.

s = pd.Series(["Hello", None, "World", np.nan])
print(s.str.lower())
# 0    hello
# 1     None   ← NaN stays NaN, no crash
# 2    world
# 3     None


# ── COMMON MISTAKES ─────────────────────────────────────────

# MISTAKE 1: Forgetting .str before the method
# df["customer"].lower()       # AttributeError — Series has no .lower()
df["customer"].str.lower()     # ✓

# MISTAKE 2: Using apply for simple string ops
df["customer"].apply(lambda x: x.lower())  # works but slow
df["customer"].str.lower()                 # faster ✓

# MISTAKE 3: Not stripping before other operations
# "  Raj  " == "Raj" → False because of spaces
# Always strip first when comparing or grouping string columns

# MISTAKE 4: Forgetting that str.contains returns NaN for null values
s = pd.Series(["hello", None, "world"])
print(s.str.contains("hello"))
# 0     True
# 1     None   ← not False, it's NaN
# 2    False
# Use na=False to treat nulls as False:
print(s.str.contains("hello", na=False))
# 0     True
# 1    False
# 2    False


# ── EXERCISE ─────────────────────────────────────────────────
#
# Use the df defined at the top of this file.
#
# 1. Clean the 'customer' column:
#      - strip whitespace
#      - convert to title case (e.g. "raj" → "Raj")
#    Store result in 'customer_clean'.
#
# 2. Standardise 'category' to lowercase.
#    Store in place (overwrite the column).
#
# 3. From the 'email' column, extract:
#      - 'email_provider' → the part between @ and .
#        e.g. "raj@gmail.com" → "gmail"
#        Hint: split on "@", take [1], then split on ".", take [0]
#
# 4. Filter df to only rows where description contains
#    the word "Delhi" (case insensitive).
#    Print the result.
#
# 5. Create a column 'customer_id_str' that combines
#    transaction_id and customer_clean like this:
#      "TXN-1001-Raj", "TXN-1002-Priya" etc.
#    Hint: transaction_id is an integer — convert it first.
#
# 6. Find all customers whose cleaned name is longer than 3 characters.
#    Print their names and lengths.
#
# Write your code below this line:
# ─────────────────────────────────────────────────────────────

df = pd.DataFrame({
    "transaction_id": [1001, 1002, 1003, 1004, 1005],
    "customer":       ["  Raj  ", "PRIYA", "amit", "Neha R.", "RAJ"],
    "email":          ["raj@gmail.com", "priya@yahoo.com", "amit@gmail.com",
                       "neha@outlook.com", "raj2@gmail.com"],
    "amount":         [5000.0, 12000.0, 8000.0, 8500.0, 3200.0],
    "category":       ["FOOD", "Travel", "food", "ELECTRONICS", "travel"],
    "description":    ["Food order - Delhi", "Flight Mumbai-Goa",
                       "Grocery Delhi store", "Phone purchase",
                       "Train ticket booking"]
})

df['customer_clean'] = df['customer'].str.strip().str.title()
df['category'] = df['category'].str.lower()
df['email_provider'] = df['email'].str.split("@").str[1].str.split(".").str[0]
print(df[df['description'].str.contains("delhi",case=False)])
df['customer_id_str'] = "TXN-" + df['transaction_id'].astype(str) +"-"+ df['customer_clean']
print(df['customer_id_str'])
df['name_len'] = df['customer_clean'].str.len()
print(df[['customer_clean','name_len']][df['name_len']>3])