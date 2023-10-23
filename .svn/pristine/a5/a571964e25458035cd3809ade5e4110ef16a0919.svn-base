# _*_coding: utf-8 -*-


from flask import Blueprint, request
import os
import sys
import json
import copy

commonApprovalManageApi = Blueprint("commonApprovalManageApi", __name__)


from commonApprovalManage.servCommonApprovalManage import servCommonApprovalManage
from userManage.servUserManage import servUserManage

from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import coCode  # 회사 코드

from companyManage.servCompanyManage import servCompanyManage

from common.commUtilService import commUtilService
from common.commonService import commonService
from common.logManage import logManage
from common import constants
from common import util_time

from companyManage.dataCompanyManage import dataCompanyManage
from commManage.servCommManage import servCommManage
from historyManage.servHistoryManage import servHistoryManage
from projectManage.servProjectManage import servProjectManage
from projectManage.sqlProjectManage import DELETE_JOINWORKFORCE_INFO, sqlProjectManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당

# 공통 승인 리스트 조회 API
@commonApprovalManageApi.route("/getCommApproList", methods=["POST"])
def getCommApproList():

    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servCommApproMana = servCommonApprovalManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공통 승인 리스트 조회 시작 ----------",
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

            #################################### 공통 승인 요청 리스트를 조회 한다. ####################################
        resCd, msg, resDataList = servCommApproMana.getCommApproList(
            loginUserInfo["id"], params
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

        ################################## Response 데이터를 생성 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Response 데이터를 생성 한다. ----------",
        )

        result = commServ.makeReturnMessage(resCd, msg, resDataList)

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
            "---------- 공통 승인 요청 리스트를 조회 한다. 종료 ----------",
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


# 상세 정보 조회
@commonApprovalManageApi.route("/getDetailCommAppro/<reqApproDate>", methods=["GET"])
def getDetailCommAppro(reqApproDate):

    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servCommApproMana = servCommonApprovalManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공통 승인 요청 상세정보 조회 시작 ----------",
        )

        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        # params = request.get_json()         # parameter recv

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "request header sysCd : "
            + sysCd
            + ", token : "
            + token
            + " / request url reqApproDate : "
            + reqApproDate,
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

            #################################### 공통 승인 요청 항목 상세 조회 한다. ####################################
        resCd, msg, commApproData = servCommApproMana.getDetailCommAppro(
            loginUserInfo["id"], reqApproDate
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

        ################################## Response 데이터를 생성 한다. ####################################
        commApproData["contents"] = json.loads(commApproData["contents"])

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Response 데이터를 생성 한다. ----------",
        )

        result = commServ.makeReturnMessage(resCd, msg, commApproData)

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
            "---------- 공통 승인 요청 상세 정보를 조회 한다. 종료 ----------",
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


