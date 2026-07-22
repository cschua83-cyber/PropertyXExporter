import os

from openpyxl import Workbook
from datetime import datetime
from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment,
)

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

HEADER_FILL = PatternFill(
    fill_type="solid",
    start_color="1F4E78",
    end_color="1F4E78"
)

HEADER_FONT = Font(
    bold=True,
    color="FFFFFF"
)

CENTER_ALIGNMENT = Alignment(
    horizontal="center",
    vertical="center"
)


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
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        
        
    for u in units:
        print(type(u.size), u.size)
        
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

    ws.auto_filter.ref = ws.dimensions
    
    ws.freeze_panes = "A2"
    
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = CENTER_ALIGNMENT

    for cell in ws["E"][1:]:
        cell.number_format = '#,##0;-#,##0'

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