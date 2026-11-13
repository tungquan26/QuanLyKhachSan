import os
import argparse
from getpass import getpass
from web import create_app

app = create_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hotel Desk — website nhập liệu khách sạn")
    parser.parse_args()
    if app.config["MYSQL_PASSWORD"] is None:
        app.config["MYSQL_PASSWORD"] = getpass("Mật khẩu MySQL: ")
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
