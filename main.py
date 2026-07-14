from src.browser import get_browser
from src.navigation import (
    ensure_landing,
    open_project,
    open_sales_gallery,
    open_live_sales,
    open_switch_project,
    switch_phase,
    switch_block,
    get_block_tabs,
)
from src.scraper import get_units
from src.config import PROJECTS


browser = get_browser()
driver = browser.get_driver()

print("=" * 60)
print("Current Page")
print("=" * 60)
print(driver.current_url)
print()

url = driver.current_url.lower()

# Home
if "workdesk.property-x.asia" in url:

    print("Current State : Workdesk Home")

    ensure_landing(driver)

    print("=" * 60)
    print("Experiment: Stay on Landing")
    print("=" * 60)

    input("请等待15秒观察Landing有没有Dialog，再按Enter继续...")

    open_project(driver, "Phase 3A")

    open_sales_gallery(driver)

    open_live_sales(driver)


# Landing
elif "/dashboards/landing" in url:

    print("Current State : Landing")

    ensure_landing(driver)

    print("=" * 60)
    print("Experiment: Stay on Landing")
    print("=" * 60)

    input("请等待15秒观察Landing有没有Dialog，再按Enter继续...")

    open_project(driver, "Phase 3A")

    open_sales_gallery(driver)

    open_live_sales(driver)
    

# Project Summary
elif "/dashboards/project-summary" in url:

    print("Current State : Project Summary")

    open_live_sales(driver)
    
    
elif "/dashboards/page-detail" in url:

    print("Current State : Page Detail")

    print("STEP 1")
    switch_phase(driver, "Phase 3A")

    print("STEP 2")
    open_live_sales(driver)

    print("STEP 3")
   

# Unit Live
elif "/unit-live/" in url:

    print("Current State : Unit Live")

    tabs = get_block_tabs(driver)

    all_units = []

    phase = "3A"

    for tab in tabs:

        block = tab.text.replace("BLOCK", "").strip()

        switch_block(driver, block)

        units = get_units(
            driver,
            phase,
            block
        )

        all_units.extend(units)

    print()
    print("=" * 60)
    print(f"Total Units : {len(all_units)}")
    print("=" * 60)