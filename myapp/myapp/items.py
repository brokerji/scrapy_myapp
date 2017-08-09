# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyappItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    flag = scrapy.Field()
    appId = scrapy.Field()
    fileSize = scrapy.Field()
    authorId = scrapy.Field()
    categoryId = scrapy.Field()
    categoryName = scrapy.Field()
    apkMd5 = scrapy.Field()
    apkUrl = scrapy.Field()
    appName = scrapy.Field()
    downloadCount = scrapy.Field()
    authorName = scrapy.Field()
    averageRating = scrapy.Field()
    pkgName = scrapy.Field()
    versionCode = scrapy.Field()
    versionName = scrapy.Field()
    apkPublishTime = scrapy.Field()
    appRatingInfo = scrapy.Field()
    snapshotsUrl = scrapy.Field()
    appTags = scrapy.Field()