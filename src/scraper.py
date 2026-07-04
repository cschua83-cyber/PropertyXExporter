
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.models import Unit


def read_details(driver):
    """
    读取右侧 Detail Panel，返回:
    {
        "Type": "...",
        "Built-up": "...",
        ...
    }
    """
    data = {}

    rows = driver.find_elements(By.CLASS_NAME, "content-wrapper")

    for row in rows:
        try:
            label = row.find_element(By.CLASS_NAME, "label-f").text.strip()
            value = row.find_element(By.CLASS_NAME, "value-f").text.strip()

            if label and value:
                data[label] = value

        except Exception:
            continue

    return data


def scan_units(driver):

    buttons = driver.find_elements(
        By.TAG_NAME,
        "button"
    )

    print(f"找到 Button 数量：{len(buttons)}")

    for i, b in enumerate(buttons[:20]):
        print("-----")
        print(i)
        print(repr(b.text))

    units = []
    current_level = ""

    for button in buttons:

        text = button.text.strip()

        if not text:
            continue

        lines = text.splitlines()
        first = lines[0].strip()

        # 楼层按钮
        if re.fullmatch(r"\d+A?", first):
            current_level = first
            continue

        # 非 Unit
        if not first.startswith("C1-"):
            continue

        u = Unit()

        u.phase = "3A"
        u.block = "C1"
        u.level = current_level
        u.unit = first

        if len(lines) >= 2:
            price = (
                lines[1]
                .replace("monetization_on", "")
                .replace(",", "")
                .strip()
            )

            if price.isdigit():
                u.price = price

        units.append(u)

    return units


def load_details(driver, unit):
    """
    点击 Unit，并读取右侧 Detail
    """

    xpath = f"//button[contains(.,'{unit.unit}')]"

    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        button
    )

    old = ""

    try:
        old = driver.find_element(
            By.XPATH,
            "//div[text()='Unit']/following-sibling::div"
        ).text
    except Exception:
        pass

    driver.execute_script(
        "arguments[0].click();",
        button
    )

    try:
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(
                By.XPATH,
                "//div[text()='Unit']/following-sibling::div"
            ).text != old
        )
    except Exception:
        pass

    print()
print("=" * 80)
print("DEBUG")

print(
    "content-wrapper :",
    len(driver.find_elements(By.CLASS_NAME, "content-wrapper"))
)

print(
    "label-f :",
    len(driver.find_elements(By.CLASS_NAME, "label-f"))
)

print(
    "value-f :",
    len(driver.find_elements(By.CLASS_NAME, "value-f"))
)

print("=" * 80)
print()

detail = read_details(driver)

print("\n" + "=" * 70)
print(f"读取：{unit.unit}")
print("=" * 70)

if not detail:
    print("没有读取到 Detail")
        print("没有读取到 Detail")
    else:
        for k, v in detail.items():
            print(f"{k:<20}: {v}")

    print("=" * 70)

    # 映射到现有 models.py
    unit.size = detail.get("Built-up", "")
    unit.orientation = detail.get("Direction", "")
    unit.carpark = detail.get("Car Park", "")
    unit.status = detail.get("Status", "")

    type_text = detail.get("Type", "")

    m = re.search(r"(\d+)\s*Bedroom", type_text, re.I)
    if m:
        unit.bedroom = m.group(1)

    m = re.search(r"(\d+)\s*Bathroom", type_text, re.I)
    if m:
        unit.bathroom = m.group(1)


def get_units(browser):
    """
    主流程
    """

    driver = browser.driver

    print("=" * 60)
    print("Scanning Units...")
    print("=" * 60)

    units = scan_units(driver)

    print(f"发现 {len(units)} 个 Unit")

    # 测试只抓第一间，验证成功后改成 units
    for i, unit in enumerate(units[:1]):

        print(f"[{i+1}/{len(units)}] {unit.unit}")

        for retry in range(3):
            try:
                load_details(driver, unit)
                break
            except Exception as e:
                print(f"Retry {retry+1}: {e}")
                time.sleep(1)

    return units
