# -*-coding:utf-8-*-
'''
Sending sms via third party gateways.
'''
import sys
import json
import time
import requests
import urllib
import datetime
import functools
import traceback
import uuid
import hashlib
import hmac
import base64
import re
import logging

ALIYUN_api = 'http://dysmsapi.aliyuncs.com'
ALIYUN_SignatureVersion = "1.0"
ALIYUN_Format = "XML"
ALIYUN_Action = "SendSms"
ALIYUN_Version = "2017-05-25"
ALIYUN_RegionId = "cn-hangzhou"
ALIYUN_TemplateCode = "SMS_166776974"
msg_sign = "ETH波动"
ALIYUN_ACCESS_ID = "LTAIYfxArveaM9C6"
ALIYUN_ACCESS_SECRET = "cXg0iumlpoANhyKoPHyf23YqHdgjY0"
logger = logging.getLogger(__name__)


def re_try(times=2, interval=1):

    def wrapper(func):
        @functools.wraps(func)
        def wrap(*arg, **kw):
            for i in range(0, times):
                try:
                    return func(*arg, **kw)
                except Exception as e:
                    print(traceback.format_exc())
                    if isinstance(e, requests.exceptions.RequestException):
                        logger.info({
                            "times": i,
                            "max_times": times,
                            "interval": interval
                        }, category='sms_retry')
                        time.sleep(interval)
                    else:
                        raise e
            else:
                raise Exception("re_try error, raise manually").with_traceback(sys.exc_info()[2])

        return wrap
    return wrapper


def get_smsurl(phone_number, name, code, msgsign):

    paras = {}
    __business_id = uuid.uuid1()
    curtime = datetime.datetime.now()
    time_gmt = curtime - datetime.timedelta(hours = 8)

    paras["SignatureMethod"] = "HMAC-SHA1"
    paras["SignatureNonce"] = str(__business_id)
    paras["AccessKeyId"] = ALIYUN_ACCESS_ID
    paras["SignatureVersion"] = ALIYUN_SignatureVersion
    paras["Timestamp"] = time_gmt.strftime("%Y-%m-%dT%H:%M:%SZ")
    paras["Format"] = ALIYUN_Format

    paras["Action"] = ALIYUN_Action
    paras["Version"] = ALIYUN_Version
    paras["RegionId"] = ALIYUN_RegionId
    paras["PhoneNumbers"] = phone_number
    paras["SignName"] = msgsign
    paras["TemplateParam"] = "{\"name\":\"" + name + "\",\"code\":\"" + code + "\"}"
    paras["TemplateCode"] = ALIYUN_TemplateCode
    paras_list = sorted(paras.items(), key=lambda x: x[0])

    def specialUrlEncode(stra):
        stra_encoded = urllib.parse.quote(stra)
        return stra_encoded.replace("+", "%20").replace("*", "%2A").replace("%7E", "~").replace("/", "%2F")

    def get_sign_string(source, secret):
        h = hmac.new(secret.encode(), source.encode(), hashlib.sha1)
        return base64.b64encode(h.digest()).strip()

    sortQueryStringTmp = ''
    for k, v in paras_list:
        strtmp = '&' + specialUrlEncode(k) + '=' + specialUrlEncode(str(v))
        sortQueryStringTmp += strtmp

    sortQueryString = sortQueryStringTmp[1:]
    stringToSign = 'GET' + '&' + specialUrlEncode('/') + '&' + specialUrlEncode(sortQueryString)
    sign = get_sign_string(stringToSign, ALIYUN_ACCESS_SECRET + "&")
    signature = specialUrlEncode(sign)
    geturl = ALIYUN_api + '/?Signature=' + signature + '&' + sortQueryString
    return geturl


@re_try(times=2, interval=1)
def aliyun_send(phone_number, name, code, source=msg_sign):
    smsurl = get_smsurl(phone_number, name, code, source)
    resg = requests.get(smsurl, timeout=30)
    if resg.status_code == 200:
        regok = r'<Code>(.*?)</Code>'
        okobj = re.search(regok, resg.text)
        logger.info("send aliyun sms: %s", json.dumps({
            'phone_number': phone_number,
            'msgcode': code,
            'time': str(datetime.datetime.now()),
            'result': resg.text}))
        print(resg.text)
        if okobj and okobj.group(1) == "OK":
            return True
        return False
    return False


if __name__ == '__main__':
    ret = aliyun_send("17701225865", "上涨", "252")
    print(ret)