# 결재 승인
@commonApprovalManageApi.route(
    "/commAppro/<reqApprovalId>/<reqApprovalDate>/<approvalStatus>", methods=["GET"]
)
def commAppro(reqApprovalId, reqApprovalDate, approvalStatus):

    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servCommApproMana = servCommonApprovalManage()

    servCompanyMana = servCompanyManage()

    servProjMana = servProjectManage()
    servHisMana = servHistoryManage()
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공통 승인 요청 상세정보 조회 시작 ----------",
        )

        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        # params = request.get_json()         # parameter recv

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "request header sysCd : "
            + sysCd
            + ", token : "
            + token
            + " / request url reqApprovalId :"
            + reqApprovalId
            + ", reqApprovalDate : "
            + reqApprovalDate
            + ", approvalStatus : "
            + approvalStatus,
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

            #################################### 공통 승인 요청 항목 상세 조회 한다. ####################################
        resCd, msg, commApproData = servCommApproMana.getDetailCommAppro(
            loginUserInfo["id"], reqApprovalDate
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

        commApproData["contents"] = json.loads(commApproData["contents"])

        if commApproData["next_approval_info"] != "":
            commApproData["next_approval_info"] = json.loads(
                commApproData["next_approval_info"]
            )
            #################################### 저장된 데이터와 Parameter 데이터를 비교 한다. ####################################

        if (
            commApproData["req_approval_id"] == reqApprovalId
            and commApproData["req_approval_date"] == reqApprovalDate
            and commApproData["approval_id"] == loginUserInfo["id"]
        ):

            # 1. 공통 승인 관리 데이터를 업데이트 한다.
            updateCommApproData = {
                "search_req_approval_id": reqApprovalId,
                "search_req_approval_date": reqApprovalDate,
                "search_approval_id": loginUserInfo["id"],
                "approval_status": approvalStatus,
                "complete_approval_date": util_time.get_current_time(
                    util_time.TIME_CURRENT_TYPE_14
                ),
            }

            resCd, msg, resData = servCommApproMana.updateCommApproval(
                updateCommApproData
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

            if (
                approvalStatus == constants.APPRO_STATUS_CD_APPRO
            ):  # 3. 승인인 경우 로직을 수행 한다.
                # 2. 승인 요청 타입을 확인 한다.
                if (
                    commApproData["req_approval_type"] == constants.COMM_APPRO_CD_CO_NEW
                ):  # 회사 신규 추가일 경우

                    if loginUserInfo["authority_code"] != constants.USER_MASTER:
                        result = commServ.makeReturnMessage(
                            constants.REST_RESPONSE_CODE_DATAFAIL,
                            "결재 승인 권한이 없습니다.",
                            None,
                        )

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Response : " + commUtilServ.jsonDumps(result),
                        )

                        return result

                    # 회사 사용 여부를 업데이트 한다.
                    updateCoInfoList = []

                    updateCoInfoData = {"key": "USE_TYPE", "value": "Y"}

                    updateCoInfoList.append(updateCoInfoData)
                    resCd, msg, resData = servCompanyMana.update_company(
                        commApproData["contents"]["co_code"], updateCoInfoList
                    )
                    # Error 발생 시 에러 코드 리턴
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        updateCommApproData["approval_status"] = commApproData[
                            "approval_status"
                        ]
                        resCd, msg, resData = servCommApproMana.updateCommApproval(
                            updateCommApproData
                        )

                        result = commServ.makeReturnMessage(resCd, msg, None)

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )

                        return result

                    # 회사 정보, 관리자 권한을 업데이트 한다.

                    updateUserInfoList = []

                    updateUserData = {
                        "key": "CO_CODE",
                        "value": commApproData["contents"]["co_code"],
                    }

                    updateUserInfoList.append(updateUserData)

                    updateUserData = {"key": "MANAGER_TYPE", "value": "Y"}
                    updateUserInfoList.append(updateUserData)

                    updateUserData = {
                        "key": "USER_STATE",
                        "value": constants.APPRO_STATUS_CD_APPRO,
                    }

                    updateUserInfoList.append(updateUserData)

                    updateUserData = {
                        "key": "AUTHORITY_CODE",
                        "value": commApproData["contents"]["after_authority_code"],
                    }
                    updateUserInfoList.append(updateUserData)

                    updateUserData = {
                        "key": "USER_POSITION",
                        "value": commApproData["contents"]["after_user_position"],
                    }
                    updateUserInfoList.append(updateUserData)
                    # updateUserData = {
                    # 	'key' : 'EMPLOY_STATUS',
                    # 	'value' : constants.EMPLOY_STATUS_CD_Y
                    # }

                    # updateUserInfoList.append(updateUserData)

                    updateUserData = {
                        "key": "CO_APPRO_DATE",
                        "value": util_time.get_current_time(
                            util_time.TIME_CURRENT_TYPE_14
                        ),
                    }

                    updateUserInfoList.append(updateUserData)

                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "response : " + commUtilServ.jsonDumps(updateUserInfoList),
                    )

                    resCd, msg, resData = servUserMana.updateUserCoInfo(
                        reqApprovalId, updateUserInfoList
                    )
                    # Error 발생 시 에러 코드 리턴
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        updateCoInfoList = []

                        updateCoInfoData = {"key": "USE_TYPE", "value": "N"}
                        updateCoInfoList.append(updateCoInfoData)
                        servCompanyMana.update_company(
                            commApproData["contents"]["co_code"], updateCoInfoList
                        )

                        updateCommApproData["approval_status"] = commApproData[
                            "approval_status"
                        ]
                        servCommApproMana.updateCommApproval(updateCommApproData)

                        result = commServ.makeReturnMessage(resCd, msg, None)

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )

                        return result
                # 				elif(commApproData['req_approval_type'] == constants.COMM_APPRO_CD_MANAGE): # 관리자 권한 위임/요청일 경우

                # 					resCd, msg, reqApprovalIdInfo = servUserMana.getUserInfo(1, commApproData['req_approval_id'], None)
                # 					if(resCd != 0):
                # 						logs.war(procName,
                # 								os.path.basename(__file__),
                # 								sys._getframe(0).f_code.co_name,
                # 								u'Database Error : ' + msg)

                # 						result = commServ.makeReturnMessage(resCd, msg, None)

                # 						logs.war(procName,
                # 								os.path.basename(__file__),
                # 								sys._getframe(0).f_code.co_name,
                # 								u'response : ' + commUtilServ.jsonDumps(result))

                # 						return result
                # 					resCd, msg, approvalIdInfo = servUserMana.getUserInfo(1, commApproData['approval_id'], None)
                # 					if(resCd != 0):
                # 						logs.war(procName,
                # 								os.path.basename(__file__),
                # 								sys._getframe(0).f_code.co_name,
                # 								u'Database Error : ' + msg)

                # 						result = commServ.makeReturnMessage(resCd, msg, None)

                # 						logs.war(procName,
                # 								os.path.basename(__file__),
                # 								sys._getframe(0).f_code.co_name,
                # 								u'response : ' + commUtilServ.jsonDumps(result))
                # 					resCd, msg, resData= servUserMana.updateUserCoInfo(reqApprovalId, updateUserInfoList)
                # 					# Error 발생 시 에러 코드 리턴
                # 					if(resCd != 0):
                # 						logs.war(procName,
                # 								os.path.basename(__file__),
                # 								sys._getframe(0).f_code.co_name,
                # 								u'Database Error : ' + msg)
                #
                # 						updateCoInfoList = []
                #
                # 						updateCoInfoData = {
                # 							'key' : "USE_TYPE",
                # 							'value' : "N"
                # 						}
                # 						updateCoInfoList.append(updateCoInfoData)
                # 						servCompanyMana.updateCompanyInfo(commApproData['contents']['co_code'], updateCoInfoList)
                #
                #
                # 						updateCommApproData['approval_status'] = commApproData['approval_status']
                # 						servCommApproMana.updateCommApproval(updateCommApproData)
                #
                #
                # 						result = commServ.makeReturnMessage(resCd, msg, None)
                #
                # 						logs.war(procName,
                # 								os.path.basename(__file__),
                # 								sys._getframe(0).f_code.co_name,
                # 								u'response : ' + commUtilServ.jsonDumps(result))
                #
                # 						return result
                elif (
                    commApproData["req_approval_type"] == constants.COMM_APPRO_CD_MANAGE
                ):  # 관리자 권한 위임/요청일 경우

                    resCd, msg, reqApprovalIdInfo = servUserMana.getUserInfo(
                        1, commApproData["req_approval_id"], None
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
                    resCd, msg, approvalIdInfo = servUserMana.getUserInfo(
                        1, commApproData["approval_id"], None
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

                    updateUserInfoListMandate = []
                    updateUserInfoListReq = []
                    if (
                        commApproData["contents"]["req_manage_type"]
                        == constants.AUTH_REQ_TYPE_MANDATE
                    ):

                        updateUserInfo = {"key": "MANAGER_TYPE", "value": ""}
                        updateUserInfoListMandate.append(updateUserInfo)

                        updateUserInfo = {"key": "MANAGER_TYPE", "value": "Y"}
                        updateUserInfoListReq.append(updateUserInfo)

                    elif (
                        commApproData["contents"]["req_manage_type"]
                        == constants.AUTH_REQ_TYPE_REQ
                    ):

                        updateUserInfo = {"key": "MANAGER_TYPE", "value": "Y"}
                        updateUserInfoListMandate.append(updateUserInfo)

                        updateUserInfoListReq = []

                        updateUserInfo = {"key": "MANAGER_TYPE", "value": ""}
                        updateUserInfoListReq.append(updateUserInfo)

                    resCd, msg, resData = servUserMana.updateUserCoInfo(
                        reqApprovalIdInfo["id"], updateUserInfoListMandate
                    )
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        updateCommApproData["approval_status"] = commApproData[
                            "approval_status"
                        ]
                        servCommApproMana.updateCommApproval(updateCommApproData)

                        result = commServ.makeReturnMessage(resCd, msg, None)

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )

                        return result

                    resCd, msg, resData = servUserMana.updateUserCoInfo(
                        approvalIdInfo["id"], updateUserInfoListReq
                    )
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        updateUserInfoListMandate = []
                        if (
                            commApproData["contents"]["req_manage_type"]
                            == constants.AUTH_REQ_TYPE_MANDATE
                        ):
                            updateUserInfo = {"key": "MANAGER_TYPE", "value": "Y"}
                            updateUserInfoListMandate.append(updateUserInfo)
                        else:
                            updateUserInfo = {"key": "MANAGER_TYPE", "value": ""}
                            updateUserInfoListMandate.append(updateUserInfo)
                        resCd, msg, resData = servUserMana.updateUserCoInfo(
                            reqApprovalIdInfo["id"], updateUserInfoListMandate
                        )

                        updateCommApproData["approval_status"] = commApproData[
                            "approval_status"
                        ]
                        servCommApproMana.updateCommApproval(updateCommApproData)

                        result = commServ.makeReturnMessage(resCd, msg, None)

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )

                        return result

                elif (
                    commApproData["req_approval_type"] == constants.COMM_APPRO_CD_SIGNUP
                ):  # 회원가입 승인일 경우
                    if loginUserInfo["authority_code"] != constants.USER_MASTER:
                        if loginUserInfo["manager_type"] != "Y":
                            result = commServ.makeReturnMessage(
                                constants.REST_RESPONSE_CODE_DATAFAIL,
                                "결재 승인 권한이 없습니다.",
                                None,
                            )

                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "Response : " + commUtilServ.jsonDumps(result),
                            )

                            return result

                    updateUserInfoSignup = []

                    # 					updateUserInfo = {
                    # 						'key' : 'EMPLOY_STATUS',
                    # 						'value' : constants.EMPLOY_STATUS_CD_Y
                    # 					}
                    # 					updateUserInfoSignup.append(updateUserInfo)

                    updateUserInfo = {
                        "key": "USER_STATE",
                        "value": constants.APPRO_STATUS_CD_APPRO,
                    }
                    updateUserInfoSignup.append(updateUserInfo)

                    updateUserInfo = {
                        "key": "CO_CODE",
                        "value": commApproData["contents"]["afterCoCode"],
                    }
                    updateUserInfoSignup.append(updateUserInfo)

                    updateUserInfo = {
                        "key": "AUTHORITY_CODE",
                        "value": commApproData["contents"]["after_authority_code"],
                    }
                    updateUserInfoSignup.append(updateUserInfo)

                    updateUserInfo = {
                        "key": "USER_POSITION",
                        "value": commApproData["contents"]["after_user_position"],
                    }
                    updateUserInfoSignup.append(updateUserInfo)

                    updateUserInfo = {
                        "key": "CO_APPRO_DATE",
                        "value": util_time.get_current_time(
                            util_time.TIME_CURRENT_TYPE_14
                        ),
                    }
                    updateUserInfoSignup.append(updateUserInfo)

                    resCd, msg, resData = servUserMana.updateUserCoInfo(
                        commApproData["req_approval_id"], updateUserInfoSignup
                    )
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        updateCommApproData["approval_status"] = commApproData[
                            "approval_status"
                        ]
                        servCommApproMana.updateCommApproval(updateCommApproData)

                        result = commServ.makeReturnMessage(resCd, msg, None)

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )

                        return result
                elif (
                    commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_WITHDRAWAL
                    or commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_LEAVE
                ):  # 회원탈퇴 승인일 경우
                    if loginUserInfo["authority_code"] != constants.USER_MASTER:
                        if loginUserInfo["manager_type"] != "Y":
                            result = commServ.makeReturnMessage(
                                constants.REST_RESPONSE_CODE_DATAFAIL,
                                "결재 승인 권한이 없습니다.",
                                None,
                            )

                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "Response : " + commUtilServ.jsonDumps(result),
                            )

                            return result

                    userId = ""

                    # if(commApproData['req_approval_type'] == constants.COMM_APPRO_CD_WITHDRAWAL):
                    userId = commApproData["req_approval_id"]
                    # else:
                    # userId = commApproData['approval_id']

                    # 재직 정보를 저장 한다.
                    # resCd, msg, userCoHistoryInfo = servHisMana.putUserCompanyHistory(commApproData['req_approval_id']) #재직 정보를 저장 한다.

                    # 참여하고 있는 프로젝트의 참여종료기간을 퇴사일로 일괄 업데이트 한다 - 삭제
                    """
                    resCd, msg, _ = servProjMana.putJoinWorkforceEnd(
                        None,
                        loginUserInfo["id"],
                        util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
                    )
                    if resCd != 0:
                        return commServ.makeReturnMessage(resCd, msg, None)
                    """
                    resCd, msg, userCoHistoryInfo = servHisMana.putUserCompanyHistory(
                        userId
                    )  # 재직 정보를 저장 한다.
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        updateCommApproData["approval_status"] = commApproData[
                            "approval_status"
                        ]
                        servCommApproMana.updateCommApproval(updateCommApproData)

                        result = commServ.makeReturnMessage(resCd, msg, None)

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )

                        return result

                    # 프로젝트 정보를 저장 한다.

                    # 1. 재직 기간 내에 해당되는 프로젝트 정보를 가져 온다.
                    resCd, msg, projectHistoryList = servProjMana.getProjectHistoryList(
                        userCoHistoryInfo
                    )
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        # 재직 정보를 원복 시킨다.
                        servHisMana.delUserCompanyHistory(userCoHistoryInfo)

                        # 결재 정보를 원복 시킨다.
                        updateCommApproData["approval_status"] = commApproData[
                            "approval_status"
                        ]
                        servCommApproMana.updateCommApproval(updateCommApproData)

                        result = commServ.makeReturnMessage(resCd, msg, None)

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )

                        return result

                    # 2. 재직 기간 내에 해당되는 프로젝트 정보를 저장 한다.
                    resCd, msg, resData = servHisMana.putProjHistoryList(
                        userCoHistoryInfo, projectHistoryList
                    )
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        # 재직 기간내 프로젝트 정보를 삭제 한다.
                        servHisMana.delProjHistoryList(
                            userCoHistoryInfo, projectHistoryList
                        )

                        # 재직 정보를 원복 시킨다.
                        servHisMana.delUserCompanyHistory(userCoHistoryInfo)

                        # 결재 정보를 원복 시킨다.
                        updateCommApproData["approval_status"] = commApproData[
                            "approval_status"
                        ]
                        servCommApproMana.updateCommApproval(updateCommApproData)

                        result = commServ.makeReturnMessage(resCd, msg, None)

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )

                        return result

                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "response : " + commUtilServ.jsonDumps(commApproData),
                    )

                    commApproData["contents"]["after_user_position"] = ""
                    commApproData["contents"][
                        "after_authority_code"
                    ] = constants.USER_INOCCUPATION
                    resCd, msg, resData = approvalWithDraw(userId, commApproData)
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )
                        # 재직 기간내 프로젝트 정보를 삭제 한다.
                        servHisMana.delProjHistoryList(
                            userCoHistoryInfo, projectHistoryList
                        )

                        # 재직 정보를 원복 시킨다.
                        servHisMana.delUserCompanyHistory(userCoHistoryInfo)

                        # 결재 정보를 원복 시킨다.
                        updateCommApproData["approval_status"] = commApproData[
                            "approval_status"
                        ]
                        servCommApproMana.updateCommApproval(updateCommApproData)

                        result = commServ.makeReturnMessage(resCd, msg, None)

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )

                        return result

                    # 3. 프로젝트에서 제외시킨다
                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        f"response : {loginUserInfo['co_code']} {loginUserInfo['id']}",
                    )
                    resCd, msg, _ = servProjMana.deleteJoinWorkforce(loginUserInfo["co_code"], loginUserInfo["id"])

                    if commApproData["next_approval_info"] != "":

                        if (
                            commApproData["next_approval_info"]["req_approval_type"]
                            == constants.COMM_APPRO_CD_INVITE
                        ):
                            updateCommApproData = {
                                "search_req_approval_id": commApproData[
                                    "next_approval_info"
                                ]["req_approval_id"],
                                "search_req_approval_date": commApproData[
                                    "next_approval_info"
                                ]["req_approval_date"],
                                "search_approval_id": commApproData[
                                    "next_approval_info"
                                ]["approval_id"],
                                "approval_status": constants.APPRO_STATUS_CD_APPRO,
                                "complete_approval_date": util_time.get_current_time(
                                    util_time.TIME_CURRENT_TYPE_14
                                ),
                            }

                            resCd, msg, resData = servCommApproMana.updateCommApproval(
                                updateCommApproData
                            )
                            # Error 발생 시 에러 코드 리턴
                            if resCd != 0:
                                logs.war(
                                    procName,
                                    os.path.basename(__file__),
                                    sys._getframe(0).f_code.co_name,
                                    "Database Error : " + msg,
                                )

                                updateCommApproData["approval_status"] = commApproData[
                                    "approval_status"
                                ]
                                servCommApproMana.updateCommApproval(
                                    updateCommApproData
                                )

                                result = commServ.makeReturnMessage(resCd, msg, None)

                                logs.war(
                                    procName,
                                    os.path.basename(__file__),
                                    sys._getframe(0).f_code.co_name,
                                    "response : " + commUtilServ.jsonDumps(result),
                                )

                                return result

                        else:
                            (
                                resCd,
                                msg,
                                resData,
                            ) = servCommApproMana.putCommonApprovalInfo(
                                commApproData["next_approval_info"]
                            )
                            if resCd != 0:
                                logs.war(
                                    procName,
                                    os.path.basename(__file__),
                                    sys._getframe(0).f_code.co_name,
                                    "Database Error : " + msg,
                                )

                                updateCommApproData["approval_status"] = commApproData[
                                    "approval_status"
                                ]
                                servCommApproMana.updateCommApproval(
                                    updateCommApproData
                                )

                                result = commServ.makeReturnMessage(resCd, msg, None)

                                logs.war(
                                    procName,
                                    os.path.basename(__file__),
                                    sys._getframe(0).f_code.co_name,
                                    "response : " + commUtilServ.jsonDumps(result),
                                )

                                return result
                elif (
                    commApproData["req_approval_type"] == constants.COMM_APPRO_CD_INVITE
                ):  # 회원 초대 승인일 경우

                    # 무직일 경우 회사 초대 승인을 한다.
                    if (
                        commApproData["contents"]["respondent_employ_status"]
                        == constants.EMPLOY_STATUS_CD_N
                    ):
                        resCd, msg, resData = approvalInvite(commApproData)
                        if resCd != 0:
                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "Database Error : " + msg,
                            )

                            updateCommApproData["approval_status"] = commApproData[
                                "approval_status"
                            ]
                            servCommApproMana.updateCommApproval(updateCommApproData)
                            result = commServ.makeReturnMessage(resCd, msg, None)

                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "response : " + commUtilServ.jsonDumps(result),
                            )

                            return result

                    # 회사에 소속된 경우 탈퇴 신청을 하고 회원 초대 상태를 승인 대기 상태로 변경 한다.(회원 탈퇴 승인 시 자동으로 회원 초대 상태를 승인으로 변경 한다.)
                    else:
                        # 승인 요청 항목을 승인 대기 상태로 변경 한다.
                        updateCommApproData[
                            "approval_status"
                        ] = constants.APPRO_STATUS_CD_APPRO_WAIT
                        resCd, msg, resData = servCommApproMana.updateCommApproval(
                            updateCommApproData
                        )
                        if resCd != 0:
                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "Database Error : " + msg,
                            )

                            updateCommApproData["approval_status"] = commApproData[
                                "approval_status"
                            ]
                            servCommApproMana.updateCommApproval(updateCommApproData)
                            result = commServ.makeReturnMessage(resCd, msg, None)

                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "response : " + commUtilServ.jsonDumps(result),
                            )

                            return result

                        # 회원 탈퇴를 신청 한다.
                        resCd, msg, resData = regWithDraw(commApproData, "Y")
                        if resCd != 0:
                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "Database Error : " + msg,
                            )

                            updateCommApproData["approval_status"] = commApproData[
                                "approval_status"
                            ]
                            servCommApproMana.updateCommApproval(updateCommApproData)
                            result = commServ.makeReturnMessage(resCd, msg, None)

                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "response : " + commUtilServ.jsonDumps(result),
                            )

                            return result

                elif (
                    commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_PROJ_NEW
                ):  # 프로젝트 생성 승인일 경우 => 조현우 수정 본사관리자도 가능
                    if (
                        loginUserInfo["authority_code"] != constants.USER_MASTER
                        and loginUserInfo["authority_code"] != constants.USER_MONITOR
                    ):
                        if loginUserInfo["manager_type"] != "Y":
                            result = commServ.makeReturnMessage(
                                constants.REST_RESPONSE_CODE_DATAFAIL,
                                "결재 승인 권한이 없습니다.",
                                None,
                            )

                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "Response : " + commUtilServ.jsonDumps(result),
                            )

                            return result
                    resCd, msg, resData = approvalProjNew(commApproData)
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        updateCommApproData["approval_status"] = commApproData[
                            "approval_status"
                        ]
                        servCommApproMana.updateCommApproval(updateCommApproData)
                        result = commServ.makeReturnMessage(resCd, msg, None)

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )

                        return result

                elif (
                    commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_PROJ_MODIFY
                ):  # 프로젝트 수정 승인일 경우 => 조현우 수정 회사관리자도 가능
                    if (
                        loginUserInfo["authority_code"] != constants.USER_MASTER
                        and loginUserInfo["authority_code"] != constants.USER_MONITOR
                    ):
                        if loginUserInfo["manager_type"] != "Y":
                            result = commServ.makeReturnMessage(
                                constants.REST_RESPONSE_CODE_DATAFAIL,
                                "결재 승인 권한이 없습니다.",
                                None,
                            )

                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "Response : " + commUtilServ.jsonDumps(result),
                            )

                            return result
                    resCd, msg, resData = approvalProjModify(commApproData)
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        updateCommApproData["approval_status"] = commApproData[
                            "approval_status"
                        ]
                        servCommApproMana.updateCommApproval(updateCommApproData)
                        result = commServ.makeReturnMessage(resCd, msg, None)

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )

                        return result
                elif (
                    commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_PROJ_DELETE
                ):  # 프로젝트 삭제 승인일 경우 => 조현우 수정 회사관리자도 가능
                    if (
                        loginUserInfo["authority_code"] != constants.USER_MASTER
                        and loginUserInfo["authority_code"] != constants.USER_MONITOR
                    ):
                        if loginUserInfo["manager_type"] != "Y":
                            result = commServ.makeReturnMessage(
                                constants.REST_RESPONSE_CODE_DATAFAIL,
                                "결재 승인 권한이 없습니다.",
                                None,
                            )

                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "Response : " + commUtilServ.jsonDumps(result),
                            )

                            return result
                    resCd, msg, resData = approvalProjDelete(commApproData)
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        updateCommApproData["approval_status"] = commApproData[
                            "approval_status"
                        ]
                        servCommApproMana.updateCommApproval(updateCommApproData)
                        result = commServ.makeReturnMessage(resCd, msg, None)

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )

                        return result

                elif (
                    commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_CO_MODIFY
                ):  # 회사 정보 수정 승인일 경우
                    if loginUserInfo["authority_code"] != constants.USER_MASTER:
                        if loginUserInfo["manager_type"] != "Y":
                            result = commServ.makeReturnMessage(
                                constants.REST_RESPONSE_CODE_DATAFAIL,
                                "결재 승인 권한이 없습니다.",
                                None,
                            )

                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "Response : " + commUtilServ.jsonDumps(result),
                            )

                            return result
                    resCd, msg, resData = approvalCoModify(commApproData)
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        result = commServ.makeReturnMessage(resCd, msg, resData)
                        return result
                elif (
                    commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_MY_MODIFY
                ):  # 내 정보 수정 승인일 경우
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "시자자자자작2",
                    )
                    commApproData["contents"]["id"] = commApproData["req_approval_id"]
                    resCd, msg, resData = approvalMyModify(commApproData)
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        result = commServ.makeReturnMessage(resCd, msg, resData)
                        return result
                elif (
                    commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_PROJ_STOP
                ):  # 프로젝트 중지 승인일 경우 => 조현우 수정 회사관리자도 가능
                    if (
                        loginUserInfo["authority_code"] != constants.USER_MASTER
                        and loginUserInfo["authority_code"] != constants.USER_MONITOR
                    ):
                        if loginUserInfo["manager_type"] != "Y":
                            result = commServ.makeReturnMessage(
                                constants.REST_RESPONSE_CODE_DATAFAIL,
                                "결재 승인 권한이 없습니다.",
                                None,
                            )

                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "Response : " + commUtilServ.jsonDumps(result),
                            )

                            return result
                    resCd, msg, resData = approvalProjStop(commApproData)
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        result = commServ.makeReturnMessage(resCd, msg, resData)
                        return result

                elif (
                    commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_PROJ_RESTART
                ):  # 프로젝트 재시작 승인일 경우 => 조현우 수정 회사관리자도 가능
                    if (
                        loginUserInfo["authority_code"] != constants.USER_MASTER
                        and loginUserInfo["authority_code"] != constants.USER_MONITOR
                    ):
                        if loginUserInfo["manager_type"] != "Y":
                            result = commServ.makeReturnMessage(
                                constants.REST_RESPONSE_CODE_DATAFAIL,
                                "결재 승인 권한이 없습니다.",
                                None,
                            )

                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "Response : " + commUtilServ.jsonDumps(result),
                            )

                            return result
                    resCd, msg, resData = approvalProjRestart(commApproData)
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        result = commServ.makeReturnMessage(resCd, msg, resData)
                        return result
            elif (
                approvalStatus == constants.APPRO_STATUS_CD_REFUSE
            ):  # 4. 거절일 경우 로직을 수행 한다.
                # 2. 승인 요청 타입을 확인 한다.
                if (
                    commApproData["req_approval_type"] == constants.COMM_APPRO_CD_CO_NEW
                ):  # 회사 신규 추가일 경우
                    if loginUserInfo["authority_code"] != constants.USER_MASTER:
                        result = commServ.makeReturnMessage(
                            constants.REST_RESPONSE_CODE_DATAFAIL,
                            "결재 승인 권한이 없습니다.",
                            None,
                        )

                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Response : " + commUtilServ.jsonDumps(result),
                        )

                        return result

                    # 회사 정보 삭제

                    resCd, msg, resData = servCompanyMana.delete_company(
                        commApproData["contents"]["regisnum"]
                    )
                    # Error 발생 시 에러 코드 리턴
                    if resCd != 0:
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "Database Error : " + msg,
                        )

                        updateCommApproData["approval_status"] = commApproData[
                            "approval_status"
                        ]
                        servCommApproMana.updateCommApproval(updateCommApproData)

                        result = commServ.makeReturnMessage(resCd, msg, None)
                        logs.war(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "response : " + commUtilServ.jsonDumps(result),
                        )

                        return result

                elif (
                    commApproData["req_approval_type"] == constants.COMM_APPRO_CD_MANAGE
                ):  # 관리자 권한 위임/요청 거절일 경우 => 조현우 수정 시스템관리자가 아닌 회사관리자이므로 담당회사 본사인력도 가능 => 거절은 누구나 전부 다 가능
                    # if loginUserInfo["authority_code"] != constants.USER_MASTER and loginUserInfo["authority_code"] != constants.USER_MONITOR:
                    pass
                    """
                    if loginUserInfo["manager_type"] != "Y":
                        result = commServ.makeReturnMessage(
                            constants.REST_RESPONSE_CODE_DATAFAIL,
                            "결재 승인 권한이 없습니다.",
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
                        "response : " + commUtilServ.jsonDumps(result),
                    )
                    """
                elif (
                    commApproData["req_approval_type"] == constants.COMM_APPRO_CD_SIGNUP
                ):  # 회원가입 거절일 경우
                    if loginUserInfo["authority_code"] != constants.USER_MASTER:
                        if loginUserInfo["manager_type"] != "Y":
                            result = commServ.makeReturnMessage(
                                constants.REST_RESPONSE_CODE_DATAFAIL,
                                "결재 승인 권한이 없습니다.",
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
                        "response : " + commUtilServ.jsonDumps(result),
                    )
                elif (
                    commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_WITHDRAWAL
                ):  # 회원탈퇴 거절일 경우
                    if (
                        commApproData["next_approval_info"] != ""
                        and commApproData["next_approval_info"]["req_approval_type"]
                        == constants.COMM_APPRO_CD_INVITE
                    ):  # 회원 초대로 인하여 탈퇴 요청을 한 경우 탈퇴 거절 시 회원 초대 승인 상태로 되돌린다.
                        updateCommApproData = {
                            "search_req_approval_id": commApproData[
                                "next_approval_info"
                            ]["req_approval_id"],
                            "search_req_approval_date": commApproData[
                                "next_approval_info"
                            ]["req_approval_date"],
                            "search_approval_id": commApproData["next_approval_info"][
                                "approval_id"
                            ],
                            "approval_status": constants.APPRO_STATUS_CD_WAIT,
                            "complete_approval_date": "",
                        }

                        resCd, msg, resData = servCommApproMana.updateCommApproval(
                            updateCommApproData
                        )
                        # Error 발생 시 에러 코드 리턴
                        if resCd != 0:
                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "Database Error : " + msg,
                            )
                            updateCommApproData["approval_status"] = commApproData[
                                "approval_status"
                            ]
                            servCommApproMana.updateCommApproval(updateCommApproData)

                            result = commServ.makeReturnMessage(resCd, msg, None)

                            logs.war(
                                procName,
                                os.path.basename(__file__),
                                sys._getframe(0).f_code.co_name,
                                "response : " + commUtilServ.jsonDumps(result),
                            )

                            return result

                # 조현우 추가 프로젝트 생성거절일 경우
                elif (
                    commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_PROJ_NEW
                ):  # 프로젝트 생성 요청 거절일 경우 => 조현우 수정 시스템관리자가 아닌 회사관리자이므로 담당회사 본사인력도 가능
                    if (
                        loginUserInfo["authority_code"] != constants.USER_MASTER
                        and loginUserInfo["authority_code"] != constants.USER_MONITOR
                    ):
                        if loginUserInfo["manager_type"] != "Y":
                            result = commServ.makeReturnMessage(
                                constants.REST_RESPONSE_CODE_DATAFAIL,
                                "결재 승인 권한이 없습니다.",
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
                        "response : " + commUtilServ.jsonDumps(result),
                    )

                # 조현우 추가 프로젝트 수정거절일 경우
                elif (
                    commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_PROJ_MODIFY
                ):  # 프로젝트 수정 요청 거절일 경우 => 조현우 수정 시스템관리자가 아닌 회사관리자이므로 담당회사 본사인력도 가능
                    if (
                        loginUserInfo["authority_code"] != constants.USER_MASTER
                        and loginUserInfo["authority_code"] != constants.USER_MONITOR
                    ):
                        if loginUserInfo["manager_type"] != "Y":
                            result = commServ.makeReturnMessage(
                                constants.REST_RESPONSE_CODE_DATAFAIL,
                                "결재 승인 권한이 없습니다.",
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
                        "response : " + commUtilServ.jsonDumps(result),
                    )

                # 조현우 추가 프로젝트 삭제 거절일 경우
                elif (
                    commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_PROJ_DELETE
                ):  # 프로젝트 삭제 요청 거절일 경우 => 조현우 수정 시스템관리자가 아닌 회사관리자이므로 담당회사 본사인력도 가능
                    if (
                        loginUserInfo["authority_code"] != constants.USER_MASTER
                        and loginUserInfo["authority_code"] != constants.USER_MONITOR
                    ):
                        if loginUserInfo["manager_type"] != "Y":
                            result = commServ.makeReturnMessage(
                                constants.REST_RESPONSE_CODE_DATAFAIL,
                                "결재 승인 권한이 없습니다.",
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
                        "response : " + commUtilServ.jsonDumps(result),
                    )

                # 조현우 추가 회사정보 수정 요청 거절일 경우
                elif (
                    commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_CO_MODIFY
                ):  # 회사정보 수정 요청 거절일 경우 => 조현우 수정 시스템관리자가 아닌 회사관리자이므로 담당회사 본사인력도 가능
                    if (
                        loginUserInfo["authority_code"] != constants.USER_MASTER
                        and loginUserInfo["authority_code"] != constants.USER_MONITOR
                    ):
                        if loginUserInfo["manager_type"] != "Y":
                            result = commServ.makeReturnMessage(
                                constants.REST_RESPONSE_CODE_DATAFAIL,
                                "결재 승인 권한이 없습니다.",
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
                        "response : " + commUtilServ.jsonDumps(result),
                    )

                """
                elif (
                    commApproData["req_approval_type"]
                    == constants.COMM_APPRO_CD_CO_MODIFY
                ):  # 회원탈퇴 거절일 경우
                    modifyContents = commApproData["contents"]["modify"]
                    if modifyContents["co_license_status"] == "C":
                        commServ.removeFile(
                            modifyContents["co_license_path"],
                            modifyContents["co_license_change_name"],
                        )
                    if modifyContents["bs_license_status"] == "C":
                        commServ.removeFile(
                            modifyContents["bs_license_path"],
                            modifyContents["bs_license_change_name"],
                        )

        # 					logs.war(procName,
        # 							os.path.basename(__file__),
        # 							sys._getframe(0).f_code.co_name,
        # 							u'response : ' + commUtilServ.jsonDumps(result))
                """
        else:
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

        ################################## Response 데이터를 생성 한다. ####################################
        # commApproData['contents'] = json.loads(commApproData['contents'])

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Response 데이터를 생성 한다. ----------",
        )

        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)

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
            "---------- 공통 승인 요청 상세 정보를 조회 한다. 종료 ----------",
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


