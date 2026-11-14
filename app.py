import os
import argparse
from getpass import getpass
from mysql.connector import Error
from database_setup import install_missing_procedures
from web import create_app
from bao_cao_2 import bao_cao_2_bp

app = create_app()
app.register_blueprint(bao_cao_2_bp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hotel Desk — website nhập liệu khách sạn")
    parser.add_argument("--init-db", action="store_true", help="Tạo thủ tục nhập liệu còn thiếu, giữ nguyên dữ liệu hiện có")
    args = parser.parse_args()
    if app.config["MYSQL_PASSWORD"] is None:
        app.config["MYSQL_PASSWORD"] = getpass("Mật khẩu MySQL (chỉ giữ trong bộ nhớ): ")
    if args.init_db:
        try:
            installed = install_missing_procedures(app.config["MYSQL_PASSWORD"])
        except (Error, ValueError) as error:
            if getattr(error, "errno", None) == 1045:
                parser.exit(1, "Sai tài khoản hoặc mật khẩu MySQL. Hãy kiểm tra lại kết nối trong Workbench.\n")
            if getattr(error, "errno", None) in (1044, 1142, 1227, 1370):
                parser.exit(1, "Tài khoản cần quyền CREATE ROUTINE trong database hotel để cài thủ tục.\n")
            parser.exit(1, f"Không cài được thủ tục. Mã MySQL: {getattr(error, 'errno', 'không có')}. Kiểm tra database hotel và các bảng đã tồn tại.\n")
        print("Đã tạo: " + ", ".join(installed) if installed else "Thủ tục ThemKhachHang đã tồn tại; không thay đổi.")
        print("Dữ liệu hiện có được giữ nguyên. Chạy lại python app.py để mở web.")
        raise SystemExit(0)
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
