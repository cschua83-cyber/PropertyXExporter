"""
navigation.py

负责网页导航：
- Block
- Phase
- Sales Gallery
- Live Sales
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def debug_tabs(driver):

    print("=" * 60)
    print("Searching Tabs...")
    print("=" * 60)

    elements = driver.find_elements(
        By.CSS_SELECTOR,
        "[role='tab']"
    )

    print(f"Found {len(elements)} elements")

    for i, e in enumerate(elements):

        print("-" * 40)
        print(f"Tab {i}")
        print("Text :", e.text)
        print("Class:", e.get_attribute("class"))
        

def open_live_sales(driver):

    print("=" * 60)
    print("Opening Live Sales...")
    print("=" * 60)

    # 记录目前有几个 Tab
    old_tab_count = len(driver.window_handles)

    # 找到 Live Sales Chart 按钮
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[.//span[contains(text(),'Live Sales Chart')]]"
            )
        )
    )

    # 点击按钮
    button.click()

    print("Live Sales Chart clicked.")

    # 等待新 Tab 开启
    WebDriverWait(driver, 10).until(
        lambda d: len(d.window_handles) > old_tab_count
    )

    # 切换到最新 Tab
    driver.switch_to.window(driver.window_handles[-1])

    print("Switched to Live Sales")

    print(driver.title)
    print(driver.current_url)

    print("=" * 60)
    

def get_block_tabs(driver):

    WebDriverWait(driver, 10).until(
        lambda d: len(
            d.find_elements(By.CSS_SELECTOR, "div[role='tab']")
        ) >= 4
    )

    tabs = driver.find_elements(
        By.CSS_SELECTOR,
        "div[role='tab']"
    )

    print("=" * 60)
    print(f"Found {len(tabs)} Tabs")
    print("=" * 60)

    for i, tab in enumerate(tabs):
        print(f"[{i}] {tab.text}")

    return tabs