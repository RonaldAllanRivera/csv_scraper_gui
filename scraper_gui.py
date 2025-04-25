
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import threading
import time
import random
import os
import tempfile

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.91 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.6367.91 Safari/537.36 Edg/124.0.2478.80"
]

def human_move_mouse(driver):
    try:
        actions = ActionChains(driver)
        for _ in range(random.randint(3, 6)):
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            actions.move_by_offset(x, y)
            actions.pause(random.uniform(0.2, 0.5))
        actions.perform()
    except Exception as e:
        print("Mouse move failed:", e)

def human_scroll_page(driver):
    try:
        for _ in range(random.randint(2, 4)):
            scroll_y = random.randint(100, 700)
            driver.execute_script(f"window.scrollBy(0, {scroll_y});")
            time.sleep(random.uniform(0.5, 1.2))
    except Exception as e:
        print("Scroll failed:", e)

def human_think_time():
    pause = random.uniform(2.5, 4.5)
    print(f"Thinking for {pause:.2f} seconds...")
    time.sleep(pause)

class ScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Scraper GUI")
        self.data = None
        self.tree = None

        tk.Button(root, text="Import CSV", command=self.import_csv).pack(pady=10)
        tk.Button(root, text="Start Scraping", command=self.start_scraping).pack(pady=10)

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            self.file_path = file_path
            self.display_table()

    def display_table(self):
        if self.tree:
            self.tree.destroy()
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = list(self.data.columns)
        self.tree["show"] = "headings"

        for col in self.data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        for index, row in self.data.iterrows():
            self.tree.insert("", "end", values=list(row))

        self.tree.pack(fill="both", expand=True)

    def start_scraping(self):
        if self.data is not None:
            threading.Thread(target=self.run_scraping, daemon=True).start()

    def run_scraping(self):
        output = self.data.copy()
        for i, row in output.iterrows():
            if pd.notna(row["Title"]) and pd.notna(row["Content"]) and pd.notna(row["Category"]):
                continue

            url = row["URL"]
            success = False

            for attempt in range(3):
                try:
                    print(f"Scraping row {i + 1}: {url} (Attempt {attempt + 1})")

                    user_agent = random.choice(USER_AGENTS)
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

                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".title_wrap h1")))
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".description")))
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.breadcrumb")))

                    title = driver.find_element(By.CSS_SELECTOR, ".title_wrap h1").text.strip()

                    paragraphs = driver.find_elements(By.CSS_SELECTOR, ".description p")
                    content = "\n\n".join(p.text.strip() for p in paragraphs if p.text.strip())

                    category_raw = driver.find_element(By.CSS_SELECTOR, "a.breadcrumb").text
                    category = category_raw.split("(")[0].strip()

                    output.at[i, "Title"] = title
                    output.at[i, "Content"] = content
                    output.at[i, "Category"] = category

                    self.tree.item(self.tree.get_children()[i], values=list(output.loc[i]))
                    success = True
                    driver.quit()
                    break

                except Exception as e:
                    print(f"Error scraping {url}: {e}")
                    time.sleep(3 + attempt * 2)
                    try:
                        driver.quit()
                    except:
                        pass

            if not success:
                output.at[i, "Title"] = "Failed"
                output.at[i, "Content"] = "Failed"
                output.at[i, "Category"] = "Failed"
                self.tree.item(self.tree.get_children()[i], values=list(output.loc[i]))

        output.to_csv(self.file_path.replace(".csv", "_output.csv"), index=False)
        messagebox.showinfo("Done", "Scraping completed and saved.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()
