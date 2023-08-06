# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals

import collections
import os
import sys
from datetime import date as Date, datetime as Datetime
from importlib import import_module

import six
from typing import Text, List, NoReturn, Any, Union

from gmdata.__version__ import __version__
from gmdata.callback import callback_controller
from gmdata.constant import DATA_TYPE_TICK
from gmdata.csdk.c_sdk import py_gmi_current, py_gmi_set_data_callback, py_gmi_subscribe, py_gmi_set_token, \
    py_gmi_unsubscribe, py_gmi_strerror, py_gmi_set_serv_addr, c_status_fail, py_gmi_start, py_gmi_get_c_version
from gmdata.model.storage import ctx, BarSubInfo, BarWaitgroupInfo
from gmdata.pb.data_pb2 import Ticks
from gmdata.pb_to_dict import protobuf_to_dict
from gmdata.utils import load_to_list, load_to_second, adjust_frequency, GmSymbols, gmdatalogger

GmDate = Union[Text, Datetime, Date]  # 自定义gm里可表示时间的类型
TextNone = Union[Text, None]  # 可表示str或者None类型

running = True


def _unsubscribe_all():
    ctx.bar_sub_infos.clear()
    ctx.tick_sub_symbols.clear()
    ctx.bar_waitgroup_frequency2Info.clear()
    ctx.bar_data_cache.clear()
    ctx.tick_data_cache.clear()
    ctx.max_tick_data_count = 1
    ctx.max_bar_data_count = 1


def set_token(token):
    # type: (Text) ->NoReturn
    """
    设置用户的token，用于身份认证
    """
    py_gmi_set_token(token)
    ctx.token = str('bearer {}'.format(token))


def get_version():
    # type: () ->Text
    return __version__


def subscribe(symbols, frequency='1d', count=1, wait_group=False, wait_group_timeout='10s', unsubscribe_previous=False):
    # type:(GmSymbols, Text, int, bool, Text, bool) ->NoReturn
    """
    订阅行情，可以指定symbol， 数据滑窗大小，以及是否需要等待全部代码的数据到齐再触发事件。
    wait_group: 是否等待全部相同频度订阅的symbol到齐再触发on_bar事件。
    一个 frequency, 只能有一个 wait_group_timeout 也就是说如果后面调用该函数时, 相同的frequency, 但是 wait_group_timeout 不同,
    则 wait_group_timeout 被忽略.
    同时要注意, 一个symbol与frequency组合, 只能有一种wait_group, 即wait_group要么为true, 要么为false
    """
    frequency = adjust_frequency(frequency)

    symbols = load_to_list(symbols)
    symbols_str = ','.join(symbols)
    status = py_gmi_subscribe(symbols_str, frequency, unsubscribe_previous)
    if c_status_fail(status, 'py_gmi_subscribe'):
        return

    if unsubscribe_previous:
        _unsubscribe_all()

    if frequency == DATA_TYPE_TICK:
        if ctx.max_tick_data_count < count:
            ctx.max_tick_data_count = count
        for sy in symbols:
            ctx.tick_data_cache[sy] = collections.deque(maxlen=count)
            ctx.tick_sub_symbols.add(sy)
        return

    # 处理订阅bar的情况
    ctx._set_onbar_waitgroup_timeout_check()
    wait_group_timeoutint = load_to_second(wait_group_timeout)
    if ctx.max_bar_data_count < count:
        ctx.max_bar_data_count = count
    for sy in symbols:
        ctx.bar_data_cache["{}_{}".format(sy, frequency)] = collections.deque(maxlen=count)
        barsubinfo = BarSubInfo(sy, frequency)
        if barsubinfo not in ctx.bar_sub_infos:
            ctx.bar_sub_infos.add(barsubinfo)
            if wait_group:
                if frequency not in ctx.bar_waitgroup_frequency2Info:
                    ctx.bar_waitgroup_frequency2Info[frequency] = BarWaitgroupInfo(frequency, wait_group_timeoutint)
                ctx.bar_waitgroup_frequency2Info[frequency].add_one_symbol(sy)
        else:
            gmdatalogger.debug("symbol=%s frequency=%s 已订阅过", sy, frequency)
            continue


