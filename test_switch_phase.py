from src.browser import get_browser
from selenium.webdriver.common.by import By

browser = get_browser()
driver = browser.get_driver()

# 如果目前在 Unit Live，就回上一页
if "/unit-live/" in driver.current_url.lower():

    driver.back()

input("确认已经回到 Page Detail，再按 Enter...")

from src.navigation import switch_phase

switch_phase(
    driver,
    "Phase 3A"
)

input("Press Enter...")