# - * - coding: utf-8 - * -

__author__ = "樊懿"

from scrapy.spiders import CrawlSpider
from JDSpider.items import JdspiderItem
from scrapy.selector import Selector
from scrapy.http import Request
import requests
import re, json

class JdSpider(CrawlSpider):
    name = "JDSpider"
    redis_key = "JDSpider:start_urls"
    # start_urls = ["http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10001-1#comfort"]
    start_urls = ["https://search.jd.com/search?keyword=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&ev=exbrand_%E4%B8%89%E6%98%9F%EF%BC%88SAMSUNG%EF%BC%89%5E&page=1&s=1&click=0"]

    # 生成手机1-170页的url列表(最初调用一次，全局使用)
    def getAllPages():
        allPagesUrlList = []
        singlePageUrl = ''
        for page in range(1, 32):
            s = 1+30*page
            if page%2 == 1:
                singlePageUrl = 'https://search.jd.com/search?keyword=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&ev=exbrand_%E4%B8%89%E6%98%9F%EF%BC%88SAMSUNG%EF%BC%89%5E&page='+str(page)+'&s='+str(s)+'&click=0' \
            # singlePageUrl = 'https://list.jd.com/list.html?cat=9987,653,655&page=' \
            #                 + str(page) + '&sort=sort%5Frank%5Fasc&trans=1&JL=6_0_0#J_main'
                allPagesUrlList.append(singlePageUrl)
        return allPagesUrlList
    def parse(self, response):
        item = JdspiderItem()
        selector = Selector(response)
        # Books = selector.xpath('/html/body/div[8]/div[2]/div[3]/div/ul/li')
        PhonesLink = selector.xpath('//*[@id="J_goodsList"]/ul/li/div/div[4]/a/@href')#每个li下面都有一个手机跳转的链接
        for each in PhonesLink:
            # num = each.xpath('div[@class="p-num"]/text()').extract()
            # bookName = each.xpath('div[@class="p-detail"]/a/text()').extract()
            # author = each.xpath('div[@class="p-detail"]/dl[1]/dd/a[1]/text()').extract()
            # press = each.xpath('div[@class="p-detail"]/dl[2]/dd/a/text()').extract()

            temphref = each.xpath('div[@class="p-detail"]/a/@href').extract()
            temphref = str(temphref)
            # BookID = str(re.search('com/(.*?)\.html',temphref).group(1))
            phoneID = str(re.search('com/(.*?)\.html',temphref).group(1))

            json_url = 'http://p.3.cn/prices/mgets?skuIds=J_' + phoneID
            r = requests.get(json_url).text
            data = json.loads(r)[0]
            price = data['m']
            # PreferentialPrice = data['p']

            item['phoneName'] = name
            item['phoneID'] = phoneID
            item['phoneRAM'] = phoneRAM
            item['phoneColor'] = phoneColor
            item['phoneBattery'] = phoneBattery
            item['price'] = price
            item['frontcamera'] = frontcamera
            item['backcamera'] = backcamera

            yield item

        nextLink = selector.xpath('/html/body/div[8]/div[2]/div[4]/div/div/span/a[7]/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            print(nextLink)
            yield Request(nextLink,callback=self.parse)
