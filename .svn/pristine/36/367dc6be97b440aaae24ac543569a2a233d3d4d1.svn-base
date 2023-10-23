# _*_coding: utf-8 -*-

# 시간을 반환 한다.
# 작성 날짜 : 2022. 7. 29
# 작성자 : 황희정
# 기능
# 	1. 2022. 07. 29 | 현재 시간을 타입별로 반환 한다.
# 변경 이력
# 	1. 2022. 07. 29 | 황희정 | 최조 작성

# system import
from datetime import datetime
import time

# define
TIME_CURRENT_TYPE_DEFAULT = 1
TIME_CURRENT_TYPE_MILLISECOND = 2
TIME_CURRENT_TYPE_14 = 3


# 1. 현재 시간을 타입별로 반환 한다.
#
# Parameter
#   - time_type | Integer | 반환 시간 값 Type
#
# return
#   - 현재 시간
def get_current_time(time_type):
    if time_type == TIME_CURRENT_TYPE_DEFAULT:
        date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    elif time_type == TIME_CURRENT_TYPE_MILLISECOND:
        date = int(time.time())
    elif time_type == TIME_CURRENT_TYPE_14:
        date = datetime.today().strftime("%Y%m%d%H%M%S")

    return date


def get_weather_date():
    baseDate = ""
    curHour = int(datetime.today().strftime("%H"))
    curMin = int(datetime.today().strftime("%M"))

    if (curHour < 1) and (curMin < 30):
        baseDate = (datetime.today() - timedelta(1)).strftime("%Y%m%d")
    else:
        baseDate = datetime.today().strftime("%Y%m%d")

    return baseDate


def get_weather_ontime():
    baseTime = ""
    curMin = int(datetime.today().strftime("%M"))

    if curMin < 30:
        curHour = int(datetime.today().strftime("%H"))

        if curHour == 0:
            curHour = 23
        else:
            curHour -= 1

        if curHour < 10:
            baseHour = "0" + str(curHour)
        else:
            baseHour = str(curHour)

        baseTime = baseHour + "30"
    else:
        curHour = datetime.today().strftime("%H")
        baseTime = curHour + "00"

    return baseTime
