from flask import Blueprint, request
from flask_restx import Resource
import json
import copy
import os
import sys

from allscapeAPIMain import db
from allscapeAPIMain import procCode
from allscapeAPIMain import procName
from allscapeAPIMain import api

from common.logManage import logManage
from logManage.servLogManage import servLogManage
from common import constants
from common.commUtilService import commUtilService
from common.commonService import commonService
from historyManage.servHistoryManage import servHistoryManage
from userManage.servUserManage import servUserManage
from projectManage.servProjectManage import servProjectManage
from projectApprovalBoardManage.servProjectApprovalBoardManage import (
    servProjectApprovalBoardManage,
)

projectApprovalBoardManageApi = api.namespace(
    "projectApprovalBoardApi", description="승인게시판 관리"
)

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


@projectApprovalBoardManageApi.route("/ApprovalBoardList/<cons_code>")
class projectApprovalListManage(Resource):
    """승인 게시글 리스트 조회 api"""

    @api.doc(description="승인 게시글 리스트 조회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument(
            "start_num", type=int, location="querys", required=True
        ),
        api.parser().add_argument(
            "end_num", type=int, location="querys", required=True
        ),
        api.parser().add_argument(
            "co_name", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "writer_name", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "post_type", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "title_keyword", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "content_keyword", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "reg_date_start", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "reg_date_end", type=str, location="querys", required=False
        ),
    )
    def get(self, cons_code):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servHisMana = servHistoryManage()
        servProjABMana = servProjectApprovalBoardManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 승인 게시글 get api 시작 ----------",
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
                params.update({"cons_code": cons_code})
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 실정보고 리스트 조회를 시도하였습니다.",
                                    json.dumps(params, ensure_ascii=False), "", resCd, msg)
                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None or (
                loginUserInfo["authority_code"] != constants.USER_BUYER
                and loginUserInfo["authority_code"] != constants.USER_MONITOR
                and loginUserInfo["authority_code"] != constants.USER_CONSTRUCTOR
                and loginUserInfo["authority_code"] != constants.USER_DESIGNER
            ):
                params.update({"cons_code": cons_code})
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 실정보고 리스트 조회를 시도하였습니다.",
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
                "co_name": "",
                "writer_name": "",
                "post_type": "",
                "title_keyword": "",
                "content_keyword": "",
                "reg_date_start": "",
                "reg_date_end": "",
            }
            conditions = request.args.to_dict()
            allowed_keys = {
                "co_name",
                "writer_name",
                "post_type",
                "title_keyword",
                "content_keyword",
                "reg_date_start",
                "reg_date_end",
            }
            for key in allowed_keys:
                if key in conditions:
                    params[key] = str(conditions.get(key))

            #################################### 해당 게시글 목록을 조회한다 ##########################

            resCd, msg, WRData = servProjABMana.get_approval_list(
                loginUserInfo["id"],
                cons_code,
                loginUserInfo["co_code"],
                params["co_name"],
                params["writer_name"],
                params["post_type"],
                params["title_keyword"],
                params["content_keyword"],
                params["reg_date_start"],
                params["reg_date_end"],
            )
            result = {
                "count": len(WRData) if WRData else 0,
                "data": WRData[params["start_num"] : params["end_num"]],
            }
            params.update({"cons_code": cons_code})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 실정보고 리스트 조회를 하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, result)

        except Exception as e:
            params.update({"cons_code": cons_code})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                    f"{loginUserInfo['id']} 사용자가 실정보고 리스트 조회를 하던 중 에러가 발생하였습니다.",
                                    json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )
        return result


