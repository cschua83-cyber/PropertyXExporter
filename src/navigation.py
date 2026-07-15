"""
navigation.py

负责网页导航：
- Block
- Phase
- Sales Gallery
- Live Sales
"""

# Python 内建模块
import re
import time

# 第三方模块
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

# 自己的模块
from src.models import Unit
    
        
def open_live_sales(driver):

    print("=" * 60)
    print("Opening Live Sales...")
    print("=" * 60)

    force_dismiss_subscription(driver)

    old_tab_count = len(driver.window_handles)

    button = WebDriverWait(
        driver,
        10
    ).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[.//span[contains(.,'Live Sales Chart')]]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        button
    )

    print("Live Sales opened.")
    
    
    WebDriverWait(driver, 10).until(
        lambda d: len(d.window_handles) > old_tab_count
    )

    driver.switch_to.window(driver.window_handles[-1])

    print("Switched to Live Sales")
    print(driver.current_url)
    
    
def open_switch_project(driver):

    print("=" * 60)
    print("Opening Switch Project...")
    print("=" * 60)

    # 找出所有 Switch Project 按钮
    buttons = driver.find_elements(
        By.CSS_SELECTOR,
        "app-switch-project button"
    )

    print(f"Found {len(buttons)} switch button(s)")

    button = None

    # 只使用画面上可见的按钮
    for i, b in enumerate(buttons):

        print("-----")
        print(i)
        print("Displayed :", b.is_displayed())
        print("Enabled   :", b.is_enabled())

        if b.is_displayed():
            button = b

    if button is None:
        raise Exception("Cannot find visible Switch Project button.")

    print("Using visible button.")

    # 模拟真人点击
    ActionChains(driver)\
        .move_to_element(button)\
        .pause(0.2)\
        .click()\
        .perform()

    # 等待 Dialog 出现
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (
                By.CSS_SELECTOR,
                "switch-project-dialog"
            )
        )
    )

    print("Switch Project opened.")
    
def get_current_phase(driver):

    title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                ".xsTitle-f"
            )
        )
    )

    text = title.text.strip()

    return text


def switch_phase(driver, phase_name):

    print("=" * 60)
    print(f"Switching Project -> {phase_name}")
    print("=" * 60)

    
    open_switch_project(driver)

    # 等 Dialog 完全加载
    time.sleep(1)

    items = driver.find_elements(
        By.CSS_SELECTOR,
        "switch-project-dialog mat-list-item"
    )

    found = False

    for item in items:

        if phase_name in item.text:

            found = True

            print("准备点击：", item.text)

            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                item
            )

            time.sleep(0.5)

            ActionChains(driver)\
                .move_to_element(item)\
                .pause(0.2)\
                .click()\
                .perform()

            print("已经执行 ActionChains.click()")

            print("Phase clicked.")
            
            wait_overlay_disappear(driver)

            break


    if not found:

        current = get_current_phase(driver)

        if phase_name in current:

            print(f"Already in {phase_name}")

            driver.find_element(
                By.TAG_NAME,
                "body"
            ).send_keys(Keys.ESCAPE)

            wait_overlay_disappear(driver)

            return

        raise Exception(f"Cannot find {phase_name}")
    
    print("Project switched.")
    
     
def wait_overlay_disappear(driver):

    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located(
            (
                By.CSS_SELECTOR,
                ".cdk-overlay-backdrop"
            )
        )
    )
            

def get_block_tabs(driver):

    print("=" * 60)
    print("Reading Block Tabs...")
    print("=" * 60)

    tabs = driver.find_elements(
        By.CSS_SELECTOR,
        "div[role='tab']"
    )

    block_tabs = []

    for tab in tabs:

        text = tab.text.strip()

        if text.startswith("BLOCK"):
            block_tabs.append(tab)

    print(f"Found {len(block_tabs)} Blocks")

    return block_tabs


def switch_block(driver, block_name):

    print("=" * 60)
    print(f"Switching Block -> {block_name}")
    print("=" * 60)

    tabs = get_block_tabs(driver)

    for tab in tabs:

        if block_name in tab.text:

            driver.execute_script(
                "arguments[0].click();",
                tab
            )

            print("Block clicked.")

            # 等网页刷新
            time.sleep(2)

            return

    raise Exception(f"Cannot find Block: {block_name}")
    
    
def open_sales_crm(driver):

    print("=" * 60)
    print("Opening Sales CRM...")
    print("=" * 60)

    sales_crm = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//p[normalize-space()='Sales CRM']"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        sales_crm
    )

    print("Sales CRM clicked.")

    WebDriverWait(driver, 10).until(
        lambda d: "sales.property-x.asia" in d.current_url
    )

    print(driver.current_url)
        
    
def open_project(driver, project_name):

    print("=" * 60)
    print(f"Opening Project: {project_name}")
    print("=" * 60)

    project = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//div[contains(@class,'mat-line') and contains(.,'{project_name}')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        project
    )

    WebDriverWait(driver, 10).until(
        lambda d: "/dashboards/project-summary" in d.current_url
    )

    print("Project Summary loaded")
    print(driver.current_url)

    time.sleep(3)
    

def open_sales_gallery(driver):

    print("=" * 60)
    print("Opening Sales Gallery...")
    print("=" * 60)

    gallery = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "mat-list-item[routerlink='/dashboards/page-detail']"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        gallery
    )

    WebDriverWait(driver, 10).until(
        lambda d: "/dashboards/page-detail" in d.current_url
    )

    print(driver.current_url)
        
    
# 👇 新增这里
def force_dismiss_subscription(driver):

    print("=" * 60)
    print("Force Dismiss Dialog")
    print("=" * 60)

    dialogs = driver.find_elements(
        By.CSS_SELECTOR,
        "mat-dialog-container"
    )

    print("Dialog:", len(dialogs))

    for dialog in dialogs:

        html = dialog.get_attribute("outerHTML")

        if "Subscription Expiring" not in html:
            continue

        print("Subscription dialog found")

        try:

            button = dialog.find_element(
                By.XPATH,
                ".//button[contains(., 'Dismiss')]"
            )

            driver.execute_script(
                "arguments[0].click();",
                button
            )

            print("Dismiss clicked")
            
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "mat-dialog-container"
                    )
                )
            )

            print("After 2 seconds")

            dialogs = driver.find_elements(
                By.CSS_SELECTOR,
                "mat-dialog-container"
            )

            print("Dialog:", len(dialogs))

            print(
                "Subscription:",
                driver.page_source.count("Subscription Expiring")
            )
            
            return True
        

        except Exception as e:

            print(e)

    print("No subscription dialog")

    return False
        
        
def ensure_landing(driver):

    url = driver.current_url.lower()

    if "workdesk.property-x.asia" in url:

        print("Currently at Workdesk Home.")
        open_sales_crm(driver)

    elif "/dashboards/landing" in url:

        print("Already at Landing.")

    else:

        print("Current page:", driver.current_url)

    # 不处理 Subscription Dialog
    
    def test_phase_blocks(driver):

        print("=" * 60)
        print("Testing Phase 3B")
        print("=" * 60)

        # 切换到 Phase 3B
        switch_phase(driver, "Phase 3B")

        # 读取所有 Block
        tabs = get_block_tabs(driver)

        print(f"Found {len(tabs)} block(s)")

        for i, tab in enumerate(tabs, start=1):

            print(f"{i}. {tab.text}")