# 결재 요청 등록
@commonApprovalManageApi.route("/reqCommAppro", methods=["PUT"])
def reqCcommAppro():
    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servCommMana = servCommManage()

    servCompanyMana = servCompanyManage()

    servCommApproMana = servCommonApprovalManage()
    sProjMana = sqlProjectManage()
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
            return result

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 로그인 사용자가 프로젝트에 참여 하고 있는지 확인 한다. ----------",
        )

        #################################### 승인 요청 타입을 확인 한다. ####################################
        if params["req_approval_type"] == constants.COMM_APPRO_CD_CO_NEW:
            resCd, msg, resData = regCompany(params["contents"], request)
            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + msg,
                )

                result = commServ.makeReturnMessage(resCd, msg, resData)
                return result

            ##########################################################################################################
            # 회사 생성 승인을 위한 데이터 생성
            common_approval_manage = {
                "req_approval_id": loginUserInfo["id"],
                "req_approval_type": constants.COMM_APPRO_CD_CO_NEW,
                "approval_status": constants.APPRO_STATUS_CD_WAIT,
                "contents": resData,
                "approval_id": "master",
                "req_approval_date": util_time.get_current_time(
                    util_time.TIME_CURRENT_TYPE_14
                ),
                "complete_approval_date": "",
                "next_approval_info": "",
            }
            ##########################################################################################################

        elif params["req_approval_type"] == constants.COMM_APPRO_CD_MANAGE:
            resCd, msg, resData = regManage(params["contents"])

            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + msg,
                )

                result = commServ.makeReturnMessage(resCd, msg, resData)
                return result

            ##########################################################################################################
            # 관리자 요청 / 위임 승인을 위한 데이터 생성
            common_approval_manage = {
                "req_approval_id": loginUserInfo["id"],
                "req_approval_type": constants.COMM_APPRO_CD_MANAGE,
                "approval_status": constants.APPRO_STATUS_CD_WAIT,
                "contents": resData,
                "approval_id": resData["approval_id"],
                "req_approval_date": util_time.get_current_time(
                    util_time.TIME_CURRENT_TYPE_14
                ),
                "complete_approval_date": "",
                "next_approval_info": "",
            }
            ##########################################################################################################

        elif params["req_approval_type"] == constants.COMM_APPRO_CD_INVITE:
            # resCd, msg, resData = regInvite(loginUserInfo, params['approval_id'], params['contents'])
            resCd, msg, resData = regInvite(loginUserInfo, params["approval_id"])

            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + msg,
                )

                result = commServ.makeReturnMessage(resCd, msg, resData)
                return result

            ##########################################################################################################
            # 회원 초대를 위한 데이터 생성
            common_approval_manage = {
                "req_approval_id": loginUserInfo["id"],
                "req_approval_type": constants.COMM_APPRO_CD_INVITE,
                "approval_status": constants.APPRO_STATUS_CD_WAIT,
                "contents": resData,
                "approval_id": params["approval_id"],
                "req_approval_date": util_time.get_current_time(
                    util_time.TIME_CURRENT_TYPE_14
                ),
                "complete_approval_date": "",
                "next_approval_info": "",
            }
            ##########################################################################################################

        elif params["req_approval_type"] == constants.COMM_APPRO_CD_LEAVE:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "퇴사요청 처리시작",
            )
            # resCd, msg, resData = regInvite(loginUserInfo, params['approval_id'], params['contents'])
            resCd, msg, resData = regLeave(loginUserInfo, params["approval_id"])

            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + msg,
                )

                result = commServ.makeReturnMessage(resCd, msg, resData)
                return result

            ##########################################################################################################
            # 퇴사 데이터 생성
            common_approval_manage = {
                "req_approval_id": loginUserInfo["id"],
                "req_approval_type": constants.COMM_APPRO_CD_LEAVE,
                "approval_status": constants.APPRO_STATUS_CD_WAIT,
                "contents": resData,
                "approval_id": params["approval_id"],
                "req_approval_date": util_time.get_current_time(
                    util_time.TIME_CURRENT_TYPE_14
                ),
                "complete_approval_date": "",
                "next_approval_info": "",
            }

        # 프로젝트 생성
        elif params["req_approval_type"] == constants.COMM_APPRO_CD_PROJ_NEW:

            # inputFlg = 'Y'

            # supervisorList = params['contents']['supervisorsList']

            # for supervisor in supervisorList:
            # 	if(supervisor['id'] == loginUserInfo['id']):
            # 		inputFlg = 'N'
            # 		break;

            # if(inputFlg == 'Y'):
            # 	# 1. 프로젝트를 생성하는 사람은 기본적으로 참여인력에 추가한다.
            # 	defaultUserInfo = {
            # 		'id' : loginUserInfo['id'],
            # 		'job_title_code' : '',
            # 		'authority_code' : loginUserInfo['authority_code']
            # 	}

            # 	if(loginUserInfo['authority_code'] == constants.USER_AUTH_SUPERVISOR_MONITOR or
            # 			loginUserInfo['authority_code'] == constants.USER_AUTH_SUPERVISOR):
            # 		defaultUserInfo['job_title_code'] = constants.JOB_TITLE_CD_SUPERVISOR_MONITOR
            # 	elif(loginUserInfo['authority_code'] == constants.USER_AUTH_SUPERVISING):
            # 		defaultUserInfo['job_title_code'] = constants.JOB_TITLE_CD_SUPERVISING_MAIN

            # 	params['contents']['supervisorsList'].append(defaultUserInfo)

            # 본사 관리자 검색
            searchList = []

            searchInfo = {"key": "CO_CODE", "value": loginUserInfo["co_code"]}
            searchList.append(searchInfo)

            searchInfo = {"key": "MANAGER_TYPE", "value": "Y"}
            searchList.append(searchInfo)

            resCd, msg, managerUserInfo = servUserMana.searchUserInfoList(searchList)
            if resCd != 0:
                return resCd, msg, None

            # inputFlg = 'Y'

            # supervisorList = params['contents']['supervisorsList']

            # for supervisor in supervisorList:
            # 	if(supervisor['id'] == managerUserInfo[0]['id']):
            # 		inputFlg = 'N'
            # 		break;

            # if(inputFlg == 'Y'):
            # 	# 1. 프로젝트를 생성하는 사람은 기본적으로 참여인력에 추가한다.
            # 	defaultUserInfo = {
            # 		'id' : managerUserInfo[0]['id'],
            # 		'job_title_code' : '',
            # 		'authority_code' : managerUserInfo[0]['authority_code']
            # 	}

            # 	if(loginUserInfo['authority_code'] == constants.USER_AUTH_SUPERVISOR_MONITOR):
            # 		defaultUserInfo['job_title_code'] = constants.JOB_TITLE_CD_SUPERVISOR_MONITOR
            # 	elif(loginUserInfo['authority_code'] == constants.USER_AUTH_SUPERVISING):
            # 		defaultUserInfo['job_title_code'] = constants.JOB_TITLE_CD_SUPERVISING_MAIN

            # 	params['contents']['supervisorsList'].append(defaultUserInfo)

            resCd, msg, resData = regProjNew(loginUserInfo, params)

            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + msg,
                )

                result = commServ.makeReturnMessage(resCd, msg, resData)
                return result

            # 프로젝트 추가 데이터 생성
            common_approval_manage = {
                "req_approval_id": loginUserInfo["id"],
                "req_approval_type": constants.COMM_APPRO_CD_PROJ_NEW,
                "approval_status": constants.APPRO_STATUS_CD_WAIT,
                "contents": params["contents"],
                "approval_id": "",
                "req_approval_date": util_time.get_current_time(
                    util_time.TIME_CURRENT_TYPE_14
                ),
                "complete_approval_date": "",
                "next_approval_info": "",
            }

            if (
                loginUserInfo["authority_code"] == constants.USER_MONITOR
                and loginUserInfo["manager_type"] == "Y"
            ):  # 본사 관리자이기 때문에 바로 프로젝트 생성을 할 수 있슴
                resCd, msg, resData = approvalProjNew(common_approval_manage)
                if resCd != 0:
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Database Error : " + msg,
                    )

                    result = commServ.makeReturnMessage(resCd, msg, resData)
                    return result

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
                    "---------- 프로젝트 생성 완료 ----------",
                )
                return result
            elif (
                loginUserInfo["authority_code"] == constants.USER_MONITOR
                and loginUserInfo["manager_type"] != "Y"
            ):  # 감리자 본사 모니터링으로 프로젝트 생성 승인을 받아야 함.
                common_approval_manage["approval_id"] = managerUserInfo[0]["id"]
                ##########################################################################################################
            else:
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "프로젝트 생성 요청 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "response : " + commUtilServ.jsonDumps(result),
                )
                return result

        # 프로젝트 수정
        elif params["req_approval_type"] == constants.COMM_APPRO_CD_PROJ_MODIFY:
            dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
            query = sProjMana.sGetJobTitleCdObj(
                params["contents"]["cons_code"], loginUserInfo["id"]
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "sGetJobTitleCdObj Query : " + query,
            )
            resCd, msg, jobResData = dbms.queryForObject(query)
            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + msg,
                )

                result = commServ.makeReturnMessage(resCd, msg, resData)
                return result
            resCd, msg, resData = regProjModify(loginUserInfo, params)
            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + msg,
                )

                result = commServ.makeReturnMessage(resCd, msg, resData)
                return result

            # 본사 관리자 검색
            searchList = []

            searchInfo = {"key": "CO_CODE", "value": loginUserInfo["co_code"]}
            searchList.append(searchInfo)

            searchInfo = {"key": "MANAGER_TYPE", "value": "Y"}
            searchList.append(searchInfo)

            resCd, msg, managerUserInfo = servUserMana.searchUserInfoList(searchList)
            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + msg,
                )

                result = commServ.makeReturnMessage(resCd, msg, resData)
                return result

            # 프로젝트 추가 데이터 생성
            common_approval_manage = {
                "req_approval_id": loginUserInfo["id"],
                "req_approval_type": constants.COMM_APPRO_CD_PROJ_MODIFY,
                "approval_status": constants.APPRO_STATUS_CD_WAIT,
                "contents": resData,
                "approval_id": "",
                "req_approval_date": util_time.get_current_time(
                    util_time.TIME_CURRENT_TYPE_14
                ),
                "complete_approval_date": "",
                "next_approval_info": "",
            }

            if (
                loginUserInfo["authority_code"] == constants.USER_MONITOR
                and loginUserInfo["manager_type"] == "Y"
            ):  # 감리자 본사 관리자이기 때문에 바로 프로젝트 생성을 할 수 있슴
                resCd, msg, resData = approvalProjModify(common_approval_manage)
                if resCd != 0:
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Database Error : " + msg,
                    )

                    result = commServ.makeReturnMessage(resCd, msg, resData)
                    return result

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
                    "---------- 프로젝트 수정 완료 ----------",
                )
                return result
            elif (
                loginUserInfo["authority_code"] == constants.USER_MONITOR
                and loginUserInfo["manager_type"] != "Y"
            ):  # 감리자 본사 모니터링으로 프로젝트 생성 승인을 받아야 함.
                common_approval_manage["approval_id"] = managerUserInfo[0]["id"]
                ##########################################################################################################
            else:
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "프로젝트 수정 요청 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "response : " + commUtilServ.jsonDumps(result),
                )
                return result

        # 프로젝트 삭제
        elif params["req_approval_type"] == constants.COMM_APPRO_CD_PROJ_DELETE:

            # 본사 관리자 검색
            searchList = []

            searchInfo = {"key": "CO_CODE", "value": loginUserInfo["co_code"]}
            searchList.append(searchInfo)

            searchInfo = {"key": "MANAGER_TYPE", "value": "Y"}
            searchList.append(searchInfo)

            resCd, msg, managerUserInfo = servUserMana.searchUserInfoList(searchList)
            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + msg,
                )

                result = commServ.makeReturnMessage(resCd, msg, resData)
                return result
            # resCd, msg, resData = regProjDelete(loginUserInfo, params)

            # if(resCd != 0):
            # 	logs.war(procName,
            # 			os.path.basename(__file__),
            # 			sys._getframe(0).f_code.co_name,
            # 			u'Database Error : ' + msg)

            # 	result = commServ.makeReturnMessage(resCd, msg, resData)
            # 	return result

            # 프로젝트 삭제 데이터 생성
            common_approval_manage = {
                "req_approval_id": loginUserInfo["id"],
                "req_approval_type": constants.COMM_APPRO_CD_PROJ_DELETE,
                "approval_status": constants.APPRO_STATUS_CD_WAIT,
                "contents": params["contents"],
                "approval_id": "",
                "req_approval_date": util_time.get_current_time(
                    util_time.TIME_CURRENT_TYPE_14
                ),
                "complete_approval_date": "",
                "next_approval_info": "",
            }

            if (
                loginUserInfo["authority_code"] == constants.USER_MONITOR
                and loginUserInfo["manager_type"] == "Y"
            ):  # 감리자 본사 관리자이기 때문에 바로 프로젝트 생성을 할 수 있슴
                resCd, msg, resData = approvalProjDelete(common_approval_manage)
                if resCd != 0:
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Database Error : " + msg,
                    )

                    result = commServ.makeReturnMessage(resCd, msg, resData)
                    return result

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
                    "---------- 프로젝트 수정 완료 ----------",
                )
                return result
            elif (
                loginUserInfo["authority_code"] == constants.USER_MONITOR
                and loginUserInfo["manager_type"] != "Y"
            ):  # 감리자 본사 모니터링으로 프로젝트 생성 승인을 받아야 함.
                common_approval_manage["approval_id"] = managerUserInfo[0]["id"]
                ##########################################################################################################
            else:
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "프로젝트 삭제 요청 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "response : " + commUtilServ.jsonDumps(result),
                )
                return result

        # 회사 정보 수정
        elif params["req_approval_type"] == constants.COMM_APPRO_CD_CO_MODIFY:
            resCd, msg, resData = regCoModify(loginUserInfo, params, request)

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "-------------------------------- 1 : "
                + commUtilServ.jsonDumps(resData),
            )
            # 본사 관리자 검색
            searchList = []

            searchInfo = {"key": "CO_CODE", "value": loginUserInfo["co_code"]}
            searchList.append(searchInfo)

            searchInfo = {"key": "MANAGER_TYPE", "value": "Y"}
            searchList.append(searchInfo)
            resCd, msg, managerUserInfo = servUserMana.searchUserInfoList(searchList)
            if resCd != 0:
                return resCd, msg, None
            # 프로젝트 추가 데이터 생성
            common_approval_manage = {
                "req_approval_id": loginUserInfo["id"],
                "req_approval_type": constants.COMM_APPRO_CD_CO_MODIFY,
                "approval_status": constants.APPRO_STATUS_CD_WAIT,
                "contents": resData,
                "approval_id": "",
                "req_approval_date": util_time.get_current_time(
                    util_time.TIME_CURRENT_TYPE_14
                ),
                "complete_approval_date": "",
                "next_approval_info": "",
            }

            if (
                loginUserInfo["authority_code"] == constants.USER_MONITOR
                and loginUserInfo["manager_type"] == "Y"
            ) or (
                loginUserInfo["authority_code"] == constants.USER_BUYER
                and loginUserInfo["manager_type"] == "Y"
            ):  # 감리자 본사 관리자이기 때문에 바로 회사 정보를 수정할 수 있슴
                resCd, msg, resData = approvalCoModify(common_approval_manage)
                if resCd != 0:
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Database Error : " + msg,
                    )

                    result = commServ.makeReturnMessage(resCd, msg, resData)
                    return result

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
                    "---------- 회사 정보 수정 완료 ----------",
                )
                return result
            elif (
                loginUserInfo["authority_code"] == constants.USER_MONITOR
                and loginUserInfo["manager_type"] != "Y"
            ) or (
                loginUserInfo["authority_code"] == constants.USER_BUYER
                and loginUserInfo["manager_type"] != "Y"
            ):  # 감리자 본사 모니터링으로 회사 정보 수정 승인을 받아야 함.
                # 			elif(loginUserInfo['authority_code'] == constants.USER_MONITOR and loginUserInfo['manager_type'] != 'Y'): #
                common_approval_manage["approval_id"] = managerUserInfo[0]["id"]
                ##########################################################################################################
            else:
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "회사정보 수정 요청 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "response : " + commUtilServ.jsonDumps(result),
                )
                return result

        # 프로젝트 중지
        elif params["req_approval_type"] == constants.COMM_APPRO_CD_PROJ_STOP:
            resCd, msg, resData = regProjStop(loginUserInfo, params)

            # 본사 관리자 검색
            searchList = []

            searchInfo = {"key": "CO_CODE", "value": loginUserInfo["co_code"]}
            searchList.append(searchInfo)

            searchInfo = {"key": "MANAGER_TYPE", "value": "Y"}
            searchList.append(searchInfo)
            resCd, msg, managerUserInfo = servUserMana.searchUserInfoList(searchList)
            if resCd != 0:
                return resCd, msg, None
            # 프로젝트 추가 데이터 생성
            common_approval_manage = {
                "req_approval_id": loginUserInfo["id"],
                "req_approval_type": constants.COMM_APPRO_CD_PROJ_STOP,
                "approval_status": constants.APPRO_STATUS_CD_WAIT,
                "contents": resData,
                "approval_id": "",
                "req_approval_date": util_time.get_current_time(
                    util_time.TIME_CURRENT_TYPE_14
                ),
                "complete_approval_date": "",
                "next_approval_info": "",
            }

            if (
                loginUserInfo["authority_code"] == constants.USER_MONITOR
                and loginUserInfo["manager_type"] == "Y"
            ):  # 본사 관리자이기 때문에 바로 프로젝트를 중지 할 수 있다.
                resCd, msg, resData = approvalProjStop(common_approval_manage)
                if resCd != 0:
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Database Error : " + msg,
                    )

                    result = commServ.makeReturnMessage(resCd, msg, resData)
                    return result

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
                    "---------- 회사 정보 수정 완료 ----------",
                )
                return result
            elif (
                loginUserInfo["authority_code"] == constants.USER_MONITOR
                and loginUserInfo["manager_type"] != "Y"
            ):  # 감리자 본사 모니터링으로 회사 정보 수정 승인을 받아야 함.
                common_approval_manage["approval_id"] = managerUserInfo[0]["id"]
                ##########################################################################################################
            else:
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "프로젝트 중지 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "response : " + commUtilServ.jsonDumps(result),
                )
                return result

        # 프로젝트 재시작
        elif params["req_approval_type"] == constants.COMM_APPRO_CD_PROJ_RESTART:
            resCd, msg, resData = regProjRestart(loginUserInfo, params)

            # 본사 관리자 검색
            searchList = []

            searchInfo = {"key": "CO_CODE", "value": loginUserInfo["co_code"]}
            searchList.append(searchInfo)

            searchInfo = {"key": "MANAGER_TYPE", "value": "Y"}
            searchList.append(searchInfo)
            resCd, msg, managerUserInfo = servUserMana.searchUserInfoList(searchList)
            if resCd != 0:
                return resCd, msg, None
            # 프로젝트 추가 데이터 생성
            common_approval_manage = {
                "req_approval_id": loginUserInfo["id"],
                "req_approval_type": constants.COMM_APPRO_CD_PROJ_RESTART,
                "approval_status": constants.APPRO_STATUS_CD_WAIT,
                "contents": resData,
                "approval_id": "",
                "req_approval_date": util_time.get_current_time(
                    util_time.TIME_CURRENT_TYPE_14
                ),
                "complete_approval_date": "",
                "next_approval_info": "",
            }

            if (
                loginUserInfo["authority_code"] == constants.USER_MONITOR
                and loginUserInfo["manager_type"] == "Y"
            ):  # 본사 관리자이기 때문에 바로 프로젝트를 재시작 할 수 있다.
                resCd, msg, resData = approvalProjRestart(common_approval_manage)
                if resCd != 0:
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Database Error : " + msg,
                    )

                    result = commServ.makeReturnMessage(resCd, msg, resData)
                    return result

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
                    "---------- 회사 정보 수정 완료 ----------",
                )
                return result
            elif (
                loginUserInfo["authority_code"] == constants.USER_MONITOR
                and loginUserInfo["manager_type"] != "Y"
            ):  # 감리자 본사 모니터링으로 회사 정보 수정 승인을 받아야 함.
                common_approval_manage["approval_id"] = managerUserInfo[0]["id"]
                ##########################################################################################################
            else:
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "프로젝트 중지 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "response : " + commUtilServ.jsonDumps(result),
                )
                return result

        # 		elif(params['req_approval_type'] == constants.COMM_APPRO_CD_SIGNUP):
        # 			resCd, msg, resData = regSignup(params['contents'])

        # 			if(resCd != 0):
        # 				logs.war(procName,
        # 						os.path.basename(__file__),
        # 						sys._getframe(0).f_code.co_name,
        # 						u'Database Error : ' + msg)

        # 				result = commServ.makeReturnMessage(resCd, msg, resData)
        # 				return result

        ##########################################################################################################
        # 회사 생성 승인을 위한 데이터 생성
        # 			common_approval_manage = {
        # 				'req_approval_id' : loginUserInfo['id'],
        # 				'req_approval_type' : constants.COMM_APPRO_CD_MANAGE,
        # 				'approval_status' : constants.APPRO_STATUS_CD_WAIT,
        # 				'contents' : resData,
        # 				'approval_id' : resData['approval_id'],
        # 				'req_approval_date' : util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
        # 				'complete_approval_date' : ''
        # 	        }
        ##########################################################################################################
        # 공통 승인 결재 정보를 저장 한다.
        resCd, msg, resData = servCommApproMana.putCommonApprovalInfo(
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
                constants.REST_RESPONSE_CODE_DATAFAIL, "결제 요청 정보를 등록 할 수 없습니다. ", None
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
            "---------- 결재 요청 정보 등록 완료 ----------",
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


def regCompany(coInfo, req):

    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servCommMana = servCommManage()
    dataCompanyMana = dataCompanyManage()

    servCompanyMana = servCompanyManage()
    ##########################################################################################################
    # 회사 정보 관리
    data_co_info_manage = dataCompanyMana.makeReqCompanyInfoModel()
    # 1. 재직 여부를 확인 한다.
    # 	if(coInfo['employ_status'] != constants.EMPLOY_STATUS_CD_N):
    searchList = []

    searchInfo = {"key": "CO_REGISNUM", "value": coInfo["co_regisnum"]}

    searchList.append(searchInfo)
    # 등록된 회사 정보가 있는지 확인 한다.
    resCd, msg, resCoInfo = servUserMana.getCoInfo(searchList)
    if resCd != 0:  # DB 에러 발생 시
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Database Error : " + commUtilServ.jsonDumps(msg),
        )
        return resCd, msg, None

    # 등록된 회사 정보가 없으면 회사 정보를 저장 데이터와 결재 정보 데이터를 생성 한다.
    if resCoInfo == None:
        resCd, msg, coNum = servCommMana.createCoNum()
        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + msg,
            )
            return resCd, msg, None

        resCd, msg, nextCoNum = servCommMana.increaseCoNum()
        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + msg,
            )

            return resCd, msg, None

        data_co_info_manage["co_code"] = coCode + str(f"{coNum:06d}")
        data_co_info_manage["co_name"] = coInfo["co_name"]
        data_co_info_manage["co_type"] = coInfo["co_type"]
        data_co_info_manage["co_ceo"] = coInfo["co_ceo"]
        data_co_info_manage["co_contact"] = coInfo["co_contact"]
        data_co_info_manage["co_address"] = coInfo["co_address"]
        data_co_info_manage["co_regisnum"] = coInfo["co_regisnum"]
        # data_co_info_manage['regisnum'] = coInfo['regisnum']

        # if(coInfo['co_regisnum'] != '' and coInfo['co_license_name'] != ''):
        # 	lpath, origName, changeName = servCompanyMana.companyFileNameManage(data_co_info_manage['co_code'], coInfo, 'co_license_name')
        # 	data_co_info_manage['co_license_path'] = lpath
        # 	data_co_info_manage['co_license_original_name'] = origName
        # 	data_co_info_manage['co_license_change_name'] = changeName
        # else:
        # 	return constants.REST_RESPONSE_CODE_DATAFAIL, u'사업자 등록 번호 또는 사업자 등록증이 누락 되었습니다.', None

        # if(coInfo['regisnum'] != '' and coInfo['bs_license_name'] != ''):
        # 		lpath, origName, changeName = servCompanyMana.companyFileNameManage(data_co_info_manage['co_code'], coInfo, 'bs_license_name')

        # 		data_co_info_manage['bs_license_path'] = lpath
        # 		data_co_info_manage['bs_license_original_name'] = origName
        # 		data_co_info_manage['bs_license_change_name'] = changeName

    else:  # 회사가 등록 되어 있는 경우
        return (
            constants.REST_RESPONSE_CODE_DATAFAIL,
            "입력하신 회사는 이미 등록되어 있습니다.",
            resCoInfo,
        )

        ##########################################################################################################
        # 회사 정보를 저장 한다.
    if data_co_info_manage["co_regisnum"] != "":
        resCd, msg, resData = servCompanyMana.post_company(data_co_info_manage)
        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + msg,
            )

            return resCd, "회사 정보를 등록 할 수 없습니다. 원인 : " + msg, None

            # 사업자 등록증 파일을 저장 한다.
            # try:
            # if(data_co_info_manage['co_license_path'] != ''):
            # 	f_co_license = req.files['f_co_license']
            # 	commServ.createDir(data_co_info_manage['co_license_path'])
            # 	commServ.saveFile(f_co_license, data_co_info_manage['co_license_path'], data_co_info_manage['co_license_change_name'])
            # except:
            # 	servCompanyMana.delCompanyInfo(data_co_info_manage['co_regisnum'])
            # 	return constants.REST_RESPONSE_CODE_DATAFAIL, u'회사 정보를 등록 할 수 없습니다. 관리자에게 문의 하세요.', None

        # 공사업 등록증 파일을 저장 한다.
        # try:
        # 	if(data_co_info_manage['bs_license_path'] != ''):
        # 		f_bs_license = req.files['f_bs_license']

        # 		commServ.createDir(data_co_info_manage['bs_license_path'])
        # 		commServ.saveFile(f_bs_license, data_co_info_manage['bs_license_path'], data_co_info_manage['bs_license_change_name'])
        # except:
        # 	if(data_co_info_manage['co_license_path'] != ''):
        # 		commServ.removeFile(data_co_info_manage['co_license_path'], data_co_info_manage['co_license_change_name'])
        # 		servCompanyMana.delete_company(data_co_info_manage['co_regisnum'])  # 회사 정보를 삭제 한다.
        # 		return constants.REST_RESPONSE_CODE_DATAFAIL, u'회사 정보를 등록 할 수 없습니다. 관리자에게 문의 하세요.', None
        ##########################################################################################################

    return constants.REST_RESPONSE_CODE_ZERO, "", data_co_info_manage


