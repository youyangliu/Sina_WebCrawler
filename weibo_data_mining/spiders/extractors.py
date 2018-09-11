#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Youyang Liu(youyangliu)
#
# Define extra function to parse response


from typing import List, Generator  # restrict input type


def genCardGroup(cards: List):
    """
    parse the data structure and get Weibo group info
    :param cards: a list that contains Weibo info
    :return: a generator that contains card_group (define in response)
    """
    for card in cards:
        card_group = card.get('card_group')
        if card_group:
            yield card_group


def genMblog(card_groups: Generator):
    """
    get single Weibo raw data
    :param card_groups: a generator that contain card_group info (defined in response)
    :return: Weibo info raw data
    """
    for card_group in card_groups:
        for item in card_group:
            mblog = item.get('mblog')
            if mblog:
                yield mblog


def genUserMblog(cards: List):
    """
    get user's Weibo, for user searching spider
    :param cards: a list that contains User Weibo Info
    :return: a generator that contains User Weibo raw data
    """
    for card in cards:
        mblog = card.get('mblog')
        if mblog:
            yield mblog


def getQuery(cards: List):
    """
    For user searching spider, if specify ContainerID, generate the user's name
    :param cards: a List that contains User Info
    :return: a user's name
    """
    query = cards[0]['mblog']['user']['screen_name']
    return query


def getUserid(cards: List):
    """
    For user searching spider, if specify Query word, get the user's ContainerID
    :param cards: a List that contains User Info
    :return: user's containerID
    """
    target_card = cards[1]['card_group'][0]
    if target_card:
        user_id = target_card['user']['id']
        return user_id


def genRCAData(data):
    """
    get raw repost/comment/attitude data
    :param data:
    :return: a generator that contains repost/comment/attitude raw data
    """
    for item in data:
        yield item
