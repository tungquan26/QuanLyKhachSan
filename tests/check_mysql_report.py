"""Run actual MySQL 8 against an isolated, disposable workspace data directory."""
import os
import subprocess
import time
import argparse
import json
from pathlib import Path
from decimal import Decimal

import mysql.connector
from mysql.connector import Error

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'output/qa/mysql-report-sql'
DATA = QA / 'data'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--mysql-base', default=os.getenv('MYSQL_BASE', 'C:/Program Files/MySQL/MySQL Server 8.0'))
BASE = Path(parser.parse_args().mysql_base).resolve()
SERVER = BASE / 'bin/mysqld.exe'
PORT = 33079
QA.mkdir(parents=True, exist_ok=True)
FLAGS = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
seed = (ROOT / 'sql/nhap-lieu-khach-san.sql').read_text(encoding='utf-8')
seed = seed.replace('SET @chi_bo_sung = TRUE;', 'SET @chi_bo_sung = FALSE;', 1)
report = (ROOT / 'sql/bao-cao-loai-phong.sql').read_text(encoding='utf-8')

def statements(script):
    delimiter = ';'
    pending = []
    for line in script.splitlines():
        if line.lstrip().startswith('--') or not line.strip():
            continue
        if line.upper().startswith('DELIMITER '):
            assert not pending
            delimiter = line.split()[1]
            continue
        pending.append(line)
        if line.rstrip().endswith(delimiter):
            yield '\n'.join(pending).rstrip()[:-len(delimiter)]
            pending = []
    if pending:
        yield '\n'.join(pending)

if not DATA.exists():
    print('Initializing isolated MySQL data directory...', flush=True)
    init = subprocess.run([str(SERVER), '--no-defaults', '--initialize-insecure',
                           f'--basedir={BASE}', f'--datadir={DATA}', '--console'],
                          capture_output=True, text=True, creationflags=FLAGS, timeout=120)
    (QA / 'initialize.log').write_text(init.stdout + init.stderr, encoding='utf-8')
    if init.returncode:
        raise RuntimeError(init.stderr[-3000:])

log = (QA / 'server.log').open('w', encoding='utf-8')
process = subprocess.Popen([str(SERVER), '--no-defaults', f'--basedir={BASE}',
    f'--datadir={DATA}', f'--port={PORT}', '--bind-address=127.0.0.1',
    '--mysqlx=OFF', '--skip-log-bin', '--innodb-buffer-pool-size=32M', '--console'],
    stdout=log, stderr=subprocess.STDOUT, creationflags=FLAGS)
