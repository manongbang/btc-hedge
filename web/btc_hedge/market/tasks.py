# coding: utf-8
from __future__ import unicode_literals, absolute_import

from celery import Celery, group
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from .models import MarketTicker, MarketDepth

app = Celery()
logger = get_task_logger(__name__)

DEFAULT_RETRY = 1


@app.task(bind=True)
def market_ticker(self, mc):
    try:
        ticker = mc.market.ticker()
        # save to db
        record = MarketTicker(
            market_type=mc.market_type,
            ticker=ticker,
        )
        record.save()
        logger.debug('[TICKER] Market Type:{mt}'.format(
            mt=mc.market_type))
    except Exception as exc:
        logger.exception('[TICKER] error happened')
        raise self.retry(exc=exc, max_retries=DEFAULT_RETRY)


@app.task(bind=True)
def market_depth(self, mc):
    try:
        depth = mc.market.depth()
        # save to db
        record = MarketDepth(
            market_type=mc.market_type,
            depth=depth,
        )
        record.save()
        logger.debug('[DEPTH] Market Type:{mt}'.format(
            mt=mc.market_type))
    except Exception as exc:
        logger.exception('[DEPTH] error happened')
        raise self.retry(exc=exc, max_retries=DEFAULT_RETRY)


@app.task(bind=True)
def check_all_markets(self):
    # TODO: 目前只通过超级管理员用户的配置来获取市场信息
    # get admin user
    UserModel = get_user_model()
    try:
        superuser = UserModel.objects.get(is_superuser=True)
    except UserModel.DoesNotExist:
        raise Exception('need superuser and market contexts')
    mcs = list(superuser.market_contexts.all())
    assert(mcs)
    group(
        group(market_ticker.s(mc), market_depth.s(mc)) for mc in mcs
    )()
