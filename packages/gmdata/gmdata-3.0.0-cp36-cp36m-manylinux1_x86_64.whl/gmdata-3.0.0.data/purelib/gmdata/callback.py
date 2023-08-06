# coding=utf-8
"""
回调任务分发
"""
from __future__ import unicode_literals, print_function, absolute_import

import collections
import datetime
import time

import six
from typing import Any, Dict, Text, List, Set, NoReturn

from gmdata.constant import CALLBACK_TYPE_TICK, CALLBACK_TYPE_BAR, CALLBACK_TYPE_ERROR, \
    CALLBACK_TYPE_TIMER, CALLBACK_TYPE_STOP, CALLBACK_TYPE_DATA_CONNECTED, CALLBACK_TYPE_DATA_DISCONNECTED
from gmdata.csdk.c_sdk import TickLikeDict2, BarLikeDict2
from gmdata.model.storage import Context, ctx, BarWaitgroupInfo, BarSubInfo
from gmdata.pb.data_pb2 import Quote, Tick, Bar
from gmdata.utils import gmdatalogger, protobuf_timestamp2bj_datetime


def tick_callback_new(data):
    tick = Tick()
    tick.ParseFromString(data)
    quotes = []
    for q in tick.quotes:  # type: Quote
        quotes.append({
            'bid_p': q.bid_p,
            'bid_v': q.bid_v,
            'ask_p': q.ask_p,
            'ask_v': q.ask_v,
        })

    if len(quotes) < 5:
        for _ in range(len(quotes), 5):
            zero_val = {'bid_p': 0, 'bid_v': 0, 'ask_p': 0, 'ask_v': 0}
            quotes.append(zero_val)

    ticknew = {
        'quotes': quotes,
        'symbol': tick.symbol,
        'created_at': protobuf_timestamp2bj_datetime(tick.created_at),
        'price': tick.price,
        'open': tick.open,
        'high': tick.high,
        'low': tick.low,
        'cum_volume': tick.cum_volume,
        'cum_amount': tick.cum_amount,
        'cum_position': tick.cum_position,
        'last_amount': tick.last_amount,
        'last_volume': tick.last_volume,
        'trade_type': tick.trade_type,
        'receive_local_time': time.time(),  # 收到时的本地时间秒数
    }
    ticknn = TickLikeDict2(ticknew)
    tick_callback(ticknn)


def tick_callback(data):
    tick = data  # type: TickLikeDict2
    symbol = tick['symbol']
    if symbol not in ctx.tick_sub_symbols:
        gmdatalogger.debug("tick data symbol=%s 不在订阅列表里, 跳过不处理", symbol)
        return

    if symbol not in ctx.tick_data_cache:
        gmdatalogger.debug("tick data's symbol= %s 在ctx.tick_data_cache key不存在, 加个key, deque长度为:%d", symbol,
                           ctx.max_tick_data_count)
        ctx.tick_data_cache[symbol] = collections.deque(maxlen=ctx.max_tick_data_count)

    ctx.tick_data_cache[symbol].appendleft(tick)
    if ctx.on_tick_fun is not None:
        ctx.on_tick_fun(tick)


# 实时模式且wait_group下的bar集合  以 frequency 作为 一级key, eob做为二级key
bars_in_waitgroup_live = dict()  # type:  Dict[Text, Dict[datetime.datetime, List[BarLikeDict2]]]


def bar_callback_new(data):
    bar = Bar()
    bar.ParseFromString(data)
    barnew = {
        'symbol': bar.symbol,
        'eob': protobuf_timestamp2bj_datetime(bar.eob),
        'bob': protobuf_timestamp2bj_datetime(bar.bob),
        'open': bar.open,
        'close': bar.close,
        'high': bar.high,
        'low': bar.low,
        'volume': bar.volume,
        'amount': bar.amount,
        'pre_close': bar.pre_close,
        'position': bar.position,
        'frequency': bar.frequency,
        'receive_local_time': time.time(),  # 收到时的本地时间秒数
    }
    barnn = BarLikeDict2(barnew)
    bar_callback(barnn)