@projectApprovalBoardManageApi.route("/ApprovalBoard/<cons_code>")
class projectApprovalManage(Resource):
    """승인 게시글 관리 api"""

    @api.doc(description="승인 게시글 작성")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("data", type=dict, location="form", required=True),
        api.parser().add_argument("files", type=list, location="form", required=False),
    )
    def post(self, cons_code):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjMana = servProjectManage()
        servProjABMana = servProjectApprovalBoardManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 승인 게시글 post api 시작 ----------",
        )

        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")
            params = json.loads(request.form["data"], encoding="utf-8")

            # System Code Check
            result, resultData = commServ.checkSystemCd(sysCd)
            if result == False:
                return resultData

            # Token Check
            result, resultData = commServ.checkTokenCd(token)
            if result == False:
                return resultData

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
                params.update({"cons_code": cons_code})
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 실정보고를 작성시도 하였습니다.",
                                    json.dumps(params, ensure_ascii=False), "", resCd, msg)
                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None or (
                loginUserInfo["authority_code"] != constants.USER_MONITOR
                and loginUserInfo["authority_code"] != constants.USER_CONSTRUCTOR
            ):
                params.update({"cons_code": cons_code})
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 실정보고를 작성시도 하였습니다.",
                                    json.dumps(params, ensure_ascii=False), loginUserInfo.get("id", "") if loginUserInfo else "", resCd, msg)
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_455, "권한이 없습니다", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )
                return result

            #################################### 해당 게시글을 작성한다 ##########################

            resCd, msg, post_uuid = servProjABMana.post_approval(
                cons_code,
                loginUserInfo["co_code"],
                loginUserInfo["id"],
                params["post_type"],
                params["title"],
                params["content"],
                params["approval"] if "approval" in params else None,
                request.files,
            )
            params.update({"cons_code": cons_code})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 작성하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, post_uuid)

        except Exception as e:
            params.update({"cons_code": cons_code})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 작성하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.doc(description="승인 게시글 조회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("uuid", type=str, location="querys", required=True),
    )
    def get(self, cons_code):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servHisMana = servHistoryManage()
        servProjABMana = servProjectApprovalBoardManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 승인 게시글 get api 시작 ----------",
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
                params = {"cons_code": cons_code, "uuid":uuid}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 실정보고를 조회시도 하였습니다.",
                                    json.dumps(params, ensure_ascii=False), "", resCd, msg)
                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None or (
                loginUserInfo["authority_code"] != constants.USER_BUYER
                and loginUserInfo["authority_code"] != constants.USER_MONITOR
                and loginUserInfo["authority_code"] != constants.USER_CONSTRUCTOR
                and loginUserInfo["authority_code"] != constants.USER_DESIGNER
            ):
                params = {"cons_code": cons_code, "uuid":uuid}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 실정보고를 조회시도 하였습니다.",
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

            #################################### 해당 게시글을 조회한다 ##########################

            resCd, msg, WRData = servProjABMana.get_approval(
                loginUserInfo["id"], cons_code, loginUserInfo["co_code"], uuid
            )
            params = {"cons_code": cons_code, "uuid":uuid}
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 조회하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, WRData)

        except Exception as e:
            params = {"cons_code": cons_code, "uuid":uuid}
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 조회하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.doc(description="승인 게시글 수정")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("data", type=str, location="form", required=True),
        api.parser().add_argument("files", type=str, location="form", required=False),
    )
    def put(self, cons_code):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjMana = servProjectManage()
        servProjABMana = servProjectApprovalBoardManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 승인 게시글 update api 시작 ----------",
        )

        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")
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

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 사용자 정보를 가져온다. ----------",
            )

            # 사용자 정보를 가져 온다.
            resCd, msg, loginUserInfo = servUserMana.getUserInfo(2, token, sysCd)
            if resCd != 0:  # DB 에러 발생 시
                params.update({"cons_code": cons_code})
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 실정보고를 수정시도 하였습니다.",
                                    json.dumps(params, ensure_ascii=False), loginUserInfo.get("id", "") if loginUserInfo else "", resCd, msg)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )
                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None or (
                loginUserInfo["authority_code"] != constants.USER_MONITOR
                and loginUserInfo["authority_code"] != constants.USER_CONSTRUCTOR
            ):
                params.update({"cons_code": cons_code})
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 실정보고를 수정시도 하였습니다.",
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

            #################################### 해당 게시글을 수정한다 ##########################

            if "post_type" not in params:
                params["post_type"] = None
            if "title" not in params:
                params["title"] = None
            if "content" not in params:
                params["content"] = None
            if "indexes" not in params:
                params["indexes"] = None
            if "approval" not in params:
                params["approval"] = None

            resCd, msg, _ = servProjABMana.put_approval(
                cons_code,
                params["uuid"],
                params["post_type"],
                params["title"],
                params["content"],
                params["approval"] if "approval" in params else None,
                params["indexes"],
                request.files,
            )
            params.update({"cons_code": cons_code})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 수정하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params.update({"cons_code": cons_code})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 수정하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.doc(description="승인 게시글 삭제")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("uuid", type=str, location="args", required=True),
    )
    def delete(self, cons_code):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjMana = servProjectManage()
        servProjABMana = servProjectApprovalBoardManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 승인 게시글 delete api 시작 ----------",
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
                params = {"cons_code": cons_code, "uuid":uuid}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 실정보고를 삭제시도 하였습니다.",
                                    json.dumps(params, ensure_ascii=False), loginUserInfo.get("id", "") if loginUserInfo else "", resCd, msg)
                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None or (
                loginUserInfo["authority_code"] != constants.USER_MONITOR
                and loginUserInfo["authority_code"] != constants.USER_CONSTRUCTOR
            ):
                params = {"cons_code": cons_code, "uuid":uuid}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 실정보고를 삭제시도 하였습니다.",
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

            #################################### 해당 게시글을 삭제한다 ##########################

            resCd, msg, _ = servProjABMana.delete_approval(cons_code, uuid)
            params = {"cons_code": cons_code, "uuid":uuid}
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 삭제하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params = {"cons_code": cons_code, "uuid":uuid}
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 삭제하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

