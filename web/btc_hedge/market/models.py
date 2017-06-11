# coding: utf-8
from __future__ import unicode_literals

import importlib
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

from common.constants import MARKET_SHORT_NAME, MARKET_TYPE_CHOICES


class UserMarketConfig(models.Model):
    trader = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='market_contexts')
    market_type = models.PositiveSmallIntegerField(
        _('Market Type'), choices=MARKET_TYPE_CHOICES)
    api_key = models.CharField(_('API Key'), max_length=256)
    api_secret = models.CharField(_('API Secret'), max_length=512)
    context = JSONField(_('Context'), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        required_db_vendor = 'postgresql'

    @property
    def market(self):
        """返回market_type对应的market实例"""
        assert(self.market_type in MARKET_SHORT_NAME.keys())
        short_name = MARKET_SHORT_NAME[self.market_type]
        MarketModule = importlib.import_module(
            'market.services.{sn}_market'.format(sn=short_name))
        MarketService = getattr(MarketModule, '{sn}Market'.format(sn=short_name))
        instance = MarketService(api_key=self.api_key, api_secret=self.api_secret)
        return instance


class MarketDepth(models.Model):
    """
        记录固定时间间隔的市场深度
        * The bid price represents the maximum price
        that a buyer or buyers are willing to pay for a security.
        * The ask price represents the minimum price
        that a seller or sellers are willing to receive
        for the security.
    """
    market_type = models.PositiveSmallIntegerField(
        _('Market Type'), choices=MARKET_TYPE_CHOICES)
    depth = JSONField(_('Market Depth'), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        required_db_vendor = 'postgresql'


class MarketTicker(models.Model):
    """
        记录固定时间间隔的市场价格
    """
    market_type = models.PositiveSmallIntegerField(
        _('Market Type'), choices=MARKET_TYPE_CHOICES)
    ticker = JSONField(_('Market Ticker'), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        required_db_vendor = 'postgresql'
