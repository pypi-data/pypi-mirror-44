# coding=utf-8
import config
from ucenter.ws_handler.manage_handler import ManageHandler

base = 'v1/{}/ws'.format(config.PLATFORM)
routes = [
    (r'/%s/manage' % base, ManageHandler)
]
