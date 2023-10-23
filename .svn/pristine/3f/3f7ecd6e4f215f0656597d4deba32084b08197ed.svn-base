# _*_coding: utf-8 -*-
import copy
import os
import sys

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.logManage import logManage
from commManage.sqlCommManage import sqlCommManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servCommManage:

    # 코드 리스트를 제공 한다.
    def getCodeList(self, reqType):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        sCommMana = sqlCommManage()

        # 쿼리 생성
        query = sCommMana.sGetCodeList(reqType)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetCodeList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 코드에 대한 코드명을 제공 한다.
    def getCodeName(self, code):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        sCommMana = sqlCommManage()

        # 쿼리 생성
        query = sCommMana.sGetCodeName(code)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetCodeName Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 회사 리스트를 제공 한다.
    def getCoList(self, coName):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        sCommMana = sqlCommManage()

        # 쿼리 생성
        query = sCommMana.sGetCoList(coName)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetCoList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 시스템 설정 값을 제공 한다.
    def getSysCfg(self, cfgName):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sCommMana = sqlCommManage()

        # 쿼리 생성
        query = sCommMana.sGetSysCfg(cfgName)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetSysCfg Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 시스템 설정 값을 업데이트 한다.
    def modifySysCfg(self, cfgName, cfgValue):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sCommMana = sqlCommManage()

        # 쿼리 생성
        query = sCommMana.uModifySysCfg(cfgName, cfgValue)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uModifySysCfg Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 시스템 문서 번호를 생성 한다.
    def createSysDocNum(self):
        resCd, msg, resData = self.getSysCfg("cfg_sysdoc_num")

        if resCd != 0:
            return resCd, msg, resData

        return resCd, msg, int(resData["cfg_value"])

    # 시스템 문서 번호를 증가 한다.
    def increaseSysDocNum(self):
        resCd, msg, resData = self.getSysCfg("cfg_sysdoc_num")

        if resCd != 0:
            return resCd, msg, resData

        curSysNum = int(resData["cfg_value"])
        curSysNum += 1

        resCd, msg, resData = self.modifySysCfg("cfg_sysdoc_num", curSysNum)

        if resCd != 0:
            return resCd, msg, resData

        return resCd, "", None

    # 시스템 문서 번호를 감소 한다.
    def decreaseSysDocNum(self):
        resCd, msg, resData = self.getSysCfg("cfg_sysdoc_num")

        if resCd != 0:
            return resCd, msg, resData

        curSysNum = int(resData["cfg_value"])
        curSysNum -= 1

        resCd, msg, resData = self.modifySysCfg("cfg_sysdoc_num", curSysNum)

        if resCd != 0:
            return resCd, msg, resData

        return resCd, "", None

    # 회사 코드를 생성 한다.
    def createCoNum(self):
        resCd, msg, resData = self.getSysCfg("cfg_company_num")

        if resCd != 0:
            return resCd, msg, resData

        return resCd, msg, int(resData["cfg_value"])

    # 회사 코드를 증가 한다.
    def increaseCoNum(self):
        resCd, msg, resData = self.getSysCfg("cfg_company_num")

        if resCd != 0:
            return resCd, msg, resData

        curSysNum = int(resData["cfg_value"])
        curSysNum += 1

        resCd, msg, resData = self.modifySysCfg("cfg_company_num", curSysNum)

        if resCd != 0:
            return resCd, msg, resData

        return resCd, "", None

    # 회사 코드를 감소 한다.
    def decreaseCoNum(self):
        resCd, msg, resData = self.getSysCfg("cfg_company_num")

        if resCd != 0:
            return resCd, msg, resData

        curSysNum = int(resData["cfg_value"])
        curSysNum -= 1

        resCd, msg, resData = self.modifySysCfg("cfg_company_num", curSysNum)

        if resCd != 0:
            return resCd, msg, resData

        return resCd, "", None

    # 프로젝트 코드를 생성 한다.
    def createProjNum(self):
        resCd, msg, resData = self.getSysCfg("cfg_project_num")

        if resCd != 0:
            return resCd, msg, resData

        self.increaseProjNum()

        return resCd, msg, int(resData["cfg_value"])

    # 프로젝트 코드를 증가 한다.
    def increaseProjNum(self):
        resCd, msg, resData = self.getSysCfg("cfg_project_num")

        if resCd != 0:
            return resCd, msg, resData

        curSysNum = int(resData["cfg_value"])
        curSysNum += 1

        resCd, msg, resData = self.modifySysCfg("cfg_project_num", curSysNum)

        if resCd != 0:
            return resCd, msg, resData

        return resCd, "", None

    # 프로젝트 코드를 감소 한다.
    def decreaseProjNum(self):
        resCd, msg, resData = self.getSysCfg("cfg_project_num")

        if resCd != 0:
            return resCd, msg, resData

        curSysNum = int(resData["cfg_value"])
        curSysNum -= 1

        resCd, msg, resData = self.modifySysCfg("cfg_project_num", curSysNum)

        if resCd != 0:
            return resCd, msg, resData

        return resCd, "", None
