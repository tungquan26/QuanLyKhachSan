USE hotel;
SET NAMES utf8mb4;

-- 1. Danh mục
CREATE TABLE KhachHang (
    MaKhachHang INT PRIMARY KEY AUTO_INCREMENT,
    HoTen VARCHAR(100) NOT NULL,
    CCCD VARCHAR(12) NOT NULL UNIQUE,
    SoDienThoai VARCHAR(20)
);

CREATE TABLE NhanVien (
    MaNhanVien INT PRIMARY KEY AUTO_INCREMENT,
    HoTen VARCHAR(100) NOT NULL,
    SoDienThoai VARCHAR(20),
    ChucVu VARCHAR(50) NOT NULL
);

CREATE TABLE LoaiPhong (
    MaLoaiPhong INT PRIMARY KEY AUTO_INCREMENT,
    TenLoaiPhong VARCHAR(80) NOT NULL,
    GiaNiemYetMoiDem DECIMAL(14,0) NOT NULL CHECK (GiaNiemYetMoiDem >= 0)
);

CREATE TABLE Phong (
    MaPhong VARCHAR(12) PRIMARY KEY,
    MaLoaiPhong INT NOT NULL,
    TinhTrangVanHanh VARCHAR(40) NOT NULL,
    FOREIGN KEY (MaLoaiPhong) REFERENCES LoaiPhong(MaLoaiPhong)
);

CREATE TABLE DichVu (
    MaDichVu INT PRIMARY KEY AUTO_INCREMENT,
    TenDichVu VARCHAR(100) NOT NULL,
    DonViTinh VARCHAR(30) NOT NULL,
    DonGiaHienHanh DECIMAL(14,0) NOT NULL CHECK (DonGiaHienHanh >= 0),
    TrangThai VARCHAR(40) NOT NULL
);

-- 2. Giao dịch
CREATE TABLE PhieuDatPhong (
    MaPhieu INT PRIMARY KEY AUTO_INCREMENT,
    MaKhachHang INT NOT NULL,
    MaNhanVienTiepNhan INT NOT NULL,
    NgayDat DATE NOT NULL,
    TrangThaiPhieu VARCHAR(40) NOT NULL,
    FOREIGN KEY (MaKhachHang) REFERENCES KhachHang(MaKhachHang),
    FOREIGN KEY (MaNhanVienTiepNhan) REFERENCES NhanVien(MaNhanVien)
);

CREATE TABLE ChiTietDatPhong (
    MaChiTietDatPhong INT PRIMARY KEY AUTO_INCREMENT,
    MaPhieu INT NOT NULL,
    MaPhong VARCHAR(12) NOT NULL,
    NgayNhanDuKien DATE NOT NULL,
    NgayTraDuKien DATE NOT NULL,
    ThoiDiemNhanThucTe DATETIME,
    ThoiDiemTraThucTe DATETIME,
    DonGiaPhongApDung DECIMAL(14,0) NOT NULL CHECK (DonGiaPhongApDung >= 0),
    CHECK (NgayTraDuKien > NgayNhanDuKien),
    CHECK (ThoiDiemTraThucTe IS NULL OR
          (ThoiDiemNhanThucTe IS NOT NULL AND ThoiDiemTraThucTe >= ThoiDiemNhanThucTe)),
    FOREIGN KEY (MaPhieu) REFERENCES PhieuDatPhong(MaPhieu),
    FOREIGN KEY (MaPhong) REFERENCES Phong(MaPhong)
);

CREATE TABLE LanSuDungDichVu (
    MaLanSuDung INT PRIMARY KEY AUTO_INCREMENT,
    MaChiTietDatPhong INT NOT NULL,
    MaDichVu INT NOT NULL,
    ThoiDiemSuDung DATETIME NOT NULL,
    SoLuong DECIMAL(9,2) NOT NULL CHECK (SoLuong > 0),
    DonGiaApDung DECIMAL(14,0) NOT NULL CHECK (DonGiaApDung >= 0),
    FOREIGN KEY (MaChiTietDatPhong) REFERENCES ChiTietDatPhong(MaChiTietDatPhong),
    FOREIGN KEY (MaDichVu) REFERENCES DichVu(MaDichVu)
);

-- 3. Quy tắc chốt giá phòng
-- Chốt giá niêm yết của loại phòng khi thêm chi tiết đặt phòng.
-- Giá đã chốt không đổi khi bảng giá của LoaiPhong thay đổi.
DROP TRIGGER IF EXISTS ChiTietDatPhong_ChotGia;
DROP TRIGGER IF EXISTS ChiTietDatPhong_KhoaGia;
DELIMITER //
CREATE TRIGGER ChiTietDatPhong_ChotGia
BEFORE INSERT ON ChiTietDatPhong
FOR EACH ROW
BEGIN
    SET NEW.DonGiaPhongApDung = (
        SELECT lp.GiaNiemYetMoiDem
        FROM Phong AS p
        JOIN LoaiPhong AS lp ON lp.MaLoaiPhong = p.MaLoaiPhong
        WHERE p.MaPhong = NEW.MaPhong
    );
END //

CREATE TRIGGER ChiTietDatPhong_KhoaGia
BEFORE UPDATE ON ChiTietDatPhong
FOR EACH ROW
BEGIN
    IF NEW.DonGiaPhongApDung <> OLD.DonGiaPhongApDung THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'DonGiaPhongApDung da duoc chot khi dat phong';
    END IF;
END //
DELIMITER ;
