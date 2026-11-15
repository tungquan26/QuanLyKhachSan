-- DU LIEU NGHIEP VU CUA BAI TAP LON: dung voi sql/khach-san.sql.
-- Giu nguyen cac ban ghi, gia, ngay va quan he cua bo du lieu ban dau.
-- Database moi: giu @chi_bo_sung = FALSE de nap 91 ban ghi cu + 13 ban ghi moi.
-- Da nap bo 91 ban ghi cu: doi @chi_bo_sung = TRUE de chi them 3 phieu moi.
-- Neu da bo sung: khong chay lai; file se bao loi va ROLLBACK neu trung phieu.
-- Du lieu duoc them trong mot transaction: loi bat ky dau se ROLLBACK toan bo.
-- LAST_INSERT_ID() lay ma vua tao, khong gia dinh ma bat dau tu 1.
-- Quyen: SELECT, INSERT, CREATE ROUTINE, ALTER ROUTINE, EXECUTE.
-- Chay trong phien khong co transaction dang lam do.
USE hotel;
SET NAMES utf8mb4;
SET @chi_bo_sung = FALSE;

DROP PROCEDURE IF EXISTS sp_nhap_lieu_khach_san_btl;
DELIMITER $$
CREATE PROCEDURE sp_nhap_lieu_khach_san_btl(IN p_chi_bo_sung BOOLEAN)
BEGIN
    DECLARE v_khach_1 INT;
    DECLARE v_khach_2 INT;
    DECLARE v_khach_3 INT;
    DECLARE v_khach_4 INT;
    DECLARE v_khach_5 INT;
    DECLARE v_khach_6 INT;
    DECLARE v_khach_7 INT;
    DECLARE v_khach_8 INT;
    DECLARE v_khach_9 INT;
    DECLARE v_khach_10 INT;
    DECLARE v_nhan_vien_1 INT;
    DECLARE v_nhan_vien_2 INT;
    DECLARE v_nhan_vien_3 INT;
    DECLARE v_nhan_vien_4 INT;
    DECLARE v_nhan_vien_5 INT;
    DECLARE v_nhan_vien_6 INT;
    DECLARE v_nhan_vien_7 INT;
    DECLARE v_nhan_vien_8 INT;
    DECLARE v_loai_1 INT;
    DECLARE v_loai_2 INT;
    DECLARE v_loai_3 INT;
    DECLARE v_loai_4 INT;
    DECLARE v_loai_5 INT;
    DECLARE v_loai_6 INT;
    DECLARE v_loai_7 INT;
    DECLARE v_loai_8 INT;
    DECLARE v_dich_vu_1 INT;
    DECLARE v_dich_vu_2 INT;
    DECLARE v_dich_vu_3 INT;
    DECLARE v_dich_vu_4 INT;
    DECLARE v_dich_vu_5 INT;
    DECLARE v_dich_vu_6 INT;
    DECLARE v_dich_vu_7 INT;
    DECLARE v_dich_vu_8 INT;
    DECLARE v_dich_vu_9 INT;
    DECLARE v_phieu_1 INT;
    DECLARE v_phieu_2 INT;
    DECLARE v_phieu_3 INT;
    DECLARE v_phieu_4 INT;
    DECLARE v_phieu_5 INT;
    DECLARE v_phieu_6 INT;
    DECLARE v_phieu_7 INT;
    DECLARE v_phieu_8 INT;
    DECLARE v_phieu_nhieu_phong INT;
    DECLARE v_phieu_huy INT;
    DECLARE v_phieu_dat_them INT;
    DECLARE v_chi_tiet_1 INT;
    DECLARE v_chi_tiet_2 INT;
    DECLARE v_chi_tiet_3 INT;
    DECLARE v_chi_tiet_4 INT;
    DECLARE v_chi_tiet_5 INT;
    DECLARE v_chi_tiet_6 INT;
    DECLARE v_chi_tiet_7 INT;
    DECLARE v_chi_tiet_8 INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    IF p_chi_bo_sung THEN
        -- CCCD la khoa UNIQUE: tim dung khach, khong gia dinh ma tu tang.
        SET v_khach_1 = (SELECT MaKhachHang FROM KhachHang WHERE CCCD = '012345000000');
        SET v_khach_9 = (SELECT MaKhachHang FROM KhachHang WHERE CCCD = '012345000008');
        SET v_khach_10 = (SELECT MaKhachHang FROM KhachHang WHERE CCCD = '012345000009');
        IF v_khach_1 IS NULL OR v_khach_9 IS NULL OR v_khach_10 IS NULL THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Thieu khach cua bo du lieu goc. Chua bo sung du lieu.';
        END IF;
        IF (SELECT COUNT(*) FROM NhanVien
            WHERE HoTen = 'Trần Thị Lan' AND SoDienThoai = '0331000001') <> 1 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Can dung mot nhan vien Tran Thi Lan, SDT 0331000001.';
        END IF;
        SET v_nhan_vien_1 = (SELECT MaNhanVien FROM NhanVien
                            WHERE HoTen = 'Trần Thị Lan' AND SoDienThoai = '0331000001');
        IF (SELECT COUNT(*) FROM Phong p JOIN LoaiPhong lp ON lp.MaLoaiPhong = p.MaLoaiPhong
            WHERE (p.MaPhong = '101' AND lp.TenLoaiPhong = 'Standard Single')
               OR (p.MaPhong = '102' AND lp.TenLoaiPhong = 'Standard Double')
               OR (p.MaPhong = '103' AND lp.TenLoaiPhong = 'Superior Single')
               OR (p.MaPhong = '107' AND lp.TenLoaiPhong = 'Suite')) <> 4 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Thieu phong 101, 102, 103, 107 hoac loai phong khac bo du lieu goc.';
        END IF;
    ELSE
    -- KhachHang: ghi ro cot va lien ket bang ma vua tao.
    INSERT INTO KhachHang (HoTen, CCCD, SoDienThoai)
    VALUES ('Nguyễn Văn A', '012345000000', '0320000000');
    SET v_khach_1 = LAST_INSERT_ID();
    INSERT INTO KhachHang (HoTen, CCCD, SoDienThoai)
    VALUES ('Nguyễn Văn B', '012345000001', '0320000001');
    SET v_khach_2 = LAST_INSERT_ID();
    INSERT INTO KhachHang (HoTen, CCCD, SoDienThoai)
    VALUES ('Nguyễn Văn C', '012345000002', '0320000002');
    SET v_khach_3 = LAST_INSERT_ID();
    INSERT INTO KhachHang (HoTen, CCCD, SoDienThoai)
    VALUES ('Nguyễn Văn D', '012345000003', '0320000003');
    SET v_khach_4 = LAST_INSERT_ID();
    INSERT INTO KhachHang (HoTen, CCCD, SoDienThoai)
    VALUES ('Nguyễn Văn E', '012345000004', '0320000004');
    SET v_khach_5 = LAST_INSERT_ID();
    INSERT INTO KhachHang (HoTen, CCCD, SoDienThoai)
    VALUES ('Nguyễn Văn F', '012345000005', '0320000005');
    SET v_khach_6 = LAST_INSERT_ID();
    INSERT INTO KhachHang (HoTen, CCCD, SoDienThoai)
    VALUES ('Nguyễn Văn G', '012345000006', '0320000006');
    SET v_khach_7 = LAST_INSERT_ID();
    INSERT INTO KhachHang (HoTen, CCCD, SoDienThoai)
    VALUES ('Nguyễn Văn H', '012345000007', '0320000007');
    SET v_khach_8 = LAST_INSERT_ID();
    INSERT INTO KhachHang (HoTen, CCCD, SoDienThoai)
    VALUES ('Nguyễn Văn I', '012345000008', '0320000008');
    SET v_khach_9 = LAST_INSERT_ID();
    INSERT INTO KhachHang (HoTen, CCCD, SoDienThoai)
    VALUES ('Nguyễn Văn K', '012345000009', '0320000009');
    SET v_khach_10 = LAST_INSERT_ID();

    -- NhanVien: ghi ro cot va lien ket bang ma vua tao.
    INSERT INTO NhanVien (HoTen, SoDienThoai, ChucVu)
    VALUES ('Trần Thị Lan', '0331000001', 'Lễ tân');
    SET v_nhan_vien_1 = LAST_INSERT_ID();
    INSERT INTO NhanVien (HoTen, SoDienThoai, ChucVu)
    VALUES ('Lê Minh Tuấn', '0331000002', 'Lễ tân');
    SET v_nhan_vien_2 = LAST_INSERT_ID();
    INSERT INTO NhanVien (HoTen, SoDienThoai, ChucVu)
    VALUES ('Phạm Ngọc Mai', '0331000003', 'Lễ tân');
    SET v_nhan_vien_3 = LAST_INSERT_ID();
    INSERT INTO NhanVien (HoTen, SoDienThoai, ChucVu)
    VALUES ('Võ Quốc Huy', '0331000004', 'Quản lý');
    SET v_nhan_vien_4 = LAST_INSERT_ID();
    INSERT INTO NhanVien (HoTen, SoDienThoai, ChucVu)
    VALUES ('Đặng Thị Hoa', '0331000005', 'Lễ tân');
    SET v_nhan_vien_5 = LAST_INSERT_ID();
    INSERT INTO NhanVien (HoTen, SoDienThoai, ChucVu)
    VALUES ('Bùi Thanh Nam', '0331000006', 'Lễ tân');
    SET v_nhan_vien_6 = LAST_INSERT_ID();
    INSERT INTO NhanVien (HoTen, SoDienThoai, ChucVu)
    VALUES ('Hoàng Mỹ Linh', '0331000007', 'Lễ tân');
    SET v_nhan_vien_7 = LAST_INSERT_ID();
    INSERT INTO NhanVien (HoTen, SoDienThoai, ChucVu)
    VALUES ('Ngô Đức Anh', '0331000008', 'Lễ tân');
    SET v_nhan_vien_8 = LAST_INSERT_ID();

    -- LoaiPhong: ghi ro cot va lien ket bang ma vua tao.
    INSERT INTO LoaiPhong (TenLoaiPhong, GiaNiemYetMoiDem)
    VALUES ('Standard Single', 400000);
    SET v_loai_1 = LAST_INSERT_ID();
    INSERT INTO LoaiPhong (TenLoaiPhong, GiaNiemYetMoiDem)
    VALUES ('Standard Double', 500000);
    SET v_loai_2 = LAST_INSERT_ID();
    INSERT INTO LoaiPhong (TenLoaiPhong, GiaNiemYetMoiDem)
    VALUES ('Superior Single', 600000);
    SET v_loai_3 = LAST_INSERT_ID();
    INSERT INTO LoaiPhong (TenLoaiPhong, GiaNiemYetMoiDem)
    VALUES ('Superior Double', 700000);
    SET v_loai_4 = LAST_INSERT_ID();
    INSERT INTO LoaiPhong (TenLoaiPhong, GiaNiemYetMoiDem)
    VALUES ('Deluxe Double', 900000);
    SET v_loai_5 = LAST_INSERT_ID();
    INSERT INTO LoaiPhong (TenLoaiPhong, GiaNiemYetMoiDem)
    VALUES ('Deluxe Twin', 1000000);
    SET v_loai_6 = LAST_INSERT_ID();
    INSERT INTO LoaiPhong (TenLoaiPhong, GiaNiemYetMoiDem)
    VALUES ('Suite', 1500000);
    SET v_loai_7 = LAST_INSERT_ID();
    INSERT INTO LoaiPhong (TenLoaiPhong, GiaNiemYetMoiDem)
    VALUES ('Family', 1800000);
    SET v_loai_8 = LAST_INSERT_ID();

    -- Phong: ghi ro cot va lien ket bang ma vua tao.
    INSERT INTO Phong (MaPhong, MaLoaiPhong, TinhTrangVanHanh)
    VALUES ('101', v_loai_1, 'Hoạt động');
    INSERT INTO Phong (MaPhong, MaLoaiPhong, TinhTrangVanHanh)
    VALUES ('102', v_loai_2, 'Hoạt động');
    INSERT INTO Phong (MaPhong, MaLoaiPhong, TinhTrangVanHanh)
    VALUES ('103', v_loai_3, 'Hoạt động');
    INSERT INTO Phong (MaPhong, MaLoaiPhong, TinhTrangVanHanh)
    VALUES ('104', v_loai_4, 'Hoạt động');
    INSERT INTO Phong (MaPhong, MaLoaiPhong, TinhTrangVanHanh)
    VALUES ('105', v_loai_5, 'Hoạt động');
    INSERT INTO Phong (MaPhong, MaLoaiPhong, TinhTrangVanHanh)
    VALUES ('106', v_loai_6, 'Hoạt động');
    INSERT INTO Phong (MaPhong, MaLoaiPhong, TinhTrangVanHanh)
    VALUES ('107', v_loai_7, 'Hoạt động');
    INSERT INTO Phong (MaPhong, MaLoaiPhong, TinhTrangVanHanh)
    VALUES ('108', v_loai_8, 'Hoạt động');

    -- DichVu: ghi ro cot va lien ket bang ma vua tao.
    INSERT INTO DichVu (TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai)
    VALUES ('Nước lọc', 'chai', 10000, 'Đang cung cấp');
    SET v_dich_vu_1 = LAST_INSERT_ID();
    INSERT INTO DichVu (TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai)
    VALUES ('Nước suối', 'chai', 10000, 'Đang cung cấp');
    SET v_dich_vu_2 = LAST_INSERT_ID();
    INSERT INTO DichVu (TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai)
    VALUES ('Nước khoáng', 'chai', 10000, 'Đang cung cấp');
    SET v_dich_vu_3 = LAST_INSERT_ID();
    INSERT INTO DichVu (TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai)
    VALUES ('Nước ngọt', 'chai', 10000, 'Đang cung cấp');
    SET v_dich_vu_4 = LAST_INSERT_ID();
    INSERT INTO DichVu (TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai)
    VALUES ('Coca Cola', 'chai', 15000, 'Đang cung cấp');
    SET v_dich_vu_5 = LAST_INSERT_ID();
    INSERT INTO DichVu (TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai)
    VALUES ('Pepsi', 'chai', 15000, 'Đang cung cấp');
    SET v_dich_vu_6 = LAST_INSERT_ID();
    INSERT INTO DichVu (TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai)
    VALUES ('Rượu trắng', 'chai', 100000, 'Đang cung cấp');
    SET v_dich_vu_7 = LAST_INSERT_ID();
    INSERT INTO DichVu (TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai)
    VALUES ('Rượu vang', 'chai', 1000000, 'Đang cung cấp');
    SET v_dich_vu_8 = LAST_INSERT_ID();
    INSERT INTO DichVu (TenDichVu, DonViTinh, DonGiaHienHanh, TrangThai)
    VALUES ('Snack', 'gói', 10000, 'Đang cung cấp');
    SET v_dich_vu_9 = LAST_INSERT_ID();

    -- PhieuDatPhong: ghi ro cot va lien ket bang ma vua tao.
    INSERT INTO PhieuDatPhong (MaPhieu, MaKhachHang, MaNhanVienTiepNhan, NgayDat, TrangThaiPhieu)
    VALUES (NULL, v_khach_1, v_nhan_vien_1, '2026-10-01', 'Đã hoàn tất');
    SET v_phieu_1 = LAST_INSERT_ID();
    INSERT INTO PhieuDatPhong (MaPhieu, MaKhachHang, MaNhanVienTiepNhan, NgayDat, TrangThaiPhieu)
    VALUES (NULL, v_khach_2, v_nhan_vien_2, '2026-10-03', 'Đã hoàn tất');
    SET v_phieu_2 = LAST_INSERT_ID();
    INSERT INTO PhieuDatPhong (MaPhieu, MaKhachHang, MaNhanVienTiepNhan, NgayDat, TrangThaiPhieu)
    VALUES (NULL, v_khach_3, v_nhan_vien_3, '2026-10-05', 'Đã hoàn tất');
    SET v_phieu_3 = LAST_INSERT_ID();
    INSERT INTO PhieuDatPhong (MaPhieu, MaKhachHang, MaNhanVienTiepNhan, NgayDat, TrangThaiPhieu)
    VALUES (NULL, v_khach_4, v_nhan_vien_4, '2026-10-07', 'Đã hoàn tất');
    SET v_phieu_4 = LAST_INSERT_ID();
    INSERT INTO PhieuDatPhong (MaPhieu, MaKhachHang, MaNhanVienTiepNhan, NgayDat, TrangThaiPhieu)
    VALUES (NULL, v_khach_5, v_nhan_vien_5, '2026-10-09', 'Đã hoàn tất');
    SET v_phieu_5 = LAST_INSERT_ID();
    INSERT INTO PhieuDatPhong (MaPhieu, MaKhachHang, MaNhanVienTiepNhan, NgayDat, TrangThaiPhieu)
    VALUES (NULL, v_khach_6, v_nhan_vien_6, '2026-10-11', 'Đã hoàn tất');
    SET v_phieu_6 = LAST_INSERT_ID();
    INSERT INTO PhieuDatPhong (MaPhieu, MaKhachHang, MaNhanVienTiepNhan, NgayDat, TrangThaiPhieu)
    VALUES (NULL, v_khach_7, v_nhan_vien_7, '2026-10-13', 'Đã hoàn tất');
    SET v_phieu_7 = LAST_INSERT_ID();
    INSERT INTO PhieuDatPhong (MaPhieu, MaKhachHang, MaNhanVienTiepNhan, NgayDat, TrangThaiPhieu)
    VALUES (NULL, v_khach_8, v_nhan_vien_8, '2026-10-15', 'Đã hoàn tất');
    SET v_phieu_8 = LAST_INSERT_ID();

    -- ChiTietDatPhong: ghi ro cot va lien ket bang ma vua tao.
    INSERT INTO ChiTietDatPhong (MaPhieu, MaPhong, NgayNhanDuKien, NgayTraDuKien, ThoiDiemNhanThucTe, ThoiDiemTraThucTe, DonGiaPhongApDung)
    VALUES (v_phieu_1, '101', '2026-10-02', '2026-10-04', '2026-10-02 14:00:00', '2026-10-04 11:00:00', 400000);
    SET v_chi_tiet_1 = LAST_INSERT_ID();
    INSERT INTO ChiTietDatPhong (MaPhieu, MaPhong, NgayNhanDuKien, NgayTraDuKien, ThoiDiemNhanThucTe, ThoiDiemTraThucTe, DonGiaPhongApDung)
    VALUES (v_phieu_2, '102', '2026-10-04', '2026-10-06', '2026-10-04 14:00:00', '2026-10-06 11:00:00', 500000);
    SET v_chi_tiet_2 = LAST_INSERT_ID();
    INSERT INTO ChiTietDatPhong (MaPhieu, MaPhong, NgayNhanDuKien, NgayTraDuKien, ThoiDiemNhanThucTe, ThoiDiemTraThucTe, DonGiaPhongApDung)
    VALUES (v_phieu_3, '103', '2026-10-06', '2026-10-08', '2026-10-06 14:00:00', '2026-10-08 11:00:00', 600000);
    SET v_chi_tiet_3 = LAST_INSERT_ID();
    INSERT INTO ChiTietDatPhong (MaPhieu, MaPhong, NgayNhanDuKien, NgayTraDuKien, ThoiDiemNhanThucTe, ThoiDiemTraThucTe, DonGiaPhongApDung)
    VALUES (v_phieu_4, '104', '2026-10-08', '2026-10-10', '2026-10-08 14:00:00', '2026-10-10 11:00:00', 700000);
    SET v_chi_tiet_4 = LAST_INSERT_ID();
    INSERT INTO ChiTietDatPhong (MaPhieu, MaPhong, NgayNhanDuKien, NgayTraDuKien, ThoiDiemNhanThucTe, ThoiDiemTraThucTe, DonGiaPhongApDung)
    VALUES (v_phieu_5, '105', '2026-10-10', '2026-10-12', '2026-10-10 14:00:00', '2026-10-12 11:00:00', 900000);
    SET v_chi_tiet_5 = LAST_INSERT_ID();
    INSERT INTO ChiTietDatPhong (MaPhieu, MaPhong, NgayNhanDuKien, NgayTraDuKien, ThoiDiemNhanThucTe, ThoiDiemTraThucTe, DonGiaPhongApDung)
    VALUES (v_phieu_6, '106', '2026-10-12', '2026-10-14', '2026-10-12 14:00:00', '2026-10-14 11:00:00', 1000000);
    SET v_chi_tiet_6 = LAST_INSERT_ID();
    INSERT INTO ChiTietDatPhong (MaPhieu, MaPhong, NgayNhanDuKien, NgayTraDuKien, ThoiDiemNhanThucTe, ThoiDiemTraThucTe, DonGiaPhongApDung)
    VALUES (v_phieu_7, '107', '2026-10-14', '2026-10-16', '2026-10-14 14:00:00', '2026-10-16 11:00:00', 1500000);
    SET v_chi_tiet_7 = LAST_INSERT_ID();
    INSERT INTO ChiTietDatPhong (MaPhieu, MaPhong, NgayNhanDuKien, NgayTraDuKien, ThoiDiemNhanThucTe, ThoiDiemTraThucTe, DonGiaPhongApDung)
    VALUES (v_phieu_8, '108', '2026-10-16', '2026-10-18', '2026-10-16 14:00:00', '2026-10-18 11:00:00', 1800000);
    SET v_chi_tiet_8 = LAST_INSERT_ID();

    -- LanSuDungDichVu: ghi ro cot va lien ket bang ma vua tao.
    INSERT INTO LanSuDungDichVu (MaChiTietDatPhong, MaDichVu, ThoiDiemSuDung, SoLuong, DonGiaApDung)
    VALUES (v_chi_tiet_1, v_dich_vu_1, '2026-10-02 18:00:00', 2, 10000);
    INSERT INTO LanSuDungDichVu (MaChiTietDatPhong, MaDichVu, ThoiDiemSuDung, SoLuong, DonGiaApDung)
    VALUES (v_chi_tiet_2, v_dich_vu_2, '2026-10-04 18:00:00', 2, 10000);
    INSERT INTO LanSuDungDichVu (MaChiTietDatPhong, MaDichVu, ThoiDiemSuDung, SoLuong, DonGiaApDung)
    VALUES (v_chi_tiet_3, v_dich_vu_3, '2026-10-06 18:00:00', 1, 10000);
    INSERT INTO LanSuDungDichVu (MaChiTietDatPhong, MaDichVu, ThoiDiemSuDung, SoLuong, DonGiaApDung)
    VALUES (v_chi_tiet_4, v_dich_vu_4, '2026-10-08 18:00:00', 3, 10000);
    INSERT INTO LanSuDungDichVu (MaChiTietDatPhong, MaDichVu, ThoiDiemSuDung, SoLuong, DonGiaApDung)
    VALUES (v_chi_tiet_5, v_dich_vu_5, '2026-10-10 18:00:00', 2, 15000);
    INSERT INTO LanSuDungDichVu (MaChiTietDatPhong, MaDichVu, ThoiDiemSuDung, SoLuong, DonGiaApDung)
    VALUES (v_chi_tiet_6, v_dich_vu_6, '2026-10-12 18:00:00', 2, 15000);
    INSERT INTO LanSuDungDichVu (MaChiTietDatPhong, MaDichVu, ThoiDiemSuDung, SoLuong, DonGiaApDung)
    VALUES (v_chi_tiet_7, v_dich_vu_7, '2026-10-14 18:00:00', 1, 100000);
    INSERT INTO LanSuDungDichVu (MaChiTietDatPhong, MaDichVu, ThoiDiemSuDung, SoLuong, DonGiaApDung)
    VALUES (v_chi_tiet_8, v_dich_vu_8, '2026-10-16 18:00:00', 1, 1000000);

    -- DangKyLuuTru: ghi ro cot va lien ket bang ma vua tao.
    INSERT INTO DangKyLuuTru (MaKhachHang, MaChiTietDatPhong, ThoiDiemVao, ThoiDiemRa)
    VALUES (v_khach_1, v_chi_tiet_1, '2026-10-02 14:00:00', '2026-10-04 11:00:00');
    INSERT INTO DangKyLuuTru (MaKhachHang, MaChiTietDatPhong, ThoiDiemVao, ThoiDiemRa)
    VALUES (v_khach_2, v_chi_tiet_2, '2026-10-04 14:00:00', '2026-10-06 11:00:00');
    INSERT INTO DangKyLuuTru (MaKhachHang, MaChiTietDatPhong, ThoiDiemVao, ThoiDiemRa)
    VALUES (v_khach_3, v_chi_tiet_3, '2026-10-06 14:00:00', '2026-10-08 11:00:00');
    INSERT INTO DangKyLuuTru (MaKhachHang, MaChiTietDatPhong, ThoiDiemVao, ThoiDiemRa)
    VALUES (v_khach_4, v_chi_tiet_4, '2026-10-08 14:00:00', '2026-10-10 11:00:00');
    INSERT INTO DangKyLuuTru (MaKhachHang, MaChiTietDatPhong, ThoiDiemVao, ThoiDiemRa)
    VALUES (v_khach_5, v_chi_tiet_5, '2026-10-10 14:00:00', '2026-10-12 11:00:00');
    INSERT INTO DangKyLuuTru (MaKhachHang, MaChiTietDatPhong, ThoiDiemVao, ThoiDiemRa)
    VALUES (v_khach_6, v_chi_tiet_6, '2026-10-12 14:00:00', '2026-10-14 11:00:00');
    INSERT INTO DangKyLuuTru (MaKhachHang, MaChiTietDatPhong, ThoiDiemVao, ThoiDiemRa)
    VALUES (v_khach_7, v_chi_tiet_7, '2026-10-14 14:00:00', '2026-10-16 11:00:00');
    INSERT INTO DangKyLuuTru (MaKhachHang, MaChiTietDatPhong, ThoiDiemVao, ThoiDiemRa)
    VALUES (v_khach_8, v_chi_tiet_8, '2026-10-16 14:00:00', '2026-10-18 11:00:00');

    -- HoaDon: ghi ro cot va lien ket bang ma vua tao.
    INSERT INTO HoaDon (MaPhieu, MaNhanVienLap, NgayLap, TrangThaiThanhToan, TongTien)
    VALUES (v_phieu_1, v_nhan_vien_1, '2026-10-04', 'Đã thanh toán', 820000);
    INSERT INTO HoaDon (MaPhieu, MaNhanVienLap, NgayLap, TrangThaiThanhToan, TongTien)
    VALUES (v_phieu_2, v_nhan_vien_2, '2026-10-06', 'Đã thanh toán', 1020000);
    INSERT INTO HoaDon (MaPhieu, MaNhanVienLap, NgayLap, TrangThaiThanhToan, TongTien)
    VALUES (v_phieu_3, v_nhan_vien_3, '2026-10-08', 'Đã thanh toán', 1210000);
    INSERT INTO HoaDon (MaPhieu, MaNhanVienLap, NgayLap, TrangThaiThanhToan, TongTien)
    VALUES (v_phieu_4, v_nhan_vien_4, '2026-10-10', 'Đã thanh toán', 1430000);
    INSERT INTO HoaDon (MaPhieu, MaNhanVienLap, NgayLap, TrangThaiThanhToan, TongTien)
    VALUES (v_phieu_5, v_nhan_vien_5, '2026-10-12', 'Đã thanh toán', 1830000);
    INSERT INTO HoaDon (MaPhieu, MaNhanVienLap, NgayLap, TrangThaiThanhToan, TongTien)
    VALUES (v_phieu_6, v_nhan_vien_6, '2026-10-14', 'Đã thanh toán', 2030000);
    INSERT INTO HoaDon (MaPhieu, MaNhanVienLap, NgayLap, TrangThaiThanhToan, TongTien)
    VALUES (v_phieu_7, v_nhan_vien_7, '2026-10-16', 'Đã thanh toán', 3100000);
    INSERT INTO HoaDon (MaPhieu, MaNhanVienLap, NgayLap, TrangThaiThanhToan, TongTien)
    VALUES (v_phieu_8, v_nhan_vien_8, '2026-10-18', 'Đã thanh toán', 4600000);

    -- ThanhToan: ghi ro cot va lien ket bang ma vua tao.
    INSERT INTO ThanhToan (MaPhieu, ThoiDiemGiaoDich, LoaiGiaoDich, SoTien)
    VALUES (v_phieu_1, '2026-10-04 11:10:00', 'Thanh toán', 820000);
    INSERT INTO ThanhToan (MaPhieu, ThoiDiemGiaoDich, LoaiGiaoDich, SoTien)
    VALUES (v_phieu_2, '2026-10-06 11:10:00', 'Thanh toán', 1020000);
    INSERT INTO ThanhToan (MaPhieu, ThoiDiemGiaoDich, LoaiGiaoDich, SoTien)
    VALUES (v_phieu_3, '2026-10-08 11:10:00', 'Thanh toán', 1210000);
    INSERT INTO ThanhToan (MaPhieu, ThoiDiemGiaoDich, LoaiGiaoDich, SoTien)
    VALUES (v_phieu_4, '2026-10-10 11:10:00', 'Thanh toán', 1430000);
    INSERT INTO ThanhToan (MaPhieu, ThoiDiemGiaoDich, LoaiGiaoDich, SoTien)
    VALUES (v_phieu_5, '2026-10-12 11:10:00', 'Thanh toán', 1830000);
    INSERT INTO ThanhToan (MaPhieu, ThoiDiemGiaoDich, LoaiGiaoDich, SoTien)
    VALUES (v_phieu_6, '2026-10-14 11:10:00', 'Thanh toán', 2030000);
    INSERT INTO ThanhToan (MaPhieu, ThoiDiemGiaoDich, LoaiGiaoDich, SoTien)
    VALUES (v_phieu_7, '2026-10-16 11:10:00', 'Thanh toán', 3100000);
    INSERT INTO ThanhToan (MaPhieu, ThoiDiemGiaoDich, LoaiGiaoDich, SoTien)
    VALUES (v_phieu_8, '2026-10-18 11:10:00', 'Thanh toán', 4600000);
    END IF;

    -- BO SUNG NGHIEP VU: 3 phieu, 6 chi tiet, 4 giao dich; giu nguyen du lieu cu.
    -- Chan ca nap lai va bo du lieu da duoc nap mot phan; khong sua phieu hien co.
    IF EXISTS (SELECT 1 FROM PhieuDatPhong
               WHERE (MaKhachHang = v_khach_9 AND NgayDat = '2026-10-20')
                  OR (MaKhachHang = v_khach_10 AND NgayDat = '2026-10-25')
                  OR (MaKhachHang = v_khach_1 AND NgayDat = '2026-10-28')) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Da co phieu trung khach va ngay cua dot bo sung. Khong ghi them.';
    END IF;

    -- Khach I dat 3 phong cho ngay 20-22/11: tinh 3 luot trong THANG 10 theo NgayDat.
    INSERT INTO PhieuDatPhong (MaPhieu, MaKhachHang, MaNhanVienTiepNhan, NgayDat, TrangThaiPhieu)
    VALUES (NULL, v_khach_9, v_nhan_vien_1, '2026-10-20', 'Đã xác nhận');
    SET v_phieu_nhieu_phong = LAST_INSERT_ID();
    INSERT INTO ChiTietDatPhong
        (MaPhieu, MaPhong, NgayNhanDuKien, NgayTraDuKien, ThoiDiemNhanThucTe, ThoiDiemTraThucTe, DonGiaPhongApDung)
    VALUES
        (v_phieu_nhieu_phong, '101', '2026-11-20', '2026-11-22', NULL, NULL, 400000),
        (v_phieu_nhieu_phong, '102', '2026-11-20', '2026-11-22', NULL, NULL, 500000),
        (v_phieu_nhieu_phong, '103', '2026-11-20', '2026-11-22', NULL, NULL, 600000);
    INSERT INTO ThanhToan (MaPhieu, ThoiDiemGiaoDich, LoaiGiaoDich, SoTien)
    VALUES (v_phieu_nhieu_phong, '2026-10-20 09:00:00', 'Đặt cọc', 500000);

    -- Khach K huy ca 2 phong truoc khi nhan: 2 chi tiet bi loai, tien coc hoan du.
    INSERT INTO PhieuDatPhong (MaPhieu, MaKhachHang, MaNhanVienTiepNhan, NgayDat, TrangThaiPhieu)
    VALUES (NULL, v_khach_10, v_nhan_vien_1, '2026-10-25', 'Đã hủy');
    SET v_phieu_huy = LAST_INSERT_ID();
    INSERT INTO ChiTietDatPhong
        (MaPhieu, MaPhong, NgayNhanDuKien, NgayTraDuKien, ThoiDiemNhanThucTe, ThoiDiemTraThucTe, DonGiaPhongApDung)
    VALUES
        (v_phieu_huy, '101', '2026-11-25', '2026-11-27', NULL, NULL, 400000),
        (v_phieu_huy, '107', '2026-11-25', '2026-11-27', NULL, NULL, 1500000);
    INSERT INTO ThanhToan (MaPhieu, ThoiDiemGiaoDich, LoaiGiaoDich, SoTien)
    VALUES (v_phieu_huy, '2026-10-25 10:00:00', 'Đặt cọc', 300000),
           (v_phieu_huy, '2026-10-26 10:00:00', 'Hoàn cọc', 300000);

    -- Khach A dat lai phong 101 sau ngay tra cua phieu nhieu phong: khong trung lich.
    INSERT INTO PhieuDatPhong (MaPhieu, MaKhachHang, MaNhanVienTiepNhan, NgayDat, TrangThaiPhieu)
    VALUES (NULL, v_khach_1, v_nhan_vien_1, '2026-10-28', 'Đã xác nhận');
    SET v_phieu_dat_them = LAST_INSERT_ID();
    INSERT INTO ChiTietDatPhong
        (MaPhieu, MaPhong, NgayNhanDuKien, NgayTraDuKien, ThoiDiemNhanThucTe, ThoiDiemTraThucTe, DonGiaPhongApDung)
    VALUES (v_phieu_dat_them, '101', '2026-11-22', '2026-11-24', NULL, NULL, 400000);
    INSERT INTO ThanhToan (MaPhieu, ThoiDiemGiaoDich, LoaiGiaoDich, SoTien)
    VALUES (v_phieu_dat_them, '2026-10-28 14:00:00', 'Đặt cọc', 200000);
    -- Chua nhan phong/da huy: khong tao luu tru, su dung dich vu hay hoa don gia.
    COMMIT;
END$$
DELIMITER ;

CALL sp_nhap_lieu_khach_san_btl(@chi_bo_sung);
DROP PROCEDURE IF EXISTS sp_nhap_lieu_khach_san_btl;

-- Sau khi nap vao database moi: bao cao 01/10/2026-31/10/2026 co
-- 10 phieu hop le, 12 luot hop le, 2 luot bi loai do huy (14 chi tiet tong cong).
-- Standard Single: 3; Standard Double: 2; Superior Single: 2; 5 loai con lai: 1.
-- Website va file bao cao doc du lieu hien tai trong hotel, khong hardcode so lieu.
SELECT MaKhachHang, HoTen, CCCD, SoDienThoai FROM KhachHang ORDER BY MaKhachHang;
