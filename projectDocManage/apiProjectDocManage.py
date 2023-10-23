# _*_coding: utf-8 -*-

from flask import Blueprint, request
import json
import copy
import os
import sys

projectDocManageApi = Blueprint("projectDocManageApi", __name__)

from projectDocManage.servProjectDocManage import servProjectDocManage

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.logManage import logManage
from common import constants
from common.commUtilService import commUtilService
from common.commonService import commonService
from common import util_time
from common.docContentService import (
    docContentService,
    ConstrDetailReq,
    ConstrDetailNtc,
    PlanReviewRPT,
    OnSiteSituationRPT,
    ConstrChangeReview,
)

from userManage.servUserManage import servUserManage
from projectManage.sqlProjectManage import sqlProjectManage

from commManage.servCommManage import servCommManage

from projectApproMaterManage.servProjectApproMaterManage import (
    servProjectApproMaterManage,
)
from projectUseMaterialManage.servProjectUseMaterialManage import (
    servProjectUseMaterialManage,
)

from projectInspMaterManage.servProjectInspMaterManage import servProjectInspMaterManage

from projectDetectionManage.servProjectDetectionManage import servProjectDetectionManage

from projectWorkLogManage.servProjectWorkLogManage import servProjectWorkLogManage

from projectManage.servProjectManage import servProjectManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


# 문서 생성
@projectDocManageApi.route("/createDocument/<consCode>/<docCode>", methods=["GET"])
def createDocument(consCode, docCode):

    commServ = commonService()
    servUserMana = servUserManage()
    commUtilServ = commUtilService()
    servProjDocMana = servProjectDocManage()

    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

    try:
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
            + " / request url consCode : "
            + consCode
            + ", docCode : "
            + docCode,
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

            #################################### 작성자가 작성 할 수 있는 문서가 맞는지 확인 한다. ####################################
        resCd, msg, resData = servProjDocMana.getDocumentInfo(
            consCode, docCode, loginUserInfo["co_code"]
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

        if resData == None:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "작성 할 수 있는 문서가 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        if docCode == constants.CD_DOC_MATSELAPPREQ:  # 자재 선정 승인 요청

            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                (jobResData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTOR)
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_MAIN
                )
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_SUB
                )
            ):
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

        elif docCode == constants.SD_DOC_MATSELAPPRES:  # 자재 선정 승인 통보
            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN
            ) and (
                jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_SUB
            ):
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

        elif docCode == constants.CD_DOC_WORKLOG:  # 자재 선정 승인 통보
            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                (jobResData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTOR)
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_MAIN
                )
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_SUB
                )
            ):
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

            # 인력 통계/ 장비 통계, 작업량 통계를 가져 온다.
            resCd, msg, workLogData = getWorkLogBasicData(consCode, loginUserInfo)
            if resCd != 0:
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "데이터를 불러 올 수 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

            responseData = {"initData": workLogData}

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

        responseData = {"docInitInfo": resData, "userInfo": loginUserInfo}

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


