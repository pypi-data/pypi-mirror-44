#!/usr/bin/env python
# coding=utf-8

from tweb import myweb, base_handler


class IndexHandler(base_handler.BaseHandler):

    # 接收get请求
    @myweb.authenticated
    def get(self):
        return self.render('index/index.html', name='Hello World!')