def regManage(reqDataInfo):

    # commServ        = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servCommMana = servCommManage()
    # dataCompanyMana = dataCompanyManage()

    # servCompanyMana = servCompanyManage()

    data_auth_info_manage = {
        "req_manage_type": "",
        "req_manage_type_name": "",
        "req_approval_id": "",
        "req_approval_name": "",
        "req_approval_regisnum": "",
        "req_approval_authority_code": "",
        "req_approval_authority_name": "",
        "req_approval_user_position": "",
        "req_approval_user_contact": "",
        "req_approval_user_email": "",
        "approval_id": "",
        "approval_name": "",
    }

    data_auth_info_manage["req_manage_type"] = reqDataInfo["req_manage_type"]
    data_auth_info_manage["req_approval_id"] = reqDataInfo["req_approval_id"]
    data_auth_info_manage["approval_id"] = reqDataInfo["approval_id"]

    resCd, msg, resData = servCommMana.getCodeName(reqDataInfo["req_manage_type"])
    if resCd != 0:
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Database Error : " + commUtilServ.jsonDumps(msg),
        )

        return resCd, msg, None
    data_auth_info_manage["req_manage_type_name"] = resData["subcode_name"]

    resCd, msg, resData = servUserMana.getUserInfo(
        1, reqDataInfo["req_approval_id"], None
    )
    if resCd != 0:
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Database Error : " + commUtilServ.jsonDumps(msg),
        )

        return resCd, msg, None

    data_auth_info_manage["req_approval_name"] = resData["user_name"]
    # data_auth_info_manage['req_approval_regisnum']			= resData['user_regisnum']
    data_auth_info_manage["req_approval_authority_code"] = resData["authority_code"]
    data_auth_info_manage["req_approval_authority_name"] = resData["authority_name"]
    data_auth_info_manage["req_approval_user_position"] = resData["user_position"]
    data_auth_info_manage["req_approval_user_contact"] = resData["user_contact"]
    data_auth_info_manage["req_approval_user_email"] = resData["user_email"]

    resCd, msg, resData = servUserMana.getUserInfo(1, reqDataInfo["approval_id"], None)
    if resCd != 0:
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Database Error : " + commUtilServ.jsonDumps(msg),
        )

        return resCd, msg, None
    data_auth_info_manage["approval_name"] = resData["user_name"]

    return constants.REST_RESPONSE_CODE_ZERO, "", data_auth_info_manage


