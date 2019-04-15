# project info

@author: youyangliu

Thanks to @contributor: Frank Wang


# tutorial 

This project use scrapy structure to crawl Weibo
and save data as json file in local path.

Right now it support 5 searching mode:

    0 for Keyword searching
    1 for User searching
    2 for Comment searching
    3 for Repost searching
    4 for Attitude searching

And it will return 5 types Item in json:

    KeywordItem for Keyword searching
    UserItem, BaikeItem for User searching
    CommentItem for Comment searching
    RepostItem for Repost searching
    AttitudeItem for Attitude searching


**In this version, it already supports multiple query word at one time**

For scrapy structure details, check scrapy documentation https://docs.scrapy.org/en/latest/

To start,

**cd to Sina_WebCrawler folder and run command for help**:

    python run_spider.py -h

it will show all details about arguments.




# Example

The data structure is saved as a dictionary that keys are defined in items.py file.

KeywordItem eg:

    {'idstr': '3565971237113805',
    'query': '爱他美',
    'weibo_type': 'keyword',
    'mblog': {'attitudes_count': 0,
           'bid': 'zrGddtQCN',
           'bmiddle_pic': 'http://ww2.sinaimg.cn/bmiddle/bd8134fcgw1e3lv8qzurdj.jpg',
           'can_edit': False,
           'comments_count': 1,
           'content_auth': 0,
           'created_at': '2013-04-11',
           'favorited': False,
           'id': '3565971237113805',
           'idstr': '3565971237113805',
           'isLongText': False,
           'is_paid': False,
           'itemid': 'seqid:2046535555|type:1|t:|pos:75-0-7|q:爱他美|ext:&cate=31&mid=3565971237113805&',
           'mblog_vip_type': 0,
           'mid': '3565971237113805',
           'more_info_type': 0,
           'original_pic': 'http://ww2.sinaimg.cn/large/bd8134fcgw1e3lv8qzurdj.jpg',
           'page_info': {'content1': '',
                         'content2': '',
                         'object_id': '1022:2315224b62a62f1871e5708f872b4487cdf2ed',
                         'page_pic': {'url': 'https://u1.sinaimg.cn/upload/2013/02/05/topic_default.png'},
                         'page_title': '#德国限购爱他美最新发展#',
                         'page_url': 'https://m.weibo.cn/p/searchall?containerid=231522type%253D1%2526q%253D%2523%25E5%25BE%25B7%25E5%259B%25BD%25E9%2599%2590%25E8%25B4%25AD%25E7%2588%25B1%25E4%25BB%2596%25E7%25BE%258E%25E6%259C%2580%25E6%2596%25B0%25E5%258F%2591%25E5%25B1%2595%2523%2526t%253D10&luicode=10000011&lfid=100103type%3D1%26q%3D%E7%88%B1%E4%BB%96%E7%BE%8E',
                         'type': 'topic'},
           'pending_approval_count': 0,
           'pics': [{'geo': False,
                     'large': {'geo': False,
                               'size': 'large',
                               'url': 'https://ww2.sinaimg.cn/large/bd8134fcgw1e3lv8qzurdj.jpg'},
                     'pid': 'bd8134fcgw1e3lv8qzurdj',
                     'size': 'orj360',
                     'url': 'https://ww2.sinaimg.cn/orj360/bd8134fcgw1e3lv8qzurdj.jpg'}],
           'reposts_count': 12,
           'rid': '8_0_0_3071691117613763259_0_0',
           'source': '微博 weibo.com',
           'status': 0,
           'text': "<a class='k' "
                   "href='https://m.weibo.cn/p/searchall?containerid=231522type%3D1%26q%3D%23%E5%BE%B7%E5%9B%BD%E9%99%90%E8%B4%AD%E7%88%B1%E4%BB%96%E7%BE%8E%E6%9C%80%E6%96%B0%E5%8F%91%E5%B1%95%23%26t%3D10&luicode=10000011&lfid=100103type%3D1%26q%3D%E7%88%B1%E4%BB%96%E7%BE%8E'>#德国限购爱他美最新发展#</a> "
                   '大家都看过这张告示了吗！！！从两盒降到一盒！！！！下一步是不是规定只能２人拼１单，一人买半盒啊！！！！（转自<a '
                   "href='https://m.weibo.cn/n/李于子都'>@李于子都</a> ） \u200b",
           'thumbnail_pic': 'http://ww2.sinaimg.cn/thumbnail/bd8134fcgw1e3lv8qzurdj.jpg',
           'user': {'avatar_hd': 'https://wx3.sinaimg.cn/orj480/bd8134fcly8fp4kc42czjj20yi0yiacm.jpg',
                    'badge': {'bind_taobao': 1,
                              'dzwbqlx_2016': 1,
                              'follow_whitelist_video': 1,
                              'user_name_certificate': 1},
                    'close_blue_v': False,
                    'cover_image_phone': 'https://tva2.sinaimg.cn/crop.0.0.640.640.640/a1d3feabjw1ecat8op0e1j20hs0hswgu.jpg',
                    'description': '招销售！微信：deguoshiye  '
                                   '微店：http://weidian.com/s/336292868?wfr=c '
                                   '欢迎私信微信各种勾搭！欢迎直邮代发各种代理！',
                    'follow_count': 2063,
                    'follow_me': False,
                    'followers_count': 43032,
                    'following': False,
                    'gender': 'm',
                    'id': 3179361532,
                    'like': False,
                    'like_me': False,
                    'mbrank': 6,
                    'mbtype': 12,
                    'profile_image_url': 'https://tvax3.sinaimg.cn/crop.0.0.1242.1242.180/bd8134fcly8fp4kc42czjj20yi0yiacm.jpg',
                    'profile_url': 'https://m.weibo.cn/u/3179361532?uid=3179361532&luicode=10000011&lfid=100103type%3D1%26q%3D%E7%88%B1%E4%BB%96%E7%BE%8E',
                    'screen_name': '德国师爷',
                    'statuses_count': 21565,
                    'urank': 43,
                    'verified': False,
                    'verified_type': -1},
           'visible': {'list_id': 0, 'type': 0},
           'weibo_position': 1}}

CommentItem

    {'idstr': 4242197014445814,
    'mblog': {'created_at': '05-21',
           'id': 4242197014445814,
           'like_counts': 0,
           'liked': False,
           'source': '',
           'text': '<br/><span class="url-icon"><img alt="[话筒]" '
                   'src="//h5.sinaimg.cn/m/emoticon/icon/others/o_huatong-9f86617336.png" '
                   'style="width:1em; height:1em;"/></span>',
           'user': {'follow_me': False,
                    'following': False,
                    'id': 5785023760,
                    'mbtype': 0,
                    'profile_image_url': 'https://tva2.sinaimg.cn/crop.0.0.310.310.180/006jvmWQjw1eyq6u2k6hqj308m08m3ys.jpg',
                    'profile_url': 'https://m.weibo.cn/u/5785023760?uid=5785023760',
                    'remark': '',
                    'screen_name': '嫪恋彼016',
                    'verified': False,
                    'verified_type': -1}},



