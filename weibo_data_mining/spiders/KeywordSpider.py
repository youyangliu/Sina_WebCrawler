#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Youyang Liu(youyangliu)
#
# Define KeywordSpider
# When specify the query words, it will crawl the weibos that contain query word

import ujson  # for parse response(it's a json file)
from scrapy.http import FormRequest  # a special Request function that can pass parameters directly
from ..items import KeywordItem  # get Item structure
from .extractors import genCardGroup, genMblog  # for parsing data
from .TemplateSpider import TemplateSpider  # for inheriting the class


class WeiboKeywordSearchSpider(TemplateSpider):
    """
    Keyword Searching Spider
    """
    name = 'weibokeywordsearch'

    def start_requests(self):
        """
        generate start Requests
        :return: upper_bound numbers of Requests
        """
        yield from (FormRequest(
            method='GET',
            url=self.url,
            formdata={'containerid': container_id, 'page': str(page_num)},
            meta={'page': page_num,
                  'id': container_id},
            callback=self.parse)
            for container_id in self.container_id
            for page_num in range(1, self.upper_bound + 1))

    def parse(self, response):
        """
        deal with return response,
        if the page meets upper bound and the response is not null,
        it will generate Request for next page info
        and for each Weibo in current page, it will generate Weibo Item

        :param response: response
        :return: a generator that contains KeywordItem,
                 Request for next page
        """
        result = ujson.loads(response.text)
        cards = result.get('data', {}).get('cards')
        if cards:
            current_page = response.meta['page']
            if current_page >= self.upper_bound:
                page_num = current_page + 1
                yield FormRequest(
                    method='GET',
                    url=self.url,
                    formdata={'containerid': response.meta['id'],
                              'page': str(page_num)},
                    meta={'page': page_num,
                          'id': response.meta['id']},
                    callback=self.parse)

            card_groups = genCardGroup(cards)
            mblogs = genMblog(card_groups)
            yield from (KeywordItem(idstr=mblog.get('idstr'),
                                    mblog=mblog,
                                    query=self.query,
                                    weibo_type=self.weibo_type)
                        for mblog in mblogs)
