# _*_coding: utf-8 -*-
import json
from common import constants


SELECT_COMAPPRO_INFO = """
	SELECT
		CAM.REQ_APPROVAL_ID AS req_approval_id, (SELECT USER_NAME FROM USER WHERE ID = CAM.REQ_APPROVAL_ID) AS req_approval_name,
		CAM.REQ_APPROVAL_TYPE AS req_approval_type, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = CAM.REQ_APPROVAL_TYPE) AS req_approval_type_name,
		CAM.APPROVAL_STATUS AS approval_status, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = CAM.APPROVAL_STATUS) AS approval_status_name,
		CAM.CONTENTS AS contents,
		CAM.APPROVAL_ID AS approval_id, (SELECT USER_NAME FROM USER WHERE ID = CAM.APPROVAL_ID) AS approval_name,
		CAM.REQ_APPROVAL_DATE AS req_approval_date, CAM.COMPLETE_APPROVAL_DATE AS complete_approval_date,
		IFNULL(CAM.NEXT_APPROVAL_INFO, '') AS next_approval_info
	FROM COMMON_APPROVAL_MANAGE CAM
	WHERE 1=1
"""

UPDATE_COMAPPRO_INFO = "UPDATE COMMON_APPROVAL_MANAGE SET "


SEARCH_1 = 'AND (CAM.APPROVAL_ID = "{userId}" OR REQ_APPROVAL_ID = "{userId}") '
SEARCH_2 = 'AND CAM.REQ_APPROVAL_DATE >= "{req_approval_start_date}" '
SEARCH_3 = 'AND CAM.REQ_APPROVAL_DATE <= "{req_approval_end_date}" '
SEARCH_4 = 'AND CAM.APPROVAL_STATUS = "{approval_status}" '
SEARCH_5 = 'AND CAM.REQ_APPROVAL_DATE = "{req_approval_date}" '

ORDER_BY_REQ_APPROVAL_DATE = "ORDER BY CAM.REQ_APPROVAL_DATE DESC"


INSERT_COMAPPRO_INFO = """INSERT INTO COMMON_APPROVAL_MANAGE(REQ_APPROVAL_ID, REQ_APPROVAL_TYPE, APPROVAL_STATUS, CONTENTS, APPROVAL_ID, REQ_APPROVAL_DATE, COMPLETE_APPROVAL_DATE, NEXT_APPROVAL_INFO) """

DELETE_COMAPPRO_INFO = """DELETE FROM COMMON_APPROVAL_MANAGE WHERE 1=1 """

# 공통 결재 관리 Query Class
class sqlCommonApprovalManage:

    # 공통 결재 정보를 저장 한다.
    def iPutCommonApprovalInfo(self, common_approval_manage):
        query = INSERT_COMAPPRO_INFO

        query += "VALUES("
        query += '"' + common_approval_manage["req_approval_id"] + '", '
        query += '"' + common_approval_manage["req_approval_type"] + '", '
        query += '"' + common_approval_manage["approval_status"] + '", '
        query += (
            "'"
            + json.dumps(common_approval_manage["contents"], ensure_ascii=False)
            + "', "
        )
        query += '"' + common_approval_manage["approval_id"] + '", '
        query += '"' + common_approval_manage["req_approval_date"] + '", '
        query += '"", '
        query += (
            "'"
            + json.dumps(
                common_approval_manage["next_approval_info"], ensure_ascii=False
            )
            + "' "
        )
        query += ")"

        return query

    # 공통 결재 정보 리스트를 조회 한다.
    def sGetCommonApprovalInfoList(self, userId, params):
        query = SELECT_COMAPPRO_INFO

        if userId != "":
            query = query + SEARCH_1.replace("{userId}", userId)

        if params["search_req_approval_start_date"] != "":
            query = query + SEARCH_2.replace(
                "{req_approval_start_date}", params["search_req_approval_start_date"]
            )

        if params["search_req_approval_end_date"] != "":
            query = query + SEARCH_3.replace(
                "{req_approval_end_date}", params["search_req_approval_end_date"]
            )

        if params["search_approval_status"] != "":
            query = query + SEARCH_4.replace(
                "{approval_status}", params["search_approval_status"]
            )

        query = query + ORDER_BY_REQ_APPROVAL_DATE

        return query

    # 공통 결재 정보 리스트를 조회 한다.
    def sGetDetailCommAppro(self, userId, reqApproDate):
        query = SELECT_COMAPPRO_INFO

        if userId != "":
            query = query + SEARCH_1.replace("{userId}", userId)

        if reqApproDate != "":
            query = query + SEARCH_5.replace("{req_approval_date}", reqApproDate)

        return query

    def uUpdateCommApproval(self, updateCommApproData):
        query = UPDATE_COMAPPRO_INFO

        query += 'APPROVAL_STATUS = "' + updateCommApproData["approval_status"] + '", '
        query += (
            'COMPLETE_APPROVAL_DATE = "'
            + updateCommApproData["complete_approval_date"]
            + '" '
        )

        query += (
            'WHERE REQ_APPROVAL_ID = "'
            + updateCommApproData["search_req_approval_id"]
            + '" '
        )
        query += (
            'AND REQ_APPROVAL_DATE = "'
            + updateCommApproData["search_req_approval_date"]
            + '" '
        )
        query += (
            'AND APPROVAL_ID = "' + updateCommApproData["search_approval_id"] + '" '
        )

        return query

    def dDelCommonApprovalInfo(self, delCommApproData):
        query = DELETE_COMAPPRO_INFO

        query += 'AND REQ_APPROVAL_ID = "' + delCommApproData["req_approval_id"] + '" '
        query += (
            'AND REQ_APPROVAL_DATE = "' + delCommApproData["req_approval_date"] + '" '
        )
        query += (
            'AND REQ_APPROVAL_TYPE = "' + delCommApproData["req_approval_type"] + '" '
        )

        return query