connection = None
verified = False
try:
    for _ in range(60):
        if process.poll() is not None:
            raise RuntimeError((QA / 'server.log').read_text(encoding='utf-8')[-3000:])
        try:
            connection = mysql.connector.connect(host='127.0.0.1', port=PORT, user='root',
                password='', ssl_disabled=True, connection_timeout=1, autocommit=True)
            break
        except Error:
            time.sleep(0.5)
    assert connection is not None, 'Isolated MySQL did not start'
    cursor = connection.cursor()
    cursor.execute('SELECT @@datadir, @@port')
    actual_dir, actual_port = cursor.fetchone()
    assert Path(actual_dir).resolve() == DATA.resolve() and actual_port == PORT, 'Wrong MySQL instance'
    verified = True

    def execute(script):
        result_sets = []
        for sql in statements(script):
            cursor.execute(sql)
            while True:
                if cursor.with_rows:
                    result_sets.append(cursor.fetchall())
                if not cursor.nextset():
                    break
        return result_sets

    def counts():
        return tuple(execute(f'SELECT COUNT(*) FROM {table};')[0][0][0]
                     for table in tables)

    schema = (ROOT / 'sql/khach-san.sql').read_text(encoding='utf-8')
    def reset():
        execute('DROP DATABASE IF EXISTS hotel;')  # Isolated test server ONLY.
        execute(schema)
    tables = ['KhachHang','NhanVien','LoaiPhong','Phong','DichVu','PhieuDatPhong',
              'ChiTietDatPhong','LanSuDungDichVu','DangKyLuuTru','HoaDon','ThanhToan']
    reset()
    # Reconstruct the original 91-row section to test upgrading an existing DB.
    # This test runs from a submitted ZIP as well: no Git history is required.
    original = seed.split('    -- BO SUNG NGHIEP VU:', 1)[0] + '''
    COMMIT;
END$$
DELIMITER ;
CALL sp_nhap_lieu_khach_san_btl(FALSE);
DROP PROCEDURE sp_nhap_lieu_khach_san_btl;
'''
    execute(original)
    baseline = {t:execute(f'SELECT * FROM {t} ORDER BY 1;')[0] for t in tables}
    reset()
    assert execute(report)[3] == [(0,0,0,0)]
    execute(seed)
    assert sum(len(v) for v in baseline.values()) == 91
    assert counts() == (10,8,8,8,9,11,14,8,8,8,12)
    for t in tables:
        assert execute(f'SELECT * FROM {t} ORDER BY 1;')[0][:len(baseline[t])] == baseline[t], t
    fresh = {t:execute(f'SELECT * FROM {t} ORDER BY 1;')[0] for t in tables}
    print('PASS: preserved 91 original records; added 13 records (104 total)', flush=True)
    result = execute(report)
    assert len(result[1]) == 9
    expected = [(3,Decimal('25.00')), (2,Decimal('16.67')), (2,Decimal('16.67'))] + [(1,Decimal('8.33'))] * 5
    assert [row[2:] for row in result[1][:-1]] == expected
    assert result[1][-1][2:] == (12,Decimal('100.00'))
    assert result[3] == [(10,12,2,14)]
    before = counts()
    try:
        execute(seed)
        raise AssertionError('Expected duplicate error')
    except Error as e:
        assert e.errno == 1062, e
    assert counts() == before
    supplement = seed.replace('SET @chi_bo_sung = FALSE;', 'SET @chi_bo_sung = TRUE;', 1)
    try:
        execute(supplement)
        raise AssertionError('Expected duplicate supplement error')
    except Error as e:
        assert e.errno == 1644, e
    assert {t:execute(f'SELECT * FROM {t} ORDER BY 1;')[0] for t in tables} == fresh
    print('PASS: 10 valid forms, 12 valid bookings, 2 cancelled details; reruns change no rows', flush=True)

    import sys, io
    from unittest.mock import patch
    from datetime import date
    sys.path.insert(0,str(ROOT))
    import database
    from web import create_app
    from openpyxl import load_workbook
    def query(sql, params, password, *, read=False):
        cursor.execute(sql, params)
        return cursor.fetchall()
    with patch('database.run_sql',side_effect=query):
        rows = database.list_room_type_bookings(date(2026,10,1),date(2026,10,31),'test')
        assert [(r[1],r[2]) for r in rows] == [(r[1],r[2]) for r in result[1][:-1]]
        client = create_app({'TESTING':True,'MYSQL_PASSWORD':'test'}).test_client()
        client.get('/bao-cao/loai-phong')
        with client.session_transaction() as session:
            csrf = session['csrf_token']
        form = {'csrf_token':csrf,'tu_ngay':'2026-10-01','den_ngay':'2026-10-31',
                'ten_khach_san':'Khách sạn Hotel Desk'}
        html = client.post('/bao-cao/loai-phong',data=form)
        assert html.status_code == 200 and '25,00' in html.get_data(as_text=True)
        xlsx = client.post('/bao-cao/loai-phong/xuat-excel',data=form)
        assert xlsx.status_code == 200
        export_dir = ROOT / 'output/bao-cao'
        export_dir.mkdir(parents=True, exist_ok=True)
        (export_dir / 'Luot_dat_theo_loai_phong_2026-10.xlsx').write_bytes(xlsx.data)
        book = load_workbook(io.BytesIO(xlsx.data))
        assert book.active['C18'].value == 12 and book.active['D18'].value == 1
        assert [book.active.cell(r,3).value for r in range(10,18)] == [3,2,2,1,1,1,1,1]
        assert book.active['D10'].value == 0.25
        book.close()
    print('PASS: SQL, application preview and exported Excel agree', flush=True)

    def period(start, end):
        return execute(report.replace("DATE('2026-10-01')", f"DATE('{start}')", 1)
                       .replace("DATE('2026-10-31')", f"DATE('{end}')", 1))
    assert period('2026-10-20','2026-10-20')[3] == [(1,3,0,3)]
    assert period('2026-10-25','2026-10-25')[3] == [(0,0,2,2)]
    assert period('2026-10-28','2026-10-28')[3] == [(1,1,0,1)]
    assert period('2026-10-01','2026-10-01')[3] == [(1,1,0,1)]
    empty_period = report.replace("DATE('2026-10-01')", "DATE('2026-11-01')").replace(
        "DATE('2026-10-31')", "DATE('2026-11-30')")
    assert all(r[2] == 0 and r[3] == 0 for r in execute(empty_period)[1])
    assert execute("""
        SELECT COUNT(*) FROM ChiTietDatPhong a
        JOIN ChiTietDatPhong b ON a.MaPhong=b.MaPhong AND a.MaChiTietDatPhong<b.MaChiTietDatPhong
        JOIN PhieuDatPhong pa ON pa.MaPhieu=a.MaPhieu JOIN PhieuDatPhong pb ON pb.MaPhieu=b.MaPhieu
        WHERE pa.TrangThaiPhieu <> 'Đã hủy' AND pb.TrangThaiPhieu <> 'Đã hủy'
          AND a.NgayNhanDuKien < b.NgayTraDuKien AND b.NgayNhanDuKien < a.NgayTraDuKien;
    """)[0][0][0] == 0
    assert execute("""
        SELECT SUM(CASE WHEN tt.LoaiGiaoDich='Đặt cọc' THEN tt.SoTien ELSE -tt.SoTien END)
        FROM ThanhToan tt JOIN PhieuDatPhong pd ON pd.MaPhieu=tt.MaPhieu WHERE pd.TrangThaiPhieu='Đã hủy';
    """)[0][0][0] == 0
    assert execute("""
        SELECT COUNT(*) FROM ChiTietDatPhong ct JOIN PhieuDatPhong pd ON pd.MaPhieu=ct.MaPhieu
        WHERE pd.NgayDat >= '2026-10-20'
          AND (ct.ThoiDiemNhanThucTe IS NOT NULL OR ct.ThoiDiemTraThucTe IS NOT NULL
            OR EXISTS (SELECT 1 FROM DangKyLuuTru lt WHERE lt.MaChiTietDatPhong=ct.MaChiTietDatPhong)
            OR EXISTS (SELECT 1 FROM LanSuDungDichVu dv WHERE dv.MaChiTietDatPhong=ct.MaChiTietDatPhong)
            OR EXISTS (SELECT 1 FROM HoaDon hd WHERE hd.MaPhieu=pd.MaPhieu));
    """)[0][0][0] == 0
    print('PASS: date boundaries, cancellation, multi-room form, zero types, no overlap, correct deposit refund', flush=True)

    reset()
    try:
        execute(supplement)
        raise AssertionError('Expected missing-parent error')
    except Error as e:
        assert e.errno == 1644, e
    assert not any(counts())
    execute(original)
    execute(supplement)
    assert {t:execute(f'SELECT * FROM {t} ORDER BY 1;')[0] for t in tables} == fresh
    print('PASS: supplement mode preserves old data and produces exactly the fresh-import result', flush=True)

    reset()
    # Force a failure after parent records and bookings have already been inserted.
    execute("CREATE TRIGGER fail_import BEFORE INSERT ON ChiTietDatPhong FOR EACH ROW SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Injected test failure';")
    try:
        execute(seed)
        raise AssertionError('Expected injected failure')
    except Error as e:
        assert e.sqlstate == '45000', e
    assert all(n == 0 for n in counts())
    execute('DROP TRIGGER fail_import;')
    # Failed transactions advance AUTO_INCREMENT. This checks IDs need not start at 1.
    execute(seed)
    assert execute('SELECT MIN(MaKhachHang) FROM KhachHang;')[0][0][0] > 1
    assert execute(report)[3] == [(10,12,2,14)]
    actual_links = execute("SELECT kh.HoTen, nv.HoTen, lp.TenLoaiPhong FROM ChiTietDatPhong ct JOIN PhieuDatPhong pd ON pd.MaPhieu=ct.MaPhieu JOIN KhachHang kh ON kh.MaKhachHang=pd.MaKhachHang JOIN NhanVien nv ON nv.MaNhanVien=pd.MaNhanVienTiepNhan JOIN Phong p ON p.MaPhong=ct.MaPhong JOIN LoaiPhong lp ON lp.MaLoaiPhong=p.MaLoaiPhong WHERE pd.NgayDat < '2026-10-20' ORDER BY p.MaPhong;")[0]
    expected_links = [(baseline['KhachHang'][i][1],baseline['NhanVien'][i][1],baseline['LoaiPhong'][i][1]) for i in range(8)]
    assert actual_links == expected_links
    print('PASS: atomic rollback and correct relationships with non-1 IDs', flush=True)
    summary = {'table_counts':dict(zip(tables,counts())), 'valid_forms':10,'valid_bookings':12,
               'cancelled_details':2,'report':[[r[1],int(r[2]),str(r[3])] for r in result[1][:-1]]}
    (ROOT / 'output/qa/ket-qua-kiem-thu.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print('ALL CHECKS PASSED on isolated MySQL; no live user data accessed.', flush=True)

finally:
    if connection:
        if verified:
            try:
                connection.cmd_shutdown()
            except Error:
                pass
        connection.close()
    try:
        process.wait(timeout=20)
    except subprocess.TimeoutExpired:
        process.terminate()
        process.wait(timeout=10)
    log.close()
