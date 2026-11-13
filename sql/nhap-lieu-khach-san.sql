use hotel;
set names utf8mb4;

insert into KhachHang values(null, "Nguyễn Văn A", "012345000000", "0320000000");
insert into KhachHang values(null, "Nguyễn Văn B", "012345000001", "0320000001");
insert into KhachHang values(null, "Nguyễn Văn C", "012345000002", "0320000002");
insert into KhachHang values(null, "Nguyễn Văn D", "012345000003", "0320000003");
insert into KhachHang values(null, "Nguyễn Văn E", "012345000004", "0320000004");
insert into KhachHang values(null, "Nguyễn Văn F", "012345000005", "0320000005");
insert into KhachHang values(null, "Nguyễn Văn G", "012345000006", "0320000006");
insert into KhachHang values(null, "Nguyễn Văn H", "012345000007", "0320000007");
insert into KhachHang values(null, "Nguyễn Văn I", "012345000008", "0320000008");
insert into KhachHang values(null, "Nguyễn Văn K", "012345000009", "0320000009");

select MaKhachHang, Hoten, CCCD, SoDienThoai from KhachHang;
delete from KhachHang where MaKhachHang;
alter table KhachHang auto_increment = 1;

insert into DichVu values(null, "Nước lọc", "chai", 10000, "Đang cung cấp");
insert into DichVu values(null, "Nước suối", "chai", 10000, "Đang cung cấp");
insert into DichVu values(null, "Nước khoáng", "chai", 10000, "Đang cung cấp");
insert into DichVu values(null, "Nước ngọt", "chai", 10000, "Đang cung cấp");
insert into DichVu values(null, "Coca Cola", "chai", 15000, "Đang cung cấp");
insert into DichVu values(null, "Pepsi", "chai", 15000, "Đang cung cấp");
insert into DichVu values(null, "Rượu trắng", "chai", 100000, "Đang cung cấp");
insert into DichVu values(null, "Rượu vang", "chai", 1000000, "Đang cung cấp");
insert into DichVu values(null, "Snack", "goi", 10000, "Đang cung cấp");

select * from DichVu;
delete from DichVu where madichvu;
update dichvu set trangthai = "Đang cung cấp" where trangthai = "Dang cung cap"
limit 20;
alter table dichvu auto_increment = 1