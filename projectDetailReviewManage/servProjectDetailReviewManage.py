# _*_coding: utf-8 -*-
import os
import sys
import copy
import re
import json

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.logManage import logManage

from projectDetailReviewManage.sqlProjectDetailReviewManage import (
    sqlProjectDetailReviewManage,
)

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectDetailReviewManage:
    """시공상세도 검토 관리 Service Class"""

    def getDetailReviewAll(self, params: dict) -> str:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectDetailReviewManage.select(params["cons_code"])
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "getDetailReviewAll: " + query,
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

        ############### 요청서와 통지서의 세부 정보들을 로드한다 ##################
        for result in results:
            req_content = json.loads(result["req_content"])
            result["req_content"] = req_content
            if result["ntc_content"]:
                ntc_content = json.loads(result["ntc_content"])
                result["ntc_content"] = ntc_content

        ############### 검색조건에 따른 필요없는 정보를 제거한다 ##################
        match_results = list()

        for result in results:
            # 요청서 작성기간 검색
            if "req_datetime_start" in params:
                if result["req_pr_date"] < params["req_datetime_start"]:
                    continue
            if "req_datetime_end" in params:
                if result["req_pr_date"] > params["req_datetime_end"]:
                    continue

            # 통지서 검토완료기간 검색 (통지서 결재 자체가 없을 때에는 항상 참)
            if "ntc_datetime_start" in params:
                if result["ntc_pr_date"] < params["ntc_datetime_start"]:
                    continue
            if "ntc_datetime_end" in params:
                if result["ntc_pr_date"] > params["req_datetime_end"]:
                    continue

            # 부위 검색 (띄어쓰기 무시)
            if "location" in params:
                search_location = re.sub("\s", "", params["location"])
                target_location = re.sub("\s", "", result["req_content"]["location"])
                if not re.findall(search_location, target_location):
                    continue

            # 시공기술자 검색
            if "eng_name" in params:
                if result["req_content"]["engineer_name"] != params["eng_name"]:
                    continue

            # 요청서 수신자 검색
            if "recv_name" in params:
                if result["req_content"]["recv_name"] != params["recv_name"]:
                    continue

            match_results.append(result)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "검색된 시공상세도 검토 목록개수: " + str(len(match_results)),
        )
        return resCd, msg, match_results
