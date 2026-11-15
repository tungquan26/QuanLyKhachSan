"""Business-rule and export checks; no connection to the user's MySQL."""
import io
import sqlite3
import unittest
from datetime import date
from unittest.mock import patch

from mysql.connector import Error
from openpyxl import load_workbook

import database
from web import create_app
from bao_cao_loai_phong import _excel, _format_percent, _report


class BookingLogicTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.create_function('LOWER', 1, lambda value: value.lower())
        self.db.executescript('''
            CREATE TABLE LoaiPhong (MaLoaiPhong INTEGER PRIMARY KEY, TenLoaiPhong TEXT);
            CREATE TABLE Phong (MaPhong TEXT PRIMARY KEY, MaLoaiPhong INTEGER);
            CREATE TABLE PhieuDatPhong (MaPhieu INTEGER PRIMARY KEY, NgayDat TEXT, TrangThaiPhieu TEXT);
            CREATE TABLE ChiTietDatPhong (MaChiTietDatPhong INTEGER PRIMARY KEY, MaPhieu INTEGER, MaPhong TEXT);
            INSERT INTO LoaiPhong VALUES (1,'Standard'), (2,'Suite'), (3,'Standard');
            INSERT INTO Phong VALUES ('101',1), ('102',1), ('201',2), ('301',3);
            INSERT INTO PhieuDatPhong VALUES
                (1,'2026-10-01','Đã hoàn tất'), (2,'2026-10-31','Đã xác nhận'),
                (3,'2026-10-12','  ĐÃ HỦY  '), (4,'2026-09-30','Đã hoàn tất'),
                (5,'2026-11-01','Đã hoàn tất');
            INSERT INTO ChiTietDatPhong VALUES
                (1,1,'101'), (2,1,'102'), (3,1,'201'), (4,2,'301'),
                (5,3,'201'), (6,4,'101'), (7,5,'101');
        ''')

    def fetch(self, start='2026-10-01', end='2026-10-31'):
        def query(sql, params, password, *, read=False):
            return self.db.execute(sql.replace('%s', '?'), params).fetchall()
        with patch('database.run_sql', side_effect=query):
            return database.list_room_type_bookings(start, end, 'unused')

    def test_counts_rooms_not_booking_forms_and_keeps_distinct_type_ids(self):
        # Two valid forms contain four rooms; two distinct type IDs share a name.
        self.assertEqual(self.fetch(), [(1,'Standard',2), (2,'Suite',1), (3,'Standard',1)])

    def test_booking_date_bounds_are_inclusive(self):
        self.assertEqual(self.fetch('2026-10-31','2026-10-31'),
                         [(3,'Standard',1), (1,'Standard',0), (2,'Suite',0)])

    def test_cancelled_spellings_are_excluded(self):
        for status in ('Đã hủy','Đã huỷ','Hủy','Huỷ','Da huy','Huy','  ĐÃ HỦY  '):
            with self.subTest(status=status):
                self.db.execute('UPDATE PhieuDatPhong SET TrangThaiPhieu=? WHERE MaPhieu=3', (status,))
                self.assertEqual(sum(row[2] for row in self.fetch()), 4)

    def test_empty_period_preserves_all_types_with_zero(self):
        rows = self.fetch('2026-12-01','2026-12-31')
        self.assertEqual(len(rows), 3)
        self.assertEqual([row[2] for row in rows], [0,0,0])
        self.assertEqual(_report(rows)['total_share'], 0)

    def test_percentage_uses_room_total(self):
        result = _report(self.fetch())
        self.assertEqual(result['total'], 4)
        self.assertEqual([_format_percent(r['share']) for r in result['rows']], ['50,00','25,00','25,00'])


class ReportExportTests(unittest.TestCase):
    def workbook(self, count=8):
        rows = [(i, f'Loại phòng {i}', 1) for i in range(count)]
        file = _excel(_report(rows), {'ten_khach_san':'=1+1'},
                      date(2026,11,15), 'Từ ngày 01/10/2026 đến ngày 31/10/2026')
        book = load_workbook(file)
        self.addCleanup(book.close)
        return book.active

    def test_export_values_and_text_are_preserved(self):
        sheet = self.workbook()
        self.assertEqual(sheet['C18'].value, 8)
        self.assertEqual(sheet['D10'].value, 0.125)
        self.assertEqual(sheet['D18'].value, 1)
        self.assertEqual(sheet['A1'].value, '=1+1')
        self.assertEqual(sheet['A1'].data_type, 's')
        self.assertEqual(sheet['A25'].value, 'Trưởng bộ phận Lễ tân')
        self.assertIsNone(sheet['A27'].value)

    def test_short_report_needs_no_manual_break(self):
        sheet = self.workbook()
        self.assertEqual(str(sheet.page_setup.paperSize), sheet.PAPERSIZE_A4)
        self.assertEqual(sheet.page_setup.scale, 100)
        self.assertEqual(len(sheet.row_breaks.brk), 0)

    def test_long_report_keeps_total_notes_and_signature_together(self):
        sheet = self.workbook(12)
        # The final two data rows start at row 20, total at row 22.
        self.assertEqual([b.id for b in sheet.row_breaks.brk], [19])
        self.assertEqual(sheet['C22'].value, 12)
        self.assertEqual(sheet['A30'].value, '(Ký, ghi rõ họ tên)')


class ReportRequestTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app({'TESTING':True,'MYSQL_PASSWORD':'unused'}).test_client()
        self.client.get('/bao-cao/loai-phong')
        with self.client.session_transaction() as session:
            csrf = session['csrf_token']
        self.form = dict(csrf_token=csrf, tu_ngay='2026-10-01', den_ngay='2026-10-31',
                         ten_khach_san='Khách sạn')

    def test_invalid_period_does_not_query_database(self):
        with patch('database.list_room_type_bookings') as query:
            response = self.client.post('/bao-cao/loai-phong', data={**self.form,'tu_ngay':'2026-11-01'})
            self.assertEqual(response.status_code, 400)
            query.assert_not_called()

    def test_preview_and_export_share_the_same_figures(self):
        with patch('database.list_room_type_bookings', return_value=[(1,'Standard',3),(2,'Suite',1)]):
            preview = self.client.post('/bao-cao/loai-phong', data=self.form)
            self.assertEqual(preview.status_code, 200)
            self.assertIn('75,00', preview.get_data(as_text=True))
            response = self.client.post('/bao-cao/loai-phong/xuat-excel', data=self.form)
            self.assertEqual(response.status_code, 200)
            with io.BytesIO(response.data) as output:
                book = load_workbook(output)
                self.assertEqual(book.active['C12'].value, 4)
                self.assertEqual(book.active['D10'].value, 0.75)
                book.close()

    def test_database_error_does_not_download_a_report(self):
        with patch('database.list_room_type_bookings', side_effect=Error('test', errno=2003)):
            response = self.client.post('/bao-cao/loai-phong/xuat-excel', data=self.form)
        self.assertEqual(response.status_code, 503)
        self.assertNotIn('attachment', response.headers.get('Content-Disposition',''))


if __name__ == '__main__':
    unittest.main()
