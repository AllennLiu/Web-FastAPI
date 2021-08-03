#!/usr/bin/python3
# -*- coding: utf-8 -*-

from re import search
from datetime import datetime
from time import mktime, strftime
from calendar import monthcalendar
from datetime import date as getDate
from argparse import ArgumentParser, RawTextHelpFormatter

def datetimer(text='', ts=True,
              date=False, weekday=False,
              fmt='%Y-%m-%dT%H:%M:%S'):
    ret = ''
    if weekday:
        return datetime.strptime(text, fmt).strftime('%A')
    if ts:
        ret = mktime(
            datetime.strptime(text, "%Y-%m-%dT%H:%M:%S").timetuple()
        ) + (3600 * 8)
    elif date:
        ret = datetime.utcfromtimestamp(
            float(text) + (3600 * 8)
        ).strftime(fmt)
    return str(ret)

def dateAutocomplete(date):
    if search(r'T(\d{2}\:){2}\d{2}', date):
        return date
    return date + 'T00:00:00'

def dateSlice(date='', part=1, slice_char='-'):
    if slice_char not in date:
        return '0/0'
    return '/'.join(str(int(s)) for s in date.split(slice_char)[part:])

def dateDayRemains(start, end):
    return int((float(end) - float(start)) / 86400)

def dateAttenuator(date='', type='increase',
                   days=0, skip_holiday=True):
    """
    Date attenuator to increase/decrease sepcified
    days on it, then return it without any holiday
    or weekend.
    """
    types = ['increase', 'decrease']
    weekend = ['Saturday', 'Sunday']
    if not date or type not in types:
        return ''
    yyyy = int(date.split('-')[0])
    holidays = getCalendarHoliday(yyyy, detail=False)
    limit = 365
    ds = 86400
    dt = dateAutocomplete(date)
    ts = float(datetimer(dt))
    for buffer in range(limit):
        if type == types[0]:
            ts = ts + float(86400 * (days + buffer))
        elif type == types[1]:
            ts = ts - float(86400 * (days - buffer))
        dt = datetimer(str(ts), ts=False, date=True)
        weekday = datetimer(dt, weekday=True)
        if holidays:
            if dt.split('T')[0] not in holidays:
                break
        else:
            if weekday not in weekend:
                break
        if not skip_holiday:
            break
    return datetimer(str(int(ts)), ts=False, date=True)

def getCalendarHoliday(yyyy, detail=True):
    """
    This function is based on external PyPi module
    'chinesecalendar' (need to upgrade anytime).
    If the module not support further, means nobody
    create new calendar on it, then it will not be
    imported this function, finally return empty list.
    """
    holiday_map = {0: "on_holiday", 1: "holiday_name"}

    # check module has been installed
    try:
        __import__('chinese_calendar')
        from chinese_calendar import get_holiday_detail
    except ImportError:
        return []

    # check current year is available and implement
    # *[s for s in string] <- [*] pass list to function arguments
    try:
        current_dates = strftime('%Y %m %d').split()
        tmp = get_holiday_detail(getDate(*[int(s) for s in current_dates]))
    except NotImplementedError:
        return []

    # return full year holiday within 365 days
    return [
        (
            {
                "date": a[1]["date"],
                "holiday_name": (
                    a[1]["holiday_name"]
                    if a[1]["holiday_name"] else
                    datetime.strptime(a[1]["date"], '%Y-%m-%d').strftime('%A')
                )
            }
            if detail else a[1]["date"]
        )
        for a in [
            [
                {holiday_map[x]: e, "date": d}
                for x, e in enumerate(get_holiday_detail(
                    getDate(*[int(s) for s in d.split('-')])
                ))
            ] for d in sorted([
                y for x in [
                    list(set(['-'.join([str(yyyy),
                                        str(k).zfill(2),
                                        str(j).zfill(2)])
                    for i in monthcalendar(yyyy, k) for j in i if j != 0]))
                    for k in range(1, 13)
                ] for y in x
            ])
        ] if a[0]["on_holiday"]
    ]

def timeConvertor(d='', is_timestamp=True):
    if not search(r'^\d{4}\-\d{2}\-\d{2}', d):
        return 0
    date = search(r'^\d{4}\-\d{2}\-\d{2}', d).group(0)
    time = search(r'(\d{2}\:){2}\d{2}', d).group(0)
    ts = int(mktime(datetime.strptime(date, "%Y-%m-%d").timetuple()))
    days = int((int(strftime('%s')) - ts) / 60 / 60 / 24)
    if is_timestamp:
        return date, ts, days
    else:
        return date, time, days

if __name__ == '__main__':

    # parser arguments
    parser = ArgumentParser(description='Public common function.',
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('--d2t',
                        action='store_true',
                        help='convert datetime to timestamps')
    parser.add_argument('--t2d',
                        action='store_true',
                        help='convert timestamps to datetime')
    parser.add_argument('-d', '--datetime',
                        action='store', type=str,
                        default=strftime('%Y-%m-%dT%H:%M:%S'),
                        help='set datetime' + 
                             '\n(default: %(default)s)')
    parser.add_argument('-t', '--timestamps',
                        action='store', type=float,
                        default=float(strftime('%s') + '.0'),
                        help='set datetime' + 
                             '\n(default: %(default)s)')
    args = parser.parse_args()
    d2t = args.d2t
    t2d = args.t2d
    dt = args.datetime
    tts = args.timestamps

    if d2t:
        print(datetimer(text=dt))
    elif t2d:
        print(datetimer(text=tts, ts=False, date=True))

