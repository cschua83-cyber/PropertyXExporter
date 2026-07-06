from src.browser import get_browser

browser = get_browser()

driver = browser.get_driver()

print(driver.title)
print(driver.current_url)

input("Press Enter...")