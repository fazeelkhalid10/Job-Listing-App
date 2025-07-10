from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import requests
import time

API_URL = "http://localhost:5000/jobs"

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.actuarylist.com")

# Wait until job titles load
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "Job_job-card__position__ic1rc"))
    )
except:
    print("[x] Job listings didn’t load — check structure or internet.")
    driver.quit()
    exit()

# Scroll to load more jobs
for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Get job cards
cards = driver.find_elements(By.CLASS_NAME, "Job_job-card__YgDAV")

if not cards:
    print("[x] No job cards found.")
    driver.quit()
    exit()

print(f"[✓] Found {len(cards)} jobs. Processing top 10...\n")

for card in cards[:10]:
    try:
        title = card.find_element(By.CLASS_NAME, "Job_job-card__position__ic1rc").text.strip()
        company = card.find_element(By.CLASS_NAME, "Job_job-card__company__7T9qY").text.strip()

        # ✅ LOCATION HANDLING — only valid cities, no "Remote"
        location_box = card.find_element(By.CLASS_NAME, "Job_job-card__locations__x1exr")

        # Country
        country = location_box.find_element(By.CLASS_NAME, "Job_job-card__country__GRVhK").text.strip()

        # Cities (exclude remote-tagged ones)
        city_elements = location_box.find_elements(By.CLASS_NAME, "Job_job-card__location__bq7jX")
        cities = [
            c.text.strip()
            for c in city_elements
            if "Job_job-card__location-remote__xAjPu" not in c.get_attribute("class")
        ]

        # Format: City and City, Country
        if len(cities) == 1:
            location = f"{cities[0]}, {country}"
        elif len(cities) > 1:
            location = f"{' and '.join(cities)}, {country}"
        else:
            location = country

        # ✅ Tags (only from tag container)
        try:
            tag_container = card.find_element(By.CLASS_NAME, "Job_job-card__tags__zfriA")
            tag_elements = tag_container.find_elements(By.CLASS_NAME, "Job_job-card__location__bq7jX")
            tags = [tag.text.strip() for tag in tag_elements if tag.text.strip()]
        except:
            tags = []

        # ✅ Job type logic (Internship > Remote > Full-time)
        if any("intern" in tag.lower() for tag in tags):
            job_type = "Internship"
        elif any("Job_job-card__location-remote__xAjPu" in c.get_attribute("class") for c in city_elements):
            job_type = "Remote"
        else:
            job_type = "Full-time"

        # ✅ Convert "3d ago" to real date
        raw_date = card.find_element(By.CLASS_NAME, "Job_job-card__posted-on__NCZaJ").text.strip()
        if "d" in raw_date:
            days_ago = int(raw_date.split("d")[0])
            date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        else:
            date = datetime.now().strftime("%Y-%m-%d")

        # ✅ Final job dict
        job = {
            "title": title,
            "company": company,
            "location": location,
            "jobType": job_type,
            "posting_date": date,
            "tags": ", ".join(tags),
            "description": "Imported from ActuaryList.com"
        }

        # POST to backend
        res = requests.post(API_URL, json=job)
        if res.status_code == 201:
            print(f"[+] Job Added: {title}")
        if res.status_code == 409:
             print(f"[~] Duplicate Skipped: {title}")
        else:
            print(f"[!] Failed to add {title} - {res.status_code}")
    except Exception as e:
        print(f"[x] Error scraping job: {e}")

driver.quit()
