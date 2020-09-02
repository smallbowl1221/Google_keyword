import requests
import string
import csv
import bs4
import os,sys
from os.path import isfile, isdir, join
from os import listdir
import time,datetime
from time import sleep
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib.request as req

#載入 Urlget.py 檔案的位置並加上目錄 Data
main_address = os.path.dirname(os.path.abspath(__file__))
#載入資料位置
Data_address = os.path.abspath("..") + "\\Data\\Google\\G_Data"

#files ==> 將 \ALL\ 資料夾中的文件存取
files = listdir(main_address + "\\IO\\" + "ALL\\")
print(files)

#載入隨機user agent
ua = UserAgent(verify_ssl=False)

#google url
google_url = "https://www.google.com.tw/"

#https://www.google.com/search?q=key1+key2&start=0


def geturl(page):
    
    #緩衝15秒
    print("緩衝中...")
    sleep(15)

    #目前搜尋頁面
    search_url_page = search_url + "&start=" + str(page) + "0"
    print("-"*200)
    print("目前抓取網頁:" + search_url_page)
 

    request = req.Request(search_url_page, headers = {"User-Agent" : ua.chrome})

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    #取得文章bs4物件
    root = bs4.BeautifulSoup(data, "html.parser")

    #抓取每一筆url相關的html
    search_set = root.find_all("div",class_= "r")
    print("search_set 數量" + str(len(search_set)))
    print()

    #判斷是否未擷取到資料
    if(len(search_set) == 0):
        print("未擷取任何URL，",end = "")
        print("重新載入中",end = "")
        for i in range(7):
            print(".",end ="")
            sleep(0.5)
        print()
        return True,None
    else:
        # 將獲取的標題和URL存入list_reg中   [ ["標題","URL"] , .... ]
        list_reg = []
        for i in search_set:
            reg = []
            print(i.h3.text)    # 標題
            reg.append(str(i.h3.text))
            print(i.a["href"])  # URL
            reg.append(str(i.a["href"]))
            print()
            list_reg.append(reg)
        return False,list_reg

for files_num in files:

    print(files_num + ":" + "="*200)

    #dataname_list 暫存 dataname
    dataname_list = []

    #存放所有key (二維)
    key_frame = []

    #path_list 暫存 path
    path_list = []

    # 讀取 input.txt 
    with open(  main_address + "\\IO\\" + "ALL\\" + files_num , "r" , newline="" , encoding="utf-8-sig") as txtFile:
        for line in txtFile:
            #去除/r/n
            line = line.strip()
            #以空格" "來分離key ==> key_list_reg為一陣列
            key_list_reg = line.split(" ")
            #將結果存入key_frame
            key_frame.append(key_list_reg)
            #key_frame = [["台積電","薪水","年終"]]

    # 逐列開始抓取URL   
    for key_list in key_frame:

        #顯示現在搜尋之詞彙
        print("="*200)
        print("現在抓取之關鍵字: " + key_list[0])
        
        #初始dataname
        dataname = ""

        # 將 key_list 中的 key 轉換成UTF-8-------------------------------------------
        # EX:    台灣 => %E5%8F%B0%E7%81%A3
        for i in range(len(key_list)):
            #設定dataname
            dataname += key_list[i] + "+"
            key = key_list[i].encode('utf-8')
            key = str(key).replace("\\x","%").upper()
            key = key[2:len(key)-1]
            key_list[i] = key

        #刪除 dataname 後面多餘的 "+"
        dataname = dataname.rstrip("+")

        #創建目錄
        address_dic = Data_address + "\\" + dataname + "\\"
        

        if not os.path.isfile(address_dic + dataname + "_url.csv"):
            #將dataname 存入 dataname_list
            dataname_list.append(dataname)
            #存放url的list

            url_list = []

            #設定google search url 格式
            search_url = "https://www.google.com/search?q="

            #將 key 加入 google search url 中
            for key in key_list:
                search_url += key + "+"

            #刪除後面多餘的 "+"
            search_url = search_url.rstrip("+")

            #逐頁抓取(共 3 頁)
            for page in range(0,3,1):
                #key of 空值
                success = True
                #times => 執行次數
                times = 0
                while(success):
                    times += 1
                    #最多執行10次
                    if(times < 10):
                        success,url_list_reg = geturl(page)
                    else:
                        success = False
                if(url_list_reg != None):
                    url_list += url_list_reg


            #創建目錄
            address_dic = Data_address + "\\" + dataname + "\\"

            #檢查目錄是否存在
            if not os.path.isdir(address_dic):
                os.mkdir(address_dic)

            #將 path 存入
            path_list.append(address_dic)

            #文章存入 CSV 檔案--------------------------------------------------------------------------------------------------------------------------------------------
            with open(address_dic + dataname +"_url.csv", "w", newline='',encoding="utf-8-sig") as csvFile:
                # 建立 CSV 檔寫入器
                writer = csv.writer(csvFile)
                writer.writerow(["Title","url"])
                for i in url_list:
                    writer.writerow([ i[0],i[1] ])

        else:
            print(dataname + "_url.csv is exist")


print("Urlget.py program finish")