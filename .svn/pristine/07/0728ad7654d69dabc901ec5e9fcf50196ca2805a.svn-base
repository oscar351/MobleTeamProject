# _*_coding: utf-8 -*-


from flask import Blueprint, request
import os
import sys
import json
import copy

projectWorkLogManageApi = Blueprint("projectWorkLogManageApi", __name__)


from projectWorkLogManage.servProjectWorkLogManage import servProjectWorkLogManage
from projectProcessManage.servProjectProcessManage import servProjectProcessManage
from userManage.servUserManage import servUserManage
from commManage.servCommManage import servCommManage
import common.util_time as util_time

from allscapeAPIMain import procName
from allscapeAPIMain import db
from projectManage.sqlProjectManage import sqlProjectManage
from projectManage.servProjectManage import servProjectManage

from historyManage.servHistoryManage import servHistoryManage

from common.commUtilService import commUtilService
from common.commonService import commonService
from common.logManage import logManage
from common import constants

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


# 작업일지 리스트 조회 API
@projectWorkLogManageApi.route("/searchWorkLogList", methods=["POST"])
def searchWorkLogList():
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servProjWorkLogMana = servProjectWorkLogManage()

    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업일지 리스트 조회 시작 ----------",
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

        jobResData = None
        if params["search_cons_code"] != "":
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
                    and loginUserInfo["authority_code"]
                    != constants.USER_AUTH_SUPERVISOR
                    and loginUserInfo["authority_code"]
                    != constants.USER_AUTH_SUPERVISOR_MONITOR
                    and loginUserInfo["authority_code"]
                    != constants.USER_AUTH_INOCCUPATION
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
        # 		else:
        # 			result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
        # 					'프로젝트 코드가 누락 되었습니다.',
        # 					None)

        # 			logs.war(procName,
        # 					os.path.basename(__file__),
        # 					sys._getframe(0).f_code.co_name,
        # 					u'Response : ' + commUtilServ.jsonDumps(result))

        # 			return result

        #################################### 작업일지를 조회 한다. ####################################
        resCd, msg, resDataList = servProjWorkLogMana.searchWorkLogList(
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

        #################################### 작업일지 리스트 수를 조회 한다. ####################################
        resCd, msg, resDataCnt = servProjWorkLogMana.searchWorkLogListCnt(
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
            "---------- 작업일지 리스트를 조회 한다. 종료 ----------",
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


# 사진 대지 리스트 조회 API
@projectWorkLogManageApi.route(
    "/searchWorkImgList/<consCode>/<searchStartDate>/<searchEndDate>", methods=["GET"]
)
def searchWorkImgList(consCode, searchStartDate, searchEndDate):
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servProjWorkLogMana = servProjectWorkLogManage()
    servHisMana = servHistoryManage()

    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업 이미지 리스트 조회 시작 ----------",
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
            + " / request Url consCode : "
            + consCode
            + ", searchStartDate : "
            + searchStartDate
            + ", searchEndDate : "
            + searchEndDate,
        )

        # System Code Check
        result, resultData = commServ.checkSystemCd(sysCd)
        if result == False:
            return resultData

        # Token Check
        result, resultData = commServ.checkTokenCd(token)
        if result == False:
            return resultData

            # 프로젝트(공사) 코드를 체크 한다.
        if commUtilServ.dataCheck(consCode) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "프로젝트 코드를 입력하여 주시기 바랍니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

            # 조회 시작 날짜를 체크 한다.
        if commUtilServ.dataCheck(searchStartDate) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "조회 시작 날짜를 입력하여 주시기 바랍니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

            # 조회 종료 날짜를 체크 한다.
        if commUtilServ.dataCheck(searchEndDate) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "조회 종료 날짜를 입력하여 주시기 바랍니다.", None
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
        #  무직자가 작업일지
        if loginUserInfo["co_code"] == "":
            # 프로젝트에 해당하는 회사 코드를 가져 온다.
            searchList = []
            searchInfo = {"key": "ID", "value": loginUserInfo["id"]}
            searchList.append(searchInfo)
            searchInfo = {"key": "CONS_CODE", "value": consCode}
            searchList.append(searchInfo)

            resCd, msg, projHisInfo = servHisMana.getProjHisList(searchList)
            # if resCd == 0:
            loginUserInfo["co_code"] = projHisInfo[0]["co_code"]

        jobResData = None
        #################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
        if (
            loginUserInfo["authority_code"] == constants.USER_BUYER
            or loginUserInfo["authority_code"] == constants.USER_CONSTRUCTOR
        ):
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
        elif loginUserInfo["authority_code"] == constants.USER_MONITOR:
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
        # 		else:
        # 			result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
        # 					'프로젝트 코드가 누락 되었습니다.',
        # 					None)

        # 			logs.war(procName,
        # 					os.path.basename(__file__),
        # 					sys._getframe(0).f_code.co_name,
        # 					u'Response : ' + commUtilServ.jsonDumps(result))

        # 			return result

        # 검색조건이 있을 경우 추가로 저장한다
        search_name = {"pc_name": "", "product_name": ""}
        conditions = request.args.to_dict()
        allowed_keys = {"pc_name", "product_name"}
        for key in allowed_keys:
            if key in conditions:
                search_name[key] = str(conditions.get(key).replace(" ", ""))

        #################################### 작업일지를 조회 한다. ####################################
        resCd, msg, resDataList = servProjWorkLogMana.searchWorkImgList(
            consCode,
            loginUserInfo["authority_code"],
            loginUserInfo["co_code"],
            searchStartDate,
            searchEndDate,
            search_name,
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

        #################################### 작업일지 리스트 수를 조회 한다. ####################################
        # 		resCd, msg, resDataCnt = servProjWorkLogMana.searchWorkLogListCnt(loginUserInfo, loginUserInfo['authority_code'], jobResData, params)
        # Error 발생 시 에러 코드 리턴
        # 		if(resCd != 0):
        # 			logs.war(procName,
        # 					os.path.basename(__file__),
        # 					sys._getframe(0).f_code.co_name,
        # 					u'Database Error : ' + msg)
        # 			result = commServ.makeReturnMessage(resCd, msg, None)

        # 			logs.war(procName,
        # 					os.path.basename(__file__),
        # 					sys._getframe(0).f_code.co_name,
        # 					u'response : ' + commUtilServ.jsonDumps(result))

        # 			return result

        # 		resultData = {
        # 			'list' : resDataList,
        # 			'cnt' : str(resDataCnt['cnt'])
        # 		}

        ################################## Response 데이터를 생성 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Response 데이터를 생성 한다. ----------",
        )

        result = commServ.makeReturnMessage(resCd, msg, resDataList)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업 이미지 리스트를 조회 한다. 종료 ----------",
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


"""
# 작업 일지/일보 저장
@projectWorkLogManageApi.route('/putWorkDLInfo', methods=['PUT'])
def putWorkDLInfo():
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servProjDocMana = servProjectDocManage()
    servProjUseMatMana = servProjectUseMaterialManage()
    servCommMana = servCommManage()

    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    try:
        logs.debug(
				procName,
				os.path.basename(__file__),
				sys._getframe(0).f_code.co_name,
				"---------- 작업 일지/일보 저장 처리 시작 ----------",
				)
        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        params = json.loads(request.form["data"], encoding="utf-8")

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
            return result

		#################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
        logs.debug(
				procName,
				os.path.basename(__file__),
				sys._getframe(0).f_code.co_name,
				"---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
				)
        query = sProjMana.sGetJobTitleCdObj(
				params["reqDocInfo"]["cons_code"], loginUserInfo["id"]
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
					constants.REST_RESPONSE_CODE_DATAFAIL,
					"현재 프로젝트에 참여하고 있지 않아 작업 일지 및 일보를 저장 할 수 없습니다.",
					None,
					)
            logs.war(
					procName,
					os.path.basename(__file__),
					sys._getframe(0).f_code.co_name,
					"Response : " + commUtilServ.jsonDumps(result),
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
"""


# 작업 일지 리스트 조회
@projectWorkLogManageApi.route("/WorkDiary/<cons_code>", methods=["GET"])
def getWorkDiary(cons_code):
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()

    servHisMana = servHistoryManage()

    sProjMana = sqlProjectManage()
    servPWMana = servProjectWorkLogManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업 일지/일보 조회 시작 ----------",
        )
        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")

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

        # 로그인 된 사용자 인지 확인한다.
        # result, resultData = commServ.userLoginChk(token, sysCd)
        # if result == False:
        #    return resultData

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
            return result

        #################################### 로직에 필요한 변수를 저장한다. ####################################
        params = {
            "cons_code": cons_code,
            "co_code": loginUserInfo["co_code"],
            "id": loginUserInfo["id"],
            "start_date": "",
            "end_date": "",
        }

        # 검색조건이 있을 경우 추가로 저장한다
        conditions = request.args.to_dict()
        allowed_keys = {"start_date", "end_date", "start_num", "end_num"}
        for key in allowed_keys:
            if key in conditions:
                params[key] = str(conditions.get(key))

        #  무직자가 작업일지
        if loginUserInfo["co_code"] == "":
            # 프로젝트에 해당하는 회사 코드를 가져 온다.
            searchList = []
            searchInfo = {"key": "ID", "value": loginUserInfo["id"]}
            searchList.append(searchInfo)
            searchInfo = {"key": "CONS_CODE", "value": params["cons_code"]}
            searchList.append(searchInfo)

            resCd, msg, projHisInfo = servHisMana.getProjHisList(searchList)
            # if resCd == 0:
            params["co_code"] = projHisInfo[0]["co_code"]
            resCd, msg, PWData = servPWMana.get_workdiary(
                params["cons_code"],
                params["co_code"],
                params["start_date"],
                params["end_date"],
            )
            if PWData:
                Result = {"count": len(PWData)}
                Result["data"] = PWData[
                    int(params["start_num"]) : int(params["end_num"])
                ]
            else:
                Result = {"count": 0, "data": []}
            return commServ.makeReturnMessage(resCd, msg, Result)

        #################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
        if (
            loginUserInfo["authority_code"] == constants.USER_BUYER
            or loginUserInfo["authority_code"] == constants.USER_CONSTRUCTOR
        ):
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
            )

            query = sProjMana.sGetJobTitleCdObj(
                params["cons_code"], loginUserInfo["id"], loginUserInfo["co_code"]
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
            resCd, msg, PWData = servPWMana.get_workdiary(
                params["cons_code"],
                params["co_code"],
                params["start_date"],
                params["end_date"],
            )

        #### 본사관리자는 자기회사의 프로젝트이면 모두 보인다
        elif loginUserInfo["authority_code"] == constants.USER_MONITOR:
            query = sProjMana.sGetCompanyin(
                params["cons_code"], loginUserInfo["co_code"]
            )
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
            resCd, msg, PWData = servPWMana.get_workdiary_master(
                params["cons_code"],
                params["co_code"],
                params["start_date"],
                params["end_date"],
            )
        #################################### 해당 작업일지 리스트를 제공한다 ##########################

        if PWData:
            Result = {"count": len(PWData)}
            Result["data"] = PWData[int(params["start_num"]) : int(params["end_num"])]
        else:
            Result = {"count": 0, "data": []}
        return commServ.makeReturnMessage(resCd, msg, Result)

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


# 작업 일지 삭제
@projectWorkLogManageApi.route(
    "/WorkDiary/<cons_code>/<sys_doc_num>", methods=["DELETE"]
)
def deleteWorkDiary(cons_code, sys_doc_num):
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servProjMana = servProjectManage()
    sProjMana = sqlProjectManage()
    servPWMana = servProjectWorkLogManage()
    servProjProMana = servProjectProcessManage()
    servProjWorkLogMana = servProjectWorkLogManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업 일지 삭제 시작 ----------",
        )
        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")

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

        # 로그인 된 사용자 인지 확인한다.
        result, resultData = commServ.userLoginChk(token, sysCd)
        if result == False:
            return resultData

        #################################### 프로젝트가 중지상태가 아닌지 확인한다 ###############################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 상태 정보를 가져온다. ----------",
        )

        resCd, msg, projectStatus = servProjMana.getProjectStatus(cons_code)
        if resCd != 0 or projectStatus["status"] == constants.PROJECT_STATUS_CD_STOP:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "작성할 수 없는 프로젝트 입니다",
            )
            return commServ.makeReturnMessage(resCd, msg, None)

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
            return result

        #################################### 로직에 필요한 변수를 저장한다. ####################################
        params = {
            "cons_code": cons_code,
            "co_code": loginUserInfo["co_code"],
            "id": loginUserInfo["id"],
            "sys_doc_num": sys_doc_num,
        }

        #################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
        if loginUserInfo["authority_code"] == constants.USER_CONSTRUCTOR:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
            )

            query = sProjMana.sGetJobTitleCdObj(
                params["cons_code"], loginUserInfo["id"], loginUserInfo["co_code"]
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

        else:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "일지 삭제 권한이 없습니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 일지 삭제 후 해당 작업일지 포함 폼목리스트를 제공한다 ##########################

        resCd, msg, _ = servPWMana.del_workdiary(
            params["cons_code"], params["co_code"], params["sys_doc_num"]
        )

        return commServ.makeReturnMessage(resCd, msg, None)

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


# 작업 상세내역 조회
@projectWorkLogManageApi.route("/DailyWork/<cons_code>/<sys_doc_num>", methods=["GET"])
def getDailyWorkAll(cons_code, sys_doc_num):
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servHisMana = servHistoryManage()
    sProjMana = sqlProjectManage()
    servPWMana = servProjectWorkLogManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업 일지/일보 조회 시작 ----------",
        )
        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")

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
            return result

        #################################### 로직에 필요한 변수를 저장한다. ####################################
        params = {
            "cons_code": cons_code,
            "co_code": loginUserInfo["co_code"],
            "sys_doc_num": sys_doc_num,
            # 				"cons_date": cons_date,
            "id": loginUserInfo["id"],
        }

        #  무직자가 작업일지
        if loginUserInfo["co_code"] == "":
            # 프로젝트에 해당하는 회사 코드를 가져 온다.
            searchList = []
            searchInfo = {"key": "ID", "value": loginUserInfo["id"]}
            searchList.append(searchInfo)
            searchInfo = {"key": "CONS_CODE", "value": params["cons_code"]}
            searchList.append(searchInfo)

            resCd, msg, projHisInfo = servHisMana.getProjHisList(searchList)
            # if resCd == 0:
            loginUserInfo["co_code"] = projHisInfo[0]["co_code"]

        #################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
        if (
            loginUserInfo["authority_code"] == constants.USER_BUYER
            or loginUserInfo["authority_code"] == constants.USER_CONSTRUCTOR
        ):
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
            )

            query = sProjMana.sGetJobTitleCdObj(
                params["cons_code"], loginUserInfo["id"], loginUserInfo["co_code"]
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
        elif loginUserInfo["authority_code"] == constants.USER_MONITOR:
            query = sProjMana.sGetCompanyin(
                params["cons_code"], loginUserInfo["co_code"]
            )
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

        #################################### 해당 일일 작업현황을 제공한다 ##########################
        # else:
        #    loginUserInfo['co_code'] = ""
        # resCd, msg, result = servPWMana.get_workdetails(params["cons_code"], params["co_code"], params["cons_date"])
        resCd, msg, result = servPWMana.get_workdetails(
            cons_code, sys_doc_num, loginUserInfo["co_code"]
        )
        return commServ.makeReturnMessage(resCd, msg, result)

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


# 0203 희정 추가
# 작업 일지/일보 저장
@projectWorkLogManageApi.route("/WorkDLInfo", methods=["POST"])
def postWorkDLInfo():
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    # servProjDocMana = servProjectDocManage()
    # servProjUseMatMana = servProjectUseMaterialManage()
    servCommMana = servCommManage()
    servProjMana = servProjectManage()
    servProjWorkLogMana = servProjectWorkLogManage()
    servProjProMana = servProjectProcessManage()

    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업 일지/일보 저장 처리 시작 ----------",
        )
        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        params = json.loads(request.form["data"], encoding="utf-8")

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

        # 로그인 된 사용자 인지 확인한다.
        result, resultData = commServ.userLoginChk(token, sysCd)
        if result == False:
            return resultData

        #################################### 프로젝트가 중지상태가 아닌지 확인한다 ###############################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 상태 정보를 가져온다. ----------",
        )

        resCd, msg, projectStatus = servProjMana.getProjectStatus(params["cons_code"])
        if resCd != 0 or projectStatus["status"] == constants.PROJECT_STATUS_CD_STOP:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "작성할 수 없는 프로젝트 입니다",
            )
            return commServ.makeReturnMessage(resCd, msg, None)

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
            return result

        #################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
        )
        query = sProjMana.sGetJobTitleCdObj(params["cons_code"], loginUserInfo["id"])
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
                "현재 프로젝트에 참여하고 있지 않아 작업 일지 및 일보를 저장 할 수 없습니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        # 1. 시스템 문서 번호를 생성한다.
        resCd, msg, sysDocNum = servCommMana.createSysDocNum()
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

        # 2. 시스템 문서 번호를 증가한다.
        resCd, msg, tmp = servCommMana.increaseSysDocNum()
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

        # 3. 작성 날짜를 생성 한다.
        writerDate = util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14)

        # 4. 작업 일지 정보를 저장 한다.
        # 4-1. 작업일지 저장 데이터를 생성 한다.
        diaryInfo = {
            "cons_code": params["cons_code"],
            "co_code": loginUserInfo["co_code"],
            "sys_doc_num": sysDocNum,
            "cons_date": str(params["cons_date"]) + "000000",
            "work_title": params["cons_date"][0:4]
            + "-"
            + str(params["cons_date"][4:6])
            + "-"
            + str(params["cons_date"][6:8])
            + " 작업 일지 및 작업 일보",
            "work_diary_content": params["work_diary"],
            # 			'work_log_cons_code' : '',
            "write_date": writerDate,
            "id": loginUserInfo["id"],
            "today_content": params["cons_content_info"]["today_content"],
            "next_content": params["cons_content_info"]["next_content"],
            "temperature": params["cons_content_info"]["temperature"],
            "sky_result": params["cons_content_info"]["sky_result"],
            "pty_result": params["cons_content_info"]["pty_result"],
        }
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "paaass1",
        )
        # 4-2. 작업일지 데이터 저장
        resCd, msg, resData = servProjWorkLogMana.putDiaryInfo(diaryInfo)
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
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "paaass2",
        )
        # 5. 작업 일지 파일을 저장 한다.
        #        resCd, msg, resData = servProjWorkLogMana.imageFileManage(
        # 				'Diary',
        # 				diaryInfo,
        # 				params['diary']['imageList'],
        # 				request)
        #        if resCd != 0:

        # 관련 파일 정보를 불러 온다.
        #            resCd, msg, resData = servProjWorkLogMana.getImageFileInfo(diaryInfo['cons_code'], loginUserInfo['co_code'], diaryInfo['sys_doc_num'])
        #            if resCd == 0 and resData != None:
        #                servProjWorkLogMana.removeImageFile(resData)
        # 작업 일지/일보 파일 정보 삭제
        #            servProjWorkLogMana.delImageFileInfo(diaryInfo['cons_code'], loginUserInfo['co_code'], diaryInfo['sys_doc_num'])
        # 작업 일지 정보 정보 삭제
        #            servProjWorkLogMana.delDiaryInfo(diaryInfo['cons_code'], loginUserInfo['co_code'], diaryInfo['sys_doc_num'])
        #            logs.war(
        # 					procName,
        # 					os.path.basename(__file__),
        # 					sys._getframe(0).f_code.co_name,
        # 					"Database Error : " + msg,
        # 					)
        #
        #            result = commServ.makeReturnMessage(resCd, msg, None)
        #            logs.war(
        # 					procName,
        # 					os.path.basename(__file__),
        # 					sys._getframe(0).f_code.co_name,
        # 					"response : " + commUtilServ.jsonDumps(result),
        # 					)
        #            return result

        # 6. 작업 일보 정보를 저장 한다.
        logList = params["cons_work_info"]
        for logInfo in logList:
            logDataInfo = {
                "cons_code": params["cons_code"],
                "co_code": loginUserInfo["co_code"],
                "sys_doc_num": sysDocNum,
                "cons_date": str(params["cons_date"]) + "000000",
                "cons_type_cd": logInfo["cons_type_cd"],
                "work_log_cons_code": logInfo["work_log_cons_code"],
                # "prev_workload": logInfo["prev_workload"],
                "today_workload": logInfo["today_workload"],
                "next_workload": logInfo["next_workload"],
                "work_log_cons_lv1": logInfo["cons_lv1"],
                "work_log_cons_lv2": logInfo["cons_lv2"],
                "work_log_cons_lv3": logInfo["cons_lv3"],
                "work_log_cons_lv4": logInfo["cons_lv4"],
                # 				'work_log_use_amount' : logInfo['use_amount'],
                # 		    	'work_log_content' : logInfo['content'],
                "log_index": logInfo["log_index"],
                "write_date": writerDate,
            }

            # 4-2. 작업일보 데이터 저장
            resCd, msg, resData = servProjWorkLogMana.putWorkLogInfo(logDataInfo)
            if resCd != 0:
                # 관련 파일 정보를 불러 온다.
                resCd, msg, resData = servProjWorkLogMana.getImageFileInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
                if resCd == 0 and resData != None:
                    servProjWorkLogMana.removeImageFile(resData)
                # 작업 일지/일보 파일 정보 삭제
                servProjWorkLogMana.delImageFileInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
                # 작업 일보 정보 정보 삭제
                servProjWorkLogMana.delWorkLogInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
                # 작업 일지 정보 정보 삭제
                servProjWorkLogMana.delDiaryInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
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
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "paaass4",
            )
            # 7. 작업 일보 파일을 저장 한다.
            resCd, msg, resData = servProjWorkLogMana.imageFileManage(
                "Log", logDataInfo, logInfo["imageList"], request
            )
            if resCd != 0:
                # 관련 파일 정보를 불러 온다.
                resCd, msg, resData = servProjWorkLogMana.getImageFileInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
                if resCd == 0 and resData != None:
                    servProjWorkLogMana.removeImageFile(resData)
                # 작업 일지/일보 파일 정보 삭제
                servProjWorkLogMana.delImageFileInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
                # 작업 일보 정보 정보 삭제
                servProjWorkLogMana.delWorkLogInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
                # 작업 일지 정보 정보 삭제
                servProjWorkLogMana.delDiaryInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
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

            # 9. 총 자재사용량 업데이트
            resCd, msg, resData = servProjProMana.update_process_auto(
                logDataInfo["cons_code"],
                loginUserInfo["co_code"],
                logInfo["work_log_cons_code"],
            )

            if resCd != 0:
                # 관련 파일 정보를 불러 온다.
                resCd, msg, resData = servProjWorkLogMana.getImageFileInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
                if resCd == 0 and resData != None:
                    servProjWorkLogMana.removeImageFile(resData)

                # 작업 일지/일보 파일 정보 삭제
                servProjWorkLogMana.delImageFileInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
                # 작업 일보 정보 정보 삭제
                servProjWorkLogMana.delWorkLogInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
                # 작업 일지 정보 정보 삭제
                servProjWorkLogMana.delDiaryInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )

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
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "paaass7",
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "--------------------------------------------------------------5",
        )
        manpList = params["cons_manp_info"]
        for manp in manpList:
            # 8. 투입 인력 정보를 저장 한다.
            workManpowerInfo = {
                "cons_code": params["cons_code"],
                "co_code": loginUserInfo["co_code"],
                "sys_doc_num": sysDocNum,
                "cons_date": str(params["cons_date"]) + "000000",
                "cons_type_cd": manp["cons_type_cd"],
                "work_log_cons_code": manp["work_log_cons_code"],
                "prev_manpower": manp["prev_manpower"],
                "today_manpower": manp["today_manpower"],
                "next_manpower": manp["next_manpower"],
            }

            resCd, msg, resData = servProjWorkLogMana.putWorkManpowerInfo(
                workManpowerInfo
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "resCd : " + str(resCd),
            )
            if resCd != 0:
                # 인력 정보를 삭제
                servProjWorkLogMana.delWorkManpowerInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
                # 관련 파일 정보를 불러 온다.
                resCd, msg, resData = servProjWorkLogMana.getImageFileInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
                if resCd == 0 and resData != None:
                    servProjWorkLogMana.removeImageFile(resData)
                # 작업 일지/일보 파일 정보 삭제
                servProjWorkLogMana.delImageFileInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
                # 작업 일보 정보 정보 삭제
                servProjWorkLogMana.delWorkLogInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
                # 작업 일지 정보 정보 삭제
                servProjWorkLogMana.delDiaryInfo(
                    logDataInfo["cons_code"],
                    loginUserInfo["co_code"],
                    logDataInfo["sys_doc_num"],
                )
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
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "paaass8",
        )
        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
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


