import config

from src.navigation import (
    open_project,
    open_sales_gallery,
    open_live_sales,
    wait_for_blocks,
    get_block_tabs,
    switch_block,
)

from src.scraper import get_units
from src.exporter import export_to_excel


def collect_phase_units(driver, phase_code):

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


def run_export_workflow(driver):

    print("=" * 60)
    print(f"Start Export : {config.CURRENT_PHASE.name}")
    print("=" * 60)

    enter_live_sales(driver)

    phase = config.CURRENT_PHASE.code

    wait_for_blocks(driver)

    all_units = collect_phase_units(
        driver,
        phase
    )

    print()
    print("=" * 60)
    print(f"Total Units : {len(all_units)}")
    print("=" * 60)

    export_to_excel(all_units)

    return all_units


def enter_live_sales(driver):

    open_project(driver, config.CURRENT_PHASE)

    open_sales_gallery(driver)

    open_live_sales(driver)