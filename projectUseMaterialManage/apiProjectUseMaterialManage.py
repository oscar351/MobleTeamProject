# _*_coding: utf-8 -*-


from flask import Blueprint, request
import json
import copy
import os
import sys
import traceback
import uuid

# from ast import literal_eval

projectUseMaterialManageApi = Blueprint("projectUseMaterialManageApi", __name__)

from projectUseMaterialManage.servProjectUseMaterialManage import (
    servProjectUseMaterialManage,
)


# user import
from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import procCode

# from allscapeAPIMain import weatherApi
# from allscapeAPIMain import fileHome
# from allscapeAPIMain import projectHome
# from allscapeAPIMain import procDetails

from common.logManage import logManage

# from common import util_time
from common import constants
from common.commUtilService import commUtilService
from common.commonService import commonService

# from common.messageService import messageService
# from common.excelService import excelService
# from logManage.dataLogManage import dataLogManage
# from logManage.sqlLogManage import sqlLogManage
# from commManage.sqlCommManage import sqlCommManage
# from commManage.dataCommManage import dataCommManage
from userManage.servUserManage import servUserManage

# from userManage.sqlUserManage import sqlUserManage

# from commManage.servCommManage import servCommManage
# from commManage.sqlCommManage import sqlCommManage

from projectManage.sqlProjectManage import sqlProjectManage


logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


# 자재 선정 요청/통보 리스트 조회
@projectUseMaterialManageApi.route("/searchMaterialSelectList", methods=["POST"])
def searchMaterialSelectList():
    commServ = commonService()
    commUtilServ = commUtilService()
    servProjUseMaterMana = servProjectUseMaterialManage()
    servUserMana = servUserManage()

    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    try:
        sysCd = request.headers.get("sysCd")
        token = request.headers.get("token")
        params = request.get_json()  # login parameter recv

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "request header token : "
            + token
            + ", sysCd : "
            + sysCd
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

        #################################### 자재 선정 리스트를 조회 힌다. ####################################
        resCd, msg, resMaterSelList = servProjUseMaterMana.searchMaterialSelectList(
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

            #################################### 자재 선정 리스트 개수를 조회 힌다. ####################################
        (
            resCd,
            msg,
            resMaterSelListCnt,
        ) = servProjUseMaterMana.searchMaterialSelectListCnt(
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

        responseData = {"list": resMaterSelList, "cnt": resMaterSelListCnt["cnt"]}

        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_ZERO, "", responseData
        )
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
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


# 선정된 자재 리스트 조회
@projectUseMaterialManageApi.route("/getAppSelMaterialList/<consCode>", methods=["GET"])
def getAppSelMaterialList(consCode):
    commServ = commonService()
    commUtilServ = commUtilService()
    servProjUseMaterMana = servProjectUseMaterialManage()
    servUserMana = servUserManage()

    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    try:
        sysCd = request.headers.get("sysCd")
        token = request.headers.get("token")

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "request header token : "
            + token
            + ", sysCd : "
            + sysCd
            + " / request url consCoode : "
            + consCode,
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

        #################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
        )

        query = sProjMana.sGetJobTitleCdObj(consCode, loginUserInfo["id"])
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

        #################################### 승인된 자재 리스트를 조회 한다. ####################################
        resCd, msg, resData = servProjUseMaterMana.getAppSelMaterialList(
            consCode, loginUserInfo
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

        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_ZERO, "", resData
        )
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
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
