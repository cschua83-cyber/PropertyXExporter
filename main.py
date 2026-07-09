from src.browser import get_browser
from src.navigation import (
    ensure_landing,
    open_project,
    open_live_sales,
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

    open_project(driver, "Phase 3B")

    open_live_sales(driver)

# Landing
elif "/dashboards/landing" in url:

    print("Current State : Landing")

    ensure_landing(driver)

    open_project(driver, "Phase 3B")

    open_live_sales(driver)

# Project Summary
elif "/dashboards/project-summary" in url:

    print("Current State : Project Summary")

    open_live_sales(driver)
    
    
elif "/dashboards/page-detail" in url:

    print("Current State : Page Detail")

    open_live_sales(driver)
    

# Unit Live
elif "/unit-live/" in url:

    print("Current State : Unit Live")

    phase = "3B"
    block = "C2-2"

    units = get_units(
        driver,
        phase,
        block
    )

    print(f"\n完成，共 {len(units)} 个 Unit")
    

# Unknown
else:

    print("Unknown Page")
    print(driver.current_url)

input("Press Enter...")