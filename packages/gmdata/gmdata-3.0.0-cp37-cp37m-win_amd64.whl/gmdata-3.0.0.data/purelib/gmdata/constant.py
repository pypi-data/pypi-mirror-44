# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import

SUB_ID = 'SUB_ID:{}:{}:{}'  # 订阅股票唯一id  由三部分组成  symbol frequency count
SUB_TAG = 'SUB_TAG:{}:{}'  # 取消订阅股票标签 由两部分组成  symbol frequency

DATA_TYPE_TICK = 'tick'
DATA_TYPE_BAR = 'bar'

"""
c-sdk回调的类型
"""

CALLBACK_TYPE_TICK = 'data.api.Tick'
CALLBACK_TYPE_BAR = 'data.api.Bar'
CALLBACK_TYPE_ERROR = 'error'
CALLBACK_TYPE_TIMER = 'timer'
CALLBACK_TYPE_STOP = 'stop'

CALLBACK_TYPE_DATA_CONNECTED = 'md-connected'
CALLBACK_TYPE_DATA_DISCONNECTED = 'md-disconnected'

TRADE_CONNECTED = 1
DATA_CONNECTED = 2

HISTORY_ADDR = 'ds-history-rpc'
HISTORY_REST_ADDR = 'ds-history-rpcgw'
FUNDAMENTAL_ADDR = 'ds-fundamental-rpc'

CSDK_OPERATE_SUCCESS = 0  # c-sdk 操作成功