#### 조현우 추가 작업일지 수정 ####
@projectWorkLogManageApi.route("/WorkDLInfo/<cons_code>/<sys_doc_num>", methods=["PUT"])
def putWorkDLInfo(cons_code, sys_doc_num):
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    # servProjDocMana = servProjectDocManage()
    # servProjUseMatMana = servProjectUseMaterialManage()
    servCommMana = servCommManage()
    servProjMana = servProjectManage()
    servProjWorkLogMana = servProjectWorkLogManage()
    servProjProMana = servProjectProcessManage()

    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업 일지/일보 수정 처리 시작 ----------",
        )
        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        params_list = json.loads(request.form["data"], encoding="utf-8")["data"]
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

        # 로그인 된 사용자 인지 확인한다.
        result, resultData = commServ.userLoginChk(token, sysCd)
        if result == False:
            return resultData

        #################################### 프로젝트가 중지상태가 아닌지 확인한다 ###############################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 상태 정보를 가져온다. ----------",
        )

        resCd, msg, projectStatus = servProjMana.getProjectStatus(cons_code)
        if resCd != 0 or projectStatus["status"] == constants.PROJECT_STATUS_CD_STOP:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "작성할 수 없는 프로젝트 입니다",
            )
            return commServ.makeReturnMessage(resCd, msg, None)

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
            return result

        #################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
        )
        query = sProjMana.sGetJobTitleCdObj(cons_code, loginUserInfo["id"])
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
                "현재 프로젝트에 참여하고 있지 않아 작업 일지 및 일보를 수정 할 수 없습니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #### 순차적으로 수정 명령 수행 ####
        #### 작업일보 -> 수정만 가능
        #### 작업로그 -> 추가, 수정, 삭제 가능
        #### 작업인력 -> 추가, 수정, 삭제 가능
        #### 이미지는 작업로그에 속해 있으므로, 작업인력 추가시 같이 추가 가능, 삭제시 연동 이미지 삭제
        for index, params in zip(range(len(params_list)), params_list):
            if params["type"] == "diary":
                if params["mode"] == "U":  # 업데이트 모드
                    resCd, msg, _ = servProjWorkLogMana.changeDiaryInfo(
                        loginUserInfo["id"], params, sys_doc_num
                    )

            elif params["type"] == "log":
                if params["mode"] == "A":  # 추가 모드
                    resCd, msg, _ = servProjWorkLogMana.postWorkLogInfo(
                        cons_code,
                        loginUserInfo["co_code"],
                        params,
                        sys_doc_num,
                        request.files.getlist(f"f_{index}"),
                    )

                elif params["mode"] == "U":  # 업데이트 모드
                    resCd, msg, _ = servProjWorkLogMana.changeWorkLogInfo(
                        params, sys_doc_num
                    )

                elif params["mode"] == "D":  # 삭제 모드
                    resCd, msg, _ = servProjWorkLogMana.deleteWorkLogInfo(
                        cons_code, loginUserInfo["co_code"], params, sys_doc_num
                    )

                servProjProMana.update_process_auto(
                    cons_code, loginUserInfo["co_code"], params["work_log_cons_code"]
                )

            elif params["type"] == "manpower":
                if params["mode"] == "A":  # 추가 모드
                    resCd, msg, _ = servProjWorkLogMana.postManpowerInfo(
                        cons_code, loginUserInfo["co_code"], params, sys_doc_num
                    )
                if params["mode"] == "U":  # 업데이트 모드
                    resCd, msg, _ = servProjWorkLogMana.changeManpowerInfo(
                        params, sys_doc_num
                    )
                elif params["mode"] == "D":  # 삭제 모드
                    resCd, msg, _ = servProjWorkLogMana.deleteManpowerInfo(
                        params, sys_doc_num
                    )

        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
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


