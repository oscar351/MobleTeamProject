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
from projectDailyReportManage.servProjectDailyReportManage import (
    servProjectDailyReportManage,
)

projectDailyReportManageApi = api.namespace(
    "projectDailyReportApi", description="공사일지 및 사진대지 관리"
)

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


@projectDailyReportManageApi.route("/DailyReportList/<cons_code>")
class projectDailyReportListManage(Resource):
    """공사일지 리스트 조회 api"""

    @api.doc(description="공사일지 리스트 조회")
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
            "writer_name_keyword", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "start_date", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "end_date", type=str, location="querys", required=False
        ),
    )
    def get(self, cons_code):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servHisMana = servHistoryManage()
        servProjDPMana = servProjectDailyReportManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공사일지 조회 api 시작 ----------",
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
                params = {"cons_code": cons_code}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 작업일지 리스트를 조회시도 하였습니다.",
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
                and loginUserInfo["authority_code"] != constants.USER_BUYER
                and loginUserInfo["authority_code"] != constants.USER_DESIGNER
            ):
                params = {"cons_code": cons_code}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 작업일지 리스트를 조회시도 하였습니다.",
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
                "co_code": loginUserInfo["co_code"],
                "writer_name_keyword": "",
                "start_date": "",
                "end_date": "",
            }
            conditions = request.args.to_dict()
            allowed_keys = [
                "writer_name_keyword",
                "start_date",
                "end_date",
            ]
            for key in allowed_keys:
                if key in conditions:
                    params[key] = str(conditions.get(key))

            # 퇴사자는 프로젝트 기록에서 참여정보 가져온다
            if loginUserInfo["authority_code"] == constants.USER_INOCCUPATION:
                resCd, msg, project_data = servHisMana.getProjHisList(
                    [{"key": "ID", "value": loginUserInfo["id"]}]
                )
                if resCd != 0:
                    commServ.makeReturnMessage(resCd, msg, None)

                for project in project_data:
                    if project["cons_code"] == cons_code:
                        params["co_code"] = project["co_code"]
                        resCd, msg, company_data = servHisMana.getCoHisList(
                            [{"key": "ID", "value": loginUserInfo["id"]}]
                        )
                        if resCd != 0:
                            commServ.makeReturnMessage(resCd, msg, None)

                        #### 재직기간 중 작업일보만 조회 가능 ####
                        for company in company_data:
                            if params["co_code"] == company["co_code"]:
                                if (
                                    params["start_date"] == ""
                                    or params["start_date"]
                                    < company["co_tenure_start_date"]
                                ):
                                    params["start_date"] = company[
                                        "co_tenure_start_date"
                                    ]
                                if (
                                    params["end_date"] == ""
                                    or params["end_date"]
                                    > company["co_tenure_end_date"]
                                ):
                                    params["end_date"] = company["co_tenure_end_date"]

            if loginUserInfo["authority_code"] == constants.USER_BUYER:
                params["co_code"] = ""

            #################################### 해당 공사일지 목록을 조회한다 ##########################

            resCd, msg, WRData = servProjDPMana.get_daily_report_list(
                cons_code,
                params["co_code"],
                params["writer_name_keyword"],
                params["start_date"],
                params["end_date"],
            )
            result = {
                "count": len(WRData) if WRData else 0,
                "data": WRData[params["start_num"] : params["end_num"]],
            }
            params.update({"cons_code": cons_code})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 공사일보 리스트를 조회하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, result)

        except Exception as e:
            params.update({"cons_code": cons_code})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 공사일보 리스트를 조회하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result


@projectDailyReportManageApi.route("/DailyReportHeadCount/<cons_code>/<co_code>")
class projectDailyReportListManage(Resource):
    """공사일지 공종별 투입인원 조회 api"""

    @api.doc(description="공사일지 공종별 투입인원 조회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument(
            "cons_date", type=str, location="querys", required=True
        ),
        api.parser().add_argument(
            "pc_name", type=str, location="querys", required=False
        ),
    )
    def get(self, cons_code, co_code):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servHisMana = servHistoryManage()
        servProjDPMana = servProjectDailyReportManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공사일지 공종별 투입인원 조회 api 시작 ----------",
        )

        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")
            pc_name = request.args.get("pc_name")
            cons_date = request.args.get("cons_date")
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

            if loginUserInfo == None or (
                loginUserInfo["authority_code"] != constants.USER_MONITOR
                and loginUserInfo["authority_code"] != constants.USER_CONSTRUCTOR
                and loginUserInfo["authority_code"] != constants.USER_BUYER
                and loginUserInfo["authority_code"] != constants.USER_DESIGNER
            ):
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

            #################################### 해당 공사일지 목록을 조회한다 ##########################
            if not pc_name:
                pc_name = ""
            resCd, msg, WRData = servProjDPMana.count_workforce(
                cons_code, co_code, cons_date, pc_name
            )
            return commServ.makeReturnMessage(resCd, msg, WRData)

        except Exception as e:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result


