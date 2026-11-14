"""Báo cáo thống kê doanh thu theo chuẩn mẫu:
- Giao diện chọn loại báo cáo, khoảng ngày, công ty/chi nhánh (Hình 1).
- Hiển thị xem trước (Preview) tờ báo cáo A4 chuẩn (Hình 2).
- Xuất file Excel .xlsx được định dạng y hệt mẫu Hình 2.
"""

import io
from datetime import date, datetime, timedelta
from flask import Blueprint, current_app, flash, render_template, request, send_file
from mysql.connector import connect, Error
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from config import MYSQL

bao_cao_2_bp = Blueprint("bao_cao_2", __name__, template_folder="web/templates")


def _password():
    val = current_app.config.get("MYSQL_PASSWORD")
    if val is None:
        raise ValueError("Chưa nhập mật khẩu MySQL trong terminal.")
    return val


def _query_doanh_thu(tu_ngay: str, den_ngay: str):
    """Truy vấn doanh thu từ bảng LanSuDungDichVu."""
    sql = """
        SELECT
            dv.TenDichVu,
            dv.DonViTinh,
            SUM(ls.SoLuong)                   AS TongSoLuong,
            dv.DonGiaHienHanh                 AS DonGia,
            SUM(ls.SoLuong * ls.DonGiaApDung) AS ThanhTien
        FROM LanSuDungDichVu ls
        JOIN DichVu dv ON dv.MaDichVu = ls.MaDichVu
        WHERE DATE(ls.ThoiDiemSuDung) BETWEEN %s AND %s
        GROUP BY dv.MaDichVu, dv.TenDichVu, dv.DonViTinh, dv.DonGiaHienHanh
        ORDER BY ThanhTien DESC
    """
    with connect(**MYSQL, password=_password()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (tu_ngay, den_ngay))
            return cur.fetchall()


def _format_money(value):
    try:
        return f"{int(round(float(value))):,}"
    except (ValueError, TypeError):
        return "0"


@bao_cao_2_bp.route("/bao-cao/doanh-thu-dich-vu", methods=["GET", "POST"])
@bao_cao_2_bp.route("/bao_cao_2", methods=["GET", "POST"])
@bao_cao_2_bp.route("/bao-cao-2", methods=["GET", "POST"])
@bao_cao_2_bp.route("/bao-cao", methods=["GET", "POST"])
def bao_cao_doanh_thu_dich_vu():
    today = date.today()
    tu_ngay = request.form.get("tu_ngay", str(today - timedelta(days=30)))
    den_ngay = request.form.get("den_ngay", str(today))
    ten_cong_ty = request.form.get("ten_cong_ty", "Khách sạn Hotel Desk")
    loai_bao_cao = request.form.get("loai_bao_cao", "dich_vu")

    rows = []
    tong_cong = 0
    executed = False

    if request.method == "POST":
        executed = True
        if not tu_ngay or not den_ngay:
            flash("Vui lòng chọn đầy đủ Từ ngày và Đến ngày.", "error")
        elif tu_ngay > den_ngay:
            flash("Từ ngày không được lớn hơn Đến ngày.", "error")
        else:
            try:
                db_rows = _query_doanh_thu(tu_ngay, den_ngay)
                if db_rows:
                    rows = [
                        {
                            "ten": r[0],
                            "don_vi": r[1],
                            "so_luong": float(r[2]),
                            "don_gia": int(r[3]),
                            "thanh_tien": int(r[4]),
                        }
                        for r in db_rows
                    ]
                    tong_cong = sum(r["thanh_tien"] for r in rows)
                else:
                    flash("Không có dữ liệu trong khoảng ngày đã chọn.", "info")
            except (ValueError, Error) as err:
                flash(f"Lỗi truy vấn CSDL: {err}", "error")

    # Format ngày kiểu Việt Nam: Ngày dd tháng mm năm yyyy
    ngay_in = f"Ngày {today.day:02d} tháng {today.month:02d} năm {today.year}"

    return render_template(
        "bao_cao_2.html",
        active="bao_cao_2",
        tu_ngay=tu_ngay,
        den_ngay=den_ngay,
        ten_cong_ty=ten_cong_ty,
        loai_bao_cao=loai_bao_cao,
        rows=rows,
        tong_cong=tong_cong,
        executed=executed,
        ngay_in=ngay_in,
        format_money=_format_money,
    )


@bao_cao_2_bp.route("/bao-cao/doanh-thu-dich-vu/xuat-excel", methods=["POST"])
@bao_cao_2_bp.route("/bao_cao_2/xuat-excel", methods=["POST"])
@bao_cao_2_bp.route("/bao-cao-2/xuat-excel", methods=["POST"])
def xuat_excel_doanh_thu_dich_vu():
    tu_ngay = request.form.get("tu_ngay", "")
    den_ngay = request.form.get("den_ngay", "")
    ten_cong_ty = request.form.get("ten_cong_ty", "Khách sạn Hotel Desk").strip()

    try:
        db_rows = _query_doanh_thu(tu_ngay, den_ngay) if tu_ngay and den_ngay else []
    except (ValueError, Error):
        db_rows = []

    # Định dạng ngày hiển thị dd/mm/yyyy
    def format_date_vn(d_str):
        try:
            p = datetime.strptime(d_str, "%Y-%m-%d")
            return p.strftime("%d/%m/%Y")
        except Exception:
            return d_str

    tu_ngay_vn = format_date_vn(tu_ngay)
    den_ngay_vn = format_date_vn(den_ngay)
    today = date.today()
    ngay_in_vn = f"Ngày {today.day:02d} tháng {today.month:02d} năm {today.year}"

    # ── Tạo workbook Excel chuẩn mẫu Hình 2 ───────────────────────────
    wb = Workbook()
    ws = wb.active
    ws.title = "Báo cáo doanh thu"
    ws.views.sheetView[0].showGridLines = True

    # Font styles
    font_company = Font(name="Times New Roman", size=13, bold=True)
    font_title = Font(name="Times New Roman", size=16, bold=True)
    font_subtitle = Font(name="Times New Roman", size=12, italic=True)
    font_header = Font(name="Times New Roman", size=11, bold=True)
    font_data = Font(name="Times New Roman", size=11)
    font_total = Font(name="Times New Roman", size=11, bold=True)
    font_date = Font(name="Times New Roman", size=11, italic=True)
    font_sign_title = Font(name="Times New Roman", size=11, bold=True)
    font_sign_sub = Font(name="Times New Roman", size=10, italic=True)

    # Borders & Alignments
    thin = Side(style="thin", color="000000")
    border_all = Border(left=thin, right=thin, top=thin, bottom=thin)
    border_box = Border(left=thin, right=thin, top=thin, bottom=thin)

    center = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    right_align = Alignment(horizontal="right", vertical="center")

    # 1. Tên công ty / Đơn vị (Góc trên bên trái giống Hình 2)
    ws["A1"] = ten_cong_ty
    ws["A1"].font = font_company
    ws["A1"].alignment = left_align

    # 2. Tiêu đề chính giữa
    ws.merge_cells("A3:E3")
    ws["A3"] = "BÁO CÁO THỐNG KÊ DOANH THU DỊCH VỤ"
    ws["A3"].font = font_title
    ws["A3"].alignment = center

    # 3. Dòng ngày tháng phụ: Từ ngày: ... Đến ngày: ...
    ws.merge_cells("A4:E4")
    ws["A4"] = f"Từ ngày: {tu_ngay_vn} Đến ngày: {den_ngay_vn}"
    ws["A4"].font = font_subtitle
    ws["A4"].alignment = center

    # 4. Header Bảng (Giống bảng kẻ khung của Hình 2)
    start_row = 6
    headers = ["STT", "TÊN DỊCH VỤ", "ĐƠN VỊ TÍNH", "ĐƠN GIÁ", "THÀNH TIỀN"]
    ws.row_dimensions[start_row].height = 24

    for col_idx, h_text in enumerate(headers, start=1):
        cell = ws.cell(row=start_row, column=col_idx, value=h_text)
        cell.font = font_header
        cell.alignment = center
        cell.border = border_all
        cell.fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")

    # 5. Dữ liệu bảng
    current_row = start_row + 1
    tong_cong = 0

    if db_rows:
        for idx, r in enumerate(db_rows, start=1):
            ten_dv, don_vi, so_luong, don_gia, thanh_tien = r
            tong_cong += int(thanh_tien)
            ws.row_dimensions[current_row].height = 20

            # STT
            c1 = ws.cell(row=current_row, column=1, value=idx)
            c1.alignment = center
            # Tên dịch vụ
            c2 = ws.cell(row=current_row, column=2, value=f"{ten_dv} (x{int(so_luong)})")
            c2.alignment = left_align
            # Đơn vị tính
            c3 = ws.cell(row=current_row, column=3, value=don_vi)
            c3.alignment = center
            # Đơn giá
            c4 = ws.cell(row=current_row, column=4, value=int(don_gia))
            c4.alignment = right_align
            c4.number_format = "#,##0"
            # Thành tiền
            c5 = ws.cell(row=current_row, column=5, value=int(thanh_tien))
            c5.alignment = right_align
            c5.number_format = "#,##0"

            for c in range(1, 6):
                cell = ws.cell(row=current_row, column=c)
                cell.font = font_data
                cell.border = border_all

            current_row += 1
    else:
        # Nếu chưa có dữ liệu, hiển thị dòng trống có kẻ bảng
        ws.merge_cells(f"A{current_row}:E{current_row}")
        c = ws.cell(row=current_row, column=1, value="(Không có dữ liệu phát sinh trong kỳ)")
        c.font = font_subtitle
        c.alignment = center
        for col in range(1, 6):
            ws.cell(row=current_row, column=col).border = border_all
        current_row += 1

    # 6. Dòng TỔNG CỘNG
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
    c_sum.number_format = "#,##0"
    c_sum.border = border_all

    # 7. Phần chân trang bên phải: Ngày tháng và Người ký (Y hệt Hình 2)
    sign_row = current_row + 2
    
    # Ngày ... tháng ... năm ...
    ws.merge_cells(f"D{sign_row}:E{sign_row}")
    c_date = ws.cell(row=sign_row, column=4, value=ngay_in_vn)
    c_date.font = font_date
    c_date.alignment = center

    # Người tạo (Kế toán / Trưởng bộ phận Lễ tân)
    ws.cell(row=sign_row + 1, column=2, value="Người tạo báo cáo").font = font_sign_title
    ws.cell(row=sign_row + 1, column=2).alignment = center
    ws.cell(row=sign_row + 2, column=2, value="(Kế toán / Trưởng bộ phận Lễ tân)").font = font_sign_sub
    ws.cell(row=sign_row + 2, column=2).alignment = center
    ws.cell(row=sign_row + 3, column=2, value="(Ký, ghi rõ họ tên)").font = font_sign_sub
    ws.cell(row=sign_row + 3, column=2).alignment = center

    # Người nhận (Ban Giám đốc)
    ws.merge_cells(f"D{sign_row + 1}:E{sign_row + 1}")
    ws.cell(row=sign_row + 1, column=4, value="Ban Giám đốc").font = font_sign_title
    ws.cell(row=sign_row + 1, column=4).alignment = center
    ws.merge_cells(f"D{sign_row + 2}:E{sign_row + 2}")
    ws.cell(row=sign_row + 2, column=4, value="(Người nhận)").font = font_sign_sub
    ws.cell(row=sign_row + 2, column=4).alignment = center
    ws.merge_cells(f"D{sign_row + 3}:E{sign_row + 3}")
    ws.cell(row=sign_row + 3, column=4, value="(Ký, đóng dấu)").font = font_sign_sub
    ws.cell(row=sign_row + 3, column=4).alignment = center

    # Độ rộng các cột
    widths = [8, 38, 16, 20, 22]
    for idx, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(idx)].width = w

    # Xuất file ra BytesIO
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
