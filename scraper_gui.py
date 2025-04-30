
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import threading
import time
import random
import os
import tempfile
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def load_user_agents(file_path="user_agents.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

USER_AGENTS = load_user_agents()

def human_move_mouse(driver):
    try:
        actions = ActionChains(driver)
        x = random.randint(200, 400)
        y = random.randint(200, 400)
        actions.move_by_offset(x, y)
        actions.pause(random.uniform(0.2, 0.4))
        actions.perform()
    except Exception as e:
        print("Mouse move failed:", e)

def human_scroll_page(driver):
    try:
        for _ in range(1):  # only 1 scroll
            scroll_y = random.randint(100, 300)
            driver.execute_script(f"window.scrollBy(0, {scroll_y});")
            time.sleep(random.uniform(0.3, 0.6))
    except Exception as e:
        print("Scroll failed:", e)

def human_think_time():
    pause = random.uniform(0.8, 1.2)
    print(f"Thinking for {pause:.2f} seconds...")
    time.sleep(pause)

class ScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Scraper GUI - Final Patched Version")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        self.data = None
        self.tree = None
        self.stop_flag = False
        self.pause_flag = False

        self.custom_font = ("Arial", 11)

        root.configure(bg="#2c2f33")

        frame = tk.Frame(root, bg="#2c2f33")
        frame.pack(pady=10)

        self.import_btn = tk.Button(frame, text="Import CSV", command=self.import_csv, font=self.custom_font,
                                    bg="#3498db", fg="white", padx=20, pady=10)
        self.import_btn.pack(side="left", padx=10)

        self.start_btn = tk.Button(frame, text="Start Scraping", command=self.start_scraping, font=self.custom_font,
                                   bg="#2ecc71", fg="white", padx=20, pady=10)
        self.start_btn.pack(side="left", padx=10)

        self.pause_btn = tk.Button(frame, text="Pause Scraping", command=self.pause_scraping, font=self.custom_font,
                                   bg="#f39c12", fg="white", padx=20, pady=10)
        self.pause_btn.pack(side="left", padx=10)

        self.continue_btn = tk.Button(frame, text="Continue Scraping", command=self.continue_scraping, font=self.custom_font,
                                   bg="#8e44ad", fg="white", padx=20, pady=10)
        self.continue_btn.pack(side="left", padx=10)

        self.stop_btn = tk.Button(frame, text="Stop Scraping", command=self.stop_scraping, font=self.custom_font,
                                  bg="#e74c3c", fg="white", padx=20, pady=10)
        self.stop_btn.pack(side="left", padx=10)

        self.progress = ttk.Progressbar(root, length=800, mode="determinate")
        self.progress.pack(pady=10)

        self.progress_label = tk.Label(root, text="", font=self.custom_font, bg="#2c2f33", fg="white")
        self.progress_label.pack()

        self.saving_label = tk.Label(root, text="", font=self.custom_font, bg="#2c2f33", fg="#00ff00")

        self.set_button_states(True, True, False, False, False)

    def set_button_states(self, import_enabled, start_enabled, pause_enabled, continue_enabled, stop_enabled):
        self.import_btn.config(state="normal" if import_enabled else "disabled")
        self.start_btn.config(state="normal" if start_enabled else "disabled")
        self.pause_btn.config(state="normal" if pause_enabled else "disabled")
        self.continue_btn.config(state="normal" if continue_enabled else "disabled")
        self.stop_btn.config(state="normal" if stop_enabled else "disabled")
               

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            self.file_path = file_path
            self.display_table()
            self.set_button_states(False, True, False, False, False)

    def display_table(self):
        if self.tree:
            self.tree.destroy()
        self.tree = ttk.Treeview(self.root, style="mystyle.Treeview")
        self.tree["columns"] = ["URL", "Title", "Content", "Category"]
        self.tree["show"] = "headings"

        style = ttk.Style()
        style.theme_use("default")
        style.configure("mystyle.Treeview", font=self.custom_font, rowheight=30, background="#2c2f33",
                        fieldbackground="#2c2f33", foreground="white")
        style.configure("mystyle.Treeview.Heading", font=("Arial", 12, "bold"), background="#23272a", foreground="white")

        for col in ["URL", "Title", "Content", "Category"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=280)

        for index, row in self.data.iterrows():
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(row["URL"], row.get("Title", ""), row.get("Content", ""), row.get("Category", "")), tags=(tag,))

        self.tree.tag_configure('evenrow', background="#2c2f33")
        self.tree.tag_configure('oddrow', background="#23272a")

        self.tree.pack(fill="both", expand=True, pady=10, padx=20)

    def start_scraping(self):
        if self.data is not None:
            self.stop_flag = False
            self.pause_flag = False
            self.set_button_states(False, False, True, False, True)
            threading.Thread(target=self.run_scraping, daemon=True).start()

    def stop_scraping(self):
        self.stop_flag = True
        self.set_button_states(True, True, False, False, False)

    def pause_scraping(self):
        self.pause_flag = True
        self.set_button_states(False, False, False, True, True)

    def continue_scraping(self):
        self.pause_flag = False
        self.set_button_states(False, False, True, False, True)

    def run_scraping(self):
        output_rows = []
        scraped_count = 0
        total_rows = len(self.data)

        tree_items = self.tree.get_children()
        for i, item in enumerate(tree_items):
            if self.stop_flag:
                break

            while self.pause_flag:
                time.sleep(0.5)

            values = self.tree.item(item, "values")
            url = values[0]

            if not url or url.strip() == "":
                continue

            try:
                print(f"Scraping row {i + 1}: {url}")

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

                self.tree.item(item, values=(url, title, content, category))

                output_rows.append({
                    "URL": url,
                    "Title": title,
                    "Content": content,
                    "Category": category
                })

                driver.quit()

            except Exception as e:
                print(f"Failed to scrape {url}: {e}")
                self.tree.item(item, values=(url, "Failed", "Failed", "Failed"))
                try:
                    driver.quit()
                except:
                    pass

            scraped_count += 1
            progress_percent = int((i+1) / total_rows * 100)
            self.progress["value"] = progress_percent
            self.progress_label.config(text=f"{progress_percent}% complete")
            self.root.update_idletasks()

        self.set_button_states(True, True, False, False, False)
        self.save_output(output_rows)

    def save_output(self, output_rows):
        if output_rows:
            self.saving_label.config(text="Saving file... Please wait...")
            self.saving_label.pack(pady=10)
            self.root.update_idletasks()

            df = pd.DataFrame(output_rows)
            filename = self.file_path.replace(".csv", f"_output_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv")
            df.to_csv(filename, index=False)

            self.saving_label.pack_forget()
            messagebox.showinfo("Done", f"Scraping completed and saved as {filename}.")
        else:
            messagebox.showinfo("Done", "No valid rows scraped. Nothing saved.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()
