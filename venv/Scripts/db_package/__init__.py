import sys
import os

workpath = os.path.dirname(os.path.abspath(sys.argv[0]))
workpath += '\\db_package'
sys.path.insert(0, workpath)
print("@__init__ sys.path",sys.path)

from db_operation import db_ops