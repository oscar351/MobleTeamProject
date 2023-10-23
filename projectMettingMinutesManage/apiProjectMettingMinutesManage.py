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
from projectMettingMinutesManage.servProjectMettingMinutesManage import (
    servProjectMettingMinutesManage,
)

projectMettingMinutesManageApi = api.namespace(
    "projectMettingMinutesManageApi", description="회의록 관리"
)

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


@projectMettingMinutesManageApi.route("/MettingMinutesList/<cons_code>")
class projectMessageListManage(Resource):
    """회의록 게시글 리스트 조회 api"""

    @api.doc(description="회의록 게시글 리스트 조회")
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
            "title_keyword", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "content_keyword", type=str, location="querys", required=False
        ),
        api.parser().add_argument(
            "issued", type=str, location="querys", required=False
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
        servProjMBMana = servProjectMettingMinutesManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 회의록 get api 시작 ----------",
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
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"식별하지 못한 사용자가 회의록 리스트를 조회시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    "",
                    resCd,
                    msg
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None:
                params = {"cons_code": cons_code}
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"권한없는 사용자가 회의록 리스트를 조회시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    loginUserInfo.get("id", "") if loginUserInfo else "",
                    resCd,
                    msg
                )
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
                "title_keyword": "",
                "content_keyword": "",
                "issued": "",
                "reg_date_start": "",
                "reg_date_end": "",
            }
            conditions = request.args.to_dict()
            allowed_keys = {
                "co_name",
                "writer_name",
                "title_keyword",
                "content_keyword",
                "issued",
                "reg_date_start",
                "reg_date_end",
            }
            for key in allowed_keys:
                if key in conditions:
                    params[key] = str(conditions.get(key))

            #################################### 해당 게시글 목록을 조회한다 ##########################

            resCd, msg, WRData = servProjMBMana.get_message_list(
                cons_code,
                params["co_name"],
                params["writer_name"],
                params["title_keyword"],
                params["content_keyword"],
                params["issued"],
                params["reg_date_start"],
                params["reg_date_end"],
            )
            result = {
                "count": len(WRData) if WRData else 0,
                "data": WRData[params["start_num"] : params["end_num"]],
            }
            params.update({"cons_code": cons_code})
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                f"{loginUserInfo['id']} 사용자가 회의록 리스트를 조회하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                msg
            )
            return commServ.makeReturnMessage(resCd, msg, result)

        except Exception as e:
            params.update({"cons_code": cons_code})
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_CRI,
                f"{loginUserInfo['id']} 사용자가 회의록 리스트를 조회하던 중 에러가 발생하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                str(e)
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result


@projectMettingMinutesManageApi.route("/MettingMinutes/<cons_code>")
class projectMessageManage(Resource):
    """회의록 관리 api"""

    @api.doc(description="회의록 작성")
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
        servProjMBMana = servProjectMettingMinutesManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 회의록 post api 시작 ----------",
        )

        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")
            params = json.loads(request.form["data"], encoding="utf-8")

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
                params = {"cons_code": cons_code}
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"식별하지 못한 사용자가 회의록을 작성시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    "",
                    resCd,
                    msg
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None:
                params = {"cons_code": cons_code}
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"권한없는 사용자가 회의록을 작성시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    loginUserInfo.get("id", "") if loginUserInfo else "",
                    resCd,
                    msg
                )
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

            #################################### 해당 게시글을 작성한다 ##########################

            resCd, msg, uuid = servProjMBMana.post_message(
                cons_code,
                loginUserInfo["id"],
                params["title"],
                params["content"],
                request.files,
            )
            params.update({"cons_code": cons_code, "uuid": uuid})
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                f"{loginUserInfo['id']} 사용자가 회의록을 작성하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                msg
            )
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params.update({"cons_code": cons_code, "uuid": uuid})
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_CRI,
                f"{loginUserInfo['id']} 사용자가 회의록을 작성하던 중 에러가 발생하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                msg
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.doc(description="회의록 조회")
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
        servProjMBMana = servProjectMettingMinutesManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 회의록 get api 시작 ----------",
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
                params = {"cons_code": cons_code, "uuid": uuid}
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"식별하지 못한 사용자가 회의록을 조회시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    "",
                    resCd,
                    msg
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None:
                params = {"cons_code": cons_code, "uuid": uuid}
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"권한없는 사용자가 회의록을 조회시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    loginUserInfo.get("id", "") if loginUserInfo else "",
                    resCd,
                    msg
                )
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

            resCd, msg, WRData = servProjMBMana.get_message(cons_code, uuid)
            params = {"cons_code": cons_code, "uuid": uuid}
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                f"{loginUserInfo['id']} 사용자가 회의록을 조회하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                msg
            )
            return commServ.makeReturnMessage(resCd, msg, WRData)

        except Exception as e:
            params = {"cons_code": cons_code, "uuid": uuid}
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_CRI,
                f"{loginUserInfo['id']} 사용자가 회의록을 조회하던 중 에러가 발생하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                str(e)
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.doc(description="회의록 수정")
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
        servProjMBMana = servProjectMettingMinutesManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 회의록 update api 시작 ----------",
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
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"식별하지 못한 사용자가 회의록을 수정시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    "",
                    resCd,
                    msg
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None:
                params.update({"cons_code": cons_code})
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"권한없는 사용자가 회의록을 수정시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    loginUserInfo.get("id", "") if loginUserInfo else "",
                    resCd,
                    msg
                )
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

            if not "title" in params:
                params["title"] = None
            if not "content" in params:
                params["content"] = None
            if not "indexes" in params:
                params["indexes"] = None

            resCd, msg, _ = servProjMBMana.put_message(
                cons_code,
                params["uuid"],
                params["title"],
                params["content"],
                params["indexes"],
                request.files,
            )
            params.update({"cons_code": cons_code})
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                f"{loginUserInfo['id']} 사용자가 회의록을 수정하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                msg
            )
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params.update({"cons_code": cons_code})
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_CRI,
                f"{loginUserInfo['id']} 사용자가 회의록을 수정하던 중 에러가 발생하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                str(e)
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.doc(description="회의록 삭제")
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
        servProjMBMana = servProjectMettingMinutesManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 회의록 delete api 시작 ----------",
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
                params = {"cons_code": cons_code, "uuid": uuid}
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"식별하지 못한 사용자가 회의록을 삭제시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    "",
                    resCd,
                    msg
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None:
                params = {"cons_code": cons_code, "uuid": uuid}
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"권한없는 사용자가 회의록을 삭제시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    loginUserInfo.get("id", "") if loginUserInfo else "",
                    resCd,
                    msg
                )
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

            #################################### 해당 회의록을 삭제한다 ##########################

            resCd, msg, _ = servProjMBMana.del_message(cons_code, uuid)
            params = {"cons_code": cons_code, "uuid": uuid}
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                f"{loginUserInfo['id']} 사용자가 회의록을 삭제하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                msg
            )
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params = {"cons_code": cons_code, "uuid": uuid}
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_CRI,
                f"{loginUserInfo['id']} 사용자가 회의록을 삭제하던 중 에러가 발생하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                str(e)
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result


