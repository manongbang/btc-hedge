# coding: utf-8
from __future__ import unicode_literals

from common.constants import DEFAUTL_SERVICE_TIMEOUT
from .base_market import BasePublicMarket, BasePrivateMarket
from .okcoin.OkcoinSpotAPI import OKCoinSpot
from .okcoin.OkcoinFutureAPI import OKCoinFuture


class okcoinMarket(BasePublicMarket, BasePrivateMarket):
    """
        API refer to:
        https://www.okcoin.com/rest_api.html
    """
    API_URL = 'https://www.okcoin.com/'

    def __init__(self, api_key, api_secret, timeout=DEFAUTL_SERVICE_TIMEOUT):
        self.timeout = timeout
        self.spot = OKCoinSpot(self.API_URL, api_key, api_secret)
        self.future = OKCoinFuture(self.API_URL, api_key, api_secret)

    # override
    def ticker(self):
        return self.spot.ticker('btc_usd')

    # override
    def depth(self):
        return self.spot.depth('btc_usd')