@projectDailyReportManageApi.route("/DailyReport/<cons_code>")
class projectDailyReportManage(Resource):
    """공사일지 api"""

    @api.doc(description="공사일지 작성")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("data", type=str, location="form", required=True),
        api.parser().add_argument("files", type=list, location="form", required=False),
    )
    def post(self, cons_code):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjDPMana = servProjectDailyReportManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공사일지 작성 api 시작 ----------",
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
                params.update({"cons_code": cons_code})
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 공사일보를 작성시도 하였습니다.",
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

            #################################### 해당 공사일지를 작성한다 ##########################

            resCd, msg, uuid = servProjDPMana.post_daily_report(
                cons_code,
                loginUserInfo["co_code"],
                params["cons_date"],
                loginUserInfo["id"],
                params["manager_name"],
                params["remarks"],
                params["temp"] if str(params["temp"]).isdigit() else '0',
                params["sky"] if str(params["sky"]).isdigit() else '0',
                params["pty"] if str(params["pty"]).isdigit() else '0',
                params["material_data"],
                params["workforce_data"],
                params["content_data"],
                params["photo_data"],
                params["auth_id"],
                request.files,
            )
            params.update({"cons_code": cons_code, "uuid": uuid})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 공사일보를 작성하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params.update({"cons_code": cons_code, "uuid": uuid})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 공사일보를 작성하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.doc(description="공사일지 상세조회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("uuid", type=str, location="querys", required=True),
    )
    def get(self, cons_code):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjDPMana = servProjectDailyReportManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공사일지 조회 api 시작 ----------",
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
                params = {"cons_code": cons_code, "uuid":uuid}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 공사일보를 조회시도 하였습니다.",
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
                and loginUserInfo["authority_code"] != constants.USER_BUYER
                and loginUserInfo["authority_code"] != constants.USER_DESIGNER
            ):
                params = {"cons_code": cons_code, "uuid":uuid}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 공사일보를 조회시도 하였습니다.",
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

            #################################### 해당 공사일지 목록을 조회한다 ##########################

            resCd, msg, WRData = servProjDPMana.get_daily_report(cons_code, uuid)
            params = {"cons_code": cons_code, "uuid":uuid}
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 공사일보를 조회하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, WRData)

        except Exception as e:
            params = {"cons_code": cons_code, "uuid":uuid}
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 공사일보를 조회하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.doc(description="공사일지 수정")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("data", type=str, location="form", required=True),
        api.parser().add_argument("files", type=list, location="form", required=False),
    )
    def put(self, cons_code):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjDPMana = servProjectDailyReportManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공사일지 수정 api 시작 ----------",
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
                params = {"cons_code": cons_code}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 공사일보를 수정시도 하였습니다.",
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
                params = {"cons_code": cons_code}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 공사일보를 수정시도 하였습니다.",
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

            #################################### 해당 공사일지 목록을 수정한다 ##########################

            resCd, msg, uuid = servProjDPMana.put_daily_report(
                cons_code,
                loginUserInfo["co_code"],
                params["cons_date"],
                params["post_uuid"],
                params["manager_name"] if "manager_name" in params else None,
                params["remarks"] if "remarks" in params else None,
                params["temp"] if "temp" in params else None,
                params["sky"] if "sky" in params else None,
                params["pty"] if "pty" in params else None,
                params["material_data"] if "material_data" in params else None,
                params["workforce_data"] if "workforce_data" in params else None,
                params["content_data"] if "content_data" in params else None,
                params["photo_data"] if "photo_data" in params else None,
                params["auth_id"] if "auth_id" in params else None,
                request.files,
            )
            params.update({"cons_code": cons_code, "uuid": params["post_uuid"]})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 공사일보를 수정하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params.update({"cons_code": cons_code, "uuid": params["post_uuid"]})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 공사일보를 수정하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.doc(description="공사일지 삭제")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("uuid", type=str, location="args", required=True),
    )
    def delete(self, cons_code):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjDPMana = servProjectDailyReportManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공사일지 삭제 api 시작 ----------",
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
                params = {"cons_code": cons_code, "uuid":uuid}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 공사일보를 삭제시도 하였습니다.",
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
                params = {"cons_code": cons_code, "uuid":uuid}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 공사일보를 삭제시도 하였습니다.",
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

            #################################### 해당 공사일지를 삭제한다 ##########################

            resCd, msg, _ = servProjDPMana.delete_daily_report(cons_code, uuid)
            params = {"cons_code": cons_code, "uuid":uuid}
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 공사일보를 삭제하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params = {"cons_code": cons_code, "uuid":uuid}
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 공사일보를 조회하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result


