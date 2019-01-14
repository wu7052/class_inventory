set @cur_date = date_format(current_date(),'%Y%m%d');
set @00 =0, @30=0, @60=0, @002=0;

#select ws.id, ws.date, ws.disc as ws_disc, ws.price as ws_price, ws.close_price as ins_price, ws.vol_tf ,dd.close as latest_price 
#from ws_201901 as ws left join code_002_201901 as dd 
#on ws.id = dd.id 
#where dd.date =  @cur_date and ws.price >= dd.close;

select count(distinct(ws.id)) into @002
from ws_201901 as ws left join code_002_201901 as dd 
on ws.id = dd.id 
where dd.date = @cur_date and ws.price >= dd.close;

select count(distinct(ws.id)) into @00
from ws_201901 as ws left join code_00_201901 as dd 
on ws.id = dd.id 
where dd.date = @cur_date and ws.price >= dd.close;

select count(distinct(ws.id)) into @30
from ws_201901 as ws left join code_30_201901 as dd 
on ws.id = dd.id 
where dd.date = @cur_date and ws.price >= dd.close;

select count(distinct(ws.id)) into @60
from ws_201901 as ws left join code_60_201901 as dd 
on ws.id = dd.id 
where dd.date = @cur_date and ws.price >= dd.close;

select @00, @30, @002, @60;