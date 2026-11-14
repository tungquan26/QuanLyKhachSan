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
        columns=("STT", "HoTen", "CCCD", "SoDienThoai"),
        table_name="KhachHang", create_endpoint="guests", create_label="Thêm khách hàng",
    )


@pages.get("/danh-sach/dich-vu")
def service_list():
    return data_list(
        database.list_services, active="service_list", title="Danh sách dịch vụ",
        columns=("STT", "TenDichVu", "DonViTinh", "DonGiaHienHanh", "TrangThai"),
        table_name="DichVu", create_endpoint="services", create_label="Thêm dịch vụ",
    )


@pages.route("/khach-hang/<int:record_id>/sua", methods=["GET", "POST"], endpoint="edit_guest")
@pages.route("/khach-hang", methods=["GET", "POST"])
def guests(record_id=None):
    values = {key: request.form.get(key, "").strip() for key in ("name", "cccd", "phone")}
    status = 200
    if record_id is not None and request.method == "GET":
        try:
            row = database.get_guest(record_id, password())
            values = dict(zip(("name", "cccd", "phone"), ("" if v is None else str(v) for v in row)))
        except database.RecordNotFound:
            flash("Khách hàng không còn tồn tại. Hãy chọn lại từ danh sách.", "error")
            return redirect(url_for("pages.guest_list"), code=303)
        except (ValueError, Error) as error:
            notify_error(error)
            return redirect(url_for("pages.guest_list"), code=303)
    if request.method == "POST":
        try:
            action = request.form.get("action")
            if action == "save":
                validation.guest(values)
                if record_id is not None:
                    database.update_guest(record_id, values["name"], values["cccd"], values["phone"], password())
                    flash(f"Đã cập nhật hồ sơ của {values['name']}.", "success")
                    return redirect(url_for("pages.guest_list"), code=303)
                database.add_guest(values["name"], values["cccd"], values["phone"], password())
                flash(f"Đã lưu hồ sơ của {values['name']}.", "success")
                return redirect(url_for("pages.guests"), code=303)
            else:
                raise ValueError("Thao tác không hợp lệ.")
        except database.RecordNotFound:
            flash("Khách hàng không còn tồn tại. Hãy chọn lại từ danh sách.", "error")
            return redirect(url_for("pages.guest_list"), code=303)
        except (ValueError, Error) as error:
            notify_error(error)
            status = 400 if isinstance(error, ValueError) else 409 if error.errno == 1062 else 503
    return render_template("guests.html", active="guest_list" if record_id is not None else "guests",
                           values=values, editing=record_id is not None), status


@pages.route("/dich-vu/<int:record_id>/sua", methods=["GET", "POST"], endpoint="edit_service")
@pages.route("/dich-vu", methods=["GET", "POST"])
def services(record_id=None):
    values = {key: request.form.get(key, "").strip() for key in ("name", "unit", "price", "status")}
    if request.method == "GET":
        values["status"] = validation.SERVICE_STATUSES[0]
    status = 200
    if record_id is not None and request.method == "GET":
        try:
            row = database.get_service(record_id, password())
            values = dict(zip(("name", "unit", "price", "status"), ("" if v is None else str(v) for v in row)))
        except database.RecordNotFound:
            flash("Dịch vụ không còn tồn tại. Hãy chọn lại từ danh sách.", "error")
            return redirect(url_for("pages.service_list"), code=303)
        except (ValueError, Error) as error:
            notify_error(error)
            return redirect(url_for("pages.service_list"), code=303)
    if request.method == "POST":
        try:
            price = validation.service(values)
            if record_id is not None:
                database.update_service(record_id, values["name"], values["unit"], price, values["status"], password())
                flash(f"Đã cập nhật dịch vụ {values['name']}.", "success")
                return redirect(url_for("pages.service_list"), code=303)
            database.add_service(values["name"], values["unit"], price, values["status"], password())
            flash(f"Đã lưu dịch vụ {values['name']}.", "success")
            return redirect(url_for("pages.services"), code=303)
        except database.RecordNotFound:
            flash("Dịch vụ không còn tồn tại. Hãy chọn lại từ danh sách.", "error")
            return redirect(url_for("pages.service_list"), code=303)
        except (ValueError, Error) as error:
            notify_error(error)
            status = 400 if isinstance(error, ValueError) else 503
    return render_template("services.html", active="service_list" if record_id is not None else "services",
                           values=values, editing=record_id is not None, statuses=validation.SERVICE_STATUSES), status
