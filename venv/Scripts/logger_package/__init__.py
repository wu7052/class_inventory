import sys
import os

workpath = os.path.dirname(os.path.abspath(sys.argv[0]))
workpath += '\\logger_package'
sys.path.insert(0, workpath)
# print("@__init__ sys.path",sys.path)

from logger import myLogger
