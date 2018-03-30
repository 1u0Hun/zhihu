# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item , Field


class UserItem(Item):
    name = Field()
    url_token = Field()
    avatar_url = Field()
    articles_count = Field()



