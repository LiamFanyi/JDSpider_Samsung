import requests
from bs4 import BeautifulSoup
import re
import csv
import time


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
    if url[8:10] == "se":
        headers = headers1
    else:
        headers = headers2

    # proxies = {'http': '114.217.129.128 8998'}
    # 使用伪装浏览器和代理Ip
    # r = requests.get(url, headers=headers, proxies=proxies)
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    return r.text


def getPhoneProperties(phoneurl):
    phoneProperties = {}
    list_value = []
    list_name = []

    infoText = getHtmlText("https://item.jd.com/%s.html" % phoneurl)
    soup = BeautifulSoup(infoText, 'html.parser')
    proSection = soup.findAll('table', attrs={'class': 'Ptable'})

    for tr in proSection:
        # 既然找不到直接去除有属性标签的方法就取个差集吧
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


url = '23009611720'
print(getPhoneProperties(url))
