# agentic-spreadsheet-processor/create_input_data.py
"""Helper script: creates data/input_data.xlsx (sheet 'SalesData') with the sample data from the lab."""
import os
import openpyxl
from openpyxl.styles import Font

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "input_data.xlsx")
os.makedirs(os.path.dirname(path), exist_ok=True)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "SalesData"
rows = [
    ["Product Name", "Quantity", "Unit Price"],
    ["Laptop", 2, 1200.50],
    ["Mouse", 5, 25.00],
    ["Keyboard", 3, 75.99],
    ["Monitor", 1, 300.00],
    ["Projector", 1, 850.00],
    ["Webcam", 10, 45.00],
    ["Headset", 4, 99.99],
    ["SSD", 2, 180.00],
    ["Router", 1, 70.00],
]
for r in rows:
    ws.append(r)
for c in ws[1]:
    c.font = Font(bold=True)
ws.column_dimensions["A"].width = 16
ws.column_dimensions["B"].width = 12
ws.column_dimensions["C"].width = 12
wb.save(path)
print("Created", path)
