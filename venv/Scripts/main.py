#from filePackage import file_class
from filePackage import MyFile
from logger_package import myLogger

import sys
import os
#import filePackage.file


if __name__ == '__main__':
    #a = file_class.MyFile("./filePackage/test.txt")
    a = MyFile("./filePackage/test.txt")
    a.printFilePath()
    a.testWriteFile()
    a.testReadFile()

logger = myLogger('.')
logger.wt.info("from logger [wuxiang]")
logger.wt.info('It works!')  # 记录该文件的运行状态
logger.wt.debug('debug message')
logger.wt.warning('warning message')
logger.wt.error('error message')
logger.wt.critical('critical message')

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
