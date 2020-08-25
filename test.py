import json,time,string,re,os
from os.path import isfile, isdir, join
from os import listdir
main_address = os.path.dirname(os.path.abspath(__file__))
files = listdir(main_address + "\\Data\\")
print(files)