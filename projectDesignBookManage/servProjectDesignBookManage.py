# _*_coding: utf-8 -*-
import os
import shutil
import sys
import copy
import json
import pdf2image
import threading
import multiprocessing

from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import projDesignBookFile
from allscapeAPIMain import projectHome

from common.logManage import logManage
from common import util_time
from common import constants

from common.commonService import commonService
from common.pdfService import pdfService
from projectDesignBookManage.sqlProjectDesignBookManage import (
    sqlProjectDesignBookManage,
)
from projectFloorPlanManage.servProjectFloorPlanManage import servProjectFloorPlanManage


logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectDesignBookManage:

    # 설계도서 정보를 저장 한다.
    def putDesignBookInfo(self, params, req):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlProjDBMana = sqlProjectDesignBookManage()
        commServ = commonService()

        result = []
        index = 0

        path = projDesignBookFile.replace("{consCode}", params["cons_code"])

        lpath, origName, changeName = commServ.createFilePathAndName(
            projectHome, "", path, params, "file_name"
        )

        params["lpath"] = lpath
        params["origName"] = origName
        params["changeName"] = changeName
        params["regDate"] = util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14)

        params["name"], params["ext"] = os.path.splitext(changeName)

        commServ.createDir(lpath)
        commServ.saveFile(req.files["f_file"], lpath, changeName, autoConvert=False)

        # 설계도서 파일 정보를 저장 한다.
        query = sqlProjDBMana.iPutDesignBookInfo(params)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutDesignBookInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)
        if resCd != 0:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "message : " + msg,
            )

            commServ.removeFile(lpath, changeName)

            return resCd, msg, resData

        # 설계도면 pdf 파일을 이미지로 변환한다
        if params["design_book_type"] == "DB000003" and params["ext"] == ".pdf":
            image_converter = multiprocessing.Process(
                target=self.convertFloorPlan, args=(params,)
            )
            image_converter.start()

        return resCd, msg, resData

    def convertFloorPlan(self, params):
        """설계도면 pdf파일을 이미지로 변환한다"""

        pdfServ = pdfService()
        servProjFPMana = servProjectFloorPlanManage()

        params["folder"] = params["lpath"] + params["name"]
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "설계도면을 이미지로 변환을 시도합니다 : " + params["folder"],
        )
        try:
            pages, subpages, codes, titles = pdfServ.pdf2image(
                params["lpath"] + params["changeName"]
            )
        except Exception as e:
            logs.war(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "이미지 변환실패 : " + str(e),
            )
            return

        for page, subpage, code, title in zip(pages, subpages, codes, titles):
            params["page"] = page
            params["subpage"] = subpage
            params["code"] = code
            params["title"] = title
            params["img_path"] = "{}/{}.jpg".format(params["folder"], page)

            resCd, msg, resData = servProjFPMana.postFloorPlan(params)
            if resCd != 0:
                logs.war(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "FloorPlan DBerror : " + msg,
                )
                return
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "설계도면을 이미지로 변환하였습니다",
        )
        return

    def getDesignBookList(self, consCode, designBookType):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlProjDBMana = sqlProjectDesignBookManage()

        # 쿼리 생성
        query = sqlProjDBMana.sGetDesignBookList(
            consCode, designBookType
        )  # 설계도서 리스트 Read Query 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetDesignBookList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    def getDesignBookVer(self, consCode, designBookType, ver_info):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlProjDBMana = sqlProjectDesignBookManage()

        # 쿼리 생성
        query = sqlProjDBMana.sGetDesignBookVer(
            consCode, designBookType, ver_info
        )  # 설계도서 특정버전 Query 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetDesignBookVer Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 문서 파일을 삭제 한다.
    def delDesignBook(self, consCode, designBookType, fileName):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlProjDBMana = sqlProjectDesignBookManage()

        commServ = commonService()

        # 지우고자 하는 파일 정보를 가져 온다.
        query = sqlProjDBMana.sGetDesignBook(consCode, designBookType, fileName)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetDesignBook Query : " + query,
        )

        resCd, msg, fileInfo = dbms.queryForObject(query)
        if resCd != 0:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "message : " + msg,
            )

            return resCd, msg, fileInfo

        if fileInfo == None:
            return constants.REST_RESPONSE_CODE_DATAFAIL, "해당 파일 정보가 없습니다.", None

        # 설계 도서 정보를 삭제 한다..
        query = sqlProjDBMana.dDelDesignBook(consCode, designBookType, fileName)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelDesignBook Query : " + query,
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

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "file_path : " + fileInfo["file_path"] + ", fileName : " + fileName,
        )
        commServ.removeFile(fileInfo["file_path"], fileName)

        # 관련된 이미지파일들도 지운다.
        if designBookType == "DB000003":
            folder, ext = os.path.splitext(fileName)
            folder_path = fileInfo["file_path"] + folder
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

        return constants.REST_RESPONSE_CODE_ZERO, "", None
