# _*_coding: utf-8 -*-

# Project 관리 REST API
# 작성 날짜 : 2022. 08. 25
# 작성자 : 황희정


from flask import Blueprint, request
import json
import copy
import os
import sys
import traceback
import uuid

# from ast import literal_eval

projectManageApi = Blueprint("projectManageApi", __name__)

from projectManage.servProjectManage import servProjectManage

# user import
from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import procCode
from allscapeAPIMain import api
from allscapeAPIMain import weatherApi
from allscapeAPIMain import fileHome
from allscapeAPIMain import projectHome
from allscapeAPIMain import procDetails

from common.logManage import logManage
from common import util_time
from common import constants
from common.commUtilService import commUtilService
from common.commonService import commonService
from common.messageService import messageService
from common.excelService import excelService
from logManage.dataLogManage import dataLogManage
from logManage.sqlLogManage import sqlLogManage

# from commManage.sqlCommManage import sqlCommManage
# from commManage.dataCommManage import dataCommManage
from userManage.servUserManage import servUserManage
from userManage.sqlUserManage import sqlUserManage

from commManage.servCommManage import servCommManage
from commManage.sqlCommManage import sqlCommManage

from projectManage.sqlProjectManage import sqlProjectManage
from projectApproMaterManage.servProjectApproMaterManage import (
    servProjectApproMaterManage,
)

from companyManage.servCompanyManage import servCompanyManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


