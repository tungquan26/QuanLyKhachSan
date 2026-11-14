-- Thiết lập bảng bằng sql/khach-san.sql trước khi chạy tệp này.
-- Hai form hiện tại: Hồ sơ khách hàng và Danh mục dịch vụ.
use hotel;
set names utf8mb4;

-- 1. Lễ tân nhập hồ sơ khách. CCCD là chuỗi để giữ chữ số 0 ở đầu.
drop procedure if exists ThemKhachHang;
delimiter //
create procedure ThemKhachHang(in p_ho_ten varchar(100), in p_cccd varchar(50),
                               in p_dien_thoai varchar(20))
begin
    declare exit handler for 1062
        signal sqlstate '45000' set message_text = 'CCCD đã có hồ sơ. Hãy tra cứu khách theo CCCD.';

    if p_ho_ten is null or trim(p_ho_ten) = '' then
        signal sqlstate '45000' set message_text = 'Hãy nhập họ tên khách.';
    end if;

    if p_cccd is null or p_cccd not regexp '^[0-9]{12}$' then
        signal sqlstate '45000' set message_text = 'CCCD phải có đúng 12 chữ số.';
    end if;

    -- Cột CCCD đã có unique nên MySQL cũng kiểm tra trùng khi lưu.
    insert into KhachHang (HoTen, CCCD, SoDienThoai)
    values (trim(p_ho_ten), p_cccd, nullif(trim(p_dien_thoai), ''));
end //
delimiter ;

-- Form 1: tra CCCD trước khi thêm. Có kết quả thì dùng lại MaKhachHang.
-- Hồ sơ dùng chung cho người đứng tên đặt phòng và người đến ở.
select MaKhachHang, HoTen, CCCD, SoDienThoai
from KhachHang
where CCCD = '000000000001';

-- 2. Lễ tân nhập danh mục dịch vụ từ web hoặc Workbench.
-- Không cần phòng, phiếu đặt phòng hoặc khách đang lưu trú.
drop procedure if exists ThemDichVu;
delimiter //
create procedure ThemDichVu(in p_ten text, in p_don_vi text,
                           in p_don_gia text, in p_trang_thai text)
begin
    if p_ten is null or char_length(trim(p_ten)) not between 1 and 100 then
        signal sqlstate '45000' set message_text = 'Nhập tên dịch vụ từ 1 đến 100 ký tự.';
    end if;

    if p_don_vi is null or char_length(trim(p_don_vi)) not between 1 and 30 then
        signal sqlstate '45000' set message_text = 'Nhập đơn vị tính từ 1 đến 30 ký tự.';
    end if;

    -- Nhận giá dưới dạng chuỗi để từ chối số lẻ trước khi MySQL làm tròn.
    if p_don_gia is null or p_don_gia not regexp '^[0-9]{1,14}$' then
        signal sqlstate '45000' set message_text = 'Đơn giá phải là số nguyên từ 0 đến 99999999999999 đồng.';
    end if;

    if p_trang_thai is null or p_trang_thai not in ('Đang cung cấp', 'Ngừng cung cấp') then
        signal sqlstate '45000' set message_text = 'Hãy chọn trạng thái Đang cung cấp hoặc Ngừng cung cấp.';
    end if;

    insert into DichVu (TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai)
    values (trim(p_ten), trim(p_don_vi), cast(p_don_gia as decimal(14,0)), p_trang_thai);
end //
delimiter ;

-- Form 2: nút Lưu dịch vụ gọi ThemDichVu rồi commit khi thành công.
-- Ví dụ thao tác lưu (bỏ dấu -- khi muốn chạy riêng để thử):
-- call ThemDichVu('Nước uống', 'chai', '20000', 'Đang cung cấp');
-- commit;

-- Chạy lại sau khi nhập trên web để đối chiếu dữ liệu mới nhất.
select MaDichVu, TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai
from DichVu
order by MaDichVu desc
limit 20;

-- DEMO: Bỏ dấu -- ở câu muốn thử rồi chạy riêng câu đó trong Workbench.
-- Nhập đúng: thêm một khách, sau đó xem hồ sơ vừa lưu.
-- call ThemKhachHang('Lê Minh', '000000000002', '0900000003');
-- select * from KhachHang where CCCD = '000000000002';
-- Chạy lại cùng lệnh call: MySQL báo trùng CCCD.
-- Nhập sai: mã chỉ có 3 chữ số, khách không được thêm.
-- call ThemKhachHang('Lê Minh', '123', '');

-- Kiểm thử form Danh mục dịch vụ trên web:
-- Tên 1–100 ký tự, đơn vị 1–30 ký tự.
-- Giá nguyên 0–99999999999999 đồng, không có dấu phân cách.
-- Trạng thái: Đang cung cấp hoặc Ngừng cung cấp.
-- Giá âm/thập phân hoặc tên/đơn vị trống: web phải từ chối lưu.
