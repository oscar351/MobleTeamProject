# _*_coding: utf-8 -*-
import json
from common import constants

SELECT_DESIGNBOOK_INFO = """
	SELECT
		DBM.CONS_CODE AS cons_code, (SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = DBM.CONS_CODE) AS cons_name,
		DBM.CLASSIFICATION_CODE AS classification_code, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = DBM.CLASSIFICATION_CODE) AS classification_name,
		DBM.VER_INFO AS ver_info, DBM.REG_DATE AS reg_date, DBM.REG_ID AS reg_id, (SELECT USER_NAME FROM USER WHERE ID = DBM.REG_ID) AS user_name,
		DBM.ORIGINAL_NAME AS original_name, DBM.CHANGE_NAME AS change_name, DBM.FILE_PATH AS file_path, DBM.EXTENSION_TYPE AS extension_type
	FROM DESIGN_BOOK_MANAGE DBM
	WHERE 1=1
	{1}
	{2}
	{3}
	ORDER BY REG_DATE DESC
	"""


SELECT_DESIGNBOOK_CONDITION_1 = 'AND DBM.CONS_CODE = "{cons_code}"'
SELECT_DESIGNBOOK_CONDITION_2 = 'AND DBM.CLASSIFICATION_CODE = "{classification_code}"'
SELECT_DESIGNBOOK_CONDITION_3 = 'AND DBM.CHANGE_NAME = "{change_name}"'
SELECT_DESIGNBOOK_CONDITION_4 = 'AND DBM.VER_INFO = "{ver_info}"'

DELETE_DESIGNBOOK_CONDITION_1 = 'AND CONS_CODE = "{cons_code}"'
DELETE_DESIGNBOOK_CONDITION_2 = 'AND CLASSIFICATION_CODE = "{classification_code}"'
DELETE_DESIGNBOOK_CONDITION_3 = 'AND CHANGE_NAME = "{change_name}"'

INSERT_DESIGNBOOK_INFO = "INSERT INTO DESIGN_BOOK_MANAGE(CONS_CODE, CLASSIFICATION_CODE, VER_INFO, REG_DATE, REG_ID, ORIGINAL_NAME, CHANGE_NAME, FILE_PATH, EXTENSION_TYPE) "


DELETE_DESIGNBOOK_INFO = "DELETE FROM DESIGN_BOOK_MANAGE WHERE 1=1 {1} {2} {3}"


# 설계도서 정보 관리 Query Class
class sqlProjectDesignBookManage:

    # 설계도서 리스트 정보를 가져 온다.
    def sGetDesignBookList(self, consCode, designBookType):
        query = SELECT_DESIGNBOOK_INFO

        query = query.replace(
            "{1}", SELECT_DESIGNBOOK_CONDITION_1.replace("{cons_code}", consCode)
        )
        query = query.replace(
            "{2}",
            SELECT_DESIGNBOOK_CONDITION_2.replace(
                "{classification_code}", designBookType
            ),
        )

        query = query.replace("{3}", "")

        return query

    # 설계도서 특정 버전을 가져 온다.
    def sGetDesignBookVer(self, consCode, designBookType, ver_info):
        query = SELECT_DESIGNBOOK_INFO

        query = query.replace(
            "{1}", SELECT_DESIGNBOOK_CONDITION_1.replace("{cons_code}", consCode)
        )
        query = query.replace(
            "{2}",
            SELECT_DESIGNBOOK_CONDITION_2.replace(
                "{classification_code}", designBookType
            ),
        )
        query = query.replace(
            "{3}",
            SELECT_DESIGNBOOK_CONDITION_4.replace("{ver_info}", ver_info),
        )

        return query

    # 설계도서 정보를 가져 온다.
    def sGetDesignBook(self, consCode, designBookType, fileName):
        query = SELECT_DESIGNBOOK_INFO

        query = query.replace(
            "{1}", SELECT_DESIGNBOOK_CONDITION_1.replace("{cons_code}", consCode)
        )
        query = query.replace(
            "{2}",
            SELECT_DESIGNBOOK_CONDITION_2.replace(
                "{classification_code}", designBookType
            ),
        )
        query = query.replace(
            "{3}", SELECT_DESIGNBOOK_CONDITION_3.replace("{change_name}", fileName)
        )

        return query

    # 설계도서 정보를 저장 한다.
    def iPutDesignBookInfo(self, dataInfo):
        query = INSERT_DESIGNBOOK_INFO

        query += "VALUES("
        query += '"' + dataInfo["cons_code"] + '", '
        query += '"' + dataInfo["design_book_type"] + '", '
        query += '"' + dataInfo["ver_info"] + '", '
        query += '"' + dataInfo["regDate"] + '", '
        query += '"' + dataInfo["regId"] + '", '
        query += '"' + dataInfo["origName"] + '", '
        query += '"' + dataInfo["changeName"] + '", '
        query += '"' + dataInfo["lpath"] + '", '
        query += '"' + dataInfo["ext"] + '" '
        query += ")"

        return query

    # 설계 도서 정보를 삭제 한다.
    def dDelDesignBook(self, consCode, designBookType, fileName):
        query = DELETE_DESIGNBOOK_INFO

        query = query.replace(
            "{1}", DELETE_DESIGNBOOK_CONDITION_1.replace("{cons_code}", consCode)
        )
        query = query.replace(
            "{2}",
            DELETE_DESIGNBOOK_CONDITION_2.replace(
                "{classification_code}", designBookType
            ),
        )
        query = query.replace(
            "{3}", DELETE_DESIGNBOOK_CONDITION_3.replace("{change_name}", fileName)
        )

        return query
