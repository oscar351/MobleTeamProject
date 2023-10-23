# _*_coding: utf-8 -*-
import os
import sys
import copy

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.logManage import logManage

from projectStatisticsManage.sqlProjectStatisticsManage import (
    sqlProjectStatisticsManage,
)


logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectStatisticsManage:
    def getProjStatusStatistics(self, userId):
        dbms = copy.copy(db)
        sProjStatistMana = sqlProjectStatisticsManage()

        query = sProjStatistMana.sGetProjStatusStatistics(userId)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetProjStatusStatistics Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    def countProjectStatusId(self, id):

        dbms = copy.copy(db)

        query = sqlProjectStatisticsManage.count_project_userin(id)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "count_project_companyin Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    def countProjectStatusCompany(self, co_code):

        dbms = copy.copy(db)

        query = sqlProjectStatisticsManage.count_project_companyin(co_code)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "count_project_companyin Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    def countProjectStatusMaster(self):

        dbms = copy.copy(db)

        query = sqlProjectStatisticsManage.count_project_master()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "count_project_master Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData
