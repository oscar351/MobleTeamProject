# _*_coding: utf-8 -*-
import os
import sys
import copy
import json
import shutil
import multiprocessing

from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import projDocFile
from allscapeAPIMain import projectHome

from common.logManage import logManage
from common import util_time
from common import constants
from common.pdfService import pdfService

from common.commonService import commonService
from projectDocManage.sqlProjectDocManage import sqlProjectDocManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectDocManage:
    # 문서 정보를 가져 온다.(작성자가 작성할 수 있는 문서인지 확인하기 위함)
    def getDocumentInfo(self, consCode, docCode, coCode):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        # 쿼리 생성
        query = sProjDocMana.sGetDocumentInfo(consCode, docCode, coCode)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetDocumentInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 문서 기본 정보를 생성 한다.
    def createDocDefaultInfo(self, userInfo, docNumber, sysDocNum):

        result = {
            "sysDocNum": str(sysDocNum),
            "documentNumber": docNumber,
            "docCreateDate": util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
            "stateCode": constants.APPRO_STATUS_CD_PROCEEDING,
            "prDate": util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
            "writer": userInfo["id"],
            "approvalDate": util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
            "coCode": userInfo["co_code"],
        }

        return result

    # 문서 번호 정보를 가져 온다.
    def getDocumentNumInfo(self, consCode, docCode, coCode):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        # 문서 번호를 가져 온다.
        query = sProjDocMana.sGetDocumentNumInfo(consCode, docCode, coCode)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetDocumentNumInfo Query : " + query,
        )

        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 문서 번호를 업데이트 한다.
    def modifyDocumentNumInfo(self, consCode, docCode, coCode, docNum):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        # 문서 번호를 가져 온다.
        query = sProjDocMana.uModifyDocumentNumInfo(consCode, docCode, coCode, docNum)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uModifyDocumentNumInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 자재 선정 승인 요청 데이터를 저장 한다.
    def putDocumentInfo(self, docDefaultInfo, dataInfo):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        # 데이터를 저장 한다.
        query = sProjDocMana.iPutDocumentInfo(docDefaultInfo, dataInfo)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutDocumentInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 자재 선정 승인 요청 데이터를 삭제 한다.
    # def delDocumentInfo(self, consCode, docCode, docNum):
    def delDocumentInfo(self, sysDocNum):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        # 데이터를 저장 한다.
        # query = sProjDocMana.dDelDocumentInfo(consCode, docCode, docNum)
        query = sProjDocMana.dDelDocumentInfo(sysDocNum)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelDocumentInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 결재 정보 데이터를 저장 한다.
    def putDocumentApprovalInfo(self, dataInfo, docNum, sysDocNum, approvalDate):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        approvalList = dataInfo["reqDocApprovalInfoList"]

        # 결재 정보를 저장 한다.
        if len(approvalList) < 2:
            return constants.REST_RESPONSE_CODE_DATAFAIL, "결재자 정보를 입력 하세요.", None

        for approval in approvalList:
            # 데이터를 저장 한다.
            query = sProjDocMana.iPutDocumentApprovalInfo(
                dataInfo["reqDocInfo"], approval, docNum, sysDocNum, approvalDate
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "iPutDocumentApprovalInfo Query : " + query,
            )

            resCd, msg, resData = dbms.execute(query)

            approvalDate = ""

            if resCd != 0:
                return resCd, msg, resData

        return constants.REST_RESPONSE_CODE_ZERO, "", None
        # return resCd, msg, resData

    # 결재 정보 데이터를 삭제 한다.
    def delDocumentApprovalInfo(self, sysDocNum):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        query = sProjDocMana.dDelDocumentApprovalInfo(sysDocNum)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelDocumentApprovalInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 연결된 문서 정보 데이터를 저장 한다.
    def putLinkDocInfo(self, consCode, sysDocNum, linkSysDocNumList):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        for linkSysDocNum in linkSysDocNumList:
            # 데이터를 저장 한다.
            query = sProjDocMana.iPutLinkDocInfo(
                consCode, sysDocNum, linkSysDocNum["link_sys_doc_num"]
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "iPutLinkDocInfo Query : " + query,
            )

            resCd, msg, resData = dbms.execute(query)
            if resCd != 0:
                return resCd, msg, resData

            query = sProjDocMana.iPutLinkDocInfo(
                consCode, linkSysDocNum["link_sys_doc_num"], sysDocNum
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "iPutLinkDocInfo Query : " + query,
            )

            resCd, msg, resData = dbms.execute(query)
            if resCd != 0:
                return resCd, msg, resData

        return resCd, msg, resData

    # 연결된 문서 정보 데이터를 삭제 한다.
    def delLinkDocInfo(self, consCode, sysDocNum, linkSysDocNumList):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        for linkSysDocNum in linkSysDocNumList:
            # 데이터를 저장 한다.
            query = sProjDocMana.dDelLinkDocInfo(
                consCode, sysDocNum, linkSysDocNum["link_sys_doc_num"]
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "dDelLinkDocInfo Query : " + query,
            )

            resCd, msg, resData = dbms.execute(query)
            if resCd != 0:
                return resCd, msg, resData

            query = sProjDocMana.dDelLinkDocInfo(
                consCode, linkSysDocNum["link_sys_doc_num"], sysDocNum
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "dDelLinkDocInfo Query : " + query,
            )

            resCd, msg, resData = dbms.execute(query)
            if resCd != 0:
                return resCd, msg, resData

        return resCd, msg, resData

    # 문서 리스트를 조회 한다.
    def searchDocList(self, userInfo, userAuth, jobAuth, searchCondition):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        query = sProjDocMana.sSearchDocList(
            userInfo, userAuth, jobAuth, searchCondition
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchDocList Query : " + query,
        )

        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 문서 리스트 개수를 조회 한다.
    def searchDocListCnt(self, userInfo, userAuth, jobAuth, searchCondition):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        query = sProjDocMana.sSearchDocListCnt(
            userInfo, userAuth, jobAuth, searchCondition
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchDocListCnt Query : " + query,
        )

        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 연결된 문서 리스트를 조회 한다.
    def getLinkDocList(self, consCode, sysDocNum):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        query = sProjDocMana.sGetLinkDocList(consCode, sysDocNum)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetLinkDocList Query : " + query,
        )

        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 문서 상세 정보를 조회 한다.
    def getDocDetailInfo(self, userInfo, userAuth, jobAuth, consCode, sysDocNum):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        query = sProjDocMana.sGetDocDetailInfo(
            userInfo, userAuth, jobAuth, consCode, sysDocNum
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetDocDetailInfo Query : " + query,
        )

        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 문서 정보를 업데이트 한다.
    def modifyDocumentInfo(self, uDataInfo):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        query = sProjDocMana.uModifyDocumentInfo(uDataInfo)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uModifyDocumentInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 결재자 정보를 조회 한다.
    def getDocApprovalInfo(self, consCode, sysDocNum):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        query = sProjDocMana.sGetDocApprovalInfo(consCode, sysDocNum)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetDocApprovalInfo Query : " + query,
        )

        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 결재정보를 업데이트 한다.
    def documentApproval(self, updateApproval):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        query = sProjDocMana.uModifyDocumentApproval(updateApproval)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uModifyDocumentApproval Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 문서 결재 상태를 업데이트 한다.
    def updateDocApprovalState(self, updateDocument):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        query = sProjDocMana.uUpdateDocApprovalState(updateDocument)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uUpdateDocApprovalState Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 문서 파일을 관리 한다.
    def docFileManage(
        self, consCode, sysDocNum, docCode, docNum, fileType, fileList, req
    ):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        commServ = commonService()

        result = []
        index = 0

        path = projDocFile.replace("{consCode}", consCode)
        path = path.replace("{sysDocNum}", sysDocNum)

        for fileInfo in fileList:
            if fileInfo["file_type"] == "Y":
                lpath, origName, changeName = commServ.createFilePathAndName(
                    projectHome, "", path, fileInfo, "file_name_new"
                )

                fileData = {
                    "file_path": lpath,
                    "file_original_name": origName,
                    "file_change_name": changeName,
                }

                result.append(fileData)

                commServ.createDir(lpath)
                commServ.saveFile(
                    req.files["f_" + str(index) + "_" + fileType], lpath, changeName
                )

                # DB에 문서 파일 정보를 저장 한다.
                query = sProjDocMana.iPutDocFileInfo(
                    consCode, sysDocNum, docCode, docNum, fileType, index, fileData
                )
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "iPutDocFileInfo Query : " + query,
                )

                resCd, msg, resData = dbms.execute(query)
                if resCd != 0:
                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "message : " + msg,
                    )

                    return resCd, msg, resData

            index += 1

        return constants.REST_RESPONSE_CODE_ZERO, "", result

    # 문서 파일을 삭제 한다.
    def removeDocFileManage(self, consCode, sysDocNum):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjDocMana = sqlProjectDocManage()

        commServ = commonService()

        # DB에 문서 파일 정보를 삭제 한다.
        query = sProjDocMana.dRemoveDocFileInfo(consCode, sysDocNum)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dRemoveDocFileInfo Query : " + query,
        )

        resCd, msg, fileList = dbms.query(query)
        if resCd != 0:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "message : " + msg,
            )

            return resCd, msg, fileList

        for fileInfo in fileList:
            commServ.removeFile(fileInfo["file_path"], fileInfo["file_change_name"])
            folder, ext = os.path.splitext(
                fileInfo["file_path"] + fileInfo["file_change_name"]
            )

        return constants.REST_RESPONSE_CODE_ZERO, "", None
