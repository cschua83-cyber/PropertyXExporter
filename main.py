from src.browser import get_browser
from src.navigation import (
    ensure_landing,
    open_project,
    open_live_sales,
    open_switch_project,
    switch_phase,
    switch_block,
    get_block_tabs,
)
from src.scraper import get_units

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

    open_project(driver, "Phase 3A")

    open_live_sales(driver)

# Landing
elif "/dashboards/landing" in url:

    print("Current State : Landing")

    ensure_landing(driver)

    open_project(driver, "Phase 3A")

    open_live_sales(driver)

# Project Summary
elif "/dashboards/project-summary" in url:

    print("Current State : Project Summary")

    open_live_sales(driver)
    
    
elif "/dashboards/page-detail" in url:

    print("Current State : Page Detail")

    switch_phase(driver, "Phase 3A")

    input("检查 Header 有没有变成 Phase 3A，再按 Enter...")
   

# Unit Live
elif "/unit-live/" in url:

    print("Current State : Unit Live")

    tabs = get_block_tabs(driver)

    print()

    all_units = []

    phase = "3B"

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
    

# Unknown
else:

    print("Unknown Page")
    print(driver.current_url)

input("Press Enter...")