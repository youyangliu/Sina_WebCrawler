#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Youyang Liu(youyangliu)
#
# run Weibo crawler
# There are some import arguments you need to customize:
# $type for spider searching mode.
# $query for query words
# required for keywords searching, optional for user searching, no need for comment/repost/attitude searching
# $containerID for user searching(optional) and comment searching(required)
# For details, check arguments description

import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from weibo_data_mining.spiders.KeywordSpider import WeiboKeywordSearchSpider
from weibo_data_mining.spiders.UserSpider import WeiboUserSpider
from weibo_data_mining.spiders.RCASpider import WeiboRCASpider

SPIDER_DICT = {
    0: WeiboKeywordSearchSpider,
    1: WeiboUserSpider,
    2: WeiboRCASpider,
    3: WeiboRCASpider,
    4: WeiboRCASpider
}

TYPE_DICT = {
    0: 'keyword',
    1: 'user',
    2: 'comment',
    3: 'repost',
    4: 'attitude'
}


def modifySettings(log_level, keyword_path, baike_path, comment_path, user_path, repost_path, attitude_path):
    settings = get_project_settings()
    settings.update({'LOG_LEVEL': log_level})

    if keyword_path:
        settings.update({'KEYWORD_FILE_PATH': keyword_path})
    if baike_path:
        settings.update({'BAIKE_FILE_PATH': baike_path})
    if comment_path:
        settings.update({'COMMENT_FILE_PATH': comment_path})
    if user_path:
        settings.update({'USER_FILE_PATH': user_path})
    if repost_path:
        settings.update({'REPOST_FILE_PATH': repost_path})
    if attitude_path:
        settings.update({'ATTITUDE_FILE_PATH': attitude_path})

    return settings


