import json,time,string,re,os
from os.path import isfile, isdir, join
from os import listdir

address = "D:\Regiser\Data"

#for i in range(10):


files_get = listdir("D:\python\crawler_NCU\Data\Google\G_Data")


#原始資料數量
# region
num = 0
files = listdir("D:\python\crawler_NCU\Google_keyword\IO\ALL")

for files_num in files:
    print(files_num)
    with open(  "D:\python\crawler_NCU\Google_keyword\IO\ALL\\" + files_num , "r" , newline="" , encoding="utf-8-sig") as txtFile:
        
        for j in files_get:
            key = False
            for i in txtFile:
                i = i.strip()
                if(i == j):
                    key = True
                    break
            if(not key):
                num+=1

                    
print(num)
# endregion

#已抓取url資料數量
#print(len(files))

