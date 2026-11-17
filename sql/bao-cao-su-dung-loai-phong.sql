
use hotel;
set names utf8mb4;

set @tu_ngay = '2026-10-01 00:00:00';
set @den_ngay = '2026-10-31 23:59:59';
set @hien_tai = now();

select lp.maloaiphong, lp.tenloaiphong,
       count(*) as soluotsudung,
       count(distinct p.maphong) as sophongdadung
from chitietdatphong ct
join phong p on p.maphong = ct.maphong
join loaiphong lp on lp.maloaiphong = p.maloaiphong
where ct.thoidiemnhanthucte <= @den_ngay
  and ct.thoidiemnhanthucte <= @hien_tai
  and (ct.thoidiemtrathucte > @tu_ngay
  or (ct.thoidiemtrathucte is null and @hien_tai > @tu_ngay))
group by lp.maloaiphong, lp.tenloaiphong
order by soluotsudung desc, lp.maloaiphong;

