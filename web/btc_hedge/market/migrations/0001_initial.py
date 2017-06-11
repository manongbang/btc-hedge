# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-11 12:58
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketDepth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market_type', models.PositiveSmallIntegerField(choices=[(1, 'OKCoin'), (2, 'Huobi Coin')], verbose_name='Market Type')),
                ('depth', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Market Depth')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'required_db_vendor': 'postgresql',
            },
        ),
        migrations.CreateModel(
            name='MarketTicker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market_type', models.PositiveSmallIntegerField(choices=[(1, 'OKCoin'), (2, 'Huobi Coin')], verbose_name='Market Type')),
                ('ticker', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Market Ticker')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'required_db_vendor': 'postgresql',
            },
        ),
        migrations.CreateModel(
            name='UserMarketConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market_type', models.PositiveSmallIntegerField(choices=[(1, 'OKCoin'), (2, 'Huobi Coin')], verbose_name='Market Type')),
                ('api_key', models.CharField(max_length=256, verbose_name='API Key')),
                ('api_secret', models.CharField(max_length=512, verbose_name='API Secret')),
                ('context', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Context')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('trader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='market_contexts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'required_db_vendor': 'postgresql',
            },
        ),
    ]