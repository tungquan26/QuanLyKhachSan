# Hotel Desk — website nhập liệu khách sạn

Giao diện web tiếng Việt dùng Flask + Jinja, chạy trong trình duyệt, kết nối cùng MySQL `hotel` với Workbench. Các trang hiện có:

- `/khach-hang`: tạo hồ sơ khách hàng; nếu CCCD trùng thì báo lỗi và giữ thông tin đã nhập.
- `/dich-vu`: thêm danh mục dịch vụ trực tiếp, không cần phòng hoặc khách đang lưu trú.
- `/danh-sach/khach-hang`: xem toàn bộ khách hàng dưới dạng bảng.
- `/danh-sach/dich-vu`: xem toàn bộ dịch vụ dưới dạng bảng.

Chưa triển khai màn hình tìm kiếm nghiệp vụ (mục 6). Không dùng CustomTkinter nữa.

## Báo cáo doanh thu dịch vụ

Mở **Báo cáo thống kê → Doanh thu dịch vụ** trên sidebar, hoặc `/bao-cao/doanh-thu-dich-vu`. Chọn khoảng ngày, nhập tên đơn vị trên báo cáo rồi bấm **Xem báo cáo** hoặc **Xuất Excel (.xlsx)**. Cài lại `pip install -r requirements.txt` để có thư viện `openpyxl`.

Báo cáo đọc bảng `LanSuDungDichVu` kết hợp `DichVu`, gồm cả ngày bắt đầu và ngày kết thúc. Doanh thu tính bằng số lượng nhân đơn giá áp dụng lúc sử dụng; một dịch vụ có nhiều đơn giá được tách thành các dòng riêng. Số lượng lẻ và phần lẻ của thành tiền được giữ nguyên. Tên đơn vị chỉ dùng làm tiêu đề, không lọc dữ liệu theo chi nhánh. File Excel giữ mẫu báo cáo với tổng cộng, ngày lập, vùng ký và cấu hình in A4. Ngày lập dùng múi giờ Việt Nam.

Tài khoản MySQL cần quyền `SELECT` trên hai bảng này. Không có dữ liệu thì báo cáo hiển thị rỗng với tổng bằng 0; lỗi truy vấn sẽ báo lỗi và không tải file Excel. Không cần chạy lại SQL hay tạo thủ tục. Các URL cũ `/bao-cao`, `/bao-cao-2`, `/bao_cao_2` vẫn dùng được.

Giao diện dạng bảng điều khiển: sidebar bên trái có nhóm **Quản lý thông tin** chứa hai mục con **Hồ sơ khách hàng** và **Danh mục dịch vụ**; vùng nội dung bên phải chứa tiêu đề và biểu mẫu. Trên màn hình nhỏ, dùng nút **Menu** để mở thanh chức năng.

Nhóm **Danh sách dữ liệu** trên sidebar chứa **Danh sách khách hàng** và **Danh sách dịch vụ**. Hai trang đọc toàn bộ dòng từ bảng `KhachHang`/`DichVu`, sắp xếp theo mã tự tăng từ nhỏ đến lớn để dữ liệu nhập trước ở trên, nhập sau ở cuối danh sách, hiển thị tổng số bản ghi. Cột mã khóa chính được ẩn trên giao diện và thay bằng **STT**, đánh số liên tục từ 1 tăng dần; mã trong database được giữ nguyên. Nút **Làm mới** đọc lại dữ liệu MySQL, kể cả dữ liệu thêm từ Workbench, và đánh lại STT theo danh sách hiện tại. Bảng cuộn ngang trên màn hình nhỏ; giá trị SQL NULL hiển thị là `NULL`, chuỗi rỗng giữ nguyên ô trống. Mỗi dòng có nút **Sửa** mở biểu mẫu chứa dữ liệu hiện tại.

Để chỉnh dữ liệu: vào danh sách khách hàng/dịch vụ → **Sửa** ở dòng cần đổi → chỉnh thông tin → **Lưu thay đổi**. Có thể sửa họ tên, CCCD, số điện thoại; hoặc tên dịch vụ, đơn vị tính, đơn giá, trạng thái cung cấp. Nút **Hủy** quay về danh sách. Cập nhật theo mã gốc, không tạo dòng mới, không đổi khóa chính hay thứ tự dòng. Khi dữ liệu không hợp lệ hoặc CCCD trùng, biểu mẫu giữ thông tin đã nhập và báo lỗi. Bản ghi đã bị xóa sẽ được thông báo và quay về danh sách.

