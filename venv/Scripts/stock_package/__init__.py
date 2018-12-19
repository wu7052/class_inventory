import sys
import os

workpath = os.path.dirname(os.path.abspath(sys.argv[0]))
workpath += '\\stock_package'
sys.path.insert(0, workpath)
print("@__init__ sys.path",sys.path)

from tushare_data import ts_data
from sh_ex_data import sh_web_data
from sz_ex_data import sz_web_data