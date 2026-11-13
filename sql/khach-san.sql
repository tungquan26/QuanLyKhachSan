use hotel;
set names utf8mb4;

-- 1. Danh mục
create table KhachHang (
    MaKhachHang int primary key auto_increment,
    HoTen varchar(100) not null,
    CCCD varchar(12) not null unique,
    SoDienThoai varchar(20)
);

create table NhanVien (
    MaNhanVien int primary key auto_increment,
    HoTen varchar(100) not null,
    SoDienThoai varchar(20),
    ChucVu varchar(50) not null
);

create table LoaiPhong (
    MaLoaiPhong int primary key auto_increment,
    TenLoaiPhong varchar(80) not null,
    GiaNiemYetMoiDem decimal(14,0) not null check (GiaNiemYetMoiDem >= 0)
);

create table Phong (
    MaPhong varchar(12) primary key,
    MaLoaiPhong int not null,
    TinhTrangVanHanh varchar(40) not null,
    foreign key (MaLoaiPhong) references LoaiPhong(MaLoaiPhong)
);

create table DichVu (
    MaDichVu int primary key auto_increment,
    TenDichVu varchar(100) not null,
    DonViTinh varchar(30) not null,
    DonGiaHienHanh decimal(14,0) not null check (DonGiaHienHanh >= 0),
    TrangThai varchar(40) not null
);

-- 2. Giao dịch
create table PhieuDatPhong (
    MaPhieu int primary key auto_increment,
    MaKhachHang int not null,
    MaNhanVienTiepNhan int not null,
    NgayDat date not null,
    TrangThaiPhieu varchar(40) not null,
    foreign key (MaKhachHang) references KhachHang(MaKhachHang),
    foreign key (MaNhanVienTiepNhan) references NhanVien(MaNhanVien)
);

create table ChiTietDatPhong (
    MaChiTietDatPhong int primary key auto_increment,
    MaPhieu int not null,
    MaPhong varchar(12) not null,
    NgayNhanDuKien date not null,
    NgayTraDuKien date not null,
    ThoiDiemNhanThucTe datetime,
    ThoiDiemTraThucTe datetime,
    DonGiaPhongApDung decimal(14,0) not null check (DonGiaPhongApDung >= 0),
    check (NgayTraDuKien > NgayNhanDuKien),
    check (ThoiDiemTraThucTe is null or
          (ThoiDiemNhanThucTe is not null and ThoiDiemTraThucTe >= ThoiDiemNhanThucTe)),
    foreign key (MaPhieu) references PhieuDatPhong(MaPhieu),
    foreign key (MaPhong) references Phong(MaPhong)
);

create table LanSuDungDichVu (
    MaLanSuDung int primary key auto_increment,
    MaChiTietDatPhong int not null,
    MaDichVu int not null,
    ThoiDiemSuDung datetime not null,
    SoLuong decimal(9,2) not null check (SoLuong > 0),
    DonGiaApDung decimal(14,0) not null check (DonGiaApDung >= 0),
    foreign key (MaChiTietDatPhong) references ChiTietDatPhong(MaChiTietDatPhong),
    foreign key (MaDichVu) references DichVu(MaDichVu)
);

-- 3. Quy tắc chốt giá phòng
-- Chốt giá niêm yết của loại phòng khi thêm chi tiết đặt phòng.
-- Giá đã chốt không đổi khi bảng giá của LoaiPhong thay đổi.
-- drop trigger if exists ChiTietDatPhong_ChotGia;
-- drop trigger if exists ChiTietDatPhong_KhoaGia;
-- delimiter //
-- create trigger ChiTietDatPhong_ChotGia
-- before insert on ChiTietDatPhong
-- for each row
-- begin
--     set new.DonGiaPhongApDung = (
--         select lp.GiaNiemYetMoiDem
--         from Phong as p
--         join LoaiPhong as lp on lp.MaLoaiPhong = p.MaLoaiPhong
--         where p.MaPhong = new.MaPhong
--     );
-- end //

-- create trigger ChiTietDatPhong_KhoaGia
-- before update on ChiTietDatPhong
-- for each row
-- begin
--     if new.DonGiaPhongApDung <> old.DonGiaPhongApDung then
--         signal sqlstate '45000'
--             set message_text = 'DonGiaPhongApDung da duoc chot khi dat phong';
--     end if;
-- end //
-- delimiter ;
