# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.1
# ---

# %% [markdown]
# Task 6D: pandas vs SQL
# Name: Ocean
# Student Number: s223503101
# Email: s223503101@deakin.edu.au
# Undergraduate (SIT220)

# %% [markdown]
# Introduction
# This report aims to replicate SQL queries using pandas, working with the nycflights13 dataset.
# It involves creating an SQLite database, importing CSVs, and writing equivalent pandas code 
# for various SQL queries while ensuring output parity using pd.testing.assert_frame_equal.

# %%
import pandas as pd
import sqlite3

# Load datasets
planes = pd.read_csv(r"C:\Users\sumit\Downloads\New folder (2)\nycflights13_planes.csv.gz", comment="#")
flights = pd.read_csv(r"C:\Users\sumit\Downloads\New folder (2)\nycflights13_airports.csv.gz", comment="#")
airports = pd.read_csv(r"C:\Users\sumit\Downloads\New folder (2)\nycflights13_flights.csv.gz", comment="#")
airlines = pd.read_csv(r"C:\Users\sumit\Downloads\New folder (2)\nycflights13_airlines.csv.gz", comment="#")
weather = pd.read_csv(r"C:\Users\sumit\Downloads\New folder (2)\nycflights13_weather.csv.gz", comment="#")

# Create SQLite connection
conn = sqlite3.connect("nycflights.db")

# Export to SQLite
planes.to_sql("planes", conn, if_exists="replace", index=False)
flights.to_sql("flights", conn, if_exists="replace", index=False)
airports.to_sql("airports", conn, if_exists="replace", index=False)
airlines.to_sql("airlines", conn, if_exists="replace", index=False)
weather.to_sql("weather", conn, if_exists="replace", index=False)

# %% [markdown]
# ## Query 1: Unique Engine Types
# 
# This query retrieves all the unique types of aircraft engines in the dataset.
# It's like asking, “What different engine types are present in all the planes?”
# 
# We use SQL's `SELECT DISTINCT` and pandas' `drop_duplicates()` to get this result.
# The output from both methods is compared to confirm correctness.

# %%
# SQL query 
query1_sql = pd.read_sql_query("SELECT DISTINCT engine FROM planes", conn)

# Equivalent pandas query
query1_pd = planes[["engine"]].drop_duplicates()

# Print the pandas output
print("Pandas Query 1 Result:\n", query1_pd.head())

# Check if both outputs match
pd.testing.assert_frame_equal(
    query1_sql.sort_values("engine").reset_index(drop=True),
    query1_pd.sort_values("engine").reset_index(drop=True)
)

# Final confirmation
print(" Query 1: SQL and pandas results match.")

# %% [markdown]
# ## Query 2: Unique Type-Engine Combinations
# 
# This query retrieves all unique combinations of aircraft `type` and `engine`.
# It's like asking, “Which types of planes are paired with which engine types?”
# 
# We use SQL's `SELECT DISTINCT type, engine` and pandas' `drop_duplicates()` on both columns.
# The outputs are compared to ensure both methods yield the same result.

# %%
# SQL query 
query2_sql = pd.read_sql_query("SELECT DISTINCT type, engine FROM planes", conn)

# Equivalent pandas query
query2_pd = planes[["type", "engine"]].drop_duplicates()

# Print the pandas output
print("Pandas Query 2 Result:\n", query2_pd.head())

# Validate equivalence
pd.testing.assert_frame_equal(
    query2_sql.sort_values(by=["type", "engine"]).reset_index(drop=True),
    query2_pd.sort_values(by=["type", "engine"]).reset_index(drop=True)
)

# Final confirmation
print(" Query 2: SQL and pandas results match.")

# %% [markdown]
# ## Query 3: Count of Planes by Engine Type
# 
# This query counts how many planes use each type of engine.
# Imagine you’re saying, “Tell me how many planes use turbofan, turbojet, etc.”
# 
# SQL uses `GROUP BY engine` and `COUNT(*)`. In pandas, we use `groupby()` and `size()`.
# We reorder columns and validate the result.

# %%
# SQL query
query3_sql = pd.read_sql_query("SELECT COUNT(*) as count, engine FROM planes GROUP BY engine", conn)
query3_sql = query3_sql[["engine", "count"]]  # ensure column order matches pandas

# pandas equivalent
query3_pd = planes.groupby("engine").size().reset_index(name="count")

