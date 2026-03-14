# Pandas Complete Notes — Data Engineer Interview Prep

---

## 1. The Basics — Series & DataFrame

A **DataFrame** is a table. A **Series** is a single column.

```python
import pandas as pd

df = pd.DataFrame({
    'name':   ['Alice', 'Bob', 'Charlie'],
    'age':    [25, 30, 35],
    'salary': [50000, 60000, 70000]
})

df.head()       # first 5 rows
df.tail()       # last 5 rows
df.info()       # column types and null counts
df.describe()   # statistical summary
df.dtypes       # data types of each column
df.shape        # (rows, columns)
```

---

## 2. Reading & Writing Data

```python
# Read
df = pd.read_csv('data.csv')
df = pd.read_excel('data.xlsx')
df = pd.read_json('data.json')
df = pd.read_parquet('data.parquet')

import sqlite3
conn = sqlite3.connect('mydb.db')
df = pd.read_sql('SELECT * FROM users', conn)

# Write
df.to_csv('output.csv', index=False)
df.to_parquet('output.parquet')
df.to_json('output.json', orient='records')
df.to_sql('table_name', conn, if_exists='replace', index=False)
# if_exists options: 'replace', 'append', 'fail'

# Chunking — for large files that don't fit in memory
chunks = []
for chunk in pd.read_csv('huge_file.csv', chunksize=100_000):
    chunk = chunk[chunk['status'] == 'delivered']
    chunks.append(chunk)
df = pd.concat(chunks, ignore_index=True)
```

---

## 3. Selecting & Filtering Data

```python
# Select columns
df['name']                    # single column → Series
df[['name', 'salary']]        # multiple columns → DataFrame

# Filter rows
df[df['age'] > 28]
df[(df['age'] > 28) & (df['salary'] > 55000)]   # AND
df[(df['age'] > 28) | (df['salary'] > 55000)]   # OR

# loc — label based
df.loc[0, 'name']
df.loc[df['age'] > 28, 'name']

# iloc — position based
df.iloc[0]        # first row
df.iloc[0:3]      # first 3 rows
df.iloc[0, 1]     # row 0, column 1

# String filtering
df[df['name'].str.contains('Ali')]
df[df['name'].str.startswith('A')]
df[df['name'].str.lower() == 'alice']

# Sorting
df.sort_values('salary', ascending=False)
df.nlargest(3, 'salary')
df.nsmallest(3, 'salary')
```

### SQL → Pandas cheat sheet

| SQL | Pandas |
|---|---|
| `SELECT col` | `df['col']` |
| `SELECT col1, col2` | `df[['col1', 'col2']]` |
| `WHERE age > 28` | `df[df['age'] > 28]` |
| `LIMIT 5` | `df.head(5)` |
| `ORDER BY salary DESC` | `df.sort_values('salary', ascending=False)` |

---

## 4. Transforming Data

```python
# Add new column
df['salary_k'] = df['salary'] / 1000

# Apply a function to a column (use sparingly — slow on large data)
df['name_upper'] = df['name'].apply(lambda x: x.upper())

# String methods
df['name'].str.lower()
df['name'].str.upper()
df['name'].str.contains('Ali')
df['name'].str.replace('Alice', 'Alicia')
df['name'].str.strip()           # remove whitespace

# Rename columns
df.rename(columns={'salary': 'annual_salary'}, inplace=True)

# Drop columns
df.drop(columns=['col1', 'col2'], inplace=True)
```

---

## 5. Groupby & Aggregation

Equivalent to SQL's `GROUP BY`.

```python
# Single aggregation
df.groupby('department')['salary'].mean()
df.groupby('department')['salary'].sum()
df.groupby('department')['salary'].count()
df.groupby('department')['salary'].max()
df.groupby('department')['salary'].min()

# Multiple aggregations at once
df.groupby('department').agg(
    avg_salary  = ('salary', 'mean'),
    headcount   = ('name', 'count'),
    max_salary  = ('salary', 'max'),
    total_spend = ('salary', 'sum')
)

# Group by multiple columns
df.groupby(['department', 'location'])['salary'].mean()

# Filter after aggregation
df.groupby('department')['salary'].sum().query('salary > 100000')
```

---

## 6. Merging & Joining

Equivalent to SQL's `JOIN`.

