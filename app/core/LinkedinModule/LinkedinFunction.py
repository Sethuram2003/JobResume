import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_linkedin_jobs(keyword, location="United States", max_jobs=20, slow_mo=0.5):
    """
    Scrape LinkedIn jobs for a given keyword and location, filtered to the last 24 hours.
    
    Parameters:
        keyword (str): Job title or keyword to search for.
        location (str): Location for the search (default: "United States").
        max_jobs (int): Maximum number of jobs to scrape (default: 20).
        slow_mo (float): Delay between actions (in seconds) to avoid rate limiting.
    
    Returns:
        list of dict: List of job dictionaries, each containing:
            job_id, title, company, location, link, promoted, easy_apply, date, description
    """
    li_at = os.environ.get("LI_AT_COOKIE")
    if not li_at:
        print("❌ LI_AT_COOKIE environment variable not set.")
        return []

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.linkedin.com")
        time.sleep(2)
        driver.add_cookie({"name": "li_at", "value": li_at, "domain": ".linkedin.com"})

        encoded_keyword = keyword.replace(' ', '%20')
        encoded_location = location.replace(' ', '%20')
        url = f"https://www.linkedin.com/jobs/search?keywords={encoded_keyword}&location={encoded_location}&f_TPR=r86400"
        driver.get(url)
        time.sleep(3)

        print("🔍 Current URL:", driver.current_url)
        print("📄 Page title:", driver.title)
        driver.save_screenshot("linkedin_page.png")
        print("📸 Screenshot saved as linkedin_page.png")

        wait = WebDriverWait(driver, 20)
        try:
            job_cards = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.job-card-container"))
            )
            print(f"✅ Found {len(job_cards)} job cards.")
        except TimeoutException:
            print("⏱️ Timeout waiting for job cards.")
            with open("linkedin_page_debug.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("💾 Saved full page HTML to linkedin_page_debug.html")
            return []

        jobs = []
        for idx, card in enumerate(job_cards[:max_jobs], 1):
            try:
                job_id = card.get_attribute("data-job-id")

                title_elem = card.find_element(By.CSS_SELECTOR, "a.job-card-list__title--link")
                title = title_elem.text.strip()
                if title.endswith("with verification"):
                    title = title.replace(" with verification", "").strip()
                link = title_elem.get_attribute("href")

                company_elem = card.find_element(By.CSS_SELECTOR, ".artdeco-entity-lockup__subtitle span")
                company = company_elem.text.strip()

                location_elem = card.find_element(By.CSS_SELECTOR, ".artdeco-entity-lockup__caption ul li span")
                location_text = location_elem.text.strip()

                card_text = card.text
                promoted = "Promoted" in card_text
                easy_apply = "Easy Apply" in card_text

                # Date not available on card – keep as N/A
                date_time = "N/A"

                # Click the card to load details
                card.click()
                time.sleep(1)  # wait for pane to start loading

                # Wait for description container
                try:
                    desc_elem = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, ".jobs-description__content .jobs-box__html-content")
                        )
                    )
                    description = desc_elem.text.strip()
                except TimeoutException:
                    print(f"⚠️ No description loaded for job {idx}: {title}")
                    description = "N/A"

                jobs.append({
                    "job_id": job_id,
                    "title": title,
                    "company": company,
                    "location": location_text,
                    "link": link,
                    "promoted": promoted,
                    "easy_apply": easy_apply,
                    "date": date_time,
                    "description": description
                })
                print(f"✓ [{idx}/{min(len(job_cards), max_jobs)}] {title} at {company}")

                time.sleep(slow_mo)  # Be gentle

            except Exception as e:
                print(f"⚠️ Error extracting job {idx}: {e}")

        return jobs

    finally:
        driver.quit()

# Example usage (if run as a script)
if __name__ == "__main__":
    jobs = scrape_linkedin_jobs("Python Developer", max_jobs=10, slow_mo=0.8)
    if jobs:
        with open("linkedin_jobs_direct.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
            writer.writeheader()
            writer.writerows(jobs)
        print(f"💾 Saved {len(jobs)} jobs to linkedin_jobs_direct.csv")
    else:
        print("No jobs scraped.")