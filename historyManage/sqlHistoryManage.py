# _*_coding: utf-8 -*-

from common import util_time

SELECT_USER_CO_INFO = """
	SELECT
		ID AS id,
		CO_CODE AS co_code,
		CO_NAME AS co_name,
		CO_CEO AS co_ceo,
		CO_CONTACT AS co_contact,
		CO_ADDRESS AS co_address,
		CO_TENURE_START_DATE AS co_tenure_start_date,
		CO_TENURE_END_DATE AS co_tenure_end_date
	FROM USER_COMPANY_HISTORY
	WHERE 1=1
"""


INSERT_USER_CO_INFO = "INSERT INTO USER_COMPANY_HISTORY(ID, CO_CODE, CO_NAME, CO_CEO, CO_CONTACT, CO_ADDRESS, CO_TENURE_START_DATE, CO_TENURE_END_DATE) "

DELETE_USER_CO_INFO = "DELETE FROM USER_COMPANY_HISTORY WHERE 1=1 "


SELECT_PROJ_HIS_INFO = """
	SELECT
		ID AS id,
		CO_CODE AS co_code,
		CO_NAME AS co_name,
		CONS_CODE AS cons_code,
		CONS_NAME AS cons_name,
		LOCATION AS location,
		PROJ_PROGRESS_START_DATE AS proj_progress_start_date,
		PROJ_PROGRESS_END_DATE AS proj_progress_end_date,
		REG_DATE AS reg_date
	FROM USER_PROJECT_HISTORY
	WHERE 1=1
"""


INSERT_PROJ_HIS_INFO = "INSERT INTO USER_PROJECT_HISTORY(ID, CO_CODE, CO_NAME, CONS_CODE, CONS_NAME, LOCATION, REG_DATE, PROJ_PROGRESS_START_DATE, PROJ_PROGRESS_END_DATE) "

DELETE_PROJ_HIS_INFO = "DELETE FROM USER_PROJECT_HISTORY WHERE 1=1 "

# 이력 관리 Query Class
class sqlHistoryManage:

    # 재직 정보 조회 Query를 생성 한다.
    def sGetCoHistoryList(self, searchList):
        query = SELECT_USER_CO_INFO
        index = 0
        listSize = len(searchList)
        for searchInfo in searchList:
            if listSize > 1:
                if index < listSize - 1:
                    query += (
                        "AND "
                        + searchInfo["key"]
                        + ' = "'
                        + searchInfo["value"]
                        + '", '
                    )
                else:
                    query += (
                        "AND " + searchInfo["key"] + ' = "' + searchInfo["value"] + '" '
                    )

                    index += 1
            else:
                query += (
                    "AND " + searchInfo["key"] + ' = "' + searchInfo["value"] + '" '
                )

        return query

    # 1. 재직 정보를 저장 Query를 생성 한다.
    def iPutUserCompanyHistory(self, userInfo):
        query = INSERT_USER_CO_INFO

        query += "VALUES( "

        query += '"' + userInfo["id"] + '", '
        query += '"' + userInfo["co_code"] + '", '
        query += '"' + userInfo["co_name"] + '", '
        query += '"' + userInfo["co_ceo"] + '", '
        query += '"' + userInfo["co_contact"] + '", '
        query += '"' + userInfo["co_address"] + '", '
        query += '"' + userInfo["co_appro_date"] + '", '
        query += '"' + util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14) + '" '

        query += ")"

        return query

    # 재직 정보 삭제 Query를 생성 한다.
    def dDelUserCompanyHistory(self, userInfo):
        query = DELETE_USER_CO_INFO

        query += 'AND ID = "' + userInfo["id"] + '" '
        query += 'AND CO_CODE = "' + userInfo["co_code"] + '" '
        query += 'AND CO_APPRO_DATE = "' + userInfo["co_appro_date"] + '" '

        return query

    # 프로젝트 이력 조회 Query를 생성 한다.
    def sGetProjHistoryList(self, searchList):
        query = SELECT_PROJ_HIS_INFO
        index = 0
        listSize = len(searchList)
        for searchInfo in searchList:
            if listSize > 1:
                if index < listSize - 1:
                    query += (
                        "AND " + searchInfo["key"] + ' = "' + searchInfo["value"] + '" '
                    )
                else:
                    query += (
                        "AND " + searchInfo["key"] + ' = "' + searchInfo["value"] + '" '
                    )

                    index += 1
            else:
                query += (
                    "AND " + searchInfo["key"] + ' = "' + searchInfo["value"] + '" '
                )

        return query

    # 프로젝트 정보 저장 Query를 생성 한다.
    def iPutProjHistoryList(self, userInfo, projHisInfo):

        query = INSERT_PROJ_HIS_INFO

        # query += "SELECT"

        query += "VALUES( "

        query += '"' + userInfo["id"] + '", '
        query += '"' + userInfo["co_code"] + '", '
        query += '"' + userInfo["co_name"] + '", '
        query += '"' + projHisInfo["cons_code"] + '", '
        query += '"' + projHisInfo["cons_name"] + '", '
        query += '"' + projHisInfo["location"] + '", '
        query += (
            '"' + util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14) + '", '
        )

        query += '"' + projHisInfo["cons_start_date"] + '", '
        query += '"' + projHisInfo["cons_end_date"] + '" '
        query += ")"

        # query += (
        #    'IFNULL(MIN(CONS_START_DATE), "") AS CONS_START_DATE, IFNULL(MAX(CONS_END_DATE), "") AS CONS_END_DATE FROM CONS_FFF WHERE CONS_CODE = "'
        #    + projHisInfo["cons_code"]
        #    + '" '
        # )
        # query += 'AND CO_CODE = "' + userInfo["co_code"] + '"'

        return query

    # 프로젝트 이력 정보 삭제 Query를 생성 한다.
    def dDelProjHistoryList(self, userInfo, projHisInfo):
        query = DELETE_PROJ_HIS_INFO

        query += 'AND ID = "' + userInfo["id"] + '" '
        query += 'AND CO_CODE = "' + userInfo["co_code"] + '" '
        query += 'AND CONS_CODE = "' + projHisInfo["cons_code"] + '" '

        return query
