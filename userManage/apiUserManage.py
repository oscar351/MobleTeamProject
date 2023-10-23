# _*_coding: utf-8 -*-

# 사용자 관리 REST API
# 작성 날짜 : 2022. 07. 29
# 작성자 : 황희정
# 기능
# 	1. 2022. 07. 29 | 로그인 API
# 	2. 2022. 07. 29 | 로그아웃 API
# 	3. 2022. 08. 02 | 사용자 정보를 제공 API(내정보)
# 변경 이력
# 	1. 2022. 07. 29 | 황희정 | 최조 작성
# 	2. 2022. 08. 02 | 황희정 | 수정 | 로그인 API response data에 user state 추가함
# 	3. 2022. 08. 02 | 황희정 | 수정 | 로그아웃 API userID를 Token으로 변경함.
# 	4. 2022. 08. 02 | 황희정 | 추가 | 사용자 정보 제공 API


# sys import
from flask import Blueprint, request, jsonify

# from urllib import parse
import json
import copy
import os
import sys
import traceback
import uuid
import shutil
import urllib

from logManage.servLogManage import servLogManage

userManageApi = Blueprint("userManageApi", __name__)

# user import
from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import procCode
from allscapeAPIMain import fileHome
from allscapeAPIMain import userHome  # 사용자 경로
from allscapeAPIMain import typeUser  # 사용자 경로
from allscapeAPIMain import typeEnterorise  # 기업 경로
from allscapeAPIMain import coCode  # 회사 코드
from allscapeAPIMain import mail  # 회사 코드

from common.logManage import logManage
from common import util_time
from common import constants
from common.dataCommonManage import dataCommonManage
from common.commonService import commonService
from common.messageService import messageService
from common.commUtilService import commUtilService
from common.passwordGenerator import passwordGenerator
from common.encryption import encryption
from common.mailService import mailService
from userManage.dataUserManage import dataUserManage
from userManage.sqlUserManage import sqlUserManage
from userManage.servUserManage import servUserManage
from logManage.dataLogManage import dataLogManage
from logManage.sqlLogManage import sqlLogManage
from commManage.servCommManage import servCommManage
from companyManage.servCompanyManage import servCompanyManage
from companyManage.dataCompanyManage import dataCompanyManage


from commonApprovalManage.servCommonApprovalManage import servCommonApprovalManage


logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


# 1. 로그인 API
#
# Pameter
# 	- userId | String | 사용자 ID
# 	- passwd | String | 사용자 Password
@userManageApi.route("/login", methods=["POST"])
def login():
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 로그인 시작 ----------",
    )
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()

    sysCd = request.headers.get("sysCd")

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    dCommManage = dataCommonManage()
    sUserManage = sqlUserManage()
    dUserManage = dataUserManage()
    sLogManage = sqlLogManage()
    dLogManage = dataLogManage()
    msgServ = messageService()

    params = request.get_json()  # login parameter recv
    userId = params["userId"]
    passwd = params["passwd"]

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "request header sysCd : "
        + sysCd
        + " / request params data : "
        + commUtilServ.jsonDumps(params),
    )

    # System Code Check
    result, resultData = commServ.checkSystemCd(sysCd)
    if result == False:
        return resultData

    # 사용자 ID Check
    if commUtilServ.dataCheck(userId) == False:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 ID가 없습니다.", None
        )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "response : " + commUtilServ.jsonDumps(result),
        )

        return result

    # 사용자 비밀번호 Check
    if commUtilServ.dataCheck(passwd) == False:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 비밀번호가 없습니다.", None
        )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "response : " + commUtilServ.jsonDumps(result),
        )

        return result

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 사용자 정보를 가져온다. ----------",
    )
    resCd, msg, resData = servUserMana.getUserInfo(1, userId, sysCd)
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
            "Response : " + commUtilServ.jsonDumps(result),
        )

        return result

    if resData == None:
        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_454, "", None)
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 사용 여부를 비교 한다. ----------",
    )
    if resData["use_type"] != "Y":
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL,
            "삭제된 사용자입니다. 관리자에게 문의 하시기 바랍니다.",
            None,
        )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 2. 비밀번호를 비교 한다. ----------",
    )
    if resData["password"] != passwd:
        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_453, "", None)
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    userState = resData["user_state"]

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 3. 사용자 token을 생성 한다. ----------",
    )
    result = dUserManage.makeLoginResult(userState)  # 사용자 토큰을 생성 한다.

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 4. 사용자 테이블에 사용자의 token을 업데이트 한다. ----------",
    )
    query = sUserManage.uUserLogin(
        userId, result["token"], sysCd
    )  # 사용자 token 발행 및 DB 저장을 위한 Query 생성
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "uUserLogin Query : " + query,
    )

    resCd, msg, resData = dbms.execute(query)  # 사용자 token update Query 실행

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

    logData = dLogManage.makeLogData(
        procCode,
        constants.LOG_LEVEL_CODE_INFO,
        userId + " 사용자가 로그인 하였습니다.",
        util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
        userId,
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 5. 로그인 로그를 DB에 저장 한다. ----------",
    )
    query = sLogManage.iLogData(logData)
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "iLogData Query : " + query,
    )

    resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그 저장 Query 실행

    if resCd != 0:
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Database Error : " + msg,
        )

    result = commServ.makeReturnMessage(
        constants.REST_RESPONSE_CODE_ZERO, "", result
    )  # 로그인 성공 시 Response Data 생성

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "response : " + commUtilServ.jsonDumps(result),
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 로그인 종료 ----------",
    )
    return result


# 2. 로그아웃 API
#
# Parameter
# 	- userId | String | 사용자 ID
# 	- token | String | token
@userManageApi.route("/logout", methods=["GET"])
def logout():
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 로그아웃 시작 ----------",
    )
    commServ = commonService()
    servUserMana = servUserManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    dCommManage = dataCommonManage()
    sUserManage = sqlUserManage()
    sLogManage = sqlLogManage()
    dLogManage = dataLogManage()
    msgServ = messageService()
    commUtilServ = commUtilService()

    token = request.headers.get("token")
    sysCd = request.headers.get("sysCd")

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "Request header token : " + token + ", sysCd : " + sysCd,
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
    resCd, msg, resData = servUserMana.getUserInfo(2, token, sysCd)
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

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 3. 사용자 로그아웃 로그 데이터를 생성 한다. ----------",
    )
    # 사용자 로그아웃 메시지 생성
    logData = dLogManage.makeLogData(
        procCode,
        constants.LOG_LEVEL_CODE_INFO,
        resData["id"] + " 사용자가 로그아웃 하였습니다.",
        util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
        resData["id"],
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 4. 사용자를 로그아웃 시킨다. ----------",
    )
    # 사용자 로그아웃
    query = sUserManage.uUserLogout(token, sysCd)  # logout을 위한 사용자 확인 Query 생성
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "uUserLogout Query : " + query,
    )

    resCd, msg, resData = dbms.execute(query)  # 사용자 로그아웃 쿼리를 싱행한다.
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

    # 로그아웃 로그를 저장한다.
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 5. 사용자 로그아웃 로그 데이터를 저장한다. ----------",
    )
    query = sLogManage.iLogData(logData)
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "iLogData Query : " + query,
    )
    resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그아웃 로그를 저장한다.
    if resCd != 0:  # DB 에러 발생 시
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Database Error : " + commUtilServ.jsonDumps(msg),
        )

    result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "Response : " + commUtilServ.jsonDumps(result),
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 로그아웃 종료 ----------",
    )
    return result


# 3. 내 정보 제공 API
#
@userManageApi.route("/getMyInfo", methods=["GET"])
def getMyInfo():
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 사용자 정보 제공 시작 ----------",
        )
        commServ = commonService()
        servUserMana = servUserManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        commUtilServ = commUtilService()
        dCommManage = dataCommonManage()
        sUserManage = sqlUserManage()
        dUserManage = dataUserManage()
        msgServ = messageService()

        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
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
        resCd, msg, resData = servUserMana.getUserInfo(2, token, sysCd)
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

        if resData == None:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_455, "", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "response : " + commUtilServ.jsonDumps(result),
            )
            return result

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 3. 제공할 사용자 모델을 생성하고 기본정보를 생성한다. ----------",
        )
        resultData = dUserManage.makeUserInfoResult(resData)

        """
		# 등급/분야 정보를 Read 한다.
		logs.debug(procName,
				os.path.basename(__file__), 
				sys._getframe(0).f_code.co_name,
				u'---------- 4. 등급/분야 정보를 가져 온다.. ----------')
	
		resCd, msg, resData = servUserMana.getUserFieldRatingInfo(1, resData['id'])	# 사용자 정보 Read Query 생성
		if(resCd != 0):										# DB 에러 발생 시
			logs.war(procName,
					os.path.basename(__file__), 
					sys._getframe(0).f_code.co_name,
					u'Database Error : ' + commUtilServ.jsonDumps(msg))

			result = commServ.makeReturnMessage(resCd, msg, None)

			logs.debug(procName,
					os.path.basename(__file__), 
					sys._getframe(0).f_code.co_name,
					u'Response : ' + commUtilServ.jsonDumps(result))
			return result
	
		if(resData != None):
			resultData['field_rating'] = resData
		"""
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_ZERO, "", resultData
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 사용자 정보 제공 완료 ----------",
        )
        return result

    except Exception as e:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
        )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "Response : " + commUtilServ.jsonDumps(result),
    )

    return result


