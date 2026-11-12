# Hotel Desk — website nhập liệu khách sạn

Giao diện web tiếng Việt dùng Flask + Jinja, chạy trong trình duyệt, kết nối cùng MySQL `hotel` với Workbench. Hai trang hiện có:

- `/khach-hang`: tạo hồ sơ và kiểm tra hồ sơ theo CCCD ngay trong biểu mẫu.
- `/dich-vu`: thêm danh mục dịch vụ trực tiếp, không cần phòng hoặc khách đang lưu trú.

Chưa triển khai màn hình tìm kiếm nghiệp vụ (mục 6) và báo cáo/xuất tệp (mục 7). Không dùng CustomTkinter nữa.

## Chạy trên Windows

Python 3.11 trở lên. Khi thiết lập MySQL lần đầu, tạo schema `hotel`, chạy `sql/khach-san.sql` rồi `sql/nhap-lieu-khach-san.sql`. Nếu đã có dữ liệu, sử dụng database hiện tại; không chạy lại script khởi tạo.

`sql/khach-san.sql` chỉ định nghĩa bảng, ràng buộc và trigger; không thêm khách, phòng hay lượt lưu trú mẫu. Hai form Khách hàng và Danh mục dịch vụ có thể nhập dữ liệu ngay khi các bảng đang trống.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Nhập mật khẩu MySQL trong terminal (không hiển thị và chỉ giữ trong bộ nhớ), rồi mở **http://127.0.0.1:5000**. Dừng bằng Ctrl+C. Có thể cấu hình `MYSQL_PASSWORD` qua biến môi trường phía server để bỏ qua lời nhắc. Không nhập mật khẩu database trên website.

Kết nối mặc định: `127.0.0.1:3306`, tài khoản `root`, database `hotel`. Đặt `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER` nếu khác; `PORT` đổi cổng website. Đây là cấu hình chạy cục bộ, chỉ lắng nghe trên loopback; chưa thiết lập tài khoản đăng nhập hoặc triển khai dùng chung qua Internet.

## Cấu trúc

Nếu không lưu được và báo **Mã MySQL: 1305**, database đang thiếu thủ tục nhập liệu. Dừng web bằng Ctrl+C và chạy:

```powershell
.\.venv\Scripts\python.exe app.py --init-db
.\.venv\Scripts\python.exe app.py
```

Nhập mật khẩu MySQL khi mỗi lệnh yêu cầu. `--init-db` đọc `sql/nhap-lieu-khach-san.sql` và chỉ tạo `ThemKhachHang` nếu chưa có, không xóa bảng, không chạy lại dữ liệu mẫu và không ghi đè thủ tục đã tồn tại. Tài khoản cài đặt cần quyền CREATE ROUTINE trong `hotel`. Sau đó lưu hồ sơ trên web như bình thường.

Trang Danh mục dịch vụ dùng INSERT trực tiếp, không cần thủ tục hoặc dữ liệu phòng/lượt lưu trú.

```text
app.py                         Điểm chạy web, nhập mật khẩu ở terminal
database_setup.py              Cài thủ tục còn thiếu qua --init-db
sql/                           Schema khách sạn và SQL cho hai form hiện tại
config.py / database.py         Cấu hình và thao tác MySQL hiện có
web/__init__.py                 Application factory, CSRF, cấu hình phiên
web/routes.py                   Hai trang và luồng GET/POST
web/validation.py               Kiểm tra dữ liệu phía server
web/templates/base.html        Header, điều hướng, bố cục, thông báo, footer
web/templates/components/      Macro trường nhập, select, CSRF dùng chung
web/templates/guests.html      Nội dung riêng của trang khách hàng
web/templates/services.html    Nội dung riêng của trang dịch vụ
web/static/css/system.css      Design tokens, component và responsive
web/static/js/interface.js     Menu mobile, phản hồi khi gửi biểu mẫu
web/static/fonts/              Host Grotesk tự lưu trữ và giấy phép OFL
DESIGN.md                      Đặc tả thiết kế do chủ dự án cung cấp
docs/ui-conventions.md         Cách áp dụng thiết kế và thêm trang mới
tests/test_web.py              Kiểm thử HTTP, validation, database mock
```

## Kiểm thử

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Các kiểm thử dùng database giả lập, không ghi dữ liệu MySQL thật. Kiểm tra giao diện bằng trình duyệt (tùy chọn, cần Edge hoặc Chrome trên Windows):

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe tests/browser_check.py
```

Ảnh kiểm tra được lưu ở `output/qa/`. Dữ liệu trong kiểm tra trình duyệt là dữ liệu mẫu; website thông thường luôn đọc MySQL.

## Thử nhập danh mục dịch vụ

Mở `/dich-vu`, nhập tên `Nước uống`, đơn vị `chai`, đơn giá `20000`, trạng thái `Đang cung cấp`, rồi bấm **Lưu dịch vụ**. Không cần tạo phòng hoặc lượt lưu trú. Giá là số nguyên đồng từ 0 đến 99999999999999, không dùng dấu chấm/phẩy phân cách. Tên tối đa 100 ký tự, đơn vị tối đa 30 ký tự.

Trong một tab Query của Workbench, chạy lại câu sau để xem dịch vụ mới:

```sql
SELECT MaDichVu, TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai
FROM hotel.DichVu
ORDER BY MaDichVu DESC
LIMIT 20;
```

Đối chiếu dòng mới nhất với thông tin vừa nhập. Refresh trang sau khi lưu không thêm dòng; bấm lưu một biểu mẫu hợp lệ lần nữa sẽ tạo dịch vụ mới, kể cả trùng tên. Nút **Làm mới** xóa biểu mẫu và đưa trạng thái về `Đang cung cấp`.

Thử giá `-1`, `1.5`, `20.000` hoặc để trống tên/đơn vị: phải báo lỗi và không thêm dữ liệu. Giá `0` hợp lệ; trạng thái `Ngừng cung cấp` cũng được lưu. Nếu lỗi database, kiểm tra thông báo mã MySQL trên trang.

## Thêm trang

Đọc `DESIGN.md` và `docs/ui-conventions.md`. Tạo template kế thừa `base.html`, sử dụng macro trong `components/forms.html` và class trong `system.css`. Đăng ký route và thêm liên kết điều hướng ở một nơi trong `base.html`. Không sao chép header, footer, CSS hoặc mã kết nối database sang từng trang.