@projectApprovalBoardManageApi.route(
    "/ApprovalBoardList/<cons_code>/<post_uuid>/drafted"
)
class projectApprovalListManage(Resource):
    """승인 게시글 기안 api"""

    @api.doc(description="승인 게시글 결재 기안")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument(
            "cons_code", type=str, location="path", required=True
        ),
        api.parser().add_argument(
            "post_uuid", type=str, location="path", required=True
        ),
    )
    def post(self, cons_code, post_uuid):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servHisMana = servHistoryManage()
        servProjABMana = servProjectApprovalBoardManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 승인 게시글 결재 기안 post api 시작 ----------",
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
                params = {"cons_code": cons_code, "uuid":post_uuid}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 실정보고를 기안시도 하였습니다.",
                                    json.dumps(params, ensure_ascii=False), "", resCd, msg)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None or (
                loginUserInfo["authority_code"] != constants.USER_MONITOR
                and loginUserInfo["authority_code"] != constants.USER_CONSTRUCTOR
            ):
                params = {"cons_code": cons_code, "uuid":post_uuid}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 실정보고를 기안시도 하였습니다.",
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

            #################################### 해당 게시글을 기안한다 ##########################

            resCd, msg, _ = servProjABMana.draft(
                cons_code, post_uuid, loginUserInfo["id"]
            )
            params = {"cons_code": cons_code, "uuid":post_uuid}
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 기안하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params = {"cons_code": cons_code, "uuid":post_uuid}
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 기안하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            return commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

@projectApprovalBoardManageApi.route(
    "/ApprovalBoardList/<cons_code>/<post_uuid>/withdraw"
)
class projectApprovalListManage(Resource):
    """승인 게시글 기안 api"""

    @api.doc(description="승인 게시글 결재 철회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument(
            "cons_code", type=str, location="path", required=True
        ),
        api.parser().add_argument(
            "post_uuid", type=str, location="path", required=True
        ),
    )
    def post(self, cons_code, post_uuid):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servHisMana = servHistoryManage()
        servProjABMana = servProjectApprovalBoardManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 승인 게시글 결재 철회 post api 시작 ----------",
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
                params = {"cons_code": cons_code, "uuid":post_uuid}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 실정보고를 철회시도 하였습니다.",
                                    json.dumps(params, ensure_ascii=False), "", resCd, msg)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None or (
                loginUserInfo["authority_code"] != constants.USER_MONITOR
                and loginUserInfo["authority_code"] != constants.USER_CONSTRUCTOR
            ):
                params = {"cons_code": cons_code, "uuid":post_uuid}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 실정보고를 철회시도 하였습니다.",
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

            #################################### 해당 게시글을 철회한다 ##########################

            resCd, msg, _ = servProjABMana.withdraw(
                cons_code, post_uuid
            )
            params = {"cons_code": cons_code, "uuid":post_uuid}
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 철회하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params = {"cons_code": cons_code, "uuid":post_uuid}
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 철회하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            return commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