# 4. 회원 가입 API
#
@userManageApi.route("/joinUser", methods=["PUT"])
def addUser():
    servComApproMana = servCommonApprovalManage()
    servCompanyMana = servCompanyManage()
    dataCompanyMana = dataCompanyManage()
    servCommMana = servCommManage()
    commServ = commonService()
    servUserMana = servUserManage()
    #    servCompanyMana = servCompanyManage()
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 회원 가입 시작 ----------",
    )

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    try:

        msgServ = messageService()
        commUtilServ = commUtilService()
        dCommManage = dataCommonManage()
        sUserManage = sqlUserManage()
        dUserManage = dataUserManage()
        dLogManage = dataLogManage()
        sLogManage = sqlLogManage()

        sysCd = request.headers.get("sysCd")
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "request header sysCd : " + sysCd,
        )

        # System Code Check
        result, resultData = commServ.checkSystemCd(sysCd)
        if result == False:
            return resultData

        params = json.loads(request.form["data"], encoding="utf-8")  # json to dict

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "request header sysCd : "
            + sysCd
            + " / request params data : "
            + commUtilServ.jsonDumps(params),
        )

        ##########################################################################################################
        # 사용자 정보 관리
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- i. 사용자 모델을 생성 한다. ----------",
        )

        #### ID ####
        if commUtilServ.dataCheck(params["id"]) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "ID가 입력되지 않았습니다. ID를 입력 하여 주시기 바랍니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #### user_name ####
        if commUtilServ.dataCheck(params["user_name"]) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "이름이 입력되지 않았습니다. 이름을 입력하여 주시기 바랍니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #### password ####
        if commUtilServ.dataCheck(params["password"]) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "Password가 입력되지 않았습니다. Password를 입력하여 주시기 바랍니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #### user_contact ####
        if commUtilServ.dataCheck(params["user_contact"]) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "연락처가 입력되지 않았습니다. 연락처를 입력하여 주시기 바랍니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #### user_email ####
        if commUtilServ.dataCheck(params["user_email"]) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "E-Mail이 입력되지 않았습니다. E-Mail을 입력하여 주시기 바랍니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "response : " + commUtilServ.jsonDumps(result),
            )
            return result

        user_info = dUserManage.makeReqUserInfoModel()  # 사용자 정보 모델을 생성
        user_info["authority_code"] = constants.USER_INOCCUPATION  # 권한 코드(업무 구분)
        user_info["id"] = params["id"]  # ID
        user_info["user_name"] = params["user_name"]  # 이름
        user_info["password"] = params["password"]  # 패스워드
        user_info["user_contact"] = params["user_contact"]  # 연락처
        user_info["user_email"] = params["user_email"]  # 이메일

        #### user_position ####
        # if commUtilServ.dataCheck(params["user_position"]) != False:
        #    user_info["user_position"] = params["user_position"]  # 직위

        user_info["join_date"] = util_time.get_current_time(
            util_time.TIME_CURRENT_TYPE_14
        )  # 회원 가입 날짜

        # 사용자 기본 정보를 저장 한다.
        resCd, msg, resData = servUserMana.putUserInfo(user_info)
        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + msg,
            )

            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "사용자 정보를 등록 할 수 없습니다. 원인 : " + msg,
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "response : " + commUtilServ.jsonDumps(result),
            )
            return result

        # 사업자 등록 번호가 입력 되지 않았으면 회원 가입만 하고 종료
        if params["co_regisnum"] == "":
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_ZERO, "", None
            )

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 회원 가입 완료 ----------",
            )

            return result

        # 회사 정보가 있으면 권한 정보를 가져 온다.

        resCd, msg, codeName = servCommMana.getCodeName(params["authority_code"])
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

        # 사업자 등록 번호가 입력 되어 있으면 회사 생성 및 회사 가입 결재 요청

        # 등록된 회사 정보가 있는지 확인 한다.
        resCd, msg, resCoInfo = servCompanyMana.get_company_by_regisnum(
            params["co_regisnum"]
        )

        if resCd != 0:  # DB 에러 발생 시
            servUserMana.delUserInfo(user_info["id"])  # delete user info
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

        common_approval_manage = None
        if params["add_co_type"] == "N":  # 등록된 회사가 있슴 - 회사 가입
            if not resCoInfo:  # 회사 정보가 조회 되지 않으면 에러 처리
                servUserMana.delUserInfo(user_info["id"])  # delete user info
                msg = "조회된 회사 정보가 없습니다. 회사 정보를 확인 하시기 바랍니다."
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    msg,
                )

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, msg, None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "response : " + commUtilServ.jsonDumps(result),
                )
                return result

            data_co_info_modify_manage = {
                "userId": user_info["id"],
                "userName": user_info["user_name"],
                #                'userRegisnum'          : user_info['user_regisnum'],
                "userContact": user_info["user_contact"],
                "userEmail": user_info["user_email"],
                "beforeCoCode": "",
                "beforeCoName": "",
                "afterCoCode": resCoInfo["co_code"],
                "afterCoName": resCoInfo["co_name"],
                "after_authority_code": params["authority_code"],  # 권한 코드(업무 구분)
                "after_authority_name": codeName["subcode_name"],  # 권한 코드(업무 구분)
                "after_user_position": params["user_position"],  # 직위
            }

            searchList = []

            searchInfo = {"key": "CO_CODE", "value": resCoInfo["co_code"]}
            searchList.append(searchInfo)

            searchInfo = {"key": "MANAGER_TYPE", "value": "Y"}
            searchList.append(searchInfo)

            resCd, msg, managerUserInfo = servUserMana.searchUserInfoList(searchList)
            if resCd != 0:
                servUserMana.delUserInfo(user_info["id"])  # delete user info
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

            if len(managerUserInfo) == 0:
                servUserMana.delUserInfo(user_info["id"])  # delete user info
                msg = "관리자 권한을 가진 사람이 없습니다. 회사에 문의 하시기 바랍니다."
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    msg,
                )

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, msg, None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "response : " + commUtilServ.jsonDumps(result),
                )
                return result

            common_approval_manage = {
                "req_approval_id": user_info["id"],
                "req_approval_type": constants.COMM_APPRO_CD_SIGNUP,
                "approval_status": constants.APPRO_STATUS_CD_WAIT,
                "contents": data_co_info_modify_manage,
                "approval_id": managerUserInfo[0]["id"],
                "req_approval_date": util_time.get_current_time(
                    util_time.TIME_CURRENT_TYPE_14
                ),
                "complete_approval_date": "",
                "next_approval_info": "",
            }

        elif params["add_co_type"] == "Y":  # 등록된 회사가 없음 - 회사 등록

            if resCoInfo != None:  # 회사 정보가 조회 되지 않으면 에러 처리
                servUserMana.delUserInfo(user_info["id"])  # delete user info
                msg = "사업자 번호가 동일한 회사가 있습니다. 사업자 번호를 확인 하시기 바랍니다."
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    msg,
                )

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, msg, None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "response : " + commUtilServ.jsonDumps(result),
                )
                return result

            resCd, msg, coNum = servCommMana.createCoNum()

            if resCd != 0:
                servUserMana.delUserInfo(user_info["id"])  # delete user info
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

            resCd, msg, nextCoNum = servCommMana.increaseCoNum()
            if resCd != 0:
                servUserMana.delUserInfo(user_info["id"])  # delete user info
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

            # 회사 정보 관리
            company_info = dataCompanyMana.makeReqCompanyInfoModel()
            company_info["co_code"] = coCode + str(f"{coNum:06d}")
            company_info["co_name"] = params["co_name"]
            company_info["co_type"] = params["co_type"]
            company_info["ceo"] = params["co_ceo"]
            company_info["contact"] = params["co_contact"]
            company_info["address"] = params["co_address"]
            company_info["regisnum"] = params["co_regisnum"]
            company_info["after_authority_code"] = params[
                "authority_code"
            ]  # 권한 코드(업무 구분)
            company_info["after_authority_name"] = codeName[
                "subcode_name"
            ]  # 권한 코드(업무 구분)
            company_info["after_user_position"] = params["user_position"]  # 직위

            resCd, msg, resData = servCompanyMana.post_company(company_info)
            if resCd != 0:
                servUserMana.delUserInfo(user_info["id"])  # delete user info
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL,
                    "회사 정보를 등록 할 수 없습니다. 원인 : " + msg,
                    None,
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "response : " + commUtilServ.jsonDumps(result),
                )
                return result

            ##########################################################################################################
            # 회사 생성 승인을 위한 데이터 생성

            common_approval_manage = {
                "req_approval_id": user_info["id"],
                "req_approval_type": constants.COMM_APPRO_CD_CO_NEW,
                "approval_status": constants.APPRO_STATUS_CD_WAIT,
                "contents": company_info,
                "approval_id": "master",
                "req_approval_date": util_time.get_current_time(
                    util_time.TIME_CURRENT_TYPE_14
                ),
                "complete_approval_date": "",
                "next_approval_info": "",
            }

            ##########################################################################################################

        else:  # 데이터 에러 처리
            servUserMana.delUserInfo(user_info["id"])  # delete user info
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "잘못된 데이터가 입력 되었습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "response : " + commUtilServ.jsonDumps(result),
            )

            return result

        # 결재 정보를 저장 한다.
        resCd, msg, resData = servComApproMana.putCommonApprovalInfo(
            common_approval_manage
        )
        if resCd != 0:
            servUserMana.delUserInfo(user_info["id"])  # delete user info

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + msg,
            )

            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "결재 정보를 등록 할 수 없습니다. 원인 : " + msg,
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "response : " + commUtilServ.jsonDumps(result),
            )
            return result

        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 회원 가입 완료 ----------",
        )
        return result

    except Exception as e:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
        )
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "response : " + commUtilServ.jsonDumps(result),
        )

    return result


# 5. ID 중복 체크
@userManageApi.route("/chkUserId/<userId>", methods=["GET"])
def chkUserId(userId):

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- ID 중복 체크 시작  ----------",
    )
    try:
        sysCd = request.headers.get("sysCd")

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        sUserManage = sqlUserManage()
        dUserManage = dataUserManage()
        dCommManage = dataCommonManage()
        commUtilServ = commUtilService()
        commServ = commonService()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "request header sysCd : " + sysCd + " / request url userId : " + userId,
        )

        # System Code Check
        result, resultData = commServ.checkSystemCd(sysCd)
        if result == False:
            return resultData

        # userId Check
        if commUtilServ.dataCheck(userId) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 ID가 없습니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "response : " + commUtilServ.jsonDumps(result),
            )

            return result

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "1. 사용자 ID가 있는지 확인 한다.",
        )
        query = sUserManage.sChkUserId(userId)  # 사용자 ID 중복 체크 Query 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sChkUserId Query : " + query,
        )

        resCd, msg, resData = dbms.queryForObject(query)
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

        resultData = dUserManage.makeUserCntResult(resData)

        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_ZERO, "", resultData
        )

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

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "Response : " + commUtilServ.jsonDumps(result),
    )
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- ID 중복 체크 완료 ----------",
    )
    return result


