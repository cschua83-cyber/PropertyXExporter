from openpyxl import Workbook
from datetime import datetime


def export_to_excel(units):

    wb = Workbook()
    ws = wb.active
    ws.title = "Units"

    ws.append([
        "Phase",
        "Block",
        "Level",
        "Unit",
        "Price",
        "Bedroom",
        "Bathroom",
        "Built-up",
        "Direction",
        "Car Park",
        "Status"
    ])

    for u in units:
        ws.append([
            u.phase,
            u.block,
            u.level,
            u.unit,
            u.price,
            u.bedroom,
            u.bathroom,
            u.size,
            u.orientation,
            u.carpark,
            u.status
        ])

    filename = f"output/Units_{datetime.now():%Y%m%d_%H%M%S}.xlsx"

    wb.save(filename)

    print(f"✅ Excel 已输出：{filename}")