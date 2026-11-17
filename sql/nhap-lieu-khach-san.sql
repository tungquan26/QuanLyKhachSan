use hotel;
set names utf8mb4;

insert into khachhang values (null, 'Nguyễn Văn A', '012345000000', '0320000000');
insert into khachhang values (null, 'Nguyễn Văn B', '012345000001', '0320000001');
insert into khachhang values (null, 'Nguyễn Văn C', '012345000002', '0320000002');
insert into khachhang values (null, 'Nguyễn Văn D', '012345000003', '0320000003');
insert into khachhang values (null, 'Nguyễn Văn E', '012345000004', '0320000004');
insert into khachhang values (null, 'Nguyễn Văn F', '012345000005', '0320000005');
insert into khachhang values (null, 'Nguyễn Văn G', '012345000006', '0320000006');
insert into khachhang values (null, 'Nguyễn Văn H', '012345000007', '0320000007');
insert into khachhang values (null, 'Nguyễn Văn I', '012345000008', '0320000008');
insert into khachhang values (null, 'Nguyễn Văn K', '012345000009', '0320000009');

insert into nhanvien values (null, 'Trần Thị Lan', '0331000001', 'Lễ tân');
insert into nhanvien values (null, 'Lê Minh Tuấn', '0331000002', 'Lễ tân');
insert into nhanvien values (null, 'Phạm Ngọc Mai', '0331000003', 'Lễ tân');
insert into nhanvien values (null, 'Võ Quốc Huy', '0331000004', 'Quản lý');
insert into nhanvien values (null, 'Đặng Thị Hoa', '0331000005', 'Lễ tân');
insert into nhanvien values (null, 'Bùi Thanh Nam', '0331000006', 'Lễ tân');
insert into nhanvien values (null, 'Hoàng Mỹ Linh', '0331000007', 'Lễ tân');
insert into nhanvien values (null, 'Ngô Đức Anh', '0331000008', 'Lễ tân');

insert into loaiphong values (null, 'Phòng tiêu chuẩn đơn', 400000);
insert into loaiphong values (null, 'Phòng tiêu chuẩn đôi', 500000);
insert into loaiphong values (null, 'Phòng cao cấp đơn', 600000);
insert into loaiphong values (null, 'Phòng cao cấp đôi', 700000);
insert into loaiphong values (null, 'Phòng sang trọng giường đôi', 900000);
insert into loaiphong values (null, 'Phòng sang trọng hai giường đơn', 1000000);
insert into loaiphong values (null, 'Phòng thượng hạng', 1500000);
insert into loaiphong values (null, 'Phòng gia đình', 1800000);

insert into phong values ('101', 1, 'Hoạt động');
insert into phong values ('102', 2, 'Hoạt động');
insert into phong values ('103', 3, 'Hoạt động');
insert into phong values ('104', 4, 'Hoạt động');
insert into phong values ('105', 5, 'Hoạt động');
insert into phong values ('106', 6, 'Hoạt động');
insert into phong values ('107', 7, 'Hoạt động');
insert into phong values ('108', 8, 'Hoạt động');

insert into dichvu values (null, 'Nước lọc', 'chai', 10000, 'Đang cung cấp');
insert into dichvu values (null, 'Nước suối', 'chai', 10000, 'Đang cung cấp');
insert into dichvu values (null, 'Nước khoáng', 'chai', 10000, 'Đang cung cấp');
insert into dichvu values (null, 'Nước ngọt', 'chai', 10000, 'Đang cung cấp');
insert into dichvu values (null, 'Coca Cola', 'chai', 15000, 'Đang cung cấp');
insert into dichvu values (null, 'Pepsi', 'chai', 15000, 'Đang cung cấp');
insert into dichvu values (null, 'Rượu trắng', 'chai', 100000, 'Đang cung cấp');
insert into dichvu values (null, 'Rượu vang', 'chai', 1000000, 'Đang cung cấp');
insert into dichvu values (null, 'Snack', 'gói', 10000, 'Đang cung cấp');

insert into phieudatphong values (null, 1, 1, '2026-10-01', 'Đã hoàn tất');
insert into phieudatphong values (null, 2, 2, '2026-10-03', 'Đã hoàn tất');
insert into phieudatphong values (null, 3, 3, '2026-10-05', 'Đã hoàn tất');
insert into phieudatphong values (null, 4, 4, '2026-10-07', 'Đã hoàn tất');
insert into phieudatphong values (null, 5, 5, '2026-10-09', 'Đã hoàn tất');
insert into phieudatphong values (null, 6, 6, '2026-10-11', 'Đã hoàn tất');
insert into phieudatphong values (null, 7, 7, '2026-10-13', 'Đã hoàn tất');
insert into phieudatphong values (null, 8, 8, '2026-10-15', 'Đã hoàn tất');