```python
# Inner join (default)
pd.merge(df1, df2, on='user_id')

# Left join
pd.merge(df1, df2, on='user_id', how='left')

# Right join
pd.merge(df1, df2, on='user_id', how='right')

# Full outer join
pd.merge(df1, df2, on='user_id', how='outer')

# Different column names in each table
pd.merge(df1, df2, left_on='dept_id', right_on='department_id')

# Join on multiple columns
pd.merge(df1, df2, on=['country', 'year'])
```

### SQL → Pandas join cheat sheet

| SQL | Pandas |
|---|---|
| `INNER JOIN` | `how='inner'` (default) |
| `LEFT JOIN` | `how='left'` |
| `RIGHT JOIN` | `how='right'` |
| `FULL OUTER JOIN` | `how='outer'` |
| `ON t1.a = t2.b` | `left_on='a', right_on='b'` |

---

## 7. Data Types & Schema Enforcement *(DE Critical)*

```python
# Check types
df.dtypes

# Cast types
df['age']         = df['age'].astype('int64')
df['salary']      = df['salary'].astype('float64')
df['is_active']   = df['is_active'].astype('bool')
df['name']        = df['name'].astype('str')

# Convert to datetime
df['date'] = pd.to_datetime(df['date'])
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')   # known format
df['date'] = pd.to_datetime(df['date'], format='mixed')       # mixed formats

# Schema validation function (write this in every pipeline)
def validate_schema(df):
    expected = {
        'user_id':   'int64',
        'salary':    'float64',
        'join_date': 'datetime64[ns]',
        'active':    'bool'
    }
    for col, dtype in expected.items():
        if col not in df.columns:
            print(f"MISSING: {col}")
        elif str(df[col].dtype) != dtype:
            print(f"WRONG TYPE: {col} → got {df[col].dtype}, expected {dtype}")
        else:
            print(f"OK: {col}")
```

> **Key rule:** `astype('int')` produces `int64` by default. Always match your expected dtype string exactly.

---

## 8. Handling Nulls *(DE Critical)*

```python
# Understand nulls
df.isnull().sum()              # null count per column
df.isnull().mean() * 100       # null % per column
df[df.isnull().any(axis=1)]    # rows with any null

# Drop rows where critical columns are null
df = df.dropna(subset=['user_id', 'order_id'])  # can pass multiple columns

# Fill strategies
df['country'] = df['country'].fillna('Unknown')           # fixed value
df['salary']  = df['salary'].fillna(df['salary'].median()) # global median

# Fill with per-group median — the DE-level move
df['salary'] = df.groupby('department')['salary'].transform(
    lambda x: x.fillna(x.median())
)
# Fallback to global median if still null
df['salary'] = df['salary'].fillna(df['salary'].median())

# Time series fills
df['price'] = df['price'].ffill()   # forward fill (carry last value forward)
df['price'] = df['price'].bfill()   # backward fill

# Null check function
def check_nulls(df):
    total = df.isnull().sum().sum()
    if total == 0:
        print("No nulls remaining ✓")
        return True
    print(df.isnull().sum())
    return False
```

---

## 9. Deduplication *(DE Critical)*

```python
# Check duplicates
df.duplicated().sum()
df.duplicated(subset=['user_id']).sum()

# Drop exact duplicates
df = df.drop_duplicates()

# Drop based on specific columns
df = df.drop_duplicates(subset=['user_id', 'order_id'])

# Keep most recent record per user — most common DE interview pattern
df['updated_at'] = pd.to_datetime(df['updated_at'])

df = (
    df.sort_values('updated_at', ascending=False)
      .drop_duplicates(subset=['user_id'], keep='first')
      .reset_index(drop=True)
)

# Keep top-N records per group (ranking approach — more flexible)
df['rank'] = df.groupby('user_id')['updated_at'].rank(
    ascending=False, method='dense'
).astype(int)

df = (
    df[df['rank'] <= 1]             # change to <= 3 for top-3
      .drop_duplicates(subset=['user_id', 'updated_at'])
      .drop(columns=['rank'])
      .reset_index(drop=True)
)
```

> **Key pattern:** sort → drop_duplicates(keep='first') is the standard dedup move. Always `reset_index(drop=True)` after.

---

## 10. Window Functions *(DE High Priority)*

Unlike `groupby` which collapses rows, window functions **keep all rows** and calculate per-row within a group.

