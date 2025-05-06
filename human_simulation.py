
# human_simulation.py – Minimal delay version for speed scraping

import random
import time
from selenium.webdriver.common.action_chains import ActionChains

def human_move_mouse(driver):
    try:
        actions = ActionChains(driver)
        x = random.randint(200, 400)
        y = random.randint(200, 400)
        actions.move_by_offset(x, y)
        actions.pause(random.uniform(0.05, 0.1))
        actions.perform()
    except Exception as e:
        print("Mouse move failed:", e)

def human_scroll_page(driver):
    try:
        scroll_y = random.randint(100, 300)
        driver.execute_script(f"window.scrollBy(0, {scroll_y});")
        time.sleep(random.uniform(0.05, 0.1))
    except Exception as e:
        print("Scroll failed:", e)

def human_think_time():
    pause = random.uniform(0.05, 0.1)
    print(f"Thinking for {pause:.2f} seconds...")
    time.sleep(pause)