def main():
    """
    There are 4 parts in this function,
    1 get arguments
    2 parse arguments
    3 modify settings
    4 start crawler
    :return: None
    """
    # get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-q',
                        '--query',
                        dest='query',
                        type=str,
                        help="query: the query word you want to search."
                             "when searching type is keyword searching, this parameter is required,"
                             "and it returns Weibo that contains query words."
                             "when searching type is user searching, and you already have user's containerID,"
                             "you don't need to set query words."
                             "if specify, it returns Weibos of the first user's you search."
                             "Not required for comments, repost, attitude searching"
                        )

    parser.add_argument('-kp',
                        '--keyword_path',
                        dest='keyword_path',
                        default='results/Keyword/keywords.json',
                        type=str,
                        help='keyword_path: the path where keyword searching Weibo results store.'
                             'If not specify, it will store at .results/Keywords/keyword/keywords.json')

    parser.add_argument('-up',
                        '--user_path',
                        dest='user_path',
                        default='results/User/',
                        type=str,
                        help='user_path: the path where user searching results store.'
                             'Right now it only support point out the directory'
                             'If not specify, it will store at .results/User/ directory.'
                             'Each user has a file')

    parser.add_argument('-cp',
                        '--comment_path',
                        dest='comment_path',
                        default='results/Comment/comments.json',
                        type=str,
                        help='comment_path: the path where comments searching results store.'
                             'If not specify, it will store at .results/Comment/Comments.json.')

    parser.add_argument('-rp',
                        '--repost_path',
                        dest='repost_path',
                        default='results/Repost/repost.json',
                        type=str,
                        help='repost_path: the path where reposts searching results store.'
                             'If not specify, it will store at .results/Repost/repost.json.')

    parser.add_argument('-ap',
                        '--attitude_path',
                        dest='attitude_path',
                        default='results/Attitude/attitude.json',
                        type=str,
                        help='attitude_path: the path where attitude searching results store.'
                             'If not specify, it will store at .results/Attitdue/attitude.json.')

    parser.add_argument('-bp',
                        '--baike_path',
                        dest='baike_path',
                        default='results/Baike/baike.json',
                        type=str,
                        help='baike_path: the path where Baike info results store.'
                             'If not specify, it will store at .results/Baike/Baike.json.')

    parser.add_argument('-bu',
                        '--baike_url',
                        dest='baike_url',
                        default='https://weibo.com/{}/baike?from=infocard',
                        type=str,
                        help='baike_url: Baike info url.'
                             'If not specify, it will be https://weibo.com/{user_id}/baike?from=infocard')

    parser.add_argument('-tcp',
                        '--temp_container_prefix',
                        dest='container_prefix',
                        default='107603{}',
                        type=str,
                        help='container_prefix: when searching user, containerID prefix.'
                             'If not specify, it will be 107603')

    parser.add_argument('-t',
                        '--type',
                        dest='type',
                        type=int,
                        default=0,
                        help='type: the different searching method of Weibo'
                             '0 for keywords search weibo'
                             '1 for user search weibo'
                             '2 for comments'
                             '3 for reposts'
                             '4 for attitudes'
                             'If not specify, it will crwal weibo that contain query words ')

    parser.add_argument('-u',
                        '--url',
                        dest='url',
                        type=str,
                        help='url: the domain part of request we want to send'
                             'If not specify,'
                             'for keywords/user weibo searching,'
                             'it will be https://m.weibo.cn/api/container/getIndex.'
                             'For comments searching, it will be https://m.weibo.cn/api/comments/show'
                             'For reposts searching, it will be https://m.weibo.cn/api/statuses/repostTimeline'
                             'For attitude searching, it will be https://m.weibo.cn/api/attitudes/show'
                        )

    parser.add_argument('-l',
                        '--log_level',
                        dest='log_level',
                        default='INFO',
                        type=str,
                        help='log_level: the log level you want to show'
                             'If not specify, it will be INFO level'
                             'For debugging, you can set it to DEBUG')

    parser.add_argument('-c',
                        '--container',
                        dest='container_id',
                        type=str,
                        help="container_id: the parameters of request url"
                             "For user searching, if containerID specify,"
                             "it will crawl the user's Weibo directly."
                             "Otherwise it will search the query words first"
                             "For comment, repost, attitude searching, it is required")

    parser.add_argument('-a',
                        '--allowed_domains',
                        dest='allowed_domains',
                        default=['m.weibo.cn', 'weibo.com'],
                        type=list,
                        help='allowed_domains: the allowed domain for crawling'
                             'If not specify, allowed_domains are'
                             'm.weibo.cn, weibo.com')

    # start to parse arguments
    args = parser.parse_args()

    TYPE = args.type
    if TYPE not in (0, 1, 2, 3, 4):
        raise ValueError('Type should be in 0, 1, 2, 3, 4')

    QUERY = args.query
    CONTAINER_ID = args.container_id
    if QUERY:
        QUERY = QUERY.split('，')
        if TYPE == 1 and CONTAINER_ID:
            raise Warning('For user searching, either query word or containerID need to be specified.'
                          'If will search for query word instead of containerID')
    else:
        if TYPE == 0:
            raise ValueError('Need query words for keywords searching')
        if TYPE == 1 and not CONTAINER_ID:
            raise ValueError('Ether query word or contianerID is needed for user searching')

    temp = '100103type={}&q={}'
    if CONTAINER_ID:
        CONTAINER_ID = CONTAINER_ID.split(',')
        if TYPE == 1 and QUERY:
            CONTAINER_ID = [temp.format(TYPE + 2, x) for x in QUERY]
    else:
        if TYPE == 0:
            CONTAINER_ID = [temp.format(TYPE + 1, x) for x in QUERY]
        elif TYPE == 1:
            CONTAINER_ID = [temp.format(TYPE + 2, x) for x in QUERY]
        elif TYPE == 2:
            raise ValueError('Container_id is required for comment searching')
        elif TYPE == 3:
            raise ValueError('Container_id is required for repost searching ')
        elif TYPE == 4:
            raise ValueError('Container_id is required for attitude searching')

    URL = args.url
    if not URL:
        if TYPE == 2:
            URL = 'https://m.weibo.cn/api/comments/show'
        elif TYPE == 3:
            URL = 'https://m.weibo.cn/api/statuses/repostTimeline'
        elif TYPE == 4:
            URL = 'https://m.weibo.cn/api/attitudes/show'
        else:
            URL = 'https://m.weibo.cn/api/container/getIndex'

    ALLOWED_DOMAINS = args.allowed_domains
    LOG_LEVEL = args.log_level
    BAIKE_URL = args.baike_url
    CONTAINER_PREFIX = args.container_prefix

    KEYWORD_PATH = args.keyword_path
    USER_PATH = args.user_path
    BAIKE_PATH = args.baike_path
    COMMENT_PATH = args.comment_path
    REPOST_PATH = args.repost_path
    ATTITUDE_PATH = args.attitude_path

    # modify settings
    settings = modifySettings(log_level=LOG_LEVEL,
                              keyword_path=KEYWORD_PATH,
                              user_path=USER_PATH,
                              baike_path=BAIKE_PATH,
                              comment_path=COMMENT_PATH,
                              repost_path=REPOST_PATH,
                              attitude_path=ATTITUDE_PATH)

    # start Crawler
    process = CrawlerProcess(settings)

    if TYPE == 1:
        process.crawl(SPIDER_DICT[TYPE],
                      query=QUERY,
                      url=URL,
                      container_id=CONTAINER_ID,
                      allowed_domains=ALLOWED_DOMAINS,
                      weibo_type=TYPE_DICT[TYPE],
                      temp_baike_url=BAIKE_URL,
                      temp_container_prefix=CONTAINER_PREFIX
                      )

    else:
        process.crawl(SPIDER_DICT[TYPE],
                      query=QUERY,
                      url=URL,
                      container_id=CONTAINER_ID,
                      allowed_domains=ALLOWED_DOMAINS,
                      weibo_type=TYPE_DICT[TYPE])

    process.start()


if __name__ == '__main__':
    main()