# 문서 조회
@projectDocManageApi.route("/searchDocList", methods=["POST"])
def searchDocList():
    commServ = commonService()
    commUtilServ = commUtilService()
    servProjDocMana = servProjectDocManage()
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
            "request header token : " + token + ", sysCd : " + sysCd
            #           + u' / request params data : ' + params)
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

        jobResData = None
        if params["cons_code"] != "":
            #################################### 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
            )
            query = sProjMana.sGetJobTitleCdObj(
                params["cons_code"], loginUserInfo["id"]
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
                # if(loginUserInfo['authority_code'] == constants.USER_AUTH_BUYER
                # 		or loginUserInfo['authority_code'] == constants.USER_AUTH_DESIGNER
                # 		or loginUserInfo['authority_code'] == constants.USER_AUTH_CONTRACTION
                # 		or loginUserInfo['authority_code'] == constants.USER_AUTH_SUPERVISING
                # 		or loginUserInfo['authority_code'] == constants.USER_AUTH_WHITEHALL
                # 		or loginUserInfo['authority_code'] == constants.USER_AUTH_INOCCUPATION):
                if (
                    loginUserInfo["authority_code"] == constants.USER_AUTH_DESIGNER
                    or loginUserInfo["authority_code"]
                    == constants.USER_AUTH_CONTRACTION
                    or loginUserInfo["authority_code"]
                    == constants.USER_AUTH_SUPERVISING
                    or loginUserInfo["authority_code"]
                    == constants.USER_AUTH_INOCCUPATION
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

                    #################################### 문서 리스트를 조회 힌다. ####################################
        resCd, msg, resDocList = servProjDocMana.searchDocList(
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

            #################################### 연결된 문서 조회  ####################################

        for index in range(0, len(resDocList)):
            resCd, msg, resLinkDocList = servProjDocMana.getLinkDocList(
                resDocList[index]["cons_code"], resDocList[index]["sys_doc_num"]
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

            resDocList[index]["linkDocList"] = resLinkDocList

            #################################### 문서 리스트 개수를 조회 힌다. ####################################
        resCd, msg, resDocListCnt = servProjDocMana.searchDocListCnt(
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

        responseData = {"list": resDocList, "cnt": resDocListCnt["cnt"]}

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


# 문서 상세 정보 조회
@projectDocManageApi.route("/getDocDetailInfo/<consCode>/<sysDocNum>", methods=["GET"])
def getDocDetailInfo(consCode, sysDocNum):

    commServ = commonService()
    commUtilServ = commUtilService()
    servProjDocMana = servProjectDocManage()
    servUserMana = servUserManage()

    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    try:
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
            + " / request url consCode : "
            + consCode
            + ", sysDocNum : "
            + sysDocNum,
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
        # 	if(loginUserInfo['authority_code'] == constants.USER_AUTH_BUYER
        # 			or loginUserInfo['authority_code'] == constants.USER_AUTH_DESIGNER
        # 			or loginUserInfo['authority_code'] == constants.USER_AUTH_CONTRACTION
        # 			or loginUserInfo['authority_code'] == constants.USER_AUTH_SUPERVISING
        # 			or loginUserInfo['authority_code'] == constants.USER_AUTH_WHITEHALL
        # 			or loginUserInfo['authority_code'] == constants.USER_AUTH_INOCCUPATION):
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
            if (
                loginUserInfo["authority_code"] == constants.USER_AUTH_DESIGNER
                or loginUserInfo["authority_code"] == constants.USER_AUTH_CONTRACTION
                or loginUserInfo["authority_code"] == constants.USER_AUTH_SUPERVISING
                or loginUserInfo["authority_code"] == constants.USER_AUTH_INOCCUPATION
            ):

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

                #################################### 문서 상세 정보를 조회 한다. ####################################
        resCd, msg, resDocInfo = servProjDocMana.getDocDetailInfo(
            loginUserInfo,
            loginUserInfo["authority_code"],
            jobResData,
            consCode,
            sysDocNum,
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

        if resDocInfo == None:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + commUtilServ.jsonDumps(msg),
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "문서 정보가 존재하지 않거나 조회 할 수 없는 문서 입니다.",
                None,
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        resDocInfo["content"] = json.loads(resDocInfo["content"])

        #################################### 문서 결재자 정보를 조회 한다. ####################################
        resCd, msg, resApprovalInfo = servProjDocMana.getDocApprovalInfo(
            consCode, sysDocNum
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

        if resApprovalInfo == None:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + commUtilServ.jsonDumps(msg),
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "결재자 정보를 조회 할 수 없습니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

            #################################### 연결된 문서 조회  ####################################
        resCd, msg, resLinkDocList = servProjDocMana.getLinkDocList(consCode, sysDocNum)
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

        responseData = {
            "docInfo": resDocInfo,
            "approInfo": resApprovalInfo,
            "linkDocList": resLinkDocList,
        }

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


# 문서 결재
@projectDocManageApi.route("/documentApproval", methods=["POST"])
def documentApproval():
    commServ = commonService()
    commUtilServ = commUtilService()
    servProjDocMana = servProjectDocManage()
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
            "request header token : " + token + ", sysCd : " + sysCd
            #           + u' / request params data : ' + params)
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

            #################################### 결재자 정보를 업데이트 한다. ####################################
        # 현재 결재 정보를 업데이트 한다.
        approvalType = int(params["approval_type"])

        approval = "Y"
        curApproval = "N"

        updateApproval = {
            "cons_code": params["cons_code"],
            "sys_doc_num": params["sys_doc_num"],
            "id": loginUserInfo["id"],
            "approval": approval,
            "cur_approval": curApproval,
            "approval_date": util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
        }

        # 결재 정보를 업데이트 한다.
        resCd, msg, resData = servProjDocMana.documentApproval(updateApproval)
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

        # 결재자 리스트를 가져 온다.
        resCd, msg, resData = servProjDocMana.getDocApprovalInfo(
            params["cons_code"], params["sys_doc_num"]
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

        if approvalType == 0:  # 결재 승인
            approver = "Y"
            receiverCurType = "Y"
            receiverInfoList = []
            for data in resData:
                if data["approval_type"] == constants.APPRO_TYPE_CD_APPROVER:
                    if data["approval"] == "N":
                        approver = "N"
                        receiverCurType = "N"
                        break

                elif data["approval_type"] == constants.APPRO_TYPE_CD_RECEIVER:
                    receiverInfoList.append(data)

            for data in resData:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "loginUserId : "
                    + loginUserInfo["id"]
                    + ", dataId : "
                    + data["id"]
                    + ", approver : "
                    + approver
                    + ", receiverCurType : "
                    + receiverCurType,
                )

                if (
                    loginUserInfo["id"] == data["id"]
                    and approver == "Y"
                    and data["approval_type"] == constants.APPRO_TYPE_CD_APPROVER
                ):
                    if receiverCurType == "Y":
                        for receiverInfo in receiverInfoList:

                            updateApproval = {
                                "cons_code": params["cons_code"],
                                "sys_doc_num": params["sys_doc_num"],
                                "id": receiverInfo["id"],
                                "approval": "N",
                                "cur_approval": "Y",
                                "approval_date": ""
                                #'approval_date' : util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14)
                            }

                            # 결재 정보를 업데이트 한다.
                            resCd, msg, resDataTmp = servProjDocMana.documentApproval(
                                updateApproval
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
                    break

            lastType = True
            for data in resData:
                if (
                    data["approval_type"] == constants.APPRO_TYPE_CD_APPROVER
                    or data["approval_type"] == constants.APPRO_TYPE_CD_RECEIVER
                ):
                    if data["approval"] == "N":
                        lastType = False
                        break

            # lastType = True

            # for data in resData:
            # 	if(data['approval'] == 'N' and data['cur_approval'] == 'N'):
            # 		lastType = False
            # 		updateApproval = {
            # 			'cons_code' : params['cons_code'],
            # 			'sys_doc_num' : params['sys_doc_num'],
            # 			'id' : data['id'],
            # 			'approval' : 'N',
            # 			'cur_approval' : 'Y',
            # 			'approval_date' : ''
            # 		}
            # 		# 현재 결재자 정보를 업데이트 한다.
            # 		resCd, msg, resData = servProjDocMana.documentApproval(updateApproval)
            # 		# Error 발생 시 에러 코드 리턴
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
            #
            # 			return result
            # 		break;

            if lastType == False:
                stateCode = constants.APPRO_STATUS_CD_PROCEEDING

            else:
                stateCode = constants.APPRO_STATUS_CD_COMPLETION

        elif approvalType == 1:  # 반려
            stateCode = constants.APPRO_STATUS_CD_COMPANION
        elif approvalType == 2:  # 철회
            # approval = 'N'
            # curApproval = 'N'

            # updateFlag = 'N'
            # for index in range(0, len(resData)):
            # 	if(updateFlag == 'Y'):
            # 		updateApproval = {
            # 			'cons_code' : params['cons_code'],
            # 			'sys_doc_num' : params['sys_doc_num'],
            # 			'id' : resData[index]['id'],
            # 			'approval' : approval,
            # 			'cur_approval' : curApproval,
            # 			'approval_date' : ''
            # 		}
            #
            # 		servProjDocMana.documentApproval(updateApproval)

            # 	if(resData[index]['id'] == loginUserInfo['id']):
            # 		updateFlag = 'Y'

            stateCode = constants.APPRO_STATUS_CD_WITHDRAW

        if stateCode == constants.APPRO_STATUS_CD_PROCEEDING:
            pcDate = ""
        else:
            pcDate = util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14)

            #################################### 문서 결재 상태를 업데이트 한다. ####################################
        updateDocument = {
            "cons_code": params["cons_code"],
            "sys_doc_num": params["sys_doc_num"],
            "state_code": stateCode,
            "pc_date": pcDate,
        }

        resCd, msg, resData = servProjDocMana.updateDocApprovalState(updateDocument)
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

        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)
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


# 문서 결재 요청(문서 등록)
@projectDocManageApi.route("/reqDocApproval", methods=["PUT"])
def reqDocApproval():

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
            "---------- 문서 결재 요청 처리 시작 ----------",
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

        # 결재중이나 결재 완료된 문서 중 데이터 입력이 필요한 문서에 대해 처리 한다.
        if (params["reqDocInfo"]["doc_code"] == constants.SD_DOC_CORRECTIONORDER) and (
            int(params["reqDocContent"]["type"]) != 1
        ):  # 시정지시서
            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                (jobResData["job_title_code"] == constants.JOB_TITLE_CD_CONTRACTOR)
                or (
                    jobResData["job_title_code"]
                    == constants.JOB_TITLE_CD_CONTRACTION_MAIN
                )
                or (
                    jobResData["job_title_code"]
                    == constants.JOB_TITLE_CD_CONTRACTION_SUB
                )
                or (
                    jobResData["job_title_code"]
                    == constants.JOB_TITLE_CD_SUPERVISING_MAIN
                )
                or (
                    jobResData["job_title_code"]
                    == constants.JOB_TITLE_CD_SUPERVISING_SUB
                )
            ):

                resCd, msg, uDataInfo = procDocCorrectionOrder(
                    params, None, jobResData, loginUserInfo, request
                )
                if resCd != 0:
                    result = commServ.makeReturnMessage(resCd, msg, None)
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Response : " + commUtilServ.jsonDumps(result),
                    )

                    return result

                resCd, msg, resData = servProjDocMana.modifyDocumentInfo(uDataInfo)
                if resCd != 0:
                    result = commServ.makeReturnMessage(resCd, msg, None)
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Response : " + commUtilServ.jsonDumps(result),
                    )

                    return result

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_ZERO, "", None
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
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서를 업데이트 할 수 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

                #################################### 작성자가 작성 할 수 있는 문서가 맞는지 확인 한다. ####################################
        resCd, msg, resData = servProjDocMana.getDocumentInfo(
            params["reqDocInfo"]["cons_code"],
            params["reqDocInfo"]["doc_code"],
            loginUserInfo["co_code"],
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

        if resData == None:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "작성 할 수 있는 문서가 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        # 시스템 문서 번호를 가져 온다.
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

        # 시스템 문서 번호를 증가 한다.
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

        # 문서 번호를 가져 온다.
        resCd, msg, docNumResData = servProjDocMana.getDocumentNumInfo(
            params["reqDocInfo"]["cons_code"],
            params["reqDocInfo"]["doc_code"],
            loginUserInfo["co_code"],
        )
        # Error 발생 시 에러 코드 리턴
        if resCd != 0:
            servCommMana.decreaseSysDocNum()  # 시스템 문서 번호를 감소 한다.
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

        if resData == None:
            servCommMana.decreaseSysDocNum()  # 시스템 문서 번호를 감소 한다.
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "문서 번호를 만들 수 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        # 분서 번호를 증가 시키고 DB에 반영 한다.
        docNum = docNumResData["doc_num"] + 1
        resCd, msg, resData = servProjDocMana.modifyDocumentNumInfo(
            params["reqDocInfo"]["cons_code"],
            params["reqDocInfo"]["doc_code"],
            loginUserInfo["co_code"],
            docNum,
        )
        # Error 발생 시 에러 코드 리턴
        if resCd != 0:
            servCommMana.decreaseSysDocNum()  # 시스템 문서 번호를 감소 한다.

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

        # 문서 기본 정보를 생성 한다.
        docDefaultInfo = servProjDocMana.createDocDefaultInfo(
            loginUserInfo,
            docNumResData["abb"] + str(docNumResData["doc_num"]),
            sysDocNum,
        )

        if (
            params["reqDocInfo"]["doc_code"] == constants.CD_DOC_MATSELAPPREQ
        ):  # 자재 선정 승인 요청

            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                (jobResData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTOR)
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_MAIN
                )
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_SUB
                )
            ):

                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

            resCd, msg, params = procDocMatSelAppReq(
                params,
                loginUserInfo,
                request,
                docDefaultInfo["documentNumber"],
                docDefaultInfo["sysDocNum"],
            )
            if resCd != 0:
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

        elif (
            params["reqDocInfo"]["doc_code"] == constants.SD_DOC_MATSELAPPRES
        ):  # 자재 선정 승인 통보
            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN
            ) and (
                jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_SUB
            ):
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

            resCd, msg, params = procDocMatSelAppRes(
                params, docDefaultInfo["sysDocNum"]
            )
            if resCd != 0:
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

        elif (
            params["reqDocInfo"]["doc_code"] == constants.SD_DOC_FACTORYVISIT
        ):  # 공장방문검사결과
            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN
            ) and (
                jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_SUB
            ):
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

            resCd, msg, params = procDocFactoryVisit(docDefaultInfo, params, request)
            if resCd != 0:
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

        elif (
            params["reqDocInfo"]["doc_code"] == constants.CD_DOC_MATSELINSPECTIONREQ
        ):  # 자재 검수 요청

            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                (jobResData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTOR)
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_MAIN
                )
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_SUB
                )
            ):

                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

            resCd, msg, params = procDocMatSelInspReq(
                params, docDefaultInfo, loginUserInfo, request
            )
            if resCd != 0:
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

        elif (
            params["reqDocInfo"]["doc_code"] == constants.SD_DOC_MATSELINSPECTIONRES
        ):  # 자재 검수 통보
            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN
            ) and (
                jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_SUB
            ):
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

            resCd, msg, params = procDocMatSelInspRes(params, docDefaultInfo)
            if resCd != 0:
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

        elif params["reqDocInfo"]["doc_code"] == constants.CD_DOC_DETECTIONREQ:  # 검측 요청

            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                (jobResData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTOR)
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_MAIN
                )
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_SUB
                )
            ):

                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

            resCd, msg, params = procDocDetection(
                params, docDefaultInfo, loginUserInfo, request, 1
            )
            if resCd != 0:
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result
        elif params["reqDocInfo"]["doc_code"] == constants.SD_DOC_DETECTIONRES:  # 검측 통보
            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN
            ) and (
                jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_SUB
            ):
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

            resCd, msg, params = procDocDetection(
                params, docDefaultInfo, loginUserInfo, request, 2
            )
            if resCd != 0:
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

        elif (
            params["reqDocInfo"]["doc_code"] == constants.SD_DOC_CORRECTIONORDER
        ):  # 시정지시서
            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN
            ) and (
                jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_SUB
            ):
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

            resCd, msg, params = procDocCorrectionOrder(
                params, docDefaultInfo, jobResData, loginUserInfo, request
            )
            if resCd != 0:
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

        elif params["reqDocInfo"]["doc_code"] == constants.CD_DOC_WORKLOG:  # 작업일지

            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                (jobResData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTOR)
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_MAIN
                )
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_SUB
                )
            ):

                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

            resCd, msg, params = procDocWorkLog(params, docDefaultInfo, loginUserInfo)
            if resCd != 0:
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

        ################################# 조현우 시공상세도 및 설계도면 검토 관련 logic 추가 ###################################################################
        elif (
            params["reqDocInfo"]["doc_code"] == constants.CD_DOC_CONSTRDETAILREQ
        ):  # 시공상세도 검토 요청서 - 시공사 작성

            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                (jobResData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTOR)
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_MAIN
                )
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_SUB
                )
            ):

                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

            resCd, msg, params["reqDocContent"] = ConstrDetailReq(
                params["reqDocContent"], params["reqDocInfo"], docDefaultInfo, request
            ).get_result()
            if resCd != 0:
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

        elif (
            params["reqDocInfo"]["doc_code"] == constants.SD_DOC_CONSTRDETAILNTC
        ):  # 시공상세도 검토 통보서 - 감리원 작성

            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                (jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISOR)
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_SUPERVISING_MAIN
                )
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_SUPERVISING_SUB
                )
            ):

                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result
            resCd, msg, params["reqDocContent"] = ConstrDetailNtc(
                params["reqDocContent"], params["reqDocInfo"]
            ).get_result()

            if resCd != 0:
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

        elif (
            params["reqDocInfo"]["doc_code"] == constants.SD_DOC_PLANREVIEWRPT
        ):  # 설계검토 보고서 - 감리원 작성

            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                (jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISOR)
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_SUPERVISING_MAIN
                )
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_SUPERVISING_SUB
                )
            ):

                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result
            resCd, msg, params["reqDocContent"] = PlanReviewRPT(
                params["reqDocContent"], params["reqDocInfo"]
            ).get_result()

            if resCd != 0:
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result
        elif (
            params["reqDocInfo"]["doc_code"] == constants.CD_DOC_ONSITESITUATIONRPT
        ):  # 현장실정 보고서 - 시공사 작성

            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                (jobResData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTOR)
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_MAIN
                )
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_CONTRACTION_SUB
                )
            ):

                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result

            resCd, msg, params["reqDocContent"] = OnSiteSituationRPT(
                params["reqDocContent"], params["reqDocInfo"]
            ).get_result()
            if resCd != 0:
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result
        elif (
            params["reqDocInfo"]["doc_code"] == constants.SD_DOC_CONSTRCHANGEREVIEW
        ):  # 설계변경검토 의견서 - 감리원 작성

            #################################### 작성자 권한을 확인 한다. ####################################
            if (
                (jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISOR)
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_SUPERVISING_MAIN
                )
                and (
                    jobResData["job_title_code"]
                    != constants.JOB_TITLE_CD_SUPERVISING_SUB
                )
            ):

                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "문서 작성 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result
            resCd, msg, params["reqDocContent"] = ConstrChangeReview(
                params["reqDocContent"], params["reqDocInfo"]
            ).get_result()

            if resCd != 0:
                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

                result = commServ.makeReturnMessage(resCd, msg, None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )

                return result
        ################################# 조현우 시공상세도 및 설계도면 검토 관련 logic 추가 end ###################################################################
        # 문서 정보를 저장 한다.
        resCd, msg, resData = servProjDocMana.putDocumentInfo(docDefaultInfo, params)
        # Error 발생 시 에러 코드 리턴
        if resCd != 0:
            docNum = docNum - 1
            servProjDocMana.modifyDocumentNumInfo(
                params["reqDocInfo"]["cons_code"],
                params["reqDocInfo"]["doc_code"],
                loginUserInfo["co_code"],
                docNum,
            )  # 문서 번호를 감소 한다.

            # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

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

        resCd, msg, resData = servProjDocMana.putDocumentApprovalInfo(
            params,
            docDefaultInfo["documentNumber"],
            docDefaultInfo["sysDocNum"],
            docDefaultInfo["approvalDate"],
        )
        # Error 발생 시 에러 코드 리턴
        if resCd != 0:
            servProjDocMana.delDocumentInfo(
                docDefaultInfo["sysDocNum"]
            )  # 문서 정보를 삭제 한다.

            docNum = docNum - 1
            servProjDocMana.modifyDocumentNumInfo(
                params["reqDocInfo"]["cons_code"],
                params["reqDocInfo"]["doc_code"],
                loginUserInfo["co_code"],
                docNum,
            )  # 문서 번호를 감소 한다.

            # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

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

        # 연결된 문서를 저장 한다.
        linkSysDocNumList = params["reqDocLinkInfoList"]

        if len(linkSysDocNumList) > 0:
            resCd, msg, resData = servProjDocMana.putLinkDocInfo(
                params["reqDocInfo"]["cons_code"],
                docDefaultInfo["sysDocNum"],
                linkSysDocNumList,
            )
            # Error 발생 시 에러 코드 리턴
            if resCd != 0:
                servProjDocMana.delLinkDocInfo(
                    params["reqDocInfo"]["cons_code"],
                    docDefaultInfo["sysDocNum"],
                    linkSysDocNumList,
                )
                servProjDocMana.delDocumentApprovalInfo(docDefaultInfo["sysDocNum"])
                servProjDocMana.delDocumentInfo(
                    docDefaultInfo["sysDocNum"]
                )  # 문서 정보를 삭제 한다.

                docNum = docNum - 1
                servProjDocMana.modifyDocumentNumInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocInfo"]["doc_code"],
                    loginUserInfo["co_code"],
                    docNum,
                )  # 문서 번호를 감소 한다.

                # servCommMana.decreaseSysDocNum()	# 시스템 문서 번호를 감소 한다.

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

        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)
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


