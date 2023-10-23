from flask import Blueprint, request
from flask_restx import Resource
import json
import copy
import os
import sys
import io

from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import api

from common.logManage import logManage
from common import constants
from common.commUtilService import commUtilService
from common.commonService import commonService
from common.excelService import excelService
from historyManage.servHistoryManage import servHistoryManage
from userManage.servUserManage import servUserManage
from projectManage.servProjectManage import servProjectManage
from projectWorkReplyManage.servProjectWorkReplyManage import servProjectWorkReplyManage
from projectWorkLogManage.servProjectWorkLogManage import servProjectWorkLogManage


projectWorkReplyManageApi = api.namespace(
    "projectWorkReplyApi", description="작업일지 댓글 관리"
)

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


@api.response(200, "Success")
@api.response(400, "Bad Request")
@api.response(500, "Server Internal Error")
@projectWorkReplyManageApi.route("/WorkReply/<sys_doc_num>")
class projectWorkReplyManage(Resource):
    """작업일지 댓글관리 api"""

    @api.response(455, "User not found")
    @api.response(401, "Unauthorized")
    @api.doc(description="작업일지 댓글 작성")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument(
            "parent_uuid", type=str, location="args", required=False
        ),
        api.parser().add_argument("content", type=str, location="json", required=True),
    )
    def post(self, sys_doc_num):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjMana = servProjectManage()
        servProjWRMana = servProjectWorkReplyManage()
        servProjWLMana = servProjectWorkLogManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업일지 댓글 post api 시작 ----------",
        )

        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")
            parent_uuid = request.args.get("parent_uuid")
            params = request.get_json()

            # System Code Check
            result, resultData = commServ.checkSystemCd(sysCd)
            if result == False:
                return resultData

            # Token Check
            result, resultData = commServ.checkTokenCd(token)
            if result == False:
                return resultData

            #################################### 프로젝트가 중지상태가 아닌지 확인한다 ###############################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 프로젝트 상태 정보를 가져온다. ----------",
            )

            resCd, msg, projectStatus = servProjMana.getProjectStatusBySysdocnum(
                sys_doc_num
            )

            if (
                resCd != 0
                or projectStatus["status"] == constants.PROJECT_STATUS_CD_STOP
            ):
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "작성할 수 없는 프로젝트 입니다",
                )
                return commServ.makeReturnMessage(resCd, msg, None)

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

            #### 시공사 (참여프로젝트 한정), 본사 관리자 (전체 프로젝트)만 댓글을 달 수 있다 ####
            if (
                loginUserInfo["authority_code"] == constants.USER_BUYER
                or loginUserInfo["authority_code"] == constants.USER_CONSTRUCTOR
            ):
                result = commServ.makeReturnMessage(401, str("권한이 없습니다"), None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )
                return result

            elif loginUserInfo["authority_code"] == constants.USER_MONITOR:
                resCd, msg, authData = servProjWLMana.check_sysnum_companyauth(
                    sys_doc_num, loginUserInfo["co_code"]
                )
                if resCd != 0 or not authData:
                    result = commServ.makeReturnMessage(403, str("권한이 없습니다"), None)
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Response : " + commUtilServ.jsonDumps(result),
                    )
                    return result

            elif loginUserInfo["authority_code"] == constants.USER_CONSTRUCTOR:
                resCd, msg, authData = servProjWLMana.check_sysnum_userauth(
                    sys_doc_num, loginUserInfo["id"]
                )
                if resCd != 0 or not authData:
                    result = commServ.makeReturnMessage(403, str("권한이 없습니다"), None)
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Response : " + commUtilServ.jsonDumps(result),
                    )
                    return result

            #################################### 해당 댓글을 작성한다 ##########################

            resCd, msg, _ = servProjWRMana.post_reply(
                sys_doc_num, parent_uuid, loginUserInfo["id"], params["content"]
            )
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.response(455, "User not found")
    @api.response(401, "Unauthorized")
    @api.doc(description="작업일지 댓글 조회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument(
            "parent_uuid", type=str, location="querys", required=False
        ),
    )
    def get(self, sys_doc_num):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjWRMana = servProjectWorkReplyManage()
        servProjWLMana = servProjectWorkLogManage()
        servHisMana = servHistoryManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 댓글 조회 api 시작 ----------",
        )

        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")
            parent_uuid = request.args.get("parent_uuid")

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
            #  무직자가 작업일지
            if loginUserInfo["co_code"] == "":
                # 프로젝트에 해당하는 회사 코드를 가져 온다.
                resCd, msg, data = servProjWLMana.get_conscode(sys_doc_num)
                if resCd == 0:
                    searchList = []
                    searchInfo = {"key": "ID", "value": loginUserInfo["id"]}
                    searchList.append(searchInfo)
                    searchInfo = {"key": "CONS_CODE", "value": data["cons_code"]}
                    searchList.append(searchInfo)

                    resCd, msg, projHisInfo = servHisMana.getProjHisList(searchList)
                    if resCd == 0:
                        loginUserInfo["co_code"] = projHisInfo[0]["co_code"]
            #### 시공사 (참여프로젝트 한정), 본사 관리자 (전체 프로젝트)만 댓글을 볼 수 있다 ####
            if (
                loginUserInfo["authority_code"] == constants.USER_BUYER
                or loginUserInfo["authority_code"] == constants.USER_CONSTRUCTOR
            ):
                result = commServ.makeReturnMessage(403, str("권한이 없습니다"), None)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )
                return result

            elif loginUserInfo["authority_code"] == constants.USER_MONITOR:
                resCd, msg, authData = servProjWLMana.check_sysnum_companyauth(
                    sys_doc_num, loginUserInfo["co_code"]
                )
                if resCd != 0 or not authData:
                    result = commServ.makeReturnMessage(403, str("권한이 없습니다"), None)
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Response : " + commUtilServ.jsonDumps(result),
                    )
                    return result

            elif loginUserInfo["authority_code"] == constants.USER_CONSTRUCTOR:
                resCd, msg, authData = servProjWLMana.check_sysnum_userauth(
                    sys_doc_num, loginUserInfo["id"]
                )
                if resCd != 0 or not authData:
                    result = commServ.makeReturnMessage(401, str("권한이 없습니다"), None)
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Response : " + commUtilServ.jsonDumps(result),
                    )
                    return result

            #################################### 로직에 필요한 변수를 저장한다. ####################################
            params = {
                "id": loginUserInfo["id"],
                "sys_doc_num": sys_doc_num,
            }

            #################################### 해당 댓글을 조회한다 ##########################

            resCd, msg, WRData = servProjWRMana.get_reply(
                params["sys_doc_num"], parent_uuid
            )
            return commServ.makeReturnMessage(resCd, msg, WRData)

        except Exception as e:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.response(455, "User not found")
    @api.response(454, "User mismatch")
    @api.doc(description="작업일지 댓글 수정")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("uuid", type=str, location="args", required=True),
        api.parser().add_argument("content", type=str, location="json", required=True),
    )
    def put(self, sys_doc_num):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjMana = servProjectManage()
        servProjWRMana = servProjectWorkReplyManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 댓글 수정 api 시작 ----------",
        )

        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")
            uuid = request.args.get("uuid")
            params = request.get_json()

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "params:" + commUtilServ.jsonDumps(params),
            )
            # System Code Check
            result, resultData = commServ.checkSystemCd(sysCd)
            if result == False:
                return resultData

            # Token Check
            result, resultData = commServ.checkTokenCd(token)
            if result == False:
                return resultData

            #################################### 프로젝트가 중지상태가 아닌지 확인한다 ###############################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 프로젝트 상태 정보를 가져온다. ----------",
            )

            resCd, msg, projectStatus = servProjMana.getProjectStatusBySysdocnum(
                sys_doc_num
            )

            if (
                resCd != 0
                or projectStatus["status"] == constants.PROJECT_STATUS_CD_STOP
            ):
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "작성할 수 없는 프로젝트 입니다",
                )
                return commServ.makeReturnMessage(resCd, msg, None)

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

            """
            # 해당 유저가 쓴 댓글인지 확인한다.
            resCd, msg, ReplyData = servProjWRMana.check_reply(
                uuid, sys_doc_num, loginUserInfo["id"]
            )
            if resCd != 0:  # DB 에러 발생 시
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + str(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if not ReplyData:
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
            """
            #################################### 해당 댓글을 수정한다 ##########################

            resCd, msg, _ = servProjWRMana.put_reply(params["content"], uuid)
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.response(455, "User not found")
    @api.response(454, "User mismatch")
    @api.doc(description="작업일지 댓글 삭제")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("uuid", type=str, location="args", required=True),
    )
    def delete(self, sys_doc_num):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjMana = servProjectManage()
        servProjWRMana = servProjectWorkReplyManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 댓글 삭제 api 시작 ----------",
        )

        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")
            uuid = request.args.get("uuid")

            # System Code Check
            result, resultData = commServ.checkSystemCd(sysCd)
            if result == False:
                return resultData

            # Token Check
            result, resultData = commServ.checkTokenCd(token)
            if result == False:
                return resultData

            #################################### 프로젝트가 중지상태가 아닌지 확인한다 ###############################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 프로젝트 상태 정보를 가져온다. ----------",
            )

            resCd, msg, projectStatus = servProjMana.getProjectStatusBySysdocnum(
                sys_doc_num
            )

            if (
                resCd != 0
                or projectStatus["status"] == constants.PROJECT_STATUS_CD_STOP
            ):
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "작성할 수 없는 프로젝트 입니다",
                )
                return commServ.makeReturnMessage(resCd, msg, None)

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
            """
            # 해당 유저가 쓴 댓글인지 확인한다.
            resCd, msg, ReplyData = servProjWRMana.check_reply(
                uuid, sys_doc_num, loginUserInfo["id"]
            )
            if resCd != 0:  # DB 에러 발생 시
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + str(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if not ReplyData:
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
            """
            #################################### 해당 댓글을 삭제한다 ##########################

            resCd, msg, _ = servProjWRMana.del_reply(uuid)
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result