# 사용자 회사 초대
def regInvite(requesterInfo, respondentId):

    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servCommMana = servCommManage()

    # 초대 받을 사람의 정보를 가져 온다.
    resCd, msg, respondentInfo = servUserMana.getUserInfo(1, respondentId, None)
    if resCd != 0:
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Database Error : " + commUtilServ.jsonDumps(msg),
        )

        return resCd, msg, None

    if respondentInfo == None:
        return (
            constants.REST_RESPONSE_CODE_DATAFAIL,
            "초대하고자 하는 사용자의 정보를 찾을 수 없습니다.",
            None,
        )

    # 초대 데이터를 생성 한다.

    data_info_manage = {
        "requester_id": requesterInfo["id"],
        "requester_name": requesterInfo["user_name"],
        "requester_position": requesterInfo["user_position"],
        "requester_contact": requesterInfo["user_contact"],
        "requester_email": requesterInfo["user_email"],
        "requester_co_code": requesterInfo["co_code"],
        "requester_co_name": requesterInfo["co_name"],
        "requester_co_type": requesterInfo["co_type"],
        "requester_co_ceo": requesterInfo["co_ceo"],
        "requester_co_contact": requesterInfo["co_contact"],
        "requester_co_address": requesterInfo["co_address"],
        "respondent_id": respondentInfo["id"],
        "respondent_name": respondentInfo["user_name"],
        "respondent_position": respondentInfo["user_position"],
        "respondent_contact": respondentInfo["user_contact"],
        "respondent_email": respondentInfo["user_email"],
        "respondent_employ_status": respondentInfo["employ_status"],
        "respondent_co_code": respondentInfo["co_code"],
        "respondent_co_name": respondentInfo["co_name"],
        "respondent_co_type": respondentInfo["co_type"],
        "respondent_co_ceo": respondentInfo["co_ceo"],
        "respondent_co_contact": respondentInfo["co_contact"],
        "respondent_co_address": respondentInfo["co_address"],
    }

    return constants.REST_RESPONSE_CODE_ZERO, "", data_info_manage


