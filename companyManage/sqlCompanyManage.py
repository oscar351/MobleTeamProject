# _*_coding: utf-8 -*-
import json
from common import constants

INSERT_COMPANY_INFO = " ".join(
    [
        "INSERT INTO",
        "COMPANY(CO_CODE, CO_NAME, CO_TYPE, CEO, CONTACT, ADDRESS, REGISNUM)"
        "VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')",
    ]
)

SELECT_COMPANY_INFO_BY_CODE = " ".join(
    [
        "SELECT",
        "CO_CODE AS co_code,",
        "CO_NAME AS co_name,",
        "CO_TYPE AS co_type,",
        "CEO AS co_ceo,",
        "CONTACT AS co_contact,",
        "ADDRESS AS co_address,",
        "REGISNUM AS co_regisnum",
        "FROM COMPANY",
        "WHERE CO_CODE = '{}'",
    ]
)

SELECT_COMPANY_INFO_BY_REGISNUM = " ".join(
    [
        "SELECT",
        "CO_CODE AS co_code,",
        "CO_NAME AS co_name,",
        "CO_TYPE AS co_type,",
        "CEO AS co_ceo,",
        "CONTACT AS co_contact,",
        "ADDRESS AS co_address,",
        "REGISNUM AS co_regisnum",
        "FROM COMPANY",
        "WHERE REGISNUM = '{}'",
    ]
)

UPDATE_COMPANY_INFO = " ".join(
    [
        "UPDATE",
        "COMPANY",
        "SET ",
    ]
)

DELETE_COMPANY_INFO = " ".join(["DELETE FROM", "COMPANY", "WHERE REGISNUM = '{}'"])


# 회사 관리 Query Class
class sqlCompanyManage:

    # 문서 정보를 저장 한다.
    def insert_company(
        self, co_code, co_name, co_type, ceo, contact, address, regisnum
    ):
        query = INSERT_COMPANY_INFO.format(
            co_code, co_name, co_type, ceo, contact, address, regisnum
        )

        return query

    def select_company_by_code(self, co_code):
        query = SELECT_COMPANY_INFO_BY_CODE.format(co_code)

        return query

    def select_company_by_regisnum(self, regisnum):
        query = SELECT_COMPANY_INFO_BY_REGISNUM.format(regisnum)

        return query

    def update_company(self, coCode, updateCoInfoList):

        query = UPDATE_COMPANY_INFO

        index = 0
        listSize = len(updateCoInfoList)
        for updateCoInfo in updateCoInfoList:

            if listSize > 1:

                if index < listSize - 1:
                    query += (
                        updateCoInfo["key"] + ' = "' + updateCoInfo["value"] + '", '
                    )
                else:
                    query += updateCoInfo["key"] + ' = "' + updateCoInfo["value"] + '" '

                index += 1
            else:
                query += updateCoInfo["key"] + ' = "' + updateCoInfo["value"] + '" '

        query += 'WHERE CO_CODE = "' + coCode + '"'

        return query

    def delete_company(self, co_regisnum):

        query = DELETE_COMPANY_INFO.format(co_regisnum)

        return query
