# _*_coding: utf-8 -*-

# 공통 관리 REST API
# 작성 날짜 : 2022. 08. 11
# 작성자 : 황희정
# 기능
# 	1. 2022. 08. 11 | 코드 리스트 제공 API
# 변경 이력
# 	1. 2022. 08. 11 | 황희정 | 최조 작성


from urllib import response
from flask import Blueprint, make_response, request, send_file
import json
import copy
import os
import sys

import urllib

commManageApi = Blueprint("commManageApi", __name__)

# user import
from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import procCode
from allscapeAPIMain import weatherApi
from common.logManage import logManage
from common import util_time
from common import constants
from common.dataCommonManage import dataCommonManage
from common.commUtilService import commUtilService
from common.commonService import commonService
from common.messageService import messageService
from logManage.dataLogManage import dataLogManage
from logManage.sqlLogManage import sqlLogManage
from commManage.servCommManage import servCommManage
from commManage.sqlCommManage import sqlCommManage
from commManage.dataCommManage import dataCommManage
from userManage.servUserManage import servUserManage

from projectUseMaterialManage.servProjectUseMaterialManage import (
    servProjectUseMaterialManage,
)
from projectManage.sqlProjectManage import sqlProjectManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


# 서버확인 API
@commManageApi.route("/getToken", methods=["GET"])
def getToken():
    response = make_response("OK")
    response.close()
    return response


# 코드 리스트 제공 API
#
# Parameter
# 	- reqType | String | 코드 요청 타입
@commManageApi.route("/getCodeList/<reqType>", methods=["GET"])
def getCodeList(reqType):
    logs.war(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 코드 리스트 제공 시작  ----------",
    )

    commServ = commonService()
    commUtilServ = commUtilService()
    servCommMana = servCommManage()

    sysCd = request.headers.get("sysCd")

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "request header sysCd : " + sysCd + " / request url reqType : " + reqType,
    )

    # System Code Check
    result, resultData = commServ.checkSystemCd(sysCd)
    if result == False:
        return resultData

    if commUtilServ.dataCheck(reqType) == False:  # 1-1. Code type 데이터 확인
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL,
            "코드 요청 타입이 없습니다.코드 요청 타입을 입력하여 주시기 바랍니다.",
            None,
        )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    logs.war(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 1. 코드 리스트를 가져 온다. ----------",
    )

    resCd, msg, resData = servCommMana.getCodeList(reqType)

    if resCd != 0:
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

    # Response data 생성
    result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, msg, resData)

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "Response: " + commUtilServ.jsonDumps(result),
    )

    return result


# 2. 기상 정보 제공 API
@commManageApi.route("/getWeatherInfo", methods=["GET"])
def getWeatherInfo():
    commServ = commonService()
    servUserMana = servUserManage()

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    weathApi = copy.copy(weatherApi)
    dCommManage = dataCommManage()
    sCommManage = sqlCommManage()
    commUtilServ = commUtilService()

    sysCd = request.headers.get("sysCd")
    token = request.headers.get("token")
    address = request.args.get("address")

    # System Code Check
    result, resultData = commServ.checkSystemCd(sysCd)
    if result == False:
        return resultData

    # Token Code Check
    result, resultData = commServ.checkTokenCd(token)
    if result == False:
        return resultData

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
        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_454, "", None)
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    arrAddress = (
        address.split(" ") if address else loginUserInfo["co_address"].split(" ")
    )
    arrAddressSize = arrAddress.__len__()

    if arrAddressSize < 1:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL,
            "주소 정보가 없어 날씨 데이터를 불러 올 수 없습니다.",
            None,
        )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    index = 0
    if arrAddressSize >= 3:
        index = 3
    elif arrAddressSize == 2:
        index = 2
    elif arrAddressSize == 1:
        index = 1

    while index > 0:
        query = sCommManage.sGetLocationInfo(index, arrAddress)

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

        if resData != None:
            index = 0
        elif (resData == None) and (index == 1):
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "주소 정보가 정확하지 않아 날씨 데이터를 불러 올 수 없습니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        index -= 1

    datas = weathApi.reqWeatherInfo(
        util_time.get_weather_date(),
        util_time.get_weather_ontime(),
        resData["grid_x"],
        resData["grid_y"],
    )

    curType = ""
    ptyResult = ""
    t1hResult = ""
    skyResult = ""
    for data in datas:
        if curType != data["category"]:
            curType = data["category"]

            if data["category"] == "PTY":
                ptyResult = data["fcstValue"]
            elif data["category"] == "T1H":
                t1hResult = data["fcstValue"]
            elif data["category"] == "SKY":
                skyResult = data["fcstValue"]

    resData = dCommManage.makeWeatherInfo(ptyResult, t1hResult, skyResult)

    # Response data 생성
    result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", resData)

    # logs.war(procName,
    # 		os.path.basename(__file__),
    # 		sys._getframe(0).f_code.co_name,
    # 		u'Response : ' + commUtilServ.jsonDumps(result))

    return result


