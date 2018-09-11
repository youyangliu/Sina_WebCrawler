#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Youyang Liu(youyangliu)
#
# Define TemplateSpider
# For parsing arguments

from scrapy import Spider


class TemplateSpider(Spider):
    """
    define a template spider to parse arguments
    """

    name = 'templatespider'

    def __init__(self, allowed_domains, container_id, query,
                 url, weibo_type, upper_bound=100):
        super().__init__()
        self.allowed_domains = allowed_domains
        self.container_id = container_id
        self.query = query
        self.url = url
        self.upper_bound = upper_bound
        self.weibo_type = weibo_type