@projectMettingMinutesManageApi.route("/MettingMinutesLock/<cons_code>/<uuid>")
class projectMessageManage(Resource):
    """회의록 검토관리 api"""

    @api.doc(description="회의록 검토상태 변경")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("issued", type=str, location="json", required=True),
    )
    def post(self, cons_code, uuid):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjMana = servProjectManage()
        servProjMBMana = servProjectMettingMinutesManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 회의록 검토완료/해제 api 시작 ----------",
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
                params.update({"cons_code": cons_code})
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"식별하지 못한 사용자가 회의록을 잠금시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    "",
                    resCd,
                    msg
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None:
                params.update({"cons_code": cons_code})
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"권한없는 사용자가 회의록을 잠금시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    loginUserInfo.get("id", "") if loginUserInfo else "",
                    resCd,
                    msg
                )
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

            #################################### 해당 게시글을 잠금/해제한다 ##########################

            resCd, msg, _ = servProjMBMana.lock_message(
                cons_code,
                uuid,
                params["issued"],
            )
            params.update({"cons_code": cons_code})
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                f"{loginUserInfo['id']} 사용자가 회의글을 잠금하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                msg
            )
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params.update({"cons_code": cons_code})
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_CRI,
                f"{loginUserInfo['id']} 사용자가 회의글을 잠금하던 중 에러가 발생하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                str(e)
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result


