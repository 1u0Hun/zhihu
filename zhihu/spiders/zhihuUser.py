# -*- coding: utf-8 -*-
from time import sleep

import scrapy
from scrapy import Spider,Request
import json

from zhihu.items import UserItem


class ZhihuuserSpider(scrapy.Spider):
    name = 'zhihuUser'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    start_user = 'excited-vczh'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'


    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user,include=self.user_query),callback=self.user_parse)
        yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query,limit=20,offset=0),callback=self.follows_parse)




    def user_parse(self, response):

        result = json.loads(response.text)
        item = UserItem()
        item['name'] = result['name']
        item['url_token']=result['url_token']
        item['avatar_url']=result['avatar_url']
        item['articles_count'] = result['articles_count']

        yield item

        yield Request(
            self.follows_url.format(user=result['url_token'], include=self.follows_query, offset=0, limit=20),
            callback=self.follows_parse)



    def follows_parse(self, response):

        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.user_parse)
                # sleep(1)


        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page,callback=self.follows_parse)