# 관리자의 회사 직원 퇴사
def regLeave(requesterInfo, respondentId):

    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servCommMana = servCommManage()

    # 초대 받을 사람의 정보를 가져 온다.
    resCd, msg, respondentInfo = servUserMana.getUserInfo(1, respondentId, None)
    if resCd != 0:
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Database Error : " + commUtilServ.jsonDumps(msg),
        )

        return resCd, msg, None

    if respondentInfo == None:
        return (
            constants.REST_RESPONSE_CODE_DATAFAIL,
            "퇴사 시키고자 하는 사용자의 정보를 찾을 수 없습니다.",
            None,
        )

    # 초대 데이터를 생성 한다.

    data_info_manage = {
        "requester_id": requesterInfo["id"],
        "requester_name": requesterInfo["user_name"],
        "requester_position": requesterInfo["user_position"],
        "requester_contact": requesterInfo["user_contact"],
        "requester_email": requesterInfo["user_email"],
        "requester_co_code": requesterInfo["co_code"],
        "requester_co_name": requesterInfo["co_name"],
        "requester_co_type": requesterInfo["co_type"],
        "requester_co_ceo": requesterInfo["co_ceo"],
        "requester_co_contact": requesterInfo["co_contact"],
        "requester_co_address": requesterInfo["co_address"],
        "respondent_id": respondentInfo["id"],
        "respondent_name": respondentInfo["user_name"],
        "respondent_position": respondentInfo["user_position"],
        "respondent_contact": respondentInfo["user_contact"],
        "respondent_email": respondentInfo["user_email"],
        "respondent_employ_status": respondentInfo["employ_status"],
        "respondent_co_code": respondentInfo["co_code"],
        "respondent_co_name": respondentInfo["co_name"],
        "respondent_co_type": respondentInfo["co_type"],
        "respondent_co_ceo": respondentInfo["co_ceo"],
        "respondent_co_contact": respondentInfo["co_contact"],
        "respondent_co_address": respondentInfo["co_address"],
        "inviteType": "N",
    }

    return constants.REST_RESPONSE_CODE_ZERO, "", data_info_manage


# 회원 초대 승인
def approvalInvite(commApproData):
    servUserMana = servUserManage()
    # 1.재직 정보 및 회사 정보를 변경 한다.
    updateUserInfoSignup = []

    updateUserInfo = {
        "key": "CO_APPRO_DATE",
        "value": util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
    }
    updateUserInfoSignup.append(updateUserInfo)

    updateUserInfo = {"key": "EMPLOY_STATUS", "value": constants.EMPLOY_STATUS_CD_Y}
    updateUserInfoSignup.append(updateUserInfo)

    updateUserInfo = {"key": "USER_STATE", "value": constants.APPRO_STATUS_CD_APPRO}
    updateUserInfoSignup.append(updateUserInfo)

    updateUserInfo = {
        "key": "CO_CODE",
        "value": commApproData["contents"]["requester_co_code"],
    }
    updateUserInfoSignup.append(updateUserInfo)

    return servUserMana.updateUserCoInfo(
        commApproData["approval_id"], updateUserInfoSignup
    )


# 회원 탈퇴
def regWithDraw(commApproData, inviteType):
    servUserMana = servUserManage()
    servCommApproMana = servCommonApprovalManage()

    resCd, msg, userInfo = servUserMana.getUserInfo(
        1, commApproData["contents"]["respondent_id"], None
    )
    if resCd != 0:
        return resCd, msg, None

    data_withdraw_co_info_manage = {
        "userId": commApproData["contents"]["respondent_id"],
        "userName": commApproData["contents"]["respondent_name"],
        "userRegisnum": userInfo["user_regisnum"],
        "userContact": userInfo["user_contact"],
        "userEmail": userInfo["user_email"],
        "beforeCoCode": commApproData["contents"]["respondent_co_code"],
        "beforeCoName": commApproData["contents"]["respondent_co_name"],
        "afterCoCode": "",
        "afterCoName": "",
        "inviteType": inviteType,
    }

    next_approval_info = ""

    if inviteType == "Y":
        data_withdraw_co_info_manage["afterCoCode"] = commApproData["contents"][
            "requester_co_code"
        ]

        next_approval_info = commApproData

    # 이전 회사 관리자 검색
    searchList = []

    searchInfo = {
        "key": "CO_CODE",
        "value": commApproData["contents"]["respondent_co_code"],
    }
    searchList.append(searchInfo)

    searchInfo = {"key": "MANAGER_TYPE", "value": "Y"}
    searchList.append(searchInfo)

    resCd, msg, managerOldUserInfo = servUserMana.searchUserInfoList(searchList)
    if resCd != 0:
        return resCd, msg, None

    common_approval_manage = {
        "req_approval_id": commApproData["contents"]["respondent_id"],
        "req_approval_type": constants.COMM_APPRO_CD_WITHDRAWAL,
        "approval_status": constants.APPRO_STATUS_CD_WAIT,
        "contents": data_withdraw_co_info_manage,
        "approval_id": managerOldUserInfo[0]["id"],
        "req_approval_date": util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
        "complete_approval_date": "",
        "next_approval_info": next_approval_info,
    }

    return servCommApproMana.putCommonApprovalInfo(common_approval_manage)


# 회원 탈퇴 승인
def approvalWithDraw(userId, commApproData):

    servUserMana = servUserManage()
    updateUserInfoWithdrawal = []

    # 	if(commApproData['contents']['inviteType'] == 'Y'):		# 다른 회사 입사 초대로 인한 탈퇴 승인 처리
    updateUserInfo = {"key": "MANAGER_TYPE", "value": ""}
    updateUserInfoWithdrawal.append(updateUserInfo)

    # 	updateUserInfo = {
    # 		'key' : 'AUTHORITY_CODE',
    # 		'value' : constants.USER_AUTH_INOCCUPATION
    # 	}
    # 	updateUserInfoWithdrawal.append(updateUserInfo)

    updateUserInfo = {
        "key": "CO_CODE",
        "value": commApproData["contents"]["afterCoCode"],
    }
    updateUserInfoWithdrawal.append(updateUserInfo)

    updateUserInfo = {
        "key": "CO_APPRO_DATE",
        "value": util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
    }
    updateUserInfoWithdrawal.append(updateUserInfo)

    updateUserInfo = {"key": "AUTHORITY_CODE", "value": constants.USER_INOCCUPATION}
    updateUserInfoWithdrawal.append(updateUserInfo)

    updateUserInfo = {
        "key": "USER_POSITION",
        "value": "",
    }
    updateUserInfoWithdrawal.append(updateUserInfo)
    # 	else:
    # 		updateUserInfo = {
    # 			'key' : 'MANAGER_TYPE',
    # 			'value' : ''
    # 		}
    # 		updateUserInfoWithdrawal.append(updateUserInfo)
    #
    # 	#	updateUserInfo = {
    # 	#		'key' : 'AUTHORITY_CODE',
    # 	#		'value' : constants.USER_AUTH_INOCCUPATION
    # 	#	}
    # 	#	updateUserInfoWithdrawal.append(updateUserInfo)
    #
    # 		updateUserInfo = {
    # 			'key' : 'CO_CODE',
    # 			'value' : ''
    # 		}
    # 		updateUserInfoWithdrawal.append(updateUserInfo)
    #
    # 		updateUserInfo = {
    # 			'key' : 'EMPLOY_STATUS',
    # 			'value' : constants.EMPLOY_STATUS_CD_N
    # 		}
    # 		updateUserInfoWithdrawal.append(updateUserInfo)
    #
    # 		updateUserInfo = {
    # 			'key' : 'CO_APPRO_DATE',
    # 			'value' : '',
    # 		}
    # 		updateUserInfoWithdrawal.append(updateUserInfo)

    # 	#return servUserMana.updateUserCoInfo(commApproData['req_approval_id'], updateUserInfoWithdrawal)
    return servUserMana.updateUserCoInfo(userId, updateUserInfoWithdrawal)


# 프로젝트 생성
def regProjNew(loginUserInfo, params):

    contentsData = params["contents"]

    # 	servUserMana    = servUserManage()
    # 	servCommMana    = servCommManage()

    # 	if(contentsData['supervInfo']['reside_class_code'] != ['']):
    # 		resCd, msg, resData = servCommMana.getCodeName(contentsData['supervInfo']['reside_class_code'])
    # 		if(resCd != 0):
    # 			return resCd, msg, resData

    # 		contentsData['supervInfo']['reside_class_name'] = resData['subcode_name']

    co_data = {"co_code": loginUserInfo["co_code"], "co_name": loginUserInfo["co_name"]}
    contentsData["coInfo"] = co_data

    # 	for n in range(0, len(contentsData['supervisorsList'])):
    #
    # 		if(contentsData['supervisorsList'][n]['id'] != ''):
    # 			resCd, msg, resData = servUserMana.getUserInfo(1, contentsData['supervisorsList'][n]['id'], None)
    # 			if(resCd != 0):
    # 				return resCd, msg, resData
    #
    # 			contentsData['supervisorsList'][n]['user_name'] = resData['user_name']
    #
    # 		if(contentsData['supervisorsList'][n]['job_title_code'] != ['']):
    # 			resCd, msg, resData = servCommMana.getCodeName(contentsData['supervisorsList'][n]['job_title_code'])
    # 			if(resCd != 0):
    # 				return resCd, msg, resData
    #
    # 			contentsData['supervisorsList'][n]['job_title_name'] = resData['subcode_name']
    #
    # 		if(contentsData['supervisorsList'][n]['authority_code'] != ['']):
    # 			resCd, msg, resData = servCommMana.getCodeName(contentsData['supervisorsList'][n]['authority_code'])
    # 			if(resCd != 0):
    # 				return resCd, msg, resData
    #
    # 			contentsData['supervisorsList'][n]['authority_name'] = resData['subcode_name']
    #
    # 	#return contentsData
    return constants.REST_RESPONSE_CODE_ZERO, "", contentsData


# 프로젝트 생성 승인
def approvalProjNew(commApproData):
    servCommMana = servCommManage()
    servProjMana = servProjectManage()

    # 프로젝트 코드를 생성 한다.
    resCd, msg, resData = servCommMana.createProjNum()

    newProjectCd = "P" + str(f"{resData:011d}")

    # 프로젝트 정보를 생성 한다.
    resCd, msg, resData = servProjMana.putProject(
        newProjectCd,
        commApproData["contents"]["projectName"],
        commApproData["contents"]["coInfo"]["co_code"],
    )

    if resCd != 0:
        return resCd, msg, None

    # 프로젝트 기본 정보를 저장 한다.
    commApproData["contents"]["cons_code"] = newProjectCd
    resCd, msg, resData = servProjMana.updateProjDefaultInfo(
        commApproData["contents"]["cons_code"],
        commApproData["contents"]["projectInfo"],
        "A",
    )
    if resCd != 0:
        servProjMana.delProject(newProjectCd)
        return resCd, msg, None

    # 감리 기본 정보를 저장 한다.
    # resCd, msg, resData = servProjMana.updateSupvDefaultInfo(commApproData['contents']['cons_code'], commApproData['contents']['supervInfo'], 'A')
    # if(resCd != 0):
    # 		servProjMana.delProject(newProjectCd)
    # 		return resCd, msg, None

    # 감리원 인력 리스트를 저장 한다.
    resCd, msg, resData = servProjMana.putJoinWorkforce(
        commApproData["contents"]["cons_code"],
        commApproData["contents"]["joinUserList"],
    )
    # if(resCd != 0):
    # 	servProjMana.delJoinWorkforce(newProjectCd, commApproData['contents']['supervisorsList'])
    # 	servProjMana.delProject(newProjectCd)
    # 	logs.debug(procName,
    # 			os.path.basename(__file__),
    # 			sys._getframe(0).f_code.co_name,
    # 			"실행")
    # 	return resCd, msg, None

    # 감리 문서를 저장 한다.
    # resCd, msg, resData = servCommMana.getCodeList('SD00')

    # if(resCd != 0):
    # 	servProjMana.delJoinWorkforce(newProjectCd, commApproData['contents']['supervisorsList'])
    # 	servProjMana.delProject(newProjectCd)
    # 	return resCd, msg, None

    # resCd, msg, resData = servProjMana.putDocNumManage(commApproData['contents']['cons_code'], commApproData['contents']['supervInfo']['superv_co_code'], resData)
    # if(resCd != 0):
    # 		servProjMana.delDocNumManage(commApproData['contents']['cons_code'], commApproData['contents']['supervInfo']['superv_co_code'])
    # 		servProjMana.delJoinWorkforce(newProjectCd, commApproData['contents']['supervisorsList'])
    # 		servProjMana.delProject(newProjectCd)
    # 		return resCd, msg, None

    return constants.REST_RESPONSE_CODE_ZERO, "", None


