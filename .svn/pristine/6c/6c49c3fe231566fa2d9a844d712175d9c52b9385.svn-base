# _*_coding: utf-8 -*-
import os
import sys
import copy

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.logManage import logManage

from historyManage.sqlHistoryManage import sqlHistoryManage
from userManage.servUserManage import servUserManage

from common.commonService import commonService

from common import constants

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servHistoryManage:
    def getCoHisList(self, searchList):
        # 1. 사용자 정보를 가져 온다.
        sqlHisMana = sqlHistoryManage()

        # 2. 재직 정보 리스트 쿼리를 생성 한다.
        query = sqlHisMana.sGetCoHistoryList(searchList)

        # 3. 재직 정보를 저장 한다.
        dbms = copy.copy(db)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetUserCompanyHistory Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    def putUserCompanyHistory(self, userId):
        # 1. 사용자 정보를 가져 온다.
        servUserMana = servUserManage()
        sqlHisMana = sqlHistoryManage()

        resCd, msg, userInfo = servUserMana.getUserInfo(1, userId, None)

        if resCd != 0:
            return resCd, msg, None

        # 2. 재직 정보 쿼리를 생성 한다.
        query = sqlHisMana.iPutUserCompanyHistory(userInfo)

        # 3. 재직 정보를 저장 한다.
        dbms = copy.copy(db)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutUserCompanyHistory Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, userInfo

    def delUserCompanyHistory(self, userInfo):
        sqlHisMana = sqlHistoryManage()

        # 1. 재직 정보 삭제 쿼리를 생성 한다.
        query = sqlHisMana.dDelUserCompanyHistory(userInfo)

        # 2. 재직 정보를 삭제 한다.
        dbms = copy.copy(db)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDdelUserCompnanyHistory Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, None

    def getProjHisList(self, searchList):
        # 1. 사용자 정보를 가져 온다.
        sqlHisMana = sqlHistoryManage()

        # 2. 재직 정보 리스트 쿼리를 생성 한다.
        query = sqlHisMana.sGetProjHistoryList(searchList)

        # 3. 재직 정보를 저장 한다.
        dbms = copy.copy(db)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetProjHistoryList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    def putProjHistoryList(self, userInfo, projHisList):
        sqlHisMana = sqlHistoryManage()

        dbms = copy.copy(db)

        for projHisInfo in projHisList:
            query = sqlHisMana.iPutProjHistoryList(userInfo, projHisInfo)

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "iPutProjHistoryList Query : " + query,
            )

            # 쿼리 실행
            resCd, msg, resData = dbms.execute(query)
            if resCd != 0:
                return resCd, msg, None

        return constants.REST_RESPONSE_CODE_ZERO, "", None

    def delProjHistoryList(self, userInfo, projHisList):
        sqlHisMana = sqlHistoryManage()

        dbms = copy.copy(db)

        for projHisInfo in projHisList:
            query = sqlHisMana.dDelProjHistoryList(userInfo, projHisInfo)

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "dDelProjHistoryList Query : " + query,
            )

            # 쿼리 실행
            resCd, msg, resData = dbms.execute(query)
            if resCd != 0:
                return resCd, msg, None

        return constants.REST_RESPONSE_CODE_ZERO, "", None
