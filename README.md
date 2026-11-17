# Hotel Desk — website nhập liệu khách sạn

Giao diện web tiếng Việt dùng Flask + Jinja, chạy trong trình duyệt, kết nối cùng MySQL `hotel` với Workbench. Các trang hiện có:

- `/khach-hang`: tạo hồ sơ khách hàng; nếu CCCD trùng thì báo lỗi và giữ thông tin đã nhập.
- `/dich-vu`: thêm danh mục dịch vụ trực tiếp, không cần phòng hoặc khách đang lưu trú.
- `/danh-sach/khach-hang`: xem và tra cứu khách hàng theo CCCD.
- `/danh-sach/dich-vu`: xem toàn bộ dịch vụ dưới dạng bảng.

Trang danh sách khách hàng đồng thời là màn hình tìm kiếm dữ liệu nghiệp vụ (mục 6): bấm kính lúp bên phải tiêu đề cột **CCCD**, nhập số CCCD hoặc một phần số rồi nhấn Enter hoặc kính lúp trong ô nhập để truy vấn MySQL và hiển thị bảng kết quả cùng số lượng tìm thấy. Bấm **Xóa lọc** để xem toàn bộ khách hàng. Chỉ tìm trong trường CCCD. Không dùng CustomTkinter nữa.

## Báo cáo doanh thu dịch vụ

Mở **Báo cáo thống kê → Doanh thu dịch vụ** trên sidebar, hoặc `/bao-cao/doanh-thu-dich-vu`. Chọn khoảng ngày rồi bấm **Xem báo cáo** hoặc **Xuất Excel (.xlsx)**. Cài lại `pip install -r requirements.txt` để có thư viện `openpyxl`.

Báo cáo đọc bảng `LanSuDungDichVu` kết hợp `DichVu`, gồm cả ngày bắt đầu và ngày kết thúc. Doanh thu tính bằng số lượng nhân đơn giá áp dụng lúc sử dụng; một dịch vụ có nhiều đơn giá được tách thành các dòng riêng. Số lượng lẻ và phần lẻ của thành tiền được giữ nguyên. File Excel giữ mẫu báo cáo với tổng cộng, ngày lập, vùng ký và cấu hình in A4. Ngày lập dùng múi giờ Việt Nam.

Tài khoản MySQL cần quyền `SELECT` trên hai bảng này. Không có dữ liệu thì báo cáo hiển thị rỗng với tổng bằng 0; lỗi truy vấn sẽ báo lỗi và không tải file Excel. Không cần chạy lại SQL hay tạo thủ tục. Các URL cũ `/bao-cao`, `/bao-cao-2`, `/bao_cao_2` vẫn dùng được.

Giao diện dạng bảng điều khiển: sidebar bên trái có nhóm **Quản lý thông tin** chứa hai mục con **Hồ sơ khách hàng** và **Danh mục dịch vụ**; vùng nội dung bên phải chứa tiêu đề và biểu mẫu. Trên màn hình nhỏ, dùng nút **Menu** để mở thanh chức năng.

Nhóm **Danh sách dữ liệu** trên sidebar chứa **Danh sách khách hàng** và **Danh sách dịch vụ**. Hai trang đọc dữ liệu từ bảng `KhachHang`/`DichVu`, sắp xếp theo mã tự tăng từ nhỏ đến lớn để dữ liệu nhập trước ở trên, nhập sau ở cuối danh sách, hiển thị số bản ghi hoặc số kết quả tra cứu. Cột mã khóa chính được ẩn trên giao diện và thay bằng **STT**, đánh số liên tục từ 1 tăng dần; mã trong database được giữ nguyên. Nhấn **F5** để đọc lại dữ liệu MySQL, kể cả dữ liệu thêm từ Workbench, giữ bộ lọc CCCD hiện tại và đánh lại STT. Kính lúp bên phải tiêu đề cột **CCCD** mở ô nhập tìm chuỗi con trong số căn cước công dân; ký tự `%` và `_` được hiểu theo mẫu tìm kiếm `like`. Truy vấn dùng tham số, không ghép từ khóa vào SQL. Khi không khớp bản ghi nào, trang hiển thị thông báo không tìm thấy. Bảng cuộn ngang trên màn hình nhỏ; giá trị SQL NULL hiển thị là `NULL`, chuỗi rỗng giữ nguyên ô trống. Chức năng thêm vẫn nằm trong nhóm **Quản lý thông tin**.

Hai danh sách chỉ hỗ trợ xem và tra cứu; chức năng sửa khách hàng và dịch vụ đã được loại bỏ.

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

