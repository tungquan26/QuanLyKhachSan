create database hotel;
use hotel;
set names utf8mb4;

create table khachhang (
    makhachhang int primary key auto_increment,
    hoten varchar(100) not null,
    cccd varchar(12) not null unique,
    sodienthoai varchar(20)
);

create table nhanvien (
    manhanvien int primary key auto_increment,
    hoten varchar(100) not null,
    sodienthoai varchar(20),
    chucvu varchar(50) not null
);

create table loaiphong (
    maloaiphong int primary key auto_increment,
    tenloaiphong varchar(80) not null unique,
    gianiemyetmoidem decimal(14,0) not null check (gianiemyetmoidem >= 0)
);

create table phong (
    maphong varchar(12) primary key,
    maloaiphong int not null,
    tinhtrangvanhanh varchar(40) not null,
    foreign key (maloaiphong) references loaiphong(maloaiphong)
);

create table dichvu (
    madichvu int primary key auto_increment,
    tendichvu varchar(100) not null unique,
    donvitinh varchar(30) not null,
    dongiahienhanh decimal(14,0) not null check (dongiahienhanh >= 0),
    trangthai varchar(40) not null
);

create table phieudatphong (
    maphieu int primary key auto_increment,
    makhachhang int not null,
    manhanvientiepnhan int not null,
    ngaydat date not null,
    trangthaiphieu varchar(40) not null,
    foreign key (makhachhang) references khachhang(makhachhang),
    foreign key (manhanvientiepnhan) references nhanvien(manhanvien)
);

create table chitietdatphong (
    machitietdatphong int primary key auto_increment,
    maphieu int not null,
    maphong varchar(12) not null,
    ngaynhandukien date not null,
    ngaytradukien date not null,
    thoidiemnhanthucte datetime,
    thoidiemtrathucte datetime,
    dongiaphongapdung decimal(14,0) not null check (dongiaphongapdung >= 0),
    check (ngaytradukien > ngaynhandukien),
    check (thoidiemtrathucte is null or
          (thoidiemnhanthucte is not null and thoidiemtrathucte >= thoidiemnhanthucte)),
    foreign key (maphieu) references phieudatphong(maphieu),
    foreign key (maphong) references phong(maphong)
);

create table lansudungdichvu (
    malansudung int primary key auto_increment,
    machitietdatphong int not null,
    madichvu int not null,
    thoidiemsudung datetime not null,
    soluong decimal(9,2) not null check (soluong > 0),
    dongiaapdung decimal(14,0) not null check (dongiaapdung >= 0),
    foreign key (machitietdatphong) references chitietdatphong(machitietdatphong),
    foreign key (madichvu) references dichvu(madichvu)
);

create table dangkyluutru (
    madangky int primary key auto_increment,
    makhachhang int not null,
    machitietdatphong int not null,
    thoidiemvao datetime not null,
    thoidiemra datetime,
    check (thoidiemra is null or thoidiemra >= thoidiemvao),
    foreign key (makhachhang) references khachhang(makhachhang),
    foreign key (machitietdatphong)
        references chitietdatphong(machitietdatphong)
);

create table hoadon (
    mahoadon int primary key auto_increment,
    maphieu int not null unique,
    manhanvienlap int not null,
    ngaylap date not null,
    trangthaithanhtoan varchar(40) not null,
    tongtien decimal(14,0) not null check (tongtien >= 0),
    foreign key (maphieu) references phieudatphong(maphieu),
    foreign key (manhanvienlap) references nhanvien(manhanvien)
);

create table thanhtoan (
	mathanhtoan int primary key auto_increment,
    maphieu int not null,
    thoidiemgiaodich datetime not null,
    loaigiaodich varchar(20) not null,
    sotien decimal(14,0) not null check (sotien >= 0),
    foreign key (maphieu) references phieudatphong(maphieu)
);
