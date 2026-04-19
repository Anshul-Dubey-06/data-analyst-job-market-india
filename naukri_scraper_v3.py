from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random
from datetime import datetime

# ─────────────────────────────────────────
#  CONFIG  — change these if you want
# ─────────────────────────────────────────
TOTAL_PAGES = 50        # 20 jobs/page → ~1000 jobs
OUTPUT_FILE = "naukri_jobs.csv"
DELAY_MIN   = 3.0       # seconds between pages
DELAY_MAX   = 6.0
HEADLESS    = True      # set False to watch the browser (useful for debugging)

# ─────────────────────────────────────────
#  SETUP DRIVER
# ─────────────────────────────────────────

def make_driver() -> webdriver.Chrome:
    opts = Options()
    if HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    # webdriver-manager auto-downloads the right ChromeDriver version
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts,
    )
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


# ─────────────────────────────────────────
#  SCRAPE ONE PAGE
# ─────────────────────────────────────────

def get_page_url(page: int) -> str:
    base = "https://www.naukri.com/data-analyst-jobs-in-india"
    return base if page == 1 else f"{base}-{page}"


def scrape_page(driver, page: int) -> list[dict]:
    url = get_page_url(page)
    driver.get(url)

    # Wait for job cards to load (up to 15s)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.srp-jobtuple-wrapper, article.jobTuple"))
        )
    except Exception:
        print(f"  [!] Timeout waiting for cards on page {page}")
        return []

    time.sleep(random.uniform(1.5, 2.5))  # extra wait for full render

    cards = driver.find_elements(By.CSS_SELECTOR, "div.srp-jobtuple-wrapper, article.jobTuple")

    jobs = []
    for card in cards:
        job = extract_job(card)
        if job["title"]:
            jobs.append(job)
    return jobs


# ─────────────────────────────────────────
#  EXTRACT FIELDS FROM ONE CARD
# ─────────────────────────────────────────

def safe_text(card, selectors: list[str]) -> str:
    """Try multiple CSS selectors; return first match's text or empty string."""
    for sel in selectors:
        try:
            el = card.find_element(By.CSS_SELECTOR, sel)
            return el.text.strip()
        except Exception:
            continue
    return ""


def safe_attr(card, selectors: list[str], attr: str) -> str:
    for sel in selectors:
        try:
            el = card.find_element(By.CSS_SELECTOR, sel)
            return el.get_attribute(attr).strip()
        except Exception:
            continue
    return ""


def extract_job(card) -> dict:
    title = safe_text(card, [
        "a.title", ".jobTitle a", "a[class*='title']", "h2 a", ".job-title a"
    ])
    company = safe_text(card, [
        "a.comp-name", ".companyInfo a", "[class*='comp-name']", ".company-name"
    ])
    experience = safe_text(card, [
        "span.expwdth", "li.experience", "[class*='exp-wrap'] span", ".exp"
    ])
    salary = safe_text(card, [
        "span.sal-wrap span", "li.salary span", "[class*='sal'] span", ".salary"
    ])
    location_els = []
    for sel in ["span.locWdth", "li.location span", "[class*='loc'] span"]:
        try:
            location_els = card.find_elements(By.CSS_SELECTOR, sel)
            if location_els:
                break
        except Exception:
            pass
    location = ", ".join(
        e.text.strip() for e in location_els if e.text.strip()
    )

    skill_els = []
    for sel in ["li.tag-li", "ul.tags-gt li", "[class*='skill'] li", "[class*='tag'] li"]:
        try:
            skill_els = card.find_elements(By.CSS_SELECTOR, sel)
            if skill_els:
                break
        except Exception:
            pass
    skills = ", ".join(e.text.strip() for e in skill_els if e.text.strip())

    posted = safe_text(card, [
        "span.job-post-day", "span[class*='post-day']", ".post-age"
    ])
    job_url = safe_attr(card, ["a.title", "a[class*='title']", "h2 a"], "href")

    return {
        "title":      title,
        "company":    company,
        "experience": experience or "Not specified",
        "salary":     salary   or "Not disclosed",
        "location":   location,
        "skills":     skills,
        "posted":     posted,
        "job_url":    job_url,
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


# ─────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────

def scrape_naukri() -> pd.DataFrame:
    print("Starting Chrome via webdriver-manager...")
    driver = make_driver()
    all_jobs = []

    try:
        for page in range(1, TOTAL_PAGES + 1):
            print(f"[Page {page:02d}/{TOTAL_PAGES}] ", end="", flush=True)
            jobs = scrape_page(driver, page)

            if not jobs:
                print(f"No jobs found — stopping.")
                break

            all_jobs.extend(jobs)
            print(f"+{len(jobs)} jobs | total: {len(all_jobs)}")
            time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

    finally:
        driver.quit()

    return pd.DataFrame(all_jobs)


# ─────────────────────────────────────────
#  SAVE + REPORT
# ─────────────────────────────────────────

def save_and_report(df: pd.DataFrame):
    if df.empty:
        print("\n[!] No data scraped.")
        print("Try setting HEADLESS = False to watch the browser and see what's happening.")
        return

    df.drop_duplicates(subset=["job_url"], inplace=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"\n{'='*52}")
    print(f"  Saved {len(df)} unique jobs  →  {OUTPUT_FILE}")
    print(f"{'='*52}")

    print(f"\n  Salary disclosed : {(df['salary'] != 'Not disclosed').sum()} / {len(df)}")

    print(f"\n  Top 10 cities:")
    cities = df["location"].str.split(",").explode().str.strip()
    print(cities.value_counts().head(10).to_string())

    print(f"\n  Top 10 skills mentioned:")
    skills = df["skills"].str.split(",").explode().str.strip().str.lower()
    skills = skills[skills != ""]
    print(skills.value_counts().head(10).to_string())

    print(f"\n  Sample rows:")
    print(df[["title", "company", "location", "salary", "experience"]].head(5).to_string(index=False))


# ─────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────

if __name__ == "__main__":
    print(f"\nNaukri Selenium scraper — 'data analyst' in 'india'")
    print(f"Target: ~{TOTAL_PAGES * 20} postings\n")
    df = scrape_naukri()
    save_and_report(df)