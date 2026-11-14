from mysql.connector import connect
from config import MYSQL


def run_sql(sql, params, password, *, read=False):
    with connect(**MYSQL, password=password) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            if read:
                return cursor.fetchall()
            # CALL also returns a final status result. Consume every result
            # before COMMIT so the connection is ready for another command.
            while cursor.nextset():
                pass
            connection.commit()


def find_guest(cccd, password):
    return run_sql("SELECT MaKhachHang, HoTen, SoDienThoai FROM KhachHang WHERE CCCD=%s",
                   (cccd,), password, read=True)


def add_guest(name, cccd, phone, password):
    run_sql("CALL ThemKhachHang(%s, %s, %s)", (name, cccd, phone), password)


def add_service(name, unit, price, status, password):
    run_sql(
        "INSERT INTO DichVu (TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai) "
        "VALUES (%s, %s, %s, %s)",
        (name, unit, price, status), password,
    )