# 6. 회원 정보 수정
#
@userManageApi.route("/modifyUser", methods=["POST"])
def modifyUser():

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 회원 정보 수정 시작  ----------",
    )
    commServ = commonService()
    servUserMana = servUserManage()
    query = ""

    dataCompanyMana = dataCompanyManage()

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

    token = request.headers.get("token")
    sysCd = request.headers.get("sysCd")

    servCommMana = servCommManage()
    msgServ = messageService()
    commUtilServ = commUtilService()
    dCommManage = dataCommonManage()
    sUserManage = sqlUserManage()
    dUserManage = dataUserManage()
    dLogManage = dataLogManage()
    sLogManage = sqlLogManage()
    servComApproMana = servCommonApprovalManage()
    servCompanyMana = servCompanyManage()

    try:

        # 1. 데이터 수신
        params = json.loads(request.form["data"], encoding="utf-8")  # json to dict

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
            "---------- 로그인 된 사용자인지 체크 한다. ----------",
        )
        # 로그인 된 사용자 인지 확인한다.
        result, resultData = commServ.userLoginChk(token, sysCd)
        if result == False:
            return resultData

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "시자자자자자작",
        )
        # 3. 내 정보를 가져 온다.
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 사용자 정보를 가져온다. ----------",
        )
        # 사용자 정보를 가져 온다.
        resCd, msg, resDataUserInfo = servUserMana.getUserInfo(2, token, sysCd)
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

        if resDataUserInfo == None:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_455, "", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "response : " + commUtilServ.jsonDumps(result),
            )
            return result

        # ID에 대해 오래된 데이터를 가져 온다.
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 사용자 정보를 가져온다. ----------",
        )
        # 사용자 정보를 가져 온다.
        resCd, msg, resDataOldUserInfo = servUserMana.getUserInfo(
            1, params["id"], sysCd
        )
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

        if resDataOldUserInfo == None:
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
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "시자자자자자작",
        )
        # 4. 수신받은 데이터 ID와 내 정보 ID를 비교 한다.
        common_approval_manage = None
        data_user_info_manage = dUserManage.makeReqUserInfoModel()  # 사용자 정보 모델을 생성
        if params["id"] == resDataUserInfo["id"]:
            # 5. ID 동일 시 내 정보를 업데이트 한다.
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 4-1. 수정된 데이터의 ID와 내 정보 ID가 동일한 경우 내 정보를 업데이트 한다. ----------",
            )
            ##########################################################################################################
            # 사용자 정보 관리
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- i. 사용자 모델을 생성 한다. ----------",
            )

            data_user_info_manage["id"] = resDataUserInfo["id"]  # ID
            if params["password"] != "" and (
                resDataUserInfo["password"] != params["password"]
            ):
                data_user_info_manage["password"] = params["password"]  # 패스워드
            else:
                data_user_info_manage["password"] = resDataUserInfo["password"]  # 패스워드

            data_user_info_manage["user_name"] = resDataUserInfo["user_name"]  # 이름
            data_user_info_manage["user_contact"] = params["user_contact"]  # 연락처
            data_user_info_manage["user_email"] = params["user_email"]  # 이메일

            if resDataUserInfo["manager_type"] == "Y":
                data_user_info_manage["authority_code"] = params["authority_code"]
                data_user_info_manage["user_position"] = params["user_position"]

            # data_user_info_manage['use_type']		= params['use_type']		# 사용 여부
            #            data_user_info_manage["user_type"] = params["user_type"]  # 사용자 구분 타입

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "manager_type : " + resDataUserInfo["manager_type"],
            )
            if resDataUserInfo["manager_type"] != "Y":

                if (
                    params["authority_code"] != resDataUserInfo["authority_code"]
                    or params["user_position"] != resDataUserInfo["user_position"]
                    or params["co_code"] != resDataUserInfo["co_code"]
                ):
                    reqApprovalType = constants.COMM_APPRO_CD_MY_MODIFY
                    next_common_approval_manage = ""

                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "시자자자자자작",
                    )
                    appro_user_info_manage = {
                        #        "id": data_user_info_manage["id"],
                        #        "user_name": data_user_info_manage["user_name"],
                        "userId": data_user_info_manage["id"],
                        "userName": data_user_info_manage["user_name"],
                        "userContact": data_user_info_manage["user_contact"],
                        "userEmail": data_user_info_manage["user_email"],
                        "before_user_position": "",
                        "after_user_position": "",
                        "before_authority_code": "",
                        "before_authority_name": "",
                        "after_authority_code": "",
                        "after_authority_name": "",
                    }

                    appro_user_info_manage["after_authority_code"] = params[
                        "authority_code"
                    ]
                    resCd, msg, coName = servCommMana.getCodeName(
                        params["authority_code"]
                    )
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

                    appro_user_info_manage["after_authority_name"] = coName[
                        "subcode_name"
                    ]

                    if params["authority_code"] != resDataUserInfo["authority_code"]:

                        appro_user_info_manage[
                            "before_authority_code"
                        ] = resDataUserInfo["authority_code"]
                        appro_user_info_manage[
                            "before_authority_name"
                        ] = resDataUserInfo["authority_name"]

                    appro_user_info_manage["after_user_position"] = params[
                        "user_position"
                    ]
                    if params["user_position"] != resDataUserInfo["user_position"]:
                        appro_user_info_manage[
                            "before_user_position"
                        ] = resDataUserInfo["user_position"]

                    searchList = []

                    if params["co_code"] != "":
                        searchInfo = {"key": "CO_CODE", "value": params["co_code"]}
                        searchList.append(searchInfo)
                    else:
                        searchInfo = {
                            "key": "CO_CODE",
                            "value": resDataUserInfo["co_code"],
                        }
                        searchList.append(searchInfo)

                    searchInfo = {"key": "MANAGER_TYPE", "value": "Y"}
                    searchList.append(searchInfo)

                    curApproUserInfo = ""

                    resCd, msg, managerUserInfo = servUserMana.searchUserInfoList(
                        searchList
                    )
                    curApproUserInfo = managerUserInfo
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

                    if len(managerUserInfo) == 0:
                        # servUserMana.delUserInfo(user_info['id'])				# delete user info
                        msg = "관리자 권한을 가진 사람이 없습니다. 회사에 문의 하시기 바랍니다."
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            msg,
                        )

                        result = commServ.makeReturnMessage(
                            constants.REST_RESPONSE_CODE_DATAFAIL, msg, None
                        )
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )
                        return result

                    # 무직에서 회사 입사 시
                    if params["co_code"] != "" and resDataUserInfo["co_code"] == "":
                        reqApprovalType = constants.COMM_APPRO_CD_SIGNUP
                        appro_user_info_manage["beforeCoCode"] = ""
                        appro_user_info_manage["beforeCoName"] = ""
                        appro_user_info_manage["afterCoCode"] = managerUserInfo[0][
                            "co_code"
                        ]
                        appro_user_info_manage["afterCoName"] = managerUserInfo[0][
                            "co_name"
                        ]

                        curApproUserInfo = managerUserInfo

                    # 기존 회사에서 회사 퇴사 시
                    elif params["co_code"] == "" and resDataUserInfo["co_code"] != "":
                        reqApprovalType = constants.COMM_APPRO_CD_LEAVE
                        appro_user_info_manage["beforeCoCode"] = managerUserInfo[0][
                            "co_code"
                        ]
                        appro_user_info_manage["beforeCoName"] = managerUserInfo[0][
                            "co_name"
                        ]
                        appro_user_info_manage["afterCoCode"] = ""
                        appro_user_info_manage["afterCoName"] = ""

                        curApproUserInfo = managerUserInfo

                    # 기존 회사에서 다른 회사로 이직 시
                    elif params["co_code"] != resDataUserInfo["co_code"]:
                        searchList = []
                        searchInfo = {
                            "key": "CO_CODE",
                            "value": resDataUserInfo["co_code"],
                        }
                        searchList.append(searchInfo)

                        searchInfo = {"key": "MANAGER_TYPE", "value": "Y"}
                        searchList.append(searchInfo)
                        (
                            resCd,
                            msg,
                            next_managerUserInfo,
                        ) = servUserMana.searchUserInfoList(searchList)
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

                        reqApprovalType = constants.COMM_APPRO_CD_LEAVE

                        curApproUserInfo = next_managerUserInfo
                        next_managerUserInfo = managerUserInfo

                        appro_user_info_manage["beforeCoCode"] = curApproUserInfo[0][
                            "co_code"
                        ]
                        appro_user_info_manage["beforeCoName"] = curApproUserInfo[0][
                            "co_name"
                        ]
                        appro_user_info_manage["afterCoCode"] = ""
                        appro_user_info_manage["afterCoName"] = ""

                        next_appro_user_info_manage = {
                            "userId": appro_user_info_manage["userId"],
                            "userName": appro_user_info_manage["userName"],
                            "userContact": data_user_info_manage["user_contact"],
                            "userEmail": data_user_info_manage["user_email"],
                            "after_user_position": appro_user_info_manage[
                                "after_user_position"
                            ],
                            "after_authority_code": appro_user_info_manage[
                                "after_authority_code"
                            ],
                            "after_authority_name": appro_user_info_manage[
                                "after_authority_name"
                            ],
                            "afterCoCode": next_managerUserInfo[0]["co_code"],
                            "afterCoName": next_managerUserInfo[0]["co_name"],
                        }

                        next_common_approval_manage = {
                            "req_approval_id": data_user_info_manage["id"],
                            "req_approval_type": constants.COMM_APPRO_CD_SIGNUP,
                            "approval_status": constants.APPRO_STATUS_CD_WAIT,
                            "contents": next_appro_user_info_manage,
                            "approval_id": next_managerUserInfo[0]["id"],
                            "req_approval_date": util_time.get_current_time(
                                util_time.TIME_CURRENT_TYPE_14
                            ),
                            "complete_approval_date": "",
                            "next_approval_info": "",
                        }

                    common_approval_manage = {
                        "req_approval_id": data_user_info_manage["id"],
                        "req_approval_type": reqApprovalType,
                        "approval_status": constants.APPRO_STATUS_CD_WAIT,
                        "contents": appro_user_info_manage,
                        "approval_id": curApproUserInfo[0]["id"],
                        "req_approval_date": util_time.get_current_time(
                            util_time.TIME_CURRENT_TYPE_14
                        ),
                        "complete_approval_date": "",
                        "next_approval_info": next_common_approval_manage,
                    }

                    # 결재 정보를 저장 한다.
                    resCd, msg, resData = servComApproMana.putCommonApprovalInfo(
                        common_approval_manage
                    )
                    if resCd != 0:

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        result = commServ.makeReturnMessage(
                            constants.REST_RESPONSE_CODE_DATAFAIL,
                            "결재 정보를 등록 할 수 없습니다. 원인 : " + msg,
                            None,
                        )
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )
                        return result

        elif resDataUserInfo["authority_code"] == constants.USER_AUTH_SYSMANAGE:
            # 7. 관리자 권한 시 사용자 정보를 수정한다.
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 4-2. 관리자 권한일 경우 사용자 정보를 업데이트 한다. ----------",
            )
            # data_user_info_manage['user_regisnum']	= resDataOldUserInfo['user_regisnum']	# 주민등록번호
            data_user_info_manage["id"] = resDataOldUserInfo["id"]  # ID
            if params["password"] != "" and (
                resDataOldUserInfo["password"] != params["password"]
            ):
                data_user_info_manage["password"] = params["password"]  # 패스워드
            else:
                data_user_info_manage["password"] = resDataOldUserInfo[
                    "password"
                ]  # 패스워드
            data_user_info_manage["user_name"] = resDataOldUserInfo["user_name"]  # 이름
            data_user_info_manage["user_position"] = params["user_position"]  # 직위
            data_user_info_manage["user_contact"] = params["user_contact"]  # 연락처
            data_user_info_manage["user_email"] = params["user_email"]  # 이메일
            # data_user_info_manage['user_state']		= params['user_state']		# 사용자 상태
            # data_user_info_manage['use_type']		= params['use_type']		# 사용 여부
            data_user_info_manage["user_type"] = params["user_type"]  # 사용자 구분 타입
            data_user_info_manage["employ_status"] = resDataOldUserInfo[
                "employ_status"
            ]  # 재직여부

            """
			if(params['employ_status'] == constants.EMPLOY_STATUS_CD_N):
				data_user_info_manage['authority_code'] = resDataOldUserInfo['authority_code']	# 권한 코드(업무 구분)
			else:
				data_user_info_manage['authority_code'] = params['authority_code']	# 권한 코드(업무 구분)
			"""

        elif (
            resDataUserInfo["authority_code"] == constants.USER_AUTH_CONTRACTOR
            or resDataUserInfo["authority_code"] == constants.USER_AUTH_SUPERVISOR
        ):
            # 8. 권한이 감리자 또는 시공자 이면서 회사명이 같으면 사용자 정보를 수정 할 수 있다.
            if resDataUserInfo["co_code"] == resDataOldUserInfo["co_code"]:
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "---------- 4-3. 권한이 감리자 또는 시공자이면서 회사코드가 동일할 경우 사용자 정보를 업데이트 한다. ----------",
                )
                # data_user_info_manage['user_regisnum']	= resDataOldUserInfo['user_regisnum']	# 주민등록번호
                data_user_info_manage["id"] = resDataOldUserInfo["id"]  # ID
                if params["password"] != "" and (
                    resDataOldUserInfo["password"] != params["password"]
                ):
                    data_user_info_manage["password"] = params["password"]  # 패스워드
                else:
                    data_user_info_manage["password"] = resDataOldUserInfo[
                        "password"
                    ]  # 패스워드
                data_user_info_manage["user_name"] = resDataOldUserInfo[
                    "user_name"
                ]  # 이름
                data_user_info_manage["user_position"] = params["user_position"]  # 직위
                data_user_info_manage["user_contact"] = params["user_contact"]  # 연락처
                data_user_info_manage["user_email"] = params["user_email"]  # 이메일
                data_user_info_manage["user_state"] = params["user_state"]  # 사용자 상태
                # data_user_info_manage['use_type']		= params['use_type']		# 사용 여부
                data_user_info_manage["user_type"] = params["user_type"]  # 사용자 구분 타입
                # data_user_info_manage['employ_status']	= resDataOldUserInfo['employ_status']			# 재직여부

                """
				if(params['employ_status'] == constants.EMPLOY_STATUS_CD_N):
					data_user_info_manage['authority_code'] = resDataOldUserInfo['authority_code']	# 권한 코드(업무 구분)
				else:
					data_user_info_manage['authority_code'] = params['authority_code']	# 권한 코드(업무 구분)
				"""
            else:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "사용자 정보 수정 권한이 없습니다.",
                )

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 정보 수정 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )
                return result

        elif (
            resDataUserInfo["authority_code"] == constants.USER_AUTH_CONTRACTOR_MONITOR
        ) or (
            resDataUserInfo["authority_code"] == constants.USER_AUTH_SUPERVISOR_MONITOR
        ):
            # 권한이 감리자 모니터링 또는 시공자 모니터링 이면서 회사명이 같고 권한이 시공자 또는 감리원이면 사용자 정보를 수정 할 수있다.
            if resDataUserInfo["co_code"] == resDataOldUserInfo["co_code"]:
                if (
                    resDataOldUserInfo["authority_code"]
                    == constants.USER_AUTH_CONTRACTION
                ) or (
                    resDataOldUserInfo["authority_code"]
                    == constants.USER_AUTH_SUPERVISING
                ):
                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "---------- 4-3. 권한이 감리자 모니터링 또는 시공자 모니터링이면서 회사명이 같고 권한기 시공자 또는 람리원이면 사용자 정보를 수정 할 수 있다. ----------",
                    )
                    # data_user_info_manage['user_regisnum']	= resDataOldUserInfo['user_regisnum']	# 주민등록번호
                    data_user_info_manage["id"] = resDataOldUserInfo["id"]  # ID
                    data_user_info_manage["password"] = params["password"]  # 패스워드
                    data_user_info_manage["user_name"] = resDataOldUserInfo[
                        "user_name"
                    ]  # 이름
                    data_user_info_manage["user_position"] = params[
                        "user_position"
                    ]  # 직위
                    data_user_info_manage["user_contact"] = params[
                        "user_contact"
                    ]  # 연락처
                    data_user_info_manage["user_email"] = params["user_email"]  # 이메일
                    data_user_info_manage["user_state"] = params["user_state"]  # 사용자 상태
                    # data_user_info_manage['use_type']		= params['use_type']		# 사용 여부
                    data_user_info_manage["user_type"] = params[
                        "user_type"
                    ]  # 사용자 구분 타입
                    # data_user_info_manage['employ_status']	= resDataOldUserInfo['employ_status']			# 재직여부

                    """
					if(params['employ_status'] == constants.EMPLOY_STATUS_CD_N):
						data_user_info_manage['authority_code'] = resDataOldUserInfo['authority_code']	# 권한 코드(업무 구분)
					else:
						data_user_info_manage['authority_code'] = params['authority_code']	# 권한 코드(업무 구분)
					"""
                else:
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "사용자 정보 수정 권한이 없습니다.",
                    )

                    result = commServ.makeReturnMessage(
                        constants.REST_RESPONSE_CODE_DATAFAIL,
                        "사용자 정보 수정 권한이 없습니다.",
                        None,
                    )

                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Response : " + commUtilServ.jsonDumps(result),
                    )
                    return result

            else:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "사용자 정보 수정 권한이 없습니다.",
                )

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 정보 수정 권한이 없습니다.", None
                )

                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )
                return result
        else:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "사용자 정보 수정 권한이 없습니다.",
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 정보 수정 권한이 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        ##########################################################################################################
        # 사용자 파일 정보 관리
        #        logs.debug(
        #           procName,
        #          os.path.basename(__file__),
        #         sys._getframe(0).f_code.co_name,
        #        "---------- 6. 파일 정보를 수정 한다. ----------",
        #   )
        #  data_user_file_info_manage = dUserManage.makeReqUserFileInfoModel()
        # data_user_file_info_manage["id"] = params["id"]

        """
		# 싸인		
		if(params['sign_status'] == 'C'):
			lpath, origName, changeName = servUserMana.userFileNameManage(params['id'], params, 'sign_name_new')

			data_user_file_info_manage['sign_path'] = lpath
			data_user_file_info_manage['sign_original_name'] = origName 
			data_user_file_info_manage['sign_change_name'] = changeName
		elif(params['sign_status'] == 'D'):
			data_user_file_info_manage['sign_path'] = '' 
			data_user_file_info_manage['sign_original_name'] = '' 
			data_user_file_info_manage['sign_change_name']	= ''
		else:
			data_user_file_info_manage['sign_path'] = resDataOldUserInfo['sign_path'] 
			data_user_file_info_manage['sign_original_name'] = resDataOldUserInfo['sign_original_name'] 
			data_user_file_info_manage['sign_change_name']	= resDataOldUserInfo['sign_change_name'] 
			

		# 등록수첩		
		if(params['user_license_status'] == 'C'):
			lpath, origName, changeName = servUserMana.userFileNameManage(params['id'], params, 'user_license_name_new')

			data_user_file_info_manage['user_license_path'] = lpath
			data_user_file_info_manage['user_license_original_name'] = origName 
			data_user_file_info_manage['user_license_change_name'] = changeName
		elif(params['user_license_status'] == 'D'):
			data_user_file_info_manage['user_license_path'] = ''
			data_user_file_info_manage['user_license_original_name'] = '' 
			data_user_file_info_manage['user_license_change_name'] = ''
		else:
			data_user_file_info_manage['user_license_path'] = resDataOldUserInfo['user_license_path'] 
			data_user_file_info_manage['user_license_original_name'] = resDataOldUserInfo['user_license_original_name'] 
			data_user_file_info_manage['user_license_change_name']	= resDataOldUserInfo['user_license_change_name'] 

		##########################################################################################################


			
		##########################################################################################################
		# 사용자 분야/등급 정보 관리

		data_user_field_rating_info_manage = []

		for frinfo in params['field_rating']:
			data_frinfo = dUserManage.makeFieldRatingModel()
			data_frinfo['id']	= data_user_info_manage['id']
			data_frinfo['field'] = frinfo['field']
			data_frinfo['rating'] = frinfo['rating']
			data_user_field_rating_info_manage.append(data_frinfo)
		##########################################################################################################


		common_approval_manage = None
		data_co_info_manage = None
		"""
        ##########################################################################################################
        # 회사 정보 관리
        # 1. 무직인 경우
        """
		if(params['employ_status'] == constants.EMPLOY_STATUS_CD_N):

			if(resDataOldUserInfo['manager_type'] == 'Y'):
				result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
						u'관리자는 탈퇴 할 수 없습니다.',
						None)
	
				return result
				

			data_co_info_manage = {
				'userId'			: resDataOldUserInfo['id'],
				'userName'			: resDataOldUserInfo['user_name'],
				'userRegisnum'		: resDataOldUserInfo['user_regisnum'],
				'userContact'		: resDataOldUserInfo['user_contact'],
				'userEmail'			: resDataOldUserInfo['user_email'],
				#'userFieldRating'	: resDataOldUserInfo['field_rating'],
				'beforeCoCode'		: resDataOldUserInfo['co_code'],
				'beforeCoName'		: resDataOldUserInfo['co_name'],
				'afterCoCode'		: '',
				'afterCoName'		: '',
				'inviteType'		: 'N'
			}

			searchList = []
			searchInfo = {
				'key' : 'CO_CODE',
				'value' : resDataOldUserInfo['co_code']
			}
			searchList.append(searchInfo)
			searchInfo = {
				'key' : 'MANAGER_TYPE',
				'value' : 'Y'
			}
			searchList.append(searchInfo)

			resCd, msg, managerUserInfo = servUserMana.searchUserInfoList(searchList)
			if(resCd != 0):
				logs.war(procName,
						os.path.basename(__file__),
						sys._getframe(0).f_code.co_name,
						u'Database Error : ' + msg)
		
				result = commServ.makeReturnMessage(resCd, msg, None)
				logs.war(procName,
						os.path.basename(__file__),
						sys._getframe(0).f_code.co_name,
						u'response : ' + commUtilServ.jsonDumps(result))
				return result
			
			
			common_approval_manage = {
				'req_approval_id' : resDataOldUserInfo['id'],
				'req_approval_type' : constants.COMM_APPRO_CD_WITHDRAWAL,
				'approval_status' : constants.APPRO_STATUS_CD_WAIT,
				'contents' : data_co_info_manage,
				'approval_id' : managerUserInfo[0]['id'],
				'req_approval_date' : util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
				'complete_approval_date' : '',
				'next_approval_info' : ''
			}
		else:
			# 2-1. 회사가 변경 되지 않은 경우
			if(resDataOldUserInfo['co_regisnum'] == params['co_regisnum']):
				data_user_info_manage['co_code']		= resDataOldUserInfo['co_code']	# 회사 코드
			# 2-2. 회사를 직접 인력인 경우
			elif(params['add_co_type'] == 'Y'):
				searchList = []
	
				searchInfo = {
					'key' : 'CO_REGISNUM',
					'value' : params['co_regisnum']
				}
				searchList.append(searchInfo)
	
				# 2-2-1. 등록된 회사 정보가 있는지 확인 한다.
				resCd, msg, resCoInfo = servUserMana.getCoInfo(searchList)
		
				if(resCd != 0):										# DB 에러 발생 시
					logs.war(procName,
						os.path.basename(__file__), 
						sys._getframe(0).f_code.co_name,
						u'Database Error : ' + commUtilServ.jsonDumps(msg))
	
		
					result = commServ.makeReturnMessage(resCd, msg, None)
		
					logs.debug(procName,
							os.path.basename(__file__), 
							sys._getframe(0).f_code.co_name,
							u'Response : ' + commUtilServ.jsonDumps(result))
					return result
				
				# 2-2-2. 회사 정보가 있으면 에러를 리턴 한다.
				if(resCoInfo != None):
					result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
							u'입력하신 사업자 등록번호는 ' + resCoInfo['co_name']  + ' 사업자 등록번호와 동일 합니다.',
							None)
					return result


				# 2-2-3. 무직에서 회사를 등록 한 경우
				if(resDataOldUserInfo['co_code'] == ''):
					resCd, msg, common_approval_manage = makeNewCompanyDataInfo(params)
					if(resCd != 0):
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'Database Error : ' + msg)
					
						result = commServ.makeReturnMessage(resCd, msg, None)
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'response : ' + commUtilServ.jsonDumps(result))
						return result
				# 2-2-4. 회사 소속으로 회사를 등록한 경우  
				else:
					resCd, msg, next_common_approval_manage = makeNewCompanyDataInfo(params)
					if(resCd != 0):
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'Database Error : ' + msg)
					
						result = commServ.makeReturnMessage(resCd, msg, None)
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'response : ' + commUtilServ.jsonDumps(result))
						return result

					searchList = []
	
					searchInfo = {
						'key' : 'CO_CODE',
						'value' : resDataOldUserInfo['co_code']
					}
					searchList.append(searchInfo)
	
					searchInfo = {
						'key' : 'MANAGER_TYPE',
						'value' : 'Y'
					}
					searchList.append(searchInfo)
		
					resCd, msg, managerOldUserInfo = servUserMana.searchUserInfoList(searchList)
					if(resCd != 0):
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'Database Error : ' + msg)
				
						result = commServ.makeReturnMessage(resCd, msg, None)
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'response : ' + commUtilServ.jsonDumps(result))
						return result

					data_withdraw_co_info_manage = {
						'userId'			: resDataOldUserInfo['id'],
						'userName'			: resDataOldUserInfo['user_name'],
						'userRegisnum'		: resDataOldUserInfo['user_regisnum'],
						'userContact'		: resDataOldUserInfo['user_contact'],
						'userEmail'			: resDataOldUserInfo['user_email'],
						#'userFieldRating'	: resDataOldUserInfo['field_rating'],
						'beforeCoCode'		: resDataOldUserInfo['co_code'],
						'beforeCoName'		: resDataOldUserInfo['co_name'],
						'afterCoCode'		: '',
						'afterCoName'		: '',
						'inviteType'		: '',
					}

					common_approval_manage = {
						'req_approval_id' : data_user_info_manage['id'],
						'req_approval_type' : constants.COMM_APPRO_CD_WITHDRAWAL,
						'approval_status' : constants.APPRO_STATUS_CD_WAIT,
						'contents' : data_withdraw_co_info_manage,
						'approval_id' : managerOldUserInfo[0]['id'],
						'req_approval_date' : util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
						'complete_approval_date' : '',
						'next_approval_info' : next_common_approval_manage
					}

			# 2-3. 회사를 검색 한 경우
			elif(params['add_co_type'] == 'N'):
				# 검색된 회사 관리자 검색
				searchList = []
	
				searchInfo = {
					'key' : 'CO_CODE',
					'value' : params['co_code']
				}
				searchList.append(searchInfo)
	
				searchInfo = {
					'key' : 'MANAGER_TYPE',
					'value' : 'Y'
				}
				searchList.append(searchInfo)
		
				resCd, msg, managerUserInfo = servUserMana.searchUserInfoList(searchList)
				if(resCd != 0):
					logs.war(procName,
							os.path.basename(__file__),
							sys._getframe(0).f_code.co_name,
							u'Database Error : ' + msg)
					
					result = commServ.makeReturnMessage(resCd, msg, None)
					logs.war(procName,
							os.path.basename(__file__),
							sys._getframe(0).f_code.co_name,
							u'response : ' + commUtilServ.jsonDumps(result))
					return result

				# 무직에서 회사 검색	
				if(resDataOldUserInfo['co_regisnum'] == ''):

					data_co_info_manage = {
						'userId'				: resDataOldUserInfo['id'],
						'userName'				: resDataOldUserInfo['user_name'],
						'userRegisnum'			: resDataOldUserInfo['user_regisnum'],
						'userContact'			: resDataOldUserInfo['user_contact'],
						'userEmail'				: resDataOldUserInfo['user_email'],
					#	'userFieldRating'		: resDataOldUserInfo['field_rating'],
						'userLicensePath'		: resDataOldUserInfo['user_license_path'],
						'userLicenseOrigName'	: resDataOldUserInfo['user_license_original_name'],
						'userLicenseChanName'	: resDataOldUserInfo['user_license_change_name'],
						'signLicensePath'		: resDataOldUserInfo['sign_path'],
						'signLicenseOrigName'	: resDataOldUserInfo['sign_original_name'],
						'signLicenseChanName'	: resDataOldUserInfo['sign_change_name'],
						'beforeCoCode'			: '',
						'beforeCoName'			: '',
						'afterCoCode'			: managerUserInfo[0]['co_code'],
						'afterCoName'			: managerUserInfo[0]['co_name']
					}

					common_approval_manage = {
						'req_approval_id' : data_user_info_manage['id'],
						'req_approval_type' : constants.COMM_APPRO_CD_SIGNUP,
						'approval_status' : constants.APPRO_STATUS_CD_WAIT,
						'contents' : data_co_info_manage,
						'approval_id' : managerUserInfo[0]['id'],
						'req_approval_date' : util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
						'complete_approval_date' : '',
						'next_approval_info' : ''
					}
				
				# 재직 중 다른 회사 검색	
				else : 
					# 검색된 회사 관리자 검색
					searchList = []
		
					searchInfo = {
						'key' : 'CO_CODE',
						'value' : params['co_code']
					}
					searchList.append(searchInfo)
		
					searchInfo = {
						'key' : 'MANAGER_TYPE',
						'value' : 'Y'
					}
					searchList.append(searchInfo)
			
					resCd, msg, managerUserInfo = servUserMana.searchUserInfoList(searchList)
					if(resCd != 0):
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'Database Error : ' + msg)
					
						result = commServ.makeReturnMessage(resCd, msg, None)
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'response : ' + commUtilServ.jsonDumps(result))
						return result
	
					data_co_info_manage = {
						'userId'				: resDataOldUserInfo['id'],
						'userName'				: resDataOldUserInfo['user_name'],
						'userRegisnum'			: resDataOldUserInfo['user_regisnum'],
						'userContact'			: resDataOldUserInfo['user_contact'],
						'userEmail'				: resDataOldUserInfo['user_email'],
						#'userFieldRating'		: resDataOldUserInfo['field_rating'],
						'userLicensePath'		: resDataOldUserInfo['user_license_path'],
						'userLicenseOrigName'	: resDataOldUserInfo['user_license_original_name'],
						'userLicenseChanName'	: resDataOldUserInfo['user_license_change_name'],
						'signLicensePath'		: resDataOldUserInfo['sign_path'],
						'signLicenseOrigName'	: resDataOldUserInfo['sign_original_name'],
						'signLicenseChanName'	: resDataOldUserInfo['sign_change_name'],
						'beforeCoCode'			: '',
						'beforeCoName'			: '',
						'afterCoCode'			: managerUserInfo[0]['co_code'],
						'afterCoName'			: managerUserInfo[0]['co_name'],
						'inviteType' : 'N'
					}

					next_common_approval_manage = {
						'req_approval_id' : data_user_info_manage['id'],
						'req_approval_type' : constants.COMM_APPRO_CD_SIGNUP,
						'approval_status' : constants.APPRO_STATUS_CD_WAIT,
						'contents' : data_co_info_manage,
						'approval_id' : managerUserInfo[0]['id'],
						'req_approval_date' : util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
						'complete_approval_date' : '',
						'next_approval_info' : ''
					}
	
					data_withdraw_co_info_manage = {
						'userId'			: resDataOldUserInfo['id'],
						'userName'			: resDataOldUserInfo['user_name'],
						'userRegisnum'		: resDataOldUserInfo['user_regisnum'],
						'userContact'		: resDataOldUserInfo['user_contact'],
						'userEmail'			: resDataOldUserInfo['user_email'],
						#'userFieldRating'	: resDataOldUserInfo['field_rating'],
						'beforeCoCode'		: resDataOldUserInfo['co_code'],
						'beforeCoName'		: resDataOldUserInfo['co_name'],
						'afterCoCode'		: '',
						'afterCoName'		: '',
						'inviteType'		: 'N'
					}

					# 검색된 회사 관리자 검색
					searchList = []
		
					searchInfo = {
						'key' : 'CO_CODE',
						'value' : resDataOldUserInfo['co_code']
					}
					searchList.append(searchInfo)
		
					searchInfo = {
						'key' : 'MANAGER_TYPE',
						'value' : 'Y'
					}
					searchList.append(searchInfo)
			
					resCd, msg, managerOldUserInfo = servUserMana.searchUserInfoList(searchList)
					if(resCd != 0):
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'Database Error : ' + msg)
						
						result = commServ.makeReturnMessage(resCd, msg, None)
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'response : ' + commUtilServ.jsonDumps(result))
						return result

					common_approval_manage = {
						'req_approval_id' : data_user_info_manage['id'],
						'req_approval_type' : constants.COMM_APPRO_CD_WITHDRAWAL,
						'approval_status' : constants.APPRO_STATUS_CD_WAIT,
						'contents' : data_withdraw_co_info_manage,
						'approval_id' : managerOldUserInfo[0]['id'],
						'req_approval_date' : util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
						'complete_approval_date' : '',
						'next_approval_info' : next_common_approval_manage
					}


			else:
				result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
						u'잘못된 정보가 입력 되었습니다.',
						None)
				return result
		"""

        ##########################################################################################################
        # 데이터를 저장 한다.

        # 사용자 기본 정보를 수정 한다.
        resCd, msg, resData = servUserMana.updateUserInfo(data_user_info_manage)
        if resCd != 0:
            if common_approval_manage != None:
                servComApproMana.delCommonApprovalInfo(common_approval_manage)

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + msg,
            )

            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "사용자 정보를 수정 할 수 없습니다. 원인 : " + msg,
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "response : " + commUtilServ.jsonDumps(result),
            )
            return result

        """
		# 사용자 분야/등급을 수정 한다.
		resCd, msg, oldFieldRatingInfo = servUserMana.getUserFieldRatingInfo(1, data_user_info_manage['id']) # 사용자 분야/등급 정보를 불러 온다.
		if(resCd != 0):										# DB 에러 발생 시
			logs.war(procName,
					os.path.basename(__file__), 
					sys._getframe(0).f_code.co_name,
					u'Database Error : ' + commUtilServ.jsonDumps(msg))

			result = commServ.makeReturnMessage(resCd, msg, None)

			logs.debug(procName,
					os.path.basename(__file__), 
					sys._getframe(0).f_code.co_name,
					u'Response : ' + commUtilServ.jsonDumps(result))
			return result

		servUserMana.delUserFieldRatingInfo(data_user_info_manage['id'])	# delete user field/rating info
		if(len(data_user_field_rating_info_manage) > 0):
			# 사용자 등급/분야 정보를 저장 한다.
			resCd, msg, resData = servUserMana.putUserFieldRatingInfo(data_user_field_rating_info_manage)
			if(resCd != 0):
				logs.war(procName,
						os.path.basename(__file__),
						sys._getframe(0).f_code.co_name,
						u'Database Error : ' + msg)
		
				servUserMana.delUserFieldRatingInfo(data_user_info_manage['id'])	# delete user field/rating info
				servUserMana.putUserFieldRatingInfo(oldFieldRatingInfo)
				servUserMana.updateUserInfo(resDataOldUserInfo)				# update old user info


				result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
						u'사용자 등급/분야 정보를 등록 할 수 없습니다. 원인 : ' + msg,
						None)
				logs.war(procName,
						os.path.basename(__file__),
						sys._getframe(0).f_code.co_name,
						u'response : ' + commUtilServ.jsonDumps(result))
				return result


		# 사용자 파일 정보를 수정 한다.
		resCd, msg, resData = servUserMana.updateUserFileInfo(data_user_file_info_manage)
		if(resCd != 0):
			logs.war(procName,
					os.path.basename(__file__),
					sys._getframe(0).f_code.co_name,
					u'Database Error : ' + msg)
		

			servUserMana.delUserFieldRatingInfo(data_user_info_manage['id'])	# delete user field/rating info
			servUserMana.putUserFieldRatingInfo(oldFieldRatingInfo)
			servUserMana.updateUserInfo(resDataOldUserInfo)				# update old user info


			result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
					u'사용자 파일 정보를 등록 할 수 없습니다. 원인 : ' + msg,
					None)
			logs.war(procName,
					os.path.basename(__file__),
					sys._getframe(0).f_code.co_name,
					u'response : ' + commUtilServ.jsonDumps(result))
			return result


		# 등록 수첨(자격증) / 싸인 파일을 저장 한다.
		try:
			if(params['user_license_status'] == 'C'):
				f_user_license = request.files['f_user_license']

				commServ.createDir(data_user_file_info_manage['user_license_path'])
				commServ.saveFile(f_user_license, data_user_file_info_manage['user_license_path'], data_user_file_info_manage['user_license_change_name'])

				if(resDataOldUserInfo['user_license_path'] != ''):
					commServ.removeFile(resDataOldUserInfo['user_license_path'], resDataOldUserInfo['user_license_change_name'])

			elif(params['user_license_status'] == 'D'):
				commServ.removeFile(data_user_file_info_manage['user_license_path'], data_user_file_info_manage['user_license_change_name'])

		except:
		
			logs.war(procName,
					os.path.basename(__file__),
					sys._getframe(0).f_code.co_name,
					u'등록 수접(자격증) 파일 저장 시 에러가 발생하여 회원 수정을 완료 할 수 없습니다.')
		
			data_user_file_info_manage['id'] = params['id']
			data_user_file_info_manage['sign_path'] = resDataOldUserInfo['sign_path'] 
			data_user_file_info_manage['sign_original_name'] = resDataOldUserInfo['sign_original_name'] 
			data_user_file_info_manage['sign_change_name']	= resDataOldUserInfo['sign_change_name'] 
			data_user_file_info_manage['user_license_path'] = resDataOldUserInfo['user_license_path'] 
			data_user_file_info_manage['user_license_original_name'] = resDataOldUserInfo['user_license_original_name'] 
			data_user_file_info_manage['user_license_change_name']	= resDataOldUserInfo['user_license_change_name'] 

			servUserMana.updateUserFileInfo(data_user_file_info_manage)
			servUserMana.delUserFieldRatingInfo(data_user_info_manage['id'])	# delete user field/rating info
			servUserMana.putUserFieldRatingInfo(oldFieldRatingInfo)
			servUserMana.updateUserInfo(resDataOldUserInfo)				# update old user info

			result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
					u'등록 수접(자격증) 파일 저장 시 에러가 발생하여 회원 수정을 완료 할 수 없습니다.',
					None)
			logs.war(procName,
					os.path.basename(__file__),
					sys._getframe(0).f_code.co_name,
					u'response : ' + commUtilServ.jsonDumps(result))
			return result

		# 싸인 파일을 저장 한다.
		try:
			if(params['sign_status'] == 'C'):
				f_sign = request.files['f_sign']

				commServ.createDir(data_user_file_info_manage['sign_path'])
				commServ.saveFile(f_sign, data_user_file_info_manage['sign_path'], data_user_file_info_manage['sign_change_name'])
				
				if(resDataOldUserInfo['sign_path'] != ''):
					commServ.removeFile(resDataOldUserInfo['sign_path'], resDataOldUserInfo['sign_change_name'])
			elif(params['sign_status'] == 'D'):
				commServ.removeFile(data_user_file_info_manage['sign_path'], data_user_file_info_manage['sign_change_name'])
	
		except:
			if(params['user_license_status'] == 'C'):
				commServ.removeFile(data_user_file_info_manage['user_license_path'], data_user_file_info_manage['user_license_change_name'])

			data_user_file_info_manage['id'] = params['id']
			data_user_file_info_manage['sign_path'] = resDataOldUserInfo['sign_path'] 
			data_user_file_info_manage['sign_original_name'] = resDataOldUserInfo['sign_original_name'] 
			data_user_file_info_manage['sign_change_name']	= resDataOldUserInfo['sign_change_name'] 
			data_user_file_info_manage['user_license_path'] = resDataOldUserInfo['user_license_path'] 
			data_user_file_info_manage['user_license_original_name'] = resDataOldUserInfo['user_license_original_name'] 
			data_user_file_info_manage['user_license_change_name']	= resDataOldUserInfo['user_license_change_name'] 

			servUserMana.updateUserFileInfo(data_user_file_info_manage)
			servUserMana.delUserFieldRatingInfo(data_user_info_manage['id'])	# delete user field/rating info
			servUserMana.putUserFieldRatingInfo(oldFieldRatingInfo)
			servUserMana.updateUserInfo(resDataOldUserInfo)				# update old user info

			logs.war(procName,
					os.path.basename(__file__),
					sys._getframe(0).f_code.co_name,
					u'Sign 파일 저장시 에러가 발생하여 회원 수정을 완료 할 수 없습니다.')

			result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
					u'Sign 파일 저장시 에러가 발생하여 회원 수정을 완료 할 수 없습니다.',
					None)
			logs.war(procName,
					os.path.basename(__file__),
					sys._getframe(0).f_code.co_name,
					u'response : ' + commUtilServ.jsonDumps(result))
			return result
		##########################################################################################################


		if(common_approval_manage != None):
			data_co_info_manage = common_approval_manage['contents']
			##########################################################################################################
			# 회사 정보를 저장 한다.
			logs.war(procName, os.path.basename(__file__), sys._getframe(0).f_code.co_name, u'------------------------------------------------------------------ 회사 소속으로 신규 회사 등록 - 0')
			if(common_approval_manage['req_approval_type'] == constants.COMM_APPRO_CD_CO_NEW):
				resCd, msg, resData = servCompanyMana.post_company(data_co_info_manage)
				if(resCd != 0):
					if(data_user_file_info_manage['sign_path'] != ''):
						commServ.removeFile(data_user_file_info_manage['sign_path'], data_user_file_info_manage['sign_change_name'])
			
					if(data_user_file_info_manage['user_license_path'] != ''):
						commServ.removeFile(data_user_file_info_manage['user_license_path'], data_user_file_info_manage['user_license_change_name'])
	
					data_user_file_info_manage['id'] = params['id']
					data_user_file_info_manage['sign_path'] = resDataOldUserInfo['sign_path'] 
					data_user_file_info_manage['sign_original_name'] = resDataOldUserInfo['sign_original_name'] 
					data_user_file_info_manage['sign_change_name']	= resDataOldUserInfo['sign_change_name'] 
					data_user_file_info_manage['user_license_path'] = resDataOldUserInfo['user_license_path'] 
					data_user_file_info_manage['user_license_original_name'] = resDataOldUserInfo['user_license_original_name'] 
					data_user_file_info_manage['user_license_change_name']	= resDataOldUserInfo['user_license_change_name'] 

					servUserMana.updateUserFileInfo(data_user_file_info_manage)
					servUserMana.delUserFieldRatingInfo(data_user_info_manage['id'])	# delete user field/rating info
					servUserMana.putUserFieldRatingInfo(oldFieldRatingInfo)
					servUserMana.updateUserInfo(resDataOldUserInfo)				# update old user info
	
					logs.war(procName,
							os.path.basename(__file__),
							sys._getframe(0).f_code.co_name,
							u'Database Error : ' + msg)
	
					result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
							u'회사 정보를 등록 할 수 없습니다. 원인 : ' + msg,
							None)
					logs.war(procName,
							os.path.basename(__file__),
							sys._getframe(0).f_code.co_name,
							u'response : ' + commUtilServ.jsonDumps(result))
					return result
	
				# 사업자 등록증 파일을 저장 한다.
				if(data_co_info_manage['co_license_path'] != ''):
					resCd, msg, returnData = commCoFileManage(request, 'co', data_co_info_manage)
					if(resCd != 0):
						servCompanyMana.delete_company(data_co_info_manage['co_regisnum'])
		
						if(data_user_file_info_manage['sign_path'] != ''):
							commServ.removeFile(data_user_file_info_manage['sign_path'], data_user_file_info_manage['sign_change_name'])
				
						if(data_user_file_info_manage['user_license_path'] != ''):
							commServ.removeFile(data_user_file_info_manage['user_license_path'], data_user_file_info_manage['user_license_change_name'])
		
						data_user_file_info_manage['id'] = params['id']
						data_user_file_info_manage['sign_path'] = resDataOldUserInfo['sign_path'] 
						data_user_file_info_manage['sign_original_name'] = resDataOldUserInfo['sign_original_name'] 
						data_user_file_info_manage['sign_change_name']	= resDataOldUserInfo['sign_change_name'] 
						data_user_file_info_manage['user_license_path'] = resDataOldUserInfo['user_license_path'] 
						data_user_file_info_manage['user_license_original_name'] = resDataOldUserInfo['user_license_original_name'] 
						data_user_file_info_manage['user_license_change_name']	= resDataOldUserInfo['user_license_change_name'] 
	
						servUserMana.updateUserFileInfo(data_user_file_info_manage)
						servUserMana.delUserFieldRatingInfo(data_user_info_manage['id'])	# delete user field/rating info
						servUserMana.putUserFieldRatingInfo(oldFieldRatingInfo)
						servUserMana.updateUserInfo(resDataOldUserInfo)				# update old user info
		
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'Database Error : ' + msg)
		
						result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
								u'회사 정보를 등록 할 수 없습니다. 원인 : ' + str(e),
								None)
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'response : ' + commUtilServ.jsonDumps(result))
						return result
				
				# 공사업 등록증 파일을 저장 한다.
				if(data_co_info_manage['bs_license_path'] != ''):
					resCd, msg, returnData = commCoFileManage(request, 'bs', data_co_info_manage)
					if(resCd != 0):
				
						if(data_co_info_manage['co_license_path'] != ''):
							commServ.removeFile(data_co_info_manage['co_license_path'], data_co_info_manage['co_license_change_name'])
	
						servCompanyMana.delete_company(data_co_info_manage['co_regisnum'])	# 회사 정보를 삭제 한다.
	
						if(data_user_file_info_manage['sign_path'] != ''):
							commServ.removeFile(data_user_file_info_manage['sign_path'], data_user_file_info_manage['sign_change_name'])
			
						if(data_user_file_info_manage['user_license_path'] != ''):
							commServ.removeFile(data_user_file_info_manage['user_license_path'], data_user_file_info_manage['user_license_change_name'])
	
	
						data_user_file_info_manage['id'] = params['id']
						data_user_file_info_manage['sign_path'] = resDataOldUserInfo['sign_path'] 
						data_user_file_info_manage['sign_original_name'] = resDataOldUserInfo['sign_original_name'] 
						data_user_file_info_manage['sign_change_name']	= resDataOldUserInfo['sign_change_name'] 
						data_user_file_info_manage['user_license_path'] = resDataOldUserInfo['user_license_path'] 
						data_user_file_info_manage['user_license_original_name'] = resDataOldUserInfo['user_license_original_name'] 
						data_user_file_info_manage['user_license_change_name']	= resDataOldUserInfo['user_license_change_name'] 

						servUserMana.updateUserFileInfo(data_user_file_info_manage)
						servUserMana.delUserFieldRatingInfo(data_user_info_manage['id'])	# delete user field/rating info
						servUserMana.putUserFieldRatingInfo(oldFieldRatingInfo)
						servUserMana.updateUserInfo(resDataOldUserInfo)				# update old user info
	

						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'Database Error : ' + msg)
	
						result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
								u'회사 정보를 등록 할 수 없습니다. 원인 : ' + msg,
								None)
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'response : ' + commUtilServ.jsonDumps(result))
						return result
			elif(common_approval_manage['next_approval_info'] != '' and common_approval_manage['next_approval_info']['req_approval_type'] == constants.COMM_APPRO_CD_CO_NEW):
				data_co_info_manage = common_approval_manage['next_approval_info']['contents']

				resCd, msg, resData = servCompanyMana.post_company(data_co_info_manage)
				if(resCd != 0):
					if(data_user_file_info_manage['sign_path'] != ''):
						commServ.removeFile(data_user_file_info_manage['sign_path'], data_user_file_info_manage['sign_change_name'])
			
					if(data_user_file_info_manage['user_license_path'] != ''):
						commServ.removeFile(data_user_file_info_manage['user_license_path'], data_user_file_info_manage['user_license_change_name'])
	
					data_user_file_info_manage['id'] = params['id']
					data_user_file_info_manage['sign_path'] = resDataOldUserInfo['sign_path'] 
					data_user_file_info_manage['sign_original_name'] = resDataOldUserInfo['sign_original_name'] 
					data_user_file_info_manage['sign_change_name']	= resDataOldUserInfo['sign_change_name'] 
					data_user_file_info_manage['user_license_path'] = resDataOldUserInfo['user_license_path'] 
					data_user_file_info_manage['user_license_original_name'] = resDataOldUserInfo['user_license_original_name'] 
					data_user_file_info_manage['user_license_change_name']	= resDataOldUserInfo['user_license_change_name'] 

					servUserMana.updateUserFileInfo(data_user_file_info_manage)
					servUserMana.delUserFieldRatingInfo(data_user_info_manage['id'])	# delete user field/rating info
					servUserMana.putUserFieldRatingInfo(oldFieldRatingInfo)
					servUserMana.updateUserInfo(resDataOldUserInfo)				# update old user info
	
					logs.war(procName,
							os.path.basename(__file__),
							sys._getframe(0).f_code.co_name,
							u'Database Error : ' + msg)
	
					result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
							u'회사 정보를 등록 할 수 없습니다. 원인 : ' + msg,
							None)
					logs.war(procName,
							os.path.basename(__file__),
							sys._getframe(0).f_code.co_name,
							u'response : ' + commUtilServ.jsonDumps(result))
					return result
	
				# 사업자 등록증 파일을 저장 한다.
				if(data_co_info_manage['co_license_path'] != ''):
					resCd, msg, returnData = commCoFileManage(request, 'co', data_co_info_manage)
					if(resCd != 0):
						servCompanyMana.delete_company(data_co_info_manage['co_regisnum'])
		
						if(data_user_file_info_manage['sign_path'] != ''):
							commServ.removeFile(data_user_file_info_manage['sign_path'], data_user_file_info_manage['sign_change_name'])
				
						if(data_user_file_info_manage['user_license_path'] != ''):
							commServ.removeFile(data_user_file_info_manage['user_license_path'], data_user_file_info_manage['user_license_change_name'])
		
						data_user_file_info_manage['id'] = params['id']
						data_user_file_info_manage['sign_path'] = resDataOldUserInfo['sign_path'] 
						data_user_file_info_manage['sign_original_name'] = resDataOldUserInfo['sign_original_name'] 
						data_user_file_info_manage['sign_change_name']	= resDataOldUserInfo['sign_change_name'] 
						data_user_file_info_manage['user_license_path'] = resDataOldUserInfo['user_license_path'] 
						data_user_file_info_manage['user_license_original_name'] = resDataOldUserInfo['user_license_original_name'] 
						data_user_file_info_manage['user_license_change_name']	= resDataOldUserInfo['user_license_change_name'] 
	
						servUserMana.updateUserFileInfo(data_user_file_info_manage)
						servUserMana.delUserFieldRatingInfo(data_user_info_manage['id'])	# delete user field/rating info
						servUserMana.putUserFieldRatingInfo(oldFieldRatingInfo)
						servUserMana.updateUserInfo(resDataOldUserInfo)				# update old user info
		
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'Database Error : ' + msg)
		
						result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
								u'회사 정보를 등록 할 수 없습니다. 원인 : ' + str(e),
								None)
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'response : ' + commUtilServ.jsonDumps(result))
						return result
				
				# 공사업 등록증 파일을 저장 한다.
				if(data_co_info_manage['bs_license_path'] != ''):
					resCd, msg, returnData = commCoFileManage(request, 'bs', data_co_info_manage)
					if(resCd != 0):
				
						if(data_co_info_manage['co_license_path'] != ''):
							commServ.removeFile(data_co_info_manage['co_license_path'], data_co_info_manage['co_license_change_name'])
	
						servCompanyMana.delete_company(data_co_info_manage['co_regisnum'])	# 회사 정보를 삭제 한다.
	
						if(data_user_file_info_manage['sign_path'] != ''):
							commServ.removeFile(data_user_file_info_manage['sign_path'], data_user_file_info_manage['sign_change_name'])
			
						if(data_user_file_info_manage['user_license_path'] != ''):
							commServ.removeFile(data_user_file_info_manage['user_license_path'], data_user_file_info_manage['user_license_change_name'])
	
	
						data_user_file_info_manage['id'] = params['id']
						data_user_file_info_manage['sign_path'] = resDataOldUserInfo['sign_path'] 
						data_user_file_info_manage['sign_original_name'] = resDataOldUserInfo['sign_original_name'] 
						data_user_file_info_manage['sign_change_name']	= resDataOldUserInfo['sign_change_name'] 
						data_user_file_info_manage['user_license_path'] = resDataOldUserInfo['user_license_path'] 
						data_user_file_info_manage['user_license_original_name'] = resDataOldUserInfo['user_license_original_name'] 
						data_user_file_info_manage['user_license_change_name']	= resDataOldUserInfo['user_license_change_name'] 

						servUserMana.updateUserFileInfo(data_user_file_info_manage)
						servUserMana.delUserFieldRatingInfo(data_user_info_manage['id'])	# delete user field/rating info
						servUserMana.putUserFieldRatingInfo(oldFieldRatingInfo)
						servUserMana.updateUserInfo(resDataOldUserInfo)				# update old user info
	

						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'Database Error : ' + msg)
	
						result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
								u'회사 정보를 등록 할 수 없습니다. 원인 : ' + msg,
								None)
						logs.war(procName,
								os.path.basename(__file__),
								sys._getframe(0).f_code.co_name,
								u'response : ' + commUtilServ.jsonDumps(result))
						return result

			##########################################################################################################



			# 공통 승인 결재 정보를 저장 한다.
#			if(data_co_info_manage['co_regisnum'] != ''):
			if(common_approval_manage != None):
				resCd, msg, resData = servComApproMana.putCommonApprovalInfo(common_approval_manage)
				if(resCd != 0):
					data_co_info_manage = common_approval_manage['contents']
					logs.war(procName,
							os.path.basename(__file__),
							sys._getframe(0).f_code.co_name,
							u'Database Error : ' + msg)
	
					result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
							u'회사 신규 추가 결재 정보를 등록 할 수 없습니다. 원인 : ' + msg,
							None)
					logs.war(procName,
							os.path.basename(__file__),
							sys._getframe(0).f_code.co_name,
							u'response : ' + commUtilServ.jsonDumps(result))

					if(data_co_info_manage['bs_license_path'] != ''):
						commServ.removeFile(data_co_info_manage['bs_license_path'], data_co_info_manage['bs_license_change_name'])
					if(data_co_info_manage['co_license_path'] != ''):
						commServ.removeFile(data_co_info_manage['co_license_path'], data_co_info_manage['co_license_change_name'])
	
					servCompanyMana.delete_company(data_co_info_manage['co_regisnum'])	# 회사 정보를 삭제 한다.
	
					if(data_user_file_info_manage['sign_path'] != ''):
						commServ.removeFile(data_user_file_info_manage['sign_path'], data_user_file_info_manage['sign_change_name'])
			
					if(data_user_file_info_manage['user_license_path'] != ''):
						commServ.removeFile(data_user_file_info_manage['user_license_path'], data_user_file_info_manage['user_license_change_name'])
	
					data_user_file_info_manage['id'] = params['id']
					data_user_file_info_manage['sign_path'] = resDataOldUserInfo['sign_path'] 
					data_user_file_info_manage['sign_original_name'] = resDataOldUserInfo['sign_original_name'] 
					data_user_file_info_manage['sign_change_name']	= resDataOldUserInfo['sign_change_name'] 
					data_user_file_info_manage['user_license_path'] = resDataOldUserInfo['user_license_path'] 
					data_user_file_info_manage['user_license_original_name'] = resDataOldUserInfo['user_license_original_name'] 
					data_user_file_info_manage['user_license_change_name']	= resDataOldUserInfo['user_license_change_name'] 

					servUserMana.updateUserFileInfo(data_user_file_info_manage)
					servUserMana.delUserFieldRatingInfo(data_user_info_manage['id'])	# delete user field/rating info
					servUserMana.putUserFieldRatingInfo(oldFieldRatingInfo)
					servUserMana.updateUserInfo(resDataOldUserInfo)				# update old user info
	
					return result
				"""

        logData = dLogManage.makeLogData(
            procCode,
            constants.LOG_LEVEL_CODE_INFO,
            resDataUserInfo["id"]
            + "("
            + resDataUserInfo["authority_name"]
            + ") 사용자가 "
            + resDataOldUserInfo["id"]
            + "("
            + resDataOldUserInfo["authority_name"]
            + ") 사용자의 정보를 수정하였습니다.",
            util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
            resDataUserInfo["id"],
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 사용자 수정 로그를 DB에 저장 한다. ----------",
        )
        query = sLogManage.iLogData(logData)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iLogData Query : " + query,
        )

        resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그 저장 Query 실행

        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + msg,
            )

        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )

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

    return result


