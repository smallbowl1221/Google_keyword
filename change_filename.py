import json,time,string,re,os
from os.path import isfile, isdir, join
from os import listdir
import os

path = "D:\\python\\資料備份\\Google\\data_half\\"

files_set = listdir(path)

#把字串全形轉半形
def strQ2B(ustring):
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全形空格直接轉換
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全形字元（除空格）根據關係轉化
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)
#判斷是否為fullwidth
def filterfull(ustring) :

    for s in ustring:
        for uchar in s:
            inside_code = ord(uchar)
            if (inside_code == 12288 or (inside_code >= 65281 and inside_code <= 65374) ):
                return True
    
    return False

def IOrename():
    A = []
    with open("D:\\python\\crawler_NCU\\Google_keyword\\IO\\1.txt","r",newline='',encoding="utf-8-sig") as files:

        for line in files:
            #去除/r/n
            #line = line.strip()
            #以空格" "來分離key ==> key_list_reg為一陣列
            #key_list_reg = line.split(" ")
            #key_frame = [["台積電","薪水","年終"]]
            A.append( strQ2B(line) )
        
    with open("D:\\python\\crawler_NCU\\Google_keyword\\IO\\All.txt","w",newline='',encoding="utf-8-sig") as files:

        for s in A:
            files.write(s)

def filerename(fullname):

    #full to falf
    falfname = strQ2B(fullname)

    # XX_url.csv
    url_oldname = path + fullname + "\\" + fullname + "_url.csv"
    url_newname = path + fullname + "\\" + falfname + "_url.csv"

    # XX_sentence.csv
    sen_oldname = path + fullname + "\\" + fullname + "_sentence.csv"
    sen_newname = path + fullname + "\\" + falfname + "_sentence.csv"

    #file
    file_oldname = path + fullname
    file_newname = path + falfname

    #rename rul.csv   
    os.rename(url_oldname,url_newname)
    print("url半形: " + falfname + "_url.csv")
    #rename sentence.csv
    os.rename(sen_oldname,sen_newname)
    print("sentence半形: " + falfname + "_sentence.csv")
    #rename file
    os.rename(file_oldname,file_newname)
    print("file半形: " + falfname)    


count = 0
for files in files_set:

    if(filterfull(files)):
        print("全形: " + files)
        filerename(files)
        count += 1

print("一共更改 " + str(count) + " 個file")