insert into chitietdatphong values (null, 1, '101', '2026-10-02', '2026-10-04', '2026-10-02 14:00:00', '2026-10-04 11:00:00', 400000);
insert into chitietdatphong values (null, 2, '102', '2026-10-04', '2026-10-06', '2026-10-04 14:00:00', '2026-10-06 11:00:00', 500000);
insert into chitietdatphong values (null, 3, '103', '2026-10-06', '2026-10-08', '2026-10-06 14:00:00', '2026-10-08 11:00:00', 600000);
insert into chitietdatphong values (null, 4, '104', '2026-10-08', '2026-10-10', '2026-10-08 14:00:00', '2026-10-10 11:00:00', 700000);
insert into chitietdatphong values (null, 5, '105', '2026-10-10', '2026-10-12', '2026-10-10 14:00:00', '2026-10-12 11:00:00', 900000);
insert into chitietdatphong values (null, 6, '106', '2026-10-12', '2026-10-14', '2026-10-12 14:00:00', '2026-10-14 11:00:00', 1000000);
insert into chitietdatphong values (null, 7, '107', '2026-10-14', '2026-10-16', '2026-10-14 14:00:00', '2026-10-16 11:00:00', 1500000);
insert into chitietdatphong values (null, 8, '108', '2026-10-16', '2026-10-18', '2026-10-16 14:00:00', '2026-10-18 11:00:00', 1800000);

insert into lansudungdichvu values (null, 1, 1, '2026-10-02 18:00:00', 2, 10000);
insert into lansudungdichvu values (null, 2, 2, '2026-10-04 18:00:00', 2, 10000);
insert into lansudungdichvu values (null, 3, 3, '2026-10-06 18:00:00', 1, 10000);
insert into lansudungdichvu values (null, 4, 4, '2026-10-08 18:00:00', 3, 10000);
insert into lansudungdichvu values (null, 5, 5, '2026-10-10 18:00:00', 2, 15000);
insert into lansudungdichvu values (null, 6, 6, '2026-10-12 18:00:00', 2, 15000);
insert into lansudungdichvu values (null, 7, 7, '2026-10-14 18:00:00', 1, 100000);
insert into lansudungdichvu values (null, 8, 8, '2026-10-16 18:00:00', 1, 1000000);

insert into dangkyluutru values (null, 1, 1, '2026-10-02 14:00:00', '2026-10-04 11:00:00');
insert into dangkyluutru values (null, 2, 2, '2026-10-04 14:00:00', '2026-10-06 11:00:00');
insert into dangkyluutru values (null, 3, 3, '2026-10-06 14:00:00', '2026-10-08 11:00:00');
insert into dangkyluutru values (null, 4, 4, '2026-10-08 14:00:00', '2026-10-10 11:00:00');
insert into dangkyluutru values (null, 5, 5, '2026-10-10 14:00:00', '2026-10-12 11:00:00');
insert into dangkyluutru values (null, 6, 6, '2026-10-12 14:00:00', '2026-10-14 11:00:00');
insert into dangkyluutru values (null, 7, 7, '2026-10-14 14:00:00', '2026-10-16 11:00:00');
insert into dangkyluutru values (null, 8, 8, '2026-10-16 14:00:00', '2026-10-18 11:00:00');

insert into hoadon values (null, 1, 1, '2026-10-04', 'Đã thanh toán', 820000);
insert into hoadon values (null, 2, 2, '2026-10-06', 'Đã thanh toán', 1020000);
insert into hoadon values (null, 3, 3, '2026-10-08', 'Đã thanh toán', 1210000);
insert into hoadon values (null, 4, 4, '2026-10-10', 'Đã thanh toán', 1430000);
insert into hoadon values (null, 5, 5, '2026-10-12', 'Đã thanh toán', 1830000);
insert into hoadon values (null, 6, 6, '2026-10-14', 'Đã thanh toán', 2030000);
insert into hoadon values (null, 7, 7, '2026-10-16', 'Đã thanh toán', 3100000);
insert into hoadon values (null, 8, 8, '2026-10-18', 'Đã thanh toán', 4600000);

insert into thanhtoan values (null, 1, '2026-10-04 11:10:00', 'Thanh toán', 820000);
insert into thanhtoan values (null, 2, '2026-10-06 11:10:00', 'Thanh toán', 1020000);
insert into thanhtoan values (null, 3, '2026-10-08 11:10:00', 'Thanh toán', 1210000);
insert into thanhtoan values (null, 4, '2026-10-10 11:10:00', 'Thanh toán', 1430000);
insert into thanhtoan values (null, 5, '2026-10-12 11:10:00', 'Thanh toán', 1830000);
insert into thanhtoan values (null, 6, '2026-10-14 11:10:00', 'Thanh toán', 2030000);
insert into thanhtoan values (null, 7, '2026-10-16 11:10:00', 'Thanh toán', 3100000);
insert into thanhtoan values (null, 8, '2026-10-18 11:10:00', 'Thanh toán', 4600000);