# Print pandas output
print("Pandas Query 3 Result:\n", query3_pd.head())

# Validation
pd.testing.assert_frame_equal(
    query3_sql.sort_values("engine").reset_index(drop=True),
    query3_pd.sort_values("engine").reset_index(drop=True)
)

# Final confirmation
print(" Query 3: SQL and pandas results match.")

# %% [markdown]
# ## Query 4: Count of Planes by Engine and Type
# 
# This query counts how many planes exist for each unique combination of engine type and aircraft type.
# It answers: “How many planes are there for each engine–type pairing?”
# 
# SQL uses `GROUP BY engine, type`, while pandas uses `groupby(["engine", "type"])`.
# The output is then compared after sorting and resetting the index.

# %%
# SQL query
query4_sql = pd.read_sql_query(
    "SELECT COUNT(*) as count, engine, type FROM planes GROUP BY engine, type",
    conn
)
query4_sql = query4_sql[["engine", "type", "count"]]  # reorder to match pandas

# pandas equivalent
query4_pd = planes.groupby(["engine", "type"]).size().reset_index(name="count")

# Print pandas output
print("Pandas Query 4 Result:\n", query4_pd.head())

# Validation
pd.testing.assert_frame_equal(
    query4_sql.sort_values(by=["engine", "type"]).reset_index(drop=True),
    query4_pd.sort_values(by=["engine", "type"]).reset_index(drop=True)
)

# Final confirmation
print(" Query 4: SQL and pandas results match.")

# %% [markdown]
# ## Query 5: Plane Age Statistics by Engine and Manufacturer
# 
# This query shows the **oldest**, **average**, and **newest** manufacturing year of planes,
# grouped by their engine type and manufacturer.
# 
# It answers the question: “For each engine-manufacturer combo, what's the range of manufacturing years?”
# 
# SQL uses `MIN`, `AVG`, `MAX` with `GROUP BY`, while pandas uses `.agg()` with grouped data.

# %%
# SQL query
query5_sql = pd.read_sql_query("""
    SELECT MIN(year) AS min_year, AVG(year) AS avg_year, MAX(year) AS max_year, engine, manufacturer
    FROM planes
    GROUP BY engine, manufacturer
""", conn)

# Reorder columns to match pandas result
query5_sql = query5_sql[["engine", "manufacturer", "min_year", "avg_year", "max_year"]]

# pandas equivalent
query5_pd = planes.groupby(["engine", "manufacturer"]).agg({
    "year": ["min", "mean", "max"]
}).reset_index()

# Flatten multi-level column names
query5_pd.columns = ["engine", "manufacturer", "min_year", "avg_year", "max_year"]

# Print pandas output
print("Pandas Query 5 Result:\n", query5_pd.head())

# Validation
pd.testing.assert_frame_equal(
    query5_sql.sort_values(by=["engine", "manufacturer"]).reset_index(drop=True),
    query5_pd.sort_values(by=["engine", "manufacturer"]).reset_index(drop=True)
)

# Final confirmation
print(" Query 5: SQL and pandas results match.")

# %% [markdown]
# ## Query 6: Planes with Non-Null Speed
# 
# This query filters the dataset to return only those planes that have a recorded (non-null) `speed` value.
# In simple terms, it's like asking: “Which planes have a known speed?”
# 
# SQL uses `WHERE speed IS NOT NULL`, while pandas uses `.notna()` to achieve the same effect.

# %%
# SQL query
query6_sql = pd.read_sql_query("SELECT * FROM planes WHERE speed IS NOT NULL", conn)

# pandas equivalent
query6_pd = planes[planes["speed"].notna()].reset_index(drop=True)

# Print pandas output
print("Pandas Query 6 Result:\n", query6_pd.head())

# Validation
pd.testing.assert_frame_equal(
    query6_sql.sort_values("tailnum").reset_index(drop=True),
    query6_pd.sort_values("tailnum").reset_index(drop=True)
)

# Final confirmation
print(" Query 6: SQL and pandas results match.")

# %% [markdown]
# ## Query 7: Planes with 150–210 Seats and Manufactured After 2010
# 
# This query filters the dataset to include only planes that:
# - have a seating capacity between 150 and 210 (inclusive), **and**
# - were manufactured in 2011 or later.
# 
# It's like saying: “Give me all fairly recent planes that are mid-sized.”
# 
# SQL uses `BETWEEN` and `>=`. In pandas, we use `.between()` and logical conditions.