# 자재 선정 승인 요청에 대한 데이터 처리 Function
def procDocMatSelAppReq(params, userInfo, req, docNum, sysDocNum):
    servProjApproMaterMana = servProjectApproMaterManage()
    servProjUseMatMana = servProjectUseMaterialManage()
    commServ = commonService()
    # 자재 관리
    # 신규 자재를 등록 한다.(수동 등록되는 자재 처리)
    materialInfoList = params["reqDocContent"]["materialInfoList"]
    index = 0

    for materialInfo in materialInfoList:
        searchInfo = []

        # 자재 번호가 없으면 자재명, 제조사, KS 여부로 자재를 조회 한다.
        if materialInfo["material_num"] == "":
            searchData = {
                "column": "MATERIAL_NAME",
                "type": "string",
                "data": materialInfo["material_name"],
            }
            searchInfo.append(searchData)

            searchData = {
                "column": "PRODUCE_CO",
                "type": "string",
                "data": materialInfo["produce_co"],
            }

            searchData = {
                "column": "KS_WHETHER",
                "type": "string",
                "data": materialInfo["ks_whether"],
            }

            searchInfo.append(searchData)

        else:  # 자재 번호가 있으면 자재 번호로 자재를 조회 한다.
            searchData = {
                "column": "MATERIAL_NUM",
                "type": "int",
                "data": materialInfo["material_num"],
            }
            searchInfo.append(searchData)

        # 기존에 자재가 있는지 확인 한다.
        resCd, msg, resMaterialData = servProjApproMaterMana.getManualInputMaterialInfo(
            searchInfo
        )
        # Error 발생 시 에러 코드 리턴
        if resCd != 0:
            return resCd, msg, resMaterialData

        if resMaterialData == None:
            # 자재가 없는 경우 기본 정보 먼저 저장 한다.
            resCd, msg, resData = servProjApproMaterMana.putManualInputMaterialInfo(
                params["reqDocContent"]["materialInfoList"][index]
            )
            # Error 발생 시 에러 코드 리턴
            if resCd != 0:
                return resCd, msg, resData

            # 저장된 정보를 조회 한다.
            (
                resCd,
                msg,
                resMaterialData,
            ) = servProjApproMaterMana.getManualInputMaterialInfo(searchInfo)
            # Error 발생 시 에러 코드 리턴
            if resCd != 0:
                return resCd, msg, resMaterialData

        params["reqDocContent"]["materialInfoList"][index][
            "material_num"
        ] = resMaterialData["material_num"]
        params["reqDocContent"]["materialInfoList"][
            index
        ] = servProjApproMaterMana.materialFileManage(
            params["reqDocContent"]["materialInfoList"][index],
            resMaterialData,
            req,
            index,
        )

        # 수동 입력되는 자재 정보를 업데이트 한다.
        resCd, msg, resData = servProjApproMaterMana.modifyManualInputMaterialInfo(
            params["reqDocContent"]["materialInfoList"][index]
        )
        # Error 발생 시 에러 코드 리턴
        if resCd != 0:
            return resCd, msg, resData

        resCd, msg, resData = servProjUseMatMana.putUseMaterialInfo(
            params["reqDocInfo"]["cons_code"],
            docNum,
            userInfo["co_code"],
            params["reqDocContent"]["constr_type_cd"],
            params["reqDocContent"]["materialInfoList"][index]["material_num"],
            sysDocNum,
        )

        # Error 발생 시 에러 코드 리턴
        if resCd != 0:
            servProjUseMatMana.delUseMaterialInfo(sysDocNum)
            return resCd, msg, resData

        index += 1

    return constants.REST_RESPONSE_CODE_ZERO, "", params


