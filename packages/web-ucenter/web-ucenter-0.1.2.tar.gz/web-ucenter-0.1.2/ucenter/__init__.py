# coding=utf-8

from ucenter.db import mongo
from ucenter import routes


def init(app):

    # 初始化本系统数据库
    mongo.init()

    # 加载路由模块
    app.load_routes(routes)
