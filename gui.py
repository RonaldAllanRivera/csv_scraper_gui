# gui.py – All user interface logic.

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import threading
import time
import random

from scraper import scrape_url, save_output
from utils import load_user_agents

USER_AGENTS = load_user_agents()

class ScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Scraper GUI - Modular")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        self.data = None
        self.tree = None
        self.stop_flag = False
        self.pause_flag = False
        self.output_rows = []
        self.custom_font = ("Arial", 11)

        self.setup_gui()
        self.set_button_states(True, False, False, False, False)

    def setup_gui(self):
        self.root.configure(bg="#2c2f33")
        frame = tk.Frame(self.root, bg="#2c2f33")
        frame.pack(pady=10)

        self.import_btn = tk.Button(frame, text="Import CSV", command=self.import_csv, font=self.custom_font,
                                    bg="#3498db", fg="white", padx=20, pady=10)
        self.import_btn.pack(side="left", padx=10)

        self.start_btn = tk.Button(frame, text="Start", command=self.start_scraping, font=self.custom_font,
                                   bg="#2ecc71", fg="white", padx=20, pady=10)
        self.start_btn.pack(side="left", padx=10)

        self.pause_btn = tk.Button(frame, text="Pause", command=self.pause_scraping, font=self.custom_font,
                                   bg="#f39c12", fg="white", padx=20, pady=10)
        self.pause_btn.pack(side="left", padx=10)

        self.continue_btn = tk.Button(frame, text="Continue", command=self.continue_scraping, font=self.custom_font,
                                   bg="#8e44ad", fg="white", padx=20, pady=10)
        self.continue_btn.pack(side="left", padx=10)

        self.stop_btn = tk.Button(frame, text="Stop", command=self.stop_scraping, font=self.custom_font,
                                  bg="#e74c3c", fg="white", padx=20, pady=10)
        self.stop_btn.pack(side="left", padx=10)

        self.progress = ttk.Progressbar(self.root, length=800, mode="determinate")
        self.progress.pack(pady=10)

        self.progress_label = tk.Label(self.root, text="", font=self.custom_font, bg="#2c2f33", fg="white")
        self.progress_label.pack()

        self.saving_label = tk.Label(self.root, text="", font=self.custom_font, bg="#2c2f33", fg="#00ff00")

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
            self.output_rows = []
            self.set_button_states(False, False, True, False, True)
            threading.Thread(target=self.run_scraping, daemon=True).start()

    def pause_scraping(self):
        self.pause_flag = True
        # Disable Stop while paused to avoid inconsistent state
        self.set_button_states(False, False, False, True, False)

    def continue_scraping(self):
        self.pause_flag = False
        self.set_button_states(False, False, True, False, True)

    def stop_scraping(self):
        self.stop_flag = True
        self.pause_flag = False  # allow thread to complete
        self.set_button_states(True, True, False, False, False)

    def run_scraping(self):
        tree_items = self.tree.get_children()
        total_rows = len(tree_items)
        for i, item in enumerate(tree_items):
            if self.stop_flag:
                break
            while self.pause_flag:
                time.sleep(0.5)

            url = self.tree.item(item, "values")[0]
            if not url or url.strip() == "":
                continue

            user_agent = random.choice(USER_AGENTS)
            result = scrape_url(url, user_agent)
            self.tree.item(item, values=(result["URL"], result["Title"], result["Content"], result["Category"]))

            if result["Title"] != "Failed":
                self.output_rows.append(result)

            self.progress["value"] = int((i + 1) / total_rows * 100)
            self.progress_label.config(text=f"{int((i + 1) / total_rows * 100)}% complete")
            self.root.update_idletasks()

        self.set_button_states(True, True, False, False, False)
        self.finish_save()

    def finish_save(self):
        if self.output_rows:
            self.saving_label.config(text="Saving file...")
            self.saving_label.pack(pady=10)
            self.root.update_idletasks()

            filename = save_output(self.file_path, self.output_rows)

            self.saving_label.pack_forget()
            messagebox.showinfo("Done", f"Scraping completed and saved as {filename}.")
        else:
            messagebox.showinfo("Done", "No valid rows scraped. Nothing saved.")
