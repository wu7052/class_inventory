#from file_class import MyFile
import sys
import os

# print("@__init__ sys.path",sys.path)
# print("@__init__sys.argv[0]",sys.argv[0])
# print("@__init__os.path.abspath(sys.argv[0])",os.path.abspath(sys.argv[0]))
workpath = os.path.dirname(os.path.abspath(sys.argv[0]))
# print("@__init__os.path.dirname()",workpath)
workpath += '\\filePackage'
# print("@__init__workpath",workpath)

sys.path.insert(0,workpath)
# print("@__init__ sys.path new:",sys.path)

from file_class import MyFile

#sys.path.append('../')
#print("@__init__ sys.path.append",sys.path)


#from file_class import MyFile