# 7. 회원 가입 승인
#
@userManageApi.route("/approvalUser/<userId>", methods=["GET"])
def approvalUser(userId):

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 회원 가입 승인 시작 ----------",
    )
    commServ = commonService()
    servUserMana = servUserManage()

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

    commUtilServ = commUtilService()
    dCommManage = dataCommonManage()
    sUserManage = sqlUserManage()
    dUserManage = dataUserManage()
    msgServ = messageService()
    dLogManage = dataLogManage()
    sLogManage = sqlLogManage()

    token = request.headers.get("token")
    sysCd = request.headers.get("sysCd")
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
    resCd, msg, resData = servUserMana.getUserInfo(2, token, sysCd)
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

    if resData == None:
        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_455, "", None)

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "response : " + commUtilServ.jsonDumps(result),
        )
        return result

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 스인 하고자 하는 사용자 정보를 가져온다. ----------",
    )
    # 사용자 정보를 가져 온다.
    resCd, msg, resDataUserInfo = servUserMana.getUserInfo(1, userId, sysCd)
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

    if resDataUserInfo == None:
        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_455, "", None)

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "response : " + commUtilServ.jsonDumps(result),
        )
        return result

    logData = dLogManage.makeLogData(
        procCode,
        constants.LOG_LEVEL_CODE_INFO,
        resData["id"]
        + "("
        + resData["authority_name"]
        + ") 사용자가 "
        + resDataUserInfo["id"]
        + "회원 가입을 승인 하였습니다.",
        util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
        resData["id"],
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 4. 사용자 승인 권한이 있는지 확인한다. ----------",
    )
    if resData["authority_code"] == constants.USER_AUTH_SYSMANAGE:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 4-1. 시스템 관리자일 경우 승인 할 수 있다.  ----------",
        )

    elif (resData["authority_code"] == constants.USER_AUTH_CONTRACTOR) or (
        resData["authority_code"] == constants.USER_AUTH_SUPERVISOR
    ):
        # 권한이 감리자 또는 시공자 이면서 회사명이 같으면 사용자 정보를 수정 할 수 있다.
        if resData["co_code"] == resDataUserInfo["co_code"]:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 4-2. 권한이 감리자 또는 시공자이면서 회사코드가 동일할 경우 사용자를 가입 승인 할 수 있다. ----------",
            )
        else:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "사용자 가입 승인 권한이 없습니다.",
            )

            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 가입 승인 권한이 없습니다.", None
            )

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

    elif (resData["authority_code"] == constants.USER_AUTH_CONTRACTOR_MONITOR) or (
        resData["authority_code"] == constants.USER_AUTH_SUPERVISOR_MONITOR
    ):
        # 권한이 감리자 모니터링 또는 시공자 모니터링 이면서 회사명이 같고 권한이 시공자 또는 감리원이면 사용자 가입 승인을 할 수 있다.
        if resData["co_code"] == resDataUserInfo["co_code"]:
            # if(resDataUserInfo['authority_code'] == constants.USER_AUTH_CONTRACTOR_MONITOR) or (resDataUserInfo['authority_code'] == constants.USER_AUTH_SUPERVISING):
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 4-3. 권한이 감리자 모니터링 또는 시공자 모니터링이면서 회사명이 같고 권한기 시공자 또는 람리원이면 사용자 가입 승인을 할 수 있다. ----------",
            )
        else:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "사용자 가입 승인 권한이 없습니다.",
            )

            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 가입 승인 권한이 없습니다.", None
            )

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result
    else:
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "사용자 가입 승인 권한이 없습니다.",
        )

        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 가입 승인 권한이 없습니다.", None
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    query = sUserManage.uApprovalUser(
        userId, util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14)
    )  # 회원 가입 승인 날짜)
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "uApprovalUser Query : " + query,
    )

    resCd, msg, resData = dbms.execute(query)
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

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 사용자 가입 승인 로그를 DB에 저장 한다. ----------",
    )
    query = sLogManage.iLogData(logData)
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "iLogData Query : " + query,
    )

    resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그 저장 Query 실행

    if resCd != 0:
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Database Error : " + msg,
        )

    result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "Response : " + commUtilServ.jsonDumps(result),
    )

    return result


