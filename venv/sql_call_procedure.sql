SET @t_60_v=0;
SET @f_60_v=0;
SET @t_30_v=0;
SET @f_30_v=0;
SET @t_00_v=0;
SET @f_00_v=0;

call list_a_total_amount('20190108',@t_60_v, @f_60_v, @t_30_v, @f_30_v, @t_00_v, @f_00_v);

select @t_60_v, @f_60_v, @t_30_v, @f_30_v, @t_00_v, @f_00_v;

#select a.id, a.total_shares, a.flow_shares, b.close, b.date from stock.list_a as a left join stock.code_30_201901 as b on a.id = b.id where b.date='20190104'
#select a.id, a.total_shares, a.flow_shares, b.close, b.date from stock.list_a as a left join stock.code_00_201901 as b on a.id = b.id where b.date='20190104';
#