```python
# Rank within group (SQL: RANK() OVER (PARTITION BY dept ORDER BY salary DESC))
df['rank'] = df.groupby('department')['salary'].rank(
    ascending=False, method='dense'
).astype(int)
# method options: 'dense' (no gaps), 'min', 'average', 'first'

# Max/min/mean within group without collapsing rows (SQL: MAX() OVER PARTITION BY)
df['dept_max_salary'] = df.groupby('department')['salary'].transform('max')
df['dept_avg_salary'] = df.groupby('department')['salary'].transform('mean')

# Difference from group max
df['diff_from_top'] = df.groupby('department')['salary'].transform('max') - df['salary']

# Shift — previous row value within group (SQL: LAG())
df = df.sort_values(['department', 'salary'])
df['prev_salary'] = df.groupby('department')['salary'].shift(1)

# Lead — next row value (SQL: LEAD())
df['next_salary'] = df.groupby('department')['salary'].shift(-1)

# Rolling average (SQL: AVG() OVER (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW))
df['rolling_avg'] = df['sales'].rolling(window=3).mean()

# Cumulative sum
df['running_total'] = df['sales'].cumsum()
df['running_total_by_dept'] = df.groupby('department')['sales'].cumsum()
```

---

## 11. Performance — apply vs vectorization *(DE Important)*

Always prefer vectorized operations over `apply()` on large data.

```python
# SLOW — apply loops row by row
df['tax'] = df['salary'].apply(lambda x: x * 0.3 if x > 50000 else x * 0.2)

# FAST — np.where (vectorized, like SQL CASE WHEN)
import numpy as np
df['tax'] = np.where(df['salary'] > 50000, df['salary'] * 0.3, df['salary'] * 0.2)

# Multiple conditions — nested np.where (like SQL CASE WHEN ... WHEN ... ELSE)
df['level'] = np.where(df['salary'] > 80000, 'Senior',
              np.where(df['salary'] > 50000, 'Mid', 'Junior'))

# FASTEST — pure vectorized math when no condition needed
df['salary_inr'] = df['salary'] * 83
```

> **Rule of thumb:** if you can express it as math or `np.where`, never use `apply`.

---

## Practice Questions

### Analyst level

**Q1.** Given an orders DataFrame with columns `order_id`, `customer`, `amount`, `status` — find the total amount spent by each customer on delivered orders only. Sort highest to lowest.

**Q2.** Given an employees and departments DataFrame — get all employees and their department name. Employees with no matching department should show NaN.

**Q3.** Given a products DataFrame with `product`, `price`, `in_stock` — get names and prices of all Apple products that are in stock, sorted by price lowest to highest.

**Q4.** Given a DataFrame with `city`, `category`, `revenue`, `orders` — for each city find total revenue, total orders, and average revenue per order (rounded to 2 decimal places).

**Q5.** Given orders and customers DataFrames — find total amount spent per customer on delivered orders only, show customer name not ID, only customers who spent more than $300, sorted highest first.

**Q6.** Given a DataFrame with `date`, `product`, `sales`, `returns` — convert date to datetime, add a `net_sales` column (sales - returns), find the product with the highest total net sales, print just the product name as a string.

---

### Data Engineer level

**Q7.** A DataFrame arrives with all columns as strings. Cast `user_id` to int, `salary` to float, `joining_date` to datetime (mixed formats), `is_active` to bool. Write a schema validation function to verify the types.

**Q8.** Given an orders DataFrame with nulls in `amount`, `country`, and `status` — drop rows where primary key columns are null, fill missing amount with per-user median (fallback to global median), fill missing country with 'Unknown', drop rows where status is null.

**Q9.** Given a users DataFrame with duplicate records per user — keep only the most recent record per user, handle ties (same updated_at), reset the index.

**Q10.** Given an employees DataFrame — add a `rank` column (1 = highest paid per department), add `salary_diff_from_top` column, add `prev_salary` column (previous employee's salary within department ordered ascending).

---

## Quick Reference — The DE Pipeline Checklist

Every time data lands in your pipeline, do this in order:

```python
# 1. Understand the data
df.shape
df.dtypes
df.isnull().sum()
df.duplicated().sum()
df.head()

# 2. Fix types
df['date']   = pd.to_datetime(df['date'], format='mixed')
df['amount'] = df['amount'].astype('float64')

# 3. Handle nulls
df = df.dropna(subset=['primary_key_col'])
df['col'] = df.groupby('group')['col'].transform(lambda x: x.fillna(x.median()))
df['col'] = df['col'].fillna(df['col'].median())

# 4. Deduplicate
df = (df.sort_values('updated_at', ascending=False)
        .drop_duplicates(subset=['id'], keep='first')
        .reset_index(drop=True))

# 5. Validate
validate_schema(df)
check_nulls(df)

# 6. Write output
df.to_parquet('output.parquet')
```
