create database hotel;
use hotel;

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

create table DangKyLuuTru (
    MaDangKy int primary key auto_increment,
    MaKhachHang int not null,
    MaChiTietDatPhong int not null,
    ThoiDiemVao datetime not null,
    ThoiDiemRa datetime,
    check (ThoiDiemRa is null or ThoiDiemRa >= ThoiDiemVao),
    foreign key (MaKhachHang) references KhachHang(MaKhachHang),
    foreign key (MaChiTietDatPhong)
        references ChiTietDatPhong(MaChiTietDatPhong)
);

create table HoaDon (
    MaHoaDon int primary key auto_increment,
    MaPhieu int not null unique,
    MaNhanVienLap int not null,
    NgayLap date not null,
    TrangThaiThanhToan varchar(40) not null,
    TongTien decimal(14,0) not null check (TongTien >= 0),
    foreign key (MaPhieu) references PhieuDatPhong(MaPhieu),
    foreign key (MaNhanVienLap) references NhanVien(MaNhanVien)
);

create table ThanhToan (
	MaThanhToan int primary key auto_increment,
    MaPhieu int not null,
    ThoiDiemGiaoDich datetime not null,
    LoaiGiaoDich varchar(20) not null,
    SoTien decimal(14,0) not null check (SoTien >= 0),
    foreign key (MaPhieu) references PhieuDatPhong(MaPhieu)
);