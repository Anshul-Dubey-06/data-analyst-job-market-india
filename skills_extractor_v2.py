import pandas as pd
import re
from collections import Counter

# ─────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────
INPUT_FILE  = "naukri_jobs.csv"
OUTPUT_FILE = "skills_analysis.csv"

# ─────────────────────────────────────────
#  SKILLS DICTIONARY — cleaned, no duplicates
# ─────────────────────────────────────────
SKILLS = {
    # Core languages
    "sql", "mysql", "postgresql", "sql server", "oracle sql",
    "python", "r", "scala",

    # BI & Visualisation
    "power bi", "tableau", "looker", "qlikview",
    "excel", "google sheets",

    # Big Data & Cloud
    "spark", "hadoop", "hive", "kafka", "airflow",
    "aws", "azure", "gcp", "databricks", "snowflake",

    # Databases & warehouses
    "mongodb", "cassandra", "redshift", "bigquery",

    # ML & Stats
    "machine learning", "deep learning", "nlp",
    "statistics", "scikit-learn", "tensorflow", "pytorch", "keras",

    # Python libraries
    "pandas", "numpy", "matplotlib", "seaborn", "plotly",

    # Tools
    "git", "jira", "confluence", "docker",
    "etl", "data pipeline", "data warehouse", "data lake",
    "dax", "power query",

    # Domain skills
    "data analysis", "data visualization",
    "data modeling", "data wrangling",
    "data cleaning", "data governance", "data quality",
    "business intelligence", "reporting",
    "dashboard", "kpi", "metrics",
    "communication", "problem solving", "critical thinking",
    "stakeholder management", "presentation",
}

# ─────────────────────────────────────────
#  MERGE RULES — aliases → canonical name
#  Any alias found in text gets counted as
#  the canonical skill instead
# ─────────────────────────────────────────
MERGE_MAP = {
    # bi variants → power bi
    "power bi":              "power bi",
    "bi":                    "power bi",
    "business intelligence": "power bi",

    # data analysis variants
    "data analysis":         "data analysis",
    "data analytics":        "data analysis",
    "analytical":            "data analysis",
    "analytics":             "data analysis",

    # data modeling variants
    "data modeling":         "data modeling",
    "data modelling":        "data modeling",

    # excel variants
    "excel":                 "excel",
    "advanced excel":        "excel",
    "ms excel":              "excel",

    # statistics variants
    "statistics":            "statistics",
    "statistical analysis":  "statistics",

    # git variants
    "git":                   "git",
    "github":                "git",

    # qlik variants
    "qlikview":              "qlikview",
    "qliksense":             "qlikview",
    "qlik":                  "qlikview",
}

# Expand SKILLS to include all aliases
ALL_PATTERNS = set(SKILLS) | set(MERGE_MAP.keys())

# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────

def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).lower()).strip()


def extract_skills_from_text(text: str) -> list[str]:
    text = normalise(text)
    found = set()
    for pattern in ALL_PATTERNS:
        if re.search(r"\b" + re.escape(pattern) + r"\b", text):
            # Map to canonical name if alias, else use as-is
            canonical = MERGE_MAP.get(pattern, pattern)
            # Only keep if canonical is in our main SKILLS set
            if canonical in SKILLS or canonical in MERGE_MAP.values():
                found.add(canonical)
    return list(found)


# ─────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────

df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df)} jobs from {INPUT_FILE}\n")

df["search_text"] = (
    df["skills"].fillna("") + " " +
    df.get("description", pd.Series([""] * len(df))).fillna("") + " " +
    df["title"].fillna("")
)

# ─────────────────────────────────────────
#  COUNT SKILL MENTIONS
# ─────────────────────────────────────────

all_found = []
skill_per_job = []

for _, row in df.iterrows():
    found = extract_skills_from_text(row["search_text"])
    all_found.extend(found)
    skill_per_job.append(", ".join(sorted(found)))

df["extracted_skills"] = skill_per_job

# ─────────────────────────────────────────
#  BUILD FREQUENCY TABLE
# ─────────────────────────────────────────

counts = Counter(all_found)
freq_df = pd.DataFrame(counts.most_common(), columns=["skill", "job_count"])
freq_df["pct_of_jobs"] = (freq_df["job_count"] / len(df) * 100).round(1)

# ─────────────────────────────────────────
#  SAVE
# ─────────────────────────────────────────

df.to_csv(INPUT_FILE, index=False, encoding="utf-8-sig")
freq_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

# ─────────────────────────────────────────
#  PRINT REPORT
# ─────────────────────────────────────────

print("=" * 55)
print(f"  Cleaned Skills Frequency Table  →  {OUTPUT_FILE}")
print("=" * 55)
print(f"\n  {'Skill':<30} {'Jobs':>6}  {'% of postings':>13}")
print(f"  {'-'*30} {'-'*6}  {'-'*13}")
for _, row in freq_df.head(30).iterrows():
    print(f"  {row['skill']:<30} {int(row['job_count']):>6}  {row['pct_of_jobs']:>12.1f}%")

print(f"\n  Key stats:")
def pct(skill):
    r = freq_df[freq_df["skill"] == skill]
    return f"{r['pct_of_jobs'].values[0]:.1f}%" if len(r) else "0.0%"

print(f"  SQL              : {pct('sql')}")
print(f"  Python           : {pct('python')}")
print(f"  Power BI         : {pct('power bi')}")
print(f"  Excel            : {pct('excel')}")
print(f"  Tableau          : {pct('tableau')}")
print(f"  Machine Learning : {pct('machine learning')}")
print(f"  Data Analysis    : {pct('data analysis')}")
print(f"\n  Total unique canonical skills tracked: {len(freq_df)}")
print(f"  Avg skills per job: {freq_df['job_count'].sum() / len(df):.1f}")
