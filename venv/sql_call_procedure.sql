SET @t_60=0, @f_60=0, @t_30=0, @f_30=0, @t_00=0, @f_0=0;

call list_a_total_amount('20190107',@t_60, @f_60, @t_30, @f_30,@t_00, @f_00);

select @t_60, @f_60, @t_30, @f_30,@t_00, @f_00;

#select a.id, a.total_shares, a.flow_shares, b.close, b.date from stock.list_a as a left join stock.code_30_201901 as b on a.id = b.id where b.date='20190104'
#select a.id, a.total_shares, a.flow_shares, b.close, b.date from stock.list_a as a left join stock.code_00_201901 as b on a.id = b.id where b.date='20190104';
#