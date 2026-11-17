use hotel;
set names utf8mb4;

set @tu_ngay = '2026-10-01 00:00:00';
set @den_ngay = '2026-10-31 23:59:59.999999';

select dv.tendichvu, dv.donvitinh,
       sum(ls.soluong) as tongsoluong,
       ls.dongiaapdung,
       sum(ls.soluong * ls.dongiaapdung) as thanhtien
from lansudungdichvu ls
join dichvu dv on dv.madichvu = ls.madichvu
where ls.thoidiemsudung between @tu_ngay and @den_ngay
group by dv.madichvu, dv.tendichvu, dv.donvitinh, ls.dongiaapdung
order by thanhtien desc, dv.madichvu, ls.dongiaapdung;

