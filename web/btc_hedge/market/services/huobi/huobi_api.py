# -*- coding: utf-8 -*-
import hashlib
import time
import urllib
import logging
import urllib
import requests

HUOBI_SERVICE_URL="http://api.huobi.com/"
HUOBI_SERVICE_API="https://api.huobi.com/apiv3"

class huobiAPI(object):

    def __init__(self, mykey, mysecret, timeout=3):
        self.mykey = mykey
        self.mysecret = mysecret
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    '''
    用户相关数据请求
    '''
    def __trade_api_call(self, nParams, extra):
        try:
            nParams['access_key'] = self.mykey
            nParams['created'] = long(time.time())
            nParams['sign'] = self.__create_sign(nParams)
            if(extra) :
                for k in extra:
                    v = extra.get(k)
                    if(v != None):
                        nParams[k] = v
            response = requests.post(HUOBI_SERVICE_API, nParams)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print 'huobi trade api call request excetion: %s' % str(e)
            self.logger.exception('huobi trade api call request excetion: %s' % str(e))
            return None

    '''
    数据格式如下
    ##实时行情数据接口 目前支持人民币现货、美元现货
    [BTC-CNY] http://api.huobi.com/staticmarket/ticker_btc_json.js
    [LTC-CNY] http://api.huobi.com/staticmarket/ticker_ltc_json.js
    [BTC-USD] http://api.huobi.com/usdmarket/ticker_btc_json.js
    报价：最高价，最低价，当前价，成交量，买1，卖1
    [BTC-CNY] http://api.huobi.com/staticmarket/depth_btc_json.js
    [LTC-CNY] http://api.huobi.com/staticmarket/depth_ltc_json.js
    [BTC-USD] http://api.huobi.com/usdmarket/depth_btc_json.js
    指定深度数据条数（1-150条）
    [BTC-CNY] http://api.huobi.com/staticmarket/depth_btc_X.js
    [LTC-CNY] http://api.huobi.com/staticmarket/depth_ltc_X.js
    [BTC-USD] http://api.huobi.com/usdmarket/depth_btc_X.js
    X表示返回多少条深度数据，可取值 1-150
    '''
    def __data_api_call(self, nParams):
        try:
            if nParams.get('currency', 'cny') == 'cny':
                nParams['currency'] = 'static'
            api_url = HUOBI_SERVICE_URL + '%smarket/' % (nParams['currency'])
            api_url += '%s_%s_%s.js' % (nParams.get('method', 'ticker'), \
                                        nParams.get('coin', 'btc'), \
                                        nParams.get('size', 'json'))
            print api_url
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print 'huobi data api call request excetion: %s' % str(e)
            self.logger.exception('huobi data api call request excetion: %s' % str(e))
            return None

    '''
    生成签名
    '''
    def __create_sign(self, params):
        params['secret_key'] = self.mysecret;
        params = sorted(params.items(), key=lambda d:d[0], reverse=False)
        message = urllib.urlencode(params)
        message=message.encode(encoding='UTF8')
        m = hashlib.md5()
        m.update(message)
        m.digest()
        sig=m.hexdigest()
        return sig

    def query_account(self):
        params = {"method" : "get_account_info"}
        extra = {}
        return self.__trade_api_call(params, extra)

    def ticker(self, coin_currency='btc_cny'):
        nParams = {'method': 'ticker'}
        nParams['coin'], nParams['currency'] = coin_currency.split('_')
        return self.__data_api_call(nParams)


    def depth(self, coin_currency='btc_cny', size=25):
        nParams = {'method': 'depth', 'size': str(size)}
        nParams['coin'], nParams['currency'] = coin_currency.split('_')
        return self.__data_api_call(nParams)

if __name__ == '__main__':
    access_key = 'access_key'
    access_secret = 'access_secret'
    api = huobiAPI(access_key, access_secret)
    print(api.query_account())
    print(api.ticker('ltc_cny'))
    print(api.depth())
