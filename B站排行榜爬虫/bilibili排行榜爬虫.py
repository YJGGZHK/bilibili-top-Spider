# -*- coding = utf-8 -*- 
# @Time :2021/8/4 10:42 
# @Author:YJGGZHK
# @File : bilibili排行榜爬虫.py
# @Software: PyCharm
from bs4 import  BeautifulSoup #网页解析pip
import re  #文字表达式
import urllib.request,urllib.error #制定url
import xlwt #Excel
import sqlite3 # 数据库

def main():
    baseurl = 'https://www.bilibili.com/v/popular/rank/all'
    # 1 爬取网页
    datalist = getdata(baseurl)
    savepath = ".\\B站视频排行榜"
    # 3保存数据
    savedata(datalist, savepath)


def askurl(url):
    head={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    request=urllib.request.Request(url,headers=head)#赋予头部信息 以此骗过浏览器
    html=""

    #查错
    try:
        response=urllib.request.urlopen(request)
        html=response.read().decode('utf-8')
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
    return html


findlink=re.compile(r'<div class="img"><a href="//(.*?)" target="_blank">')#视频链接
findname=re.compile(r'<a .*>(.*)</a>')#视频名称
findpingfeng=re.compile(r'<div class="pts"><div>(.*)</div>')#视屏评分
findup=re.compile(r'<a .*><span class="data-box up-name"><i class="b-icon author"></i>(.*)</span></a>')#视屏作者




def getdata(baseurl):
    datalist=[]
    rank=0
    for i in range (0,1):
        url=baseurl
        html=askurl(url) #保存返回值 网页源代码
        soup=BeautifulSoup(html,"html.parser")#将HTML内的东西装换为html编译
        for item in soup.find_all('div',class_="content"):
            data=[]
            item=str(item)

            rank+=1
            data.append(rank)

            link = re.findall(findlink, item)  # 查找影片的链接
            data.append(link)



            titles = re.findall(findname, item)
            data.append(titles)


            pf = re.findall(findpingfeng, item)
            data.append(pf)

            
            up = re.findall(findup, item)
            data.append(up)

            datalist.append(data)
           


    return datalist

# 3保存数据
def savedata(datalist,savepath):
    book=xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet=book.add_sheet('bilibili视屏排行榜top100',cell_overwrite_ok=True)
    col=('排名','链接','名称','评分','作者') #,'评论数','播放数',
    for i in range(0,5):
        sheet.write(0,i,col[i])
    for i in range(0,100):
        data=datalist[i]
        for j in range(0,5):
            sheet.write(i+1,j,data[j])
    book.save('bilibili视屏排行榜top100.xls')



if __name__=='__main__': #调用函数
    main()