def bar_callback(data):
    global bars_in_waitgroup_live
    bar = data  # type: BarLikeDict2
    symbol, frequency = bar['symbol'], bar['frequency']  # type: Text, Text
    if BarSubInfo(symbol, frequency) not in ctx.bar_sub_infos:
        gmdatalogger.debug("bar data symbol=%s frequency=%s 不在订阅列表里, 跳过不处理", symbol, frequency)
        return

    k = symbol + "_" + frequency
    # wait_group = True的情况下, 就先不要放入, 不然第一个symbol得到的数据跟别的symbol的数据对不齐
    if not ctx.has_wait_group:
        ctx.bar_data_cache[k].appendleft(bar)

    if ctx.on_bar_fun is None:
        return

    # 没有wait_group的情况, 那就直接发了
    if not ctx.has_wait_group:
        ctx.on_bar_fun([bar, ])
        return

    # wait_group = True, 但是股票不在waitgroup的列表里时, 直接发了.
    # 在调用完 on_bar_fun 后, 在把数据放入到bar_data_cache里
    barwaitgroupinfo = ctx.bar_waitgroup_frequency2Info.get(frequency, BarWaitgroupInfo(frequency, 0))
    if not barwaitgroupinfo.is_symbol_in(symbol):
        gmdatalogger.debug('wait_group = True, 但是股票不在waitgroup的列表里时, 直接发了, symbol=%s, frequency=%s', symbol, frequency)
        ctx.on_bar_fun([bar, ])
        ctx._add_bar2bar_data_cache(k, bar)
        return

    eob = bar['eob']  # type: datetime.datetime

    if frequency not in bars_in_waitgroup_live:
        bars_in_waitgroup_live[frequency] = dict()

    # 以eob做为key值, bar做为value值. 二级dict
    eob_bar_dict = bars_in_waitgroup_live[frequency]  # type: Dict[datetime.datetime, List[BarLikeDict2]]
    if eob not in eob_bar_dict:
        eob_bar_dict[eob] = [bar]
    else:
        eob_bar_dict[eob].append(bar)

    # 检查一下是否全部都到了. 到了的话触发一下
    if len(barwaitgroupinfo) == len(eob_bar_dict[eob]):
        gmdatalogger.debug("实时模式下, wait_group的bar都到齐了, 触发on_bar. eob=%s", eob)
        ctx.on_bar_fun(eob_bar_dict[eob])
        del eob_bar_dict[eob]
        ctx.bar_data_cache[k].appendleft(bar)
    else:
        ctx.bar_data_cache[k].appendleft(bar)

    return


def _or_not_none(a, b):
    # type: (Any, Any) -> bool
    """
    两个中有一个不为None
    """
    return a is not None or b is not None


def default_err_callback(code, info):
    # type: (Text, Text) -> NoReturn
    if code in ('1201', '1200'):
        gmdatalogger.warning(
            '行情重连中..., error code=%s, info=%s. 可用on_error事件处理', code, info
        )
    else:
        gmdatalogger.warning(
            '发生错误, 调用默认的处理函数, error code=%s, info=%s.  你可以在自定义on_error函数接管它. 类似于on_tick',
            code, info
        )


def err_callback(data):
    """
    遇到错误时回调, 错误代码跟错误信息的对应关系参考: https://www.myquant.cn/docs/cpp/170
    """
    if ctx.on_error_fun is None:
        ctx.on_error_fun = default_err_callback

    try:
        data_unicode = data.decode('utf8')
        sparr = data_unicode.split('|', 1)
        if len(sparr) == 1:
            code, info = "code解析不出来", sparr[0]
        else:
            code, info = sparr
        ctx.on_error_fun(code, info)
    except Exception as e:
        gmdatalogger.exception("字符编码解析错误", e)
        ctx.on_error_fun("1011", data)


