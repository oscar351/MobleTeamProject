# _*_coding: utf-8 -*-

# 로그를 기록 한다.
# 작성 날짜 : 2022. 7. 29
# 작성자 : 황희정
# 기능
# 	1. 2022. 07. 29 | Debug 로그를 기록 한다.
# 	2. 2022. 07. 29 | Info 로그를 기록 한다.
# 	3. 2022. 07. 29 | War 로그를 기록 한다.
# 	4. 2022. 07. 29 | Cri 로그를 기록 한다.
# 변경 이력
# 	1. 2022. 07. 29 | 황희정 | 최조 작성

# system import
import sys
import logging
import inspect

# user import
from common import util_time

# 로그 기록 관리 Class
class logManage:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s: %(levelname)s (%(message)s', stream=sys.stderr)
    # 1. Debug 로그를 기록 한다.
    #
    # Parameter
    # 	- procName | String | 프로세스명
    # 	- className | String | 실행중인 클래스명
    # 	- funcName | String | 실행중인 기능 명
    # 	- content | String | 로그 내용
    def debug(self, procName, className, funcName, content):
        #current_time = util_time.get_current_time(util_time.TIME_CURRENT_TYPE_DEFAULT)
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        log_msg = f"{procName}: DEBUG ({className}) - {caller.function} (line: {caller.lineno}) > {content}"
        logging.debug(log_msg)

    # 2. Info 로그를 기록 한다.
    #
    # Parameter
    # 	- procName | String | 프로세스명
    # 	- className | String | 실행중인 클래스명
    # 	- funcName | String | 실행중인 기능 명
    # 	- content | String | 로그 내용
    def info(self, procName, className, funcName, content):
        #current_time = util_time.get_current_time(util_time.TIME_CURRENT_TYPE_DEFAULT)
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        log_msg = f"{procName}: INFO ({className}) - {caller.function} (line: {caller.lineno}) > {content}"
        logging.info(log_msg)
    # 3. War 로그를 기록 한다.
    #
    # Parameter
    # 	- procName | String | 프로세스명
    # 	- className | String | 실행중인 클래스명
    # 	- funcName | String | 실행중인 기능 명
    # 	- content | String | 로그 내용
    def war(self, procName, className, funcName, content):
        #current_time = util_time.get_current_time(util_time.TIME_CURRENT_TYPE_DEFAULT)
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        log_msg = f"{procName}: WARNING ({className}) - {caller.function} (line: {caller.lineno}) > {content}"
        logging.warning(log_msg)

    # 4. Cri 로그를 기록 한다.
    #
    # Parameter
    # 	- procName | String | 프로세스명
    # 	- className | String | 실행중인 클래스명
    # 	- funcName | String | 실행중인 기능 명
    # 	- content | String | 로그 내용
    def cri(self, procName, className, funcName, content):
        #current_time = util_time.get_current_time(util_time.TIME_CURRENT_TYPE_DEFAULT)
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        log_msg = f"{procName}: CRITICAL ({className}) - {caller.function} (line: {caller.lineno}) > {content}"
        logging.critical(log_msg)
