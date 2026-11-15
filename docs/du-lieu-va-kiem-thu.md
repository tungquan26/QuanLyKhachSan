# Dữ liệu nghiệp vụ và cách đối chiếu báo cáo

## Nạp dữ liệu

Nguồn cấu trúc là `sql/khach-san.sql`; nguồn dữ liệu duy nhất là `sql/nhap-lieu-khach-san.sql`. File nhập liệu giữ nguyên 91 bản ghi cũ và thêm 13 bản ghi gồm **3 phiếu, 6 chi tiết đặt phòng và 4 giao dịch**. Tổng cộng có 104 bản ghi trên 11 bảng khi nạp vào database mới.

| Trạng thái database | Cách thực hiện trong Workbench |
|---|---|
| Chưa có database `hotel` | Chạy file cấu trúc, giữ `SET @chi_bo_sung = FALSE;`, rồi chạy toàn bộ file nhập liệu. |
| Có schema nhưng chưa nhập dữ liệu | Giữ `@chi_bo_sung = FALSE`, chạy toàn bộ file nhập liệu. |
| Đã có bộ 91 bản ghi cũ | Đổi **một dòng** trong file nhập liệu thành `SET @chi_bo_sung = TRUE;`, rồi chạy toàn bộ file đó. Không chạy lại file tạo database. |
| Đã có 3 phiếu bổ sung | Không nạp lại. Chạy file báo cáo hoặc mở website để đọc dữ liệu. |

Chế độ bổ sung tra khách bằng CCCD duy nhất, kiểm tra nhân viên và loại của các phòng cần dùng. Nếu thiếu dữ liệu nền hoặc có phiếu trùng khách/ngày với đợt bổ sung, file báo lỗi và không ghi thêm. Các thao tác nhập chạy trong một transaction; lỗi sẽ rollback dữ liệu của lần chạy đó. Mã mới được lấy bằng `LAST_INSERT_ID()`, không giả định các mã luôn bắt đầu từ 1. Phòng 101, 102, 103, 107 là mã nghiệp vụ có sẵn, không phải khóa tự tăng.

File cần quyền `SELECT`, `INSERT`, `CREATE ROUTINE`, `ALTER ROUTINE`, `EXECUTE`. Thủ tục hỗ trợ được xóa sau khi chạy thành công; website không phụ thuộc thủ tục này.

## Ba tình huống được bổ sung

| Ngày đặt / khách | Phòng và lịch dự kiến | Trạng thái / giao dịch | Tác động đến báo cáo tháng 10 |
|---|---|---|---|
| 20/10/2026 / Nguyễn Văn I | 101, 102, 103; nhận 20/11, trả 22/11 | Đã xác nhận; cọc 500.000 đồng | **1 phiếu nhưng 3 lượt**: mỗi loại Standard Single, Standard Double, Superior Single thêm 1. |
| 25/10/2026 / Nguyễn Văn K | 101, 107; dự kiến 25–27/11 | Đã hủy trước nhận phòng; cọc 300.000 đồng và hoàn đủ ngày 26/10 | **2 chi tiết bị loại** vì phiếu hủy. |
| 28/10/2026 / Nguyễn Văn A | 101; nhận 22/11, trả 24/11 | Đã xác nhận; cọc 200.000 đồng | Thêm 1 lượt Standard Single. |

Phòng 101 được trả ngày 22/11 ở phiếu đầu và nhận ngày 22/11 ở phiếu sau; hai khoảng lưu trú không chồng nhau. Các phiếu mới chưa nhận phòng hoặc đã hủy nên thời gian thực tế để `NULL`, chưa có khách lưu trú, dịch vụ hay hóa đơn. Tiền cọc là giao dịch, không phải thêm một lượt đặt.

Các lịch nhận phòng nằm ở tháng 11 nhưng lượt đặt thuộc tháng 10 vì báo cáo lọc theo `PhieuDatPhong.NgayDat`. Đây là điểm cần giải thích rõ khi bảo vệ bài.

## Kết quả đối chiếu

Với bộ dữ liệu từ file nhập liệu, kỳ **01/10/2026–31/10/2026**:

| Loại phòng | Lượt hợp lệ | Tỷ lệ |
|---|---:|---:|
| Standard Single | 3 | 25,00% |
| Standard Double | 2 | 16,67% |
| Superior Single | 2 | 16,67% |
| Superior Double | 1 | 8,33% |
| Deluxe Double | 1 | 8,33% |
| Deluxe Twin | 1 | 8,33% |
| Suite | 1 | 8,33% |
| Family | 1 | 8,33% |
| **Tổng cộng** | **12** | **100,00%** |

Đối chiếu độc lập: **11 phiếu tổng cộng = 10 phiếu hợp lệ + 1 phiếu hủy**; **14 chi tiết = 12 lượt hợp lệ + 2 lượt bị hủy**. Cộng tỷ lệ đã làm tròn từng dòng ra 99,99%; tỷ lệ tổng vẫn là 100% vì được tính từ tổng lượt gốc.

| Khoảng ngày đặt | Phiếu hợp lệ | Lượt hợp lệ | Chi tiết bị hủy | Mục đích trình bày |
|---|---:|---:|---:|---|
| 20/10–20/10/2026 | 1 | 3 | 0 | Đếm phòng thay vì đếm phiếu; các loại khác hiện 0. |
| 25/10–25/10/2026 | 0 | 0 | 2 | Loại toàn bộ phòng trong phiếu hủy. |
| 28/10–28/10/2026 | 1 | 1 | 0 | Một phòng có thể được đặt lại trong phiếu khác. |
| 01/11–30/11/2026 | 0 | 0 | 0 | Có lịch nhận tháng 11 nhưng không có ngày đặt tháng 11. |

