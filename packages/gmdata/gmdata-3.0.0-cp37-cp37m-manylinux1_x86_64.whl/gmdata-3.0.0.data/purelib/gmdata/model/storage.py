# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import

import collections
import datetime
import struct
import sys
import sysconfig

from typing import NoReturn, Text, Dict, Any, Set, Sequence, Deque

from gmdata import __version__
from gmdata.csdk.c_sdk import py_gmi_set_timer
from gmdata.utils import gmdatalogger, beijing_tzinfo


class BarSubInfo(object):
    __slots__ = ['symbol', 'frequency']

    def __init__(self, symbol, frequency):
        self.symbol = symbol  # type: Text
        self.frequency = frequency  # type: Text

    def __hash__(self):
        return hash((self.symbol, self.frequency))

    def __eq__(self, other):
        if not isinstance(other, BarSubInfo):
            return False

        return (self.symbol, self.frequency) == (other.symbol, other.frequency)


class BarWaitgroupInfo(object):
    __slots__ = ['symbols', 'frequency', 'timeout_seconds']

    def __init__(self, frequency, timeout_seconds):
        self.symbols = set()  # type: Set[Text]
        self.frequency = frequency  # type: Text
        self.timeout_seconds = timeout_seconds  # type: int

    def add_one_symbol(self, symbol):
        # type: (Text) ->NoReturn
        self.symbols.add(symbol)

    def add_symbols(self, syms):
        # type: (Sequence[Text]) ->NoReturn
        self.symbols.union(syms)

    def remove_one_symbol(self, symbol):
        # type: (Text) ->NoReturn
        self.symbols.discard(symbol)

    def is_symbol_in(self, symbol):
        # type: (Text) -> bool
        return symbol in self.symbols

    def __len__(self):
        return len(self.symbols)


class DefaultFileModule(object):
    def on_tick(self, tick):
        print('请初始化on_tick方法')

    def on_bar(self, bar):
        print('请初始化on_bar方法')

    def on_market_data_connected(self):
        pass

    def on_market_data_disconnected(self):
        pass


class Context(object):
    """
    运行的上下文类. 这在整个进程中要保证是单一实例
    注意: 一个运行的python进程只能运行一个实例.
    警告: 客户写的代码不要直接使用这个类来实例化, 而是使用 sdk 实例化好的 context 实例
    """
    inside_file_module = DefaultFileModule()
    on_bar_fun = None
    on_tick_fun = None
    on_error_fun = None
    on_shutdown_fun = None
    on_market_data_connected_fun = None
    on_market_data_disconnected_fun = None

    token = None  # type: Text

    sdk_lang = "python{}.{}".format(sys.version_info.major, sys.version_info.minor)  # type: Text
    sdk_version = __version__.__version__  # type: Text
    sdk_arch = str(struct.calcsize("P") * 8)  # type: Text
    sdk_os = sysconfig.get_platform()  # type: Text

    tick_data_cache = dict()  # type: Dict[Text, Deque[Any]]
    max_tick_data_count = 1
    bar_data_cache = dict()  # type: Dict[Text, Deque[Any]]  # 以 bar.symbol+bar.frequency作为key
    max_bar_data_count = 1
    bar_data_set = set()  # type: Set  # 保存已有的bar的 (symbol, frequency, eob), 用于判断是否重复值
    tick_sub_symbols = set()  # type: Set[Text]   # 订阅tick的symbol
    bar_sub_infos = set()  # type: Set[BarSubInfo]   # 订阅bar的信息集合
    # 订阅bar用freequency做为key, 相应的股票集合做为value
    bar_waitgroup_frequency2Info = dict()  # type: Dict[Text, BarWaitgroupInfo]

    is_set_onbar_timeout_check = False

    def _set_onbar_waitgroup_timeout_check(self):
        if not self.is_set_onbar_timeout_check:
            # 实时模式下 3000毫秒触发一次timer事件 用来处理wait_group的过期.
            # fixme 这里底层不支持动态设置多个, 先固定一个吧
            py_gmi_set_timer(3000)
            self.is_set_onbar_timeout_check = True

    def _add_bar2bar_data_cache(self, k, bar):
        # type: (Text, Dict[Text, Any]) -> NoReturn
        kk = (bar['symbol'], bar['frequency'], bar['eob'])
        if kk in self.bar_data_set:
            gmdatalogger.debug("bar data %s 已存在, 跳过不加入", kk)
        else:
            if k not in ctx.bar_data_cache:
                gmdatalogger.debug("bar data %s 在context.bar_data_cache相应的key=%s不存在, 加个key, deque长度为:%d", kk, k,
                                   ctx.max_bar_data_count)
                ctx.bar_data_cache[k] = collections.deque(maxlen=ctx.max_bar_data_count)

            ctx.bar_data_cache[k].appendleft(bar)
            self.bar_data_set.add(kk)

    @property
    def has_wait_group(self):
        # type: () ->bool
        return len(self.bar_waitgroup_frequency2Info) > 0

    @property
    def now(self):
        # type: ()->datetime.datetime
        """
        返回当前本地时间
        """
        return datetime.datetime.now().replace(tzinfo=beijing_tzinfo)

    @property
    def symbols(self):
        # type: ()->Set[Text]
        """
        订阅bar跟tick的symbol集合
        bar 的symbols + tick 的symbols
        """
        return set(barsub.symbol for barsub in self.bar_sub_infos).union(self.tick_sub_symbols)


# 提供给API的唯一上下文实例
ctx = Context()
