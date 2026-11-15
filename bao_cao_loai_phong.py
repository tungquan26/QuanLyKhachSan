"""Room-type booking report: on-screen preview and printable Excel export."""
import io
import re
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP

from flask import Blueprint, render_template, request, send_file
from mysql.connector import Error
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.pagebreak import Break

import database
from web.routes import notify_error, password


room_report_bp = Blueprint("room_report", __name__)
TITLE = "Báo cáo thống kê lượt đặt phòng theo loại phòng"
SCOPE = "Không bao gồm các phiếu đặt phòng đã hủy."
METHOD = "Mỗi phòng trong một phiếu được tính là một lượt đặt; kỳ báo cáo tính theo ngày đặt."
RATIO_NOTE = "Tỷ lệ = số lượt đặt của loại phòng / tổng lượt đặt × 100%. Có thể có chênh lệch do làm tròn."
AUTHOR_ROLE = "Trưởng bộ phận Lễ tân"
RECIPIENT = "Ban Giám đốc khách sạn"


def _today():
    return datetime.now(timezone(timedelta(hours=7))).date()


def _validate(values):
    dates = []
    for key, label in (("tu_ngay", "Từ ngày"), ("den_ngay", "Đến ngày")):
        try:
            if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", values[key]):
                raise ValueError
            dates.append(date.fromisoformat(values[key]))
        except ValueError:
            raise ValueError(f"{label} phải là ngày hợp lệ theo định dạng năm-tháng-ngày.") from None
    if dates[0] > dates[1]:
        raise ValueError("Từ ngày không được lớn hơn Đến ngày.")
    hotel_name = values["ten_khach_san"]
    if not 1 <= len(hotel_name) <= 100:
        raise ValueError("Tên khách sạn phải có từ 1 đến 100 ký tự.")
    if any(ord(char) < 32 for char in hotel_name):
        raise ValueError("Tên khách sạn không được chứa ký tự điều khiển hoặc xuống dòng.")
    return dates


def _report(db_rows):
    total = sum(row[2] for row in db_rows)
    return {
        "rows": [
            {"name": name, "count": count,
             "share": Decimal(count) / Decimal(total) if total else Decimal(0)}
            for _, name, count in db_rows
        ],
        "total": total,
        "total_share": Decimal(1) if total else Decimal(0),
    }


def _format_percent(share):
    return str((share * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)).replace(".", ",")


def _date_label(day):
    return f"Ngày {day.day:02d} tháng {day.month:02d} năm {day.year}"


def _render(values, today, report=None, period=None, status=200):
    return render_template(
        "bao_cao_loai_phong.html", active="room_report", values=values,
        report=report, period=period, title=TITLE, scope=SCOPE, method=METHOD,
        ratio_note=RATIO_NOTE, author_role=AUTHOR_ROLE, recipient=RECIPIENT,
        issued_on=_date_label(today), format_percent=_format_percent,
        format_count=lambda value: f"{value:,}".replace(",", "."),
    ), status


