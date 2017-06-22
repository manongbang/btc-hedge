# coding: utf-8
from __future__ import unicode_literals

from rest_framework import generics
from rest_framework import filters

from .models import MarketDepth, MarketTicker
from .serializers import (
    MarketTickerSerializer, MarketDepthSerializer,
)


class MarketTickerList(generics.ListAPIView):
    queryset = MarketTicker.objects.all()
    serializer_class = MarketTickerSerializer
    filter_backends = (
        filters.DjangoFilterBackend, filters.OrderingFilter,
    )
    filter_fields = ('market_type', 'created', )
    ordering_fields = ('market_type', 'created', )
    ordering = ('created', )
    pagination_class = None


class MarketDepthList(generics.ListAPIView):
    queryset = MarketDepth.objects.all()
    serializer_class = MarketDepthSerializer
    filter_backends = (
        filters.DjangoFilterBackend, filters.OrderingFilter,
    )
    filter_fields = ('market_type', 'created', )
    ordering_fields = ('market_type', 'created', )
    ordering = ('created', )
    pagination_class = None
