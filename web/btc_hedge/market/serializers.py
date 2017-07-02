# coding: utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from .models import MarketTicker, MarketDepth


class MarketTickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketTicker
        fields = ('market_type', 'ticker' 'created', )


class MarketDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketDepth
        fields = ('market_type', 'depth' 'created', )
