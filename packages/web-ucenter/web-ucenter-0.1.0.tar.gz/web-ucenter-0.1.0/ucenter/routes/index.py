# coding=utf-8

from ucenter.http_handler.index_handler import IndexHandler

base = ''
routes = [
    (r"/%s" % base, IndexHandler),
]
