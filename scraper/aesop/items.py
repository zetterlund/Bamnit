# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# import numpy as np
# import math

class ListingItem(scrapy.Item):
    aesop_id = scrapy.Field()
    teacher = scrapy.Field()
    title = scrapy.Field()
    position = scrapy.Field()
    subject = scrapy.Field()
    campus = scrapy.Field()
    times = scrapy.Field()
    begin_time = scrapy.Field()
    end_time = scrapy.Field()
    dates = scrapy.Field()
    begin_date = scrapy.Field()
    end_date = scrapy.Field()
    multiday = scrapy.Field()
    fullday = scrapy.Field()
    notes = scrapy.Field()
    date_posted = scrapy.Field()
    date_removed = scrapy.Field()
    language = scrapy.Field()
    grade = scrapy.Field()
    notification_sent = scrapy.Field()