#!/usr/bin/python
# coding:utf-8

import pymongo
from tornado.options import options

MongoDB = {
    'active': True,    # 是否启用
    'dev': {
        'host': 'udl.link',
        'port': 27017,
        'db': 'ucdb',
        'user': 'app',
        'pwd': 'Uc2app'
    },
    'prod': {
        'host': 'udl.link',
        'port': 27017,
        'db': 'ucdb',
        'user': 'app',
        'pwd': 'Uc2app'
    }
}

mongo_client = None
mongo_db = None

users = None


def init():
    if not MongoDB['active']:
        return

    global mongo_client
    global mongo_db
    global users

    mongo_cfg = MongoDB[options.env]

    mongo_client = pymongo.MongoClient(host=mongo_cfg['host'],
                                       port=mongo_cfg['port'],
                                       username=mongo_cfg['user'],
                                       password=mongo_cfg['pwd'],
                                       authSource=mongo_cfg['db'])
    mongo_db = mongo_client[mongo_cfg['db']]

    # collections
    users = mongo_db.users

    # 创建索引
    _users_index()


def start_session():
    return mongo_client.start_session()


def _users_index():
    """ users sample
    {
        "_id": ObjectId("5c393f37e155ac54355b37ef"), # 用户ID，使用ObjectId
        "status": 1,                                 # 0: 锁定，1: 正常
        "name": "jack",                              # 登录帐号
        "email": "jack@qq.com",
        "mobile": "86-13012345678",                  # 格式："国家代码-号码"
        "card_id": "422420199009101234",
        "real_name": "张杰克",
        "nickname": "笨笨哥",
        "gender": 1,                                 # 1：男， 2：女
        "country_code": 86,
        "country": "中国",
        "province": "广东",
        "city": "深圳",
        "icon": "http://example.com/icon/jack.png",
        "birthday": "1990-09-10",
        "pwd_hash": "adsfas293rjlsdjfl232489",
        "salt": "23jkas2342",
        "created": 1546763523000,                    # 毫秒
        "updated": 1546763523000,                    # 毫秒
        "weixin": {
            "open_id": "a7823c872348d234889234d323",
            "union_id": "b34d2342a23423bb342c23dd",
            "nickname": "哈哈BBG",
            "icon": "http://qq.com/icon/jack.png",
            "extend": "any string"
        },
        "weibo": {
            "open_id": "cbd232d2342a23423f234e2342b",
            "union_id": "aadd898c899e98998e9e9bb8234",
            "nickname": "大杰张",
            "icon": "http://weibo.com/icon/jack.png",
            "extend": "any string"
        },
        "addresses": [
            {
                "receiver": "张杰克",
                "address": "深圳南山科技园路123号",
                "country_code": 86,
                "zip_code": 518000,
                "tel": "0755-26261234",
                "mobile": "86-13012345678",
                "is_default": 1
            }
        ]
    }
    """
    # users.create_index('_id', unique=True)
    users.create_index('name', unique=True, sparse=True)
    users.create_index('email', unique=True, sparse=True)
    users.create_index('mobile', unique=True, sparse=True)
    users.create_index('card_id', unique=True, sparse=True)
    users.create_index('weixin.open_id', unique=True, sparse=True)
    users.create_index('weixin.union_id')
    users.create_index('wxmp.open_id', unique=True, sparse=True)
    users.create_index('wxmp.union_id')

