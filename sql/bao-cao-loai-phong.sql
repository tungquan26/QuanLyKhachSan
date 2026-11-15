-- BAO CAO LUOT DAT THEO LOAI PHONG + DOI CHIEU DU LIEU (MySQL 8.0+).
-- Dung schema sql/khach-san.sql, co bang LoaiPhong rieng.
-- Chi doc du lieu; khong chen/sua/xoa ban ghi hay tao bang.
-- Chay toan bo file trong Workbench, xem cac tab Result Grid.
-- Du lieu duoc nap tu nhap-lieu-khach-san.sql hoac nhap nghiep vu vao hotel.
-- Doc TOAN BO du lieu phu hop ky bao cao, khong loc theo bo du lieu rieng.
-- Can SELECT tren LoaiPhong, Phong, PhieuDatPhong, ChiTietDatPhong.

USE hotel;
SET NAMES utf8mb4;

-- A. THAM SO: doi hai ngay nay de xem ky khac (tu_ngay <= den_ngay).
SET @bc_tu_ngay = DATE('2026-10-01');
SET @bc_den_ngay = DATE('2026-10-31');
SET @bc_ten_don_vi = 'Khách sạn Hotel Desk';
SET @bc_nguoi_lap = 'Trưởng bộ phận Lễ tân';
SET @bc_nguoi_nhan = 'Ban Giám đốc khách sạn';

-- B. THONG TIN SU DUNG BAO CAO: ai lap, gui ai, dung de lam gi.
SELECT @bc_ten_don_vi AS DonVi,
       'Báo cáo thống kê lượt đặt phòng theo loại phòng' AS TenBaoCao,
       @bc_tu_ngay AS TuNgay, @bc_den_ngay AS DenNgay,
       @bc_nguoi_lap AS NguoiLap, @bc_nguoi_nhan AS NguoiNhan,
       'Toàn bộ lượt đặt trong kỳ, không bao gồm phiếu đã hủy' AS PhamVi,
       'Theo dõi nhu cầu từng loại phòng, phục vụ khuyến mãi và kế hoạch kinh doanh.' AS MucDich,
       'Theo ngày đặt; mỗi chi tiết là một lượt; không bao gồm phiếu đã hủy.' AS CachTinh,
       CASE WHEN @bc_tu_ngay IS NULL OR @bc_den_ngay IS NULL OR @bc_tu_ngay > @bc_den_ngay
                 THEN 'Kỳ không hợp lệ: sửa hai ngày rồi chạy lại toàn bộ file.'
            ELSE 'Sẵn sàng' END AS KiemTraThamSo;

-- C. BANG BAO CAO.
-- LuotHopLe: loc ngay dat va trang thai TRUOC khi dem.
-- LEFT JOIN: giu loai phong chua duoc dat; COALESCE chuyen NULL thanh 0.
-- Nhom theo MA loai, tranh gop nham hai loai khac ma nhung trung ten.
WITH LuotHopLe AS (
    SELECT p.MaLoaiPhong, ct.MaChiTietDatPhong
    FROM ChiTietDatPhong ct
    JOIN PhieuDatPhong pd ON pd.MaPhieu = ct.MaPhieu
    JOIN Phong p ON p.MaPhong = ct.MaPhong
    WHERE pd.NgayDat BETWEEN @bc_tu_ngay AND @bc_den_ngay
      AND LOWER(TRIM(pd.TrangThaiPhieu)) NOT IN
          ('đã hủy', 'đã huỷ', 'hủy', 'huỷ', 'da huy', 'huy')
), SoLuotTheoLoai AS (
    SELECT MaLoaiPhong, COUNT(MaChiTietDatPhong) AS SoLuotDat
    FROM LuotHopLe
    GROUP BY MaLoaiPhong
), ChiTietBaoCao AS (
    SELECT lp.MaLoaiPhong, lp.TenLoaiPhong,
           COALESCE(sl.SoLuotDat, 0) AS SoLuotDat
    FROM LoaiPhong lp
    LEFT JOIN SoLuotTheoLoai sl ON sl.MaLoaiPhong = lp.MaLoaiPhong
    WHERE @bc_tu_ngay <= @bc_den_ngay
), Tong AS (
    SELECT COALESCE(SUM(SoLuotDat), 0) AS TongLuot FROM ChiTietBaoCao
), KetQua AS (
    SELECT 0 AS DongTong,
           ROW_NUMBER() OVER (ORDER BY ct.SoLuotDat DESC, ct.MaLoaiPhong) AS STT,
           ct.MaLoaiPhong, ct.TenLoaiPhong, ct.SoLuotDat,
           COALESCE(ROUND(ct.SoLuotDat * 100.0 / NULLIF(t.TongLuot, 0), 2), 0) AS TyLePhanTram
    FROM ChiTietBaoCao ct CROSS JOIN Tong t
    UNION ALL
    SELECT 1, NULL, NULL, 'TỔNG CỘNG', TongLuot,
           CASE WHEN TongLuot = 0 THEN 0.00 ELSE 100.00 END
    FROM Tong
)
SELECT STT, TenLoaiPhong AS LoaiPhong, SoLuotDat, TyLePhanTram AS `TyLe (%)`
FROM KetQua
ORDER BY DongTong, SoLuotDat DESC, MaLoaiPhong;

