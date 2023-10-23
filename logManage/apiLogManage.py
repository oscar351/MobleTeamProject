from flask import Blueprint, request
from flask_restx import Resource
import json
import copy
import os
import sys

from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import api

from common.logManage import logManage
from common import constants
from userManage.servUserManage import servUserManage
from common.commUtilService import commUtilService
from common.commonService import commonService
from logManage.servLogManage import servLogManage

logManageApi = api.namespace("logApi", description="시스템 로그 관리")

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


@logManageApi.route("/logList")
class loglistManage(Resource):
    """시스템 로그 리스트 조회 api"""

    @api.doc(description="시스템 로그 리스트 조회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument(
            "log_id", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "title_keyword", type=str, location="querys", required=False
        ),
    )
    def get(self):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servLogMana = servLogManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 시스템 로그 리스트 get api 시작 ----------",
        )

        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")
            log_id = request.args.get("log_id")
            title_keyword = request.args.get("title_keyword")

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

                return result

            if (
                loginUserInfo == None
                or loginUserInfo["authority_code"] != constants.USER_MASTER
            ):
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

            #################################### 해당 로그 목록을 조회한다 ##########################

            resCd, msg, logData = servLogMana.get_log_list(log_id, title_keyword)
            return commServ.makeReturnMessage(resCd, msg, logData)

        except Exception as e:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result


@logManageApi.route("/log/<log_id>")
class loglistManage(Resource):
    """시스템 로그 조회 api"""

    @api.doc(description="시스템 로그 조회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
    )
    def get(self, log_id):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servLogMana = servLogManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 시스템 로그 리스트 get api 시작 ----------",
        )

        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")

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

                return result

            if (
                loginUserInfo == None
                or loginUserInfo["authority_code"] != constants.USER_MASTER
            ):
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

            #################################### 해당 로그 목록을 조회한다 ##########################

            resCd, msg, logData = servLogMana.get_log(log_id)
            return commServ.makeReturnMessage(resCd, msg, logData)

        except Exception as e:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result
