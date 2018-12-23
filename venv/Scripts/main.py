from logger_package import myLogger
from filePackage import MyFile
from db_package import db_ops
from stock_package import ts_data, sz_web_data, sh_web_data
import sys
import os
import pandas as pd

if __name__ == '__main__':
    # print("@__init__ sys.path", sys.path)

    # 深市 所有股票的基本信息获取
    sz_data = sz_web_data()
    sz_basic_list_url = "http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1110&TABKEY=tab1&PAGENO=2&random=0.6886288319449341"
    json_str = sz_data.get_json_str(sz_basic_list_url)
    pos = json_str.find('"error":null') # 定位截取Json字符串的位置
    json_str = json_str[1:pos-1] + '}'
    # sz_data.logger.wt.info(json_str)
    sz_basic_info_df = sz_data.basic_info_json_parse(json_str)
    # sz_data.logger.wt.info("\n{}".format(sz_basic_info_df))
    sz_data.db_load_into_list_a(sz_basic_info_df)


    """  
    # 沪市 所有股票的所属行业 DataFrame
    sh_data = sh_web_data()
    sh_data.industry_df_build() # 沪市股票 所属的行业类型、公司全称
    sh_data.logger.wt.info("Return from [industry_df_build]\n{}".format(sh_data.industry_df))

    # 从Web获取沪市 所有股票的基本信息
    # 从Json读取 股票代码、名称、总股份、流动股份、上市日期
    page_counter = 1
    while True:
        sh_basic_list_url = 'http://query.sse.com.cn/security/stock/getStockListData2.do?&jsonCallBack=jsonpCallback99887&' \
              'isPagination=true&stockCode=&csrcCode=&areaName=&stockType=1&pageHelp.cacheSize=1&pageHelp.beginPage=' \
              + str(page_counter) + '&pageHelp.pageSize=25&pageHelp.pageNo=' + str(page_counter) + \
              '&pageHelp.endPage=' + str(page_counter) + '1&_=1517320503161' + str(page_counter)
        json_str = sh_data.get_json_str(sh_basic_list_url)
        json_str = '{"content":' + json_str[19:-1] + '}'
        basic_info_df = sh_data.basic_info_json_parse(json_str)
        # sh_data.logger.wt.info(basic_info_df)

        # 基本信息 与 公司全名、所属行业、行业代码 等补充信息进行合并
        basic_info_df = pd.merge(basic_info_df, sh_data.industry_df, how='left', left_on='ID', right_on='ID')
        sh_data.logger.wt.info("Total Page:{}---{}\n========================================"
                               .format(sh_data.total_page, page_counter))
        # sh_data.logger.wt.info("Total Page:{}---{}\n{}".format(sh_data.total_page, page_counter, basic_info_df))

        # 开始写入数据库 Stock -- 表list_a
        for array in basic_info_df.get_values():
            sql = "select * from list_a where id ='"+array[0]+"'"
            # sql =  'select count(*) from list_a where id = \'%s\''%array[0]
            iCount = db.cursor.execute(sql) # 返回值，受影响的行数， 不需要 fetchall 来读取了
            if iCount == 0:
                sql ="insert into list_a (id, name, total_shares, flow_shares, list_date, full_name, industry, industry_code) " \
                     "values (%s, %s, %s ,%s, %s, %s, %s, %s)"
                sh_data.logger.wt.info("Insert id={0}, name={1}, t_shares={2}, f_shares={3}, date={4}, f_name={5}, industry={6}, industry_code={7}".
                             format(array[0], array[1], array[2], array[3], array[4], array[5], array[6], array[7]))
                db.cursor.execute(sql,(array[0], array[1], float(array[2]), float(array[3]), array[4], array[5], array[6], array[7]))
                db.handle.commit()
            elif iCount == 1:
                sh_data.logger.wt.info("Existed\t[{0}==>{1}]".format(array[0], array[1]))
            else:
                sh_data.logger.wt.info("iCount == %d , what happended ???"% iCount)

        page_counter += 1
        if page_counter > int(sh_data.total_page[0]):
            break
        else:
            continue
        """



"""
# stock = ts_data()
# data = stock.basic_info()
# print(data)
# pass
"""

"""
# Logger 测试代码

logger = myLogger('.')
logger.wt.info("from logger [wuxiang]")
logger.wt.info('It works!')  # 记录该文件的运行状态
logger.wt.debug('debug message')
logger.wt.warning('warning message')
logger.wt.error('error message')
logger.wt.critical('critical message')
"""

"""
# MySQL 测试代码
try:
    db = db_ops(host='127.0.0.1', db='stock', user='wx', pwd='5171013')
    sql = "SELECT ID FROM LIST_A "
    db.cursor.execute(sql)
    db.handle.commit()
    result = db.cursor.fetchall()
    for _ in result:
        print(_[0])

    db.cursor.close()
    db.handle.close()
except Exception as e:
    print("Err occured {}".format(e))
"""

"""
# MyFile 测试代码
#a = file_class.MyFile("./filePackage/test.txt")
a = MyFile("./filePackage/test.txt")
a.printFilePath()
a.testWriteFile()
a.testReadFile()
"""

# workpath = os.path.dirname(os.path.abspath(sys.argv[0]))
# pack_name = ['logger_package','stock_package','filePackage','db_package']
# for _ in pack_name:
#     pack_path = workpath+'\\'+_
#     sys.path.insert(0, pack_path)

# logfile_dir = os.path.dirname(os.path.abspath('.'))
# logfile_dir += '\\log\\'
# print (logfile_dir)

# path= sys.path
# print (path)

# path = sys.argv[0]
# print (sys.argv[0])
# print (os.path.abspath(sys.argv[0]))
# workpath = os.path.dirname(os.path.abspath(sys.argv[0]))
# sys.path.insert(0, os.path.join(workpath, 'modules'))
