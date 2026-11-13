from mysql.connector import connect
from config import MYSQL


def run_sql(sql, params, password, *, read=False):
    with connect(**MYSQL, password=password) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            if read:
                return cursor.fetchall()
            connection.commit()


def list_guests(password):
    return run_sql(
        "select MaKhachHang, HoTen, CCCD, SoDienThoai from KhachHang "
        "order by MaKhachHang desc", (), password, read=True,
    )


def list_services(password):
    return run_sql(
        "select MaDichVu, TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai from DichVu "
        "order by MaDichVu desc", (), password, read=True,
    )


def add_guest(name, cccd, phone, password):
    run_sql(
        "insert into KhachHang (HoTen, CCCD, SoDienThoai) values (%s, %s, %s)",
        (name, cccd, phone), password,
    )


def add_service(name, unit, price, status, password):
    run_sql(
        "insert into DichVu (TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai) "
        "values (%s, %s, %s, %s)",
        (name, unit, price, status), password,
    )
