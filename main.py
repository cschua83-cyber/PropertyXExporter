from src.browser import get_browser
from src.navigation import open_live_sales, get_block_tabs

browser = get_browser()

driver = browser.get_driver()

browser = get_browser()

driver = browser.get_driver()

if "unit-live" not in driver.current_url:
    open_live_sales(driver)

tabs = get_block_tabs(driver)

block_tabs = tabs[1:]   # 跳过 PHASE

print()
print("Blocks")
print("-" * 40)

for tab in block_tabs:
    print(tab.text)

input("Press Enter...")