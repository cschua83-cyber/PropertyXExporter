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

browser = get_browser()
driver = browser.get_driver()


def export_current_phase(driver, phase_code):

    tabs = get_block_tabs(driver)

    all_units = []

    for tab in tabs:

        block = tab.text.replace("BLOCK", "").strip()

        print(f"Processing {block}")

        switch_block(driver, block)

        units = get_units(
            driver,
            phase_code,
            block
        )

        all_units.extend(units)

    return all_units


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

    open_project(driver, "Phase 3B")

    open_sales_gallery(driver)

    open_live_sales(driver)


# Landing
elif "/dashboards/landing" in url:

    print("Current State : Landing")

    ensure_landing(driver)

    print("=" * 60)
    print("Experiment: Stay on Landing")
    print("=" * 60)

    open_project(driver, "Phase 3B")

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

    all_units = export_current_phase(
        driver,
        "3A"
    )

    print()
    print("=" * 60)
    print(f"Total Units : {len(all_units)}")
    print("=" * 60)