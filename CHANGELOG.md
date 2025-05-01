## 📦 CHANGELOG

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
