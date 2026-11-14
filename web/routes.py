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
        message = "CCCD đã có hồ sơ. Hãy dùng Tra CCCD để kiểm tra."
    elif error.errno == 1644:
        message = error.msg
    else:
        messages = {
            1045: "MySQL từ chối đăng nhập. Hãy dừng web bằng Ctrl+C, chạy lại app.py và nhập đúng mật khẩu MySQL như trong Workbench.",
            1049: "Chưa có database hotel. Hãy tạo schema hotel và chạy các tệp SQL theo README.md.",
            1146: "Database hotel đang thiếu bảng cần thiết. Hãy kiểm tra các bảng được tạo từ sql/khach-san.sql trong Workbench.",
            1305: "Chưa có thủ tục lưu trong database hotel. Trong terminal, dừng web bằng Ctrl+C, chạy python app.py --init-db để cài thủ tục còn thiếu, rồi chạy lại python app.py.",
            1044: "Tài khoản MySQL chưa có quyền truy cập database hotel.",
            1142: "Tài khoản MySQL chưa có quyền thao tác trên bảng dữ liệu.",
            1370: "Tài khoản MySQL chưa có quyền chạy thủ tục lưu dữ liệu.",
            2002: "Không kết nối được MySQL. Kiểm tra dịch vụ MySQL, địa chỉ và cổng kết nối.",
            2003: "Không kết nối được MySQL. Kiểm tra dịch vụ MySQL, địa chỉ và cổng kết nối.",
            2013: "Kết nối MySQL bị gián đoạn. Hãy kiểm tra MySQL và thử lại.",
            2014: "Chưa xử lý xong phản hồi MySQL. Hãy khởi động lại web để dùng bản sửa mới rồi thử lại.",
        }
        message = messages.get(error.errno, "Không thể lưu với cơ sở dữ liệu. Hãy cung cấp mã lỗi bên dưới để kiểm tra.")
        message += f" (Mã MySQL: {error.errno if error.errno is not None else 'không có'})"
        current_app.logger.error("MySQL operation failed: errno=%s sqlstate=%s", error.errno, error.sqlstate)
    flash(message, "error")


@pages.get("/")
def index():
    return redirect(url_for("pages.guests"))


@pages.route("/khach-hang", methods=["GET", "POST"])
def guests():
    values = {key: request.form.get(key, "").strip() for key in ("name", "cccd", "phone")}
    status = 200
    if request.method == "POST":
        try:
            action = request.form.get("action")
            if action == "lookup":
                rows = database.find_guest(validation.identity(values["cccd"]), password())
                if rows:
                    code, values["name"], phone = rows[0]
                    values["phone"] = phone or ""
                    flash(f"Đã tìm thấy hồ sơ khách số {code}. Hồ sơ hiện có không được cập nhật bằng nút Lưu hồ sơ.", "success")
                else:
                    flash("Chưa có hồ sơ cho CCCD này. Bạn có thể nhập thông tin và tạo hồ sơ mới.", "info")
            elif action == "save":
                validation.guest(values)
                database.add_guest(values["name"], values["cccd"], values["phone"], password())
                flash(f"Đã lưu hồ sơ của {values['name']}.", "success")
                return redirect(url_for("pages.guests"), code=303)
            else:
                raise ValueError("Thao tác không hợp lệ.")
        except (ValueError, Error) as error:
            notify_error(error)
            status = 400 if isinstance(error, ValueError) else 503
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