Các truy vấn của web được đọc từ thư mục `sql`, nhóm theo đối tượng:

- `khach-hang.sql`: lần lượt là truy vấn danh sách, tra cứu CCCD và thêm khách hàng.
- `dich-vu.sql`: lần lượt là truy vấn danh sách và thêm dịch vụ.
- `bao-cao-doanh-thu-dich-vu.sql`: thống kê doanh thu dịch vụ.

Mỗi file truy vấn có `use hotel`, cấu hình UTF-8 và các lệnh `set @ten_bien = ...` với giá trị mẫu nếu cần tham số. Trong MySQL Workbench, chạy hai dòng đầu rồi chọn chạy phần chức năng cần dùng, bao gồm các lệnh `set` của phần đó. Phần thêm sẽ ghi dữ liệu mẫu vào database, tự lưu nếu Workbench bật autocommit. Chạy toàn bộ file gộp cũng thực hiện thao tác thêm; chạy lại có thể báo trùng CCCD hoặc tên dịch vụ.

`database.py` dùng `load_sql(filename, query_index=0)` để lấy một câu `select` hoặc `insert` theo thứ tự trong file, đánh số từ 0. File khách hàng dùng 0 cho danh sách, 1 cho tra cứu CCCD, 2 cho thêm; file dịch vụ dùng 0 cho danh sách, 1 cho thêm. Không cần comment đánh dấu. Giữ đúng thứ tự truy vấn; nếu đổi thứ tự phải cập nhật chỉ số tương ứng trong Python. Các file báo cáo dùng chỉ số mặc định 0. Web chỉ thực thi câu truy vấn được chọn, không chạy toàn bộ file. Các biến `@ten_bien` được chuyển thành `%s` theo thứ tự xuất hiện, rồi truyền giá trị thật từ web riêng qua thư viện MySQL. Web không chạy phần `set` mẫu. Mỗi câu truy vấn bắt đầu ở đầu dòng và kết thúc bằng dấu chấm phẩy, không chứa dấu chấm phẩy trong chuỗi; tên biến chỉ dùng chữ thường, chữ số và dấu gạch dưới, đặt ở vị trí tham số. Các file `khach-san.sql` và `nhap-lieu-khach-san.sql` không được bộ đọc tự động thực thi.

Hai trang Khách hàng và Danh mục dịch vụ kiểm tra dữ liệu ở phía server, dùng `INSERT` có tham số rồi commit khi thành công. Tài khoản MySQL cần quyền `SELECT` và `INSERT` trên cả `KhachHang` và `DichVu`.

```text
app.py                         Điểm chạy web, nhập mật khẩu ở terminal
sql/                           Schema khách sạn và SQL cho hai form hiện tại
config.py / database.py         Cấu hình và thao tác MySQL hiện có
web/__init__.py                 Application factory, CSRF, cấu hình phiên
web/routes.py                   Các trang thêm GET/POST, danh sách và báo cáo
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

## Chống trùng danh mục

Tên dịch vụ và tên loại phòng phải duy nhất, lần lượt được bảo vệ bởi
`uq_dichvu_tendichvu` và `uq_loaiphong_tenloaiphong`. Dịch vụ cùng tên vẫn bị
từ chối dù khác đơn vị tính, giá hoặc trạng thái. Việc so sánh tên dùng
collation hiện có của cột; form loại khoảng trắng đầu và cuối trước khi lưu.

Database mới nhận các ràng buộc từ `sql/khach-san.sql`. Với database đã có dữ
liệu, mở `sql/nang-cap-unique-danh-muc.sql` trong Workbench và chạy hai truy vấn
kiểm tra trước. Nếu có kết quả, xử lý các bản ghi trùng theo nghiệp vụ rồi kiểm
tra lại; script không tự xóa hoặc gộp dữ liệu. Khi cả hai kết quả rỗng, bỏ comment
và chạy từng lệnh `alter table` cuối file một lần. Không chạy các lệnh này nếu
database đã có ràng buộc tương ứng. Các lệnh thay đổi cấu trúc không tạo thành
một transaction chung; nếu một lệnh thất bại, kiểm tra cấu trúc trước khi chạy lại.

Form dịch vụ báo “Tên dịch vụ đã tồn tại.” và giữ thông tin nhập khi gặp tên
trùng (HTTP 409). CCCD khách hàng và mã phiếu trên hóa đơn tiếp tục có `unique`;
các bảng khác giữ khóa chính và các ràng buộc hiện tại.

## Chạy kiểm thử

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
