# -*- coding: utf-8 -*-
from websocket import create_connection
import gzip
import time
import conf
import json
import datetime
import requests
import utils

send_key = '12431-0355c73a8b4ddbf191cce09acdccbfbc'


def send_notify(text):
    requests.get(f'https://pushbear.ftqq.com/sub?sendkey={send_key}&text={text}')


def check_min_value(value):
    try:
        now = utils.strftime(datetime.datetime.now())
        if value <= float(conf.MIN_VALUE):
            send_notify('[%s] ETH已下跌至指定价格%s，请及时关注。' % (now, value))
        if value >= float(conf.MAX_VALUE):
            send_notify('[%s] ETH已上涨至指定价格%s，请及时关注。' % (now, value))
    except Exception:
        pass


if __name__ == '__main__':
    while True:
        try:
            ws = create_connection("wss://api.huobi.pro/ws")
            break
        except:
            print('connect ws error,retry...')
            time.sleep(5)

    # 订阅 KLine 数据
    tradeStr = """{"sub": "market.ethusdt.kline.1min","id": "id10"}"""

    ws.send(tradeStr)
    while True:
        compressData = ws.recv()
        result = gzip.decompress(compressData).decode('utf-8')
        if result[:7] == '{"ping"':
            ts = result[8:21]
            pong = '{"pong":'+ts+'}'
            ws.send(pong)
            ws.send(tradeStr)
        else:
            data = json.loads(result)
            print(data)
            check_min_value(float(data['tick']['close']))