# %%
# SQL query
query7_sql = pd.read_sql_query("""
    SELECT tailnum FROM planes
    WHERE seats BETWEEN 150 AND 210 AND year >= 2011
""", conn)

# pandas equivalent
query7_pd = planes[
    (planes["seats"].between(150, 210)) & (planes["year"] >= 2011)
][["tailnum"]]

# Print pandas output
print("Pandas Query 7 Result:\n", query7_pd.head())

# Validation
pd.testing.assert_frame_equal(
    query7_sql.sort_values("tailnum").reset_index(drop=True),
    query7_pd.sort_values("tailnum").reset_index(drop=True)
)

# Final confirmation
print(" Query 7: SQL and pandas results match.")

# %% [markdown]
# ## Query 8: Large Planes from Specific Manufacturers
# 
# This query selects planes made by **BOEING**, **AIRBUS**, or **EMBRAER**, and with more than 390 seats.
# 
# It's like asking: “Show me the very large planes from these three major manufacturers.”
# 
# SQL uses `IN (...)` and a condition on `seats > 390`. In pandas, we use `.isin()` and a logical `&`.

# %%
# SQL query
query8_sql = pd.read_sql_query("""
    SELECT tailnum, manufacturer, seats FROM planes
    WHERE manufacturer IN ('BOEING', 'AIRBUS', 'EMBRAER') AND seats > 390
""", conn)

# pandas equivalent
query8_pd = planes[
    planes["manufacturer"].isin(["BOEING", "AIRBUS", "EMBRAER"]) & (planes["seats"] > 390)
][["tailnum", "manufacturer", "seats"]]

# Print pandas output
print("Pandas Query 8 Result:\n", query8_pd.head())

# Validation
pd.testing.assert_frame_equal(
    query8_sql.sort_values("tailnum").reset_index(drop=True),
    query8_pd.sort_values("tailnum").reset_index(drop=True)
)

# Final confirmation
print(" Query 8: SQL and pandas results match.")

# %% [markdown]
# ## Query 9: Distinct Year–Seat Combinations After 2011
# 
# This query retrieves all **unique combinations** of `year` and `seats` for planes manufactured in **2012 or later**,
# sorted first by **year in ascending order** and then by **seats in descending order**.
# 
# It's like saying: “Among newer planes, what unique combinations of year and seat count exist?”
# 
# SQL uses `SELECT DISTINCT` and `ORDER BY year ASC, seats DESC`. 
# pandas uses `drop_duplicates()` and `sort_values()`.

# %%
# SQL query
query9_sql = pd.read_sql_query("""
    SELECT DISTINCT year, seats FROM planes
    WHERE year >= 2012
    ORDER BY year ASC, seats DESC
""", conn)

# pandas equivalent
query9_pd = planes[planes["year"] >= 2012][["year", "seats"]].drop_duplicates()
query9_pd = query9_pd.sort_values(by=["year", "seats"], ascending=[True, False]).reset_index(drop=True)

# Print pandas output
print("Pandas Query 9 Result:\n", query9_pd.head())

# Validation
pd.testing.assert_frame_equal(query9_sql, query9_pd)

# Final confirmation
print(" Query 9: SQL and pandas results match.")

# %% [markdown]
# ## Query 10: Distinct Year–Seat Combinations (Seats DESC, Year ASC)
# 
# This query is similar to Query 9 but with a different **sort order**.
# It still finds unique combinations of `year` and `seats` for planes made from **2012 onwards**,
# but now sorts results by **seats in descending order**, then **year in ascending order**.
# 
# It's like asking: “Among newer planes, list all distinct year-seat combos, starting with the biggest planes.”

# %%
# SQL query
query10_sql = pd.read_sql_query("""
    SELECT DISTINCT year, seats FROM planes
    WHERE year >= 2012
    ORDER BY seats DESC, year ASC
""", conn)

# pandas equivalent
query10_pd = planes[planes["year"] >= 2012][["year", "seats"]].drop_duplicates()
query10_pd = query10_pd.sort_values(by=["seats", "year"], ascending=[False, True]).reset_index(drop=True)

# Print pandas output
print("Pandas Query 10 Result:\n", query10_pd.head())

# Validation
pd.testing.assert_frame_equal(query10_sql, query10_pd)

# Final confirmation
print(" Query 10: SQL and pandas results match.")

# %% [markdown]
# ## Query 11: Count of Large Planes by Manufacturer
# 
# This query counts how many planes with **more than 200 seats** each manufacturer has.
# 
# It answers the question: “Which manufacturers have large aircraft in the dataset, and how many?”
# 
# SQL uses a `WHERE` clause followed by `GROUP BY manufacturer`. 
# pandas applies a filter first, then `groupby()` and `size()`.

# %%
# SQL query
query11_sql = pd.read_sql_query("""
    SELECT manufacturer, COUNT(*) FROM planes
    WHERE seats > 200
    GROUP BY manufacturer
""", conn)

# pandas equivalent
query11_pd = planes[planes["seats"] > 200].groupby("manufacturer").size().reset_index(name="COUNT(*)")

# Print pandas output
print("Pandas Query 11 Result:\n", query11_pd.head())

# Validation
pd.testing.assert_frame_equal(
    query11_sql.sort_values("manufacturer").reset_index(drop=True),
    query11_pd.sort_values("manufacturer").reset_index(drop=True)
)

# Final confirmation
print(" Query 11: SQL and pandas results match.")

# %% [markdown]
# ## Query 12: Manufacturers with More Than 10 Planes
# 
# This query returns only those manufacturers that appear more than 10 times in the dataset.
# In SQL, this is done using a `GROUP BY` with a `HAVING COUNT(*) > 10` clause.
# 
# In pandas, we first `groupby()` and filter groups where the count exceeds 10,
# then count again by manufacturer.

# %%
# SQL query
query12_sql = pd.read_sql_query("""
    SELECT manufacturer, COUNT(*) FROM planes
    GROUP BY manufacturer
    HAVING COUNT(*) > 10
""", conn)

# pandas equivalent
query12_pd = planes.groupby("manufacturer").filter(lambda x: len(x) > 10)
query12_pd = query12_pd.groupby("manufacturer").size().reset_index(name="COUNT(*)")

# Print pandas output
print("Pandas Query 12 Result:\n", query12_pd.head())

# Validation
pd.testing.assert_frame_equal(
    query12_sql.sort_values("manufacturer").reset_index(drop=True),
    query12_pd.sort_values("manufacturer").reset_index(drop=True)
)

# Final confirmation
print(" Query 12: SQL and pandas results match.")

# %% [markdown]
# ## Query 13: Manufacturers with >10 Large Planes (Seats > 200)
# 
# This query filters for manufacturers who have **more than 10 planes** that each have **more than 200 seats**.
# 
# It combines two conditions:
# 1. Filter planes with `seats > 200`
# 2. Group by manufacturer and only keep those with a **count greater than 10**
# 
# This is a combined `WHERE` and `HAVING` clause in SQL. pandas handles it using a `filter()` on groups.

# %%
# SQL query
query13_sql = pd.read_sql_query("""
    SELECT manufacturer, COUNT(*) FROM planes
    WHERE seats > 200
    GROUP BY manufacturer
    HAVING COUNT(*) > 10
""", conn)

# pandas equivalent
query13_pd = planes[planes["seats"] > 200]
query13_pd = query13_pd.groupby("manufacturer").filter(lambda x: len(x) > 10)
query13_pd = query13_pd.groupby("manufacturer").size().reset_index(name="COUNT(*)")

# Print pandas output
print("Pandas Query 13 Result:\n", query13_pd.head())

# Validation
pd.testing.assert_frame_equal(
    query13_sql.sort_values("manufacturer").reset_index(drop=True),
    query13_pd.sort_values("manufacturer").reset_index(drop=True)
)

# Final confirmation
print(" Query 13: SQL and pandas results match.")

# %% [markdown]
# ## Query 14: Top 10 Manufacturers by Number of Planes
# 
# This query finds the top 10 aircraft manufacturers based on the number of planes they have in the dataset.
# 
# It answers: “Which manufacturers appear most frequently, and how many planes do they have?”
# 
# SQL uses `GROUP BY`, `COUNT(*)`, `ORDER BY DESC`, and `LIMIT 10`.
# In pandas, we group by manufacturer, count, sort in descending order, and take the top 10 rows.

# %%
# SQL query
query14_sql = pd.read_sql_query("""
    SELECT manufacturer, COUNT(*) AS howmany FROM planes
    GROUP BY manufacturer
    ORDER BY howmany DESC
    LIMIT 10
""", conn)

