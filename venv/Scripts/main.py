from logger_package import myLogger
from filePackage import MyFile
from db_package import db_ops
from stock_package import ts_data, sz_web_data, sh_web_data
import sys
import os



if __name__ == '__main__':
    # print("@__init__ sys.path", sys.path)
    sh_data = sh_web_data()
    # sh_data.logger.wt.debug("calling from main")
    page_counter =1
    url = 'http://query.sse.com.cn/security/stock/getStockListData2.do?&jsonCallBack=jsonpCallback99887&' \
          'isPagination=true&stockCode=&csrcCode=&areaName=&stockType=1&pageHelp.cacheSize=1&pageHelp.beginPage=' \
          + str(page_counter) + '&pageHelp.pageSize=25&pageHelp.pageNo=' + str(page_counter) + \
          '&pageHelp.endPage=' + str(page_counter) + '1&_=1517320503161' + str(page_counter)
    json_str = sh_data.get_json_str(url)
    json_str = '{"content":' + json_str[19:-1] + '}'
    df = sh_data.json_parse(json_str)
    sh_data.logger.wt.info(df)
    # print(json_str)
    pass

    # stock = ts_data()
    # data = stock.basic_info()
    # print(data)
    # pass

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

#path = sys.argv[0]
#print (sys.argv[0])
#print (os.path.abspath(sys.argv[0]))
#workpath = os.path.dirname(os.path.abspath(sys.argv[0]))
#sys.path.insert(0, os.path.join(workpath, 'modules'))
