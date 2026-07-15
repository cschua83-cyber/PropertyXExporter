
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.models import Unit

UNIT_PATTERN = re.compile(
    r"^[A-Z]\d(?:-\d+)?-\d{2}-\d{2}$"
)

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


def scan_units(driver, phase, block):

    buttons = driver.find_elements(
        By.TAG_NAME,
        "button"
    )

    print(f"找到 Button 数量：{len(buttons)}")

    units = []
    current_level = ""

    for i, b in enumerate(buttons[:20]):
        print("-----")
        print(i)
        print(repr(b.text))

    for button in buttons:

        classes = button.get_attribute("class") or ""
                   
        # 已售直接跳过
        if "unavailable" in classes:
            continue
        
        # 没有 available 也跳过
        if "available" not in classes:
            continue
        
        text = button.text.strip()

        if not text:
            continue

        lines = text.splitlines()
        first = lines[0].strip()

        # 楼层按钮
        if re.fullmatch(r"\d+A?", first):
            current_level = first
            continue

        if not UNIT_PATTERN.match(first):
            continue

        u = Unit()

        u.phase = phase
        u.block = block
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


    time.sleep(2)
    
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
    
    time.sleep(1)
    
   

    try:
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(
                By.XPATH,
                "//div[text()='Unit']/following-sibling::div"
            ).text != old
        )
    except Exception:
        pass


    # ==========================================================
    # 等待 Detail 完全加载（最多重试 5 次）
    # ==========================================================
    detail = {}

    for attempt in range(5):

        detail = read_details(driver)

        # 正常都会有约 8 个字段
        if len(detail) >= 7:
                break

        print(f"Detail 尚未加载完成，等待中... ({attempt+1}/5)")

        time.sleep(0.5)

    print("\n" + "=" * 70)
    print(f"读取：{unit.unit}")
    print("=" * 70)

    if not detail:
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
        
    # ==========================================================
    # 关闭 Detail Dialog（ESC）
    # ==========================================================
    driver.find_element(
        By.TAG_NAME,
        "body"
    ).send_keys(Keys.ESCAPE)
    
    WebDriverWait(driver, 10).until(
    EC.invisibility_of_element_located(
        (By.CLASS_NAME, "cdk-overlay-backdrop")
    )
)

    time.sleep(1.5)

    print("Dialog 已关闭")

    WebDriverWait(driver, 5).until(
        EC.invisibility_of_element_located(
            (By.CLASS_NAME, "cdk-overlay-backdrop")
        )
    )

    time.sleep(0.3)

    m = re.search(r"(\d+)\s*Bathroom", type_text, re.I)
    if m:
        unit.bathroom = m.group(1)
    
    
def get_units(driver, phase, block):
    """
    读取当前 Block 的所有 Unit
    """

    print("=" * 60)
    print(f"Scanning Units ({phase} / {block})...")
    print("=" * 60)

    units = scan_units(driver, phase, block)

    print(f"发现 {len(units)} 个 Unit")

    for i, unit in enumerate(units):

        print(f"[{i+1}/{len(units)}] {unit.unit}")

        for retry in range(3):

            try:
                load_details(driver, unit)
                break

            except Exception as e:

                print(f"Retry {retry+1}: {e}")

                time.sleep(1)

    return units
