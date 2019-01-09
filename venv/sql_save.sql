#select count(id) from stock.list_a where id like '60%';

#SELECT count(distinct id) as total FROM stock.code_60_201901;


#select count(id) from stock.list_a where id like '00%';

#SELECT count(distinct id) as total FROM stock.code_00_201901;

#select count(id) from stock.list_a where id like '30%';

#SELECT count(distinct id) as total FROM stock.code_30_201901;

#select A.id from stock.list_a AS A left join stock.code_60_201901 as B ON A.id = B.id WHERE A.id like '60%' and B.id is null

#select A.id from stock.list_a AS A left join stock.code_30_201901 as B ON A.id = B.id WHERE A.id like '30%' and B.id is null

select A.id from stock.list_a AS A left join stock.code_00_201901 as B ON A.id = B.id WHERE A.id like '00%' and B.id is null