# 프로젝트 수정
def regProjModify(loginUserInfo, params):
    contentsData = params["contents"]

    servProjMana = servProjectManage()
    servUserMana = servUserManage()
    servCommMana = servCommManage()

    # 오래된 프로젝트 기본 정보를 가져 온다.
    resCd, msg, oldProjInfo = servProjMana.getProjDefaultInfo(contentsData["cons_code"])
    if resCd != 0:
        return resCd, msg, None
    # if(contentsData['modifyType'] == 'supervInfo'):
    # 	# 수정된 내용에 대한 코드 정보를 가져온다.
    # 	if(contentsData['supervInfo']['reside_class_code'] != ''):
    # 		resCd, msg, resData = servCommMana.getCodeName(contentsData['supervInfo']['reside_class_code'])
    # 		if(resCd != 0):
    # 			return resCd, msg, resData
    #
    # 			contentsData['supervInfo']['reside_class_name'] = resData['subcode_name']
    # 		else:
    # 			contentsData['supervInfo']['reside_class_code'] = ''
    # 			contentsData['supervInfo']['reside_class_name'] = ''

    # 		contentsData['supervInfo']['superv_co_code'] = loginUserInfo['co_code']
    # 		contentsData['supervInfo']['superv_co_name'] = loginUserInfo['co_name']

    co_data = {"co_code": loginUserInfo["co_code"], "co_name": loginUserInfo["co_name"]}
    contentsData["coInfo"] = co_data

    returnData = {}

    if contentsData["modifyType"] == "projectInfo":
        # 데이터 구조를 생성 한다.
        returnData = {
            "cons_code": contentsData["cons_code"],
            "modifyType": contentsData["modifyType"],
            "projectInfo": {
                "old": {
                    "cons_name": oldProjInfo["cons_name"],
                    "location": oldProjInfo["location"],
                    "cons_type": oldProjInfo["cons_type"],
                    "purpose": oldProjInfo["purpose"],
                    "building_name": oldProjInfo["building_name"],
                    "location_contact": oldProjInfo["location_contact"],
                    "business_outline": oldProjInfo["business_outline"],
                    "go_price": oldProjInfo["go_price"],
                    "design_price": oldProjInfo["design_price"],
                    "structure": oldProjInfo["structure"],
                    "ground": oldProjInfo["ground"],
                    "underground": oldProjInfo["underground"],
                    "main_building": oldProjInfo["main_building"],
                    "sub_building": oldProjInfo["sub_building"],
                    "households": oldProjInfo["households"],
                    "site_area": oldProjInfo["site_area"],
                    "building_area": oldProjInfo["building_area"],
                    "total_area": oldProjInfo["total_area"],
                    "floor_area": oldProjInfo["floor_area"],
                    "add_info": oldProjInfo["add_info"],
                    "cons_start_date": oldProjInfo["cons_start_date"],
                    "cons_end_date": oldProjInfo["cons_end_date"],
                },
                "modify": contentsData["projectInfo"],
            },
        }
    elif contentsData["modifyType"] == "joinUserList":
        resCd, msg, oldJoinWorkforceInfoList = servProjMana.getJoinWorkforceInfo(
            contentsData["cons_code"], None
        )
        if resCd != 0:
            return resCd, msg, None

        returnData = {
            "cons_code": contentsData["cons_code"],
            "modifyType": contentsData["modifyType"],
            "joinUserList": {
                "old": oldJoinWorkforceInfoList,
                "modify": contentsData["joinUserList"],
            },
        }

    else:
        return constants.REST_RESPONSE_CODE_DATAFAIL, "수정 타입이 잘못 입력 되었습니다.", None

    # 오래된 공사 참여자 정보를 가져 온다.
    # 	jobList = [constants.JOB_TITLE_CD_SUPERVISING_MAIN, constants.JOB_TITLE_CD_SUPERVISING_SUB, constants.JOB_TITLE_CD_SUPERVISOR_MONITOR]
    # 	resCd, msg, oldJoinWorkforceInfoList = servProjMana.getJoinWorkforceInfo(contentsData['cons_code'], jobList)
    # 	if(resCd != 0):
    # 		return resCd, msg, None
    #
    # 	oldSupervList = []
    #
    # 	for oldJoinWorkforceInfo in oldJoinWorkforceInfoList:
    # 		info = {
    # 			'id' : oldJoinWorkforceInfo['id'],
    # 			'user_name' : oldJoinWorkforceInfo['user_name'],
    # 			'authority_code' : oldJoinWorkforceInfo['authority_code'],
    # 			'authority_name' : oldJoinWorkforceInfo['authority_name'],
    # 			'job_title_code' : oldJoinWorkforceInfo['job_title_code'],
    # 			'job_title_name' : oldJoinWorkforceInfo['job_title_name']
    # 		}
    # 		oldSupervList.append(info)
    #
    # 	if(contentsData['modifyType'] == 'supervisorsList'):
    #
    # 		# 프로젝트 사용자 추가일 경우
    # 		for n in range(0, len(contentsData['supervisorsList']['add'])):
    #
    # 			if(contentsData['supervisorsList']['add'][n]['id'] != ''):
    # 				resCd, msg, resData = servUserMana.getUserInfo(1, contentsData['supervisorsList']['add'][n]['id'], None)
    # 				if(resCd != 0):
    # 					return resCd, msg, resData
    #
    # 				contentsData['supervisorsList']['add'][n]['user_name'] = resData['user_name']
    #
    # 			if(contentsData['supervisorsList']['add'][n]['job_title_code'] != ''):
    # 				resCd, msg, resData = servCommMana.getCodeName(contentsData['supervisorsList']['add'][n]['job_title_code'])
    # 				if(resCd != 0):
    # 					return resCd, msg, resData

    # 				contentsData['supervisorsList']['add'][n]['job_title_name'] = resData['subcode_name']

    # 			if(contentsData['supervisorsList']['add'][n]['authority_code'] != ''):
    # 				resCd, msg, resData = servCommMana.getCodeName(contentsData['supervisorsList']['add'][n]['authority_code'])
    # 				if(resCd != 0):
    # 					return resCd, msg, resData

    # 				contentsData['supervisorsList']['add'][n]['authority_name'] = resData['subcode_name']

    # 프로젝트 사용자 수정일 경우
    # 		for n in range(0, len(contentsData['supervisorsList']['modify'])):

    # 			if(contentsData['supervisorsList']['modify'][n]['id'] != ''):
    # 				resCd, msg, resData = servUserMana.getUserInfo(1, contentsData['supervisorsList']['modify'][n]['id'], None)
    # 				if(resCd != 0):
    # 					return resCd, msg, resData

    # 				contentsData['supervisorsList']['modify'][n]['user_name'] = resData['user_name']

    # 			if(contentsData['supervisorsList']['modify'][n]['job_title_code'] != ''):
    # 				resCd, msg, resData = servCommMana.getCodeName(contentsData['supervisorsList']['modify'][n]['job_title_code'])
    # 				if(resCd != 0):
    # 					return resCd, msg, resData
    #
    # 				contentsData['supervisorsList']['modify'][n]['job_title_name'] = resData['subcode_name']

    # 			if(contentsData['supervisorsList']['modify'][n]['authority_code'] != ''):
    # 				resCd, msg, resData = servCommMana.getCodeName(contentsData['supervisorsList']['modify'][n]['authority_code'])
    # 				if(resCd != 0):
    # 					return resCd, msg, resData

    # 				contentsData['supervisorsList']['modify'][n]['authority_name'] = resData['subcode_name']

    # 프로젝트 사용자 삭제일 경우
    # 		for n in range(0, len(contentsData['supervisorsList']['del'])):
    #
    # 			if(contentsData['supervisorsList']['del'][n]['id'] != ''):
    # 				resCd, msg, resData = servUserMana.getUserInfo(1, contentsData['supervisorsList']['del'][n]['id'], None)
    # 				if(resCd != 0):
    # 					return resCd, msg, resData

    # 				contentsData['supervisorsList']['del'][n]['user_name'] = resData['user_name']

    # 			if(contentsData['supervisorsList']['del'][n]['job_title_code'] != ''):
    # 				resCd, msg, resData = servCommMana.getCodeName(contentsData['supervisorsList']['del'][n]['job_title_code'])
    # 				if(resCd != 0):
    # 					return resCd, msg, resData

    # 				contentsData['supervisorsList']['del'][n]['job_title_name'] = resData['subcode_name']

    # 			if(contentsData['supervisorsList']['del'][n]['authority_code'] != ''):
    # 				resCd, msg, resData = servCommMana.getCodeName(contentsData['supervisorsList']['del'][n]['authority_code'])
    # 				if(resCd != 0):
    # 					return resCd, msg, resData

    # 				contentsData['supervisorsList']['del'][n]['authority_name'] = resData['subcode_name']

    # 데이터 구조를 생성 한다.
    # 	returnData = {
    # 		'cons_code' : contentsData['cons_code'],
    # 		'modifyType' : contentsData['modifyType'],
    # 		'projectInfo' : {
    # 			'old' : {
    # 				'cons_name'			: oldProjInfo['cons_name'],
    # 				'location'			: oldProjInfo['location'],
    # 				'cons_type'			: oldProjInfo['cons_type'],
    # 				'purpose'			: oldProjInfo['purpose'],
    # 				'building_name'		: oldProjInfo['building_name'],
    # 				'location_contact'	: oldProjInfo['location_contact'],
    # 				'business_outline'	: oldProjInfo['business_outline'],
    # 				'go_price'			: oldProjInfo['go_price'],
    # 				'design_price'		: oldProjInfo['design_price'],
    # 				'structure'			: oldProjInfo['structure'],
    # 				'ground'			: oldProjInfo['ground'],
    # 				'underground'		: oldProjInfo['underground'],
    # 				'main_building'		: oldProjInfo['main_building'],
    # 				'sub_building'		: oldProjInfo['sub_building'],
    # 				'households'		: oldProjInfo['households'],
    # 				'site_area'			: oldProjInfo['site_area'],
    # 				'building_area'		: oldProjInfo['building_area'],
    # 				'total_area'		: oldProjInfo['total_area'],
    # 				'floor_area'		: oldProjInfo['floor_area'],
    # 				'add_info'			: oldProjInfo['add_info'],
    # 				'cons_start_date'	: oldProjInfo['cons_start_date'],
    # 				'cons_end_date'		: oldProjInfo['cons_end_date']
    # 			},
    # 			'modify' : contentsData['projectInfo']
    # 		},
    # 		'supervInfo' : {
    # 			'old' : {
    # 				'reside_class_code'		: oldProjInfo['reside_class_code'],
    # 				'reside_class_name'		: oldProjInfo['reside_class_name'],
    # 				'superv_contract_date'	: oldProjInfo['superv_contract_date'],
    # 				'superv_price'			: oldProjInfo['superv_price'],
    # 				'superv_start_date'		: oldProjInfo['superv_start_date'],
    # 				'superv_end_date'		: oldProjInfo['superv_end_date'],
    # 				'superv_co_code'		: oldProjInfo['co_code'],
    # 				'superv_co_name'		: oldProjInfo['co_name']
    # 			},
    # 			'modify' : contentsData['supervInfo']
    # 		},
    # 		'supervisorsList' : {
    # 			'old' : oldSupervList,
    # 			'modify' : contentsData['supervisorsList']
    # 		}
    #
    # 	}

    return constants.REST_RESPONSE_CODE_ZERO, "", returnData


# 프로젝트 수정 승인
def approvalProjModify(commApproData):
    servCommMana = servCommManage()
    servProjMana = servProjectManage()

    if commApproData["contents"]["modifyType"] == "projectInfo":

        resCd, msg, resData = servProjMana.updateProjDefaultInfo(
            commApproData["contents"]["cons_code"],
            commApproData["contents"]["projectInfo"]["modify"],
            "U",
        )
        if resCd != 0:
            return resCd, msg, None

    # 	elif(commApproData['contents']['modifyType'] == 'supervInfo'):
    # 		resCd, msg, resData = servProjMana.updateSupvDefaultInfo(commApproData['contents']['cons_code'], commApproData['contents']['supervInfo']['modify'], 'U')
    # 		if(resCd != 0):
    # 			return resCd, msg, None

    elif commApproData["contents"]["modifyType"] == "joinUserList":
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "프로젝트 인력 수정 시작",
        )
        addUser = commApproData["contents"]["joinUserList"]["modify"]["add"]
        putUser = commApproData["contents"]["joinUserList"]["modify"]["put"]
        delUser = commApproData["contents"]["joinUserList"]["modify"]["del"]

        resCd, msg, resData = servProjMana.modifyJoinWorkforce(
            commApproData["contents"]["cons_code"], addUser, putUser, delUser
        )

    # 		if(len(modifyUser) > 0):
    # 			resCd, msg, resData = servProjMana.updateJoinWorkforce(commApproData['contents']['cons_code'], modifyUser)
    # 			if(resCd != 0):
    #
    # 				if(len(addUser) > 0):
    # 					servProjMana.delJoinWorkforce(commApproData['contents']['cons_code'], addUser)

    # if(len(delUser) > 0):
    # 	servProjMana.putJoinWorkforce(commApproData['contents']['cons_code'], delUser)

    # 				servProjMana.delJoinWorkforce(commApproData['contents']['cons_code'], commApproData['contents']['supervisorsList']['old'])
    # 				servProjMana.putJoinWorkforce(commApproData['contents']['cons_code'], commApproData['contents']['supervisorsList']['old'])

    # 				return resCd, msg, None

    else:
        return constants.REST_RESPONSE_CODE_DATAFAIL, "잘못된 데이터가 입력 되었습니다.", None

    return constants.REST_RESPONSE_CODE_ZERO, "", None


# 프로젝트 삭제 승인
def approvalProjDelete(commApproData):
    servProjMana = servProjectManage()

    resCd, msg, resData = servProjMana.delProject(
        commApproData["contents"]["cons_code"]
    )
    if resCd != 0:
        return resCd, msg, None

    return constants.REST_RESPONSE_CODE_ZERO, "", None


