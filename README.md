# CSV Scraper GUI

A professional desktop scraper app for websites with heavy protection, using real human-like browser behavior.

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
   pip install pandas selenium pyinstaller
   ```

2. Download matching **ChromeDriver** for your Chrome version.

3. Run:

   ```bash
   python scraper_gui.py
   ```

---

## 📦 How to Use (Windows EXE Version)

> If you already have the prebuilt `.EXE` (scraper_gui.exe), you don't need Python installed.

1. Double-click `scraper_gui.exe`
2. Use the graphical interface normally:
   - Import CSV
   - Start, Pause, Continue, Stop scraping
   - CSV output is saved automatically
3. **Important:** Keep `chromedriver.exe` in the same folder as `scraper_gui.exe`.

---

## ⚙️ Build the EXE Yourself (Optional)

If you want to rebuild the EXE manually:

```bash
pyinstaller --onefile --noconsole scraper_gui.py
```

The `.EXE` will be inside the `dist/` folder.

---

## 📄 CSV Input Format

| URL | Title | Content | Category |
| :-- | :---- | :------ | :------- |

- Only `URL` is needed initially.
- `Title`, `Content`, `Category` are filled by the scraper.

---

## 📦 Files in Final Folder

| File             | Purpose                            |
| :--------------- | :--------------------------------- |
| scraper_gui.exe  | The desktop application            |
| chromedriver.exe | Needed by Selenium                 |
| user_agents.txt  | Random desktop browser User-Agents |
