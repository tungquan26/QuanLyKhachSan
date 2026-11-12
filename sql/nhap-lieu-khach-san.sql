-- Thiết lập bảng bằng sql/khach-san.sql trước khi chạy tệp này.
-- Hai form hiện tại: Hồ sơ khách hàng và Danh mục dịch vụ.
USE hotel;
SET NAMES utf8mb4;

-- 1. Lễ tân nhập hồ sơ khách. CCCD là chuỗi để giữ chữ số 0 ở đầu.
DROP PROCEDURE IF EXISTS ThemKhachHang;
DELIMITER //
CREATE PROCEDURE ThemKhachHang(IN p_ho_ten VARCHAR(100), IN p_cccd VARCHAR(50),
                               IN p_dien_thoai VARCHAR(20))
BEGIN
    DECLARE EXIT HANDLER FOR 1062
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'CCCD đã có hồ sơ. Hãy tra cứu khách theo CCCD.';

    IF p_ho_ten IS NULL OR TRIM(p_ho_ten) = '' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Hãy nhập họ tên khách.';
    END IF;

    IF p_cccd IS NULL OR p_cccd NOT REGEXP '^[0-9]{12}$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'CCCD phải có đúng 12 chữ số.';
    END IF;

    -- Cột CCCD đã có UNIQUE nên MySQL cũng kiểm tra trùng khi lưu.
    INSERT INTO KhachHang (HoTen, CCCD, SoDienThoai)
    VALUES (TRIM(p_ho_ten), p_cccd, NULLIF(TRIM(p_dien_thoai), ''));
END //
DELIMITER ;

-- Form 1: tra CCCD trước khi thêm. Có kết quả thì dùng lại MaKhachHang.
-- Hồ sơ dùng chung cho người đứng tên đặt phòng và người đến ở.
SELECT MaKhachHang, HoTen, CCCD, SoDienThoai
FROM KhachHang
WHERE CCCD = '000000000001';

-- Form 2: tạo danh mục dịch vụ bằng INSERT trực tiếp, không cần thủ tục.
-- Không cần phòng, phiếu đặt phòng hoặc khách đang lưu trú.
-- Ví dụ thao tác lưu (bỏ dấu -- khi muốn chạy riêng để thử):
-- INSERT INTO DichVu (TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai)
-- VALUES ('Nước uống', 'chai', 20000, 'Đang cung cấp');
-- COMMIT;

-- Chạy lại sau khi nhập trên web để đối chiếu dữ liệu mới nhất.
SELECT MaDichVu, TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai
FROM DichVu
ORDER BY MaDichVu DESC
LIMIT 20;

-- DEMO: Bỏ dấu -- ở câu muốn thử rồi chạy riêng câu đó trong Workbench.
-- Nhập đúng: thêm một khách, sau đó xem hồ sơ vừa lưu.
-- CALL ThemKhachHang('Lê Minh', '000000000002', '0900000003');
-- SELECT * FROM KhachHang WHERE CCCD = '000000000002';
-- Chạy lại cùng lệnh CALL: MySQL báo trùng CCCD.
-- Nhập sai: mã chỉ có 3 chữ số, khách không được thêm.
-- CALL ThemKhachHang('Lê Minh', '123', '');

-- Kiểm thử form Danh mục dịch vụ trên web:
-- Tên 1–100 ký tự, đơn vị 1–30 ký tự.
-- Giá nguyên 0–99999999999999 đồng, không có dấu phân cách.
-- Trạng thái: Đang cung cấp hoặc Ngừng cung cấp.
-- Giá âm/thập phân hoặc tên/đơn vị trống: web phải từ chối lưu.