# 회사 정보 수정
def regCoModify(loginUserInfo, params, req):
    servUserMana = servUserManage()
    commServ = commonService()
    servCompanyMana = servCompanyManage()
    commUtilServ = commUtilService()
    searchList = []

    searchInfo = {"key": "CO_CODE", "value": params["contents"]["co_code"]}
    searchList.append(searchInfo)

    # 등록된 회사 정보가 있는지 확인 한다.
    resCd, msg, oldCoInfo = servUserMana.getCoInfo(searchList)
    if resCd != 0:  # DB 에러 발생 시
        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Database Error : " + commUtilServ.jsonDumps(msg),
        )
        return resCd, msg, None

    if oldCoInfo == None:
        return constants.REST_RESPONSE_CODE_DATAFAIL, "조건에 맞는 회사 정보가 없습니다.", None

    modifyContent = params["contents"]
    # 	coLicensePath = ''
    # 	coLicenseOriginalName = ''
    # 	coLicenseChangeName = ''
    # 사업자 등록증이 변경되 었는지 확인 한다.
    # 	if modifyContent['co_license_status'] == 'C':
    # 		lpath, origName, changeName = servCompanyMana.companyFileNameManage(params['contents']['co_code'], params['contents'], 'co_license_name_new')
    # 		coLicensePath = lpath
    # 		coLicenseOriginalName = origName
    # 		coLicenseChangeName = changeName

    # 		try:
    # 			f_co_license = req.files['f_co_license']
    #
    # 			commServ.createDir(coLicensePath)
    # 			commServ.saveFile(f_co_license, coLicensePath, coLicenseChangeName)
    # 		except:
    # 			return constants.REST_RESPONSE_CODE_DATAFAIL, u'회사 정보를 등록 할 수 없습니다. 관리자에게 문의 하세요.', None

    # 자격증이 변경 되었는지 확인 한다.
    # 	bsLicensePath = ''
    # 	bsLicenseOriginalName = ''
    # 	bsLicenseChangeName = ''
    # 	if modifyContent['bs_license_status'] == 'C':
    # 		lpath, origName, changeName = servCompanyMana.companyFileNameManage(params['contents']['co_code'], params['contents'], 'bs_license_name_new')
    # 		bsLicensePath = lpath
    # 		bsLicenseOriginalName = origName
    # 		bsLicenseChangeName = changeName
    #
    # 		# 공사업 등록증 파일을 저장 한다.
    # 		try:
    # 			f_bs_license = req.files['f_bs_license']
    #
    # 			commServ.createDir(bsLicensePath)
    # 			commServ.saveFile(f_bs_license, bsLicensePath, bsLicenseChangeName)
    # 		except:
    # 			commServ.removeFile(coLicensePath, coLicenseChangeName)
    # 			return constants.REST_RESPONSE_CODE_DATAFAIL, u'회사 정보를 등록 할 수 없습니다. 관리자에게 문의 하세요.', None

    modifyCoInfo = {
        "co_code": modifyContent["co_code"],
        "co_name": modifyContent["co_name"],
        "co_type": modifyContent["co_type"],
        "co_ceo": modifyContent["co_ceo"],
        "co_contact": modifyContent["co_contact"],
        "co_address": modifyContent["co_address"],
        # 		'co_regisnum'				: modifyContent['co_regisnum'],
        "co_regisnum": modifyContent["co_regisnum"],
        # 		'co_license_status'			: modifyContent['co_license_status'],
        # 		'co_license_path'			: coLicensePath,
        # 		'co_license_original_name'	: coLicenseOriginalName,
        # 		'co_license_change_name'	: coLicenseChangeName,
        # 		'bs_license_status'			: modifyContent['bs_license_status'],
        # 		'bs_license_path'			: bsLicensePath,
        # 		'bs_license_original_name'	: bsLicenseOriginalName,
        # 		'bs_license_change_name'	: bsLicenseChangeName
    }

    returnData = {"old": oldCoInfo, "modify": modifyCoInfo}

    return constants.REST_RESPONSE_CODE_ZERO, "", returnData


# 회사 정보 수정 승인
def approvalCoModify(commApproData):
    servCompanyMana = servCompanyManage()
    commServ = commonService()
    commUtilServ = commUtilService()

    updateCoInfoList = []

    oldContents = commApproData["contents"]["old"]
    modifyContents = commApproData["contents"]["modify"]

    if oldContents["co_name"] != modifyContents["co_name"]:
        updateCoInfo = {"key": "CO_NAME", "value": modifyContents["co_name"]}
        updateCoInfoList.append(updateCoInfo)

    if oldContents["co_type"] != modifyContents["co_type"]:
        updateCoInfo = {"key": "CO_TYPE", "value": modifyContents["co_type"]}
        updateCoInfoList.append(updateCoInfo)

    if oldContents["co_ceo"] != modifyContents["co_ceo"]:
        updateCoInfo = {"key": "CEO", "value": modifyContents["co_ceo"]}
        updateCoInfoList.append(updateCoInfo)

    if oldContents["co_contact"] != modifyContents["co_contact"]:
        updateCoInfo = {"key": "CONTACT", "value": modifyContents["co_contact"]}
        updateCoInfoList.append(updateCoInfo)

    if oldContents["co_address"] != modifyContents["co_address"]:
        updateCoInfo = {"key": "ADDRESS", "value": modifyContents["co_address"]}
        updateCoInfoList.append(updateCoInfo)

    # if oldContents['co_regisnum']	!= modifyContents['co_regisnum']:
    # 	updateCoInfo = {
    # 		'key' : 'CO_REGISNUM',
    # 		'value' : modifyContents['co_regisnum']
    # 	}
    # 	updateCoInfoList.append(updateCoInfo)

    if oldContents["co_regisnum"] != modifyContents["co_regisnum"]:
        updateCoInfo = {"key": "REGISNUM", "value": modifyContents["co_regisnum"]}
        updateCoInfoList.append(updateCoInfo)

    # if modifyContents['co_license_status'] == 'C':
    # 		updateCoInfo = {
    # 			'key' : 'co_license_path',
    # 			'value' : modifyContents['co_license_path']
    # 		}
    # 		updateCoInfoList.append(updateCoInfo)
    # 		updateCoInfo = {
    # 			'key' : 'co_license_original_name',
    # 			'value' : modifyContents['co_license_original_name']
    # 		}
    # 		updateCoInfoList.append(updateCoInfo)
    # 		updateCoInfo = {
    # 			'key' : 'co_license_change_name',
    # 			'value' : modifyContents['co_license_change_name']
    # 		}
    # 		updateCoInfoList.append(updateCoInfo)

    # 	elif modifyContents['co_license_status'] == 'D':
    # 		updateCoInfo = {
    # 			'key' : 'co_license_path',
    # 			'value' : ''
    # 		}
    # 		updateCoInfoList.append(updateCoInfo)
    # 		updateCoInfo = {
    # 			'key' : 'co_license_original_name',
    # 			'value' : ''
    # 		}
    # 		updateCoInfoList.append(updateCoInfo)
    # 		updateCoInfo = {
    # 			'key' : 'co_license_change_name',
    # 			'value' : ''
    # 		}
    # 		updateCoInfoList.append(updateCoInfo)
    #
    # 	if modifyContents['bs_license_status'] == 'C':
    # 		updateCoInfo = {
    # 			'key' : 'bs_license_path',
    # 			'value' : modifyContents['bs_license_path']
    # 		}
    # 		updateCoInfoList.append(updateCoInfo)
    # 		updateCoInfo = {
    # 			'key' : 'bs_license_original_name',
    # 			'value' : modifyContents['bs_license_original_name']
    # 		}
    # 		updateCoInfoList.append(updateCoInfo)
    # 		updateCoInfo = {
    # 			'key' : 'bs_license_change_name',
    # 			'value' : modifyContents['bs_license_change_name']
    # 		}
    # 		updateCoInfoList.append(updateCoInfo)
    #
    # 	elif modifyContents['bs_license_status'] == 'D':
    # 		updateCoInfo = {
    # 			'key' : 'bs_license_path',
    # 			'value' : ''
    # 		}
    # 		updateCoInfoList.append(updateCoInfo)
    # 		updateCoInfo = {
    # 			'key' : 'bs_license_original_name',
    # 			'value' : ''
    # 		}
    # 		updateCoInfoList.append(updateCoInfo)
    # 		updateCoInfo = {
    # 			'key' : 'bs_license_change_name',
    # 			'value' : ''
    # 		}
    # 		updateCoInfoList.append(updateCoInfo)

    if len(updateCoInfoList) < 1:
        return constants.REST_RESPONSE_CODE_DATAFAIL, "업데이트 할 데이터가 없습니다.", None

    resCd, msg, resData = servCompanyMana.update_company(
        oldContents["co_code"], updateCoInfoList
    )
    if resCd != 0:
        return resCd, msg, None

    # 	if modifyContents['co_license_status'] == 'C' or modifyContents['co_license_status'] == 'D' :
    # 		commServ.removeFile(oldContents['co_license_path'], oldContents['co_license_change_name'])

    # 	if modifyContents['bs_license_status'] == 'C' or modifyContents['bs_license_status'] == 'D' :
    # 		commServ.removeFile(oldContents['bs_license_path'], oldContents['bs_license_change_name'])

    return constants.REST_RESPONSE_CODE_ZERO, "", None


# 내 정보 수정
def approvalMyModify(commApproData):
    servUserMana = servUserManage()
    commServ = commonService()
    commUtilServ = commUtilService()

    logs.war(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "시자자자자작",
    )
    updateUserInfoList = []

    contentsInfo = commApproData["contents"]

    if contentsInfo["before_user_position"] != contentsInfo["after_user_position"]:
        updateUserInfo = {
            "key": "USER_POSITION",
            "value": contentsInfo["after_user_position"],
        }
        updateUserInfoList.append(updateUserInfo)

    if contentsInfo["before_authority_code"] != contentsInfo["after_authority_code"]:
        updateUserInfo = {
            "key": "AUTHORITY_CODE",
            "value": contentsInfo["after_authority_code"],
        }
        updateUserInfoList.append(updateUserInfo)

    if len(updateUserInfoList) < 1:
        return constants.REST_RESPONSE_CODE_DATAFAIL, "업데이트 할 데이터가 없습니다.", None
    logs.war(
        procName,
        os.path.basename(__file__),
        sys._getframe(0).f_code.co_name,
        "시자자자자작",
    )
    resCd, msg, resData = servUserMana.updateUserCoInfo(
        contentsInfo["id"], updateUserInfoList
    )
    if resCd != 0:
        return resCd, msg, None

    return constants.REST_RESPONSE_CODE_ZERO, "", None


# 프로젝트 중지
def regProjStop(loginUserInfo, params):
    servProjMana = servProjectManage()
    commServ = commonService()
    servCompanyMana = servCompanyManage()
    commUtilServ = commUtilService()
    searchList = []

    contents = params["contents"]

    resCd, msg, projInfo = servProjMana.getProjDefaultInfo(contents["cons_code"])
    if resCd != 0:
        return resCd, msg, None

    consName = projInfo["cons_name"]

    returnData = {
        "cons_name": projInfo["cons_name"],
        "cons_code": contents["cons_code"],
        "proj_stop_date": contents["proj_stop_date"],
        "proj_stop_cause": contents["proj_stop_cause"],
        "proj_stop_reg_date": util_time.get_current_time(
            util_time.TIME_CURRENT_TYPE_14
        ),
        "req_id": loginUserInfo["id"],
        "req_co_code": loginUserInfo["co_code"],
    }

    return constants.REST_RESPONSE_CODE_ZERO, "", returnData


# 프로젝트 중지 승인
def approvalProjStop(commApproData):
    servProjMana = servProjectManage()
    commServ = commonService()
    commUtilServ = commUtilService()

    contentsInfo = commApproData["contents"]
    contentsInfo["proj_stop_appro_date"] = util_time.get_current_time(
        util_time.TIME_CURRENT_TYPE_14
    )
    # 중지 이력 데이터를 저장 한다.
    resCd, msg, resData = servProjMana.putProjStopHis(contentsInfo)
    if resCd != 0:
        return resCd, msg, None

    # 프로젝트 정보를 업데이트 한다.
    updateInfoList = []
    updateInfo = {"key": "PROJECT_STATUS", "value": constants.PROJECT_STATUS_CD_STOP}
    updateInfoList.append(updateInfo)
    resCd, msg, resData = servProjMana.updateProjInfo(
        contentsInfo["cons_code"], updateInfoList
    )
    if resCd != 0:
        # 업데이트 실패 시 이력 정보를 삭제 한다.
        servProjMana.delProjStopHis(contentsInfo)
        return resCd, msg, None

    return constants.REST_RESPONSE_CODE_ZERO, "", None


# 프로젝트 재시작
def regProjRestart(loginUserInfo, params):
    servProjMana = servProjectManage()
    commServ = commonService()
    servCompanyMana = servCompanyManage()
    commUtilServ = commUtilService()
    searchList = []

    contents = params["contents"]

    resCd, msg, projInfo = servProjMana.getProjDefaultInfo(contents["cons_code"])
    if resCd != 0:
        return resCd, msg, None

    consName = projInfo["cons_name"]

    returnData = {
        "cons_name": projInfo["cons_name"],
        "cons_code": contents["cons_code"],
        "proj_restart_date": contents["proj_restart_date"],
        "proj_restart_reg_date": util_time.get_current_time(
            util_time.TIME_CURRENT_TYPE_14
        ),
        "req_id": loginUserInfo["id"],
        "req_co_code": loginUserInfo["co_code"],
    }

    return constants.REST_RESPONSE_CODE_ZERO, "", returnData


# 프로젝트 재시작 승인
def approvalProjRestart(commApproData):
    servProjMana = servProjectManage()
    commServ = commonService()
    commUtilServ = commUtilService()

    contentsInfo = commApproData["contents"]
    contentsInfo["proj_stop_appro_date"] = util_time.get_current_time(
        util_time.TIME_CURRENT_TYPE_14
    )
    # 중지 이력 데이터를 저장 한다.
    resCd, msg, resData = servProjMana.updateProjRestartHis(contentsInfo)
    if resCd != 0:
        return resCd, msg, None

    # 프로젝트 정보를 업데이트 한다.
    updateInfoList = []
    updateInfo = {"key": "PROJECT_STATUS", "value": constants.PROJECT_STATUS_CD_PROC}
    updateInfoList.append(updateInfo)
    resCd, msg, resData = servProjMana.updateProjInfo(
        contentsInfo["cons_code"], updateInfoList
    )
    if resCd != 0:
        # 업데이트 실패 시 이력 정보를 삭제 한다.
        servProjMana.delProjStopHis(contentsInfo)
        return resCd, msg, None

    return constants.REST_RESPONSE_CODE_ZERO, "", None
