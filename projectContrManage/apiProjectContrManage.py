from flask import Blueprint, request
from flask_restx import Resource
import json
import copy
import os
import sys
import traceback
import uuid
from werkzeug.datastructures import FileStorage

from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import api

from common.logManage import logManage
from common import constants
from common.commUtilService import commUtilService
from common.commonService import commonService
from common.excelService import excelService
from userManage.servUserManage import servUserManage
from projectManage.sqlProjectManage import sqlProjectManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당

projectContrManageApi = api.namespace(
    "projectContrManageApi", description="프로젝트 시공정보 관리"
)


@projectContrManageApi.route("/projContr/<cons_code>")
class BasicConsInfoManage(Resource):
    """기본 공사정보 관리 api"""

    @api.response(200, "Success")
    @api.response(400, "Bad Request")
    @api.response(500, "Server Internal Error")
    @api.doc(description="시공사 공사기본정보 등록")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("data", type=str, location="form", required=True),
        api.parser().add_argument(
            "f_proc_details", type=FileStorage, location="files", required=True
        ),
    )
    def post(self, cons_code):
        commServ = commonService()
        servUserMana = servUserManage()
        servProjMana = servProjectManage()
        servCommMana = servCommManage()
        excelServ = excelService()
        try:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 프로젝트 기본 정보 저장 시작 ----------",
            )

            dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

            commUtilServ = commUtilService()
            sProMana = sqlProjectManage()
            sProjMana = sqlProjectManage()

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

            params["cons_code"] = cons_code
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
            resCd, msg, resData = dbms.queryForObject(query)

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

            #################################### 시공 기본 정보를 저장 할 수 있는 권한이 있는지 확인 한다. ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 시공 기본 정보를 저장 할 수 있는 권한이 있는지 확인 한다. ----------",
            )
            if (
                resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTOR
                and resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_MAIN
            ):

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL,
                    "시공 기본 정보를 입력 할 수 있는 권한이 없습니다.",
                    None,
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )
                return result

            #################################### 공정 상세 내역서가 있는지 확인 한다. ####################################
            if (params["proc_details_name"] == None) or (
                params["proc_details_name"] == ""
            ):
                params["proc_details_path"] = ""
                params["proc_details_original_name"] = ""
                params["proc_details_change_name"] = ""
            else:

                newDir = (
                    fileHome
                    + projectHome
                    + procDetails.replace("{projectCode}", params["cons_code"])
                )
                newDir = newDir.replace("{coCode}", loginUserInfo["co_code"])

                params["proc_details_path"] = newDir
                params["proc_details_original_name"] = params["proc_details_name"]
                name, ext = os.path.splitext(params["proc_details_name"])
                params["proc_details_change_name"] = str(uuid.uuid4()) + ext

                #################################### 디렉터리를 생성 한다. ####################################
                try:
                    if not os.path.exists(newDir):
                        os.makedirs(newDir)
                except:
                    Err = "디렉터리가 이미 생성되어 있습니다."

                #################################### 파일을 저장 한다. ####################################
                f_proc_details = request.files["f_proc_details"]
                f_proc_details.save(
                    params["proc_details_path"] + params["proc_details_change_name"]
                )
                f_proc_details.flush()

                #################################### 엑셀 파일 데이터를 Read 한다. ####################################
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "file_pah : "
                    + params["proc_details_path"]
                    + params["proc_details_change_name"],
                )
                dataList = excelServ.baseOnProcessDetails(
                    params["proc_details_path"] + params["proc_details_change_name"]
                )

                #################################### 공종 코드 정보를 가져 온다. ####################################
                resCd, msg, constrResData = servCommMana.getCodeList("FE00")

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

                ####################################  단위 코드 정보를 가져 온다. ####################################
                resCd, msg, unitResData = servCommMana.getCodeList("UN00")

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

                ####################################  직종 코드 정보를 가져 온다. ####################################
                resCd, msg, occResData = servCommMana.getCodeList("OC00")

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

                regDate = util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14)
                ####################################  공종 코드 정보와 단위 코드 정보를 비교한다. ####################################
                for data in dataList:
                    constrTypeCode = ""
                    unitCode = ""

                    for constr in constrResData:
                        if data["constr_type_name"] == constr["subcode_name"]:
                            constrTypeCode = constr["fullcode"]

                    for matInfo in data["material_list"]:
                        for unit in unitResData:
                            if matInfo["mat_ui_info"] == unit["subcode_name"]:
                                unitCode = unit["fullcode"]
                                break

                        resCd, msg, resData = servProjMana.putBaseOnProcDetails(
                            params["cons_code"],
                            loginUserInfo["co_code"],
                            constrTypeCode,
                            materialNum,
                            unitCode,
                            matInfo,
                            regDate,
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

                    for occInfo in data["occupation_list"]:
                        for occ in occResData:
                            if occInfo["mat_nm_info"] == occ["subcode_name"]:
                                occCode = occ["fullcode"]
                                break

                        for unit in unitResData:
                            if matInfo["mat_ui_info"] == unit["subcode_name"]:
                                unitCode = unit["fullcode"]
                                break

                        resCd, msg, resData = servProjMana.putBaseOnOccupationDetails(
                            params["cons_code"],
                            loginUserInfo["co_code"],
                            constrTypeCode,
                            occCode,
                            unitCode,
                            occInfo,
                            regDate,
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

            #################################### 시공 기본 정보를 저장 한다. ####################################
            params["co_code"] = loginUserInfo["co_code"]
            resCd, msg, resData = servProjMana.putContDefaultInfo(params)

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

            #################################### 작업 일지 작성 기준 정보를 저장 한다.####################################
            resCd, msg, resData = servProjMana.putWorkLogWriteStandard(
                params["cons_code"],
                loginUserInfo["co_code"],
                constants.WORK_LOG_WRITE_CD_YS,
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

            #################################### 시공 기본 정보 갱신 로그 데이터를 생성 한다. ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 시공 기본 정보 갱신 로그 데이터를 생성 한다. ----------",
            )

            logData = dLogManage.makeLogData(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                loginUserInfo["id"]
                + " 사용자가 시공 기본 정보를 업데이트 하였습니다. Project Code : "
                + params["cons_code"]
                + ", 회사 코드 : "
                + params["co_code"],
                util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
                loginUserInfo["id"],
            )

            query = sLogManage.iLogData(logData)
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "iLogData Query : " + query,
            )

            resCd, msg, resData = dbms.execute(query)  # 로그 저장 Query 실행
            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

            #################################### Response 데이터를 생성 한다. ####################################
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
                "---------- 공사 기본 정보를 저장한다. 종료 ----------",
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

    @api.doc(description="시공사 공사기본정보 조회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
    )
    def get(self, cons_code):
        commServ = commonService()
        servUserMana = servUserManage()
        servProjMana = servProjectManage()
        servCommMana = servCommManage()
        try:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 감리 및 시공사의 기본 정보 조회 시작 ----------",
            )

            dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

            commUtilServ = commUtilService()
            sCommMana = sqlCommManage()
            sProMana = sqlProjectManage()
            dLogManage = dataLogManage()
            sLogManage = sqlLogManage()
            sProjMana = sqlProjectManage()

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
                + cons_code,
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
            query = sProjMana.sGetJobTitleCdObj(cons_code, loginUserInfo["id"])
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "sGetJobTitleCdObj Query : " + query,
            )
            resCd, msg, resData = dbms.queryForObject(query)

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
                if (
                    loginUserInfo["authority_code"] == constants.USER_AUTH_BUYER
                    or loginUserInfo["authority_code"] == constants.USER_AUTH_DESIGNER
                    or loginUserInfo["authority_code"]
                    == constants.USER_AUTH_CONTRACTION
                    or loginUserInfo["authority_code"]
                    == constants.USER_AUTH_SUPERVISING
                    or loginUserInfo["authority_code"] == constants.USER_AUTH_WHITEHALL
                    or loginUserInfo["authority_code"]
                    == constants.USER_AUTH_INOCCUPATION
                ):

                    result = commServ.makeReturnMessage(
                        constants.REST_RESPONSE_CODE_DATAFAIL,
                        "현재 프로젝트 참여자가 아닙니다.",
                        None,
                    )

                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Response : " + commUtilServ.jsonDumps(result),
                    )

                    return result

            #################################### 시공 기본 정보를 조회 할 수 있는 권한이 있는지 확인 한다. ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 시공 기본 정보를 조회 할 수 있는 권한이 있는지 확인 한다. ----------",
            )

            coCode = ""
            if resData == None:
                if (
                    loginUserInfo["authority_code"] == constants.USER_AUTH_CONTRACTOR
                    or loginUserInfo["authority_code"]
                    == constants.USER_AUTH_CONTRACTOR_MONITOR
                ):
                    coCode = loginUserInfo["co_code"]
                elif (
                    loginUserInfo["authority_code"] == constants.USER_AUTH_SUPERVISOR
                    or loginUserInfo["authority_code"]
                    == constants.USER_AUTH_SUPERVISOR_MONITOR
                ):
                    coCode = ""
            elif (
                resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTOR
                and resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_MAIN
                and resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_SUB
                and resData["job_title_code"]
                != constants.JOB_TITLE_CD_CONTRACTOR_MONITOR
            ):
                coCode = ""
            else:
                coCode = loginUserInfo["co_code"]

            #################################### 시공사 기본 정보를 조회 한다. ####################################
            resCd, msg, resData = servProjMana.getContDefaultInfo(cons_code, coCode)
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

            #################################### Response 데이터를 생성 한다. ####################################
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
                "---------- 공사 기본 정보를 조회 한다. 종료 ----------",
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

    @api.doc(description="시공사 공사기본정보 수정")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
        api.parser().add_argument("data", type=str, location="form", required=True),
        api.parser().add_argument(
            "f_proc_details", type=FileStorage, location="files", required=True
        ),
    )
    def put(self, cons_code):
        commServ = commonService()
        servUserMana = servUserManage()
        servProjMana = servProjectManage()
        servCommMana = servCommManage()
        excelServ = excelService()
        servProjAppMatMana = servProjectApproMaterManage()
        try:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 감리 및 시공사의 기본 정보 수정 시작 ----------",
            )

            dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

            commUtilServ = commUtilService()
            sCommMana = sqlCommManage()
            sProMana = sqlProjectManage()
            dLogManage = dataLogManage()
            sLogManage = sqlLogManage()
            sProjMana = sqlProjectManage()

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

            params["cons_code"] = cons_code
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
            resCd, msg, resData = dbms.queryForObject(query)

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

            #################################### 시공 기본 정보를 저장 할 수 있는 권한이 있는지 확인 한다. ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 시공 기본 정보를 수정 할 수 있는 권한이 있는지 확인 한다. ----------",
            )
            if (
                resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTOR
                and resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_MAIN
            ):

                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL,
                    "시공 기본 정보를 입력 할 수 있는 권한이 없습니다.",
                    None,
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )
                return result

            #################################### 공정 상세 내역서가 수정 되었는지 확인 한다. ####################################

            if params["proc_details_status"] == "D":
                params["proc_details_path"] = ""
                params["proc_details_original_name"] = ""
                params["proc_details_change_name"] = ""
            elif params["proc_details_status"] == "C":
                newDir = (
                    fileHome
                    + projectHome
                    + procDetails.replace("{projectCode}", params["cons_code"])
                )
                newDir = newDir.replace("{coCode}", loginUserInfo["co_code"])

                params["proc_details_path"] = newDir
                params["proc_details_original_name"] = params["proc_details_name_new"]
                name, ext = os.path.splitext(params["proc_details_name_new"])
                params["proc_details_change_name"] = str(uuid.uuid4()) + ext

                #################################### 디렉터리를 생성 한다. ####################################
                try:
                    if not os.path.exists(newDir):
                        os.makedirs(newDir)
                except:
                    Err = "디렉터리가 이미 생성되어 있습니다."

                #################################### 파일을 저장 한다. ####################################
                f_proc_details = request.files["f_proc_details"]
                f_proc_details.save(
                    params["proc_details_path"] + params["proc_details_change_name"]
                )
                f_proc_details.flush()

                #################################### 엑셀 파일 데이터를 Read 한다. ####################################
                dataList = excelServ.baseOnProcessDetails(
                    params["proc_details_path"] + params["proc_details_change_name"]
                )

                #################################### 공종 코드 정보를 가져 온다. ####################################
                resCd, msg, constrResData = servCommMana.getCodeList("FE00")

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

                ####################################  단위 코드 정보를 가져 온다. ####################################
                resCd, msg, unitResData = servCommMana.getCodeList("UN00")

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

                ####################################  기존 기준 상세 공정 내역서 데이터는 삭제 한다. ####################################
                resCd, msg, resData = servProjMana.delBaseOnProcDetails(
                    params["cons_code"], loginUserInfo["co_code"]
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

                ####################################  공종 코드 정보와 단위 코드 정보를 비교한다. ####################################
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "---------------- : " + commUtilServ.jsonDumps(dataList),
                )
                regDate = util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14)
                for data in dataList:
                    constrTypeCode = ""
                    unitCode = ""

                    for constr in constrResData:
                        if data["constr_type_name"] == constr["subcode_name"]:
                            constrTypeCode = constr["fullcode"]

                    for matInfo in data["material_list"]:
                        for unit in unitResData:
                            if matInfo["mat_ui_info"] == unit["subcode_name"]:
                                unitCode = unit["fullcode"]
                                break

                        # 	searchList = {
                        # 		'search_material_name' : matInfo['mat_nm_info'],
                        # 		'search_standard' : matInfo['mat_st_info'],
                        # 		'search_produce_co' : '',
                        # 		'search_approval_num' : '',
                        # 		'search_start_approval_date' : '',
                        # 		'search_end_approval_date' : '',
                        # 		'search_formal_name' : '',
                        # 		'search_use_type' : '',
                        # 		'search_unit' : unitCode
                        # 	}

                        # 	logs.war(procName, os.path.basename(__file__), sys._getframe(0).f_code.co_name, u'------------------------------- 0 ')
                        # 	resCd, msg, materialInfo = servProjAppMatMana.getApproMaterList(searchList)
                        # 	logs.war(procName, os.path.basename(__file__), sys._getframe(0).f_code.co_name, u'------------------------------- 1 ')
                        materialNum = ""

                        # 	if(materialInfo != None) :
                        # 		materialNum = materialInfo['material_num']

                        resCd, msg, resData = servProjMana.putBaseOnProcDetails(
                            params["cons_code"],
                            loginUserInfo["co_code"],
                            constrTypeCode,
                            materialNum,
                            unitCode,
                            matInfo,
                            regDate,
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

                    for occInfo in data["occupation_list"]:
                        for occ in occResData:
                            if occInfo["mat_nm_info"] == occ["subcode_name"]:
                                occCode = occ["fullcode"]
                                break

                        for unit in unitResData:
                            if matInfo["mat_ui_info"] == unit["subcode_name"]:
                                unitCode = unit["fullcode"]
                                break

                        resCd, msg, resData = servProjMana.putBaseOnOccupationDetails(
                            params["cons_code"],
                            loginUserInfo["co_code"],
                            constrTypeCode,
                            occCode,
                            unitCode,
                            occInfo,
                            regDate,
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

            #################################### 시공 기본 정보를 수정 한다. ####################################
            params["co_code"] = loginUserInfo["co_code"]
            resCd, msg, resData = servProjMana.modifyContDefaultInfo(params)

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

            #################################### 시공 기본 정보 갱신 로그 데이터를 생성 한다. ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 시공 기본 정보 갱신 로그 데이터를 생성 한다. ----------",
            )

            logData = dLogManage.makeLogData(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                loginUserInfo["id"]
                + " 사용자가 시공 기본 정보를 업데이트 하였습니다. Project Code : "
                + params["cons_code"]
                + ", 회사 코드 : "
                + params["co_code"],
                util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
                loginUserInfo["id"],
            )

            query = sLogManage.iLogData(logData)
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "iLogData Query : " + query,
            )

            resCd, msg, resData = dbms.execute(query)  # 로그 저장 Query 실행
            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

            #################################### Response 데이터를 생성 한다. ####################################
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
                "---------- 공사 기본 정보를 저장한다. 종료 ----------",
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
