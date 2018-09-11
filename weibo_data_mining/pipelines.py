#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Youyang Liu(youyangliu)
#
# Deal with Item yield from spider and store Item into Json file

import ujson
from .items import KeywordItem
from .items import UserItem
from .items import CommentItem
from .items import BaikeItem
from .items import RepostItem
from .items import AttitudeItem


class JsonWriterPipeline(object):
    def __init__(self, file_path_for_keyword,
                 file_path_for_baike,
                 file_path_for_comment,
                 file_path_for_user,
                 file_path_for_repost,
                 file_path_for_attitude):
        self.file_path_for_keyword = file_path_for_keyword
        self.file_path_for_baike = file_path_for_baike
        self.file_path_for_comment = file_path_for_comment
        self.file_path_for_user = file_path_for_user
        self.file_path_for_repost = file_path_for_repost
        self.file_path_for_attitude = file_path_for_attitude

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            file_path_for_keyword=settings.get('KEYWORD_FILE_PATH', 'items.jl'),
            file_path_for_baike=settings.get('BAIKE_FILE_PATH', 'items.jl'),
            file_path_for_user=settings.get('USER_FILE_PATH', 'items.jl'),
            file_path_for_comment=settings.get('COMMENT_FILE_PATH', 'items.jl'),
            file_path_for_repost=settings.get('REPOST_FILE_PATH', 'items.jl'),
            file_path_for_attitude=settings.get('ATTITUDE_FILE_PATH', 'items.jl')
        )

    def open_spider(self, spider):
        if spider.name == 'weibokeywordsearch':
            self.file_for_keyword = open(self.file_path_for_keyword, 'a+')
        if spider.name == 'weibouserspider':
            self.file_path_for_user = '{}{}.json'.format(
                self.file_path_for_user, spider.query)
            self.file_for_user = open(self.file_path_for_user, 'a+')
            self.file_for_baike = open(self.file_path_for_baike, 'a+')
        if spider.name == 'weiborcaspider':
            self.file_for_comment = open(self.file_path_for_comment, 'a+')
            self.file_for_repost = open(self.file_path_for_repost, 'a+')
            self.file_for_attitude = open(self.file_path_for_attitude, 'a+')

    def close_spider(self, spider):
        if spider.name == 'weibokeywordsearch':
            self.file_for_keyword.close()
        if spider.name == 'weibouserspider':
            self.file_for_user.close()
            self.file_for_baike.close()
        if spider.name == 'weiborcaspider':
            self.file_for_comment.close()
            self.file_for_repost.close()
            self.file_for_attitude.close()

    def process_item(self, item, spider):
        line = '{}\n'.format(ujson.dumps(dict(item)))
        if isinstance(item, KeywordItem):
            self.file_for_keyword.write(line)

        if isinstance(item, UserItem):
            self.file_for_user.write(line)

        if isinstance(item, BaikeItem):
            self.file_for_baike.write(line)

        if isinstance(item, CommentItem):
            self.file_for_comment.write(line)

        if isinstance(item, RepostItem):
            self.file_for_repost.write(line)

        if isinstance(item, AttitudeItem):
            self.file_for_attitude.write(line)

        return item
