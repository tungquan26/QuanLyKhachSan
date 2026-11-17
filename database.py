from datetime import datetime, time, timedelta, timezone
from pathlib import Path
import re

from mysql.connector import connect
from config import MYSQL

SQL_DIR = Path(__file__).resolve().parent / "sql"

def load_sql(filename, query_index=0):
    script = (SQL_DIR / filename).read_text(encoding="utf-8")
    queries = re.findall(r"^(?:select|insert)\b.*?;", script, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if query_index < 0 or query_index >= len(queries):
        raise ValueError(f"Không tìm thấy truy vấn thứ {query_index + 1} trong {filename}")
    query = queries[query_index]
    query = re.sub(r"@[a-z][a-z0-9_]*\b", "%s", query)
    return query.strip().removesuffix(";")

def run_sql(sql, params, password, *, read=False):
    with connect(**MYSQL, password=password) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            if read:
                return cursor.fetchall()
            connection.commit()

def search_pattern(keyword):
    return "%" + keyword + "%"

def list_guests(password, keyword=""):
    query_index = 1 if keyword else 0
    params = (search_pattern(keyword),) if keyword else ()
    return run_sql(load_sql("khach-hang.sql", query_index), params, password, read=True)

def list_services(password):
    return run_sql(
        load_sql("dich-vu.sql"), (), password, read=True,
    )

def add_guest(name, cccd, phone, password):
    run_sql(
        load_sql("khach-hang.sql", 2),
        (name, cccd, phone), password,
    )

def add_service(name, unit, price, status, password):
    run_sql(
        load_sql("dich-vu.sql", 1),
        (name, unit, price, status), password,
    )

def list_service_revenue(start_date, end_date, password):
    return run_sql(
        load_sql("bao-cao-doanh-thu-dich-vu.sql"),
        (datetime.combine(start_date, time.min), datetime.combine(end_date, time.max)),
        password, read=True,
    )

def list_room_type_usage(start_date, end_date, password):
    start = datetime.combine(start_date, time.min)
    end = datetime.combine(end_date, time.max)
    now = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
    # Thu tu gia tri khop voi cac bien @... trong cau SQL.
    return run_sql(
        load_sql("bao-cao-su-dung-loai-phong.sql"),
        (end, now, start, now, start),
        password, read=True,
    )