@projectDailyReportManageApi.route("/PhotoList/<cons_code>")
class projectPhotoListManage(Resource):
    """사진대지 리스트 조회 api"""

    @api.doc(description="사진대지 리스트 조회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument(
            "pc_name_keyword", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "writer_name_keyword", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "content_keyword", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "location_keyword", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "start_date", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "end_date", type=str, location="querys", required=False
        ),
    )
    def get(self, cons_code):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjDPMana = servProjectDailyReportManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 사진대지 조회 api 시작 ----------",
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
                params = {"cons_code": cons_code}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 사진대지 리스트를 조회시도 하였습니다.",
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
                and loginUserInfo["authority_code"] != constants.USER_BUYER
                and loginUserInfo["authority_code"] != constants.USER_DESIGNER
            ):
                params = {"cons_code": cons_code}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 사진대지 리스트를 조회시도 하였습니다.",
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
                "co_code": loginUserInfo["co_code"],
                "writer_name_keyword": "",
                "pc_name_keyword": "",
                "content_keyword": "",
                "location_keyword": "",
                "start_date": "",
                "end_date": "",
            }
            conditions = request.args.to_dict()
            allowed_keys = [
                "writer_name_keyword",
                "pc_name_keyword",
                "content_keyword",
                "location_keyword",
                "start_date",
                "end_date",
            ]
            for key in allowed_keys:
                if key in conditions:
                    params[key] = str(conditions.get(key))

            if loginUserInfo["authority_code"] == constants.USER_BUYER:
                params["co_code"] = ""

            #################################### 해당 공사일지 목록을 조회한다 ##########################

            resCd, msg, WRData = servProjDPMana.get_photo_list(
                cons_code,
                params["co_code"],
                params["writer_name_keyword"],
                params["pc_name_keyword"],
                params["content_keyword"],
                params["location_keyword"],
                params["start_date"],
                params["end_date"],
            )
            params.update({"cons_code": cons_code})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가 사진대지를 조회하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, WRData)

        except Exception as e:
            params.update({"cons_code": cons_code})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 사진대지를 조회하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

@projectDailyReportManageApi.route("/dailyReportStatus/<cons_code>")
class projectPhotoListManage(Resource):
    """공사 현황 조회 api"""

    @api.doc(description="공사 현황 조회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
    )
    def get(self, cons_code):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjDPMana = servProjectDailyReportManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공사 현황 조회 api 시작 ----------",
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
                params = {"cons_code": cons_code}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"식별하지 못한 사용자가 공사 현황 조회를 시도 하였습니다.",
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
            ):
                params = {"cons_code": cons_code}
                servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_WAR,
                                    f"권한없는 사용자가 공사 현황 조회를 시도 하였습니다.",
                                    json.dumps(cons_code, ensure_ascii=False), loginUserInfo.get("id", "") if loginUserInfo else "", resCd, msg)
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


            #################################### 해당 공사일지 목록을 조회한다 ##########################
            params = {'cons_code': cons_code}

            resCd, msg, WRData = servProjDPMana.get_daily_report_status(
                cons_code
            )
            params.update({"cons_code": cons_code})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_INFO,
                                   f"{loginUserInfo['id']} 사용자가  공사 현황을 조회하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, msg)
            return commServ.makeReturnMessage(resCd, msg, WRData)

        except Exception as e:
            params = {'cons_code': cons_code}
            params.update({"cons_code": cons_code})
            servLogManage.post_log(procCode, constants.LOG_LEVEL_CODE_CRI,
                                   f"{loginUserInfo['id']} 사용자가 공사 현황을 조회하던 중 에러가 발생하였습니다.",
                                   json.dumps(params, ensure_ascii=False), loginUserInfo['id'], resCd, str(e))
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result