-- D. DOI CHIEU: moi dong chi tiet trong ky, ke ca dong bi loai do huy.
-- Nhieu dong cung MaPhieu la binh thuong: mot phieu dat nhieu phong.
SELECT ct.MaChiTietDatPhong, pd.MaPhieu, pd.NgayDat, pd.TrangThaiPhieu,
       ct.MaPhong, lp.TenLoaiPhong,
       CASE WHEN LOWER(TRIM(pd.TrangThaiPhieu)) IN
                     ('đã hủy', 'đã huỷ', 'hủy', 'huỷ', 'da huy', 'huy')
            THEN 'Không tính: phiếu đã hủy' ELSE 'Được tính' END AS XuLyBaoCao
FROM ChiTietDatPhong ct
JOIN PhieuDatPhong pd ON pd.MaPhieu = ct.MaPhieu
JOIN Phong p ON p.MaPhong = ct.MaPhong
JOIN LoaiPhong lp ON lp.MaLoaiPhong = p.MaLoaiPhong
WHERE pd.NgayDat BETWEEN @bc_tu_ngay AND @bc_den_ngay
ORDER BY pd.NgayDat, pd.MaPhieu, ct.MaChiTietDatPhong;

-- E. DOI CHIEU DOC LAP: so phieu khac so luot dat phong.
-- Du lieu sau bo sung thang 10/2026: 10 phieu hop le, 12 luot, 2 luot bi huy.
WITH ChiTietTrongKy AS (
    SELECT pd.MaPhieu, ct.MaChiTietDatPhong,
           CASE WHEN LOWER(TRIM(pd.TrangThaiPhieu)) IN
                         ('đã hủy', 'đã huỷ', 'hủy', 'huỷ', 'da huy', 'huy')
                THEN 1 ELSE 0 END AS DaHuy
    FROM ChiTietDatPhong ct
    JOIN PhieuDatPhong pd ON pd.MaPhieu = ct.MaPhieu
    JOIN Phong p ON p.MaPhong = ct.MaPhong
    JOIN LoaiPhong lp ON lp.MaLoaiPhong = p.MaLoaiPhong
    WHERE pd.NgayDat BETWEEN @bc_tu_ngay AND @bc_den_ngay
)
SELECT COUNT(DISTINCT CASE WHEN DaHuy = 0 THEN MaPhieu END) AS SoPhieuHopLe,
       COUNT(CASE WHEN DaHuy = 0 THEN MaChiTietDatPhong END) AS SoLuotHopLe,
       COUNT(CASE WHEN DaHuy = 1 THEN MaChiTietDatPhong END) AS SoLuotBiHuy,
       COUNT(*) AS TongChiTietTrongKy
FROM ChiTietTrongKy;

-- Chu y: ty le tung dong lam tron 2 chu so nen co the cong thanh 99.99/100.01.
-- Tong van la 100% khi co luot, 0% khi khong phat sinh. Khong chia cho 0.
-- TrangThaiPhieu dang la van ban tu do. Neu them cach ghi trang thai huy moi,
-- can bo sung dong nhat vao danh sach huy trong cac truy van tren.
