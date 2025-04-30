# scraper.py – Browser automation and scraping logic.

import tempfile
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from human_simulation import human_move_mouse, human_scroll_page, human_think_time

def scrape_url(url, user_agent):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--remote-debugging-port=9222")

    user_data_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    driver.get(url)

    human_move_mouse(driver)
    human_scroll_page(driver)
    human_think_time()

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".title_wrap h1")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".description")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.breadcrumb")))

        title = driver.find_element(By.CSS_SELECTOR, ".title_wrap h1").text.strip()
        paragraphs = driver.find_elements(By.CSS_SELECTOR, ".description p")
        content = "\n\n".join(p.text.strip() for p in paragraphs if p.text.strip())
        category_raw = driver.find_element(By.CSS_SELECTOR, "a.breadcrumb").text
        category = category_raw.split("(")[0].strip()

        result = {
            "URL": url,
            "Title": title,
            "Content": content,
            "Category": category
        }

    except Exception as e:
        print(f"Scraping failed: {e}")
        result = {
            "URL": url,
            "Title": "Failed",
            "Content": "Failed",
            "Category": "Failed"
        }
    finally:
        driver.quit()

    return result

def save_output(file_path, output_rows):
    df = pd.DataFrame(output_rows)
    filename = file_path.replace(".csv", f"_output_{pd.Timestamp.now().strftime('%Y-%m-%d_%H-%M')}.csv")
    df.to_csv(filename, index=False)
    return filename
