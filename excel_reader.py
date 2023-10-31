import openpyxl
"""
excel_reader.py - Reads Excel files and stores the data.

Usage:
    from excel_reader import read_excel

Arguments:
    filename: The Excel file to read.

Description:
    This script contains functions for reading Excel files.
    It uses the openpyxl library to read Excel files and stores
    the data in a list of dictionaries for further processing.
"""


class ExcelReader:
    records = []

    def __init__(self, file_path):
        self.file_path = file_path
        self.records = []
        self.read_excel()

    def read_excel(self):
        # Load the workbook
        workbook = openpyxl.load_workbook(self.file_path)

        # Get the first sheet
        sheet = workbook.active

        # Get the headers (assuming they are in the first row)
        headers = [cell.value for cell in sheet[1]]

        rownum = 0
        # Populate records
        for row in sheet.iter_rows(min_row=2, values_only=True):
            record = {}
            rownum += 1
            for header, cell_value in zip(headers, row):
                # determine if cell_value is a string and trim it
                if isinstance(cell_value, str):
                    cv = cell_value.strip()
                else:
                    cv = cell_value
                record[header] = cv
            record["rownum"] = rownum
            self.records.append(record)

    def __str__(self):
        s = ''
        for record in self.records:
            s += f"{record}\n"
        return s

