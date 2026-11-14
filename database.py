from mysql.connector import connect
from config import MYSQL


class RecordNotFound(Exception):
    pass


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
        "order by MaKhachHang asc", (), password, read=True,
    )


def list_services(password):
    return run_sql(
        "select MaDichVu, TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai from DichVu "
        "order by MaDichVu asc", (), password, read=True,
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


def list_service_revenue(start_date, end_date, password):
    from datetime import datetime, time

    return run_sql(
        """
        SELECT dv.TenDichVu, dv.DonViTinh, SUM(ls.SoLuong),
               ls.DonGiaApDung, SUM(ls.SoLuong * ls.DonGiaApDung) AS ThanhTien
        FROM LanSuDungDichVu ls
        JOIN DichVu dv ON dv.MaDichVu = ls.MaDichVu
        WHERE ls.ThoiDiemSuDung >= %s AND ls.ThoiDiemSuDung <= %s
        GROUP BY dv.MaDichVu, dv.TenDichVu, dv.DonViTinh, ls.DonGiaApDung
        ORDER BY ThanhTien DESC, dv.MaDichVu, ls.DonGiaApDung
        """,
        (datetime.combine(start_date, time.min), datetime.combine(end_date, time.max)),
        password, read=True,
    )


def get_guest(record_id, password):
    rows = run_sql(
        "select HoTen, CCCD, SoDienThoai from KhachHang where MaKhachHang = %s",
        (record_id,), password, read=True,
    )
    if not rows:
        raise RecordNotFound()
    return rows[0]


def get_service(record_id, password):
    rows = run_sql(
        "select TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai from DichVu where MaDichVu = %s",
        (record_id,), password, read=True,
    )
    if not rows:
        raise RecordNotFound()
    return rows[0]


def update_sql(sql, params, lookup_sql, record_id, password):
    with connect(**MYSQL, password=password) as connection:
        with connection.cursor() as cursor:
            # Lock the existing row until commit, including when values are unchanged.
            cursor.execute(lookup_sql, (record_id,))
            if cursor.fetchone() is None:
                raise RecordNotFound()
            cursor.execute(sql, params)
            connection.commit()


def update_guest(record_id, name, cccd, phone, password):
    update_sql(
        "update KhachHang set HoTen = %s, CCCD = %s, SoDienThoai = %s where MaKhachHang = %s",
        (name, cccd, phone, record_id),
        "select MaKhachHang from KhachHang where MaKhachHang = %s for update",
        record_id, password,
    )


def update_service(record_id, name, unit, price, status, password):
    update_sql(
        "update DichVu set TenDichVu = %s, DonViTinh = %s, DonGiaHienHanh = %s, TrangThai = %s "
        "where MaDichVu = %s",
        (name, unit, price, status, record_id),
        "select MaDichVu from DichVu where MaDichVu = %s for update",
        record_id, password,
    )