# 8. 회원 삭제
#
@userManageApi.route("/deleteUser/<userId>", methods=["DELETE"])
def deleteUser(userId):

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 회원 삭제 시작 ----------",
    )
    commServ = commonService()
    servUserMana = servUserManage()

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

    commUtilServ = commUtilService()
    dCommManage = dataCommonManage()
    sUserManage = sqlUserManage()
    msgServ = messageService()
    dLogManage = dataLogManage()
    sLogManage = sqlLogManage()

    token = request.headers.get("token")
    sysCd = request.headers.get("sysCd")
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
    resCd, msg, resData = servUserMana.getUserInfo(2, token, sysCd)
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

    if resData == None:
        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_455, "", None)

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    logData = dLogManage.makeLogData(
        procCode,
        constants.LOG_LEVEL_CODE_INFO,
        resData["id"]
        + "("
        + resData["authority_name"]
        + ") 사용자가 "
        + userId
        + " 사용자를 삭제 하였습니다.",
        util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
        resData["id"],
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 3. 사용자 삭제 권한이 있는지 확인한다. ----------",
    )
    if (
        resData["authority_code"] == constants.USER_AUTH_SYSMANAGE
        or resData["id"] == userId
    ):
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 3-1. 시스템 관리자일 경우 사용자를 삭제 할 수 있다.  ----------",
        )
        query = sUserManage.uDeleteUser(userId)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uDeleteUser Query : " + query,
        )
        resCd, msg, resData = dbms.execute(query)
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

    else:
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "사용자 삭제 권한이 없습니다.",
        )

        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 삭제 권한이 없습니다.", None
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 사용자 회원 삭제 로그를 DB에 저장 한다. ----------",
    )
    query = sLogManage.iLogData(logData)
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "iLogData Query : " + query,
    )

    resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그 저장 Query 실행

    if resCd != 0:
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Database Error : " + msg,
        )

    result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "Response : " + commUtilServ.jsonDumps(result),
    )

    return result


