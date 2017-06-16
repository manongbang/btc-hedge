# coding: utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext as _


def enum(**enums):
    return type(str('Enum'), (), enums)

DEFAUTL_SERVICE_TIMEOUT = 3

MARKET_TYPES = enum(
    OKCOIN=1,
    HUOBI=2,
    CHBTC=3,
    # TODO: add more market here
)

MARKET_SHORT_NAME = {
    MARKET_TYPES.OKCOIN: 'okcoin',
    MARKET_TYPES.HUOBI: 'huobi',
    MARKET_TYPES.CHBTC: 'chbtc'
}

MARKET_TYPE_CHOICES = [
    (MARKET_TYPES.OKCOIN, _('OKCoin')),
    (MARKET_TYPES.HUOBI, _('Huobi Coin')),
    (MARKET_TYPES.CHBTC, _('China BTC')),
]
