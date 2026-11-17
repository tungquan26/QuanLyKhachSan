import io
import re
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from flask import Blueprint, render_template, request, send_file
from mysql.connector import Error
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import database
from web.routes import notify_error, password

bao_cao_2_bp = Blueprint("bao_cao_2", __name__)

def _today():
    return datetime.now(timezone(timedelta(hours=7))).date()

def _format_money(value):
    return f"{Decimal(value):,.2f}".rstrip("0").rstrip(".")

def _validate(values):
    parsed = []
    for key, label in (("tu_ngay", "Từ ngày"), ("den_ngay", "Đến ngày")):
        value = values[key]
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
            raise ValueError(f"{label} phải là ngày hợp lệ theo định dạng năm-tháng-ngày.")
        try:
            parsed.append(date.fromisoformat(value))
        except ValueError:
            raise ValueError(f"{label} không hợp lệ.") from None
    if parsed[0] > parsed[1]:
        raise ValueError("Từ ngày không được lớn hơn Đến ngày.")
    return parsed

def _render_report(values, rows=None, status=200):
    today = _today()
    return render_template(
        "bao_cao_2.html", active="bao_cao_2", **values, rows=rows,
        tong_cong=sum((r[4] for r in rows or []), Decimal(0)),
        ngay_in=f"Ngày {today.day:02d} tháng {today.month:02d} năm {today.year}",
        format_money=_format_money,
    ), status

def _report_request(*, export=False):
    today = _today()
    if request.method == "GET":
        return _render_report({
            "tu_ngay": str(today - timedelta(days=30)), "den_ngay": str(today),
        })
    values = {key: request.form.get(key, "").strip()
              for key in ("tu_ngay", "den_ngay")}
    try:
        start_date, end_date = _validate(values)
        rows = database.list_service_revenue(start_date, end_date, password())
    except (ValueError, Error) as error:
        notify_error(error)
        return _render_report(values, status=400 if isinstance(error, ValueError) else 503)
    if export:
        return _excel(rows, values, today)
    return _render_report(values, rows=rows)

@bao_cao_2_bp.route("/bao_cao_2", methods=["GET", "POST"])
@bao_cao_2_bp.route("/bao-cao-2", methods=["GET", "POST"])
@bao_cao_2_bp.route("/bao-cao", methods=["GET", "POST"])
@bao_cao_2_bp.route("/bao-cao/doanh-thu-dich-vu", methods=["GET", "POST"])
def bao_cao_doanh_thu_dich_vu():
    return _report_request()

@bao_cao_2_bp.post("/bao_cao_2/xuat-excel")
@bao_cao_2_bp.post("/bao-cao-2/xuat-excel")
@bao_cao_2_bp.post("/bao-cao/doanh-thu-dich-vu/xuat-excel")
def xuat_excel_doanh_thu_dich_vu():
    return _report_request(export=True)

def _excel(db_rows, values, today):
    tu_ngay, den_ngay = (values[k] for k in ("tu_ngay", "den_ngay"))
    tu_ngay_vn = date.fromisoformat(tu_ngay).strftime("%d/%m/%Y")
    den_ngay_vn = date.fromisoformat(den_ngay).strftime("%d/%m/%Y")
    ngay_in_vn = f"Ngày {today.day:02d} tháng {today.month:02d} năm {today.year}"

    wb = Workbook()
    ws = wb.active
    ws.title = "Báo cáo doanh thu"
    ws.views.sheetView[0].showGridLines = True

    font_title = Font(name="Times New Roman", size=16, bold=True)
    font_subtitle = Font(name="Times New Roman", size=12, italic=True)
    font_header = Font(name="Times New Roman", size=11, bold=True)
    font_data = Font(name="Times New Roman", size=11)
    font_total = Font(name="Times New Roman", size=11, bold=True)
    font_date = Font(name="Times New Roman", size=11, italic=True)
    font_sign_title = Font(name="Times New Roman", size=11, bold=True)
    font_sign_sub = Font(name="Times New Roman", size=10, italic=True)

    thin = Side(style="thin", color="000000")
    border_all = Border(left=thin, right=thin, top=thin, bottom=thin)

    center = Alignment(horizontal="center", vertical="center")
    right_align = Alignment(horizontal="right", vertical="center")

    ws.merge_cells("A3:E3")
    ws["A3"] = "BÁO CÁO THỐNG KÊ DOANH THU DỊCH VỤ"
    ws["A3"].font = font_title
    ws["A3"].alignment = center

    ws.merge_cells("A4:E4")
    ws["A4"] = f"Từ ngày: {tu_ngay_vn} Đến ngày: {den_ngay_vn}"
    ws["A4"].font = font_subtitle
    ws["A4"].alignment = center

    start_row = 6
    headers = ["STT", "TÊN DỊCH VỤ", "ĐƠN VỊ TÍNH", "ĐƠN GIÁ", "THÀNH TIỀN"]
    ws.row_dimensions[start_row].height = 24

    for col_idx, h_text in enumerate(headers, start=1):
        cell = ws.cell(row=start_row, column=col_idx, value=h_text)
        cell.font = font_header
        cell.alignment = center
        cell.border = border_all
        cell.fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")

    current_row = start_row + 1
    tong_cong = Decimal(0)

    if db_rows:
        for idx, r in enumerate(db_rows, start=1):
            ten_dv, don_vi, so_luong, don_gia, thanh_tien = r
            tong_cong += thanh_tien
            ws.row_dimensions[current_row].height = 48

            c1 = ws.cell(row=current_row, column=1, value=idx)
            c1.alignment = center

            c2 = ws.cell(row=current_row, column=2, value=f"{ten_dv} (x{_format_money(so_luong)})")
            c2.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            c2.data_type = "s"

            c3 = ws.cell(row=current_row, column=3, value=don_vi)
            c3.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            c3.data_type = "s"

            c4 = ws.cell(row=current_row, column=4, value=don_gia)
            c4.alignment = right_align
            c4.number_format = "#,##0.##"

            c5 = ws.cell(row=current_row, column=5, value=thanh_tien)
            c5.alignment = right_align
            c5.number_format = "#,##0.##"

            for c in range(1, 6):
                cell = ws.cell(row=current_row, column=c)
                cell.font = font_data
                cell.border = border_all

            current_row += 1
    else:

        ws.merge_cells(f"A{current_row}:E{current_row}")
        c = ws.cell(row=current_row, column=1, value="(Không có dữ liệu phát sinh trong kỳ)")
        c.font = font_subtitle
        c.alignment = center
        for col in range(1, 6):
            ws.cell(row=current_row, column=col).border = border_all
        current_row += 1

    ws.row_dimensions[current_row].height = 22
    ws.merge_cells(f"A{current_row}:D{current_row}")
    c_label = ws.cell(row=current_row, column=1, value="TỔNG CỘNG")
    c_label.font = font_total
    c_label.alignment = center
    for col in range(1, 5):
        ws.cell(row=current_row, column=col).border = border_all

    c_sum = ws.cell(row=current_row, column=5, value=tong_cong)
    c_sum.font = font_total
    c_sum.alignment = right_align
    c_sum.number_format = "#,##0.##"
    c_sum.border = border_all

    sign_row = current_row + 2

    ws.merge_cells(f"D{sign_row}:E{sign_row}")
    c_date = ws.cell(row=sign_row, column=4, value=ngay_in_vn)
    c_date.font = font_date
    c_date.alignment = center

    ws.cell(row=sign_row + 1, column=2, value="Người tạo báo cáo").font = font_sign_title
    ws.cell(row=sign_row + 1, column=2).alignment = center
    ws.cell(row=sign_row + 2, column=2, value="(Kế toán / Trưởng bộ phận Lễ tân)").font = font_sign_sub
    ws.cell(row=sign_row + 2, column=2).alignment = center
    ws.cell(row=sign_row + 3, column=2, value="(Ký, ghi rõ họ tên)").font = font_sign_sub
    ws.cell(row=sign_row + 3, column=2).alignment = center

    ws.merge_cells(f"D{sign_row + 1}:E{sign_row + 1}")
    ws.cell(row=sign_row + 1, column=4, value="Ban Giám đốc").font = font_sign_title
    ws.cell(row=sign_row + 1, column=4).alignment = center
    ws.merge_cells(f"D{sign_row + 2}:E{sign_row + 2}")
    ws.cell(row=sign_row + 2, column=4, value="(Người nhận)").font = font_sign_sub
    ws.cell(row=sign_row + 2, column=4).alignment = center
    ws.merge_cells(f"D{sign_row + 3}:E{sign_row + 3}")
    ws.cell(row=sign_row + 3, column=4, value="(Ký, đóng dấu)").font = font_sign_sub
    ws.cell(row=sign_row + 3, column=4).alignment = center

    widths = [8, 38, 16, 20, 22]
    for idx, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(idx)].width = w

    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.orientation = "portrait"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_title_rows = "1:6"
    ws.print_area = f"A1:E{sign_row + 7}"

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    filename = f"Doanh_thu_{tu_ngay}_den_{den_ngay}.xlsx"
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
