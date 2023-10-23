# _*_coding: utf-8 -*-

from flask import Blueprint, request
from flask_restx import Resource
import os
import sys
import json
import copy

projectStatisticsManageApi = Blueprint("projectStatisticsManageApi", __name__)


from projectStatisticsManage.servProjectStatisticsManage import (
    servProjectStatisticsManage,
)
from userManage.servUserManage import servUserManage
from common.commonService import commonService
from common.commUtilService import commUtilService
from common.logManage import logManage
from common import constants


from allscapeAPIMain import procName
from allscapeAPIMain import api


logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당

projectStatisticsManageApi = api.namespace(
    "projectStatisticsManageApi", description="프로젝트 통계 관리"
)

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당

# 프로젝트 진행 상태 통계 조회 API


@api.response(200, "Success")
@api.response(400, "Bad Request")
@api.response(500, "Server Internal Error")
@projectStatisticsManageApi.route("/ProjStatusStatistics")
class projectStatisticsManage(Resource):
    @api.response(455, "User not found")
    @api.doc(description="작업일지 댓글 조회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
    )
    def get(self):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()

        servProjStatistMana = servProjectStatisticsManage()

        try:

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 프로젝트 상태 통계 조회 시작 ----------",
            )

            token = request.headers.get("token")
            sysCd = request.headers.get("sysCd")

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "request header sysCd : " + sysCd + ", token : " + token,
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

            #################################### 로그인 사용자 정보를 가져 온다. ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 사용자 정보를 가져온다. ----------",
            )

            # 사용자 정보를 가져 온다.
            resCd, msg, loginUserInfo = servUserMana.getUserInfo(2, token, sysCd)
            # Error 발생 시 에러 코드 리턴
            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + msg,
                )
                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "response : " + commUtilServ.jsonDumps(result),
                )
                return result

            if loginUserInfo == None:
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_454, "", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )
                return result

            #################################### 프로젝트 상태 통계를 조회 한다. ####################################
            if loginUserInfo["authority_code"] == constants.USER_MASTER:
                resCd, msg, psData = servProjStatistMana.countProjectStatusMaster()
            elif loginUserInfo["authority_code"] == constants.USER_MONITOR:
                resCd, msg, psData = servProjStatistMana.countProjectStatusCompany(
                    loginUserInfo["co_code"]
                )
            else:
                resCd, msg, psData = servProjStatistMana.countProjectStatusId(
                    loginUserInfo["id"]
                )
            return commServ.makeReturnMessage(resCd, msg, psData)

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
