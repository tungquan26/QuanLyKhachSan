from datetime import date
from io import BytesIO

from flask import send_file
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

def export_excel(rows, values, today):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sử dụng loại phòng"
    ws.sheet_view.showGridLines = False
    border = Border(**{key: Side(style="thin", color="000000")
                       for key in ("left", "right", "top", "bottom")})

    def merged(row, start, end, text, *, bold=False, size=11):
        ws.merge_cells(start_row=row, start_column=start, end_row=row, end_column=end)
        cell = ws.cell(row, start, text)
        cell.data_type = "s"
        cell.font = Font(name="Times New Roman", size=size, bold=bold)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    merged(1, 1, 4, "BÁO CÁO THỐNG KÊ SỬ DỤNG LOẠI PHÒNG", bold=True, size=16)
    ws.row_dimensions[1].height = 32
    start, end = (date.fromisoformat(values[key]).strftime("%d/%m/%Y")
                  for key in ("tu_ngay", "den_ngay"))
    merged(2, 1, 4, f"Từ ngày: {start} đến ngày: {end}", size=12)
    ws.row_dimensions[2].height = 24
    for col, label in enumerate(("STT", "LOẠI PHÒNG", "SỐ LƯỢT SỬ DỤNG", "SỐ PHÒNG ĐÃ DÙNG"), 1):
        ws.cell(4, col, label)
    for index, (_, name, uses, rooms) in enumerate(rows, 1):
        for col, value in enumerate((index, name, uses, rooms), 1):
            cell = ws.cell(index + 4, col, value)
            if col == 2:
                cell.data_type = "s"
    if not rows:
        merged(5, 1, 4, "Không có phòng được sử dụng trong khoảng ngày đã chọn.")
    total_row = 5 + max(len(rows), 1)
    merged(total_row, 1, 2, "TỔNG CỘNG", bold=True)
    ws.cell(total_row, 3, sum(row[2] for row in rows))
    ws.cell(total_row, 4, sum(row[3] for row in rows))
    for row in ws.iter_rows(min_row=4, max_row=total_row, max_col=4):
        ws.row_dimensions[row[0].row].height = 36
        for cell in row:
            cell.border = border
            cell.font = Font(name="Times New Roman", size=11, bold=cell.row in (4, total_row))
            cell.alignment = Alignment(horizontal="left" if cell.column == 2 else "center",
                                       vertical="center", wrap_text=True)
            if cell.row in (4, total_row):
                cell.fill = PatternFill("solid", fgColor="F2F2F2")
            if cell.column >= 3 and cell.row > 4:
                cell.number_format = "#,##0"
    sign = total_row + 2
    merged(sign, 3, 4, f"Ngày {today.day:02d} tháng {today.month:02d} năm {today.year}")
    for offset, left, right in (
        (1, "Người tạo báo cáo", "Ban Giám đốc"),
        (2, "Kế toán / Trưởng bộ phận Lễ tân", "(Người nhận)"),
        (3, "(Ký, ghi rõ họ tên)", "(Ký, ghi rõ họ tên)"),
    ):
        merged(sign + offset, 1, 2, left, bold=offset == 1)
        merged(sign + offset, 3, 4, right, bold=offset == 1)
        ws.row_dimensions[sign + offset].height = 26
    for index, width in enumerate((8, 46, 25, 25), 1):
        ws.column_dimensions[get_column_letter(index)].width = width
    ws.freeze_panes = "C5"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.orientation = "portrait"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_title_rows = "1:4"
    ws.print_area = f"A1:D{sign + 7}"
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return send_file(output, as_attachment=True,
                     download_name=f"Su_dung_loai_phong_{values['tu_ngay']}_den_{values['den_ngay']}.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
