# _*_coding: utf-8 -*-
import os
import sys
import copy

from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import projectHome
from allscapeAPIMain import companyHome

from common.logManage import logManage

from companyManage.sqlCompanyManage import sqlCompanyManage
from common.commonService import commonService

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servCompanyManage:
    def post_company(self, company):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlCompanyMana = sqlCompanyManage()

        query = sqlCompanyMana.insert_company(
            company["co_code"],
            company["co_name"],
            company["co_type"],
            company["ceo"],
            company["contact"],
            company["address"],
            company["regisnum"],
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "insert_company Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    def get_company_by_code(self, co_code):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlCompanyMana = sqlCompanyManage()

        query = sqlCompanyMana.select_company_by_code(co_code)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_company_by_code Query : " + query,
        )

        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    def get_company_by_regisnum(self, regisnum):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlCompanyMana = sqlCompanyManage()

        query = sqlCompanyMana.select_company_by_regisnum(regisnum)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_company_by_regisnum Query : " + query,
        )

        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    def update_company(self, co_code, company_info):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlCompanyMana = sqlCompanyManage()

        query = sqlCompanyMana.update_company(co_code, company_info)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_company Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    def delete_company(self, co_regisnum):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlCompanyMana = sqlCompanyManage()

        query = sqlCompanyMana.delete_company(co_regisnum)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delete_company Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData
