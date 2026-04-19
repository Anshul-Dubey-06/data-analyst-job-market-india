import pandas as pd
import mysql.connector
from mysql.connector import Error

# ─────────────────────────────────────────
#  CONFIG — fill in your password below
# ─────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "Anshul@2106",   # ← replace this
}
DB_NAME    = "naukri_jobs"
TABLE_NAME = "jobs"
INPUT_FILE = "naukri_jobs.csv"

# ─────────────────────────────────────────
#  CONNECT & CREATE DATABASE
# ─────────────────────────────────────────

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("Connected to MySQL successfully!\n")

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")
    print(f"Database '{DB_NAME}' ready.\n")

except Error as e:
    print(f"[!] Connection failed: {e}")
    print("Check your password in the script and make sure MySQL is running.")
    exit()

# ─────────────────────────────────────────
#  LOAD & CLEAN CSV
# ─────────────────────────────────────────

df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df)} rows from {INPUT_FILE}")

# Replace NaN with None (MySQL compatible)
df = df.where(pd.notnull(df), None)

# Shorten any values over 500 chars (safety for TEXT fields)
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].apply(lambda x: x[:500] if isinstance(x, str) else x)

print(f"Columns: {list(df.columns)}\n")

# ─────────────────────────────────────────
#  CREATE TABLE
# ─────────────────────────────────────────

cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")

create_sql = f"""
CREATE TABLE {TABLE_NAME} (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    title           VARCHAR(300),
    company         VARCHAR(300),
    experience      VARCHAR(100),
    salary          VARCHAR(150),
    location        VARCHAR(300),
    skills          TEXT,
    posted          VARCHAR(100),
    job_url         VARCHAR(500),
    scraped_at      VARCHAR(50),
    city            VARCHAR(100),
    salary_min_lpa  FLOAT,
    salary_max_lpa  FLOAT,
    salary_mid_lpa  FLOAT,
    exp_min_yrs     FLOAT,
    exp_max_yrs     FLOAT,
    exp_mid_yrs     FLOAT,
    company_type    VARCHAR(50),
    extracted_skills TEXT,
    search_text     TEXT
)
"""
cursor.execute(create_sql)
print(f"Table '{TABLE_NAME}' created.\n")

# ─────────────────────────────────────────
#  INSERT ROWS
# ─────────────────────────────────────────

cols = [c for c in df.columns]
placeholders = ", ".join(["%s"] * len(cols))
col_names    = ", ".join(cols)
insert_sql   = f"INSERT INTO {TABLE_NAME} ({col_names}) VALUES ({placeholders})"

import math
def clean_val(v):
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    return v

rows = [tuple(clean_val(v) for v in row) for row in df.itertuples(index=False, name=None)]

cursor.executemany(insert_sql, rows)
conn.commit()
print(f"Inserted {cursor.rowcount} rows into '{TABLE_NAME}'.\n")

# ─────────────────────────────────────────
#  QUICK VERIFICATION
# ─────────────────────────────────────────

cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
count = cursor.fetchone()[0]
print(f"Verified: {count} rows in MySQL table.\n")

cursor.execute(f"""
    SELECT city, COUNT(*) as jobs
    FROM {TABLE_NAME}
    GROUP BY city
    ORDER BY jobs DESC
    LIMIT 5
""")
print("Top 5 cities in MySQL:")
for row in cursor.fetchall():
    print(f"  {row[0]:<20} {row[1]} jobs")

cursor.close()
conn.close()

print(f"\nDone! Open MySQL Workbench and connect to database '{DB_NAME}'")
print("Then run your SQL queries on the 'jobs' table.")
