# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals

import sys

# 基本api
from gmdata import __version__
from gmdata.csdk.c_sdk import py_gmi_set_version, BarLikeDict2, TickLikeDict2, QuoteItemLikeDict2
from gmdata.enum import *
from gmdata.model.storage import Context
from .basic import set_token, get_version, subscribe, unsubscribe, current, get_strerror, start, set_endpoint, stop
# 数据查询api
from gmdata.api.query import (
    history_n, history, get_fundamentals, get_dividend, get_continuous_contracts, get_next_trading_date,
    get_previous_trading_date, get_trading_dates, get_concept, get_industry, get_constituents, get_history_constituents,
    get_history_instruments, get_instrumentinfos, get_instruments, get_fundamentals_n
)
from gmdata.utils import gmdatalogger

__all__ = [
    'BarLikeDict2', 'TickLikeDict2', 'QuoteItemLikeDict2',

    'set_token', 'get_version', 'subscribe', 'unsubscribe', 'current', 'get_strerror', 'start', 'stop',

    'history_n', 'history', 'get_fundamentals', 'get_dividend', 'get_continuous_contracts', 'get_next_trading_date',
    'get_previous_trading_date', 'get_trading_dates', 'get_concept', 'get_industry', 'get_constituents',
    'get_history_constituents', 'get_history_instruments', 'get_instrumentinfos', 'get_fundamentals_n',
    'get_instruments', 'set_endpoint',

    'Context', 'gmdatalogger',

    'ADJUST_NONE',
    'ADJUST_PREV',
    'ADJUST_POST',
    'SEC_TYPE_STOCK',
    'SEC_TYPE_FUND',
    'SEC_TYPE_INDEX',
    'SEC_TYPE_FUTURE',
    'SEC_TYPE_OPTION',
    'SEC_TYPE_CONFUTURE',
]

try:
    if sys.version_info.major < 3:
        __all__ = [str(item) for item in __all__]
    ver_info = sys.version_info
    sdk_lang = "python{}.{}".format(ver_info.major, ver_info.minor)
    sdk_version = __version__.__version__

    py_gmi_set_version(sdk_version, sdk_lang)
except BaseException as e:
    pass
