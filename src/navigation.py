"""
navigation.py

负责网页导航：
- Block
- Phase
- Sales Gallery
- Live Sales
"""
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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
        
def open_project_dialog(driver):

    print("=" * 60)
    print("Opening Switch Project...")
    print("=" * 60)

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "app-switch-project button"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        button
    )

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "mat-dialog-container"
            )
        )
    )

    print("Switch Project dialog opened.")


def open_live_sales(driver):

    print("=" * 60)
    print("Opening Live Sales...")
    print("=" * 60)

    
    input("停在这里，按 Enter 后继续...")

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
    

def switch_project(driver, project_name):

    open_project_dialog(driver)

    print("=" * 60)
    print(f"Switch Project -> {project_name}")
    print("=" * 60)

    dialog = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "mat-dialog-container"
            )
        )
    )

    projects = dialog.find_elements(
        By.CSS_SELECTOR,
        "mat-list-item"
    )

    for project in projects:

        if project_name in project.text:

            driver.execute_script(
                "arguments[0].click();",
                project
            )

            print("Project switched.")

            return

    raise Exception(f"Project '{project_name}' not found.")
    
    
def debug_projects(driver):

    print("=" * 60)
    print("Searching dialog...")
    print("=" * 60)

    dialogs = driver.find_elements(
        By.CSS_SELECTOR,
        "[role='dialog']"
    )

    print(f"Found {len(dialogs)} dialog(s)")

    for i, dialog in enumerate(dialogs):

        print("-" * 60)
        print(f"Dialog {i}")

        print("-" * 60)
        

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

    print("Before Click:")
    print(driver.current_url)

    driver.execute_script(
        "arguments[0].click();",
        project
    )

    import time
    time.sleep(3)

    print("After Click:")
    print(driver.current_url)
    
    
def dismiss_subscription(driver):

    print("=" * 60)
    print("Checking Subscription Dialog...")
    print("=" * 60)

    try:

        button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(., 'Dismiss')]"
                )
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            button
        )

        print("Subscription dialog dismissed.")

    except TimeoutException:

        print("No subscription dialog.")
        
        
def ensure_landing(driver):

    url = driver.current_url.lower()

    if "workdesk.property-x.asia" in url:

        print("Currently at Workdesk Home.")
        open_sales_crm(driver)

    elif "/dashboards/landing" in url:

        print("Already at Landing.")

    else:

        print("Current page:", driver.current_url)

    dismiss_subscription(driver)