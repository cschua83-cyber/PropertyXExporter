HEADERS = [
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
]

import os

from openpyxl import Workbook
from datetime import datetime
from openpyxl.styles import Font


def export_to_excel(units):
    
    os.makedirs(
    "output",
    exist_ok=True
    )

    wb = Workbook()
    ws = wb.active
    ws.title = "Units"

    ws.append(HEADERS)
    
    for cell in ws[1]:
        cell.font = Font(bold=True)

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
    
    for column in ws.columns:

        max_length = 0
        column_letter = column[0].column_letter

        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass

        ws.column_dimensions[column_letter].width = max_length + 2

    wb.save(filename)

    print(f"✅ Excel 已输出：{filename}")