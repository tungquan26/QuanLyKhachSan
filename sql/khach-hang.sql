use hotel;
set names utf8mb4;

select makhachhang, hoten, cccd, sodienthoai from khachhang order by makhachhang asc;

-- set @cccd = '%012345%';

select makhachhang, hoten, cccd, sodienthoai from khachhang where cccd like @cccd order by makhachhang asc;

-- set @ho_ten = 'Khách hàng mẫu';
-- set @cccd = '099999999999';
-- set @so_dien_thoai = '0901234567';

insert into khachhang (hoten, cccd, sodienthoai) values (@ho_ten, @cccd, @so_dien_thoai);