# 已超时触发过的eob集合, 原则上是触发过的, 即可后面在收到数据也不再次触发
already_fire_timeout_eobs = set()  # type: Set[datetime.datetime]


def timer_callback(data):
    global bars_in_waitgroup_live, already_fire_timeout_eobs
    if (ctx.on_bar_fun is not None) and ctx.has_wait_group:
        # 这里处理实时模式下wait_group=true时, on_bar超时触发
        # 比较逻辑是: 取本地时间, 然后跟相同的eob的bars里的第1个bar的 receive_local_time (接收到时的本地时间) 相比
        cur_now_s = time.time()
        must_del_keys = []
        for frequency, eob_tick_dict in six.iteritems(bars_in_waitgroup_live):
            barwaitgroupinfo = ctx.bar_waitgroup_frequency2Info.get(frequency, None)
            if barwaitgroupinfo is not None:
                timeout_seconds = barwaitgroupinfo.timeout_seconds
                for eob_time in list(six.iterkeys(eob_tick_dict)):
                    first_bar = eob_tick_dict[eob_time][0]  # 这个eob下的收到的第1个bar
                    delta_second = cur_now_s - first_bar['receive_local_time']  # type: float
                    if delta_second >= timeout_seconds:
                        if eob_time in already_fire_timeout_eobs:
                            gmdatalogger.debug(
                                'frequency=%s eob=%s timeout_seconds=%d, 已超时触发过, 后面又收到数据, 不进行触发',
                                frequency, eob_time
                            )
                            del eob_tick_dict[eob_time]
                            continue

                        gmdatalogger.info(
                            "frequency=%s eob=%s timeout_seconds=%d 已超时了超时秒数=%s, 触发on_bar",
                            frequency, eob_time, timeout_seconds, delta_second
                        )
                        ctx.on_bar_fun(eob_tick_dict[eob_time])
                        del eob_tick_dict[eob_time]
                        already_fire_timeout_eobs.add(eob_time)
            else:
                # 说明有些 frequency 已经退订了
                gmdatalogger.debug("frequency =%s 已全部退订", frequency)
                must_del_keys.append(frequency)

        if must_del_keys:
            for k in must_del_keys:
                del bars_in_waitgroup_live[k]
        return


def stop_callback(data):
    if ctx.on_shutdown_fun is not None:
        ctx.on_shutdown_fun()

    from gmdata.api import stop
    print("!~~~~~~~~~~~!停止!~~~~~~~~~~~!")
    stop()


def data_connected_callback():
    gmdatalogger.info("连接行情服务成功")
    if ctx.on_market_data_connected_fun is not None:
        ctx.on_market_data_connected_fun()


def data_disconnected_callback():
    if ctx.on_market_data_disconnected_fun is not None:
        ctx.on_market_data_disconnected_fun()


def callback_controller(msg_type, data):
    """
    回调任务控制器
    """
    try:
        # python 3 传过来的是bytes 类型， 转成str
        if isinstance(msg_type, bytes):
            msg_type = bytes.decode(msg_type)

        if msg_type == CALLBACK_TYPE_TICK:
            return tick_callback_new(data)

        if msg_type == CALLBACK_TYPE_BAR:
            return bar_callback_new(data)

        if msg_type == CALLBACK_TYPE_ERROR:
            return err_callback(data)

        if msg_type == CALLBACK_TYPE_TIMER:
            return timer_callback(data)

        if msg_type == CALLBACK_TYPE_STOP:
            return stop_callback(data)

        if msg_type == CALLBACK_TYPE_DATA_CONNECTED:
            return data_connected_callback()

        if msg_type == CALLBACK_TYPE_DATA_DISCONNECTED:
            return data_disconnected_callback()

        gmdatalogger.warn("没有处理消息:%s的处理函数", msg_type)

    except SystemExit:
        gmdatalogger.debug("^^--------------SystemExit--------------^^")
        from gmdata.api import stop
        stop()

    except BaseException as e:
        gmdatalogger.exception("^^--------------遇到exception--------------^^")
        from gmdata.api import stop
        stop()
