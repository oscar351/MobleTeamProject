# _*_coding: utf-8 -*-


from common.commUtilService import commUtilService


INSERT_PROJECTSITEINSP_INFO = """INSERT INTO PROJECT_SITE_INSPECTION(
		CONS_CODE,
		AUTHOR_ID,
		WRITING_TIME,
		TITLE,
		CONTENT,
		FILE_PATH,
		FILE_ORIGINAL_NAME,
		FILE_CHANGE_NAME) """


SELECT_PROJECTSITEINSP_INFO = """SELECT 
									A.INSP_ID AS insp_id,
									A.CONS_CODE AS cons_code,
									A.AUTHOR_ID AS author_id,
									A.WRITING_TIME AS writing_time,
									A.TITLE AS title,
									A.CONTENT AS content,
									A.FILE_PATH AS file_path,
									A.FILE_ORIGINAL_NAME AS file_original_name,
									A.FILE_CHANGE_NAME AS file_change_name,
									A.INSP_CONTENT AS insp_content,
									A.INSP_FILE_PATH AS insp_file_path,
									A.INSP_FILE_ORIGINAL_NAME AS insp_file_original_name,
									A.INSP_FILE_CHANGE_NAME AS insp_file_change_name,
									A.INSP_AUTH_ID AS insp_auth_id,
									A.INSP_WRITING_TIME AS insp_writing_time
								FROM
									PROJECT_SITE_INSPECTION A
								WHERE
									1=1 """

UPDATE_PROJECTSITEINSP_INFO = """UPDATE PROJECT_SITE_INSPECTION SET """


# 현장 점검 SQL
class sqlProjectInspManage:

    # 현장 점검 저장
    def iPutInspInfo(self, userId, dataInfo):

        query = INSERT_PROJECTSITEINSP_INFO

        query += "VALUES("
        query += '"' + dataInfo["cons_code"] + '", '
        query += '"' + userId + '", '
        query += '"' + dataInfo["writing_time"] + '", '
        query += '"' + dataInfo["title"] + '", '
        query += '"' + dataInfo["content"] + '", '
        query += '"' + dataInfo["file_path"] + '", '
        query += '"' + dataInfo["file_original_name"] + '", '
        query += '"' + dataInfo["file_change_name"] + '"'

        query += ")"

        return query

    # 현장 점검 데이터를 가져 온다.
    def sGetInspInfoObj(self, inspId):
        query = SELECT_PROJECTSITEINSP_INFO

        query += "AND A.INSP_ID = " + str(inspId)

        return query

    # 현장 점검 데이터를 수정 한다.
    def uUpdateInspInfo(self, dataInfo):
        query = UPDATE_PROJECTSITEINSP_INFO

        query += 'TITLE = "' + dataInfo["title"] + '", '
        query += 'CONTENT = "' + dataInfo["content"] + '", '
        query += 'FILE_PATH = "' + dataInfo["file_path"] + '", '
        query += 'FILE_ORIGINAL_NAME = "' + dataInfo["file_original_name"] + '", '
        query += 'FILE_CHANGE_NAME = "' + dataInfo["file_change_name"] + '" '

        query += "WHERE INSP_ID = " + str(dataInfo["insp_id"])

        return query

    # 현장 점검 정보 리스트를 조회 한다.
    def sGetInspInfoList(self, params):
        commUtilServ = commUtilService()

        query = "SELECT * FROM ("

        query += SELECT_PROJECTSITEINSP_INFO

        query += 'AND A.CONS_CODE = "' + params["cons_code"] + '" '

        if commUtilServ.dataCheck(params["search_title"]) != False:
            query += 'AND A.TITLE LIKE "%' + params["search_title"] + '%" '

        if commUtilServ.dataCheck(params["search_start_writing_date"]) != False:
            query += (
                'AND A.WRITING_TIME >= "' + params["search_start_writing_date"] + '" '
            )

        if commUtilServ.dataCheck(params["search_end_writing_date"]) != False:
            query += (
                'AND A.WRITING_TIME <= "' + params["search_end_writing_date"] + '" '
            )

        query += ") B WHERE 1=1 "

        query += "ORDER BY " + params["sort_column"] + " " + params["sort_type"] + " "
        query += "LIMIT " + params["start_num"] + ", " + params["end_num"]

        return query

    # 현장 점검 정보 리스트 개수를 조회 한다.
    def sGetInspInfoCnt(self, params):
        commUtilServ = commUtilService()

        query = "SELECT COUNT(*) AS cnt FROM ("

        query += SELECT_PROJECTSITEINSP_INFO

        query += 'AND A.CONS_CODE = "' + params["cons_code"] + '" '

        if commUtilServ.dataCheck(params["search_title"]) != False:
            query += 'AND A.TITLE LIKE "%' + params["search_title"] + '%" '

        if commUtilServ.dataCheck(params["search_start_writing_date"]) != False:
            query += (
                'AND A.WRITING_TIME >= "' + params["search_start_writing_date"] + '" '
            )

        if commUtilServ.dataCheck(params["search_end_writing_date"]) != False:
            query += (
                'AND A.WRITING_TIME <= "' + params["search_end_writing_date"] + '" '
            )

        query += ") B WHERE 1=1 "

        return query

    # 현장 점검 조치사항 데이터를 업데이트 한다.
    def uUpdateInspActionInfo(self, userId, dataInfo):
        query = UPDATE_PROJECTSITEINSP_INFO

        query += 'INSP_CONTENT = "' + dataInfo["insp_content"] + '", '
        query += 'INSP_FILE_PATH = "' + dataInfo["insp_file_path"] + '", '
        query += (
            'INSP_FILE_ORIGINAL_NAME = "' + dataInfo["insp_file_original_name"] + '", '
        )
        query += 'INSP_FILE_CHANGE_NAME = "' + dataInfo["insp_file_change_name"] + '", '
        query += 'INSP_AUTH_ID = "' + userId + '", '
        query += 'INSP_WRITING_TIME = "' + dataInfo["insp_writing_time"] + '" '

        query += "WHERE INSP_ID = " + str(dataInfo["insp_id"])

        return query
