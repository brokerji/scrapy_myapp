from scrapy.spiders import CrawlSpider
from scrapy.http import  Request
from scrapy.selector import  Selector
import re
import json
from itertools import islice
from .. import items
class Application(CrawlSpider):
    name = "myapp"
    redis_key = 'myapp:start_urls'
    start_urls = ['http://android.myapp.com/myapp/category.htm?orgame=1']
    url = 'http://android.myapp.com/myapp/category.htm?orgame=1'
    url_raw = 'http://android.myapp.com/myapp/category.htm'
    url_cat = 'http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=106&pageSize=20&pageContext=40'
    url_cat1 = 'http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId='
    #global urlj
    count =[]

    def parseCategory(self,response):
        selector = Selector(response)
        #print(type(response.url))
        lis = selector.xpath('//div[@class="main"]/ul[@class="app-list clearfix"]/li/div[@class="app-info clearfix"]/div[@class="app-info-desc"]/a[1]/text()').extract()
        pageContext = selector.xpath('body/script[1]').extract()
        match = re.findall(r'\d+',str(pageContext))
        match2 = re.findall(r'\d+',response.url)
       # print(match[1])#pageContext =40
       # print(match2[1])#categoryId = 111
       # print(lis)
        urlj = self.url_cat1 +""+ match2[1]+ "&pageSize=20"+"&pageContext=0"
        yield Request(urlj,callback=self.parseCateJiazai)

    def parseCateJiazai(self,response):
        item = items.MyappItem()
        encodejson = bytes.decode(response.body)
        e2 = json.loads(encodejson)
        all = e2['obj']
        for i in all:
            print(i['appName'])
            print(str(i['appDownCount'] / 10000) + "万")
            print(i['appRatingInfo'])
            item['flag'] = i['flag']
            item['appId'] = i['appId']
            item['fileSize'] = i['fileSize']
            item['authorId'] = i['authorId']
            item['categoryId'] = i['categoryId']
            item['categoryName'] = i['categoryName']
            item['apkMd5'] = i['apkMd5']
            item['apkUrl'] = i['apkUrl']
            item['appName'] = i['appName']
            item['downloadCount'] = i['appDownCount']
            item['authorName'] = i['authorName']
            item['averageRating'] = i['averageRating']
            item['pkgName'] = i['pkgName']
            item['versionCode'] = i['versionCode']
            item['versionName'] = i['versionName']
            item['apkPublishTime'] = i['apkPublishTime']
            item['appRatingInfo'] = i['appRatingInfo']
            item['snapshotsUrl'] = i['snapshotsUrl']
            item['appTags'] = i['appTags']
            yield item

        if e2['pageContext']!= "":
            if response.url[-2] == "=":
                urlx = (response.url[:-1])+ e2['pageContext']
            elif response.url[-3] == "=":
                urlx = (response.url[:-2])+ e2['pageContext']
            elif response.url[-4] == "=":
                urlx = (response.url[:-3]) + e2['pageContext']
            yield Request(urlx,callback=self.parseCateJiazai)

    def parse(self, response):
        selector = Selector(response)
        urls = selector.xpath('//div[@class="nav-menu"]/ul[@class="menu"]/li[1]/ul[@class="menu-junior"]/li/a/@href').extract()
        cates = selector.xpath('//div[@class="nav-menu"]/ul[@class="menu"]/li[1]/ul[@class="menu-junior"]/li/a/text()').extract()
#category[社交]=?orgame=1&amp;categoryId=106
        #print(urls)
        #print(cates)
        category = {}
        for urli,cate in zip(urls,cates):
            #if cate == '全部软件'and urli =='?orgame=1':
            #    continue
            #if cate == '展开更多'and urli == 'javascript:void(0);':
            #    continue
            if cate == '全部软件':
                continue
            if cate == '展开更多':
                continue
            if cate == '腾讯软件':
                continue
            else :
                nums = re.findall(r'\d+', str(urli))
                #print(nums[1]) #106
             #   urlj = self.url_cat1 + nums[1]+'&pageSize=20&'
              #  print (urlj)
                urli = self.url_raw + urli
                category[cate] = urli
                yield  Request(urli,callback=self.parseCategory)





