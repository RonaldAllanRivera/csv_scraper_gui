# CSV Scraper GUI

A professional desktop app for scraping data intelligently from websites with a full GUI interface.

Built with **Python, Tkinter, Selenium**, and **ChromeDriver**.

---

## ✨ Features

- 🖥️ Dark Mode GUI for desktop/laptop users
- 📥 Import CSV with list of URLs to scrape
- 🔎 Live update scraped data in the app during scraping
- 🛑 Pause and ▶️ Continue scraping at any time
- ✅ Show successful and failed scrapes visually
- 🧹 Save only successful scrapes to final CSV output
- 📊 Progress bar shows % complete
- 💾 Save progress when stopping scraping manually
- 🎯 Human-like browser actions (mouse movements, scrolling, random thinking time)

---

## 📋 How to Use

1. Clone or download this repository
2. Install Python dependencies:

   ```bash
   pip install pandas selenium
   ```

3. Download **ChromeDriver** matching your Chrome browser version and place it in the same folder.
4. Run the application:

   ```bash
   python scraper_gui.py
   ```

5. Use the app interface to:
   - Import your CSV of URLs
   - Start scraping
   - Pause, Continue, or Stop when needed
6. Successfully scraped results will be saved automatically into a new CSV.

---

## 📄 CSV Format

Input CSV should have these columns:

| URL | Title | Content | Category |
| :-- | :---- | :------ | :------- |

Only the `URL` is required initially. The scraper fills `Title`, `Content`, and `Category`.

---

## ⚙️ Configuration

- ChromeDriver must match your installed Google Chrome version.
- You can add more User-Agents by editing `user_agents.txt`.
