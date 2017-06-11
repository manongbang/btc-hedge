# coding: utf-8
from __future__ import unicode_literals


class BasePublicMarket(object):
    """
        公开市场接口(用于获取市场数据)
    """

    def ticker(self):
        """获取市场价格(ticker)"""
        raise NotImplemented

    def depth(self):
        """获取市场深度(depth)"""
        raise NotImplemented


class BasePrivateMarket(object):
    """
        私有市场接口(用于账户交易)
    """

    def balance(self):
        """获取账户信息"""
        raise NotImplemented

    def orders(self):
        """获取订单信息"""
        raise NotImplemented

    def buy(self, price, trade_type=None):
        """提交买入单"""
        raise NotImplemented

    def sell(self, price, trade_type=None):
        """提交卖出单"""
        raise NotImplemented