# 9. 사용자 상세 정보 제공 API
#
@userManageApi.route("/getUserInfo/<userId>", methods=["GET"])
def getUserInfo(userId):
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 사용자 정보 제공 시작 ----------",
    )
    commServ = commonService()
    servUserMana = servUserManage()

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

    commUtilServ = commUtilService()
    dCommManage = dataCommonManage()
    sUserManage = sqlUserManage()
    dUserManage = dataUserManage()
    msgServ = messageService()

    token = request.headers.get("token")
    sysCd = request.headers.get("sysCd")
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
    resCd, msg, resData = servUserMana.getUserInfo(2, token, sysCd)
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

    if resData == None:
        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_455, "", None)
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    # ID에 대한 사용자 정보를 가져 온다.
    resCd, msg, resDataUserInfo = servUserMana.getUserInfo(1, userId, sysCd)
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

    if resDataUserInfo == None:
        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_455, "", None)

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "response : " + commUtilServ.jsonDumps(result),
        )
        return result

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 4. 제공할 사용자 모델을 생성하고 기본정보를 생성한다. ----------",
    )
    resultData = dUserManage.makeUserInfoResult(resDataUserInfo)

    """
	# 등급/분야 정보를 Read 한다.
	logs.debug(procName,
			os.path.basename(__file__), 
			sys._getframe(0).f_code.co_name,
			u'---------- 7. 등급/분야 정보를 가져 온다.. ----------')
	resCd, msg, resData = servUserMana.getUserFieldRatingInfo(1, userId) # 사용자 정보를 불러 온다.
	if(resCd != 0):										# DB 에러 발생 시
		logs.war(procName,
				os.path.basename(__file__), 
				sys._getframe(0).f_code.co_name,
				u'Database Error : ' + commUtilServ.jsonDumps(msg))

		result = commServ.makeReturnMessage(resCd, msg, None)

		logs.debug(procName,
				os.path.basename(__file__), 
				sys._getframe(0).f_code.co_name,
				u'Response : ' + commUtilServ.jsonDumps(result))
		return result
	
	if(resData != None):
		resultData['field_rating'] = resData
	"""

    result = commServ.makeReturnMessage(
        constants.REST_RESPONSE_CODE_ZERO, "", resultData
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "Response : " + commUtilServ.jsonDumps(result),
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 사용자 정보 제공 완료 ----------",
    )

    return result


# 10. 사용자 리스트 조회 API
#
@userManageApi.route("/searchUserInfo", methods=["POST"])
def searchUserInfo():
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 사용자 리스트 검색 시작 ----------",
    )
    commServ = commonService()
    servUserMana = servUserManage()

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    dCommManage = dataCommonManage()
    sUserManage = sqlUserManage()
    msgServ = messageService()
    commUtilServ = commUtilService()

    sysCd = request.headers.get("sysCd")
    token = request.headers.get("token")
    params = request.get_json()  # login parameter recv

    params["co_name"] = urllib.parse.unquote(params["co_name"])
    params["user_name"] = urllib.parse.unquote(params["user_name"])
    params["user_email"] = urllib.parse.unquote(params["user_email"])

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "request header token : " + token + ", sysCd : " + sysCd
        # 			+ u' / request params data : ' + params)
        + " / request params data : " + commUtilServ.jsonDumps(params),
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
    resCd, msg, resData = servUserMana.getUserInfo(2, token, sysCd)
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

    if resData == None:
        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_455, "", None)
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 3. 사용자 검색 권한이 있는지 확인한다. ----------",
    )

    #################################### 사용자 정보를 검색 한다. ####################################
    resCd, msg, resUserList = servUserMana.searchUserList(
        resData, params
    )  # 사용자 정보를 불러 온다.
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

    #################################### 회원 수를 가져 온다. ####################################
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 회원 수를 가져 온다. ----------",
    )
    resCd, msg, resUserCnt = servUserMana.searchUserCnt(resData, params)
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

    #################################### Response 데이터를 생성 한다. ####################################
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- Response 데이터를 생성 한다. ----------",
    )

    resultData = {"list": resUserList, "cnt": str(resUserCnt["cnt"])}

    result = commServ.makeReturnMessage(
        constants.REST_RESPONSE_CODE_ZERO, "", resultData
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "Response : " + commUtilServ.jsonDumps(resultData),
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 사용자 리스트 검색 완료 ----------",
    )

    return result