# 3. 현재 시간  제공 API
@commManageApi.route("/getCurTimeInfo", methods=["GET"])
def getCurTimeInfo():
    commServ = commonService()

    sysCd = request.headers.get("sysCd")
    token = request.headers.get("token")

    # System Code Check
    result, resultData = commServ.checkSystemCd(sysCd)
    if result == False:
        return resultData

    # Token Code Check
    result, resultData = commServ.checkTokenCd(token)
    if result == False:
        return resultData

    # 로그인 된 사용자 인지 확인한다.
    result, resultData = commServ.userLoginChk(token, sysCd)
    if result == False:
        return resultData

    # Response data 생성
    result = commServ.makeReturnMessage(
        constants.REST_RESPONSE_CODE_ZERO,
        "",
        util_time.get_current_time(util_time.TIME_CURRENT_TYPE_DEFAULT),
    )

    # logs.war(procName,
    # 		os.path.basename(__file__),
    # 		sys._getframe(0).f_code.co_name,
    # 		u'Response : ' + commUtilServ.jsonDumps(result))

    return result


# 4. 파일 전송다운로드 API
@commManageApi.route("/download/<userId>/<fileType>/<fileSeparation>", methods=["GET"])
def download(userId, fileType, fileSeparation):
    commServ = commonService()
    servUserMana = servUserManage()

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    commUtilServ = commUtilService()

    sysCd = request.headers.get("sysCd")
    token = request.headers.get("token")

    # System Code Check
    result, resultData = commServ.checkSystemCd(sysCd)
    if result == False:
        return resultData

    # Token Code Check
    result, resultData = commServ.checkTokenCd(token)
    if result == False:
        return resultData

    # userId Check
    if commUtilServ.dataCheck(userId) == False:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "사용자 ID를 입력하여 주시기 바랍니다.", None
        )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )

        return result

    # fileType Check
    if commUtilServ.dataCheck(fileType) == False:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "파일 유형을 입력하여 주시기 바랍니다.", None
        )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )

        return result

    # fileSeparation Check
    if commUtilServ.dataCheck(fileSeparation) == False:
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "파일 구분을 입력하여 주시기 바랍니다.", None
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
        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_454, "", None)
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    resCd, msg, loginUserInfo = servUserMana.getUserInfo(1, userId, sysCd)

    # 파일 유형을 구분 한다.
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "---------- 3. 파일 유형을 구분 한다.사용자가 일치하는지 확인 한다. ----------",
    )

    originalFile = ""
    changeFile = ""
    filePath = ""

    if fileType == "user":  # 사용자 파일일 경우
        # 사용자가 일치하는지 확인 한다.
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 4. 사용자가 일치하는지 확인 한다. ----------",
        )

        # if(loginUserInfo['id'] != userId):
        # 	result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
        # 			u'파일 다운로드 권한이 없습니다.',
        # 			None)
        # 	logs.war(procName,
        # 			os.path.basename(__file__),
        # 			sys._getframe(0).f_code.co_name,
        # 			u'Response : ' + commUtilServ.jsonDumps(result))
        # 	return result

        if fileSeparation == "sign":
            originalFile = loginUserInfo["sign_original_name"]
            changeFile = loginUserInfo["sign_change_name"]
            filePath = loginUserInfo["sign_path"]
        elif fileSeparation == "userlicense":
            originalFile = loginUserInfo["user_license_original_name"]
            changeFile = loginUserInfo["user_license_change_name"]
            filePath = loginUserInfo["user_license_path"]
        elif fileSeparation == "bslicense":
            originalFile = loginUserInfo["bs_license_original_name"]
            changeFile = loginUserInfo["bs_license_change_name"]
            filePath = loginUserInfo["bs_license_path"]
        elif fileSeparation == "colicense":
            originalFile = loginUserInfo["co_license_original_name"]
            changeFile = loginUserInfo["co_license_change_name"]
            filePath = loginUserInfo["co_license_path"]
        else:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "파일 구분이 잘못 입력 되었습니다.",
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "파일 구분이 잘못 입력 되었습니다.", None
            )

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

    elif fileType == "project":  # 프로젝트 파일일 경우
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "파일 다운로드 권한이 없습니다.", None
        )
        logs.war(
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
            "파일 유형이 잘못 입력 되었습니다.",
        )
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_DATAFAIL, "파일 유형이 잘못 입력 되었습니다.", None
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    logs.war(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "path : " + filePath + changeFile + ", name : " + originalFile,
    )

    # return send_file(filePath+changeFile, attachment_filename=originalFile.encode('utf-8').decode('iso-8859-1'), as_attachment=True)
    return send_file(
        filePath + changeFile, download_name=originalFile, as_attachment=True
    )
    # return send_file(filePath+changeFile, attachment_filename=originalFile.encode('utf-8'), as_attachment=True)