# 1. 프로젝트 추가 API 조현우
#
# Parameter
@projectManageApi.route("/addProject", methods=["PUT"])
def addProject():
    # classInfo['procName'] = procName
    # classInfo['fileName'] = os.path.basename(__file__)
    # classInfo['funcName'] = sys._getframe(0).f_code.co_name

    commServ = commonService()
    servUserMana = servUserManage()
    servCompMana = servCompanyManage()
    servProMana = servProjectManage()
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 추가----------",
        )

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        commUtilServ = commUtilService()
        sCommMana = sqlCommManage()
        sProMana = sqlProjectManage()
        sUserManage = sqlUserManage()
        dLogManage = dataLogManage()
        sLogManage = sqlLogManage()

        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        params = request.get_json()  # login parameter recv

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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

        # 책임 감리원을 체크 한다.
        # 		if(commUtilServ.dataCheck(respSupervisor) == False):
        # 			result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
        # 					u'책임 감리원을 입력하여 주시기 바랍니다.',
        # 					None)

        # 			logs.war(procName,
        # 					os.path.basename(__file__),
        # 					sys._getframe(0).f_code.co_name,
        # 					u'Response : ' + commUtilServ.jsonDumps(result))

        # 			return result

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

        #################################### 프로젝트 생성 권한이 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 생성 권한이 있는지 확인 한다. ----------",
        )
        if (loginUserInfo["authority_code"] != constants.USER_MONITOR) and (
            loginUserInfo["user_state"] != constants.APPRO_STATUS_CD_APPRO
        ):
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "프로젝트 생성 권한이 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        # 프로젝트 명을 체크 한다.
        if commUtilServ.dataCheck(params["projectName"]) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "프로젝트 명을 입력하여 주시기 바랍니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        """
        #################################### 책임 감리원 정보를 가져 온다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 책임 감리원 정보를 가져 온다. ----------",
        )
        # 사용자 정보를 가져 온다.
        supervisorUserInfo = None
        if respSupervisor != "":
            resCd, msg, supervisorUserInfo = servUserMana.getUserInfo(
                1, respSupervisor, sysCd
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

        # 		if(supervisorUserInfo == None):
        # 			result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_DATAFAIL,
        # 					u'감리원 정보가 없습니다. 감리원 정보를 확인 하시기 바랍니다.',
        # 					None)
        # 			logs.war(procName,
        # 					os.path.basename(__file__),
        # 					sys._getframe(0).f_code.co_name,
        # 					u'Response : ' + commUtilServ.jsonDumps(result))
        """
        #################################### 프로젝트 생성 권한을 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 생성 권한을 확인 한다. ----------",
        )
        if (
            loginUserInfo["authority_code"] != constants.USER_MONITOR
            and loginUserInfo["authority_code"] != constants.USER_AUTH_SUPERVISOR
        ):
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "프로젝트 생성 권한이 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 프로젝트 코드를 생성 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 코드를 생성 한다. ----------",
        )
        query = sCommMana.sGetSysCfg("cfg_project_num")
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetSysCfg Query : " + query,
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

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        number = int(resData["cfg_value"])
        newProjectCd = "P" + str(f"{number:011d}")  # 프로젝트 코드 생성

        number += 1

        # 프로젝트 코드 설정 값을 업데이트 한다.
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 코드 설정 값을 업데이트 한다. ----------",
        )

        # query = sCommMana.uUpdateSysCfg('cfg_project_num', str(number))
        query = sCommMana.uModifySysCfg("cfg_project_num", str(number))
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uModifySysCfg Query : " + query,
        )
        resCd, msg, resData = dbms.execute(query)
        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + commUtilServ.jsonDumps(msg),
            )

            result = commServ.makeReturnMessage(resCd, msg, None)

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 프로젝트 테이블에 프로젝트 명과 코드를 추가 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 테이블에 프로젝트 명과 코드를 추가 한다. ----------",
        )
        query = sProMana.iPutProject(
            newProjectCd, params["projectName"], loginUserInfo["co_code"]
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iAddProject Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)
        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + commUtilServ.jsonDumps(msg),
            )

            # 프로젝트를 추가 하지 못했을 경우 프로젝트 코드 설정 번호를 다시 원래 상태로 되돌린다.
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 프로젝트를 추가 하지 못했을 경우 프로젝트 코드 설정 번호를 다시 원래 상태로 되돌린다. ----------",
            )
            number -= 1
            # query = sCommMana.uUpdateSysCfg('cfg_project_num', str(number))
            query = sCommMana.uModifySysCfg("cfg_project_num", str(number))

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "uModifySysCfg Query : " + query,
            )
            dbms.execute(query)

            result = commServ.makeReturnMessage(resCd, msg, None)

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 프로젝트 생성 로그 데이터를 생성 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 생성 로그 데이터를 생성 하고 저장 한다. ----------",
        )

        logData = dLogManage.makeLogData(
            procCode,
            constants.LOG_LEVEL_CODE_INFO,
            "프로젝트가 생성 되었습니다. PROJECT CODE : "
            + newProjectCd
            + ", 프로젝트 명 : "
            + params["projectName"],
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

        resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그 저장 Query 실행
        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + commUtilServ.jsonDumps(msg),
            )

        #################################### 프로젝트 참여 인력 테이블에 감리자 및 책임감리원을 추가 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 참여 인력 테이블에 감리자 및 책임 감리원을 추가 한다. ----------",
        )

        if params["joinUserList"]:
            """
            supervisorUserInfo[
                "job_title_code"
            ] = constants.JOB_TITLE_CD_SUPERVISING_MAIN
            if loginUserInfo["authority_code"] == constants.USER_AUTH_SUPERVISOR:
                loginUserInfo["job_title_code"] = constants.JOB_TITLE_CD_SUPERVISOR
            # 	userList = [loginUserInfo, supervisorUserInfo]
            else:
                loginUserInfo[
                    "job_title_code"
                ] = constants.JOB_TITLE_CD_SUPERVISOR_MONITOR
                # 감리자 정보를 가져 온다.
                # supervisorInfo['job_title_code'] = constants.JOB_TITLE_CD_SUPERVISOR
                # userList = [supervisorInfo, loginUserInfo, supervisorUserInfo]
            """
            userList = [loginUserInfo, params["joinUserList"]]
        else:
            """
            loginUserInfo["job_title_code"] = constants.JOB_TITLE_CD_SUPERVISOR_MONITOR
            """
            userList = [loginUserInfo]
            # if(loginUserInfo['authority_code'] == constants.USER_AUTH_SUPERVISOR):
            # 	loginUserInfo['job_title_code'] = constants.JOB_TITLE_CD_SUPERVISOR
            # 	userList = [loginUserInfo, supervisorUserInfo]
            # else:
            # 	loginUserInfo['job_title_code'] = constants.JOB_TITLE_CD_SUPERVISOR_MONITOR
            # 감리자 정보를 가져 온다.
            # supervisorInfo['job_title_code'] = constants.JOB_TITLE_CD_SUPERVISOR
            # userList = [supervisorInfo, loginUserInfo, supervisorUserInfo]
            # 	userList = [loginUserInfo, supervisorUserInfo]

        query = sProMana.iPutJoinWorkforce(newProjectCd, params["joinUserList"])
        # query = sProMana.iPutJoinWorkforce(newProjectCd, userList)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutJoinWorkforce Query : " + query,
        )
        resCd, msg, resData = dbms.execute(query)

        #### 프로젝트 상세정보도 추가한다 ####
        if resCd == 0:
            resCd, msg, resData = servProMana.updateProjDefaultInfo(
                newProjectCd, params["projectInfo"], "A"
            )

        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + commUtilServ.jsonDumps(msg),
            )

            # 인원을 추가 하지 못했을 경우 프로젝트 코드 설정 번호를 다시 원래 상태로 되돌린다.
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 인원을 추가 하지 못했을 경우 프로젝트 코드 설정 번호를 다시 원래 상태로 되돌린다. ----------",
            )
            number -= 1
            # query = sCommMana.uUpdateSysCfg('cfg_project_num', str(number))
            query = sCommMana.uModifySysCfg("cfg_project_num", str(number))
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "uModifySysCfg Query : " + query,
            )
            dbms.execute(query)

            # 인원을 추가 하지 못했을 경우 저장된 프로젝트를 삭제 한다.
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 인원을 추가 하지 못했을 경우 저장된 프로젝트를 삭제 한다. ----------",
            )

            query = sProMana.dDelProject(newProjectCd)
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "dRemoveProject Query : " + query,
            )

            dbms.execute(query)

            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "프로젝트 생성중 오류가 발생하였습니다. 관리자에게 문의 하시기 바랍니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result
            """
            #################################### 책임 감리원 등록 로그 데이터를 생성 한다. ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 책임 감리원 등록 데이터를 생성 하고 저장 한다. ----------",
            )

            logData = dLogManage.makeLogData(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                loginUserInfo["user_name"]
                + "("
                + loginUserInfo["id"]
                + ")"
                + "사용자가 "
                + supervisorUserInfo["user_name"]
                + "("
                + supervisorUserInfo["id"]
                + ")"
                + " 감리원을 "
                + projectName
                + "의 책임감리원으로 등록하였습니다.",
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

        #################################### 감리 업무에 사용 되는 문서의 문서번호를 생성 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 감리 업무에 사용 되는 문서의 문서번호를 생성 한다. ----------",
        )

        query = sCommMana.sGetCodeList("SD00")
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetCodeList Query : " + query,
        )

        # resCd, msg, resData = dbms.query(query)
        resCd, msg, resDocList = dbms.query(query)
        if resCd != 0:  # DB 에러 발생 시
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + commUtilServ.jsonDumps(msg),
            )

            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "문서 번호 생성 중 에러가 발생하였습니다. 문서 번호 설정 화면에서 생성 하시기 바랍니다.",
                None,
            )

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        if resDocList == None:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + commUtilServ.jsonDumps(msg),
            )

            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "문서 정보가 존재하지 않아 문서 번소를 생성 할 수 없습니다. 관리자에게 문의 하시기 바랍니다.",
                None,
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        query = sProMana.iPutDocnumManage(
            newProjectCd,
            loginUserInfo["co_code"],
            json.loads(json.dumps(resDocList, ensure_ascii=False)),
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutDocnumManage Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)
        if resCd != 0:  # DB 에러 발생 시
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + commUtilServ.jsonDumps(msg),
            )

            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "문서 번호 생성 중 에러가 발생하였습니다. 문서 번호 설정 화면에서 생성 하시기 바랍니다.",
                None,
            )

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 감리원 문서 등록 로그 데이터를 생성 한다. ####################################
        if supervisorUserInfo != None:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 감리원 문서 등록 로그 데이터를 생성 한다. ----------",
            )

            logData = dLogManage.makeLogData(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                projectName
                + "("
                + newProjectCd
                + ") "
                + supervisorUserInfo["co_name"]
                + "("
                + supervisorUserInfo["co_code"]
                + ")"
                + " 감리 문서가 "
                + str(resDocList.__len__())
                + "건이 등록 되었습니다.",
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
        """
        resData = {"projectCd": newProjectCd}

        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_ZERO, "", resData
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
            "---------- 프로젝트 추가 종료 ----------",
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


# 프로젝트 참여 인력 추가 API
#
# Parameter
@projectManageApi.route("/addJoinWorkforce", methods=["POST"])
def addJoinWorkforce():
    commServ = commonService()
    servUserMana = servUserManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 참여 인력 추가 ----------",
        )

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        commUtilServ = commUtilService()
        sCommMana = sqlCommManage()
        sProMana = sqlProjectManage()
        sUserManage = sqlUserManage()
        dLogManage = dataLogManage()
        sLogManage = sqlLogManage()

        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        # params = {}  # login parameter recv
        # params.update(json.loads(request.form["data"], encoding="utf-8"))
        params = request.get_json()  # login parameter recv

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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

        consCode = params["cons_code"]
        userList = params["user_list"]

        # 프로젝트 코드를 체크 한다.
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

        #################################### 프로젝트 사용자 추가 권한을 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 사용자 추가 권한을 확인 한다. ----------",
        )
        if not (
            loginUserInfo["authority_code"] == constants.USER_MASTER
            or loginUserInfo["authority_code"] == constants.USER_MONITOR
        ):
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "프로젝트 사용자 추가 권한이 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        """
        # 직책 구분을 체크 한다.
        if commUtilServ.dataCheck(jobType) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "직책 구분을 입력하여 주시기 바랍니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result
        """

        # 저장 ID 데이터를 체크 한다.
        if (userList == None) or (len(userList) == 0):
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "프로젝트 참여 인력 정보를 확인하여 주시기 바랍니다.",
                None,
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        """
        #################################### 프로젝트 참여 직책 정보를 가져 온다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 참여 직책 정보를 가져온다. ----------",
        )
        query = sProMana.sGetJobTitleCdObj(consCode, loginUserInfo["id"])
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetbTitleCdObj Query : " + query,
        )
        resCd, msg, resData = dbms.queryForObject(query)
        consName = resData["cons_name"]

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
                constants.REST_RESPONSE_CODE_DATAFAIL, "책임 감리원 정보가 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result
        """

        """
        #################################### 데이터를 체크 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 데이터를 체크 한다. ----------",
        )

        checkResult = True

        for info in userList:

            if jobType == "0":  # 발주처
                if info["job_title_code"] != constants.JOB_TITLE_CD_BUYER:
                    checkResult = False
            elif jobType == "1":  # 설계사
                if info["job_title_code"] != constants.JOB_TITLE_CD_DESIGNER:
                    checkResult = False
            elif jobType == "2":  # 시공
                if (
                    (info["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTOR)
                    and (
                        info["job_title_code"]
                        != constants.JOB_TITLE_CD_CONTRACTION_MAIN
                    )
                    and (
                        info["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_SUB
                    )
                    and (
                        info["job_title_code"]
                        != constants.JOB_TITLE_CD_CONTRACTOR_MONITOR
                    )
                ):
                    checkResult = False
            elif jobType == "3":  # 감리
                if (
                    (info["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN)
                    and (
                        info["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_SUB
                    )
                    and (
                        info["job_title_code"]
                        != constants.JOB_TITLE_CD_SUPERVISOR_MONITOR
                    )
                ):
                    checkResult = False
            elif jobType == "4":  # 관/청
                if info["job_title_code"] != constants.JOB_TITLE_CD_WHITEHALL:
                    checkResult = False
            else:
                checkResult = False

        if checkResult == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "잘못된 데이터가 입력 되었습니다. 데이터를 확인 하시기 바랍니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result
        """

        #################################### 프로젝트 참여자 권한 코드를 가져온다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 참여자 권한 코드를 가져온다. ----------",
        )
        query = sUserManage.sUserInfoList(userList)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sUserInfoList Query : " + query,
        )
        resCd, msg, resData = dbms.query(query)
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
                constants.REST_RESPONSE_CODE_DATAFAIL, "참여 인력의 정보를 불러 올 수 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        userInfo = json.loads(json.dumps(resData, ensure_ascii=False))

        #################################### 기존 데이터에 권한 코드를 추가 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 기존 코드에 권한 코드를 추가 한다. ----------",
        )
        size = userList.__len__()

        for num in range(0, size):
            for data in userInfo:
                if userList[num]["id"] == data["id"]:
                    userList[num]["authority_code"] = data["authority_code"]

            num += 1

        #################################### 프로젝트 참여 인력을 저장 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 참여 인력을 저장한다. ----------",
        )

        # query  = sProMana.iAddJoinWorkforce(consCode, userList)
        query = sProMana.iPutJoinWorkforce(consCode, userList)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutJoinWorkforce Query : " + query,
        )
        resCd, msg, resData = dbms.execute(query)
        # Error 발생 시 에러 코드 리턴
        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + msg,
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

        #################################### 사용자의 회사 코드를 중복 제거 후 리스트에 저장 한다. ####################################
        coCodeList = []
        #        if jobType == "2":  # 시공
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 사용자의 회사 코드를 중복 제거 후 리스트에 저장한다. ----------",
        )
        coCodeName = ""

        for data in userInfo:
            # if(data['co_code'] != '') and (data['co_code'] not in coCodeList):
            if data["co_code"] not in coCodeList == True:
                #################################### 문서가 저장 되어 있는지 확인 한다. ####################################
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "---------- 프로젝트에 문서가 저장되어 있는지 확인 한다. ----------",
                )

                query = sProMana.sCheckDocInProject(consCode, data["co_code"])

                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "sCheckDocInProject Query : " + query,
                )

                resCd, msg, resData = dbms.queryForObject(query)
                if resCd != 0:  # DB 에러 발생 시
                    logs.war(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Database Error : " + commUtilServ.jsonDumps(msg),
                    )

                    result = commServ.makeReturnMessage(
                        constants.REST_RESPONSE_CODE_DATAFAIL,
                        "문서 번호 생성 중 에러가 발생하였습니다. 문서 번호 설정 화면에서 생성 하시기 바랍니다.",
                        None,
                    )

                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "Response : " + commUtilServ.jsonDumps(result),
                    )
                    return result

                if resData["cnt"] == 0:
                    coInfo = {
                        "co_code": data["co_code"],
                        "co_name": data["co_name"],
                    }
                    coCodeList.append(coInfo)
                    # coCodeList.append(data['co_code'])

    #        if coCodeList.__len__() > 0:
    #################################### 시공 업무에 사용 되는 문서의 문서번호를 생성 한다. ####################################
    #            logs.debug(
    #                procName,
    #                os.path.basename(__file__),
    #                sys._getframe(0).f_code.co_name,
    #                "---------- 시공 업무에 사용 되는 문서의 문서번호를 생성 한다. ----------",
    #            )

    #            query = sCommMana.sGetCodeList("CD00")
    #            logs.debug(
    #                procName,
    #                os.path.basename(__file__),
    #                sys._getframe(0).f_code.co_name,
    #                "sGetCodeList Query : " + query,
    #            )

    #            resCd, msg, resDocList = dbms.query(query)
    #            if resCd != 0:  # DB 에러 발생 시
    #                logs.war(
    #                    procName,
    #                    os.path.basename(__file__),
    #                    sys._getframe(0).f_code.co_name,
    #                    "Database Error : " + commUtilServ.jsonDumps(msg),
    #                )

    #                result = commServ.makeReturnMessage(
    #                    constants.REST_RESPONSE_CODE_DATAFAIL,
    #                    "문서 번호 생성 중 에러가 발생하였습니다. 문서 번호 설정 화면에서 생성 하시기 바랍니다.",
    #                    None,
    #                )

    #                logs.debug(
    #                    procName,
    #                    os.path.basename(__file__),
    #                    sys._getframe(0).f_code.co_name,
    #                    "Response : " + commUtilServ.jsonDumps(result),
    #                )
    #                return result

    #            if resDocList == None:
    #                logs.war(
    #                    procName,
    #                    os.path.basename(__file__),
    #                    sys._getframe(0).f_code.co_name,
    #                    "Database Error : " + commUtilServ.jsonDumps(msg),
    #                )

    #                result = commServ.makeReturnMessage(
    #                    constants.REST_RESPONSE_CODE_DATAFAIL,
    #                    "문서 정보가 존재하지 않아 문서 번소를 생성 할 수 없습니다. 관리자에게 문의 하시기 바랍니다.",
    #                    None,
    #                )

    #                logs.war(
    #                    procName,
    #                    os.path.basename(__file__),
    #                    sys._getframe(0).f_code.co_name,
    #                    "Response : " + commUtilServ.jsonDumps(result),
    #                )
    #                return result

    #            logs.debug(
    #                procName,
    #                os.path.basename(__file__),
    #                sys._getframe(0).f_code.co_name,
    #                "-------------------------" + json.dumps(coCodeList),
    #            )
    #            for coCodeTmp in coCodeList:
    # query = sProMana.iAddDocnumManage(consCode, coCodeTmp['co_code'], json.loads(json.dumps(resDocList, ensure_ascii=False)))
    #                query = sProMana.iPutDocNumManage(
    #                    consCode, coCodeTmp["co_code"], resDocList
    #                )
    #
    #                logs.debug(
    #                    procName,
    #                    os.path.basename(__file__),
    #                    sys._getframe(0).f_code.co_name,
    #                    "iPutDocNumManage Query : " + query,
    #                )
    #
    #                resCd, msg, resData = dbms.execute(query)
    #                if resCd != 0:  # DB 에러 발생 시
    #                    if resCd != 1062:
    #                        logs.war(
    #                            procName,
    #                            os.path.basename(__file__),
    #                            sys._getframe(0).f_code.co_name,
    #                            "Database Error : " + commUtilServ.jsonDumps(msg),
    #                        )
    #
    #                        result = commServ.makeReturnMessage(
    #                            constants.REST_RESPONSE_CODE_DATAFAIL,
    #                            "문서 번호 생성 중 에러가 발생하였습니다. 문서 번호 설정 화면에서 생성 하시기 바랍니다.",
    #                            None,
    #                        )
    #
    #                        logs.debug(
    #                            procName,
    #                            os.path.basename(__file__),
    #                            sys._getframe(0).f_code.co_name,
    #                            "Response : " + commUtilServ.jsonDumps(result),
    #                        )
    #                        return result
    #
    #################################### 프로젝트 참여인력 추가 로그 데이터를 생성 한다. ####################################
    #        logs.debug(
    #            procName,
    #            os.path.basename(__file__),
    #            sys._getframe(0).f_code.co_name,
    #            "---------- 프로젝트 참여인력 추가 로그 데이터를 생성 하고 저장 한다. ----------",
    #        )

    #        job_type_msg = ""
    #        if jobType == "0":  # 발주처
    #            job_type_msg = "발주처"
    #        elif jobType == "1":  # 설계사
    #            job_type_msg = "설계사"
    #        elif jobType == "2":  # 시공
    #            job_type_msg = "시공"
    #        elif jobType == "3":  # 감리
    #            job_type_msg = "감리"
    #        elif jobType == "4":  # 관/청
    #            job_type_msg = "관청"

    #        idList = ""
    #        size = userList.__len__()
    #        num = 0
    #        for user in userList:
    #            idList += user["id"]
    #
    #            if num < size - 1:
    #                idList += ","
    #            else:
    #                idList += ""
    #
    #            num += 1
    #
    #        logData = dLogManage.makeLogData(
    #            procCode,
    #            constants.LOG_LEVEL_CODE_INFO,
    #            "프로젝트 참여 인력이 수정 되었습니다. PROJECT CODE : "
    #            + consCode
    #            + ", 직책 구분 : "
    #            + job_type_msg
    #            + ", 추가 ID : "
    #            + idList,
    #            util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
    #            loginUserInfo["id"],
    #        )
    #
    #        query = sLogManage.iLogData(logData)
    #        logs.debug(
    #            procName,
    #            os.path.basename(__file__),
    #            sys._getframe(0).f_code.co_name,
    #            "iLogData Query : " + query,
    #        )
    #
    #        resCd, msg, resData = dbms.execute(query)  # 로그 저장 Query 실행
    #        if resCd != 0:
    #            logs.war(
    #                procName,
    #                os.path.basename(__file__),
    #                sys._getframe(0).f_code.co_name,
    #                "Database Error : " + commUtilServ.jsonDumps(msg),
    #            )

    #################################### 시공사 문서 등록 로그 데이터를 생성 한다. ####################################
    #        logs.debug(
    #            procName,
    #            os.path.basename(__file__),
    #            sys._getframe(0).f_code.co_name,
    #            "---------- 시공사 문서 등록 로그 데이터를 생성 한다. ----------",
    #        )
    #
    #        for coCodeTmp in coCodeList:
    #            logData = dLogManage.makeLogData(
    #                procCode,
    #                constants.LOG_LEVEL_CODE_INFO,
    #                consName
    #                + "("
    #                + consCode
    #                + ") "
    #                + coCodeTmp["co_name"]
    #                + "("
    #                + coCodeTmp["co_code"]
    #                + ")"
    #                + " 시공 문서가 "
    #                + str(resDocList.__len__())
    #                + "건이 등록 되었습니다.",
    #                util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
    #                loginUserInfo["id"],
    #            )
    #
    #            query = sLogManage.iLogData(logData)
    #            logs.debug(
    #                procName,
    #                os.path.basename(__file__),
    #                sys._getframe(0).f_code.co_name,
    #                "iLogData Query : " + query,
    #            )
    #
    #            resCd, msg, resData = dbms.execute(query)  # 로그 저장 Query 실행
    #            if resCd != 0:
    #                logs.war(
    #                    procName,
    #                    os.path.basename(__file__),
    #                    sys._getframe(0).f_code.co_name,
    #                    "Database Error : " + commUtilServ.jsonDumps(msg),
    #                )

    except KeyError as e:
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
    except NameError as e:
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
    except TypeError as e:
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

    result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)

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
        "---------- 참여 인력 추가 종료 ----------",
    )

    return result


# 2-1. 프로젝트 참여 인력 수정 API
#
# Parameter
@projectManageApi.route("/JoinWorkforce", methods=["PUT"])
def JoinWorkforce():
    commServ = commonService()
    servUserMana = servUserManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 참여 인력 수정 ----------",
        )

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        commUtilServ = commUtilService()
        servProMana = servProjectManage()
        sCommMana = sqlCommManage()
        sProMana = sqlProjectManage()
        sUserManage = sqlUserManage()
        dLogManage = dataLogManage()
        sLogManage = sqlLogManage()

        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        params = request.get_json()  # login parameter recv

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

        if (
            loginUserInfo == None
            or loginUserInfo["manager_type"] != "Y"
            or loginUserInfo["co_code"] != params["contents"]["co_code"]
        ):
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

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "프로젝트 인력 수정 시작",
        )
        addUser = params["contents"]["joinUserList"]["add"]
        putUser = params["contents"]["joinUserList"]["put"]
        delUser = params["contents"]["joinUserList"]["del"]

        resCd, msg, resData = servProjMana.modifyJoinWorkforce(
            params["contents"]["cons_code"], addUser, putUser, delUser
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


# 3.프로젝트 참여 인력 삭제 API
#
# Parameter
@projectManageApi.route("/delJoinWorkforce", methods=["POST"])
def delJoinWorkforce():
    commServ = commonService()
    servUserMana = servUserManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 참여 인력 삭제 ----------",
        )

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        commUtilServ = commUtilService()
        servProMana = servProjectManage()
        sCommMana = sqlCommManage()
        sProMana = sqlProjectManage()
        sUserManage = sqlUserManage()
        dLogManage = dataLogManage()
        sLogManage = sqlLogManage()

        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        params = request.get_json()  # login parameter recv
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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

        consCode = params["cons_code"]
        jobType = params["job_type"]
        userList = params["user_list"]

        # 프로젝트 코드를 체크 한다.
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

        # 직책 구분을 체크 한다.
        if commUtilServ.dataCheck(jobType) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "직책 구분을 입력하여 주시기 바랍니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        # 저장 ID 데이터를 체크 한다.
        if (userList == None) or (userList.__len__() == 0):
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "프로젝트 참여 인력 정보를 확인하여 주시기 바랍니다.",
                None,
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        #################################### 프로젝트 참여 직책 정보를 가져 온다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 참여 직책 정보를 가져온다. ----------",
        )
        query = sProMana.sGetJobTitleCdObj(consCode, loginUserInfo["id"])
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetJobTitlecdObj Query : " + query,
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
                "response : " + commUtilServ.jsonDumps(result),
            )

            return result

        if resData == None:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "프로젝트 참여자 정보가 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 프로젝트 사용자 추가 권한을 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 사용자 추가 권한을 확인 한다. ----------",
        )
        if (
            loginUserInfo["authority_code"] != constants.USER_MASTER
            and loginUserInfo["authority_code"] != constants.USER_MONITOR
        ):
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "프로젝트 사용자 추가 권한이 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 데이터를 체크 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 데이터를 체크 한다. ----------",
        )

        #        checkResult = True
        #
        #        for info in userList:
        #
        #            if jobType == "0":  # 발주처
        #                if info["job_title_code"] != constants.JOB_TITLE_CD_BUYER:
        #                    checkResult = False
        #            elif jobType == "1":  # 설계사
        #                if info["job_title_code"] != constants.JOB_TITLE_CD_DESIGNER:
        #                    checkResult = False
        #            elif jobType == "2":  # 시공
        #                if (
        #                    (info["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTOR)
        #                    and (
        #                        info["job_title_code"]
        #                        != constants.JOB_TITLE_CD_CONTRACTION_MAIN
        #                    )
        #                    and (
        #                        info["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_SUB
        #                    )
        #                    and (
        #                        info["job_title_code"]
        #                        != constants.JOB_TITLE_CD_CONTRACTOR_MONITOR
        #                    )
        #                ):
        #                    checkResult = False
        #            elif jobType == "3":  # 감리
        #                if (
        #                    (info["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN)
        #                    and (
        #                        info["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_SUB
        #                    )
        #                    and (
        #                        info["job_title_code"]
        #                        != constants.JOB_TITLE_CD_SUPERVISOR_MONITOR
        #                    )
        #                ):
        #                    checkResult = False
        #            elif jobType == "4":  # 관/청
        #                if info["job_title_code"] != constants.JOB_TITLE_CD_WHITEHALL:
        #                    checkResult = False
        #            else:
        #                checkResult = False
        #
        #        if checkResult == False:
        #            result = commServ.makeReturnMessage(
        #                constants.REST_RESPONSE_CODE_DATAFAIL,
        #                "잘못된 데이터가 입력 되었습니다. 데이터를 확인 하시기 바랍니다.",
        #                None,
        #            )
        #            logs.war(
        #                procName,
        #                os.path.basename(__file__),
        #                sys._getframe(0).f_code.co_name,
        #                "Response : " + commUtilServ.jsonDumps(result),
        #            )
        #            return result

        #################################### 프로젝트 참여 인력을 삭제 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 참여 인력을 삭제한다. ----------",
        )
        resCd, msg, _ = servProMana.delJoinWorkforce(consCode, userList)
        """
        #### 조현우 추가할예정 인력DB에서 삭제하는 대신 종료일을 맞춤 ####
        query = sProMana.dDelJoinWorkforce(consCode, userList)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelJoinWorkforce Query : " + query,
        )
        resCd, msg, resData = dbms.execute(query)


        query = sProMana.expelJoinWorkforce(consCode, userList)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelJoinWorkforce Query : " + query,
        )
        resCd, msg, resData = dbms.execute(query)
         """
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

        #################################### 프로젝트 참여인력 추가 로그 데이터를 생성 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 참여인력 삭제 로그 데이터를 생성 하고 저장 한다. ----------",
        )

        job_type_msg = ""
        if jobType == "0":  # 발주처
            job_type_msg = "발주처"
        elif jobType == "1":  # 설계사
            job_type_msg = "설계사"
        elif jobType == "2":  # 시공
            job_type_msg = "시공"
        elif jobType == "3":  # 감리
            job_type_msg = "감리"
        elif jobType == "4":  # 관/청
            job_type_msg = "관청"

        idList = ""
        size = userList.__len__()
        num = 0
        for user in userList:
            idList += user["id"]

            if num < size - 1:
                idList += ","
            else:
                idList += ""

            num += 1

        logData = dLogManage.makeLogData(
            procCode,
            constants.LOG_LEVEL_CODE_INFO,
            "프로젝트 참여 인력이 삭제 되었습니다. PROJECT CODE : "
            + consCode
            + ", 직책 구분 : "
            + job_type_msg
            + ", 추가 ID : "
            + idList,
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

        resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그 저장 Query 실행
        if resCd != 0:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + commUtilServ.jsonDumps(msg),
            )

    except KeyError as e:
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
    except NameError as e:
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
    except TypeError as e:
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

    result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)

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
        "---------- 참여 인력 삭제 종료 ----------",
    )

    return result


# 4. 프로젝트 참여 인력 조회 API
#
# Parameter
@projectManageApi.route("/searchJoinWorkforce/<consCode>/<jobType>", methods=["GET"])
def searchJoinWorkforce(consCode, jobType):
    commServ = commonService()
    servUserMana = servUserManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 참여 인력 조회 ----------",
        )

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        commUtilServ = commUtilService()
        sCommMana = sqlCommManage()
        sProMana = sqlProjectManage()
        sUserManage = sqlUserManage()
        dLogManage = dataLogManage()
        sLogManage = sqlLogManage()

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
            + ", jobType : "
            + jobType,
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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

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

        # 직책 구분을 체크 한다.
        if commUtilServ.dataCheck(jobType) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "직책 구분을 입력하여 주시기 바랍니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        jobType = int(jobType)

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
                constants.REST_RESPONSE_CODE_454, "직책 구분을 입력하여 주시기 바랍니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

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
            query = sProMana.sGetJobTitleCdObj(consCode, loginUserInfo["id"])
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
                    "response : " + commUtilServ.jsonDumps(result),
                )

                return result

            if resData == None:
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

        #################################### 검색 데이터를 생성 한다. ####################################
        #        logs.debug(
        #            procName,
        #            os.path.basename(__file__),
        #            sys._getframe(0).f_code.co_name,
        #            "---------- 검색 데이터를 생성 한다. ----------",
        #        )

        #        jobList = []
        #        if jobType == 0:  # 발주처
        #            jobList.append(constants.JOB_TITLE_CD_BUYER)
        #        elif jobType == 1:  # 설계사
        #            jobList.append(constants.JOB_TITLE_CD_DESIGNER)
        #        elif jobType == 2:  # 시공
        #            jobList.append(constants.JOB_TITLE_CD_CONTRACTOR)
        #            jobList.append(constants.JOB_TITLE_CD_CONTRACTION_MAIN)
        #            jobList.append(constants.JOB_TITLE_CD_CONTRACTION_SUB)
        #            jobList.append(constants.JOB_TITLE_CD_CONTRACTOR_MONITOR)
        #        elif jobType == 3:  # 감리
        #            jobList.append(constants.JOB_TITLE_CD_SUPERVISING_MAIN)
        #            jobList.append(constants.JOB_TITLE_CD_SUPERVISING_SUB)
        #            jobList.append(constants.JOB_TITLE_CD_SUPERVISOR_MONITOR)
        #        elif jobType == 4:  # 관청
        #            jobList.append(constants.JOB_TITLE_CD_WHITEHALL)
        #        elif jobType == 5:  # 감리자
        #            jobList.append(constants.JOB_TITLE_CD_SUPERVISOR)
        #        else:
        #            result = commServ.makeReturnMessage(
        #                constants.REST_RESPONSE_CODE_DATAFAIL, "직책 타입이 잘못 입력 되었습니다.", None
        #            )
        #            logs.war(
        #                procName,
        #                os.path.basename(__file__),
        #                sys._getframe(0).f_code.co_name,
        #                "Response : " + commUtilServ.jsonDumps(result),
        #            )
        #            return result

        #################################### 프로젝트 참여 인력을 검색 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 참여 인력을 검색 한다. ----------",
        )
        query = sProMana.sGetJoinWorkforceInfo(consCode, None)
        # query = sProMana.sGetJoinWorkforceInfo(consCode, jobList)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetJoinworkforceInfo Query : " + query,
        )
        resCd, msg, resData = dbms.query(query)

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

        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_ZERO, "", resData
        )

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
            "---------- 참여 인력 조회 종료 ----------",
        )

        return result
    except KeyError as e:
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
    except NameError as e:
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
    except TypeError as e:
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


# 5. 문서 번호 설정 조회 API
#
# Parameter
@projectManageApi.route("/getProjDocNumCfg/<consCode>", methods=["GET"])
def getProjDocNumCfg(consCode):
    commServ = commonService()
    servUserMana = servUserManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 문서번호 설정 조회 시작 ----------",
        )

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        commUtilServ = commUtilService()
        sProjMana = sqlProjectManage()
        sUserManage = sqlUserManage()
        servProjMana = servProjectManage()

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
            + consCode,
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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

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
                "response : " + commUtilServ.jsonDumps(result),
            )

            return result

        if resData == None:
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

        #################################### 문서 설정 정보 조회 권한이 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 문서 설정 정보 조회 권한이 있는지 확인 한다. ----------",
        )
        if (
            (resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_MAIN)
            and (resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_SUB)
            and (resData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN)
            and (resData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_SUB)
        ):
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "문서 설정 정보 조회 권한이 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 문서 설정 정보를 조회 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 문서 설정 정보를 조회 한다. ----------",
        )

        resCd, msg, resData = servProjMana.getProjDocNumCfg(
            consCode, loginUserInfo["co_code"]
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
            "---------- 프로젝트 문서번호 설정 조회 종료 ----------",
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


# 5. 문서 번호 설정 API
#
# Parameter
@projectManageApi.route("/updateProjDocNumCfg", methods=["POST"])
def updateProjDocNumCfg():
    commServ = commonService()
    servUserMana = servUserManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 문서번호 설정 시작 ----------",
        )

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        commUtilServ = commUtilService()
        sProjMana = sqlProjectManage()
        sUserManage = sqlUserManage()
        servProjMana = servProjectManage()
        dLogManage = dataLogManage()
        sLogManage = sqlLogManage()

        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        params = request.get_json()  # login parameter recv
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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

        consCode = params["consCode"]
        updateDocList = params["updateDocList"]

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

        # 업데이트 문서 데이터를 체크 한다.
        if updateDocList.__len__() < 1:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "업데이트 할 문서를 입력 하여 주시기 바랍니다.",
                None,
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

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
        resCd, msg, resData = dbms.queryForObject(query)
        consName = resData["cons_name"]

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
                constants.REST_RESPONSE_CODE_DATAFAIL, "현재 프로젝트 참여자가 아닙니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 문서 설정 정보 수정 권한이 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 문서 설정 정보 수정 권한이 있는지 확인 한다. ----------",
        )
        if (
            (resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_MAIN)
            and (resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_SUB)
            and (resData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN)
            and (resData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_SUB)
        ):
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "문서 설정 정보 수정 권한이 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 문서 설정 정보를 업데이트 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 문서 설정 정보를 업데이트 한다. ----------",
        )

        for docInfo in updateDocList:
            resCd, msg, updateResData = servProjMana.updateProjDocNumCfg(
                consCode, loginUserInfo["co_code"], docInfo
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

        #################################### 문서 수정 로그 데이터를 생성 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 문서 수정 로그 데이터를 생성 한다. ----------",
        )

        docType = ""
        if (resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_MAIN) and (
            resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_SUB
        ):
            docType = " 시공 문서"
        else:
            docType = " 감리 문서"

        logData = dLogManage.makeLogData(
            procCode,
            constants.LOG_LEVEL_CODE_INFO,
            consName
            + "("
            + consCode
            + ") "
            + loginUserInfo["co_name"]
            + "("
            + loginUserInfo["co_code"]
            + ")"
            + docType
            + "가 업데이트 되었습니다.",
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

        resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그 저장 Query 실행
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

        result = commServ.makeReturnMessage(resCd, msg, None)

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
            "---------- 프로젝트 문서번호 설정 종료 ----------",
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


# 6. 소방 시설 공사 등록 API
#
# Parameter
@projectManageApi.route("/cfgFireFigPlan", methods=["PUT"])
def cfgFireFigPlan():
    commServ = commonService()
    servUserMana = servUserManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 소방 시설 공사 등록 ----------",
        )

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        commUtilServ = commUtilService()
        sProjMana = sqlProjectManage()
        sUserManage = sqlUserManage()
        servProjMana = servProjectManage()
        dLogManage = dataLogManage()
        sLogManage = sqlLogManage()

        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        params = request.get_json()  # login parameter recv
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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

        consCode = params["consCode"]
        ffPlanList = params["ffPlanList"]

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

        # 소방 시설 공사 데이터를 체크 한다.
        if ffPlanList.__len__() < 1:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "등록 할 소방 시선 공사 데이터를 입력 하여 주시기 바랍니다.",
                None,
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

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
        resCd, msg, resData = dbms.queryForObject(query)
        consName = resData["cons_name"]

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
                constants.REST_RESPONSE_CODE_DATAFAIL, "현재 프로젝트 참여자가 아닙니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 소방시설공사 등록 권한이 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 소방시설공사 등록 권한이 있는지 확인 한다. ----------",
        )
        if (
            (resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_MAIN)
            and (resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_SUB)
            and (resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTOR)
        ):
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "소방 시설 공사 등록 권한이 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 소방시설공사 정보를 등록 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 소방시설공사 정보를 등록 한다. ----------",
        )

        for ffPlan in ffPlanList:
            resCd, msg, resData = servProjMana.cfgFFPlan(
                consCode, loginUserInfo["co_code"], ffPlan
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

            #################################### 소방시설공사 정보 등록 로그 데이터를 생성 한다. ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 소방시설공사 정보 등록 로그 데이터를 생성 한다. ----------",
            )

            logMsg = ""
            if ffPlan["type"] == "A":
                logMsg = "등록"
            elif ffPlan["type"] == "C":
                logMsg = "수정"
            elif ffPlan["type"] == "D":
                logMsg = "삭제"

            logData = dLogManage.makeLogData(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                loginUserInfo["co_name"]
                + "("
                + loginUserInfo["co_code"]
                + ")의 "
                + loginUserInfo["user_name"]
                + "가 "
                + consName
                + "("
                + consCode
                + ") "
                + ffPlan["ff_plan_name"]
                + "("
                + ffPlan["ff_plan_code"]
                + ")을 "
                + logMsg
                + " 하였습니다.",
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

            resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]]) # 로그 저장 Query 실행
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

        result = commServ.makeReturnMessage(resCd, msg, None)

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
            "---------- 소방시설 공사 등록 종료 ----------",
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


#  소방 시설 공사 조회 API
#
# Parameter
@projectManageApi.route("/getFireFigPlan/<consCode>", methods=["GET"])
def getFireFigPlan(consCode):
    commServ = commonService()
    servUserMana = servUserManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 소방 시설 공사 조회 ----------",
        )

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        commUtilServ = commUtilService()
        sProjMana = sqlProjectManage()
        sUserManage = sqlUserManage()
        servProjMana = servProjectManage()

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
            + " / request url data : "
            + consCode,
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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

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
        if (
            loginUserInfo["authority_code"] == constants.USER_AUTH_BUYER
            or loginUserInfo["authority_code"] == constants.USER_AUTH_DESIGNER
            or loginUserInfo["authority_code"] == constants.USER_AUTH_CONTRACTION
            or loginUserInfo["authority_code"] == constants.USER_AUTH_SUPERVISING
            or loginUserInfo["authority_code"] == constants.USER_AUTH_WHITEHALL
            or loginUserInfo["authority_code"] == constants.USER_AUTH_INOCCUPATION
        ):
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
            resCd, msg, resData = dbms.queryForObject(query)
            consName = resData["cons_name"]

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
                    constants.REST_RESPONSE_CODE_DATAFAIL, "현재 프로젝트 참여자가 아닙니다.", None
                )

                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )
                return result

        #################################### 소방시설공사 정보를 조회 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 소방시설공사 정보를 조회 한다. ----------",
        )

        resCd, msg, resData = servProjMana.getFFPlan(consCode, loginUserInfo)

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
            "---------- 소방시설 공사 조회 종료 ----------",
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


#  책임 감리원 전용 회원 검색
#
# Parameter
@projectManageApi.route("/searchFieldUserListAll", methods=["POST"])
def searchFieldUserListAll():
    commUtilServ = commUtilService()
    commServ = commonService()
    servUserMana = servUserManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 책임 감리원 전용 회원 검색 ----------",
        )

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        sProjMana = sqlProjectManage()
        sUserManage = sqlUserManage()
        servProjMana = servProjectManage()

        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        params = request.get_json()  # login parameter recv

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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

        consCode = params["consCode"]

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

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "-------------------- 0",
        )
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
        resCd, msg, resData = dbms.queryForObject(query)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "-------------------- 1",
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
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "-------------------- 2",
        )

        # consName = ''
        if resData == None:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "-------------------- 3",
            )
            if (
                loginUserInfo["authority_code"] == constants.USER_BUYER
                #        or loginUserInfo["authority_code"] == constants.USER_MONITOR
                or loginUserInfo["authority_code"] == constants.USER_CONSTRUCTOR
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

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "-------------------- 4",
        )
        #################################### 회원 검색 권한이 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 회원 검색 권한이 있는지 확인한다. ----------",
        )
        if resData == None:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "-------------------- 5",
            )
            if (
                loginUserInfo["authority_code"] != constants.USER_MASTER
                and loginUserInfo["authority_code"] != constants.USER_MONITOR
            ):
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL, "회원 검색 권한이 없습니다.", None
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )
                return result
            # else :
            # consName = loginUserInfo['cons_name']

        #        elif (
        #            resData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN
        #        ) and (resData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISOR_MONITOR):
        #            logs.debug(
        #                procName,
        #                os.path.basename(__file__),
        #                sys._getframe(0).f_code.co_name,
        #                "-------------------- 6",
        #            )
        #            result = commServ.makeReturnMessage(
        #                constants.REST_RESPONSE_CODE_DATAFAIL, "회원 검색 권한이 없습니다.", None
        #            )
        #            logs.war(
        #                procName,
        #                os.path.basename(__file__),
        #                sys._getframe(0).f_code.co_name,
        #                "Response : " + commUtilServ.jsonDumps(result),
        #            )
        #            return result
        # else:
        # consName = resData['cons_name']

        #################################### 회원을 검색 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 회원을 검색 한다. ----------",
        )

        resCd, msg, resData = servUserMana.searchFieldUserListAll(params)

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
            "---------- 책임 감리원 전용 회원 검색 종료 ----------",
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


#  공종에 따른 세부 공종 리스트를 조회하는 API.
#
# Parameter
@projectManageApi.route("/getDetailConstrList/<constrCode>", methods=["GET"])
def getDetailConstrList(constrCode):
    commServ = commonService()
    servUserMana = servUserManage()
    servProjMana = servProjectManage()
    sUserManage = sqlUserManage()
    sProjMana = sqlProjectManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공종에 따른 세부 공종 리스트 조회 ----------",
        )

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        commUtilServ = commUtilService()

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
            + " / request url data : "
            + constrCode,
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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

        # 프로젝트(공사) 코드를 체크 한다.
        if commUtilServ.dataCheck(constrCode) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "공종 코드를 입력하여 주시기 바랍니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

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

        #################################### 공종에 따른 세부 공종 리스트를 조회 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공종에 따른 세부 공종 리스트를 조회 한다. ----------",
        )

        resCd, msg, resData = servProjMana.getDetailConstrList(constrCode)

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
            "---------- 공종에 따른 세부 공종 리스트 조회 종료 ----------",
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


#  세부 공종에 대한 체크 리스트 조회 API.
#
# Parameter
@projectManageApi.route(
    "/getCheckList/<constrCode>/<detailConstrCode>", methods=["GET"]
)
def getCheckList(constrCode, detailConstrCode):
    commServ = commonService()
    servUserMana = servUserManage()
    servProjMana = servProjectManage()
    sUserManage = sqlUserManage()
    sProjMana = sqlProjectManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 세부 공종에 따른 체크 리스트 조회 ----------",
        )

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        commUtilServ = commUtilService()

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
            + " / request url data : "
            + constrCode
            + ", "
            + detailConstrCode,
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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

        # 공종 코드를 체크 한다.
        if commUtilServ.dataCheck(constrCode) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "공종 코드를 입력하여 주시기 바랍니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        # 세부 공종 코드를 체크 한다.
        if commUtilServ.dataCheck(detailConstrCode) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "세부 공종 코드를 입력하여 주시기 바랍니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

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

        #################################### 세부 공종에 따른 체크 리스트를 조회 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 세부 공종에 따른 체크 리스트를 조회 한다. ----------",
        )

        resCd, msg, resData = servProjMana.getCheckList(constrCode, detailConstrCode)

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
            "---------- 세부 공종에 따른 체크 리스트 조회 종료 ----------",
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


# 프로젝트 공정에 대한 세부 공정 체크 리스트 추가
#
# Parameter
@projectManageApi.route("/addCheckList", methods=["PUT"])
def addCheckList():
    commServ = commonService()
    servUserMana = servUserManage()
    servProjMana = servProjectManage()
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 공정에 대한 세부 공정 체크 리스트 추가 ----------",
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
        params = request.get_json()  # login parameter recv
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

        consCode = params["cons_code"]
        constrCode = params["constr_code"]
        detailConstrList = params["detailConstrList"]

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
                "response : " + commUtilServ.jsonDumps(result),
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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

        # 프로젝트 코드를 체크 한다.
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

        # 공사종류 코드를 체크 한다.
        if commUtilServ.dataCheck(constrCode) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "공사종류코드를 입력하여 주시기 바랍니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        # 상세 공사 코드 리스트 데이터를 체크 한다.
        if (detailConstrList == None) or (detailConstrList.__len__() == 0):
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "상세 공사 코드 리스트 정보를 확인하여 주시기 바랍니다.",
                None,
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        #################################### 프로젝트의 공종별 체크 리스트 추가 권한을 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 체크리스트 추가 권한을 확인 한다. ----------",
        )
        if (loginUserInfo["authority_code"] != constants.USER_AUTH_CONTRACTOR) and (
            loginUserInfo["authority_code"] != constants.USER_AUTH_CONTRACTION
        ):
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "체크리스트 추가 권한이 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 기존 체크 리스트를 삭제 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 기존 체크 리스트를 삭제 한다. ----------",
        )

        resCd, msg, resData = servProjMana.delProjDetectionChkList(
            consCode, loginUserInfo, params["constr_code"]
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

        #################################### 프로젝트의 공종 별/회사별 세부 공종 별 체크리스트를 추가 한다. ####################################
        resCd, msg, resData = servProjMana.putProjDetectionChkList(
            loginUserInfo["co_code"], params
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

        #################################### 프로젝트의 공종 별/회사별 세부 공종 별 체크리스트 설정 로그 데이터를 생성 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트의 공종 별/회사별 세부 공종 별 체크리스트 설정 로그 데이터를 생성 한다. ----------",
        )

        detailConstrList = params["detailConstrList"]

        for detailConstr in detailConstrList:
            for chkmsg in detailConstr["chk_msg_list"]:
                logData = dLogManage.makeLogData(
                    procCode,
                    constants.LOG_LEVEL_CODE_INFO,
                    loginUserInfo["id"]
                    + " 사용자가 검측 체크리스트 항목을 설정 하였습니다. Project Code : "
                    + params["cons_code"]
                    + ", 회사 명 : "
                    + loginUserInfo["co_name"]
                    + "("
                    + loginUserInfo["co_code"]
                    + ") 공종 코드 : "
                    + params["constr_code"]
                    + ", 상세 공종 코드 : "
                    + detailConstr["detail_constr_code"]
                    + "체크리스트 : "
                    + chkmsg["chk_msg"]
                    + ", 검측 기준 코드 : "
                    + chkmsg["insp_crit_code"],
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

                resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]]) # 로그 저장 Query 실행
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
            "---------- 프로젝트 공정에 대한 세부 공정 체크 리스트 추가 종료 ----------",
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


# 프로젝트별-회사별-공종별 체크 리스트를 가져온다.
#
# Parameter
@projectManageApi.route("/getProjCheckList/<consCode>/<constrCode>", methods=["GET"])
def getProjCheckList(consCode, constrCode):
    commServ = commonService()
    servUserMana = servUserManage()
    servProjMana = servProjectManage()
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트별-회사별-공종별 체크 리스트를 가져온다. ----------",
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
            + consCode
            + ", constrCode : "
            + constrCode,
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
                "response : " + commUtilServ.jsonDumps(result),
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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

        # 프로젝트 코드를 체크 한다.
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

        # 공사종류 코드를 체크 한다.
        if commUtilServ.dataCheck(constrCode) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "공사종류코드를 입력하여 주시기 바랍니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        #################################### 프로젝트별-회사별-공종별 체크리스트를 가져돈다. ####################################
        resCd, msg, resData = servProjMana.getProjDetectionChkList(
            consCode, loginUserInfo["co_code"], constrCode
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
            "---------- 프로젝트별-회사별-공종별 체크 리스트를 가져온다. 종료 ----------",
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


# 프로젝트 참여 인력 현황 제공(소방서 전용)
#
# Parameter
@projectManageApi.route("/getProjPartManpStatus", methods=["GET"])
def getProjPartManpStatus():
    commServ = commonService()
    servUserMana = servUserManage()
    servProjMana = servProjectManage()
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 참여 인력 현황 제공(소방서 전용) 시작 ----------",
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

        #################################### 프로젝트 리스트를 가져 온다. ####################################
        resCd, msg, resData = servProjMana.getAreaProjPartManpStatus(
            loginUserInfo["co_code"]
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
            "---------- 프로젝트별-회사별-공종별 체크 리스트를 가져온다. 종료 ----------",
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


# 프로젝트 기본정보 저장
#
# Parameter
@projectManageApi.route("/updateProjDefaultInfo", methods=["PUT"])
def updateProjDefaultInfo():
    commServ = commonService()
    servUserMana = servUserManage()
    servProjMana = servProjectManage()
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 기본 정보 저장 시작 ----------",
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
        params = request.get_json()  # login parameter recv
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
                "response : " + commUtilServ.jsonDumps(result),
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

        #################################### 공사 기본 정보를 저장 할 수 있는 권한이 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공사 기본 정보를 저장 할 수 있는 권한이 있는지 확인 한다. ----------",
        )
        # if resData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN:
        if (
            loginUserInfo["authority_code"] != constants.USER_MASTER
            and loginUserInfo["authority_code"] != constants.USER_MONITOR
        ):
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "공사 기본 정보를 입력 할 수 있는 권한이 없습니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 공사 기본 정보를 저장 한다. ####################################
        resCd, msg, resData = servProjMana.updateProjDefaultInfo(
            params["cons_code"], params, "U"
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

        #################################### 공사 기본 정보 갱신 로그 데이터를 생성 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공사 기본 정보 갱신 로그 데이터를 생성 한다. ----------",
        )

        logData = dLogManage.makeLogData(
            procCode,
            constants.LOG_LEVEL_CODE_INFO,
            loginUserInfo["id"]
            + " 사용자가 프로젝트 기본 정보를 업데이트 하였습니다. Project Code : "
            + params["cons_code"],
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

        resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그 저장 Query 실행
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


# 공사 기본 정보를 조회 한다.
#
# Parameter
@projectManageApi.route("/getProjDefaultInfo/<consCode>", methods=["GET"])
def getProjDefaultInfo(consCode):
    commServ = commonService()
    servUserMana = servUserManage()
    servProjMana = servProjectManage()
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 공사 기본 정보를 조회 한다. ----------",
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
            + consCode,
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
            query = sProjMana.sGetJobTitleCdObj(consCode, loginUserInfo["id"])
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
                    "response : " + commUtilServ.jsonDumps(result),
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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

        # 프로젝트 코드를 체크 한다.
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

        #################################### 프로젝트 기본 정보를 조회 한다. ####################################
        resCd, msg, resData = servProjMana.getProjDefaultInfo(consCode)

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
            "---------- 프로젝트 기본 정보를 조회 한다. 종료 ----------",
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


# 감리 및 시공사의 공사 기본 정보를 저장한다.
#
# Parameter
@projectManageApi.route("/putBasicConsInfoByCompany", methods=["PUT"])
def putBasicConsInfoByCompany():
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
        sCommMana = sqlCommManage()
        sProMana = sqlProjectManage()
        dLogManage = dataLogManage()
        sLogManage = sqlLogManage()
        sProjMana = sqlProjectManage()

        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        # params = request.get_json()			# login parameter recv
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

        #################################### 감리인지 시공사인지 체크 한다.(company_type : 0 이면 감리, 1이면 시공) ####################################
        if params["company_type"] == None:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "감리 / 시공 구분 데이터가 입력 되지 않았습니다.",
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "감리 / 시공 구분 데이터가 입력 되지 않았습니다.",
                None,
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        if params["company_type"] == "0":  # 감리일 경우
            #################################### 감리 기본 정보를 저장 할 수 있는 권한이 있는지 확인 한다. ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 감리 기본 정보를 저장 할 수 있는 권한이 있는지 확인 한다. ----------",
            )
            if resData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN:
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL,
                    "감리 기본 정보를 입력 할 수 있는 권한이 없습니다.",
                    None,
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )
                return result

            #################################### 감리 기본 정보를 저장 한다. ####################################
            resCd, msg, resData = servProjMana.updateSupvDefaultInfo(params)

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

            #################################### 감리 기본 정보 갱신 로그 데이터를 생성 한다. ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 감리 기본 정보 갱신 로그 데이터를 생성 한다. ----------",
            )

            logData = dLogManage.makeLogData(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                loginUserInfo["id"]
                + " 사용자가 감리 기본 정보를 업데이트 하였습니다. Project Code : "
                + params["cons_code"],
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

            resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그 저장 Query 실행
            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

        elif params["company_type"] == "1":  # 시공일 경우
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

                        # searchList = {
                        # 	'search_material_name' : matInfo['mat_nm_info'],
                        # 	'search_standard' : matInfo['mat_st_info'],
                        # 	'search_unit' : unitCode
                        # }

                        # resCd, msg, materialInfo = servProjAppMatMana.getApproMaterList(searchList)
                        materialNum = ""

                        # if(materialInfo != None) :
                        # 	materialNum = materialInfo['material_num']

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

            resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그 저장 Query 실행
            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

        else:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "감리 / 시공 구분 데이터가 잘못 입력되었습니다.",
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "감리 / 시공 구분 데이터가 잘못 입력 되었습니다.",
                None,
            )

            logs.war(
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


# 감리 및 시공사의 공사 기본 정보를 수정한다.
#
# Parameter
@projectManageApi.route("/modifyBasicConsInfoByCompany", methods=["POST"])
def modifyBasicConsInfoByCompany():
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
        # params = request.get_json()			# login parameter recv
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

        #################################### 감리인지 시공사인지 체크 한다.(company_type : 0 이면 감리, 1이면 시공) ####################################
        if params["company_type"] == None:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "감리 / 시공 구분 데이터가 입력 되지 않았습니다.",
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "감리 / 시공 구분 데이터가 입력 되지 않았습니다.",
                None,
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        if params["company_type"] == "0":  # 감리일 경우
            #################################### 감리 기본 정보를 저장 할 수 있는 권한이 있는지 확인 한다. ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 감리 기본 정보를 수정 할 수 있는 권한이 있는지 확인 한다. ----------",
            )
            if resData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN:
                result = commServ.makeReturnMessage(
                    constants.REST_RESPONSE_CODE_DATAFAIL,
                    "감리 기본 정보를 수정 할 수 있는 권한이 없습니다.",
                    None,
                )
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Response : " + commUtilServ.jsonDumps(result),
                )
                return result

            #################################### 감리 기본 정보를 저장 한다. ####################################
            resCd, msg, resData = servProjMana.updateSupvDefaultInfo(params)

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

            #################################### 감리 기본 정보 갱신 로그 데이터를 생성 한다. ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 감리 기본 정보 갱신 로그 데이터를 생성 한다. ----------",
            )

            logData = dLogManage.makeLogData(
                procCode,
                constants.LOG_LEVEL_CODE_INFO,
                loginUserInfo["id"]
                + " 사용자가 감리 기본 정보를 업데이트 하였습니다. Project Code : "
                + params["cons_code"],
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

            resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그 저장 Query 실행
            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

        elif params["company_type"] == "1":  # 시공일 경우
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

            resCd, msg, resData = dbms.executeSpecial(query, [logData["log_content"], logData["msg"]])  # 로그 저장 Query 실행
            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "Database Error : " + commUtilServ.jsonDumps(msg),
                )

        else:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "감리 / 시공 구분 데이터가 잘못 입력되었습니다.",
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "감리 / 시공 구분 데이터가 잘못 입력 되었습니다.",
                None,
            )

            logs.war(
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


# 감리 및 시공사의 공사 기본 정보를 조회한다.
#
# Parameter
@projectManageApi.route(
    "/searchBasicConsInfoByCompany/<consCode>/<companyType>", methods=["GET"]
)
def searchBasicConsInfoByCompany(consCode, companyType):
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
            + consCode
            + ", companyType : "
            + companyType,
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
                or loginUserInfo["authority_code"] == constants.USER_AUTH_CONTRACTION
                or loginUserInfo["authority_code"] == constants.USER_AUTH_SUPERVISING
                or loginUserInfo["authority_code"] == constants.USER_AUTH_WHITEHALL
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

        #################################### 감리인지 시공사인지 체크 한다.(company_type : 0 이면 감리, 1이면 시공) ####################################
        if companyType == None:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "감리 / 시공 구분 데이터가 입력 되지 않았습니다.",
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "감리 / 시공 구분 데이터가 입력 되지 않았습니다.",
                None,
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        if companyType == "0":  # 감리일 경우
            #################################### 감리 기본 정보를 조회 한다. ####################################
            resCd, msg, resData = servProjMana.getSupvDefaultInfo(consCode)

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
        elif companyType == "1":  # 시공일 경우
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
            resCd, msg, resData = servProjMana.getContDefaultInfo(consCode, coCode)
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

        else:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "감리 / 시공 구분 데이터가 잘못 입력되었습니다.",
            )
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "감리 / 시공 구분 데이터가 잘못 입력 되었습니다.",
                None,
            )

            logs.war(
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


# 프로젝트 리스트를 조회한다.
#
# Parameter
@projectManageApi.route("/getProjectList/<projectStatus>", methods=["GET"])
def getProjectList(projectStatus):
    commServ = commonService()
    servUserMana = servUserManage()
    servProjMana = servProjectManage()
    servCommMana = servCommManage()
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 리스트 조회 ----------",
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

        # 프로젝트 상태를 체크 한다.
        if commUtilServ.dataCheck(projectStatus) == False:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                "프로젝트 상태 코드를 입력하여 주시기 바랍니다.",
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

        #################################### 프로젝트 조회 권한이 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 프로젝트 조회 권한이 있는지 확인 한다. ----------",
        )
        if loginUserInfo["user_state"] != constants.APPRO_STATUS_CD_APPRO:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "프로젝트 조회 권한이 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 프로젝트 리스트를 조회 한다. ####################################
        resCd, msg, resData = servProjMana.getProjectList(loginUserInfo, projectStatus)
        # resCd, msg, resData = servProjMana.getProjectList(loginUserInfo['id'], projectStatus)
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
            "---------- 프로젝트 리스트를 조회 한다. 종료 ----------",
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


# 작업 일지 작성 기준을 조회 한다.
#
# Parameter
@projectManageApi.route("/getWorkLogWriSta/<consCode>", methods=["GET"])
def getWorkLogWriSta(consCode):
    commServ = commonService()
    servUserMana = servUserManage()
    servProjMana = servProjectManage()
    servCommMana = servCommManage()
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업 일지 작성 기준을 조회 한다. ----------",
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

        #################################### 작업일지 작성 기준 정보를 조회 한다. ####################################
        resCd, msg, resData = servProjMana.getWorkLogWriSta(
            consCode, loginUserInfo["co_code"]
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
            "---------- 작업일지 작성 기준을 조회 한다. 종료 ----------",
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


# 작업일지 작성 기준 정보를 수정 한다.
#
# Parameter
@projectManageApi.route("/modifyWorkLogWriSta", methods=["POST"])
def modifyWorkLogWriSta():
    commUtilServ = commUtilService()
    commServ = commonService()
    servUserMana = servUserManage()

    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업일지 작성 기준 정보를 수정 한다. ----------",
        )

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        sProjMana = sqlProjectManage()
        sUserManage = sqlUserManage()
        servProjMana = servProjectManage()

        token = request.headers.get("token")
        sysCd = request.headers.get("sysCd")
        params = request.get_json()  # login parameter recv

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

        #################################### Parameter 확인 ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- Parameter를 확인 한다. ----------",
        )

        consCode = params["cons_code"]
        workLogWriSatCd = params["work_log_wri_sat_cd"]

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
        resCd, msg, resData = dbms.queryForObject(query)
        consName = resData["cons_name"]

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
                constants.REST_RESPONSE_CODE_DATAFAIL, "현재 프로젝트 참여자가 아닙니다.", None
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 작업일지 수정 권한이 있는지 확인 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업일지 작성 기준 수정 권한이 있는지 확인한다. ----------",
        )
        if (
            resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_MAIN
            and resData["job_title_code"] != constants.JOB_TITLE_CD_CONTRACTION_SUB
        ):
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "작업일지 작성 기준 수정 권한이 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return result

        #################################### 작업일지 작성 기준 정보를 검색 한다. ####################################
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 작업일지 작성 기준 정보를 수정 한다. ----------",
        )

        resCd, msg, resData = servProjMana.modifyWorkLogWriSta(
            consCode, loginUserInfo["co_code"], workLogWriSatCd
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
            "---------- 작업일지 작성 기준 정보를 수정 한다. 종료 ----------",
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