@projectApprovalBoardManageApi.route(
    "/ApprovalBoardList/<cons_code>/<post_uuid>/approved"
)
class projectApprovalListManage(Resource):
    """승인 게시글 결재 승인 api"""

    @api.doc(description="승인 게시글 결재 승인")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("remarks", type=str, location="json", required=True),
    )
    def post(self, cons_code, post_uuid):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servHisMana = servHistoryManage()
        servProjABMana = servProjectApprovalBoardManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 승인 게시글 결재 승인 post api 시작 ----------",
        )

        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")
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

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 사용자 정보를 가져온다. ----------",
            )

            # 사용자 정보를 가져 온다.
            resCd, msg, loginUserInfo = servUserMana.getUserInfo(2, token, sysCd)
            if resCd != 0:  # DB 에러 발생 시
                params.update({"cons_code": cons_code, "uuid":post_uuid})
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 실정보고를 결재시도 하였습니다.",
                                    json.dumps(params, ensure_ascii=False), "", resCd, msg)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None or (
                loginUserInfo["authority_code"] != constants.USER_BUYER
                and loginUserInfo["authority_code"] != constants.USER_MONITOR
                and loginUserInfo["authority_code"] != constants.USER_CONSTRUCTOR
                and loginUserInfo["authority_code"] != constants.USER_DESIGNER
            ):
                params.update({"cons_code": cons_code, "uuid":post_uuid})
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 실정보고를 결재시도 하였습니다.",
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

            #################################### 해당 게시글을 승인한다 ##########################

            resCd, msg, _ = servProjABMana.approve(
                cons_code,
                post_uuid,
                loginUserInfo["id"],
                loginUserInfo["co_code"],
                params["remarks"],
            )
            params.update({"cons_code": cons_code, "uuid":post_uuid})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 결재하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params.update({"cons_code": cons_code, "uuid":post_uuid})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 결재하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            return commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )


@projectApprovalBoardManageApi.route(
    "/ApprovalBoardList/<cons_code>/<post_uuid>/denied"
)
class projectApprovalListManage(Resource):
    """승인 게시글 결재 거절 api"""

    @api.doc(description="승인 게시글 결재 거절")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("remarks", type=str, location="json", required=True),
    )
    def post(self, cons_code, post_uuid):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servHisMana = servHistoryManage()
        servProjABMana = servProjectApprovalBoardManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 승인 게시글 결재 거절 post api 시작 ----------",
        )

        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")
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

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 사용자 정보를 가져온다. ----------",
            )

            # 사용자 정보를 가져 온다.
            resCd, msg, loginUserInfo = servUserMana.getUserInfo(2, token, sysCd)
            if resCd != 0:  # DB 에러 발생 시
                params.update({"cons_code": cons_code, "uuid":post_uuid})
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 실정보고를 반려시도 하였습니다.",
                                    json.dumps(params, ensure_ascii=False), "", resCd, msg)
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None or (
                loginUserInfo["authority_code"] != constants.USER_BUYER
                and loginUserInfo["authority_code"] != constants.USER_MONITOR
                and loginUserInfo["authority_code"] != constants.USER_CONSTRUCTOR
                and loginUserInfo["authority_code"] != constants.USER_DESIGNER
            ):
                params.update({"cons_code": cons_code, "uuid":post_uuid})
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 실정보고를 반려시도 하였습니다.",
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

            #################################### 해당 게시글을 거절한다 ##########################

            resCd, msg, _ = servProjABMana.deny(
                cons_code, post_uuid, loginUserInfo["id"], params["remarks"]
            )
            params.update({"cons_code": cons_code, "uuid":post_uuid})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 반려하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params.update({"cons_code": cons_code, "uuid":post_uuid})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 실정보고를 반려하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            return commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )
