# _*_coding: utf-8 -*-
import os
import sys
import copy
import json

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.commonService import commonService
from common.logManage import logManage

from common.commonService import commonService
from projectPlanReviewManage.sqlProjectPlanReviewManage import (
    sqlProjectPlanReviewManage,
)

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectPlanReviewManage:
    """설계도면 이미지 관리 Service Class"""

    def postPlanReview(self, params: dict) -> dict:
        """설계도면 감리의견 등록"""

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "설계도면 감리의견 등록",
        )

        commServ = commonService()
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        # 해당 조건의 이미지 도면 등록
        query = sqlProjectPlanReviewManage.insert(
            params["cons_code"],
            params["ver_info"],
            params["page"],
            params["x_posper"],
            params["y_posper"],
            params["shape"],
            params["category"],
            params["location"],
            params["problem"],
            params["reason"],
            params["supv_opn"],
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "postPlanReview Query : " + query,
        )

        return dbms.executeMulti(query)

    def getPlanReview(self, params: dict) -> dict:
        """설계도면 감리의견 확인"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectPlanReviewManage.select(
            params["cons_code"],
            params["ver_info"],
            params["number"],
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "getPlanReview Query : " + query,
        )

        return dbms.queryForObject(query)

    def getPlanReviewAll(self, params: dict) -> dict:
        """설계도면 감리의견 전체 확인"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectPlanReviewManage.select_all(
            params["cons_code"],
            params["ver_info"],
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "getPlanReviewAll Query : " + query,
        )

        return dbms.query(query)

    def putPlanReview(self, params: dict) -> dict:
        """설계도면 감리의견 수정"""

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "설계도면 감리의견 수정시작",
        )
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectPlanReviewManage.update(
            params["cons_code"],
            params["ver_info"],
            params["number"],
            params["page"],
            params["x_posper"],
            params["y_posper"],
            params["shape"],
            params["category"],
            params["location"],
            params["problem"],
            params["reason"],
            params["supv_opn"],
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "updatePlanReview Query : " + query,
        )

        return dbms.execute(query)

    def delPlanReview(self, params: dict) -> dict:
        """설계도면 등록된 감리의견 삭제"""

        commServ = commonService()
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectPlanReviewManage.delete(
            params["cons_code"],
            params["ver_info"],
            params["number"],
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delPlanReview Query : " + query,
        )

        return dbms.executeMulti(query)

    def delPlanReviewAll(self, params: dict) -> dict:
        """설계도면 페이지 모든 등록된 감리의견 삭제"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectPlanReviewManage.delete_all(
            params["cons_code"],
            params["ver_info"],
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delPlanReviewAll Query : " + query,
        )

        return dbms.execute(query)

    def getPlanReviewPRT(self, params: dict):
        """설계도면 검토보고서 조회"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectPlanReviewManage.select_prt(params["cons_code"])
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "getPlanReviewPRT: " + query,
        )
        resCd, msg, results = dbms.query(query)
        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error: " + msg,
            )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "result: " + str(len(results)),
        )
        ############### 요청서와 통지서의 세부 정보들을 로드한다 ##################
        for result in results:
            content = json.loads(result["content"])
            result["content"] = content

        ############### 검색조건에 따른 필요없는 정보를 제거한다 ##################
        match_results = list()

        for result in results:

            # 설계도면 버전 검색
            if "ver_info" in params:
                if result["content"]["ver_info"] != params["ver_info"]:
                    continue

            # 검색조건에 충족하는 결과들은 저장한다.
            match_results.append(result)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "검색된 설계도면 검토 목록개수: " + str(len(results)),
        )
        return resCd, msg, match_results