def _report_request(*, export=False):
    today = _today()
    if request.method == "GET":
        return _render({
            "tu_ngay": str(today.replace(day=1)), "den_ngay": str(today),
            "ten_khach_san": "Khách sạn Hotel Desk",
        }, today)
    values = {key: request.form.get(key, "").strip()
              for key in ("tu_ngay", "den_ngay", "ten_khach_san")}
    try:
        start, end = _validate(values)
        report = _report(database.list_room_type_bookings(start, end, password()))
    except (ValueError, Error) as error:
        notify_error(error)
        return _render(values, today, status=400 if isinstance(error, ValueError) else 503)
    period = f"Từ ngày {start:%d/%m/%Y} đến ngày {end:%d/%m/%Y}"
    if not export:
        return _render(values, today, report, period)
    output = _excel(report, values, today, period)
    return send_file(
        output, as_attachment=True,
        download_name=f"Luot_dat_theo_loai_phong_{start}_den_{end}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@room_report_bp.route("/bao-cao/loai-phong", methods=["GET", "POST"])
def preview():
    return _report_request()


@room_report_bp.post("/bao-cao/loai-phong/xuat-excel")
def export_excel():
    return _report_request(export=True)


def _paginate(sheet, total_row, last_row):
    """Keep the last two data rows, total and signature together on A4.

    Heights are in points. Reserve 24 points for printer differences; use
    100% scaling so Excel honours manual breaks and keeps the font readable.
    The four fixed-width columns already fit the printable A4 width.
    """
    def height(first, last):
        return sum(sheet.row_dimensions[row].height or sheet.sheet_format.defaultRowHeight
                   for row in range(first, last + 1))

    page_height = 297 / 25.4 * 72
    available = page_height - (sheet.page_margins.top + sheet.page_margins.bottom) * 72 - 24
    header_height = height(1, 9)
    used = header_height
    tail_start = max(10, total_row - 2)
    groups = [(row, row) for row in range(10, tail_start)] + [(tail_start, last_row)]
    for first, last in groups:
        group_height = height(first, last)
        if used + group_height > available and used > header_height:
            sheet.row_breaks.append(Break(id=first - 1))
            used = header_height
        used += group_height


def _excel(report, values, today, period):
    """Export the same calculated report used by the HTML preview."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Lượt đặt theo loại phòng"
    sheet.sheet_view.showGridLines = False
    sheet.freeze_panes = "C10"
    border = Border(**{edge: Side(style="thin", color="777777")
                       for edge in ("left", "right", "top", "bottom")})

    def cell(row, column, value, *, bold=False, size=11, align="left", italic=False):
        target = sheet.cell(row, column, value)
        if isinstance(value, str):
            # All user/database text stays literal, even when it starts with '='.
            target.data_type = "s"
        target.font = Font(name="Times New Roman", size=size, bold=bold, italic=italic)
        target.alignment = Alignment(horizontal=align, vertical="center", wrap_text=True)
        return target

    def merged(row, first, last, value, **style):
        sheet.merge_cells(start_row=row, start_column=first, end_row=row, end_column=last)
        return cell(row, first, value, **style)

    merged(1, 1, 4, values["ten_khach_san"], bold=True, size=13)
    sheet.row_dimensions[1].height = 40
    merged(3, 1, 4, "BÁO CÁO THỐNG KÊ LƯỢT ĐẶT PHÒNG\nTHEO LOẠI PHÒNG",
           bold=True, size=15, align="center")
    sheet.row_dimensions[3].height = 44
    merged(4, 1, 4, period, italic=True, align="center")
    sheet.row_dimensions[4].height = 24
    merged(6, 1, 4, f"Kính gửi: {RECIPIENT}", bold=True)
    sheet.row_dimensions[6].height = 22
    merged(7, 1, 4, SCOPE, italic=True)
    sheet.row_dimensions[7].height = 22

    for column, label in enumerate(("STT", "LOẠI PHÒNG", "SỐ LƯỢT ĐẶT", "TỶ LỆ (%)"), 1):
        header = cell(9, column, label, bold=True, align="center")
        header.fill = PatternFill("solid", fgColor="EDEDED")
        header.border = border
    sheet.row_dimensions[9].height = 30

    row_number = 10
    for index, item in enumerate(report["rows"], 1):
        cell(row_number, 1, index, align="center")
        cell(row_number, 2, item["name"])
        cell(row_number, 3, item["count"], align="right").number_format = "#,##0"
        cell(row_number, 4, item["share"], align="right").number_format = "0.00%"
        for column in range(1, 5):
            sheet.cell(row_number, column).border = border
        sheet.row_dimensions[row_number].height = 54 if len(item["name"]) > 35 else 28
        row_number += 1
    if not report["rows"]:
        merged(row_number, 1, 4, "Chưa có danh mục loại phòng.", italic=True, align="center")
        for column in range(1, 5):
            sheet.cell(row_number, column).border = border
        sheet.row_dimensions[row_number].height = 28
        row_number += 1

    total_row = row_number
    merged(row_number, 1, 2, "TỔNG CỘNG", bold=True, align="center")
    cell(row_number, 3, report["total"], bold=True, align="right").number_format = "#,##0"
    cell(row_number, 4, report["total_share"], bold=True, align="right").number_format = "0.00%"
    for column in range(1, 5):
        sheet.cell(row_number, column).border = border
        sheet.cell(row_number, column).fill = PatternFill("solid", fgColor="EDEDED")
    sheet.row_dimensions[row_number].height = 28

    if report["total"] == 0:
        row_number += 1
        merged(row_number, 1, 4, "Không phát sinh lượt đặt hợp lệ trong kỳ.", italic=True)
        sheet.row_dimensions[row_number].height = 24
    note_row = row_number + 2
    merged(note_row, 1, 4, METHOD, italic=True)
    merged(note_row + 1, 1, 4, RATIO_NOTE, italic=True)
    sheet.row_dimensions[note_row].height = 32
    sheet.row_dimensions[note_row + 1].height = 32
    sign_row = note_row + 3
    merged(sign_row, 3, 4, _date_label(today), italic=True, align="center")
    sheet.row_dimensions[sign_row].height = 28
    for first, last, label, role in ((1, 2, "NGƯỜI LẬP BÁO CÁO", AUTHOR_ROLE),
                                    (3, 4, "NGƯỜI NHẬN", RECIPIENT)):
        merged(sign_row + 1, first, last, label, bold=True, align="center")
        merged(sign_row + 2, first, last, role, align="center")
        merged(sign_row + 3, first, last, "(Ký, ghi rõ họ tên)", italic=True, align="center")
    for offset in (1, 2, 3):
        sheet.row_dimensions[sign_row + offset].height = 22
    last_row = sign_row + 4
    sheet.row_dimensions[last_row].height = 64

    for column, width in (("A", 7), ("B", 41), ("C", 19), ("D", 19)):
        sheet.column_dimensions[column].width = width
    sheet.sheet_properties.pageSetUpPr.fitToPage = False
    sheet.page_setup.paperSize = sheet.PAPERSIZE_A4
    sheet.page_setup.orientation = "portrait"
    sheet.page_setup.scale = 100
    sheet.page_margins = PageMargins(left=0.35, right=0.35, top=0.4, bottom=0.4,
                                     header=0.15, footer=0.2)
    sheet.print_options.horizontalCentered = True
    sheet.print_title_rows = "1:9"
    sheet.print_area = f"A1:D{last_row}"
    sheet.oddFooter.center.text = "Trang &P / &N"
    _paginate(sheet, total_row, last_row)

    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    return output