def unsubscribe(symbols, frequency='1d'):
    # type: (GmSymbols, Text) ->NoReturn
    """
    unsubscribe - 取消行情订阅

    取消行情订阅，默认取消所有已订阅行情
    """
    symbols = load_to_list(symbols)
    symbols_str = ','.join(symbols)
    frequency = adjust_frequency(frequency)

    status = py_gmi_unsubscribe(symbols_str, frequency)
    if c_status_fail(status, 'py_gmi_unsubscribe'):
        return

    if symbols_str == '*':
        _unsubscribe_all()
        return

    if frequency == DATA_TYPE_TICK:
        for sy in symbols:
            if sy in list(six.iterkeys(ctx.tick_data_cache)):
                del ctx.tick_data_cache[sy]
                ctx.tick_sub_symbols.remove(sy)
        return

    # 处理bar的退订
    for sy in symbols:
        k = sy + "_" + frequency
        if k in list(six.iterkeys(ctx.bar_data_cache)):
            del ctx.bar_data_cache[k]
            ctx.bar_sub_infos.remove(BarSubInfo(sy, frequency))
            barwaitgroupinfo = ctx.bar_waitgroup_frequency2Info.get(frequency, None)
            if barwaitgroupinfo:
                barwaitgroupinfo.remove_one_symbol(sy)

    # 处理已全部退订的 frequency
    for frequency in list(six.iterkeys(ctx.bar_waitgroup_frequency2Info)):
        if len(ctx.bar_waitgroup_frequency2Info[frequency]) == 0:
            gmdatalogger.debug('frequency=%s 已全部取消订阅', frequency)
            del ctx.bar_waitgroup_frequency2Info[frequency]


def current(symbols, fields=''):
    # type: (GmSymbols, Text) -> List[Any]
    """
    查询当前行情快照，返回tick数据
    """
    symbols = load_to_list(symbols)
    fields = load_to_list(fields)

    symbols_str = ','.join(symbols)
    fields_str = ','.join(fields)

    ticks = Ticks()
    status, data = py_gmi_current(symbols_str, fields_str)
    if c_status_fail(status, 'py_gmi_current'):
        return []

    ticks.ParseFromString(data)
    ticks = [protobuf_to_dict(tick, including_default_value_fields=False) for tick in ticks.data]
    if not fields:
        return ticks

    return ticks


def get_strerror(error_code):
    # type: (int) -> Text
    return py_gmi_strerror(error_code)


def _all_not_none(a, b):
    # type: (Any, Any) -> bool
    """
    全部都不为None
    """
    return a is not None and b is not None


def start(filename=None, token=None, endpoint=None):
    # type: (TextNone, TextNone, TextNone) -> int
    """
    启动eventloop，接收数据事件并触发回调函数. 返回int值, 0表示成功, 非0为失败
    """

    # 处理用户传入 __file__这个特殊变量的情况
    syspathes = set(s.replace('\\', '/') for s in sys.path)
    commonpaths = [os.path.commonprefix([p, filename]) for p in syspathes]
    commonpaths.sort(key=lambda s: len(s), reverse=True)
    maxcommonpath = commonpaths[0]
    filename = filename.replace(maxcommonpath, '')  # type: str
    if filename.startswith('/'):
        filename = filename[1:]

    if filename.endswith(".py"):
        filename = filename[:-3]
    filename = filename.replace("/", ".")
    filename = filename.replace('\\', ".")
    fmodule = import_module(filename)

    # 把gmtrade.api里的所有的符号都导出到当前文件(fmodule)的命令空间, 方便使用
    from gmdata import api
    for name in api.__all__:
        if name not in fmodule.__dict__:
            fmodule.__dict__[name] = getattr(api, name)

    if token:
        set_token(token)
    if endpoint:
        set_endpoint(endpoint)

    # 调用户文件的init
    ctx.inside_file_module = fmodule
    ctx.on_tick_fun = getattr(fmodule, 'on_tick', None)
    ctx.on_bar_fun = getattr(fmodule, 'on_bar', None)

    ctx.on_error_fun = getattr(fmodule, 'on_error', None)
    ctx.on_shutdown_fun = getattr(fmodule, 'on_shutdown', None)
    ctx.on_market_data_connected_fun = getattr(fmodule, 'on_market_data_connected', None)
    ctx.on_market_data_disconnected_fun = getattr(fmodule, 'on_market_data_disconnected', None)

    py_gmi_set_data_callback(callback_controller)  # 设置事件处理的回调函数

    splash_msgs = [
        '-' * 40,
        'python gmdata-sdk version: {}'.format(__version__),
        'c_sdk version: {}'.format(py_gmi_get_c_version()),
        '-' * 40,
    ]

    print(os.linesep.join(splash_msgs))
    global running
    status = py_gmi_start()  # type: int
    if c_status_fail(status, 'gmi_start'):
        running = False
        return status
    else:
        running = True
    return status


def stop():
    """
    停止eventloop，不再接收数据事件
    """
    global running
    running = False
    sys.exit(2)


def set_endpoint(addr):
    # type: (Text) -> NoReturn
    """
    设置终端服务地址
    """
    py_gmi_set_serv_addr(addr)
