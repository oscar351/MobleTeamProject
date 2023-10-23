# _*_coding: utf-8 -*-
import os
import sys
import copy

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.logManage import logManage

from projectInspManage.sqlProjectInspManage import sqlProjectInspManage


logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


# 현장 점검 서비스
class servProjectInspManage:

    # 현장 점검 데이터를 저장 한다.
    def putInspInfo(self, userId, dataInfo):
        dbms = copy.copy(db)
        sProjInspMana = sqlProjectInspManage()

        query = sProjInspMana.iPutInspInfo(userId, dataInfo)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutInspInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 현장 점검 데이터를 가져 온다.
    def getInspInfoObj(self, inspId):
        dbms = copy.copy(db)
        sProjInspMana = sqlProjectInspManage()

        query = sProjInspMana.sGetInspInfoObj(inspId)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetInspInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 현장 점검 데이터를 수정 한다.
    def updateInspInfo(self, dataInfo):
        dbms = copy.copy(db)
        sProjInspMana = sqlProjectInspManage()

        query = sProjInspMana.uUpdateInspInfo(dataInfo)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uUpdateInspInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 현장 점검 정보 리스트를 조회 한다.
    def searchInspInfoList(self, params):
        dbms = copy.copy(db)
        sProjInspMana = sqlProjectInspManage()

        query = sProjInspMana.sGetInspInfoList(params)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetInspInfoList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 현장 점검 정보 리스트 개수를 조회 한다.
    def searchInspInfoCnt(self, params):
        dbms = copy.copy(db)
        sProjInspMana = sqlProjectInspManage()

        query = sProjInspMana.sGetInspInfoCnt(params)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetInspInfoCnt Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 현장 점검 조치사항 데이터를 저장 한다.
    def updateInspActionInfo(self, userId, dataInfo):
        dbms = copy.copy(db)
        sProjInspMana = sqlProjectInspManage()

        query = sProjInspMana.uUpdateInspActionInfo(userId, dataInfo)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uUpdateInspActionInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData
