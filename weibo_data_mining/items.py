#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Youyang Liu(youyangliu)
#
# Define Item structure

from scrapy import Item
from scrapy import Field


class KeywordItem(Item):
    """
    define KeywordItem structure
    """
    idstr = Field()
    mblog = Field()
    query = Field()
    weibo_type = Field()


class UserItem(Item):
    """
    Define UserItem structure
    """
    idstr = Field()
    mblog = Field()
    query = Field()
    weibo_type = Field()


class BaikeItem(Item):
    """
    Define BaikeItem structure
    """
    user_id = Field()
    source = Field()
    query = Field()


class CommentItem(Item):
    """
    Define CommentItem structure
    """
    idstr = Field()
    mblog = Field()
    weibo_type = Field()


class RepostItem(Item):
    """
    Define RepostItem structure
    """
    idstr = Field()
    mblog = Field()
    weibo_type = Field()


class AttitudeItem(Item):
    """
    Define AttitudeItem structure
    """
    idstr = Field()
    mblog = Field()
    weibo_type = Field()
