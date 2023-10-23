# _*_coding: utf-8 -*-
import os
import sys
import copy

from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import materialHome
from allscapeAPIMain import materialFile


from common.logManage import logManage

from projectInspMaterManage.sqlProjectInspMaterManage import sqlProjectInspMaterManage
from common.commonService import commonService

from common import constants

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectInspMaterManage:

    # 자재 검수 요청 정보를 저장 한다.
    def putInspMaterInfo(self, params, docDefaultInfo, coCode):
        dbms = copy.copy(db)
        sProjInspMaterMana = sqlProjectInspMaterManage()

        materialList = params["reqDocContent"]["material_list"]

        index = 0
        for material in materialList:
            query = sProjInspMaterMana.iPutInspMaterInfo(
                params["reqDocInfo"]["cons_code"],
                material,
                docDefaultInfo,
                coCode,
                index,
            )

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "iPutInspMaterInfo Query : " + query,
            )

            # 쿼리 실행
            resCd, msg, resData = dbms.execute(query)
            index += 1
            if resCd != 0:
                return resCd, msg, resData

        return constants.REST_RESPONSE_CODE_ZERO, "", None

    # 자재 검수 통보 정보를 저장 한다.
    def modifyInspMaterInfo(self, params, docDefaultInfo):
        dbms = copy.copy(db)
        sProjInspMaterMana = sqlProjectInspMaterManage()

        query = sProjInspMaterMana.uModifyInspMaterInfo(
            params["reqDocInfo"]["cons_code"],
            params["reqDocContent"]["req_sys_doc_num"],
            params["reqDocContent"]["insp_result"],
            params["reqDocContent"]["insp_date"],
            docDefaultInfo["sysDocNum"],
        )

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

        # 검수 자재 리스트롤 조회 한다.

    def searchInspMaterList(self, userInfo, userAuth, jobAuth, searchData):
        dbms = copy.copy(db)
        sProjInspMaterMana = sqlProjectInspMaterManage()

        query = sProjInspMaterMana.sSearchInspMaterList(
            userInfo, userAuth, jobAuth, searchData
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchInspMaterList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

        # 검수 자재 리스트 개수롤 조회 한다.

    def searchInspMaterListCnt(self, userInfo, userAuth, jobAuth, searchData):
        dbms = copy.copy(db)
        sProjInspMaterMana = sqlProjectInspMaterManage()

        query = sProjInspMaterMana.sSearchInspMaterListCnt(
            userInfo, userAuth, jobAuth, searchData
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchInspMaterListCnt Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData
