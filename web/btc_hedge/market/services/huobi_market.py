# coding: utf-8
from __future__ import unicode_literals

from common.constants import DEFAUTL_SERVICE_TIMEOUT
from .base_market import BasePublicMarket, BasePrivateMarket
from .huobi.huobi_api import huobiAPI


class huobiMarket(BasePublicMarket, BasePrivateMarket):
    """
        API refer to:
        https://api.huobi.com/apiv3
    """

    def __init__(self, api_key, api_secret, timeout=DEFAUTL_SERVICE_TIMEOUT):
        self.timeout = timeout
        self.service = huobiAPI(api_key, api_secret, self.timeout)

    # override
    def ticker(self):
        return self.service.ticker(currency='btc_cny')

    # override
    def depth(self):
        return self.service.depth(currency='btc_cny')
