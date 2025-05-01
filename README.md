# CSV Scraper GUI

A professional Python desktop scraper app built with Selenium, Tkinter, and ChromeDriver, designed to handle websites with heavy protection (e.g., Cloudflare) using real human-like browser automation and behavior simulation.

---

## ✨ Features

- 🖥️ Dark Mode desktop UI
- 📥 Import CSV of links to scrape
- 🔎 Live updating data in the GUI
- 🛑 Pause and ▶️ Continue scraping at any time
- ✅ Mark failed scrapes (not saved to final CSV)
- 📊 Progress bar shows scraping % completion
- 💾 Export only successfully scraped rows to output CSV

---

## 📋 How to Use (Python Version)

1. Install requirements:

```bash
pip install -r requirements.txt
```

2. Download matching **ChromeDriver** for your Chrome version.
3. Run:

```bash
python main.py
```

---

## 📦 How to Use (Windows EXE Version)

> Already have `scraper_gui.exe`? You don’t need Python.

1. Double-click `scraper_gui.exe`
2. Use the graphical interface:
   - Import CSV
   - Start, Pause, Continue, Stop scraping
   - CSV output is saved automatically
3. **Important:** Keep `chromedriver.exe` in the same folder as `scraper_gui.exe`

---

## ⚙️ Build the EXE Yourself (Optional)

```bash
pyinstaller --onefile --noconsole --name scraper_gui main.py
```

- The `.exe` will appear in the `dist/` folder
- You can delete the `build/` folder unless you plan to rebuild it again

---

## 📄 CSV Input Format

| URL | Title | Content | Category |
| :-- | :---- | :------ | :------- |

- Only `URL` is needed initially
- The rest will be filled by the scraper

---

## 📁 File Overview

| File               | Purpose                                |
| ------------------ | -------------------------------------- |
| `main.py`          | App launcher and Tkinter GUI entry     |
| `scraper.py`       | All scraping logic                     |
| `gui.py`           | All user interface logic.              |
| `utils.py`         | User-agent loading and helpers.        |
| `user_agents.txt`  | Random desktop user agents             |
| `requirements.txt` | Python packages needed to run          |
| `setup.py`         | Package definition for `pip install .` |
| `scraper_gui.exe`  | Windows executable (if prebuilt)       |
| `chromedriver.exe` | Required by Selenium Chrome automation |
