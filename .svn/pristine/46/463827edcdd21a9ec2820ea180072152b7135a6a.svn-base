# _*_coding: utf-8 -*-
import os
import sys
import copy

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.logManage import logManage

from commonApprovalManage.sqlCommonApprovalManage import sqlCommonApprovalManage

# from common.commonService import commonService

# from common import constants

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servCommonApprovalManage:
    def putCommonApprovalInfo(self, common_approval_manage):
        dbms = copy.copy(db)
        sqlComApproMana = sqlCommonApprovalManage()

        query = sqlComApproMana.iPutCommonApprovalInfo(common_approval_manage)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutCommonApprocalInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    def getCommApproList(self, userId, params):
        dbms = copy.copy(db)
        sqlComApproMana = sqlCommonApprovalManage()

        query = sqlComApproMana.sGetCommonApprovalInfoList(userId, params)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetCommonApprovalInfoList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    def getDetailCommAppro(self, userId, reqApproDate):
        dbms = copy.copy(db)
        sqlComApproMana = sqlCommonApprovalManage()

        query = sqlComApproMana.sGetDetailCommAppro(userId, reqApproDate)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetDetailCommAppro Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    def updateCommApproval(self, updateCommApproData):
        dbms = copy.copy(db)
        sqlComApproMana = sqlCommonApprovalManage()

        query = sqlComApproMana.uUpdateCommApproval(updateCommApproData)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uUpdateCommApproval Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    def delCommonApprovalInfo(self, common_approval_manage):
        dbms = copy.copy(db)
        sqlComApproMana = sqlCommonApprovalManage()

        query = sqlComApproMana.dDelCommonApprovalInfo(common_approval_manage)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelCommonApprocalInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData
