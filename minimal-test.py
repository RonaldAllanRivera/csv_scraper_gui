from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument("--headless")  # leave visible for testing
driver = webdriver.Chrome(service=Service(), options=options)
driver.get("https://example.com")
input("Press Enter to close...")
driver.quit()
