SET @t_60_v=0;
SET @f_60_v=0;
SET @t_30_v=0;
SET @f_30_v=0;
SET @t_00_v=0;
SET @f_00_v=0;
SET @t_002_v=0;
SET @f_002_v=0;

call list_a_total_amount('20190114',@t_60_v, @f_60_v, @t_30_v, @f_30_v, @t_00_v, @f_00_v, @t_002_v, @f_002_v);

select @t_60_v as '上证（亿）', @f_60_v as '上证流动（亿）', 
		@t_30_v as '创业（亿）', @f_30_v as '创业流动（亿）', 
        @t_00_v as '深证', @f_00_v as '深证（流动)',
        @t_002_v as '深证', @f_002_v as '深证（流动)';

#select a.id, a.total_shares, a.flow_shares, b.close, b.date from stock.list_a as a left join stock.code_30_201901 as b on a.id = b.id where b.date='20190104'
#select a.id, a.total_shares, a.flow_shares, b.close, b.date from stock.list_a as a left join stock.code_00_201901 as b on a.id = b.id where b.date='20190104';
#