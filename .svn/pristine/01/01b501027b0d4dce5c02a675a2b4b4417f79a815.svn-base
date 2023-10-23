from flask import Blueprint, request
import json
import copy
import os
import sys


from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.logManage import logManage
from common import constants
from common.commUtilService import commUtilService
from common.commonService import commonService
from userManage.servUserManage import servUserManage
from projectManage.sqlProjectManage import sqlProjectManage
from projectChangeReviewManage.servProjectChangeReviewManage import (
    servProjectChangeReviewManage,
)

projectChangeReviewManageApi = Blueprint("projectChangeReviewManageApi", __name__)

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


@projectChangeReviewManageApi.route(
    "/ChangeReview/<cons_code>",
    methods=["GET"],
)
def projectChangeReviewAllManage(cons_code: str) -> dict:
    """설계변경 전체 검토 api"""

    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    sProjMana = sqlProjectManage()
    servProjCRMana = servProjectChangeReviewManage()

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 설계변경 검토 api 시작 ----------",
    )

    try:
        sysCd = request.headers.get("sysCd")
        token = request.headers.get("token")

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "request header token : " + token + ", sysCd : " + sysCd,
        )

        # System Code Check
        result, resultData = commServ.checkSystemCd(sysCd)
        if result == False:
            return resultData

        # Token Check
        result, resultData = commServ.checkTokenCd(token)
        if result == False:
            return resultData

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 로그인 된 사용자인지 확인 한다. ----------",
        )

        # 로그인 된 사용자 인지 확인한다.
        result, resultData = commServ.userLoginChk(token, sysCd)
        if result == False:
            return resultData

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 사용자 정보를 가져온다. ----------",
        )

        # 사용자 정보를 가져 온다.
        resCd, msg, loginUserInfo = servUserMana.getUserInfo(2, token, sysCd)
        if resCd != 0:  # DB 에러 발생 시
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + commUtilServ.jsonDumps(msg),
            )

            result = commServ.makeReturnMessage(resCd, msg, None)

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        if loginUserInfo == None:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_455, "", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 로직에 필요한 변수를 저장한다. ####################################
        params = {
            "cons_code": cons_code,
            "id": loginUserInfo["id"],
        }

        #################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
        )
        query = sProjMana.sGetJobTitleCdObj(params["cons_code"], params["id"])
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetJobTitleCdObj Query : " + query,
        )
        resCd, msg, jobResData = dbms.queryForObject(query)

        # Error 발생 시 에러 코드 리턴
        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error: " + msg,
            )

            result = commServ.makeReturnMessage(resCd, msg, None)
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "response : " + commUtilServ.jsonDumps(result),
            )

            return result

        #################################### 검색조건을 저장한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "검색조건을 저장한다",
        )

        conditions = request.args.to_dict()
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "search conditions : " + str(conditions),
        )

        # 검색조건이 있을 경우 추가로 저장한다
        if "req_datetime_start" in conditions:
            params["req_datetime_start"] = str(conditions.get("req_datetime_start"))
        if "req_datetime_end" in conditions:
            params["req_datetime_end"] = str(conditions.get("req_datetime_end"))
        if "writer_ID" in conditions:
            params["writer_ID"] = str(conditions.get("writer_ID"))
        if "status" in conditions:
            params["status"] = str(conditions.get("status"))

        if request.method == "GET":

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 설계변경 검토조회 처리 시작 ----------" + params["cons_code"],
            )

            resCd, msg, DRData = servProjCRMana.getChangeReviewAll(params)
            return commServ.makeReturnMessage(resCd, msg, DRData)

    except Exception as e:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
        )

    logs.war(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "Response : " + commUtilServ.jsonDumps(result),
    )

    return result
