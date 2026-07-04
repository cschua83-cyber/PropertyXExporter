from src.browser import get_browser
from src.scraper import get_units
from src.exporter import export_to_excel

browser = get_browser()

units = get_units(browser)

export_to_excel(units)

input("Press Enter...")