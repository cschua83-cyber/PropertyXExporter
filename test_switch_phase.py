from src.browser import get_browser
from src.navigation import switch_phase

browser = get_browser()
driver = browser.get_driver()

print("=" * 60)
print("Testing switch_phase()")
print("=" * 60)

switch_phase(
    driver,
    "Phase 3A"
)

input("Press Enter...")