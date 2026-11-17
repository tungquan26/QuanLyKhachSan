use hotel;
set names utf8mb4;

select madichvu, tendichvu, donvitinh, dongiahienhanh, trangthai from dichvu order by madichvu asc;

-- set @ten_dich_vu = 'Nước uống';
-- set @don_vi_tinh = 'chai';
-- set @don_gia = 20000;
-- set @trang_thai = 'Đang cung cấp';

insert into dichvu (tendichvu, donvitinh, dongiahienhanh, trangthai) values (@ten_dich_vu, @don_vi_tinh, @don_gia, @trang_thai);

