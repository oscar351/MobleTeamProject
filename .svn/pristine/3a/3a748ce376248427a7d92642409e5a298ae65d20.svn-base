# _*_coding: utf-8 -*-
import os
import sys
import copy

from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import materialHome
from allscapeAPIMain import materialFile


from common.logManage import logManage

from projectDetectionManage.sqlProjectDetectionManage import sqlProjectDetectionManage
from common.commonService import commonService

from common import constants

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectDetectionManage:

    # 검측 요청 정보를 저장 한다.
    def putDetectionInfo(self, params, docDefaultInfo, coCode, writerDate):
        dbms = copy.copy(db)
        sProjDeteMana = sqlProjectDetectionManage()

        # 검측 정보를 저장 한다.
        query = sProjDeteMana.iPutDetectionInfo(
            params, docDefaultInfo, coCode, writerDate
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutDetectionInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)
        if resCd != 0:
            return resCd, msg, resData

        return constants.REST_RESPONSE_CODE_ZERO, "", None

    # 검측 체크리스트를 저장 한다.
    def putDeteChkList(self, consCode, sysDocNum, chkList):
        dbms = copy.copy(db)
        sProjDeteMana = sqlProjectDetectionManage()

        for chkInfo in chkList:
            # 검측 정보를 저장 한다.
            query = sProjDeteMana.iPutDeteChkList(consCode, sysDocNum, chkInfo)

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "iPutDeteChkList Query : " + query,
            )

            # 쿼리 실행
            resCd, msg, resData = dbms.execute(query)
            if resCd != 0:
                return resCd, msg, resData

        return constants.REST_RESPONSE_CODE_ZERO, "", None

    # 검측 체크리스트를 삭제 한다.
    def delDeteChkList(self, consCode, sysDocNum):
        dbms = copy.copy(db)
        sProjDeteMana = sqlProjectDetectionManage()

        query = sProjDeteMana.dDelDeteChkList(consCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelDeteChkList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)
        if resCd != 0:
            return resCd, msg, resData

    # 검측 통보 정보를 저장 한다.
    def modifyDetectionInfo(self, params, docDefaultInfo):
        dbms = copy.copy(db)
        sProjDeteMana = sqlProjectDetectionManage()

        query = sProjDeteMana.uModifyDetectionInfo(params, docDefaultInfo)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uModifyInspMaterInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)
        if resCd != 0:
            return resCd, msg, resData

        return constants.REST_RESPONSE_CODE_ZERO, "", None

    # 검측 체크리스트 결과를 업데이트 한다.
    def modifyDeteChkList(self, consCode, reqSysDocNum, chkList):
        dbms = copy.copy(db)
        sProjDeteMana = sqlProjectDetectionManage()

        for chkInfo in chkList:
            # 검측 정보를 저장 한다.
            query = sProjDeteMana.uModifyDeteChkList(consCode, reqSysDocNum, chkInfo)

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "uModifyDeteChkList Query : " + query,
            )

            # 쿼리 실행
            resCd, msg, resData = dbms.execute(query)
            if resCd != 0:
                return resCd, msg, resData

        return constants.REST_RESPONSE_CODE_ZERO, "", None

        # 검측 리스트를 조회 한다.

    def searchDetectionInfoList(self, userInfo, userAuth, jobAuth, searchData):
        dbms = copy.copy(db)
        sProjDeteMana = sqlProjectDetectionManage()

        query = sProjDeteMana.sSearchDetectionInfoList(
            userInfo, userAuth, jobAuth, searchData
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchDetectionInfoList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

        # 검수 자재 리스트 개수롤 조회 한다.

    def searchDetectionInfoListCnt(self, userInfo, userAuth, jobAuth, searchData):
        dbms = copy.copy(db)
        sProjDeteMana = sqlProjectDetectionManage()

        query = sProjDeteMana.sSearchDetectionInfoListCnt(
            userInfo, userAuth, jobAuth, searchData
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchDetectionInfoListCnt Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData
