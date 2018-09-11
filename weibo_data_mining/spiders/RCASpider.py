# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Youyang Liu(youyangliu)
#
# Define RCASpider
# When specify weibo_id, it will crawl the reposts/comments/attitude of this weibo

import ujson
from scrapy.http import FormRequest
from ..items import CommentItem, RepostItem, AttitudeItem
from .extractors import genRCAData
from .TemplateSpider import TemplateSpider

ITEM_DICT = {
    'comment': CommentItem,
    'repost': RepostItem,
    'attitude': AttitudeItem
}


class WeiboRCASpider(TemplateSpider):
    """
    Repost/Comment/Attitude Searching Spider
    it will return different item depending on spider.weibo_type
    """

    name = 'weiborcaspider'

    def start_requests(self):
        """
        Generate Requests for reposts/comments/attitude
        :return: upper_bound numbers of requests
        """
        yield from (FormRequest(
            method='GET',
            url=self.url,
            formdata={'id': container_id, 'page': str(page_num)},
            meta={'page': page_num,
                  'id': container_id},
            callback=self.parse)
            for container_id in self.container_id
            for page_num in range(1, self.upper_bound + 1))

    def parse(self, response):
        """
        Deal with the response and return RepostItem/CommentItem/AttitudeItem
        :param response: response from start_request
        :return: a generator contains CommentItem
        """
        result = ujson.loads(response.text)
        data = result.get('data', {}).get('data')
        if data:
            current_page = response.meta['page']
            if current_page >= self.upper_bound:
                page = current_page + 1
                yield FormRequest(
                    method='GET',
                    url=self.url,
                    formdata={'id': response.meta['id'],
                              'page': str(page)},
                    meta={'page': page,
                          'id': response.meta['id']},
                    callback=self.parse)

            items = genRCAData(data)
            yield from (ITEM_DICT[self.weibo_type](idstr=self.container_id,
                                                   mblog=item,
                                                   weibo_type=self.weibo_type)
                        for item in items)
