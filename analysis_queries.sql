-- ============================================================
--  PROJECT 1: Data Analyst Job Market Analysis
--  Database: naukri_jobs | Table: jobs
--  Run these queries in MySQL Workbench one section at a time
-- ============================================================
create database naukri_jobs;

SHOW DATABASES;
USE naukri_jobs;
SHOW TABLES;
-- ────────────────────────────────────────────────────────────
--  Q1: Which cities have the most data analyst jobs?
-- ────────────────────────────────────────────────────────────
SELECT 
    city,
    COUNT(*) AS total_jobs,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM jobs), 1) AS pct_of_market
FROM jobs
WHERE city NOT IN ('Unknown', 'Pan India')
GROUP BY city
ORDER BY total_jobs DESC
LIMIT 10;


-- ────────────────────────────────────────────────────────────
--  Q2: Which cities pay the most? (avg mid salary in LPA)
-- ────────────────────────────────────────────────────────────
SELECT 
    city,
    ROUND(AVG(salary_mid_lpa), 1)   AS avg_salary_lpa,
    ROUND(MIN(salary_min_lpa), 1)   AS min_salary_lpa,
    ROUND(MAX(salary_max_lpa), 1)   AS max_salary_lpa,
    COUNT(*)                         AS jobs_with_salary
FROM jobs
WHERE salary_mid_lpa IS NOT NULL
  AND city NOT IN ('Unknown', 'Pan India')
GROUP BY city
HAVING jobs_with_salary >= 3
ORDER BY avg_salary_lpa DESC
LIMIT 10;


-- ────────────────────────────────────────────────────────────
--  Q3: Experience distribution — what level do most jobs want?
-- ────────────────────────────────────────────────────────────
SELECT 
    CASE
        WHEN exp_mid_yrs < 2  THEN '0-2 yrs  (Fresher)'
        WHEN exp_mid_yrs < 5  THEN '2-5 yrs  (Junior)'
        WHEN exp_mid_yrs < 9  THEN '5-9 yrs  (Mid-level)'
        WHEN exp_mid_yrs >= 9 THEN '9+ yrs   (Senior)'
    END AS experience_band,
    COUNT(*) AS job_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM jobs WHERE exp_mid_yrs IS NOT NULL), 1) AS pct
FROM jobs
WHERE exp_mid_yrs IS NOT NULL
GROUP BY experience_band
ORDER BY job_count DESC;


-- ────────────────────────────────────────────────────────────
--  Q4: Does more experience = higher salary?
-- ────────────────────────────────────────────────────────────
SELECT 
    CASE
        WHEN exp_mid_yrs < 2  THEN '0-2 yrs'
        WHEN exp_mid_yrs < 5  THEN '2-5 yrs'
        WHEN exp_mid_yrs < 9  THEN '5-9 yrs'
        WHEN exp_mid_yrs >= 9 THEN '9+ yrs'
    END AS experience_band,
    ROUND(AVG(salary_mid_lpa), 1) AS avg_salary_lpa,
    COUNT(*) AS jobs_with_both
FROM jobs
WHERE exp_mid_yrs IS NOT NULL
  AND salary_mid_lpa IS NOT NULL
GROUP BY experience_band
ORDER BY avg_salary_lpa DESC;


-- ────────────────────────────────────────────────────────────
--  Q5: Top 20 hiring companies
-- ────────────────────────────────────────────────────────────
SELECT 
    company,
    COUNT(*)        AS job_postings,
    company_type,
    GROUP_CONCAT(DISTINCT city ORDER BY city SEPARATOR ', ') AS cities_hiring
FROM jobs
WHERE company != ''
GROUP BY company, company_type
ORDER BY job_postings DESC
LIMIT 20;


-- ────────────────────────────────────────────────────────────
--  Q6: IT Services vs Product companies — salary gap
-- ────────────────────────────────────────────────────────────
SELECT 
    company_type,
    COUNT(*)                          AS total_jobs,
    SUM(CASE WHEN salary_mid_lpa IS NOT NULL THEN 1 ELSE 0 END) AS jobs_with_salary,
    ROUND(AVG(salary_mid_lpa), 1)     AS avg_salary_lpa,
    ROUND(MIN(salary_min_lpa), 1)     AS min_salary_lpa,
    ROUND(MAX(salary_max_lpa), 1)     AS max_salary_lpa
FROM jobs
WHERE company_type != 'Unknown'
GROUP BY company_type
ORDER BY avg_salary_lpa DESC;


-- ────────────────────────────────────────────────────────────
--  Q7: Remote vs Office jobs
-- ────────────────────────────────────────────────────────────
SELECT
    CASE 
        WHEN LOWER(location) LIKE '%remote%' THEN 'Remote'
        WHEN LOWER(location) LIKE '%hybrid%' THEN 'Hybrid'
        ELSE 'On-site'
    END AS work_mode,
    COUNT(*) AS jobs,
    ROUND(AVG(salary_mid_lpa), 1) AS avg_salary_lpa
