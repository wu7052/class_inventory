set @s_00 = 0;
set @s_002 =0;
set @s_30 = 0;
set @s_60 = 0;
#set @cur_date =  current_date();
set @cur_date = date_format(current_date(),'%Y%m%d');

#set @cur_date = utc_date();
#set @cur_date = now();
select @cur_date;

select count(id) into @s_00 from code_00_201901 where date= @cur_date;
select count(id) into @s_002 from code_002_201901 where date= @cur_date;
select count(id) into @s_30 from code_30_201901 where date= @cur_date;
select count(id) into @s_60 from code_60_201901 where date= @cur_date;

set @total = @s_00+ @s_002+ @s_30+ @s_60;
select @cur_date, @s_00, @s_002, @s_30, @s_60, @total;