# -*- coding: utf-8 -*-
import gzip
import time
import conf
import json
import datetime
import requests
import functools
from cache_util import cache
from websocket import create_connection
from sms import aliyun_send

phone = '17701225865'
send_key = '12431-0355c73a8b4ddbf191cce09acdccbfbc'


def write_log(message):
    print('%s: %s' % (datetime.datetime.now(), message))


def time_lock(func):
    @functools.wraps(func)
    def wrapper(*sub, **kw):
        interval = getattr(conf, 'NOTIFY_INTERVAL', 300)
        lock_state = cache.add(func.__name__, 'time_lock', interval)
        if not lock_state:
            return None
        return func(*sub, **kw)
    return wrapper


@time_lock
def send_notify(action, price):
    text = 'ETH已%s至指定价格%s，请及时关注。' % (action, price)
    notify_url = f'https://pushbear.ftqq.com/sub?sendkey={send_key}&text={text}'
    write_log('#notify: %s' % notify_url)
    requests.get(notify_url)
    aliyun_send(phone, action, str(price))


def check_eth_price(price):

    def _check_min_value(value):
        if price <= float(value):
            send_notify('下跌', price)

    def _check_max_value(value):
        if price >= float(value):
            send_notify('上涨', price)
    try:
        list(map(_check_min_value, str(conf.MIN_VALUE).split('|')))
        list(map(_check_max_value, str(conf.MAX_VALUE).split('|')))
    except Exception as ex:
        write_log(ex)


if __name__ == '__main__':
    while True:
        try:
            ws = create_connection("wss://api.huobi.pro/ws")
            break
        except:
            write_log('connect ws error,retry...')
            time.sleep(5)

    # 订阅 KLine 数据
    tradeStr = """{"sub": "market.ethusdt.kline.1min","id": "id10"}"""

    ws.send(tradeStr)
    while True:
        try:
            compressData = ws.recv()
            result = gzip.decompress(compressData).decode('utf-8')
            if result[:7] == '{"ping"':
                ts = result[8:21]
                pong = '{"pong":'+ts+'}'
                ws.send(pong)
                ws.send(tradeStr)
            else:
                data = json.loads(result)
                if 'tick' in data:
                    write_log(data)
                    check_eth_price(float(data['tick']['close']))
        except Exception:
            time.sleep(5)
