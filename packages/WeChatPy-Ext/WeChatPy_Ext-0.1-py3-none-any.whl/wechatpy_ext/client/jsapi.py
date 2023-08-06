# -*- coding: utf-8 -*-

import time
from wechatpy import WeChatClient
from wechatpy.client.api.jsapi import WeChatJSAPI
from wechatpy.utils import random_string, to_text


def get_jsapi_params(appid, secret, url, noncestr=None, timestamp=None):
    """获取调用 JS API 时需要的参数"""
    client = WeChatClient(appid, secret)
    jsapi_client = WeChatJSAPI(client=client)
    timestamp = timestamp or to_text(int(time.time()))
    noncestr = noncestr or random_string(32)
    jsapi_ticket = jsapi_client.get_jsapi_ticket()
    signature = jsapi_client.get_jsapi_signature(noncestr, jsapi_ticket, timestamp, url)

    params = {
        'appId': appid,
        'timestamp': timestamp,
        'nonceStr': noncestr,
        'signature': signature,
    }

    return params
