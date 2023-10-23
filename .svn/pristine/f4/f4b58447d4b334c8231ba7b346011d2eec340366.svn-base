# _*_coding: utf-8 -*-

import os
import sys
import copy

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.logManage import logManage

from projectUseMaterialManage.sqlProjectUseMaterialManage import (
    sqlProjectUseMaterialManage,
)

logs = logManage()


class servProjectUseMaterialManage:

    # 자재 선정 요청에 대한 자재 정보를 저장 한다.
    def putUseMaterialInfo(
        self, consCode, docNum, coCode, constrTypeCd, materialNum, sysDocNum
    ):

        dbms = copy.copy(db)
        sProjUseMatMana = sqlProjectUseMaterialManage()

        query = sProjUseMatMana.iPutUseMaterialInfo(
            consCode, docNum, coCode, constrTypeCd, materialNum, sysDocNum
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutUseMaterialInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 자재 선정 요청에 대한 자재 정보를 삭제 한다.
    # def delUseMaterialInfo(self, consCode, docNum, coCode):
    def delUseMaterialInfo(self, sysDocNum):
        dbms = copy.copy(db)
        sProjUseMatMana = sqlProjectUseMaterialManage()

        # query = sProjUseMatMana.dDelUseMaterialInfo(consCode, docNum, coCode)
        query = sProjUseMatMana.dDelUseMaterialInfo(sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelUseMaterialInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 자재 선정 리스트롤 조회 한다.
    def searchMaterialSelectList(self, userInfo, userAuth, jobAuth, searchData):
        dbms = copy.copy(db)
        sProjUseMatMana = sqlProjectUseMaterialManage()

        query = sProjUseMatMana.sSearchMaterialSelectList(
            userInfo, userAuth, jobAuth, searchData
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchMaterialSelectList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 자재 선정 리스트 개수롤 조회 한다.
    def searchMaterialSelectListCnt(self, userInfo, userAuth, jobAuth, searchData):
        dbms = copy.copy(db)
        sProjUseMatMana = sqlProjectUseMaterialManage()

        query = sProjUseMatMana.sSearchMaterialSelectListCnt(
            userInfo, userAuth, jobAuth, searchData
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchMaterialSelectListCnt Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 자재 선정 통보에 대한 자재 정보를 저장 한다.
    def modifyUseMaterialInfo(
        self, consCode, reqSysDocNum, constrTypeCd, approvalInfo, sysDocNum
    ):

        dbms = copy.copy(db)
        sProjUseMatMana = sqlProjectUseMaterialManage()

        query = sProjUseMatMana.uModifyUseMaterialInfo(
            consCode, reqSysDocNum, constrTypeCd, approvalInfo, sysDocNum
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uModifyUseMaterialInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 공장방문 검사 결과 정보를 저장 한다.
    def putFactoryVisitResult(self, docDefaultInfo, params):

        dbms = copy.copy(db)
        sProjUseMatMana = sqlProjectUseMaterialManage()

        query = sProjUseMatMana.iPutFactoryVisitResult(docDefaultInfo, params)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutFactoryVisitResult Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 공장방문 검사 결과 정보를 삭제 한다.
    def delFactoryVisitResult(self, consCode, sysDocNum):

        dbms = copy.copy(db)
        sProjUseMatMana = sqlProjectUseMaterialManage()

        query = sProjUseMatMana.dDelFactoryVisitResult(consCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelFactoryVisitResult Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 선정된 자재 리스트를 조회 한다.
    def getAppSelMaterialList(self, consCode, loginUserInfo):

        dbms = copy.copy(db)
        sProjUseMatMana = sqlProjectUseMaterialManage()

        query = sProjUseMatMana.sGetAppSelMaterialList(consCode, loginUserInfo)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetAppSelMaterialList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 해당 문서를 볼 수 있는지 확인 한다.
    def checkDocViewAuth(self, consCode, userId, sysDocNum):

        dbms = copy.copy(db)
        sProjUseMatMana = sqlProjectUseMaterialManage()

        query = sProjUseMatMana.sCheckDocViewAuth(consCode, userId, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sCheckDocViewAuth Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData
