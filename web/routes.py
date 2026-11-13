from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from mysql.connector import Error
import database
from . import validation

pages = Blueprint("pages", __name__)


def password():
    value = current_app.config["MYSQL_PASSWORD"]
    if value is None:
        raise ValueError("Chưa cấu hình kết nối. Hãy chạy python app.py và nhập mật khẩu MySQL trong terminal.")
    return value


def notify_error(error):
    if isinstance(error, ValueError):
        message = str(error)
    elif error.errno == 1062:
        message = "CCCD bị trùng, đã có trong hệ thống."
    elif error.errno == 1644:
        message = error.msg
    else:
        messages = {
            1045: "MySQL từ chối đăng nhập. Hãy dừng web bằng Ctrl+C, chạy lại app.py và nhập đúng mật khẩu MySQL như trong Workbench.",
            1049: "Chưa có database hotel. Hãy tạo schema hotel và chạy các tệp SQL theo README.md.",
            1146: "Database hotel đang thiếu bảng cần thiết. Hãy kiểm tra các bảng được tạo từ sql/khach-san.sql trong Workbench.",
            1044: "Tài khoản MySQL chưa có quyền truy cập database hotel.",
            1142: "Tài khoản MySQL chưa có quyền thao tác trên bảng dữ liệu.",
            2002: "Không kết nối được MySQL. Kiểm tra dịch vụ MySQL, địa chỉ và cổng kết nối.",
            2003: "Không kết nối được MySQL. Kiểm tra dịch vụ MySQL, địa chỉ và cổng kết nối.",
            2013: "Kết nối MySQL bị gián đoạn. Hãy kiểm tra MySQL và thử lại.",
            2014: "Chưa xử lý xong phản hồi MySQL. Hãy khởi động lại web để dùng bản sửa mới rồi thử lại.",
        }
        message = messages.get(error.errno, "Không thể thao tác với cơ sở dữ liệu. Hãy cung cấp mã lỗi bên dưới để kiểm tra.")
        message += f" (Mã MySQL: {error.errno if error.errno is not None else 'không có'})"
        current_app.logger.error("MySQL operation failed: errno=%s sqlstate=%s", error.errno, error.sqlstate)
    flash(message, "error")


@pages.get("/")
def index():
    return redirect(url_for("pages.guests"))


def data_list(fetch_rows, *, active, title, columns, table_name, create_endpoint, create_label):
    rows = None
    status = 200
    try:
        rows = fetch_rows(password())
    except (ValueError, Error) as error:
        notify_error(error)
        status = 503
    return render_template(
        "data_list.html", active=active, list_title=title, columns=columns,
        table_name=table_name, rows=rows, create_endpoint=create_endpoint,
        create_label=create_label,
    ), status


@pages.get("/danh-sach/khach-hang")
def guest_list():
    return data_list(
        database.list_guests, active="guest_list", title="Danh sách khách hàng",
        columns=("MaKhachHang", "HoTen", "CCCD", "SoDienThoai"),
        table_name="KhachHang", create_endpoint="guests", create_label="Thêm khách hàng",
    )


@pages.get("/danh-sach/dich-vu")
def service_list():
    return data_list(
        database.list_services, active="service_list", title="Danh sách dịch vụ",
        columns=("MaDichVu", "TenDichVu", "DonViTinh", "DonGiaHienHanh", "TrangThai"),
        table_name="DichVu", create_endpoint="services", create_label="Thêm dịch vụ",
    )


@pages.route("/khach-hang", methods=["GET", "POST"])
def guests():
    values = {key: request.form.get(key, "").strip() for key in ("name", "cccd", "phone")}
    status = 200
    if request.method == "POST":
        try:
            action = request.form.get("action")
            if action == "save":
                validation.guest(values)
                database.add_guest(values["name"], values["cccd"], values["phone"], password())
                flash(f"Đã lưu hồ sơ của {values['name']}.", "success")
                return redirect(url_for("pages.guests"), code=303)
            else:
                raise ValueError("Thao tác không hợp lệ.")
        except (ValueError, Error) as error:
            notify_error(error)
            status = 400 if isinstance(error, ValueError) else 409 if error.errno == 1062 else 503
    return render_template("guests.html", active="guests", values=values), status


@pages.route("/dich-vu", methods=["GET", "POST"])
def services():
    values = {key: request.form.get(key, "").strip() for key in ("name", "unit", "price", "status")}
    if request.method == "GET":
        values["status"] = validation.SERVICE_STATUSES[0]
    status = 200
    if request.method == "POST":
        try:
            price = validation.service(values)
            database.add_service(values["name"], values["unit"], price, values["status"], password())
            flash(f"Đã lưu dịch vụ {values['name']}.", "success")
            return redirect(url_for("pages.services"), code=303)
        except (ValueError, Error) as error:
            notify_error(error)
            status = 400 if isinstance(error, ValueError) else 503
    return render_template("services.html", active="services", values=values,
                           statuses=validation.SERVICE_STATUSES), status