#### 조현우 추가 작업일지 이미지 추가 ####
@projectWorkLogManageApi.route(
    "/WorkDLImage/<cons_code>/<sys_doc_num>/<file_index>", methods=["POST"]
)
def postWorkLogImage(cons_code, sys_doc_num, file_index):
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    # servProjDocMana = servProjectDocManage()
    # servProjUseMatMana = servProjectUseMaterialManage()
    servCommMana = servCommManage()
    servProjWorkLogMana = servProjectWorkLogManage()
    servProjProMana = servProjectProcessManage()
    servProjMana = servProjectManage()
    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업 일보 이미지 등록 처리 시작 ----------",
        )
        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        params = json.loads(request.form["data"], encoding="utf-8")

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

        # 로그인 된 사용자 인지 확인한다.
        result, resultData = commServ.userLoginChk(token, sysCd)
        if result == False:
            return resultData

        #################################### 프로젝트가 중지상태가 아닌지 확인한다 ###############################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 상태 정보를 가져온다. ----------",
        )

        resCd, msg, projectStatus = servProjMana.getProjectStatus(cons_code)
        if resCd != 0 or projectStatus["status"] == constants.PROJECT_STATUS_CD_STOP:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "작성할 수 없는 프로젝트 입니다",
            )
            return commServ.makeReturnMessage(resCd, msg, None)

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
            return result

        #################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
        )
        query = sProjMana.sGetJobTitleCdObj(cons_code, loginUserInfo["id"])
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
                "현재 프로젝트에 참여하고 있지 않아 작업 일지 및 일보를 수정 할 수 없습니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        resCd, msg, _ = servProjWorkLogMana.postWorkLogImage(
            cons_code,
            loginUserInfo["co_code"],
            params,
            sys_doc_num,
            file_index,
            request.files["f_image"],
        )

        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
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


