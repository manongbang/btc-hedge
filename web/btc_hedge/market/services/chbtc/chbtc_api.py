import logging
import hashlib
import struct
import sha
import time
import requests

logger = logging.getLogger(__name__)


class chbtcAPI(object):
    TRADE_URL = 'https://trade.chbtc.com/api/'
    DATA_URL = 'http://api.chbtc.com/data/v1/'

    def __init__(self, mykey, mysecret, timeout=3):
        self.mykey = mykey
        self.mysecret = mysecret
        self.timeout = timeout

    def __fill(self, value, length, fillByte):
        if len(value) >= length:
            return value
        else:
            fillSize = length - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s)
        for index in xrange(len(slist)):
            slist[index] = chr(ord(slist[index]) ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb = struct.pack("%ds" % len(aKey), aKey)
        value = struct.pack("%ds" % len(aValue), aValue)
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad)
        m.update(value)
        dg = m.digest()

        m = hashlib.md5()
        m.update(k_opad)
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value = struct.pack("%ds" % len(aValue), aValue)
        # print value
        h = sha.new()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def __trade_api_call(self, path, params=''):
        try:
            SHA_secret = self.__digest(self.mysecret)
            sign = self.__hmacSign(params, SHA_secret)
            reqTime = (int)(time.time()*1000)
            params += '&sign=%s&reqTime=%d' % (sign, reqTime)
            url = self.TRADE_URL + path + '?' + params
            response = requests.get(url, timeout=self.timeout)
            return response.json()
        except Exception:
            logger.exception('chbtc trade API request exception')
            return None

    def __data_api_call(self, path, params=''):
        try:
            url = self.DATA_URL + path + '?' + params
            response = requests.get(url, timeout=self.timeout)
            return response.json()
        except Exception:
            logger.exception('chbtc data API request exception')
            return None

    def query_account(self):
        params = "method=getAccountInfo&accesskey=" + self.mykey
        path = 'getAccountInfo'
        try:
            obj = self.__trade_api_call(path, params)
            return obj
        except Exception:
            logger.exception('chbtc query_account exception')
        return None

    def ticker(self, currency='btc_cny'):
        params = "currency=" + currency
        path = 'ticker'
        try:
            obj = self.__data_api_call(path, params)
            return obj
        except Exception:
            logger.exception('chbtc get ticker exception')
        return None

    def depth(self, currency='btc_cny', size=25):
        params = "currency={c}&size={size}".format(c=currency, size=size)
        path = 'depth'
        try:
            obj = self.__data_api_call(path, params)
            return obj
        except Exception:
            logger.exception('chbtc get depth exception')
        return None


if __name__ == '__main__':
    access_key = 'accesskey'
    access_secret = 'secretkey'

    api = chbtcAPI(access_key, access_secret)

    print api.query_account()
