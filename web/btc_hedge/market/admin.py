from django.contrib import admin

from .models import UserMarketConfig, MarketDepth, MarketTicker


@admin.register(UserMarketConfig)
class UserMarketConfigAdmin(admin.ModelAdmin):
    list_display = (
        'trader', 'market_type', 'created', 'updated',
    )
    list_filter = ('market_type', )
    search_fields = ['trader__username', 'trader__email', ]
    readonly_fields = ('created', 'updated', )


@admin.register(MarketDepth)
class MarketDepthAdmin(admin.ModelAdmin):
    list_display = (
        'market_type', 'created',
    )
    list_filter = ('market_type', )
    readonly_fields = ('created', )


@admin.register(MarketTicker)
class MarketTickerAdmin(admin.ModelAdmin):
    list_display = (
        'market_type', 'created',
    )
    list_filter = ('market_type', )
    readonly_fields = ('created', )