# 자재 선정 승인 통보에 대한 데이터 처리 Function
def procDocMatSelAppRes(params, sysDocNum):
    servProjUseMatMana = servProjectUseMaterialManage()

    approvalInfoList = params["reqDocContent"]["approvalInfoList"]
    for approvalInfo in approvalInfoList:
        resCd, msg, resData = servProjUseMatMana.modifyUseMaterialInfo(
            params["reqDocInfo"]["cons_code"],
            params["reqDocContent"]["req_sys_doc_num"],
            params["reqDocContent"]["constr_type_cd"],
            approvalInfo,
            sysDocNum,
        )

        # Error 발생 시 에러 코드 리턴
        if resCd != 0:
            for removeInfo in approvalInfoList:
                removeInfo["review_opinion"] = ""
                removeInfo["judgment"] = ""
                removeInfo["uniqueness"] = ""

                servProjUseMatMana.modifyUseMaterialInfo(
                    params["reqDocInfo"]["cons_code"],
                    params["reqDocContent"]["req_sys_doc_num"],
                    params["reqDocContent"]["constr_type_cd"],
                    removeInfo,
                    sysDocNum,
                )

            return resCd, msg, resData

    return constants.REST_RESPONSE_CODE_ZERO, "", params


# 공장 방문 결과 보고서 데이터 처리 Function
def procDocFactoryVisit(docDefaultInfo, params, req):
    servCommMana = servCommManage()
    servProjDocMana = servProjectDocManage()
    servProjUseMatMana = servProjectUseMaterialManage()
    servProjApproMaterMana = servProjectApproMaterManage()

    resCd, msg, resData = servProjUseMatMana.putFactoryVisitResult(
        docDefaultInfo, params
    )
    # Error 발생 시 에러 코드 리턴
    if resCd != 0:
        return resCd, msg, resData

    resCd, msg, resData = servCommMana.getCodeName(
        params["reqDocContent"]["constr_type_cd"]
    )
    # Error 발생 시 에러 코드 리턴
    if resCd != 0:
        return resCd, msg, resData

    resCd, msg, materialInfo = servProjApproMaterMana.getDetailApproMater(
        params["reqDocContent"]["material_num"]
    )

    factVisitData = {
        "constr_type_cd": params["reqDocContent"]["constr_type_cd"],
        "constr_type_name": resData["subcode_name"],
        "material_num": params["reqDocContent"]["material_num"],
        "material_name": materialInfo["material_name"],
        "facility_name": params["reqDocContent"]["facility_name"],
        "co_name": params["reqDocContent"]["co_name"],
        "factory_name": params["reqDocContent"]["factory_name"],
        "place": params["reqDocContent"]["place"],
        "visit_date": params["reqDocContent"]["visit_date"],
        "inspection_key_content": params["reqDocContent"]["inspection_key_content"],
        "specialties": params["reqDocContent"]["specialties"],
        "inspector": params["reqDocContent"]["inspector"],
        "inspector_id": params["reqDocContent"]["inspector_id"],
        "checker": params["reqDocContent"]["checker"],
        "checker_id": params["reqDocContent"]["checker_id"],
        "inspection_picture_list": [],
        "perf_test_measure_result_list": [],
    }

    if len(params["reqDocContent"]["inspection_picture_list"]) > 0:
        # factVisitData['inspection_picture_list'] = servProjDocMana.docFileManage(params['reqDocInfo']['cons_code'],
        resCd, msg, resData = servProjDocMana.docFileManage(
            params["reqDocInfo"]["cons_code"],
            docDefaultInfo["sysDocNum"],
            params["reqDocInfo"]["doc_code"],
            docDefaultInfo["documentNumber"],
            "inspection_picture",
            params["reqDocContent"]["inspection_picture_list"],
            req,
        )

        if resCd != 0:
            servProjDocMana.removeDocFileManage(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjUseMatMana.delFactoryVisitResult(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, resData

        factVisitData["inspection_picture_list"] = resData

    if len(params["reqDocContent"]["perf_test_measure_result_list"]) > 0:
        # factVisitData['perf_test_measure_result_list'] = servProjDocMana.docFileManage(params['reqDocInfo']['cons_code'],
        resCd, msg, resData = servProjDocMana.docFileManage(
            params["reqDocInfo"]["cons_code"],
            docDefaultInfo["sysDocNum"],
            params["reqDocInfo"]["doc_code"],
            docDefaultInfo["documentNumber"],
            "perf_test_measure_result",
            params["reqDocContent"]["perf_test_measure_result_list"],
            req,
        )

        if resCd != 0:
            servProjDocMana.removeDocFileManage(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjUseMatMana.delFactoryVisitResult(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, resData

        factVisitData["perf_test_measure_result_list"] = resData

    params["reqDocContent"] = factVisitData

    return constants.REST_RESPONSE_CODE_ZERO, "", params


# 자재 검수 승인 요청에 대한 데이터 처리 Function
def procDocMatSelInspReq(params, docDefaultInfo, userInfo, req):
    servProjInspMaterMana = servProjectInspMaterManage()
    servProjDocMana = servProjectDocManage()
    servProjUseMatMana = servProjectUseMaterialManage()

    materInspData = {
        "material_list": params["reqDocContent"]["material_list"],
        "trading_statement_list": [],
        "photo_board_list": [],
    }

    if len(params["reqDocContent"]["trading_statement_list"]) > 0:
        # factVisitData['inspection_picture_list'] = servProjDocMana.docFileManage(params['reqDocInfo']['cons_code'],
        resCd, msg, resData = servProjDocMana.docFileManage(
            params["reqDocInfo"]["cons_code"],
            docDefaultInfo["sysDocNum"],
            params["reqDocInfo"]["doc_code"],
            docDefaultInfo["documentNumber"],
            "trading_statement",
            params["reqDocContent"]["trading_statement_list"],
            req,
        )

        if resCd != 0:
            servProjDocMana.removeDocFileManage(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjUseMatMana.delFactoryVisitResult(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, resData

        materInspData["trading_statement_list"] = resData

    if len(params["reqDocContent"]["photo_board_list"]) > 0:
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "------------------------------------------- 0 ",
        )

        oldPhotoBoardList = params["reqDocContent"]["photo_board_list"]

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "------------------------------------------- 1 ",
        )
        # factVisitData['inspection_picture_list'] = servProjDocMana.docFileManage(params['reqDocInfo']['cons_code'],
        resCd, msg, resData = servProjDocMana.docFileManage(
            params["reqDocInfo"]["cons_code"],
            docDefaultInfo["sysDocNum"],
            params["reqDocInfo"]["doc_code"],
            docDefaultInfo["documentNumber"],
            "photo_board",
            params["reqDocContent"]["photo_board_list"],
            req,
        )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "------------------------------------------- 2 ",
        )
        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "------------------------------------------- 3 ",
            )
            servProjDocMana.removeDocFileManage(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "------------------------------------------- 4 ",
            )
            servProjUseMatMana.delFactoryVisitResult(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "------------------------------------------- 5 ",
            )
            return resCd, msg, resData

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "------------------------------------------- 6 ",
        )
        materInspData["photo_board_list"] = resData
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "------------------------------------------- 7 ",
        )

        index = 0
        for oldPhotoBoard in oldPhotoBoardList:
            materInspData["photo_board_list"][index]["content"] = oldPhotoBoard[
                "content"
            ]
            materInspData["photo_board_list"][index]["date"] = oldPhotoBoard["date"]
            index += 1

    logs.war(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "------------------------------------------- 9 ",
    )
    params["reqDocContent"] = materInspData

    logs.war(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "------------------------------------------- 10 ",
    )
    resCd, msg, resData = servProjInspMaterMana.putInspMaterInfo(
        params, docDefaultInfo, userInfo["co_code"]
    )
    logs.war(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "------------------------------------------- 11 ",
    )
    if resCd != 0:
        servProjDocMana.removeDocFileManage(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjUseMatMana.delFactoryVisitResult(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        return resCd, msg, params

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "------------------------------------------- 12 ",
        )

    return constants.REST_RESPONSE_CODE_ZERO, "", params


# 자재 검수 승인 통보에 대한 데이터 처리 Function
def procDocMatSelInspRes(params, docDefaultInfo):
    servProjInspMaterMana = servProjectInspMaterManage()

    resCd, msg, resData = servProjInspMaterMana.modifyInspMaterInfo(
        params, docDefaultInfo
    )
    if resCd != 0:
        return resCd, msg, params

    return constants.REST_RESPONSE_CODE_ZERO, "", params


# 검측 데이터 처리 Function
def procDocDetection(params, docDefaultInfo, userInfo, req, type):
    servCommMana = servCommManage()
    servUserMana = servUserManage()
    commServ = commonService()
    commUtilServ = commUtilService()
    servProjDocMana = servProjectDocManage()
    servProjDeteMana = servProjectDetectionManage()

    if type == 1:  # 검측 요청
        resCd, msg, constrTypeCdData = servCommMana.getCodeName(
            params["reqDocContent"]["constr_type_cd"]
        )
        # Error 발생 시 에러 코드 리턴
        if resCd != 0:
            return resCd, msg, constrTypeCdData

        resCd, msg, detailConstrTypeCdData = servCommMana.getCodeName(
            params["reqDocContent"]["detail_constr_type_cd"]
        )
        # Error 발생 시 에러 코드 리턴
        if resCd != 0:
            return resCd, msg, detailConstrTypeCdData

        # 사용자 정보를 가져 온다.
        resCd, msg, userInfo1 = servUserMana.getUserInfo(
            1, params["reqDocContent"]["cont_1st_id"], None
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

        if userInfo1 == None:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        user1stName = userInfo1["user_name"]

        if params["reqDocContent"]["cont_2st_id"] != "":
            # 사용자 정보를 가져 온다.
            resCd, msg, userInfo2 = servUserMana.getUserInfo(
                1, params["reqDocContent"]["cont_2st_id"], None
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

            if userInfo1 == None:
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )
                return result

            user2stName = userInfo2["user_name"]
        else:
            user2stName = ""

        detectionTable = params["reqDocContent"]["detection_table"]
        detectionTableResult = []

        for detection in detectionTable:
            resCd, msg, resultData = servCommMana.getCodeName(detection["insp_crid_cd"])
            # Error 발생 시 에러 코드 리턴
            if resCd != 0:
                return resCd, msg, resultData

            detectionInfo = {
                "chk_msg": detection["chk_msg"],
                "insp_crid_cd": detection["insp_crid_cd"],
                "insp_crid_nm": resultData["subcode_name"],
                "cont_1st_result": detection["cont_1st_result"],
                "cont_2st_result": detection["cont_2st_result"],
            }

            detectionTableResult.append(detectionInfo)

        detectionData = {
            "constr_type_cd": params["reqDocContent"]["constr_type_cd"],
            "constr_type_name": constrTypeCdData["subcode_name"],
            "detail_constr_type_cd": params["reqDocContent"]["detail_constr_type_cd"],
            "detail_constr_type_name": detailConstrTypeCdData["subcode_name"],
            "location": params["reqDocContent"]["location"],
            "dete_req_date": params["reqDocContent"]["dete_req_date"],
            "dete_area": params["reqDocContent"]["dete_area"],
            "cont_1st_id": params["reqDocContent"]["cont_1st_id"],
            "cont_1st_name": user1stName,
            "cont_2st_id": params["reqDocContent"]["cont_2st_id"],
            "cont_2st_name": user2stName,
            "detection_table": detectionTableResult,
            "drawing_list": params["reqDocContent"]["drawing_list"],
        }

        if len(params["reqDocContent"]["cons_part_real_nm_book"]) > 0:
            resCd, msg, resData = servProjDocMana.docFileManage(
                params["reqDocInfo"]["cons_code"],
                docDefaultInfo["sysDocNum"],
                params["reqDocInfo"]["doc_code"],
                docDefaultInfo["documentNumber"],
                "cons_part_real_nm",
                params["reqDocContent"]["cons_part_real_nm_book"],
                req,
            )

            if resCd != 0:
                servProjDocMana.removeDocFileManage(
                    params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
                )
                # servProjUseMatMana.delFactoryVisitResult(params['reqDocInfo']['cons_code'],	docDefaultInfo['sysDocNum'])
                return resCd, msg, resData

            detectionData["cons_part_real_nm_book"] = resData

        if len(params["reqDocContent"]["photo_artboard_list"]) > 0:
            resCd, msg, resData = servProjDocMana.docFileManage(
                params["reqDocInfo"]["cons_code"],
                docDefaultInfo["sysDocNum"],
                params["reqDocInfo"]["doc_code"],
                docDefaultInfo["documentNumber"],
                "photo_artboard",
                params["reqDocContent"]["photo_artboard_list"],
                req,
            )

            if resCd != 0:
                servProjDocMana.removeDocFileManage(
                    params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
                )
                # servProjUseMatMana.delFactoryVisitResult(params['reqDocInfo']['cons_code'],	docDefaultInfo['sysDocNum'])
                return resCd, msg, resData

            detectionData["photo_artboard_list"] = resData

        params["reqDocContent"] = detectionData

    elif type == 2:  # 검측 통보
        # 사용자 정보를 가져 온다.
        resCd, msg, userInfo1 = servUserMana.getUserInfo(
            1, params["reqDocContent"]["supe_1st_id"], None
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

        if userInfo1 == None:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        user1stName = userInfo1["user_name"]

        if params["reqDocContent"]["supe_2st_id"] != "":
            # 사용자 정보를 가져 온다.
            resCd, msg, userInfo2 = servUserMana.getUserInfo(
                1, params["reqDocContent"]["supe_2st_id"], None
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

            if userInfo1 == None:
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )
                return result

            user2stName = userInfo2["user_name"]
        else:
            user2stName = ""

        detectionTable = params["reqDocContent"]["detection_table"]
        detectionTableResult = []

        for detection in detectionTable:
            resCd, msg, resultData = servCommMana.getCodeName(detection["insp_crid_cd"])
            # Error 발생 시 에러 코드 리턴
            if resCd != 0:
                return resCd, msg, resultData

            detectionInfo = {
                "chk_msg": detection["chk_msg"],
                "insp_crid_cd": detection["insp_crid_cd"],
                "insp_crid_nm": resultData["subcode_name"],
                "supe_1st_result": detection["supe_1st_result"],
                "supe_2st_result": detection["supe_2st_result"],
                "dete_action": detection["dete_action"],
            }

            detectionTableResult.append(detectionInfo)

        detectionData = {
            "dete_req_sys_doc_num": params["reqDocContent"]["dete_req_sys_doc_num"],
            "dete_date": params["reqDocContent"]["dete_date"],
            "dete_result": params["reqDocContent"]["dete_result"],
            "instruction": params["reqDocContent"]["instruction"],
            "supe_1st_id": params["reqDocContent"]["supe_1st_id"],
            "supe_1st_name": user1stName,
            "supe_2st_id": params["reqDocContent"]["supe_2st_id"],
            "supe_2st_name": user2stName,
            "detection_table": detectionTableResult,
        }

        params["reqDocContent"] = detectionData

    if type == 1:  # 검측 요청

        writerDate = util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14)

        resCd, msg, resultData = servProjDeteMana.putDeteChkList(
            params["reqDocInfo"]["cons_code"],
            docDefaultInfo["sysDocNum"],
            params["reqDocContent"]["detection_table"],
        )

        if resCd != 0:

            servProjDeteMana.delDeteChkList(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, resultData

        resCd, msg, resultData = servProjDeteMana.putDetectionInfo(
            params, docDefaultInfo, userInfo["co_code"], writerDate
        )

        if resCd != 0:

            servProjDeteMana.delDeteChkList(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, resultData

    elif type == 2:  # 검측 통보

        resCd, msg, resultData = servProjDeteMana.modifyDeteChkList(
            params["reqDocInfo"]["cons_code"],
            params["reqDocContent"]["dete_req_sys_doc_num"],
            params["reqDocContent"]["detection_table"],
        )
        if resCd != 0:

            index = 0
            detectionTableLen = len(params["reqDocContent"]["detection_table"])

            while index < detectionTableLen:
                if (
                    params["reqDocContent"]["detection_table"][index]["supe_2st_result"]
                    != ""
                ):
                    params["reqDocContent"]["detection_table"][index][
                        "supe_2st_result"
                    ] = ""
                else:
                    params["reqDocContent"]["detection_table"][index][
                        "supe_1st_result"
                    ] = ""
                    params["reqDocContent"]["detection_table"][index][
                        "supe_2st_result"
                    ] = ""

                index += 1

            servProjDeteMana.modifyDeteChkList(
                params["reqDocInfo"]["cons_code"],
                params["reqDocContent"]["dete_req_sys_doc_num"],
                params["reqDocContent"]["detection_table"],
            )
            return resCd, msg, resultData

        resCd, msg, resultData = servProjDeteMana.modifyDetectionInfo(
            params, docDefaultInfo
        )
        if resCd != 0:
            index = 0
            detectionTableLen = len(params["reqDocContent"]["detection_table"])

            while index < detectionTableLen:
                if (
                    params["reqDocContent"]["detection_table"][index]["supe_2st_result"]
                    != ""
                ):
                    params["reqDocContent"]["detection_table"][index][
                        "supe_2st_result"
                    ] = ""
                else:
                    params["reqDocContent"]["detection_table"][index][
                        "supe_1st_result"
                    ] = ""
                    params["reqDocContent"]["detection_table"][index][
                        "supe_2st_result"
                    ] = ""

                index += 1

            servProjDeteMana.modifyDeteChkList(
                params["reqDocInfo"]["cons_code"],
                params["reqDocContent"]["dete_req_sys_doc_num"],
                params["reqDocContent"]["detection_table"],
            )
            return resCd, msg, resultData

    return constants.REST_RESPONSE_CODE_ZERO, "", params


# 시정 지시서 데이터 처리 Function
def procDocCorrectionOrder(params, docDefaultInfo, jobAuth, userInfo, req):
    servCommMana = servCommManage()
    servUserMana = servUserManage()
    commServ = commonService()
    commUtilServ = commUtilService()
    servProjDocMana = servProjectDocManage()
    servProjDeteMana = servProjectDetectionManage()

    type = int(params["reqDocContent"]["type"])

    if type == 1:  # 시정 지시서 최초 등록
        corrOrderData = {
            "constr_type_cd": params["reqDocContent"]["constr_type_cd"],
            "write_date": params["reqDocContent"]["write_date"],
            "title": params["reqDocContent"]["title"],
            "content": params["reqDocContent"]["content"],
        }

        resCd, msg, constrTypeCdData = servCommMana.getCodeName(
            params["reqDocContent"]["constr_type_cd"]
        )
        # Error 발생 시 에러 코드 리턴
        if resCd != 0:
            return resCd, msg, None

        corrOrderData["constr_type_name"] = constrTypeCdData["subcode_name"]

        if len(params["reqDocContent"]["correction_area_photo_list"]) > 0:
            resCd, msg, resData = servProjDocMana.docFileManage(
                params["reqDocInfo"]["cons_code"],
                docDefaultInfo["sysDocNum"],
                params["reqDocInfo"]["doc_code"],
                docDefaultInfo["documentNumber"],
                "correction_area_photo",
                params["reqDocContent"]["correction_area_photo_list"],
                req,
            )

            if resCd != 0:
                servProjDocMana.removeDocFileManage(
                    params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
                )
                # servProjUseMatMana.delFactoryVisitResult(params['reqDocInfo']['cons_code'],	docDefaultInfo['sysDocNum'])
                return resCd, msg, resData

            corrOrderData["correction_area_photo_list"] = resData

        params["reqDocContent"] = corrOrderData

    else:
        sysDocNum = str(params["reqDocContent"]["correction_order_sys_doc_num"])
        #################################### 문서 상세 정보를 조회 한다. ####################################
        resCd, msg, resDocInfo = servProjDocMana.getDocDetailInfo(
            userInfo["id"],
            userInfo["authority_code"],
            jobAuth,
            params["reqDocInfo"]["cons_code"],
            sysDocNum,
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

        if resDocInfo == None:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + commUtilServ.jsonDumps(msg),
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "문서 정보가 존재하지 않거나 조회 할 수 없는 문서 입니다.",
                None,
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        resDocInfo["content"] = json.loads(resDocInfo["content"])

        if type == 2:

            if len(params["reqDocContent"]["correction_check_doc_list"]) > 0:
                resCd, msg, resData = servProjDocMana.docFileManage(
                    resDocInfo["cons_code"],
                    str(resDocInfo["sys_doc_num"]),
                    resDocInfo["doc_code"],
                    resDocInfo["doc_num"],
                    "correction_check_doc",
                    params["reqDocContent"]["correction_check_doc_list"],
                    req,
                )

                if resCd != 0:
                    return resCd, msg, resData

                resDocInfo["content"]["correction_check_doc_list"] = resData

            if len(params["reqDocContent"]["correction_check_photo_list"]) > 0:
                resCd, msg, resData = servProjDocMana.docFileManage(
                    resDocInfo["cons_code"],
                    str(resDocInfo["sys_doc_num"]),
                    resDocInfo["doc_code"],
                    resDocInfo["doc_num"],
                    "correction_check_photo",
                    params["reqDocContent"]["correction_check_photo_list"],
                    req,
                )

                if resCd != 0:
                    return resCd, msg, resData

                for data in params["reqDocContent"]["correction_check_photo_list"]:

                    index = 0
                    for rData in resData:
                        if data["file_name_new"] == rData["file_original_name"]:
                            resData[index]["content"] = data["content"]
                            resData[index]["date"] = data["date"]
                            break

                        index += 1

                resDocInfo["content"]["correction_check_photo_list"] = resData

        elif type == 3:
            resDocInfo["content"]["correction_order_check_content"] = params[
                "reqDocContent"
            ]["correction_order_check_content"]

        params = resDocInfo

    return constants.REST_RESPONSE_CODE_ZERO, "", params


def getWorkLogBasicData(consCode, loginUserInfo):

    servProjWorkLogMana = servProjectWorkLogManage()
    servCommMana = servCommManage()

    occStatDataList = []

    # 직종 통계 정보를 가져 온다.
    resCd, msg, occStatDataList = servProjWorkLogMana.getOccStatList(
        consCode, loginUserInfo["co_code"]
    )

    if resCd != 0:
        return resCd, msg, None

    if occStatDataList == None or len(occStatDataList) < 1:
        occStatDataList = []
        resCd, msg, occDataList = servCommMana.getCodeList("OC00")
        if resCd != 0:
            return resCd, msg, None

        for occData in occDataList:
            occInfo = {
                "occ_code": occData["fullcode"],
                "occ_name": occData["subcode_name"],
                "prev_day_total": "0",
            }

            occStatDataList.append(occInfo)

    equStatDataList = []
    # 장비 통계 정보를 가져 온다.
    resCd, msg, equStatDataList = servProjWorkLogMana.getEquStatList(
        consCode, loginUserInfo["co_code"]
    )
    if resCd != 0:
        return resCd, msg, None

    if equStatDataList == None or len(equStatDataList) < 1:
        equStatDataList = []
        resCd, msg, equDataList = servCommMana.getCodeList("EQ00")
        if resCd != 0:
            return resCd, msg, None

        for equData in equDataList:
            equInfo = {
                "equip_code": equData["fullcode"],
                "equip_name": equData["subcode_name"],
                "prev_day_total": "0",
            }

            equStatDataList.append(equInfo)

    resCd, msg, workLoadStatDataList = servProjWorkLogMana.getWorkLoadStatList(
        consCode, loginUserInfo["co_code"]
    )
    if resCd != 0:
        return resCd, msg, None

    workLoadDataInfo = {
        "occStatInfo": occStatDataList,
        "equStatInfo": equStatDataList,
        "workLoadStatInfo": workLoadStatDataList,
    }

    return constants.REST_RESPONSE_CODE_ZERO, "", workLoadDataInfo


def procDocWorkLog(params, docDefaultInfo, loginUserInfo):
    commUtilServ = commUtilService()
    servProjMana = servProjectManage()
    servProjWorkLogMana = servProjectWorkLogManage()
    servCommMana = servCommManage()

    # 작성 기준 정보를 가져 온다.
    resCd, msg, resData = servProjMana.getWorkLogWriSta(
        params["reqDocInfo"]["cons_code"], docDefaultInfo["coCode"]
    )
    if resCd != 0:
        return resCd, msg, None

    if resData == None:
        return constants.REST_RESPONSE_CODE_DATAFAIL, "작업일지 작성 기준이 설정되어 있지 않습니다.", None

    errMsg = ""

    try:
        # 작업 일지 데이터 저장
        resCd, msg, resData = servProjWorkLogMana.putWorkLog(
            params, docDefaultInfo, resData["write_standard_code"]
        )
        if resCd != 0:
            return resCd, msg, None
    except KeyError as e:
        errMsg = str(e)
    except NameError as e:
        errMsg = str(e)
    except TypeError as e:
        errMsg = str(e)
    except AttributeError as e:
        errMsg = str(e)
    except Exception as e:
        errMsg = str(e)

    # 금일 작업 내용 데이터 저장
    workLogTodayList = params["reqDocContent"]["workLogTodayList"]

    for index in range(0, len(workLogTodayList)):

        commUtilServ = commUtilService()
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "workLogTodayList ------------------- : "
            + commUtilServ.jsonDumps(
                params["reqDocContent"]["workLogTodayList"][index]
            ),
        )

        resCd, msg, resData = servProjWorkLogMana.putWorkLogToday(
            params["reqDocInfo"]["cons_code"],
            params["reqDocContent"]["workLogTodayList"][index],
            docDefaultInfo,
            params["reqDocContent"]["workDate"],
        )

        if resCd != 0:
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, None

        resCd, msg, resData = servCommMana.getCodeName(
            params["reqDocContent"]["workLogTodayList"][index]["occ_code"]
        )
        if resCd != 0:
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, None

        params["reqDocContent"]["workLogTodayList"][index]["occ_name"] = resData[
            "subcode_name"
        ]

        resCd, msg, resData = servCommMana.getCodeName(
            params["reqDocContent"]["workLogTodayList"][index]["work_unit"]
        )
        if resCd != 0:
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, None

        params["reqDocContent"]["workLogTodayList"][index]["work_unit_name"] = resData[
            "subcode_name"
        ]

        resCd, msg, resData = servCommMana.getCodeName(
            params["reqDocContent"]["workLogTodayList"][index]["gr_ungr"]
        )
        if resCd != 0:
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, None

        params["reqDocContent"]["workLogTodayList"][index]["gr_ungr_nm"] = resData[
            "subcode_name"
        ]

        resCd, msg, resData = servCommMana.getCodeName(
            params["reqDocContent"]["workLogTodayList"][index]["constr_type_cd"]
        )
        if resCd != 0:
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, None

        params["reqDocContent"]["workLogTodayList"][index]["constr_type_nm"] = resData[
            "subcode_name"
        ]

        resCd, msg, resData = servCommMana.getCodeName(
            params["reqDocContent"]["workLogTodayList"][index]["detail_constr_type_cd"]
        )
        if resCd != 0:
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, None

        params["reqDocContent"]["workLogTodayList"][index][
            "detail_constr_type_nm"
        ] = resData["subcode_name"]

    # 직종 통계 데이터 저장
    # 직종 통계 정보를 가져 온다.
    occStatDataList = []
    resCd, msg, occStatDataList = servProjWorkLogMana.getOccStatList(
        params["reqDocInfo"]["cons_code"], docDefaultInfo["coCode"]
    )

    if resCd != 0:
        servProjWorkLogMana.delWorkLogDrawing(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogToday(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLog(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        return resCd, msg, None

    if occStatDataList == None or len(occStatDataList) < 1:
        occStatDataList = []
        resCd, msg, occDataList = servCommMana.getCodeList(
            "OC00"
        )  # 직종 통계 정보 없을 시 최초 통계 정보를 생성할 데이터를 가져 온다.
        if resCd != 0:
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )

            return resCd, msg, None

        for occData in occDataList:
            occInfo = {
                "cons_code": params["reqDocInfo"]["cons_code"],
                "sys_doc_num": docDefaultInfo["sysDocNum"],
                "work_date": params["reqDocContent"]["workDate"],
                "occ_code": occData["fullcode"],
                "occ_name": occData["subcode_name"],
                "prev_day_total": 0.0,
                "today_total": 0.0,
                "total_running": 0.0,
            }

            occStatDataList.append(occInfo)

    workLogTodayList = params["reqDocContent"]["workLogTodayList"]

    for index in range(0, len(occStatDataList)):
        occStatDataList[index]["cons_code"] = params["reqDocInfo"]["cons_code"]
        occStatDataList[index]["sys_doc_num"] = docDefaultInfo["sysDocNum"]
        occStatDataList[index]["work_date"] = params["reqDocContent"]["workDate"]

        for workLogToday in workLogTodayList:
            # 			logs.debug(procName, os.path.basename(__file__), sys._getframe(0).f_code.co_name, u'----------------------------------' + commUtilServ.jsonDumps(workLogToday))

            if occStatDataList[index]["occ_code"] == workLogToday["occ_code"]:
                # if(resData['write_standard_code'] == constants.WORK_LOG_WRITE_CD_YS):
                # elif(resData['write_standard_code'] == constants.WORK_LOG_WRITE_CD_TO):

                # occStatDataList[index]['cons_code'] = params['reqDocInfo']['cons_code']
                # occStatDataList[index]['sys_doc_num'] = docDefaultInfo['sysDocNum']
                # occStatDataList[index]['work_date'] = params['reqDocContent']['workDate']
                occStatDataList[index]["prev_day_total"] = occStatDataList[index][
                    "total_running"
                ]
                occStatDataList[index]["today_total"] = float(
                    workLogToday["today_work_load"]
                )
                occStatDataList[index]["total_running"] = float(
                    occStatDataList[index]["total_running"]
                ) + float(workLogToday["today_work_load"])

    # logs.debug(procName, os.path.basename(__file__), sys._getframe(0).f_code.co_name, u'----------------------------------0')
    # logs.debug(procName, os.path.basename(__file__), sys._getframe(0).f_code.co_name, u'----------------------------------1')
    # logs.debug(procName, os.path.basename(__file__), sys._getframe(0).f_code.co_name, u'----------------------------------2')
    # logs.debug(procName, os.path.basename(__file__), sys._getframe(0).f_code.co_name, u'----------------------------------3')
    # logs.debug(procName, os.path.basename(__file__), sys._getframe(0).f_code.co_name, u'----------------------------------4')
    for occStatData in occStatDataList:
        # 		logs.debug(procName, os.path.basename(__file__), sys._getframe(0).f_code.co_name, u'----------------------------------0 ' + commUtilServ.jsonDumps(occStatData))
        resCd, msg, resData = servProjWorkLogMana.putWorkLogTodayWorkerStatistics(
            occStatData, docDefaultInfo["coCode"]
        )
        # 		logs.debug(procName, os.path.basename(__file__), sys._getframe(0).f_code.co_name, u'----------------------------------1')
        if resCd != 0:
            servProjWorkLogMana.delWorkLogTodayWorkerStatistics(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )

            return resCd, msg, None

    params["reqDocContent"]["workLogTodayStatistics"] = occStatDataList

    # 금일 투입 장비 현황 데이터 저장
    todayInputEquipStatusList = params["reqDocContent"]["todayInputEquipStatusList"]

    for index in range(0, len(todayInputEquipStatusList)):
        resCd, msg, resData = servProjWorkLogMana.putWorkLogTodayInputEquipStatus(
            params["reqDocInfo"]["cons_code"],
            params["reqDocContent"]["todayInputEquipStatusList"][index],
            docDefaultInfo,
        )
        if resCd != 0:
            servProjWorkLogMana.delWorkLogTodayInputEquipStatus(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogTodayWorkerStatistics(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, None

        resCd, msg, resData = servCommMana.getCodeName(
            params["reqDocContent"]["todayInputEquipStatusList"][index][
                "constr_type_cd"
            ]
        )
        if resCd != 0:
            servProjWorkLogMana.delWorkLogTodayInputEquipStatus(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogTodayWorkerStatistics(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, None

        params["reqDocContent"]["todayInputEquipStatusList"][index][
            "constr_type_nm"
        ] = resData["subcode_name"]

        resCd, msg, resData = servCommMana.getCodeName(
            params["reqDocContent"]["todayInputEquipStatusList"][index][
                "detail_constr_type_cd"
            ]
        )
        if resCd != 0:
            servProjWorkLogMana.delWorkLogTodayInputEquipStatus(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogTodayWorkerStatistics(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, None

        params["reqDocContent"]["todayInputEquipStatusList"][index][
            "detail_constr_type_nm"
        ] = resData["subcode_name"]

        resCd, msg, resData = servCommMana.getCodeName(
            params["reqDocContent"]["todayInputEquipStatusList"][index]["equip_code"]
        )
        if resCd != 0:
            servProjWorkLogMana.delWorkLogTodayInputEquipStatus(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogTodayWorkerStatistics(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, None

        params["reqDocContent"]["todayInputEquipStatusList"][index][
            "equip_nm"
        ] = resData["subcode_name"]

        resCd, msg, resData = servCommMana.getCodeName(
            params["reqDocContent"]["todayInputEquipStatusList"][index]["input_unit"]
        )
        if resCd != 0:
            servProjWorkLogMana.delWorkLogTodayInputEquipStatus(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogTodayWorkerStatistics(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            return resCd, msg, None

        params["reqDocContent"]["todayInputEquipStatusList"][index][
            "input_unit_nm"
        ] = resData["subcode_name"]

    # 장비 통계 데이터 저장
    # 장비 통계 정보를 가져 온다.
    equipStatDataList = []
    resCd, msg, equipStatDataList = servProjWorkLogMana.getEquStatList(
        params["reqDocInfo"]["cons_code"], docDefaultInfo["coCode"]
    )
    if resCd != 0:
        servProjWorkLogMana.delWorkLogTodayInputEquipStatus(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogTodayWorkerStatistics(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogDrawing(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogToday(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLog(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        return resCd, msg, None

    if equipStatDataList == None or len(equipStatDataList) < 1:
        equipStatDataList = []
        resCd, msg, equipDataList = servCommMana.getCodeList(
            "EQ00"
        )  # 장비 통계 정보 없을 시 최초 통계 정보를 생성할 데이터를 가져 온다.
        if resCd != 0:
            servProjWorkLogMana.delWorkLogTodayInputEquipStatus(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogTodayWorkerStatistics(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )

            return resCd, msg, None

        for equipData in equipDataList:
            equipInfo = {
                "cons_code": params["reqDocInfo"]["cons_code"],
                "sys_doc_num": docDefaultInfo["sysDocNum"],
                "equip_code": equipData["fullcode"],
                "equip_name": equipData["subcode_name"],
                "input_date": params["reqDocContent"]["workDate"],
                "prev_day_total": 0.0,
                "today_total": 0.0,
                "total_running": 0.0,
            }

            equipStatDataList.append(equipInfo)

    todayInputEquipStatusList = params["reqDocContent"]["todayInputEquipStatusList"]

    for index in range(0, len(equipStatDataList)):
        equipStatDataList[index]["cons_code"] = params["reqDocInfo"]["cons_code"]
        equipStatDataList[index]["sys_doc_num"] = docDefaultInfo["sysDocNum"]
        equipStatDataList[index]["input_date"] = params["reqDocContent"]["workDate"]

        for todayInputEquipStatus in todayInputEquipStatusList:
            # logs.debug(procName, os.path.basename(__file__), sys._getframe(0).f_code.co_name, u'----------------------------------0 ' + commUtilServ.jsonDumps(todayInputEquipStatus))

            if (
                equipStatDataList[index]["equip_code"]
                == todayInputEquipStatus["equip_code"]
            ):
                # if(resData['write_standard_code'] == constants.WORK_LOG_WRITE_CD_YS):
                # elif(resData['write_standard_code'] == constants.WORK_LOG_WRITE_CD_TO):

                # equipStatDataList[index]['cons_code'] = params['reqDocInfo']['cons_code']
                # equipStatDataList[index]['sys_doc_num'] = docDefaultInfo['sysDocNum']
                # equipStatDataList[index]['input_date'] = params['reqDocContent']['workDate']
                equipStatDataList[index]["prev_day_total"] = equipStatDataList[index][
                    "total_running"
                ]
                equipStatDataList[index]["today_total"] = float(
                    todayInputEquipStatus["today_input_load"]
                )
                equipStatDataList[index]["total_running"] = float(
                    equipStatDataList[index]["total_running"]
                ) + float(todayInputEquipStatus["today_input_load"])

    for equipStatData in equipStatDataList:
        resCd, msg, resData = servProjWorkLogMana.putWorkLogTodayInputEquipStatistics(
            equipStatData, docDefaultInfo["coCode"]
        )
        if resCd != 0:
            servProjWorkLogMana.delWorkLogTodayInputEquipStatistics(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogTodayInputEquipStatus(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogTodayWorkerStatistics(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )

            return resCd, msg, None

    params["reqDocContent"]["todayInputEquipStatusStatistics"] = equipStatDataList

    # 특이사항 데이터 저장
    resCd, msg, resData = servProjWorkLogMana.putWorkLogUniqueness(
        params, docDefaultInfo
    )
    if resCd != 0:
        servProjWorkLogMana.delWorkLogUniqueness(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogTodayInputEquipStatistics(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogTodayInputEquipStatus(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogTodayWorkerStatistics(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogDrawing(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogToday(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLog(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )

        return resCd, msg, None

    # 명일 예상 작업 데이터 저장
    resCd, msg, resData = servProjWorkLogMana.putWorkLogExceptedWorkTom(
        params, docDefaultInfo
    )
    if resCd != 0:
        servProjWorkLogMana.delWorkLogExceptedWorkTom(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogUniqueness(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogTodayInputEquipStatistics(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogTodayInputEquipStatus(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogTodayWorkerStatistics(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogDrawing(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogToday(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLog(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )

        return resCd, msg, None

    # 자재 사용량 데이터 저장
    resCd, msg, workLoadStatList = servProjWorkLogMana.getWorkLoadStatList(
        params["reqDocInfo"]["cons_code"], docDefaultInfo["coCode"]
    )
    if resCd != 0:
        servProjWorkLogMana.delWorkLogExceptedWorkTom(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogUniqueness(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogTodayInputEquipStatistics(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogTodayInputEquipStatus(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogTodayWorkerStatistics(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogDrawing(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLogToday(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )
        servProjWorkLogMana.delWorkLog(
            params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
        )

        return resCd, msg, None

    workLoadList = params["reqDocContent"]["workLoadList"]

    if len(workLoadList) > 0:
        for index in range(0, len(workLoadStatList)):
            workLoadStatList[index]["cons_code"] = params["reqDocInfo"]["cons_code"]
            workLoadStatList[index]["sys_doc_num"] = docDefaultInfo["sysDocNum"]
            workLoadStatList[index]["work_date"] = params["reqDocContent"]["workDate"]
            workLoadStatList[index]["amount_use_today"] = 0.0
            workLoadStatList[index]["today_complet_rate"] = workLoadStatList[index][
                "prev_day_complet_rate"
            ]

            for j in range(0, len(workLoadList)):

                if (
                    workLoadStatList[index]["constr_type_cd"]
                    == params["reqDocContent"]["workLoadList"][j]["constr_type_cd"]
                    and workLoadStatList[index]["material_name"]
                    == params["reqDocContent"]["workLoadList"][j]["material_name"]
                ):
                    workLoadStatList[index]["amount_use_prev_day"] = float(
                        workLoadStatList[index]["amount_use_prev_day"]
                    ) + float(
                        workLoadStatList[index]["amount_use_today"]
                    )  # 전일까지 사용 물량
                    workLoadStatList[index]["prev_day_complet_rate"] = round(
                        (
                            float(workLoadStatList[index]["amount_use_prev_day"])
                            / float(
                                params["reqDocContent"]["workLoadList"][j][
                                    "mat_total_cnt"
                                ]
                            )
                        )
                        * 100,
                        2,
                    )
                    workLoadStatList[index]["amount_use_today"] = float(
                        params["reqDocContent"]["workLoadList"][j]["amount_use_today"]
                    )
                    workLoadStatList[index]["today_complet_rate"] = round(
                        (
                            (
                                float(workLoadStatList[index]["amount_use_prev_day"])
                                + float(workLoadStatList[index]["amount_use_today"])
                            )
                            / float(
                                params["reqDocContent"]["workLoadList"][j][
                                    "mat_total_cnt"
                                ]
                            )
                        )
                        * 100,
                        2,
                    )

                    resCd, msg, resData = servCommMana.getCodeName(
                        params["reqDocContent"]["workLoadList"][j]["constr_type_cd"]
                    )
                    if resCd != 0:
                        servProjWorkLogMana.delWorkLogExceptedWorkTom(
                            params["reqDocInfo"]["cons_code"],
                            docDefaultInfo["sysDocNum"],
                        )
                        servProjWorkLogMana.delWorkLogUniqueness(
                            params["reqDocInfo"]["cons_code"],
                            docDefaultInfo["sysDocNum"],
                        )
                        servProjWorkLogMana.delWorkLogTodayInputEquipStatistics(
                            params["reqDocInfo"]["cons_code"],
                            docDefaultInfo["sysDocNum"],
                        )
                        servProjWorkLogMana.delWorkLogTodayInputEquipStatus(
                            params["reqDocInfo"]["cons_code"],
                            docDefaultInfo["sysDocNum"],
                        )
                        servProjWorkLogMana.delWorkLogTodayWorkerStatistics(
                            params["reqDocInfo"]["cons_code"],
                            docDefaultInfo["sysDocNum"],
                        )
                        servProjWorkLogMana.delWorkLogDrawing(
                            params["reqDocInfo"]["cons_code"],
                            docDefaultInfo["sysDocNum"],
                        )
                        servProjWorkLogMana.delWorkLogToday(
                            params["reqDocInfo"]["cons_code"],
                            docDefaultInfo["sysDocNum"],
                        )
                        servProjWorkLogMana.delWorkLog(
                            params["reqDocInfo"]["cons_code"],
                            docDefaultInfo["sysDocNum"],
                        )
                        return resCd, msg, None

                    params["reqDocContent"]["workLoadList"][j][
                        "constr_type_nm"
                    ] = resData["subcode_name"]
                    params["reqDocContent"]["workLoadList"][j][
                        "today_complet_rate"
                    ] = workLoadStatList[index]["today_complet_rate"]

                    break

    for workLoadStat in workLoadStatList:
        # logs.debug(procName, os.path.basename(__file__), sys._getframe(0).f_code.co_name, u'----------------------------------0')
        resCd, msg, resData = servProjWorkLogMana.putWorkLogWorkLoad(
            workLoadStat, params["reqDocContent"]["workDate"]
        )
        if resCd != 0:
            servProjWorkLogMana.delWorkLogWorkLoad(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogTodayInputEquipStatistics(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogTodayInputEquipStatus(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogTodayWorkerStatistics(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogDrawing(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLogToday(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )
            servProjWorkLogMana.delWorkLog(
                params["reqDocInfo"]["cons_code"], docDefaultInfo["sysDocNum"]
            )

            return resCd, msg, None

    return constants.REST_RESPONSE_CODE_ZERO, "", params
