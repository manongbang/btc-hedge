# coding: utf-8
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    MarketTickerList, MarketDepthList,
)

api_urlpatterns = [
    url(
        r'^ticker/list/$',
        MarketTickerList.as_view(),
        name='api_market_ticker_list'
    ),
    url(
        r'^depth/list/$',
        MarketDepthList.as_view(),
        name='api_market_depth_list'
    ),
]

versioned_api_urlpatterns = [
    url(
        r'^api/v1/',
        include(api_urlpatterns, namespace='market_v1')
    ),
]

urlpatterns = format_suffix_patterns(
    versioned_api_urlpatterns, allowed=['json']
)
