# The Data Analyst Job Market — Decoded 🎯

## The Problem I Was Solving
I was trying to enter the data analyst job market. Instead of 
guessing what skills to learn, I scraped the market itself — 
1,000 real job postings from Naukri.com — to find out exactly 
what employers actually want.

## The Core Insight
Most job seekers learn skills based on YouTube recommendations 
or course curricula. I learned skills based on what 1,000 
hiring managers actually asked for.

## Surprising Findings

### Finding 1 — Power BI beats Tableau 4:1 in India
Power BI appears in 31.5% of postings.
Tableau appears in only 7%.
Most online courses teach Tableau first. The Indian market 
disagrees strongly.

### Finding 2 — Machine Learning is not an analyst skill
ML appears in only 7.5% of data analyst postings.
It's a data scientist requirement, not an analyst one.
Stop learning TensorFlow if you want an analyst job.

### Finding 3 — 590 jobs need neither SQL nor Python
The largest segment of analyst jobs only requires Excel 
and Power BI. There is a huge market for pure BI analysts 
that nobody talks about.

### Finding 4 — Bengaluru is not the only option
Bengaluru has 26% of jobs but Gurugram pays comparably.
Top 3 cities cover 49% of market — Hyderabad and Pune 
are seriously underrated destinations.

### Finding 5 — Salary transparency is broken
Only 10.6% of postings disclosed salary.
The Indian job market has a serious transparency problem 
that hurts both candidates and employers.

## How I Built This

### Step 1 — Scraped 1,000 live job postings
Used Python + Selenium to scrape Naukri.com across 
12 search pages. Naukri blocks simple scrapers — 
had to build a browser automation solution.

### Step 2 — Built a skills extractor
Written string matching across 60+ skills with 
deduplication logic — merging "bi" + "business intelligence" 
+ "power bi" into one canonical skill.

### Step 3 — SQL analysis in MySQL
10 SQL queries covering salary by city, experience 
distribution, company type salary gaps and skill combos.

### Step 4 — Power BI dashboard
6 visuals with insight text boxes — not just charts 
but actual findings.

## The MVP Formula for Skill Priority
If a skill appears in >20% of postings → Must learn
If a skill appears in 10-20% → Should learn
If a skill appears in <5% → Nice to have

## Tools Used
| Tool | Purpose |
|------|---------|
| Python + Selenium | Scraping Naukri.com live data |
| pandas | Cleaning, deduplication, skill extraction |
| MySQL | Storage and SQL analysis |
| Power BI | 6-visual dashboard with insights |

## Key Numbers
- 1,000 job postings scraped
- 55 unique skills tracked
- 12 SQL analysis queries
- 10.6% salary disclosure rate

## Files
| File | Description |
|------|-------------|
| naukri_scraper_v3.py | Selenium scraper — handles JS rendering |
| skills_extractor_v2.py | NLP skill extraction with deduplication |
| load_to_mysql.py | Data cleaning and MySQL loader |
| analysis_queries.sql | 12 SQL queries |
| naukri_jobs.csv | 1,000 scraped job postings |
| skills_analysis.csv | 55 skills with frequency counts |
| dashboard.pdf | Power BI dashboard |

## Interview Answer
"I scraped 1,000 data analyst job postings from Naukri 
to understand what employers actually want. I found Power BI 
appears 4x more than Tableau in India — directly opposite 
to what most online courses teach. SQL appears in 27% of 
postings, Python in 20%. Machine Learning? Only 7.5% — 
it's a data scientist skill, not an analyst skill. 
This project changed how I prioritized my own learning."
