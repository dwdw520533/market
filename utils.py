# -*-coding:utf-8 -*-
import six
import time
import datetime
import calendar


def to_local_format(time):
    return time.strftime(u'%Y年%m月%d日 %H:%M:%S')


def increase_day(day, source=None):
    '''
    根据给定的source date, 获得增加一定天数的时间
    '''
    source = source if source else datetime.datetime.now()
    return source + datetime.timedelta(days=day)


def increase_month(month, source=None):
    '''
    根据给定的source date, 获得增加一定月份的时间
    '''
    source = source if source else datetime.datetime.now()
    _m = source.month - 1 + month
    _y = source.year + int(_m // 12)
    _m = _m % 12 + 1
    _d = min(source.day, calendar.monthrange(_y, _m)[1])
    return type(source)(_y, _m, _d)


def increase_year(year, source=None):
    '''
    根据给定的source date, 获得增加一定天数的时间
    '''
    source = source if source else datetime.datetime.now()
    _y = source.year + year
    _m = source.month
    _d = min(source.day, calendar.monthrange(_y, source.month)[1])
    return type(source)(_y, _m, _d)


def increase_hour(hour, source=None):
    '''
    根据给定的source date, 获得增加一定小时的时间
    '''
    source = source if source else datetime.datetime.now()
    return source + datetime.timedelta(hours=hour)


def increase_period(period, source=None):
    '''
    根据给定的source date, 获得增加一定月份的时间
    '''
    if not period:
        return source

    if period.endswith('y'):
        _year = int(period.split('y')[0])
        return increase_year(_year, source)
    elif period.endswith('m'):
        _month = int(period.split('m')[0])
        return increase_month(_month, source)
    elif period.endswith('d'):
        _day = int(period.split('d')[0])
        return increase_day(_day, source)
    elif period.endswith('h'):
        _h = int(period.split('h')[0])
        return increase_hour(_h, source)
    else:
        return source


def format_seconds(sec):
    '''
    Convert seconds to "HH:MM:SS" format representation.
    '''
    sec = int(sec)
    hours = int(sec // 3600)
    minutes = int(sec % 3600 / 60)
    seconds = sec % 60
    return '%02d:%02d:%02d' % (hours, minutes, seconds)


def utc_to_local(utc_dt):
    '''
    Convert utc datetime object to local datetime object.
    '''
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.datetime.fromtimestamp(timestamp)
    return local_dt


def utc_to_timestamp(utc_dt):
    timestamp = calendar.timegm(utc_dt.timetuple())
    return timestamp


def strptime(str_dtime, time_format='%Y-%m-%d %H:%M:%S'):
    '''
    字符串转化为 datetime for < 2.6
    @str_dtime: 字符串格式的时间
    @time_format: 时间格式串
    return: datetime.datetime
    '''
    time_stamp = time.mktime(time.strptime(str_dtime, time_format))
    return datetime.datetime.fromtimestamp(time_stamp)


def strftime(date_time, time_format='%Y-%m-%d %H:%M:%S'):
    """
    格式化时间
    @date_time: 时间对象
    @time_format: 时间格式串
    return: 字符串时间
    """
    return datetime.datetime.strftime(date_time, time_format)


def time_delta(date_time, days=0, hours=0, seconds=0, time_format='%Y-%m-%d %H:%M:%S'):
    """
    给指定时间加上增量
    @date_time: datetime.datetime对象
    @days: 天数
    @hours: 小时
    @seconds: 秒
    return: 加上增量后的时间对象
    """
    if isinstance(date_time, six.string_types):
        date_time = datetime.datetime.strptime(date_time, time_format)
    return date_time + datetime.timedelta(days=days, hours=hours, seconds=seconds)


def time_stamp(date_time, days=0, hours=0, seconds=0, time_format='%Y-%m-%d %H:%M:%S'):
    """
    计算指定时间加上增量之后的时间戳
    @date_time: datetime.datetime对象
    @days: 天数
    @hours: 小时
    @seconds: 秒
    return: 加上增量后的时间戳字符串
    """
    if not date_time:
        return None
    if isinstance(date_time, six.string_types):
        date_time = datetime.datetime.strptime(date_time, time_format)
    date_time = time_delta(date_time, days, hours, seconds, time_format)
    return int(time.mktime(date_time.timetuple()) * 1000)


def date_stamp(date_time, days=0, time_format='%Y-%m-%d'):
    """
    计算指定日期加上增量之后的时间戳
    @date_time: datetime.datetime对象
    @days: 天数
    @hours: 小时
    @seconds: 秒
    return: 加上增量后的时间戳字符串
    """
    if not date_time:
        return None
    if isinstance(date_time, six.string_types):
        date_time = datetime.datetime.strptime(date_time, time_format)
    date_time = time_delta(date_time, days=days, time_format=time_format)
    return int(time.mktime(date_time.timetuple()) * 1000)


def timestamp_delta(timestamp, days=0, hours=0):
    """
    给指定时间戳加上增量
    @timestamp: 时间戳
    @days: 天数
    @hours: 小时
    return: 加上增量后的时间戳字符串
    """
    if isinstance(timestamp, six.string_types):
        timestamp = int(timestamp)
    return int((timestamp + days * 24 * 3600 + hours * 3600) * 1000)


def format_timestamp(timestamp, scale=1000, date_format='%Y-%m-%d %H:%M:%S', to_str=True):
    """
    format_timestamp to date time.
    """
    if not timestamp:
        return None
    if isinstance(timestamp, six.string_types):
        timestamp = int(timestamp)
    if to_str:
        return datetime.datetime.fromtimestamp(timestamp / scale).strftime(date_format)
    else:
        return datetime.datetime.fromtimestamp(timestamp / scale)


# 根据恒生返回的日期字符串和时间字符串获取毫秒级时间戳
def get_stamp_from_hs_date_and_time(sdate, stime):
    format_str = '%Y%m%d%H%M%S'
    s = sdate + stime
    return int(time.mktime(time.strptime(s, format_str)) * 1000)


def get_next_deposit(next_deposit, month=0):
    now = datetime.datetime.now()
    next_month = datetime.datetime(now.year, now.month, next_deposit)
    next_month = increase_month(month, source=next_month)
    if next_deposit <= datetime.datetime.now().day:
        next_month = increase_month(1, source=next_month)
    return date_stamp(next_month)


def convert_date(date_str):
    date_str = str(date_str)
    return "%s-%s-%s" % (date_str[:4], date_str[4:6], date_str[-2:])


def convert_timestamp(time_stamp, date_format="%Y-%m-%d"):
    return strftime(strptime(format_timestamp(time_stamp)), date_format)


# 将日期转换时间戳
def date_to_stamp(dt):
    if dt:
        s = time.mktime((dt.year, dt.month, dt.day,
                         dt.hour, dt.minute, dt.second,
                         0, 0, 0))
        return int(s * 1000)


# 时间戳转换字符串
def stamp_to_str(s):
    t = time.localtime(s)
    return time.strftime('%Y-%m-%d 00:00:00', t)


def format_income_date(income_date):
    return convert_date(income_date)[-5:] if income_date else ""


# 既不是月初三天、也不是月末三天
def neither_sides_3day_of_month(td=None):
    if not isinstance(td, datetime.datetime):
        td = datetime.datetime.now()
    bd = td + datetime.timedelta(-3)
    ad = td + datetime.timedelta(3)
    return td.month == bd.month == ad.month