Khi database được nhập thêm nghiệp vụ, kết quả phải thay đổi theo dữ liệu; bảng trên chỉ là mốc đối chiếu của bộ nhập liệu hiện tại. Không có bộ lọc riêng để ép báo cáo trả các con số này.

## Bộ kiểm thử để nộp cùng project

Chạy 11 kiểm thử nhanh, không cần dịch vụ MySQL:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

`tests/test_room_report.py` kiểm tra đơn vị đếm, loại phiếu hủy, biên ngày, loại có 0 lượt, tên loại trùng, phần trăm, lỗi biểu mẫu, lỗi database và nội dung/ngắt trang Excel. Phần truy vấn dùng SQLite trong bộ nhớ với hàm chuyển chữ thường tiếng Việt, không thay thế kiểm tra MySQL.

Kiểm tra tích hợp với MySQL 8 được cài trên máy:

```powershell
.\.venv\Scripts\python.exe tests/check_mysql_report.py
```

Nếu MySQL nằm ở thư mục khác:

```powershell
.\.venv\Scripts\python.exe tests/check_mysql_report.py --mysql-base "D:\MySQL\MySQL Server 8.0"
```

Công cụ tự mở MySQL riêng ở `127.0.0.1:33079`, dùng thư mục `output/qa/mysql-report-sql/data`, kiểm tra đúng thư mục/cổng trước khi tạo lại database thử nghiệm, rồi dừng tiến trình khi xong. Không dùng tài khoản hay kết nối MySQL trong `config.py`, không truy cập database đang dùng ở cổng 3306. Cổng 33079 phải đang rảnh.

Kiểm tra gồm: nạp mới 104 bản ghi; giữ 91 bản ghi cũ khi bổ sung; từ chối nhập trùng hoặc thiếu dữ liệu nền; rollback khi lỗi; mã tự tăng không bắt đầu từ 1; không trùng lịch phòng; hoàn cọc đủ; SQL, màn hình và Excel khớp nhau. Kết quả tóm tắt ghi vào `output/qa/ket-qua-kiem-thu.json`; file Excel kiểm tra ghi vào `output/bao-cao`.

## `output/qa` là gì?

Tên thư mục hiện tại là **`output/qa`**, không phải `out/qa`. `QA` là kiểm tra chất lượng. Website chạy bằng `app.py` không đọc số liệu từ thư mục này. Đây là nơi lưu công cụ thử tạm, ảnh xem trước, file in kiểm tra và database MySQL riêng dùng trong kiểm thử.

| File / thư mục | Công dụng | Vai trò hiện tại |
|---|---|---|
| `check_report_sql.py` | Lối gọi cũ, chuyển tiếp đến `tests/check_mysql_report.py`. | Dùng lệnh trong `tests` khi kiểm tra/nộp bài. |
| `mysql-report-sql/` | Database thử nghiệm, nhật ký khởi tạo và nhật ký MySQL. | Không phải dữ liệu website, không cần nộp. Được tạo lại bởi kiểm thử khi thiếu. |
| `ket-qua-kiem-thu.json` | Tổng số bản ghi, số phiếu/lượt và kết quả thống kê sau lần kiểm thử thành công. | Bằng chứng đối chiếu; không làm nguồn cho báo cáo. |
| `check_print_cases.py` | Tạo các ca bố cục riêng: 12 loại phòng, tên dài, không phát sinh lượt. | Chỉ kiểm tra khả năng in; không ghi vào database. |
| `print-cases/` | Excel và PDF của các ca bố cục trên. | Không dùng các số liệu thử này làm báo cáo nghiệp vụ. |
| `export_excel_pdf.ps1` | Mở workbook bằng Excel ở chế độ chỉ đọc, xuất PDF để xem bản in A4. | Công cụ kiểm tra, cần Microsoft Excel. Không gửi lệnh đến máy in; khôi phục tùy chọn đổi A4/Letter sau khi xuất. |
| `ban-in-loai-phong.png` | Ảnh bản in của báo cáo lấy từ bộ SQL. | Xem trước; có thể cũ nếu chưa xuất/render lại sau khi đổi dữ liệu. |
| `12-loai-page2.png`, `8-ten-dai-*.png` | Ảnh kiểm tra ngắt trang và tên loại dài. | Bằng chứng kiểm tra bố cục. |
| `serve_room_report.py` | Máy chủ thử cũ ở cổng 5051 với số liệu cố định để thử giao diện. | Không phải lệnh chạy project; chạy website thật bằng `app.py`. |
| `room-report-sample.xlsx` | File thử cũ do máy chủ trên tạo. | Không dùng để nộp báo cáo. |
| `prepare_project_sql.py` | Công cụ một lần đã dùng để chuyển file nhập liệu cũ sang cách lấy ID bằng `LAST_INSERT_ID()`. | Không chạy lại: có thể ghi đè file SQL hiện tại bằng logic chuyển đổi cũ. |
| `update_sql_check.py` | Công cụ một lần đã dùng để sửa phiên bản kiểm thử cũ. | Không chạy lại: có thể ghi đè lối gọi kiểm thử hiện tại. |
| `nghiep-vu-doc/image*.png` | Các ảnh trích từ tài liệu nghiệp vụ đã gửi để đối chiếu. | Tài liệu kiểm tra tạm. |

`output/` được loại khỏi Git vì chứa kết quả sinh lại được và database thử nghiệm có thể lớn. Các phần cần giữ cùng bài là mã ứng dụng, `sql/`, `tests/`, `docs/`, `tools/`, file requirements và README. Khi cần nộp Excel/PDF cuối, chọn riêng bản trong `output/bao-cao`.
