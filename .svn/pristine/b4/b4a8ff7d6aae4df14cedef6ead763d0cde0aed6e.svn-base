# _*_coding: utf-8 -*-

# 공통으로 사용되는 Function 관리 Class
# 작성 날짜 : 2022. 08. 02
# 작성자 : 황희정
# 기능
# 	1. 2022. 08. 02 | 사용자 로그인 체크
# 변경 이력
# 	1. 2022. 08. 02 | 황희정 | 최조 작성

# sys import
import json
import copy
import os
import sys
import uuid
import shutil
import multiprocessing
from flask import make_response, jsonify

# user import
from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import procCode
from allscapeAPIMain import fileHome

from common.messageService import messageService
from common.dataCommonManage import dataCommonManage
from common.commUtilService import commUtilService
from common.logManage import logManage
from common import constants


from userManage.dataUserManage import dataUserManage
from userManage.sqlUserManage import sqlUserManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당

# 공통으로 사용되는 Function 관리 Class
class commonService:

    # 사용자 로그인 정보 체크
    def userLoginChk(self, token, sysCd):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sUserManage = sqlUserManage()
        commUtilServ = commUtilService()

        query = sUserManage.sChkUserLoginInfo(token, sysCd)
        resCd, msg, resData = dbms.queryForObject(query)  # Query를 실행한다.
        if resCd != 0:  # DB 에러 발생 시
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Database Error : " + msg,
            )

            result = self.makeReturnMessage(resCd, msg, None)

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )
            return False, result

        if (resData == None) or (resData["cnt"] < 1):
            result = self.makeReturnMessage(constants.REST_RESPONSE_CODE_455, msg, "")

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Rresponse : " + commUtilServ.jsonDumps(result),
            )
            return False, result

        return True, None
        # return True, result

    # System Code Check
    def checkSystemCd(self, sysCd):
        commUtilServ = commUtilService()

        if commUtilServ.dataCheck(sysCd) == False:
            result = self.makeReturnMessage(constants.REST_RESPONSE_CODE_456, "", None)

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return False, result

        return True, None

    # Token Check
    def checkTokenCd(self, token):
        commUtilServ = commUtilService()

        if commUtilServ.dataCheck(token) == False:
            result = self.makeReturnMessage(constants.REST_RESPONSE_CODE_457, "", None)

            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "Response : " + commUtilServ.jsonDumps(result),
            )

            return False, result

        return True, None

    # Make return message
    def makeReturnMessage(self, code, msg, data):
        dCommManage = dataCommonManage()
        msgServ = messageService()

        resStatus = constants.REST_RESPONSE_CODE_SUCCESS
        resMessage = ""
        resData = data
        if code != 0:
            resStatus = code
            resMessage = msg
            resData = None

        return dCommManage.makeResResult(
            resStatus, msgServ.getCustomMessage(resStatus, resMessage), resData
        )

    def make_response(self, code: str, msg: str, value: dict):
        dCommManage = dataCommonManage()
        msgServ = messageService()

        resStatus = constants.REST_RESPONSE_CODE_SUCCESS
        resMessage = ""
        resData = value
        if code != 0:
            resStatus = code
            resMessage = msg
            resData = None

        #### response의 status_code까지 설정해 주어야함
        resMessage = msgServ.getCustomMessage(resStatus, resMessage)
        response = make_response(
            jsonify({"code": resStatus, "msg": resMessage, "value": resData})
        )
        response.status_code = resStatus
        return response

    # 파일 관련 서비스 Start ##############################################################################
    # 파일 경로 및 파일명을 생성 한다.
    def createFilePathAndName(self, typeHome, type, path, data, key):
        filePath = fileHome + typeHome + path
        fileOriginalName = data[key]
        name, ext = os.path.splitext(data[key])
        fileChangeName = str(uuid.uuid4()) + ext

        return filePath, fileOriginalName, fileChangeName

    # 디렉터리 경로를 설정 한다.
    def createDir(self, filePath):
        try:
            if not os.path.exists(filePath):
                os.makedirs(filePath)
        except:
            Err = "디렉터리가 이미 생성되어 있습니다."

    # 파일을 저장 한다. autoConvert가 켜져있으면 자동으로 pdf로 변환한다
    def saveFile(self, f_file, filePath, fileName, autoConvert=True):
        f_file.save(filePath + fileName)
        f_file.flush()
        folder, ext = os.path.splitext(filePath + fileName)
        if autoConvert == True and ext == ".pdf":
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "이미지변환시작" + folder,
            )
            image_converter = multiprocessing.Process(
                target=self.convert_pdf,
                args=(
                    filePath,
                    fileName,
                ),
            )
            image_converter.start()

    # pdf파일을 이미지로 변환해둔다.
    def convert_pdf(self, file_path, file_name):
        from common.pdfService import pdfService

        pdfServ = pdfService()
        folder, ext = os.path.splitext(file_path + file_name)
        if ext != ".pdf":
            return
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "업로드한 pdf 파일을 이미지로 변환을 시도합니다 : " + folder,
        )
        try:
            pdfServ.raw_pdf2image(file_path + file_name)
        except Exception as e:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "이미지 변환실패 : " + str(e),
            )
        return

    # 파일을 삭제 한다.
    def removeFile(self, filePath, fileName):
        try:
            if os.path.isfile(filePath + fileName):
                os.remove(filePath + fileName)
                # pdf 파일이면 관련이미지도 지운다
                folder, ext = os.path.splitext(filePath + fileName)
                if os.path.exists(folder):
                    shutil.rmtree(folder)
        except:
            raise NameError("파일을 삭제할 수 없습니다")

    # 파일 관련 서비스 End ##############################################################################
