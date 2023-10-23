# _*_coding: utf-8 -*-

# DB 연결 관리 Class
# 작성 날짜 : 2022. 7. 29
# 작성자 : 황희정
# 기능
# 	1. 2022. 07. 29 | DB 연결 관리 Class 초기화
# 	2. 2022. 07. 29 | DB에 연결한다.
# 	3. 2022. 07. 29 | DB Cursor를 반환 한다.
# 	4. 2022. 07. 29 | DB 연결을 종료 한다.
# 	5. 2022. 07. 29 | 데이터를 저장 한다.
#   6. 2022. 07. 29 | Query를 실행 한다.
# 변경 이력
# 	1. 2022. 07. 29 | 황희정 | 최조 작성
#   2. 2023. 01. 19 | 조현우 | 다중쿼리지원기능 및 에러 수정

# lib import
import pymysql
from typing import Tuple, Optional
from pymysql.constants import CLIENT
import os
import sys

# user import
from common.logManage import logManage
from common.messageService import messageService

from common import constants

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


# DB 연결 관리 Class
class dbManage:
    msgServ = messageService()

    def __init__(self, procName, user, passwd, host, port, database):
        """DB 연결 관리 Class를 초기화 한다."""
        print('.............................' + user)
        self.procName = procName
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port
        self.database = database

    def connect(self):
        """DB connection"""
        try:
            return pymysql.connect(
                user=self.user,
                password=self.passwd,
                host=self.host,
                port=self.port,
                database=self.database,
            )
            """
            return mysql.connector.connect(
                user=self.user,
                password=self.passwd,
                host=self.host,
                port=self.port,
                database=self.database,
            )
            """
        except Exception as e:
            errmsg = f"Error {type(e)} : {str(e)}"
            logs.cri(
                self.procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                errmsg,
            )
            return None

    def connectMulti(self):
        """DB에 다중쿼리문 지원모드로 연결한다."""
        try:
            return pymysql.connect(
                user=self.user,
                password=self.passwd,
                host=self.host,
                port=self.port,
                database=self.database,
                client_flag=CLIENT.MULTI_STATEMENTS,
            )
            """
            return mysql.connector.connect(
                user=self.user,
                password=self.passwd,
                host=self.host,
                port=self.port,
                database=self.database,
            )
            """
        except Exception as e:
            errmsg = f"Error {type(e)} : {str(e)}"
            logs.cri(
                self.procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                errmsg,
            )
            return None

    def getCursor(self, dbHandler):
        """DB Cursor를 반환 한다."""
        try:
            return dbHandler.cursor(pymysql.cursors.DictCursor)

        except Exception as e:
            errmsg = f"Error {type(e)} : {str(e)}"
            logs.cri(
                self.procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                errmsg,
            )
            return None

    def execute(self, query):
        """쿼리를 실행 한다. (커밋 포함)"""

        try:
            with self.connect() as handler:  # 1. DB에 연결한다.
                with self.getCursor(handler) as csor:  # 2. Cursor를 가져온다.
                    csor.execute(query)  # 4. query를 실행 한다.
                    handler.commit()  # 5. 변경사항을 DB에 적용한다.
                    return 0, "", None

        except Exception as e:  # 3. 연결 실패 시 에러 메시지를 생성한다.
            errMsg = f"Error {type(e)} : {str(e)}"
            return int(e.args[0]), errMsg, None

    def executeSpecial(self, query, data):
        """특수문자 쿼리를 실행 한다. (커밋 포함)"""

        try:
            with self.connect() as handler:  # 1. DB에 연결한다.
                with self.getCursor(handler) as csor:  # 2. Cursor를 가져온다.
                    csor.execute(query, data)  # 4. query를 실행 한다.
                    handler.commit()  # 5. 변경사항을 DB에 적용한다.
                    return 0, "", None

        except Exception as e:  # 3. 연결 실패 시 에러 메시지를 생성한다.
            errMsg = f"Error {type(e)} : {str(e)}"
            return int(e.args[0]), errMsg, None

    def executeMulti(self, query):
        """멀티 쿼리를 실행 한다. (커밋 포함)"""

        try:
            with self.connectMulti() as handler:  # 1. DB에 연결한다.
                with self.getCursor(handler) as csor:  # 2. Cursor를 가져온다.
                    csor.execute(query)  # 4. query를 실행 한다.
                    handler.commit()  # 5. 변경사항을 DB에 적용한다.
                    return 0, "", None

        except Exception as e:  # 3. 연결 실패 시 에러 메시지를 생성한다.
            errMsg = f"Error {type(e)} : {str(e)}"
            return int(e.args[0]), errMsg, None

    def executeMultiSpeical(self, query, data):
        """멀티 특수 쿼리를 실행 한다. (커밋 포함)"""

        try:
            with self.connectMulti() as handler:  # 1. DB에 연결한다.
                with self.getCursor(handler) as csor:  # 2. Cursor를 가져온다.
                    csor.execute(query, data)  # 4. query를 실행 한다.
                    handler.commit()  # 5. 변경사항을 DB에 적용한다.
                    return 0, "", None

        except Exception as e:  # 3. 연결 실패 시 에러 메시지를 생성한다.
            errMsg = f"Error {type(e)} : {str(e)}"
            return int(e.args[0]), errMsg, None

    def executeIterSpecial(self, queryList, dataList):
        """다수 특수문자 쿼리를 실행 한다."""

        try:
            with self.connect() as handler:  # 1. DB에 연결한다.
                with self.getCursor(handler) as csor:  # 2. Cursor를 가져온다.
                    for query, data in zip(queryList, dataList):
                        csor.execute(query, data)  # 4. query를 실행 한다.
                    handler.commit()  # 5. 변경사항을 DB에 적용한다.
                    return 0, "", None

        except Exception as e:  # 3. 연결 실패 시 에러 메시지를 생성한다.
            errMsg = f"Error {type(e)} : {str(e)}"
            return int(e.args[0]), errMsg, None

    def executeIter(self, queryList):
        """다수 쿼리를 실행 한다."""

        try:
            with self.connect() as handler:  # 1. DB에 연결한다.
                with self.getCursor(handler) as csor:  # 2. Cursor를 가져온다.
                    for query in queryList:
                        csor.execute(query)  # 4. query를 실행 한다.
                    handler.commit()  # 5. 변경사항을 DB에 적용한다.
                    return 0, "", None

        except Exception as e:  # 3. 연결 실패 시 에러 메시지를 생성한다.
            errMsg = f"Error {type(e)} : {str(e)}"
            return int(e.args[0]), errMsg, None

    def executeMany(self, queryHead, queryBodies):
        """다수 데이터를 삽입 한다."""

        try:
            with self.connect() as handler:  # 1. DB에 연결한다.
                with self.getCursor(handler) as csor:  # 2. Cursor를 가져온다.
                    csor.execute(queryHead)  # 4. query를 실행 한다.
                    for queryBody in queryBodies:
                        csor.execute(queryBody)
                    handler.commit()  # 5. 변경사항을 DB에 적용한다
                    return 0, "", None

        except Exception as e:  # 3. 연결 실패 시 에러 메시지를 생성한다.
            errMsg = f"Error {type(e)} : {str(e)}"
            return int(e.args[0]), errMsg, None

    def queryForObject(self, query):
        """단일 데이터를 조회 한다."""

        try:
            with self.connect() as handler:  # 1. DB에 연결한다.
                with self.getCursor(handler) as csor:  # 2. Cursor를 가져온다.
                    csor.execute(query)  # 4. query를 실행 한다.
                    queryResult = csor.fetchone()  # 5. 데이터를 가져온다.
                    return 0, "", queryResult

        except Exception as e:  # 3. 연결 실패 시 에러 메시지를 생성한다.
            errMsg = f"Error {type(e)} : {str(e)}"
            return int(e.args[0]), errMsg, None

    def queryForObjectSpeical(self, query, data):
        """단일 특수 데이터를 조회 한다."""

        try:
            with self.connect() as handler:  # 1. DB에 연결한다.
                with self.getCursor(handler) as csor:  # 2. Cursor를 가져온다.
                    csor.execute(query, data)  # 4. query를 실행 한다.
                    queryResult = csor.fetchone()  # 5. 데이터를 가져온다.
                    return 0, "", queryResult

        except Exception as e:  # 3. 연결 실패 시 에러 메시지를 생성한다.
            errMsg = f"Error {type(e)} : {str(e)}"
            return int(e.args[0]), errMsg, None


    def query(self, query) -> Tuple[int, str, Optional[list]]:
        """복수 데이터를 조회 한다."""

        try:
            with self.connect() as handler:  # 1. DB에 연결한다.
                with self.getCursor(handler) as csor:  # 2. Cursor를 가져온다.
                    csor.execute(query)  # 4. query를 실행 한다.
                    queryResult = csor.fetchall()  # 5. 데이터를 가져온다.
                    return 0, "", queryResult

        except Exception as e:  # 3. 연결 실패 시 에러 메시지를 생성한다.
            errMsg = f"Error {type(e)} : {str(e)}"
            return int(e.args[0]), errMsg, None

    def querySpecial(self, query, data) -> Tuple[int, str, Optional[list]]:
        """복수 특수 데이터를 조회 한다."""

        try:
            with self.connect() as handler:  # 1. DB에 연결한다.
                with self.getCursor(handler) as csor:  # 2. Cursor를 가져온다.
                    csor.execute(query, data)  # 4. query를 실행 한다.
                    queryResult = csor.fetchall()  # 5. 데이터를 가져온다.
                    return 0, "", queryResult

        except Exception as e:  # 3. 연결 실패 시 에러 메시지를 생성한다.
            errMsg = f"Error {type(e)} : {str(e)}"
            return int(e.args[0]), errMsg, None