# 11. 사용자 ID 찾기 API
#
@userManageApi.route("/findUserId", methods=["POST"])
def findUserId():
    commServ = commonService()

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 사용자 ID 찾기 시작 ----------",
    )

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    dCommManage = dataCommonManage()
    sUserManage = sqlUserManage()
    msgServ = messageService()
    commUtilServ = commUtilService()

    sysCd = request.headers.get("sysCd")
    params = request.get_json()  # login parameter recv

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "request header sysCd : "
        + sysCd
        + " / request params data : "
        + commUtilServ.jsonDumps(params),
    )

    # System Code Check
    result, resultData = commServ.checkSystemCd(sysCd)
    if result == False:
        return resultData

    # 사용자 이름 Check
    if commUtilServ.dataCheck(params["user_name"]) == False:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 이름을 입력하여 주시기 바랍니다.", None
        )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "response : " + commUtilServ.jsonDumps(result),
        )

        return result

    # 사용자 이메일 Check
    if commUtilServ.dataCheck(params["user_email"]) == False:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 이메일을 입력하여 주시기 바랍니다.", None
        )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "response : " + commUtilServ.jsonDumps(result),
        )

        return result

    query = sUserManage.sFindUserId(params)  # 사용자 ID 찾기

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "sFindUserId Query : " + query,
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 1. 사용자 ID를 찾는다. ----------",
    )
    resCd, msg, resData = dbms.queryForObject(query)  # 사용자 정보를 불러 온다.
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

    if resData == None:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "일치하는 ID가 없습니다.", None
        )
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Rresponse : " + commUtilServ.jsonDumps(result),
        )
        return result

    result = commServ.makeReturnMessage(
        constants.REST_RESPONSE_CODE_ZERO, "", resData["id"]
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "Response : " + commUtilServ.jsonDumps(resData),
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 사용자 ID 찾기 완료 ----------",
    )

    return result


# 12. 비밀번호 초기화 API
#
@userManageApi.route("/initUserPasswd", methods=["POST"])
def initUserPasswd():
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 사용자 비밀번호 초기화 시작 ----------",
    )

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    mailServ = copy.copy(mail)  # DB 속성이 중복 되지 않도록 객체 복사
    dCommManage = dataCommonManage()
    sUserManage = sqlUserManage()
    msgServ = messageService()
    commUtilServ = commUtilService()
    commServ = commonService()
    dLogManage = dataLogManage()
    sLogManage = sqlLogManage()

    sysCd = request.headers.get("sysCd")
    params = request.get_json()  # login parameter recv

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "request header sysCd : "
        + sysCd
        + " / request params data : "
        + commUtilServ.jsonDumps(params),
    )

    # System Code Check
    result, resultData = commServ.checkSystemCd(sysCd)
    if result == False:
        return resultData

    # 사용자 ID Check
    if commUtilServ.dataCheck(params["id"]) == False:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 ID를 입력하여 주시기 바랍니다.", None
        )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "response : " + commUtilServ.jsonDumps(result),
        )

        return result

    # 사용자 이름 Check
    if commUtilServ.dataCheck(params["user_name"]) == False:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 이름을 입력하여 주시기 바랍니다.", None
        )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "response : " + commUtilServ.jsonDumps(result),
        )

        return result

    # 사용자 이메일 Check
    if commUtilServ.dataCheck(params["user_email"]) == False:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 이메일을 입력하여 주시기 바랍니다.", None
        )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "response : " + commUtilServ.jsonDumps(result),
        )

        return result

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 1. 사용자 정보를 찾는다. ----------",
    )
    query = sUserManage.sFindUserInfo(params)  # 사용자 정보 찾기
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "sFindUserInfo Query : " + query,
    )
    resCd, msg, resData = dbms.queryForObject(query)  # 사용자 정보를 불러 온다.
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

    if resData == None:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "일치하는 사용자 정보가 없습니다.", None
        )
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Rresponse : " + commUtilServ.jsonDumps(result),
        )
        return result

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 2. 새로운 비밀번호를 생성한다. ----------",
    )

    newPassword = passwordGenerator().generate(8)
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "new Password : " + newPassword,
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 3. 비밀번호를 암호화 한다. ----------",
    )
    encryptPassword = str(encryption().encrypt(newPassword))
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "encrypt Password : " + encryptPassword,
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 4. 비밀번호를 저장한다. ----------",
    )
    query = sUserManage.uInitPassword(
        params, encryptPassword
    )  # 사용자 token 발행 및 DB 저장을 위한 Query 생성
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "uInitPassword Query : " + query,
    )

    resCd, msg, resData = dbms.execute(query)  # 사용자 token update Query 실행
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

    logData = dLogManage.makeLogData(
        procCode,
        constants.LOG_LEVEL_CODE_INFO,
        params["id"] + " 사용자가 Password를 초기화 하였습니다.",
        util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
        params["id"],
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 5. 비밀번호 초기화 로그를 DB에 저장 한다. ----------",
    )
    query = sLogManage.iLogData(logData)
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "iLogData Query : " + query,
    )

    resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그 저장 Query 실행

    if resCd != 0:
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Database Error : " + msg,
        )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 6. 비밀번호를 이메일로 전송 한다. ----------",
    )
    mailServ.sendMail(
        params["user_email"],
        "비밀번호 초기화",
        params["id"]
        + "의 비밀번호를 "
        + newPassword
        + "로 변경 하였습니다. 로그인 후 비밀번호를 변경 하시기 바랍니다.",
    )

    logData = dLogManage.makeLogData(
        procCode,
        constants.LOG_LEVEL_CODE_INFO,
        params["id"] + " 사용자가 비밀번호를 이메일로 전송 하였습니다.",
        util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
        params["id"],
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 7. 비밀번호 초기화 로그를 DB에 저장 한다. ----------",
    )
    query = sLogManage.iLogData(logData)
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "iLogData Query : " + query,
    )

    resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그 저장 Query 실행

    if resCd != 0:
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Database Error : " + msg,
        )

    result = commServ.makeReturnMessage(
        constants.REST_RESPONSE_CODE_ZERO,
        "",
        params["id"]
        + "의 새로운 비밀번호를 "
        + params["user_email"]
        + "로 전송 하였습니다. 로그인 후 반드시 비밀번호를 변경 하시기 바랍니다.",
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "Response : " + commUtilServ.jsonDumps(result),
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 사용자 패스워드 초기화 완료 ----------",
    )

    return result


# 회사별 인력 정보 조회
@userManageApi.route("/getCompUserInfo/<userId>", methods=["GET"])
def getCompUserInfo(userId):
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 회사별 인력 정보 조회 ----------",
    )
    commServ = commonService()
    servUserMana = servUserManage()

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

    commUtilServ = commUtilService()
    dCommManage = dataCommonManage()
    sUserManage = sqlUserManage()
    dUserManage = dataUserManage()
    msgServ = messageService()

    token = request.headers.get("token")
    sysCd = request.headers.get("sysCd")
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
        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_455, "", None)
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 5. 회사별 사용자 조회 권한이 있는지 확인한다. ----------",
    )
    if (
        (loginUserInfo["authority_code"] != constants.USER_AUTH_CONTRACTOR)
        and (loginUserInfo["authority_code"] == constants.USER_AUTH_SUPERVISOR)
        and (loginUserInfo["authority_code"] == constants.USER_AUTH_CONTRACTOR_MONITOR)
        and (loginUserInfo["authority_code"] == constants.USER_AUTH_SUPERVISOR_MONITOR)
    ):
        # 권한이 감리자 모니터링 또는 시공자 모니터링 이면서 회사명이 같고 권한이 시공자 또는 감리원이면 사용자 정보를 조회 할 수 있다.
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "회사의 인력 정보를 조회 권한이 없습니다.",
        )

        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "회사의 인력 정보룰 조회 권한이 없습니다.", None
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 회사의 인력 정보를 조회 한다. ----------",
    )
    # 회사 인력 정보를 가져 온다.
    if userId == "ALL" and loginUserInfo["co_code"] == "":
        userId = loginUserInfo["id"]

    resCd, msg, resDataUserInfo = servUserMana.getCompUserInfo(
        loginUserInfo["co_code"], userId
    )
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

    if resDataUserInfo == None:
        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_458, "", None)
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    result = commServ.makeReturnMessage(
        constants.REST_RESPONSE_CODE_ZERO, "", resDataUserInfo
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "Response : " + commUtilServ.jsonDumps(result),
    )

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 사용자 정보 제공 완료 ----------",
    )

    return result


# 신규 회사 등록 데이터 생성
def makeNewCompanyDataInfo(params):

    commServ = commonService()
    dataCompanyMana = dataCompanyManage()
    servCommMana = servCommManage()
    servCompanyMana = servCompanyManage()

    resCd, msg, coNum = servCommMana.createCoNum()

    if resCd != 0:
        return resCd, msg, None
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

    resCd, msg, nextCoNum = servCommMana.increaseCoNum()
    if resCd != 0:
        return resCd, msg, None
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

    data_co_info_manage = dataCompanyMana.makeReqCompanyInfoModel()
    data_co_info_manage["co_code"] = coCode + str(f"{coNum:06d}")
    data_co_info_manage["co_name"] = params["co_name"]
    data_co_info_manage["co_type"] = params["co_type"]
    data_co_info_manage["co_ceo"] = params["co_ceo"]
    data_co_info_manage["co_contact"] = params["co_contact"]
    data_co_info_manage["co_address"] = params["co_address"]
    data_co_info_manage["co_regisnum"] = params["co_regisnum"]
    data_co_info_manage["regisnum"] = params["regisnum"]
    if params["co_regisnum"] != "" and params["co_license_name_new"] != "":
        lpath, origName, changeName = servCompanyMana.companyFileNameManage(
            data_co_info_manage["co_code"], params, "co_license_name_new"
        )

        data_co_info_manage["co_license_path"] = lpath
        data_co_info_manage["co_license_original_name"] = origName
        data_co_info_manage["co_license_change_name"] = changeName
    else:
        return (
            constants.REST_RESPONSE_CODE_DATAFAIL,
            "사업자 등록 번호 또는 사업자 등록증이 누락 되었습니다.",
            None,
        )

    if params["regisnum"] != "" and params["bs_license_name_new"] != "":
        lpath, origName, changeName = servCompanyMana.companyFileNameManage(
            data_co_info_manage["co_code"], params, "bs_license_name_new"
        )

        data_co_info_manage["bs_license_path"] = lpath
        data_co_info_manage["bs_license_original_name"] = origName
        data_co_info_manage["bs_license_change_name"] = changeName

    common_approval_manage = {
        "req_approval_id": params["id"],
        "req_approval_type": constants.COMM_APPRO_CD_CO_NEW,
        "approval_status": constants.APPRO_STATUS_CD_WAIT,
        "contents": data_co_info_manage,
        "approval_id": "master",
        "req_approval_date": util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
        "complete_approval_date": "",
        "next_approval_info": "",
    }

    return constants.REST_RESPONSE_CODE_ZERO, "", common_approval_manage

# 유저 결재 정보 리스트 조회
@userManageApi.route("/ApprovalList/<cons_code>", methods=["GET"])
def getApprovalList(cons_code):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 유저 결재 정보 리스트  get api 시작 ----------",
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
                params = {"cons_code":cons_code}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 결재 리스트 조회를 시도하였습니다.",
                                    json.dumps(params, ensure_ascii=False), "", resCd, msg)
                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None:
                params = {"cons_code":cons_code}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 결재 리스트 조회를 시도하였습니다.",
                                    json.dumps(params, ensure_ascii=False), loginUserInfo.get("id", "") if loginUserInfo else "", resCd, msg)
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
                "start_num": int(request.args.get("start_num")),
                "end_num": int(request.args.get("end_num")),
                "cons_code":cons_code,
            }

            #################################### 해당 결재 리스트 목록을 조회한다 ##########################

            resCd, msg, ALData = servUserMana.get_user_approvals(loginUserInfo.get("id", ""), cons_code)
            result = {
                "count": len(ALData) if ALData else 0,
                "data": ALData[params["start_num"] : params["end_num"]],
            }
            logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + str(result),
                )
            params.update({"id": loginUserInfo.get("id", "")})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 결재 리스트 조회를 하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, result)

        except Exception as e:
            params = {"id": loginUserInfo.get("id", "")}
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                    f"{loginUserInfo['id']} 사용자가 결재 리스트 조회를 하던 중 에러가 발생하였습니다.",
                                    json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )
        return result    