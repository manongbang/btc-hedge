# coding: utf-8
from __future__ import unicode_literals

from common.constants import DEFAUTL_SERVICE_TIMEOUT
from .base_market import BasePublicMarket, BasePrivateMarket
from .chbtc.chbtc_api import chbtcAPI


class chbtcMarket(BasePublicMarket, BasePrivateMarket):
    """
        API refer to:
        https://www.chbtc.com/i/developer/restApi
    """

    def __init__(self, api_key, api_secret, timeout=DEFAUTL_SERVICE_TIMEOUT):
        self.timeout = timeout
        self.service = chbtcAPI(api_key, api_secret, self.timeout)

    # override
    def ticker(self):
        return self.service.ticker(currency='btc_cny')

    # override
    def depth(self):
        return self.service.depth(currency='btc_cny')