# 4. 파일 전송다운로드 API
@commManageApi.route("/docFileDownload", methods=["POST"])
def docFileDownload():
    commServ = commonService()
    servUserMana = servUserManage()

    servProjUseMaterMana = servProjectUseMaterialManage()

    sProjMana = sqlProjectManage()

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    commUtilServ = commUtilService()

    sysCd = request.headers.get("sysCd")
    token = request.headers.get("token")
    params = request.get_json()  # login parameter recv

    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        str(params),
    )
    # System Code Check
    result, resultData = commServ.checkSystemCd(sysCd)
    if result == False:
        return resultData

    # Token Code Check
    result, resultData = commServ.checkTokenCd(token)
    if result == False:
        return resultData

    consCode = params["consCode"]
    sysDocNum = params["sysDocNum"]
    filePath = params["filePath"]
    oriName = params["oriName"]
    chaName = params["chaName"]

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
        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_454, "", None)
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )
        return result

    """
마스터 -> 그냥 다보임
발주처 -> 프로젝트참여
본사 -> 그냥 다보임 자기회사 한정
디자인 -> 프로젝트참여
시공 -> 프로덱트참여
"""
    logs.debug(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        f"image auth check1 {loginUserInfo['authority_code']}",
    )
    #################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
    if loginUserInfo["authority_code"] == constants.USER_CONSTRUCTOR:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
        )

        query = sProjMana.sGetJobTitleCdObj(
            consCode, loginUserInfo["id"], loginUserInfo["co_code"]
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
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "현재 프로젝트 참여자가 아닙니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

    #### 자기회사의 프로젝트이면 보인다
    elif (loginUserInfo["authority_code"] == constants.USER_MONITOR or 
    loginUserInfo["authority_code"] == constants.USER_BUYER):
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "image auth check2",
        )
        query = sProjMana.sGetCompanyin(consCode, loginUserInfo["co_code"])
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetCompanyin Query : " + query,
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
                constants.REST_RESPONSE_CODE_DATAFAIL, "현재 프로젝트 참여회사가 아닙니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            f"권한 존재: {consCode}, {loginUserInfo['id']}",
        )

    return send_file(filePath + chaName, download_name=oriName, as_attachment=True)


# 회사 정보 리스트 제공 API
#
# Parameter
# 	- co_name | String | 회사명
# @commManageApi.route('/getCoList/<coName>', methods=['GET'])
@commManageApi.route("/getCoList", methods=["POST"])
def getCoList():
    # 	coName = urllib.parse.unquote(coName)
    # coName = coName.decode('cp949').encode('utf-8')

    commServ = commonService()
    servCommMana = servCommManage()
    commUtilServ = commUtilService()

    try:
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 회사 리스트 제공 시작  ----------",
        )

        sysCd = request.headers.get("sysCd")
        params = request.get_json()

        coName = params["coName"]

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "request header sysCd : " + sysCd + " / request url reqType : " + coName,
        )

        # System Code Check
        result, resultData = commServ.checkSystemCd(sysCd)
        if result == False:
            return resultData

        if commUtilServ.dataCheck(coName) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "회사명을 입력하여 주시기 바랍니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 회사 리스트를 가져 온다. ----------",
        )

        resCd, msg, resData = servCommMana.getCoList(coName)

        if resCd != 0:
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

        # Response data 생성
        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_ZERO, msg, resData
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response: " + commUtilServ.jsonDumps(result),
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
        "Response : " + commUtilServ.jsonDumps(result),
    )

    return result
