import os
import sys
import copy
import re
import json

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.logManage import logManage

from projectChangeReviewManage.sqlProjectChangeReviewManage import (
    sqlProjectChangeReviewManage,
)

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectChangeReviewManage:
    """설계변경 검토 관리 Service Class"""

    def getChangeReviewAll(self, params: dict) -> str:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectChangeReviewManage.select(params["cons_code"])
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "getChangeReviewAll: " + query,
        )
        resCd, msg, results = dbms.query(query)
        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error: " + msg,
            )
            return resCd, msg, None

        ############### 실정서와 의견서의 세부 정보들을 로드한다 ##################
        for result in results:
            req_content = json.loads(result["req_content"])
            result["req_content"] = req_content
            if result["ntc_content"]:
                ntc_content = json.loads(result["ntc_content"])
                result["ntc_content"] = ntc_content

        ############### 검색조건에 따른 필요없는 정보를 제거한다 ##################
        match_results = list()

        for result in results:
            # 실정서 작성기간 검색 (요청서 결재 자체가 없을 때에는 항상 참)
            if "req_datetime_start" in params and "req_pc_date" in result:
                if result["req_pc_date"] < params["req_datetime_start"]:
                    continue
            if "req_datetime_end" in params and "req_pc_date" in result:
                if result["req_pc_date"] > params["req_datetime_end"]:
                    continue

            # 시공기술자 검색
            if "writer_ID" in params:
                if result["writer_ID"] != params["writer_ID"]:
                    continue

            # 상태 검색
            if "status" in params:
                if result["req_content"]["req_state_code"] != params["status"]:
                    continue

            match_results.append(result)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "검색된 설계변경 검토 목록개수: " + str(len(results)),
        )
        return resCd, msg, match_results
