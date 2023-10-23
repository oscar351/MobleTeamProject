# _*_coding: utf-8 -*-


from flask import Blueprint, request
import os
import sys
import json
import copy

projectInspMaterManageApi = Blueprint("projectInspMaterManageApi", __name__)


from projectInspMaterManage.servProjectInspMaterManage import servProjectInspMaterManage
from userManage.servUserManage import servUserManage

from allscapeAPIMain import procName
from allscapeAPIMain import db
from projectManage.sqlProjectManage import sqlProjectManage


from common.commUtilService import commUtilService
from common.commonService import commonService
from common.logManage import logManage
from common import constants

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당

# 자재 검수 요청/통보 리스트 조회 API
@projectInspMaterManageApi.route("/searchInspMaterList", methods=["POST"])
def searchInspMaterList():
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servProjInspMaterMana = servProjectInspMaterManage()

    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 검수 자재 리스트 조회 시작 ----------",
        )

        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        params = request.get_json()  # parameter recv

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "request header sysCd : "
            + sysCd
            + ", token : "
            + token
            + " / request params data : "
            + commUtilServ.jsonDumps(params),
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

            #################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
        )

        query = sProjMana.sGetJobTitleCdObj(
            params["search_cons_code"], loginUserInfo["id"]
        )
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

        if jobResData == None:
            if (
                loginUserInfo["authority_code"] != constants.USER_AUTH_CONTRACTOR
                and loginUserInfo["authority_code"]
                != constants.USER_AUTH_CONTRACTOR_MONITOR
                and loginUserInfo["authority_code"] != constants.USER_AUTH_SUPERVISOR
                and loginUserInfo["authority_code"]
                != constants.USER_AUTH_SUPERVISOR_MONITOR
                and loginUserInfo["authority_code"] != constants.USER_AUTH_INOCCUPATION
                and loginUserInfo["authority_code"] != constants.USER_AUTH_SYSMANAGE
                and loginUserInfo["authority_code"] != constants.USER_AUTH_BUYER
                and loginUserInfo["authority_code"] != constants.USER_AUTH_WHITEHALL
            ):
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL,
                    "현재 프로젝트에 참여하고 있지 않아 프로젝트 참여자를 조회 할 수 없습니다.",
                    None,
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

                #################################### 검수 자재 리스트를 조회 한다. ####################################
        resCd, msg, resDataList = servProjInspMaterMana.searchInspMaterList(
            loginUserInfo, loginUserInfo["authority_code"], jobResData, params
        )
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

        #################################### 검수 자재 리스트 수를 조회 한다. ####################################
        resCd, msg, resDataCnt = servProjInspMaterMana.searchInspMaterListCnt(
            loginUserInfo, loginUserInfo["authority_code"], jobResData, params
        )
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

        resultData = {"list": resDataList, "cnt": str(resDataCnt["cnt"])}

        ################################## Response 데이터를 생성 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Response 데이터를 생성 한다. ----------",
        )

        result = commServ.makeReturnMessage(resCd, msg, resultData)

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 검수 자재 리스트를 조회 한다. 종료 ----------",
        )

        return result

    except KeyError as e:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
        )
    except NameError as e:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
        )
    except TypeError as e:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
        )
    except AttributeError as e:
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
