# _*_coding: utf-8 -*-

from flask import Blueprint, request
import json
import copy
import os
import sys

projectDesignBookManageApi = Blueprint("projectDesignBookManageApi", __name__)

from projectDesignBookManage.servProjectDesignBookManage import (
    servProjectDesignBookManage,
)

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.logManage import logManage
from common import constants
from common.commUtilService import commUtilService
from common.commonService import commonService
from common.pdfService import pdfService
from common import util_time
from userManage.servUserManage import servUserManage
from projectManage.sqlProjectManage import sqlProjectManage

from commManage.servCommManage import servCommManage

# from allscapeAPIMain import projectHome

# from projectApproMaterManage.servProjectApproMaterManage import servProjectApproMaterManage
# from projectUseMaterialManage.servProjectUseMaterialManage import servProjectUseMaterialManage

# from projectInspMaterManage.servProjectInspMaterManage import servProjectInspMaterManage

# from projectDetectionManage.servProjectDetectionManage import servProjectDetectionManage

# from projectWorkLogManage.servProjectWorkLogManage import servProjectWorkLogManage

# from projectManage.servProjectManage import servProjectManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


# 설계 도서 조회
@projectDesignBookManageApi.route(
    "/getDesignBookList/<consCode>/<designBookType>", methods=["GET"]
)
def getDesignBookList(consCode, designBookType):
    commServ = commonService()
    commUtilServ = commUtilService()
    servProjDBMana = servProjectDesignBookManage()
    servUserMana = servUserManage()

    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    try:
        sysCd = request.headers.get("sysCd")
        token = request.headers.get("token")

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "request header token : "
            + token
            + ", sysCd : "
            + sysCd
            + " / request url consCode : "
            + consCode
            + ", designBookType : "
            + designBookType,
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
        # if(params['cons_code'] != ''):
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
                "현재 프로젝트에 참여하고 있지 않아 설계도서를 조회 할 수 없습니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

            #################################### 설계 도서 리스트를 조회 힌다. ####################################
        resCd, msg, resDesignBookList = servProjDBMana.getDesignBookList(
            consCode, designBookType
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

        result = commServ.makeReturnMessage(
            constants.REST_RESPONSE_CODE_ZERO, "", resDesignBookList
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


# 설계 도서 등록
@projectDesignBookManageApi.route("/regDesignBook", methods=["PUT"])
def regDesignBook():

    commServ = commonService()
    commUtilServ = commUtilService()
    servUserMana = servUserManage()
    servProjDBMana = servProjectDesignBookManage()
    # servProjDocMana = servProjectDocManage()
    # servProjUseMatMana = servProjectUseMaterialManage()
    servCommMana = servCommManage()

    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    try:
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "---------- 설계도서 등록 요청 처리 시작 ----------",
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
                "현재 프로젝트에 참여하고 있지 않아 프로젝트 참여자를 조회 할 수 없습니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "1Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        #################################### 설계도서 등록 권한을 확인 한다. ####################################
        if (
            jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN
        ) and (jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_SUB):

            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "설계 도서 등록 권한이 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "2Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        # 설계도서 파일을 체크 한다.
        if params["file_name"] == "":
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL,
                str("파일 선택 후 다시 등록하여 주시기 바랍니다."),
                None,
            )

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "3Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        # 설계도서 파일 정보를 저장 한다.
        params["regId"] = loginUserInfo["id"]
        resCd, msg, result = servProjDBMana.putDesignBookInfo(params, request)

        if resCd != 0:
            result = commServ.makeReturnMessage(resCd, msg, None)

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "4Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        result = commServ.makeReturnMessage(constants.REST_RESPONSE_CODE_ZERO, "", None)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "5Response : " + commUtilServ.jsonDumps(result),
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
        "6Response : " + commUtilServ.jsonDumps(result),
    )

    return result


# 설계 도서 삭제
@projectDesignBookManageApi.route(
    "/delDesignBook/<consCode>/<designBookType>/<fileName>", methods=["DELETE"]
)
def delDesignBook(consCode, designBookType, fileName):
    commServ = commonService()
    commUtilServ = commUtilService()
    servProjDBMana = servProjectDesignBookManage()
    servUserMana = servUserManage()

    sProjMana = sqlProjectManage()
    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    try:
        sysCd = request.headers.get("sysCd")
        token = request.headers.get("token")

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "request header token : "
            + token
            + ", sysCd : "
            + sysCd
            + " / request url consCode : "
            + consCode
            + ", designBookType : "
            + designBookType
            + ", fileName : "
            + fileName,
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
        # if(params['cons_code'] != ''):
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
                "현재 프로젝트에 참여하고 있지 않아 설계도서를 조회 할 수 없습니다.",
                None,
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        #################################### 설계도서 삭제 권한을 확인 한다. ####################################
        if (
            jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_MAIN
        ) and (jobResData["job_title_code"] != constants.JOB_TITLE_CD_SUPERVISING_SUB):

            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, "설계 도서 삭제 권한이 없습니다.", None
            )
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return result

        #################################### 설계 도서를 삭제 한다. ####################################
        resCd, msg, resData = servProjDBMana.delDesignBook(
            consCode, designBookType, fileName
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
