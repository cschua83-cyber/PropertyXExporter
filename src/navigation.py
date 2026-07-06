"""
navigation.py

负责网页导航：
- Block
- Phase
- Sales Gallery
- Live Sales
"""

from selenium.webdriver.common.by import By

def get_block_tabs(driver):
    tabs = driver.find_elements(
        By.CSS_SELECTOR,
        "div[role='tab']"
    )

    print("=" * 60)
    print(f"Found {len(tabs)} Block Tabs")
    print("=" * 60)

    for i, tab in enumerate(tabs):
        print(f"[{i}] {tab.text}")

    return tabs