@projectMettingMinutesManageApi.route("/MettingMinutesReply/<post_uuid>")
class projectMessageReplyManage(Resource):
    """회의록 댓글 관리 api"""

    @api.doc(description="회의록 댓글 작성")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument(
            "parent_uuid", type=str, location="args", required=False
        ),
        api.parser().add_argument("content", type=str, location="json", required=True),
    )
    def post(self, post_uuid):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjMBMana = servProjectMettingMinutesManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 회의록 댓글 post api 시작 ----------",
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
                params.update(
                    {"post_uuid": post_uuid, "parent_uuid": parent_uuid}
                )
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"식별하지 못한 사용자가 회의록 댓글을 작성시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    "",
                    resCd,
                    msg
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None:
                params.update(
                    {"post_uuid": post_uuid, "parent_uuid": parent_uuid}
                )
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"권한없는 사용자가 회의록 댓글을 작성시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    loginUserInfo.get("id", "") if loginUserInfo else "",
                    resCd,
                    msg
                )
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

            #################################### 해당 댓글을 작성한다 ##########################

            resCd, msg, _ = servProjMBMana.post_reply(
                post_uuid, parent_uuid, loginUserInfo["id"], params["content"]
            )
            params.update(
                {"post_uuid": post_uuid, "parent_uuid": parent_uuid}
            )
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                f"{loginUserInfo['id']} 사용자가 회의록 댓글을 작성하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                msg
            )
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params.update(
                {"post_uuid": post_uuid, "parent_uuid": parent_uuid}
            )
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_CRI,
                f"{loginUserInfo['id']} 사용자가 회의록 댓글을 작성하던 중 에러가 발생하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                str(e)
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.doc(description="회의록 조회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument(
            "parent_uuid", type=str, location="querys", required=False
        ),
    )
    def get(self, post_uuid):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servHisMana = servHistoryManage()
        servProjMBMana = servProjectMettingMinutesManage()

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
                params = {
                    "post_uuid": post_uuid,
                    "parent_uuid": parent_uuid,
                }
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"식별하지 못한 사용자가 회의록 댓글을 조회시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    "",
                    resCd,
                    msg
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None:
                params = {
                    "post_uuid": post_uuid,
                    "parent_uuid": parent_uuid,
                }
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"권한없는 사용자가 회의록 댓글을 조회시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    loginUserInfo.get("id", "") if loginUserInfo else "",
                    resCd,
                    msg
                )
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

            #################################### 해당 댓글을 조회한다 ##########################

            resCd, msg, WRData = servProjMBMana.get_reply(post_uuid, parent_uuid)
            params = {"post_uuid": post_uuid, "parent_uuid": parent_uuid}
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                f"{loginUserInfo['id']} 사용자가 회의록 댓글을 조회하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                msg
            )
            return commServ.makeReturnMessage(resCd, msg, WRData)

        except Exception as e:
            params = {"post_uuid": post_uuid, "parent_uuid": parent_uuid}
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_CRI,
                f"{loginUserInfo['id']} 사용자가 회의록 댓글을 조회하던 중 에러가 발생하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                str(e)
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.doc(description="회의록 수정")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("uuid", type=str, location="args", required=True),
        api.parser().add_argument("content", type=str, location="json", required=True),
    )
    def put(self, post_uuid):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjMana = servProjectManage()
        servProjMBMana = servProjectMettingMinutesManage()

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
                params.update({"post_uuid": post_uuid, "uuid": uuid})
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"식별하지 못한 사용자가 회의록 댓글을 수정시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    "",
                    resCd,
                    msg
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None:
                params.update({"post_uuid": post_uuid, "uuid": uuid})
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"권한없는 사용자가 회의록 댓글을 수정시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    loginUserInfo.get("id", "") if loginUserInfo else "",
                    resCd,
                    msg
                )
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

            #################################### 해당 댓글을 수정한다 ##########################

            resCd, msg, _ = servProjMBMana.put_reply(post_uuid, uuid, params["content"])
            params.update({"post_uuid": post_uuid, "uuid": uuid})
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                f"{loginUserInfo['id']} 사용자가 회의록 댓글을 수정하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                msg
            )
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params.update({"post_uuid": post_uuid, "uuid": uuid})
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_CRI,
                f"{loginUserInfo['id']} 사용자가 회의록 댓글을 수정하던 중 에러가 발생하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                str(e)
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result

    @api.doc(description="회의록 삭제")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("uuid", type=str, location="args", required=True),
    )
    def delete(self, post_uuid):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjMana = servProjectManage()
        servProjMBMana = servProjectMettingMinutesManage()

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
                params = {"post_uuid": post_uuid, "uuid": uuid}
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"식별하지 못한 사용자가 회의록 댓글을 삭제시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    "",
                    resCd,
                    msg
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

                result = commServ.makeReturnMessage(resCd, msg, None)

                return result

            if loginUserInfo == None:
                params = {"post_uuid": post_uuid, "uuid": uuid}
                servLogManage.post_log(
                    procCode,
                    constants.LOG_LEVEL_CODE_WAR,
                    f"권한없는 사용자가 회의록 댓글을 삭제시도 하였습니다.",
                    json.dumps(params, ensure_ascii=False),
                    loginUserInfo.get("id", "") if loginUserInfo else "",
                    resCd,
                    msg
                )
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

            #################################### 해당 댓글을 삭제한다 ##########################

            resCd, msg, _ = servProjMBMana.del_reply(post_uuid, uuid)
            params = {"post_uuid": post_uuid, "uuid": uuid}
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                f"{loginUserInfo['id']} 사용자가 회의록 댓글을 삭제하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                msg
            )
            return commServ.makeReturnMessage(resCd, msg, None)

        except Exception as e:
            params = {"post_uuid": post_uuid, "uuid": uuid}
            servLogManage.post_log(
                procCode,
                constants.LOG_LEVEL_CODE_CRI,
                f"{loginUserInfo['id']} 사용자가 회의록 댓글을 삭제하던 중 에러가 발생하였습니다.",
                json.dumps(params, ensure_ascii=False),
                loginUserInfo["id"],
                resCd,
                str(e)
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        return result
