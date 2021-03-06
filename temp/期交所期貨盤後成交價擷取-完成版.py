﻿import urllib, re

"""
執行結果為於執行目錄下,將產生一個**期交所每日期貨收盤資料.txt**文字檔
"""
"""
期交所盤後約14:30分,網站才更新今日大盤資料
故14:30前需要去抓昨天以前的資料
期交所網站http://www.taifex.com.tw/chinese/3/3_1_1.asp
假設查詢不到該日期,將會將網頁跳至今天的日期
"""
import time

start = time.time() #記錄程式執行後的開始時間

from time import strftime
today = strftime('%Y/%m/%d')
hour = strftime('%H%M')
year =  strftime('%Y')
month = strftime('%m')
day = strftime('%d')

# 1430下午兩點半以前抓昨天以前的資料,1430以後抓今天以前的資料
if int(hour) < 1430:
#    day=int(day)-1 為何要抓昨天以前即前天資料?
    day=int(day)
    if day < 9:
        download_date = year+'/'+month+'/'+'0'+str(day)
else:
    download_date = today


f = open(u'期交所每日期貨收盤資料.txt','w') #欲儲存資料的文字檔檔名
f.write("開盤價         最高價         最低價         最後成交價     成交量         未沖銷契約量   日期\n") #文字檔標頭

year = [2015] # 想要哪何年資料,用逗號分隔
month = [5]   # 想要哪何月資料,用逗號分隔

print u"正在連結期交所網站抓取資料，請稍等。抓取一個月的資料約10秒，需等待多久取決於抓取多少月份的資料"

# 年月日迴圈
for iyear in year:
    iyear = str(iyear)
    for imonth in month:
        imonth=str(imonth)

        j=1
        while j <=31:
          
            print iyear,imonth,j # 每連結一天,於螢幕列印該天日期.
            date = str(j)
            optionUrl = "http://www.taifex.com.tw/chinese/3/3_1_1.asp?goday=&syear="+iyear+"&smonth="+imonth+"&sday="+date+"&COMMODITY_ID=TX"  #連結期交所該天網頁

            html = urllib.urlopen(optionUrl)  #open file-like object

            regexp = re.compile(r"<TD align=right class=\"12bk\">(?P<file>.*)</TD>") #Compile a regular expression pattern, returning a pattern object., 成交價格
            check_date = re.compile(r"<h3 align=\'left\'>日期：(?P<file>.*)</h3>") # 該網頁的日期
           
            # 正規表示式 (?P<file>.*)  一個括號裡面的東西為一個group
                     
            i = 0 #只抓前六筆符合的資料(開盤價 最高價 最低價  最後成交價 成交量  未沖銷契約量)
            for line in html.readlines():
                result = regexp.search(line)
                date_ck = check_date.search(line)
                #search(string[, pos[, endpos]]) --> match object or None.
                #Scan through string looking for a match, and return a corresponding
                #MatchObject instance. Return None if no position in the string matches.
                if date_ck != None:  #輸入不正確日期,會連結到今天的網頁
                    tmp1 = date_ck.group('file')  #參數可以打 'file'  或只打數字 1  變數regexp一個括號裡面的東西為一個group
                    if tmp1 == download_date: # 假設網頁是今天跳出for迴圈,不儲存資料.期交所網站輸入不正確的日期會跳到今天日期的網頁
                        break
                                                          
                if result != None:   #列假日與國定假日都抓不到資料為None
                    fileName = result.group('file')  #參數可以打 'file'  或只打數字 1  變數regexp一個括號裡面的東西為一個group
                    # MatchObject instances support the following methods and attributes:
                    # http://docs.python.org/release/2.5.2/lib/match-objects.html
                    i+=1
                                        
                    f.write('%-15s'%(fileName)) #儲存價格資料
                           
                if i >= 6 :  #只抓前六筆符合的資料(開盤價 最高價 最低價  最後成交價 成交量  未沖銷契約量),超過前六筆資料後列印日期與跳出for迴圈
                    f.write('%s-%s-%s'%(iyear,imonth,j))
                    f.write('\n')
                    break
            j+=1
          
            html.close()
        
f.close()


print u"抓取資料完成"

end = time.time() # 紀錄程式執行完的結束時間
elapsed = end - start # 總程式執行時間

print u"總共花費", elapsed, u"秒."
    
