# -*- coding: utf-8 -*-
# 用于进行http请求，以及MD5加密，生成签名的工具类

import requests
import hashlib

DEFAULT_TIMOUT = 10  # seconds


def buildMySign(params, secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) + '&'
    data = sign + 'secret_key=' + secretKey
    return hashlib.md5(data.encode("utf8")).hexdigest().upper()


def httpGet(url, resource, params='', timeout=DEFAULT_TIMOUT):
    r = requests.get(url + resource + '?' + params, timeout=timeout)
    return r.json()


def httpPost(url, resource, params, timeout=DEFAULT_TIMOUT):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    r = requests.post(url + resource, headers=headers, data=params)
    return r.json()
