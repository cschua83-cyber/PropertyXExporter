from src.browser import get_browser
from src.navigation import ensure_landing
from src.exporter import export_to_excel
from src.workflow import(
    run_export_workflow,
    collect_phase_units,
)

import config

def run(phase):

    config.CURRENT_PHASE = phase

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

        run_export_workflow(driver)


    # Landing
    elif "/dashboards/landing" in url:

        print("Current State : Landing")

        run_export_workflow(driver)
        

    # Project Summary
    elif "/dashboards/project-summary" in url:

        print("Current State : Project Summary")

        run_export_workflow(driver)
        
        
    # Unit Live
    elif "/unit-live/" in url:

        print("Current State : Unit Live")

        phase = config.CURRENT_PHASE.code

        all_units = collect_phase_units(
            driver,
            phase
        )

        print()
        print("=" * 60)
        print(f"Total Units : {len(all_units)}")
        print("=" * 60)

        export_to_excel(all_units)

        
if __name__ == "__main__":

    run(config.CURRENT_PHASE)