#### 조현우 추가 작업일지 이미지 제목변경 ####
@projectWorkLogManageApi.route(
    "/WorkDLImage/<cons_code>/<sys_doc_num>/<work_log_cons_code>/<file_index>",
    methods=["PUT"],
)
def putWorkLogImage(cons_code, sys_doc_num, work_log_cons_code, file_index):
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    # servProjDocMana = servProjectDocManage()
    # servProjUseMatMana = servProjectUseMaterialManage()
    servCommMana = servCommManage()
    servProjWorkLogMana = servProjectWorkLogManage()
    servProjProMana = servProjectProcessManage()
    servProjMana = servProjectManage()
    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업 일보 이미지 등록 처리 시작 ----------",
        )
        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        params = request.get_json()

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

        # 로그인 된 사용자 인지 확인한다.
        result, resultData = commServ.userLoginChk(token, sysCd)
        if result == False:
            return resultData

        #################################### 프로젝트가 중지상태가 아닌지 확인한다 ###############################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 상태 정보를 가져온다. ----------",
        )

        resCd, msg, projectStatus = servProjMana.getProjectStatus(cons_code)
        if resCd != 0 or projectStatus["status"] == constants.PROJECT_STATUS_CD_STOP:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "작성할 수 없는 프로젝트 입니다",
            )
            return commServ.makeReturnMessage(resCd, msg, None)

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
            return result

        #################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
        )
        query = sProjMana.sGetJobTitleCdObj(cons_code, loginUserInfo["id"])
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
                "현재 프로젝트에 참여하고 있지 않아 작업 일지 및 일보를 수정 할 수 없습니다.",
                None,
            )
            return result

        resCd, msg, _ = servProjWorkLogMana.putWorkLogImage(
            cons_code,
            loginUserInfo["co_code"],
            sys_doc_num,
            work_log_cons_code,
            file_index,
            params["title"],
        )

        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)
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