## Chạy trên Windows

Python 3.11 trở lên. Khi thiết lập MySQL lần đầu, chạy `sql/khach-san.sql` để tạo database `hotel` và các bảng. Nếu đã có dữ liệu, sử dụng database hiện tại; không chạy lại script khởi tạo.

`sql/khach-san.sql` chỉ định nghĩa bảng, ràng buộc và trigger; không thêm khách, phòng hay lượt lưu trú mẫu. Hai form Khách hàng và Danh mục dịch vụ có thể nhập dữ liệu ngay khi các bảng đang trống.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Nhập mật khẩu MySQL trong terminal (không hiển thị và chỉ giữ trong bộ nhớ), rồi mở **http://127.0.0.1:5000**. Dừng bằng Ctrl+C. Có thể cấu hình `MYSQL_PASSWORD` qua biến môi trường phía server để bỏ qua lời nhắc. Không nhập mật khẩu database trên website.

Kết nối mặc định: `127.0.0.1:3306`, tài khoản `root`, database `hotel`. Đặt `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER` nếu khác; `PORT` đổi cổng website. Đây là cấu hình chạy cục bộ, chỉ lắng nghe trên loopback; chưa thiết lập tài khoản đăng nhập hoặc triển khai dùng chung qua Internet.

## Cấu trúc

Hai trang Khách hàng và Danh mục dịch vụ kiểm tra dữ liệu ở phía server, dùng `INSERT` có tham số để thêm và `UPDATE ... WHERE` có tham số để sửa bảng `KhachHang` và `DichVu`, rồi commit khi thành công. Không cần stored procedure hoặc chạy `--init-db`. Tài khoản MySQL cần quyền `SELECT`, `INSERT` và `UPDATE` trên cả `KhachHang` và `DichVu`.

```text
app.py                         Điểm chạy web, nhập mật khẩu ở terminal
sql/                           Schema khách sạn và SQL cho hai form hiện tại
config.py / database.py         Cấu hình và thao tác MySQL hiện có
web/__init__.py                 Application factory, CSRF, cấu hình phiên
web/routes.py                   Các trang thêm/sửa GET/POST và danh sách GET
web/validation.py               Kiểm tra dữ liệu phía server
web/templates/base.html        Sidebar, thanh tiêu đề, bố cục, thông báo, footer
web/templates/components/      Macro trường nhập, select, CSRF dùng chung
web/templates/guests.html      Nội dung riêng của trang khách hàng
web/templates/services.html    Nội dung riêng của trang dịch vụ
web/templates/data_list.html   Bảng dữ liệu dùng chung cho khách hàng/dịch vụ
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

Nhập trực tiếp bằng SQL:

```sql
use hotel;
insert into DichVu (TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai)
values ('Nước uống', 'chai', 20000, 'Đang cung cấp');
commit;
```

Trong một tab Query của Workbench, chạy lại câu sau để xem dịch vụ mới:

```sql
select MaDichVu, TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai
from hotel.DichVu
order by MaDichVu desc
limit 20;
```

Đối chiếu dòng mới nhất với thông tin vừa nhập. Refresh trang sau khi lưu không thêm dòng; bấm lưu một biểu mẫu hợp lệ lần nữa sẽ tạo dịch vụ mới, kể cả trùng tên. Nút **Làm mới** xóa biểu mẫu và đưa trạng thái về `Đang cung cấp`.

Thử giá `-1`, `1.5`, `20.000` hoặc để trống tên/đơn vị: phải báo lỗi và không thêm dữ liệu. Giá `0` hợp lệ; trạng thái `Ngừng cung cấp` cũng được lưu. Nếu lỗi database, kiểm tra thông báo mã MySQL trên trang.

## Thêm trang

Đọc `DESIGN.md` và `docs/ui-conventions.md`. Tạo template kế thừa `base.html`, sử dụng macro trong `components/forms.html` và class trong `system.css`. Đăng ký route và thêm liên kết điều hướng ở một nơi trong `base.html`. Không sao chép header, footer, CSS hoặc mã kết nối database sang từng trang.
