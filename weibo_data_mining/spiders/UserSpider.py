#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Youyang Liu(youyangliu)
#
# Define UserSpider
# Ether query or ContainerID need to be specified,
# When specify query, it will crawl weibos of the first user that when we searching the query word
# When specify ContainerID, it will crawl weibo of the containerId's owner

import ujson
from scrapy.http import FormRequest, Request
from ..items import UserItem, BaikeItem
from .extractors import genUserMblog  # for parsing data
from .extractors import getUserid  # for parsing data
from .extractors import getQuery  # for parsing data
from .TemplateSpider import TemplateSpider  # for inheriting class


class WeiboUserSpider(TemplateSpider):
    """
    User Searching Spider
    """

    name = 'weibouserspider'

    def __init__(self, temp_baike_url, temp_container_prefix,
                 container_id, query, url, allowed_domains, weibo_type):
        super().__init__(allowed_domains, container_id, query, url, weibo_type)
        self.temp_baike_url = temp_baike_url
        self.temp_container_prefix = temp_container_prefix

    def start_requests(self):
        """
        If specify the query word, it will start user searching request, and pass it to parse_search function
        If specify the containerID, it will start the user's Weibo request, and pass it to parse_user function
        :return: Request for searching user or Requests for user's Weibo
        """
        if self.query:

            yield from(FormRequest(method='GET',
                                   url=self.url,
                                   formdata={'containerid': x,
                                             'page': str(1)},
                                   callback=self.parse_search)
                       for x in self.container_id)

        else:
            yield from (FormRequest(
                method='GET',
                url=self.url,
                formdata={'containerid': self.container_id,
                          'page': str(page_num)},
                meta={'page': page_num},
                callback=self.parse_user)
                for page_num in range(1, self.upper_bound + 1))

    def parse_search(self, response):
        """
        From user searching url to get containerID and get Baike info,
        then pass it to parse_user function
        :param response: Response from start_request
        :return: Request for BaikeInfo & a generator of Requests for User's weibo
        """
        result = ujson.loads(response.text)
        cards = result.get('data', {}).get('cards')

        if not cards:
            raise ValueError("Didn't find people you are searching for")
        user_id = getUserid(cards)

        yield Request(
            url=self.temp_baike_url.format(user_id),
            callback=self.parse_baike,
            meta={'user_id': user_id}
        )

        container_id = self.temp_container_prefix.format(user_id)
        yield from (FormRequest(
            method='GET',
            url=self.url,
            formdata={'containerid': container_id,
                      'page': str(page_num)},
            meta={'page': page_num,
                  'id': container_id},
            callback=self.parse_user)
            for page_num in range(1, self.upper_bound + 1))

    def parse_user(self, response):
        """
        To get all Weibo of target user
        :param response: Response from start_request or parse_search function
        :return: a generator that contains UserItem,
                 Request for Baike Info
                 Request for next page
        """
        result = ujson.loads(response.text)
        cards = result.get('data', {}).get('cards')
        if cards:
            if not self.query:
                self.query = getQuery(cards)
                user_id = self.container_id.rstrip('107603')
                yield Request(
                    url=self.temp_baike_url.format(user_id),
                    callback=self.parse_baike,
                    meta={'user_id': user_id}
                )
            current_page = response.meta['page']
            if current_page >= self.upper_bound:
                page = current_page + 1
                yield FormRequest(
                    method='GET',
                    url=self.url,
                    formdata={'containerid': response.meta['id'],
                              'page': str(page)},
                    meta={'page': page,
                          'id':response.meta['id']},
                    callback=self.parse)

            mblogs = genUserMblog(cards)
            yield from (UserItem(idstr=mblog.get('idstr'),
                                 mblog=mblog,
                                 query=self.query,
                                 weibo_type=self.weibo_type)
                        for mblog in mblogs if mblog)

    def parse_baike(self, response):
        """
        grab Baike Info
        :param response: Response from parse_search or parse_user
        :return: A generator contains BaikeItem
        """
        yield BaikeItem(user_id=response.meta['user_id'],
                        query=self.query,
                        source=response.text)