#### 조현우 추가 작업일지 이미지 삭제 ####
@projectWorkLogManageApi.route(
    "/WorkDLImage/<cons_code>/<sys_doc_num>/<work_log_cons_code>/<file_index>",
    methods=["DELETE"],
)
def deleteWorkLogImage(cons_code, sys_doc_num, work_log_cons_code, file_index):
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    # servProjDocMana = servProjectDocManage()
    # servProjUseMatMana = servProjectUseMaterialManage()
    servCommMana = servCommManage()
    servProjMana = servProjectManage()
    servProjWorkLogMana = servProjectWorkLogManage()
    servProjProMana = servProjectProcessManage()

    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업 일보 수정 이미지 삭제처리 시작 ----------",
        )
        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")

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

        # 로그인 된 사용자 인지 확인한다.
        result, resultData = commServ.userLoginChk(token, sysCd)
        if result == False:
            return resultData

        #################################### 프로젝트가 중지상태가 아닌지 확인한다 ###############################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 상태 정보를 가져온다. ----------",
        )

        resCd, msg, projectStatus = servProjMana.getProjectStatus(cons_code)
        if resCd != 0 or projectStatus["status"] == constants.PROJECT_STATUS_CD_STOP:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "작성할 수 없는 프로젝트 입니다",
            )
            return commServ.makeReturnMessage(resCd, msg, None)

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
            return result

        #################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
        )
        query = sProjMana.sGetJobTitleCdObj(cons_code, loginUserInfo["id"])
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
                "현재 프로젝트에 참여하고 있지 않아 작업 일지 및 일보를 수정 할 수 없습니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        resCd, msg, _ = servProjWorkLogMana.deleteWorkLogImage(
            cons_code,
            loginUserInfo["co_code"],
            sys_doc_num,
            work_log_cons_code,
            file_index,
        )

        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)

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
