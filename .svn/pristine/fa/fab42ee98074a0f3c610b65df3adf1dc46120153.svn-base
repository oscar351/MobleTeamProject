# _*_coding: utf-8 -*-


from flask import Blueprint, request
import os
import sys
import json
import copy

projectApproMaterManageApi = Blueprint("projectApproMaterManageApi", __name__)


from projectApproMaterManage.servProjectApproMaterManage import (
    servProjectApproMaterManage,
)
from userManage.servUserManage import servUserManage

from allscapeAPIMain import procName

from common.commUtilService import commUtilService
from common.commonService import commonService
from common.logManage import logManage
from common import constants

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당

# 승인 자재 리스트 조회 API
@projectApproMaterManageApi.route("/getApproMaterList", methods=["POST"])
def getApproMaterList():
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servProjApproMaterMana = servProjectApproMaterManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 승인 자재 리스트 조회 시작 ----------",
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

            #################################### 승인 자재 리스트를 조회 한다. ####################################
        resCd, msg, resDataList = servProjApproMaterMana.getApproMaterList(params)
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

        #################################### 승인 자재 리스트 수를 조회 한다. ####################################
        resCd, msg, resDataCnt = servProjApproMaterMana.getApproMaterCnt(params)
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
            "---------- 승인 자재 리스트를 조회 한다. 종료 ----------",
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


# 승인 자재 상세 조회 API
@projectApproMaterManageApi.route("/getDetailApproMater/<materialNo>", methods=["GET"])
def getDetailApproMater(materialNo):
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servProjApproMaterMana = servProjectApproMaterManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 승인 자재 상세 조회 시작 ----------",
        )

        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "request header sysCd : "
            + sysCd
            + ", token : "
            + token
            + " / request url materialNo : "
            + materialNo,
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

            #################################### 승인 자재를 상세 조회 한다. ####################################
        resCd, msg, resData = servProjApproMaterMana.getDetailApproMater(materialNo)
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

        ################################## Response 데이터를 생성 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Response 데이터를 생성 한다. ----------",
        )

        result = commServ.makeReturnMessage(resCd, msg, resData)

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
            "---------- 승인 자재를 상세 조회 한다. 종료 ----------",
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
