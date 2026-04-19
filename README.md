# Data Analyst Job Market India — 2026

## Overview
Scraped 1,000 real data analyst job postings from Naukri.com 
to decode what Indian employers actually want in 2026.

## Key Findings
- Power BI (31.5%) is more demanded than Tableau (7%) — a 4x gap
- SQL (27%) + Python (20%) are the core technical stack
- Bengaluru accounts for 26% of all openings
- Top 3 cities cover nearly 50% of the entire market
- Only 10.6% of postings disclose salary
- 590 jobs require neither SQL nor Python — Excel/Power BI only roles
- Staffing firms post more jobs than product companies

## Tools Used
| Tool | Purpose |
|------|---------|
| Python + Selenium | Scraping Naukri.com |
| pandas | Data cleaning |
| MySQL | Data storage & SQL analysis |
| Power BI | Dashboard & visualization |

## Project Structure
| File | Description |
|------|-------------|
| naukri_scraper_v3.py | Selenium scraper for Naukri.com |
| skills_extractor_v2.py | NLP skills frequency analysis |
| load_to_mysql.py | Data cleaning & MySQL loader |
| analysis_queries.sql | 12 SQL analysis queries |
| naukri_jobs.csv | Raw scraped dataset (1000 rows) |
| skills_analysis.csv | Skills frequency table (55 skills) |
| dashboard.pdf | Power BI dashboard export |

## How to Run
1. Install dependencies:
pip install selenium webdriver-manager pandas mysql-connector-python

2. Run scraper:
python naukri_scraper_v3.py

3. Extract skills:
python skills_extractor_v2.py

4. Load to MySQL:
python load_to_mysql.py

5. Open analysis_queries.sql in MySQL Workbench

6. Open dashboard.pdf to view the Power BI dashboard

## Dashboard Preview
[View Dashboard PDF](dashboard.pdf)
