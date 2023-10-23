# _*_coding: utf-8 -*-

from flask import Blueprint, request
from flask_restx import Resource
import json
import copy
import os
import sys

from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import api

from common.logManage import logManage
from common import constants
from common.commUtilService import commUtilService
from common.commonService import commonService
from userManage.servUserManage import servUserManage
from projectManage.sqlProjectManage import sqlProjectManage
from projectDesignBookManage.servProjectDesignBookManage import (
    servProjectDesignBookManage,
)
from projectFloorPlanManage.servProjectFloorPlanManage import servProjectFloorPlanManage
from commManage.servCommManage import servCommManage

projectFloorPlanManageApi = api.namespace(
    "projectFloorPlanApi", description="설계도면 이미지 관리"
)

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


@projectFloorPlanManageApi.route("/FloorPlan/<string:cons_code>/<string:ver_info>")
class projectFloorPlanManageAll(Resource):
    """전체 설계도면 관리 api"""

    @api.response(200, "Success")
    @api.response(400, "Bad Request")
    @api.response(500, "Server Internal Error")
    @api.doc(description="설계도면 전체 이미지를 조회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
    )
    def get(self, cons_code, ver_info):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjFPMana = servProjectFloorPlanManage()
        sProjMana = sqlProjectManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 설계도면 이미지 조회 시작 ----------",
        )
        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "request header token : " + token + ", sysCd : " + sysCd,
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

            #################################### 로직에 필요한 변수를 저장한다. ####################################
            params = {"cons_code": cons_code, "ver_info": ver_info}

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

            #################################### 해당 도면을 조회한다 ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 전체 도면을 조회한다. ----------",
            )

            resCd, msg, resData = servProjFPMana.getFloorPlanAll(params)
            return commServ.make_response(resCd, msg, resData)

        except Exception as e:
            result = commServ.make_response(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )

        return result

    @api.doc(description="설계도면 전체 이미지를 삭제")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
    )
    def delete(self, cons_code, ver_info):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjFPMana = servProjectFloorPlanManage()
        sProjMana = sqlProjectManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 설계도면 이미지 조회 시작 ----------",
        )
        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "request header token : " + token + ", sysCd : " + sysCd,
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

            #################################### 로직에 필요한 변수를 저장한다. ####################################
            params = {"cons_code": cons_code, "ver_info": ver_info}

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

            #################################### 해당 도면을 삭제한다 ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 해당 전체 도면을 삭제한다. ----------",
            )

            resCd, msg, resData = servProjFPMana.delFloorPlanAll(params)
            return commServ.make_response(resCd, msg, resData)

        except Exception as e:
            result = commServ.make_response(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )

        return result


@projectFloorPlanManageApi.route(
    "/FloorPlan/<string:cons_code>/<string:ver_info>/<int:page>"
)
class projectFloorPlanManage(Resource):
    """설계도면 관리 api"""

    @api.response(200, "Success")
    @api.response(400, "Bad Request")
    @api.response(500, "Server Internal Error")
    @api.doc(description="설계도면 특정 페이지 이미지를 조회")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
    )
    def get(self, cons_code, ver_info, page):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjFPMana = servProjectFloorPlanManage()
        sProjMana = sqlProjectManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 설계도면 이미지 조회 시작 ----------",
        )
        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "request header token : " + token + ", sysCd : " + sysCd,
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

            #################################### 로직에 필요한 변수를 저장한다. ####################################
            params = {"cons_code": cons_code, "ver_info": ver_info, "page": page}

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

            #################################### 해당 도면을 조회한다 ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 해당 도면을 조회한다. ----------",
            )

            resCd, msg, resData = servProjFPMana.getFloorPlan(params)
            return commServ.make_response(resCd, msg, resData)

        except Exception as e:
            result = commServ.make_response(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )

        return result

    @api.doc(description="설계도면 특정 페이지 이미지를 삭제")
    @api.expect(
        api.parser().add_argument("token", type=str, location="headers", required=True),
        api.parser().add_argument("sysCd", type=str, location="headers", required=True),
    )
    def delete(self, cons_code, ver_info, page):
        commServ = commonService()
        commUtilServ = commUtilService()
        servUserMana = servUserManage()
        servProjFPMana = servProjectFloorPlanManage()
        sProjMana = sqlProjectManage()

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 설계도면 이미지 조회 시작 ----------",
        )
        try:
            sysCd = request.headers.get("sysCd")
            token = request.headers.get("token")

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "request header token : " + token + ", sysCd : " + sysCd,
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

            #################################### 로직에 필요한 변수를 저장한다. ####################################
            params = {"cons_code": cons_code, "ver_info": ver_info, "page": page}

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

            #################################### 해당 도면을 삭제한다 ####################################
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "---------- 해당 전체 도면을 삭제한다. ----------",
            )

            resCd, msg, resData = servProjFPMana.delFloorPlan(params)
            return commServ.make_response(resCd, msg, resData)

        except Exception as e:
            result = commServ.make_response(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )

        return result
