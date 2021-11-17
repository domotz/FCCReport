from typing import Optional

from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

from . import ReportBuilder, AbstractCell, StringCell, HyperLinkCell, NumberCell


class ExcelReport(ReportBuilder):
    def __init__(self):
        self.workbook: Optional[Workbook] = None
        self.worksheet: Optional[Worksheet] = None

    def create(self, file_name: str):
        self.workbook = Workbook(f"{file_name}.xlsx")

        self.worksheet = self.workbook.add_worksheet()

    def header(self, headers_labels) -> int:
        bold = self.workbook.add_format({"bold": True})
        self.worksheet.autofilter("A1:J1")
        self.worksheet.freeze_panes(1, 0)
        row = 0
        col = 0
        for title in headers_labels:
            self.worksheet.write(row, col, title, bold)
            col += 1
        return row + 1

    def write(self, row, col, cell: AbstractCell):

        if isinstance(cell, StringCell):
            self.worksheet.write_string(row, col, string=cell.text)

        elif isinstance(cell, HyperLinkCell):
            self.worksheet.write_url(row, col, cell.url, string=cell.label)

        elif isinstance(cell, NumberCell):
            self.worksheet.write_number(row, col, cell.number)

    def close(self):
        self.workbook.close()
