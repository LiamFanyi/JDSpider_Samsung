# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import csv
import time

# use url to get HTML file
def getHtmlText(url):
    headers1 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "search.jd.com",
        "Cookie": "xtest=5669.cf6b6759; ipLoc-djd=53283-53309-0-0; __jdc=122270672; __jdv=122270672|direct|-|none|-|1523216742562; __jdu=1523216742561181941258; rkv=V0700; 3AB9D23F7A4B3C9B=JM46L2ZP3IFRQM5YP6I63L6DXQXMILGFJHINJP7QZ676NI5DGJMSKKNDNOC5XEKVDIBF552TV7ZFY6PQZNO6JNQE5A; qrsc=3; __jda=122270672.1523216742561181941258.1523216743.1523216743.1523220838.2; __jdb=122270672.3.1523216742561181941258|2.1523220838",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    print(url)
    if url[8:10] == "se":#把搜索页面和手机详细页面区分开
        headers = headers1
    else:
        headers = headers2

    # proxies = {'http': '114.217.129.128 8998'}
    # use agent Ip
    # r = requests.get(url, headers=headers, proxies=proxies)
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    return r.text

    # To generate a url list(global var)

def getAllPages():#get all the searching page
    allPagesUrlList = []
    singlePageUrl = ''
    for page in range(1, 32):#16 pages in total
        s = 1+30*page
        if page%2 == 1:#odd page contains all the information
            singlePageUrl = 'https://search.jd.com/search?keyword=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&ev=exbrand_%E4%B8%89%E6%98%9F%EF%BC%88SAMSUNG%EF%BC%89%5E&page='+str(page)+'&s='+str(s)+'&click=0'
            allPagesUrlList.append(singlePageUrl)
    return allPagesUrlList

# To get detail information of cellphone
def getPhonesUrl(pageUrl):

    time.sleep(1)
    html = getHtmlText(pageUrl)
    pat = "data-pid=\".*\">"
    phonesIdList = [string[10:-2] for string in re.findall(pat, html)]
    return phonesIdList

#To get the name of the cellphone
def getPhoneName(phoneurl):
    time.sleep(1)
    infoText = getHtmlText("https://item.jd.com/"+phoneurl+".html")
    soup = BeautifulSoup(infoText, 'html.parser')
    name = soup.find('div', attrs={'class': 'sku-name'}).get_text().strip()
    return name

#To get the price of the cellphone
def getPhonePrice(phoneurl):
    # the price cannot be directly get, you have to use the request header to get a url to use your item ID to get the price
    time.sleep(1)
    priceUrl = 'https://p.3.cn/prices/mgets?skuIds=J_' + phoneurl
    print(priceUrl,phoneurl)
    priceText = getHtmlText(priceUrl)
    pattern = re.compile('"p":"(.*?)"')
    price = re.findall(pattern, priceText)[0]
    return price

#To get the properties of cellphone
def getPhoneProperties(phoneurl):
    phoneProperties = {}
    list_value = []
    list_name = []

    time.sleep(1)
    infoText = getHtmlText("https://item.jd.com/"+phoneurl+".html")
    soup = BeautifulSoup(infoText, 'html.parser')
    proSection = soup.findAll('div', attrs={'class': 'Ptable-item'})
    #there are 2 types of info format, to find which one can be used
    #TYPE 1
    for pro in proSection:
        # using difference set to get the info
        list_all = pro.find_all('dd')
        list_extracted = pro.find_all('dd', {'class': 'Ptable-tips'})
        list_chosen = [i for i in list_all if i not in list_extracted]

        for dd in list_chosen:
            list_value.append(dd.string)

        for dt in pro.find_all('dt'):
            list_name.append(dt.string)

    for i in range(0, len(list_name)):
        phoneProperties.update({list_name[i]: list_value[i]})
    if len(phoneProperties) == 0:#if none can be found in TYPE1, then TYPE2
        #TYPE 2
        proSection = soup.findAll('table', attrs={'class': 'Ptable'})

        for tr in proSection:
            # using difference set
            list_all = tr.find_all('td')
            # print(list_all)
            list_extracted = tr.find_all('td', {'class': 'tdTitle'})
            list_chosen = [i for i in list_all if i not in list_extracted]

            for td in list_chosen:
                list_value.append(td.string)

            for td in list_extracted:
                list_name.append(td.string)

        for i in range(0, len(list_name)):
            phoneProperties.update({list_name[i]: list_value[i]})


    return phoneProperties

#directly get all the info of phone(call several function)
def getPhoneInfo(phoneurl):
    time.sleep(1)
    phoneInfo = {}
    price = getPhonePrice(phoneurl)
    phoneInfo.update({'价格':price})  # 字符串
    name = getPhoneName(phoneurl)
    phoneInfo.update({'名称': name})  # 字符串
    phoneProperties = getPhoneProperties(phoneurl)
    phoneInfo.update({'手机配置':phoneProperties})  #  字典

    return phoneInfo

#main function
if __name__ == '__main__':
    url = 'https://search.jd.com/search?keyword=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&ev=exbrand_%E4%B8%89%E6%98%9F%EF%BC%88SAMSUNG%EF%BC%89%5E&page=1&s=1&click=0'
    phoneInfoAll = []
    requests.adapters.DEFAULT_RETRIES = 5
    # 程序开始时间
    allPagesUrlList = getAllPages()#get all searching pages' url
    print(allPagesUrlList)
    # for i in  allPagesUrlList:
    #     print i
    startTime = time.clock()
    for search_page_url in allPagesUrlList:#traversal every single searching page
        phoneUrls = getPhonesUrl(search_page_url)
        # for x in phoneUrls:
        #     print x

        for phoneurl in phoneUrls:#traversal every url to get detail of phone
            time.sleep(1)
            print(u'正在爬取第', str(phoneUrls.index(phoneurl) + 1), u'部手机......')
            print(len(phoneUrls))
            wrongURL =["https://p.3.cn/prices/mgets?skuIds=J_23390489103",
                       "https://p.3.cn/prices/mgets?skuIds=J_4520002",
                       "https://p.3.cn/prices/mgets?skuIds=J_25440508942",
                       "https://p.3.cn/prices/mgets?skuIds=J_1990031660"]
            if phoneurl in wrongURL :
                continue
            info = getPhoneInfo(phoneurl)
            phoneInfoAll.append(info)

            phoneName = info['名称']
            print(phoneName)
            phonePrice = info['价格']
            print(phonePrice)
            phoneProperties = info['手机配置']
            print(phoneProperties)
            with open("JDresult.csv", "a",newline='',encoding='UTF-8') as csvfile:#write into csv
                writer = csv.writer(csvfile)
                # 先写入columns_name
                writer.writerow([phoneName,phonePrice])
                for key in phoneProperties.keys():
                    InfoNeeded =['机身颜色','RAM','电池容量（mAh）','前置摄像头','后置摄像头']#choose the info we need
                    if key in InfoNeeded:
                        writer.writerow([key+":"+phoneProperties[key]])#写入csv
    endTime = time.clock()
    print('所有手机爬取完毕,程序耗费的时间为：', endTime - startTime)