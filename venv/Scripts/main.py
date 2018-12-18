# from filePackage import MyFile
# from logger_package import myLogger
from db_package import db_ops
import sys
import os

if __name__ == '__main__':
    try:
        db = db_ops(host='127.0.0.1', db='stock', user='wx', pwd='5171013')
        sql = "SELECT COUNT(*) FROM LIST_A "
        db.cursor.execute(sql)
        db.handle.commit()
        result = db.cursor.fetchall()
        print(result)

        db.cursor.close()
        db.handle.close()
    except Exception as e:
        print("Err occured {}".format(e))



"""
# MyFile 测试代码
#a = file_class.MyFile("./filePackage/test.txt")
a = MyFile("./filePackage/test.txt")
a.printFilePath()
a.testWriteFile()
a.testReadFile()
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