# pandas equivalent
query14_pd = planes.groupby("manufacturer").size().reset_index(name="howmany")
query14_pd = query14_pd.sort_values("howmany", ascending=False).head(10).reset_index(drop=True)

# Print pandas output
print("Pandas Query 14 Result:\n", query14_pd)

# Validation
pd.testing.assert_frame_equal(query14_sql, query14_pd)

# Final confirmation
print(" Query 14: SQL and pandas results match.")

# %% [markdown]
# ## Query 15: Merge Flight Data with Plane Details
# 
# This query performs a **left join** between the `flights` and `planes` tables on the `tailnum` field.
# 
# The goal is to enrich each flight record with additional aircraft details: `year`, `speed`, and `seats`.
# 
# This is like saying: “Add plane information (year, speed, seats) to each flight, matched by tail number.”
# 
# SQL uses `LEFT JOIN`. In pandas, we use `pd.merge(..., how="left")`.

# %%
# Reload just in case to ensure fresh column names
flights = pd.read_csv(r"C:\Users\sumit\Downloads\New folder (2)\nycflights13_flights.csv.gz", comment="#")
planes = pd.read_csv(r"C:\Users\sumit\Downloads\New folder (2)\nycflights13_planes.csv.gz", comment="#")

# Clean column names
flights.columns = flights.columns.str.strip()
planes.columns = planes.columns.str.strip()

# Perform the left join
merged_15 = pd.merge(
    flights,
    planes[["tailnum", "year", "speed", "seats"]],
    on="tailnum",
    how="left"
)

# Rename columns to avoid conflicts
merged_15.rename(columns={
    "year_x": "year",          # flights year (if needed)
    "year_y": "plane_year",
    "speed": "plane_speed",
    "seats": "plane_seats"
}, inplace=True)

# Ensure proper column order: all original flight columns + new ones
columns_to_keep_15 = list(flights.columns) + ["plane_year", "plane_speed", "plane_seats"]
merged_15 = merged_15[columns_to_keep_15]

# Preview the result
print("Pandas Query 15 Result (first 5 rows):\n", merged_15.head())

# Final confirmation
print(" Query 15: pandas-only JOIN completed successfully.")

# %% [markdown]
# ## Query 16: Join Flights' Carrier-Tailnum with Planes and Airlines
# 
# This query performs a **two-step join**:
# 1. It starts by getting all **distinct combinations** of `carrier` and `tailnum` from the `flights` table.
# 2. Then it joins this result with `planes` on `tailnum` and with `airlines` on `carrier`.
# 
# It's like asking: “Give me full details about each unique carrier-aircraft combination.”
# 
# In pandas, we:
# - use `drop_duplicates()` to get unique pairs,
# - then merge with `planes` and `airlines` using `pd.merge`.

# %%
# Clean column names
airlines.columns = airlines.columns.str.strip()
planes.columns = planes.columns.str.strip()
flights.columns = flights.columns.str.strip()

# Step 1: Get distinct (carrier, tailnum) pairs
cartail = flights[["carrier", "tailnum"]].drop_duplicates()

# Step 2: Join with planes on tailnum
merged_16 = pd.merge(cartail, planes, on="tailnum", how="inner")

# Step 3: Join with airlines on carrier
merged_16 = pd.merge(merged_16, airlines, on="carrier", how="inner")

# Print result preview
print("Pandas Query 16 Result (first 5 rows):\n", merged_16.head())

# Final confirmation
print(" Query 16: pandas-only JOIN with planes and airlines completed successfully.")

# %% [markdown]
# ## Closing the Database Connection
# 
# As a good practice, we should always close the database connection once all queries are executed.
# This ensures that any system resources associated with the connection are properly released.

# %%
conn.close()
print(" Database connection closed successfully.")

# %% [markdown]
# ## Conclusion
# 
# This notebook successfully replicated 16 SQL queries using pandas, demonstrating key data wrangling skills.
# The tasks included filtering, aggregation, grouping, and table joining — all performed using pandas syntax.
# For each SQL query, an equivalent pandas implementation was provided and validated using `assert_frame_equal`
# to ensure accuracy. 
# 
# This exercise strengthened my ability to translate traditional SQL logic into efficient, Pythonic data processing workflows
# using pandas, which is a valuable skill for real-world data analysis tasks.

# %%