FROM jobs
GROUP BY work_mode
ORDER BY jobs DESC;


-- ────────────────────────────────────────────────────────────
--  Q8: Which skills command the highest salaries?
-- ────────────────────────────────────────────────────────────
SELECT 
    'SQL'             AS skill, ROUND(AVG(salary_mid_lpa), 1) AS avg_lpa, COUNT(*) AS jobs
FROM jobs WHERE extracted_skills LIKE '%sql%' AND salary_mid_lpa IS NOT NULL
UNION ALL
SELECT 'Python',      ROUND(AVG(salary_mid_lpa), 1), COUNT(*)
FROM jobs WHERE extracted_skills LIKE '%python%' AND salary_mid_lpa IS NOT NULL
UNION ALL
SELECT 'Power BI',    ROUND(AVG(salary_mid_lpa), 1), COUNT(*)
FROM jobs WHERE extracted_skills LIKE '%power bi%' AND salary_mid_lpa IS NOT NULL
UNION ALL
SELECT 'Tableau',     ROUND(AVG(salary_mid_lpa), 1), COUNT(*)
FROM jobs WHERE extracted_skills LIKE '%tableau%' AND salary_mid_lpa IS NOT NULL
UNION ALL
SELECT 'Machine Learning', ROUND(AVG(salary_mid_lpa), 1), COUNT(*)
FROM jobs WHERE extracted_skills LIKE '%machine learning%' AND salary_mid_lpa IS NOT NULL
UNION ALL
SELECT 'Excel',       ROUND(AVG(salary_mid_lpa), 1), COUNT(*)
FROM jobs WHERE extracted_skills LIKE '%excel%' AND salary_mid_lpa IS NOT NULL
UNION ALL
SELECT 'Azure',       ROUND(AVG(salary_mid_lpa), 1), COUNT(*)
FROM jobs WHERE extracted_skills LIKE '%azure%' AND salary_mid_lpa IS NOT NULL
UNION ALL
SELECT 'Snowflake',   ROUND(AVG(salary_mid_lpa), 1), COUNT(*)
FROM jobs WHERE extracted_skills LIKE '%snowflake%' AND salary_mid_lpa IS NOT NULL
ORDER BY avg_lpa DESC;


-- ────────────────────────────────────────────────────────────
--  Q9: SQL + Python combo — how common and does it pay more?
-- ────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN extracted_skills LIKE '%sql%' AND extracted_skills LIKE '%python%' THEN 'SQL + Python'
        WHEN extracted_skills LIKE '%sql%' AND extracted_skills NOT LIKE '%python%' THEN 'SQL only'
        WHEN extracted_skills NOT LIKE '%sql%' AND extracted_skills LIKE '%python%' THEN 'Python only'
        ELSE 'Neither'
    END AS skill_combo,
    COUNT(*) AS jobs,
    ROUND(AVG(salary_mid_lpa), 1) AS avg_salary_lpa
FROM jobs
GROUP BY skill_combo
ORDER BY jobs DESC;


-- ────────────────────────────────────────────────────────────
--  Q10: Fresher-friendly jobs (0-2 yrs experience required)
-- ────────────────────────────────────────────────────────────
SELECT 
    title,
    company,
    city,
    salary,
    extracted_skills
FROM jobs
WHERE exp_max_yrs <= 2
  AND city NOT IN ('Unknown')
ORDER BY 
    CASE WHEN salary_mid_lpa IS NOT NULL THEN 0 ELSE 1 END,
    salary_mid_lpa DESC
LIMIT 20;

-- Query 11: Which companies hire the most freshers?
SELECT 
    company,
    COUNT(*) AS fresher_jobs,
    company_type
FROM jobs
WHERE exp_max_yrs <= 2
  AND company != ''
GROUP BY company, company_type
ORDER BY fresher_jobs DESC
LIMIT 10;


-- Query 12: SQL + Python combo salary premium
SELECT
    CASE
        WHEN extracted_skills LIKE '%sql%' 
         AND extracted_skills LIKE '%python%' THEN 'SQL + Python'
        WHEN extracted_skills LIKE '%sql%' 
         AND extracted_skills NOT LIKE '%python%' THEN 'SQL only'
        WHEN extracted_skills NOT LIKE '%sql%' 
         AND extracted_skills LIKE '%python%' THEN 'Python only'
        ELSE 'Neither'
    END AS skill_combo,
    COUNT(*) AS total_jobs,
    SUM(CASE WHEN salary_mid_lpa IS NOT NULL THEN 1 ELSE 0 END) AS jobs_with_salary
FROM jobs
GROUP BY skill_combo
ORDER BY total_jobs DESC;
 