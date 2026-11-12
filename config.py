import os

# Cùng địa chỉ, cổng và tài khoản với kết nối trong MySQL Workbench.
MYSQL = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": os.getenv("MYSQL_PORT", "3306"),
    "user": os.getenv("MYSQL_USER", "tungquan26"),
    "database": "hotel",
    "charset": "utf8mb4",
    "connection_timeout": 4,
}
