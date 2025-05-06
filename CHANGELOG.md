## 📦 CHANGELOG

### v2.2.0 (Pause/Stop Fix + Faster Simulation)

- 🐛 Fixed bug where clicking Stop after Pause skipped CSV output
- 🚫 Disabled the "Stop" button while paused to prevent state loss
- ⚡ Greatly reduced mouse, scroll, and delay timing in `human_simulation.py` for faster scraping
- 🧪 Minor UI usability improvements for data preservation

### v2.1.0 (Improved Scrape Reliability)

- 🔁 Added 1 retry attempt for failed rows to improve scraping success rate
- ✅ Only marks as "Failed" if second attempt also fails
- 💼 Prepared for long-run scraping with minimal slowdown

### v2.0.0 (Stable GUI Refactor)

- 🧩 Fully modularized the code into separate Python modules
- 🖥️ Enhanced desktop GUI with dark theme, pause/continue, button management
- 📦 Includes README, CHANGELOG, requirements.txt for packaging
- 🐞 Removed retry attempts for failed scrapes to avoid slowdowns

### v1.0.0 (Initial Script)

- CSV input/output
- Selenium scraping
- Basic GUI with import/start/stop
- Random user-agent rotation
