# _*_coding: utf-8 -*-

from common.commUtilService import commUtilService

from common import constants


INSERT_DETECTION_INFO = """INSERT INTO PROJECT_DETECTION(CONS_CODE, DETE_REQ_SYS_DOC_NUM, DETE_REQ_DOC_NUM, DETE_REQ_DOC_CODE, CO_CODE, CONSTR_TYPE_CD, DETAIL_CONSTR_TYPE_CD, LOCATION, DETE_REQ_DATE, DETE_AREA, DETE_REQ_WRITER_DATE, CONT_1ST_ID, CONT_2ST_ID) """


UPDATE_DETECTION_INFO = """UPDATE PROJECT_DETECTION SET """


INSERT_DETECHKRESULT_INFO = """INSERT INTO PROJECT_DETECTION_CHECK_RESULT(CONS_CODE, DETE_REQ_SYS_DOC_NUM, CHK_MSG, INSP_CRID_CD, CONT_1ST_RESULT, CONT_2ST_RESULT) """

UPDATE_DETECHKRESULT_INFO = """UPDATE PROJECT_DETECTION_CHECK_RESULT SET """
DELETE_DETECHKRESULT_INFO = (
    """DELETE FROM PROJECT_DETECTION_CHECK_RESULT WHERE 1 = 1 """
)
SELECT_DETECTIONLIST_INFO = """
	SELECT 
		AD.CONS_CODE AS cons_code, AD.DETE_REQ_SYS_DOC_NUM AS dete_req_sys_doc_num, AD.DETE_REQ_DOC_NUM AS dete_req_doc_num, 
		AD.DETE_REQ_DOC_CODE AS dete_req_doc_code, AD.DETE_REQ_DOC_NAME AS dete_req_doc_name,
		AD.CO_CODE AS co_code, AD.CO_NAME AS co_name,
		AD.CONSTR_TYPE_CD AS constr_type_cd, AD.CONSTR_TYPE_NAME AS constr_type_name,
		AD.DETAIL_CONSTR_TYPE_CD AS detail_constr_type_cd, AD.DETAIL_CONSTR_TYPE_NAME AS detail_constr_type_name,
		AD.DETE_REQ_DATE AS dete_req_date, AD.LOCATION AS location, AD.DETE_AREA AS dete_area, AD.DETE_REQ_WRITER_DATE AS dete_req_writer_date,
		AD.DETE_RES_SYS_DOC_NUM AS res_sys_doc_num, AD.DETE_RES_DOC_NUM AS dete_res_doc_num,
		AD.DETE_RES_DOC_CODE AS res_doc_code, AD.DETE_RES_DOC_NAME AS dete_res_doc_name,
		AD.DETE_DATE AS dete_date, AD.DETE_RESULT AS dete_result, AD.INSTRUCTION AS instruction,
		AD.CONT_1ST_ID AS cont_1st_id, AD.CONT_1ST_NAME AS cont_1st_name,
		AD.CONT_2ST_ID AS cont_2st_id, AD.CONT_2ST_NAME AS cont_2st_name,
		AD.SUPE_1ST_ID AS supe_1st_id, AD.SUPE_1ST_NAME AS supe_1st_name,
		AD.SUPE_2ST_ID AS supe_2st_id, AD.SUPE_2ST_NAME AS supe_2st_name,
		AD.DETE_REQ_WRITER AS dete_req_writer, AD.DETE_REQ_WRITER_NM AS dete_req_writer_nm,
		AD.DETE_RES_WRITER AS dete_res_writer, AD.DETE_RES_WRITER_NM AS dete_res_writer_nm,
		AD.DETE_RES_WRITER_DATE AS dete_res_writer_date,
		AD.REQ_STATE_CD AS dete_req_state_cd, AD.REQ_STATE_NM AS dete_req_state_nm,
		AD.RES_STATE_CD AS dete_res_state_cd, AD.RES_STATE_NM AS dete_res_state_nm
	FROM (
			SELECT 
				PD.CONS_CODE, PD.DETE_REQ_SYS_DOC_NUM, PD.DETE_REQ_DOC_NUM, 
				PD.DETE_REQ_DOC_CODE, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = PD.DETE_REQ_DOC_CODE) AS DETE_REQ_DOC_NAME,
				PD.CO_CODE, (SELECT CO_NAME FROM CO_INFO_MANAGE WHERE CO_CODE = PD.CO_CODE) AS CO_NAME,
				PD.CONSTR_TYPE_CD, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = PD.CONSTR_TYPE_CD) AS CONSTR_TYPE_NAME,
				PD.DETAIL_CONSTR_TYPE_CD, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = PD.DETAIL_CONSTR_TYPE_CD) AS DETAIL_CONSTR_TYPE_NAME,
				PD.DETE_REQ_DATE, PD.LOCATION, PD.DETE_AREA, PD.DETE_REQ_WRITER_DATE,
				PD.DETE_RES_SYS_DOC_NUM, PD.DETE_RES_DOC_NUM,
				PD.DETE_RES_DOC_CODE, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = PD.DETE_RES_DOC_CODE) AS DETE_RES_DOC_NAME,
				PD.DETE_DATE, PD.DETE_RESULT, PD.INSTRUCTION,
				PD.CONT_1ST_ID, (SELECT USER_NAME FROM USER WHERE ID = PD.CONT_1ST_ID) AS CONT_1ST_NAME,
				PD.CONT_2ST_ID, (SELECT USER_NAME FROM USER WHERE ID = PD.CONT_2ST_ID) AS CONT_2ST_NAME,
				PD.SUPE_1ST_ID, (SELECT USER_NAME FROM USER WHERE ID = PD.SUPE_1ST_ID) AS SUPE_1ST_NAME,
				PD.SUPE_2ST_ID, (SELECT USER_NAME FROM USER WHERE ID = PD.SUPE_1ST_ID) AS SUPE_2ST_NAME,
				DM1.STATE_CODE AS REQ_STATE_CD,(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = DM1.STATE_CODE) AS REQ_STATE_NM,
				DM1.WRITER AS DETE_REQ_WRITER, (SELECT USER_NAME FROM USER WHERE ID = DM1.WRITER) AS DETE_REQ_WRITER_NM,
				DM2.STATE_CODE AS RES_STATE_CD,(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = DM2.STATE_CODE) AS RES_STATE_NM,
				DM2.WRITER AS DETE_RES_WRITER, (SELECT USER_NAME FROM USER WHERE ID = DM2.WRITER) AS DETE_RES_WRITER_NM,
				DM2.PR_DATE AS DETE_RES_WRITER_DATE
			FROM 
				PROJECT_DETECTION PD LEFT OUTER JOIN DOC_MANAGE DM1 ON PD.DETE_REQ_SYS_DOC_NUM = DM1.SYS_DOC_NUM 
									 LEFT OUTER JOIN DOC_MANAGE DM2 ON PD.DETE_RES_SYS_DOC_NUM = DM2.SYS_DOC_NUM
			WHERE 1=1
			{1}	
			{2}
			{3}
			{4}
			{5}
			{6}			
			{7}			
			{8}			
			{9}			
			{10}			
			{11}		
			{13}		
			{14}		
			{15}		
			{16}		
			{17}			
		) AD
	WHERE 1=1
	{12}		
	{23}		
	{18}
	{19}
	{20}
	{24}
	{25}
	{26}
	{27}
	{21}
	{22}
"""

SELECT_DETELIST_CONDITION_1 = 'AND PD.CONS_CODE = "{cons_code}"'
# SELECT_DETELIST_CONDITION_2 = 'AND (PD.CONT_1ST_ID IN (SELECT SYS_DOC_NUM FROM APPROVAL_INFORMATION WHERE DOC_CODE = "CD000000" AND ID = "{loginUserId}") OR PD.CONT_2ST_ID IN (SELECT SYS_DOC_NUM FROM APPROVAL_INFORMATION WHERE DOC_CODE = "CD000000" AND ID = "{loginUserId}"))'
# SELECT_DETELIST_CONDITION_2_1 = 'AND (PD.DETE_REQ_SYS_DOC_NUM IN (SELECT SYS_DOC_NUM FROM APPROVAL_INFORMATION WHERE WHERE 1=1 AND (DOC_CODE = "CD000000" OR DOC_CODE = "SD000005") AND ID = "{loginUserId}" OR PD.DETE_RES_SYS_DOC_NUM IN (SELECT SYS_DOC_NUM FROM APPROVAL_INFORMATION WHERE DOC_CODE = "CD000000" AND ID = "{loginUserId}")) '
SELECT_DETELIST_CONDITION_2_1 = 'AND PD.DETE_REQ_SYS_DOC_NUM IN (SELECT SYS_DOC_NUM FROM APPROVAL_INFORMATION WHERE 1=1 AND (DOC_CODE = "CD000000" OR DOC_CODE = "SD000005") AND ID = "{loginUserId}") '
SELECT_DETELIST_CONDITION_2_2 = 'AND PD.DETE_REQ_SYS_DOC_NUM IN (SELECT DISTINCT SYS_DOC_NUM FROM APPROVAL_INFORMATION WHERE 1=1 AND CONS_CODE = "{cons_code}" AND (DOC_CODE = "CD000000" OR DOC_CODE = "SD000005") AND ID IN (SELECT ID FROM USER WHERE CO_CODE IN (SELECT CO_CODE FROM USER WHERE ID = "{loginUserId}")) AND (APPROVAL = "Y" OR CUR_APPROVAL = "Y")) '
SELECT_DETELIST_CONDITION_2_3 = 'AND PD.DETE_REQ_SYS_DOC_NUM IN (SELECT DISTINCT SYS_DOC_NUM FROM APPROVAL_INFORMATION WHERE 1=1 AND CONS_CODE = "{cons_code}" AND (DOC_CODE = "CD000000" OR DOC_CODE = "SD000005" OR DOC_CODE = "SD000007") AND CO_CODE = "{coCode}")'
SELECT_DETELIST_CONDITION_3 = 'AND PD.DETE_REQ_DOC_NUM LIKE "%{dete_req_doc_num}%"'
SELECT_DETELIST_CONDITION_4 = 'AND PD.CONSTR_TYPE_CD = "{constr_type_cd}"'
SELECT_DETELIST_CONDITION_5 = 'AND PD.DETAIL_CONSTR_TYPE_CD = "{detail_constr_type_cd}"'
SELECT_DETELIST_CONDITION_6 = 'AND PD.LOCATION LIKE "%{location}%"'
SELECT_DETELIST_CONDITION_7 = 'AND PD.DETE_REQ_DATE >= "{start_dete_req_date}"'
SELECT_DETELIST_CONDITION_8 = 'AND PD.DETE_REQ_DATE <= "{end_dete_req_date}"'
SELECT_DETELIST_CONDITION_9 = 'AND PD.DETE_AREA = "{dete_area}"'
SELECT_DETELIST_CONDITION_10 = (
    'AND PD.DETE_REQ_WRITER_DATE >= "{start_dete_req_write_date}"'
)
SELECT_DETELIST_CONDITION_11 = (
    'AND PD.DETE_REQ_WRITER_DATE <= "{end_dete_req_write_date}"'
)
SELECT_DETELIST_CONDITION_12 = 'AND AD.DETE_REQ_WRITER_NM LIKE "%{dete_req_writer}%"'
SELECT_DETELIST_CONDITION_23 = 'AND AD.DETE_RES_WRITER_NM LIKE "%{dete_res_writer}%"'
SELECT_DETELIST_CONDITION_13 = 'AND PD.DETE_RES_DOC_NUM LIKE "%{dete_res_doc_num}%"'
SELECT_DETELIST_CONDITION_14 = 'AND PD.DETE_DATE >= "{start_dete_date}"'
SELECT_DETELIST_CONDITION_15 = 'AND PD.DETE_DATE <= "{end_dete_date}"'
SELECT_DETELIST_CONDITION_16 = 'AND PD.DETE_RESULT LIKE "%{dete_result}%"'
SELECT_DETELIST_CONDITION_17 = 'AND PD.INSTRUCTION LIKE "%{instruction}%"'
SELECT_DETELIST_CONDITION_18 = 'AND AD.CO_NAME LIKE "%{co_name}%"'
SELECT_DETELIST_CONDITION_19 = 'AND (AD.CONT_1ST_NAME LIKE "%{cont_tester}%" OR AD.CONT_2ST_NAME LIKE "%{cont_tester}%")'
SELECT_DETELIST_CONDITION_20 = 'AND (AD.SUPE_1ST_NAME LIKE "%{supe_tester}%" OR AD.SUPE_2ST_NAME LIKE "%{supe_tester}%")'
SELECT_DETELIST_CONDITION_21 = "ORDER BY AD.{sort_column} {sort_type}"
SELECT_DETELIST_CONDITION_22 = "LIMIT {start_num}, {end_num}"
SELECT_DETELIST_CONDITION_24 = (
    'AND AD.DETE_RES_WRITER_DATE >= "{start_dete_res_write_date}"'
)
SELECT_DETELIST_CONDITION_25 = (
    'AND AD.DETE_RES_WRITER_DATE <= "{end_dete_res_write_date}"'
)
SELECT_DETELIST_CONDITION_26 = 'AND AD.REQ_STATE_CD = "{req_state_cd}"'
SELECT_DETELIST_CONDITION_27 = 'AND AD.RES_STATE_CD = "{res_state_cd}"'


class sqlProjectDetectionManage:

    # 검측 정보를 저장 한다.
    def iPutDetectionInfo(self, params, docDefaultInfo, coCode, writerDate):

        query = INSERT_DETECTION_INFO

        query += "VALUES("
        query += '"' + params["reqDocInfo"]["cons_code"] + '", '
        query += "" + str(docDefaultInfo["sysDocNum"]) + ", "
        query += '"' + docDefaultInfo["documentNumber"] + '", '
        query += '"' + params["reqDocInfo"]["doc_code"] + '", '
        query += '"' + coCode + '", '
        query += '"' + params["reqDocContent"]["constr_type_cd"] + '", '
        query += '"' + params["reqDocContent"]["detail_constr_type_cd"] + '", '
        query += '"' + params["reqDocContent"]["location"] + '", '
        query += '"' + params["reqDocContent"]["dete_req_date"] + '", '
        query += '"' + params["reqDocContent"]["dete_area"] + '", '
        query += '"' + writerDate + '", '
        query += '"' + params["reqDocContent"]["cont_1st_id"] + '", '
        query += '"' + params["reqDocContent"]["cont_2st_id"] + '" '
        query += ")"

        return query

    # 검측 체크리스트 정보를 저장 한다.
    def iPutDeteChkList(self, consCode, sysDocNum, chkInfo):

        query = INSERT_DETECHKRESULT_INFO

        query += "VALUES("
        query += '"' + consCode + '", '
        query += "" + str(sysDocNum) + ", "
        query += '"' + chkInfo["chk_msg"] + '", '
        query += '"' + chkInfo["insp_crid_cd"] + '", '
        query += '"' + chkInfo["cont_1st_result"] + '", '
        query += '"' + chkInfo["cont_2st_result"] + '" '
        query += ")"

        return query

    # 검측 체크리스트 정보를 삭제 한다.
    def dDelDeteChkList(self, consCode, sysDocNum):

        query = DELETE_DETECHKRESULT_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += "AND DETE_REQ_SYS_DOC_NUM = " + str(sysDocNum) + " "

        return query

    # 검측 통보 정보 저장
    def uModifyDetectionInfo(self, params, docDefaultInfo):
        query = UPDATE_DETECTION_INFO

        query += "DETE_RES_SYS_DOC_NUM = " + str(docDefaultInfo["sysDocNum"]) + ", "
        query += 'DETE_RES_DOC_NUM = "' + docDefaultInfo["documentNumber"] + '", '
        query += 'DETE_RES_DOC_CODE = "' + params["reqDocInfo"]["doc_code"] + '", '
        query += 'DETE_DATE = "' + params["reqDocContent"]["dete_date"] + '", '
        query += 'DETE_RESULT = "' + params["reqDocContent"]["dete_result"] + '", '
        query += 'INSTRUCTION = "' + params["reqDocContent"]["instruction"] + '", '
        query += 'SUPE_1ST_ID = "' + params["reqDocContent"]["supe_1st_id"] + '", '
        query += 'SUPE_2ST_ID = "' + params["reqDocContent"]["supe_2st_id"] + '" '

        query += "WHERE 1=1 "
        query += 'AND CONS_CODE = "' + params["reqDocInfo"]["cons_code"] + '" '
        query += "AND DETE_REQ_SYS_DOC_NUM = " + str(
            params["reqDocContent"]["dete_req_sys_doc_num"]
        )

        return query

    # 검측 체크리스트 정보를 업데이트 한다.
    def uModifyDeteChkList(self, consCode, deteReqSysDocNum, chkInfo):
        query = UPDATE_DETECHKRESULT_INFO

        query += 'SUPE_1ST_RESULT = "' + chkInfo["supe_1st_result"] + '", '
        query += 'SUPE_2ST_RESULT = "' + chkInfo["supe_2st_result"] + '", '
        query += 'DETE_ACTION = "' + chkInfo["dete_action"] + '" '

        query += "WHERE 1=1 "
        query += 'AND CONS_CODE = "' + consCode + '" '
        query += "AND DETE_REQ_SYS_DOC_NUM = " + str(deteReqSysDocNum) + " "
        query += 'AND CHK_MSG = "' + chkInfo["chk_msg"] + '" '

        return query

    # 검측 리스트를 조회 한다.
    def sSearchDetectionInfoList(self, userInfo, userAuth, jobAuth, searchData):
        query = SELECT_DETECTIONLIST_INFO

        query = query.replace(
            "{1}",
            SELECT_DETELIST_CONDITION_1.replace(
                "{cons_code}", searchData["search_cons_code"]
            ),
        )

        if jobAuth == None:
            if (
                userAuth == constants.USER_AUTH_CONTRACTOR
                or userAuth == constants.USER_AUTH_CONTRACTOR_MONITOR
                or userAuth == constants.USER_AUTH_SUPERVISOR
                or userAuth == constants.USER_AUTH_SUPERVISOR_MONITOR
            ):
                qryTmp = SELECT_DETELIST_CONDITION_2_3.replace(
                    "{coCode}", userInfo["co_code"]
                )
                qryTmp = qryTmp.replace("{cons_code}", searchData["search_cons_code"])

                query = query.replace("{2}", qryTmp)
            elif (
                userAuth == constants.USER_AUTH_DESIGNER
                or userAuth == constants.USER_AUTH_CONTRACTION
                or userAuth == constants.USER_AUTH_SUPERVISING
                or userAuth == constants.USER_AUTH_INOCCUPATION
            ):
                query = query.replace(
                    "{2}",
                    SELECT_DETELIST_CONDITION_2_1.replace(
                        "{loginUserId}", userInfo["id"]
                    ),
                )
            else:
                query = query.replace("{2}", "")
        elif (jobAuth["job_title_code"] == constants.JOB_TITLE_CD_BUYER) or (
            jobAuth["job_title_code"] == constants.JOB_TITLE_CD_WHITEHALL
        ):
            query = query.replace("{2}", "")
        else:
            query = query.replace(
                "{2}",
                SELECT_DETELIST_CONDITION_2_1.replace("{loginUserId}", userInfo["id"]),
            )

        if searchData["search_dete_req_doc_num"] != "":
            query = query.replace(
                "{3}",
                SELECT_DETELIST_CONDITION_3.replace(
                    "{dete_req_doc_num}", searchData["search_dete_req_doc_num"]
                ),
            )
        else:
            query = query.replace("{3}", "")

        if searchData["search_constr_type_code"] != "":
            query = query.replace(
                "{4}",
                SELECT_DETELIST_CONDITION_4.replace(
                    "{constr_type_cd}", searchData["search_constr_type_code"]
                ),
            )
        else:
            query = query.replace("{4}", "")

        if searchData["search_detail_constr_type_code"] != "":
            query = query.replace(
                "{5}",
                SELECT_DETELIST_CONDITION_5.replace(
                    "{detail_constr_type_cd}",
                    searchData["search_detail_constr_type_code"],
                ),
            )
        else:
            query = query.replace("{5}", "")

        if searchData["search_location"] != "":
            query = query.replace(
                "{6}",
                SELECT_DETELIST_CONDITION_6.replace(
                    "{location}", searchData["search_location"]
                ),
            )
        else:
            query = query.replace("{6}", "")

        if searchData["search_start_dete_req_date"] != "":
            query = query.replace(
                "{7}",
                SELECT_DETELIST_CONDITION_7.replace(
                    "{start_dete_req_date}", searchData["search_start_dete_req_date"]
                ),
            )
        else:
            query = query.replace("{7}", "")

        if searchData["search_end_dete_req_date"] != "":
            query = query.replace(
                "{8}",
                SELECT_DETELIST_CONDITION_8.replace(
                    "{end_dete_req_date}", searchData["search_end_dete_req_date"]
                ),
            )
        else:
            query = query.replace("{8}", "")

        if searchData["search_dete_area"] != "":
            query = query.replace(
                "{9}",
                SELECT_DETELIST_CONDITION_9.replace(
                    "{dete_area}", searchData["search_dete_area"]
                ),
            )
        else:
            query = query.replace("{9}", "")

        if searchData["search_start_dete_req_write_date"] != "":
            query = query.replace(
                "{10}",
                SELECT_DETELIST_CONDITION_10.replace(
                    "{start_dete_req_write_date}",
                    searchData["search_start_dete_req_write_date"],
                ),
            )
        else:
            query = query.replace("{10}", "")

        if searchData["search_end_dete_req_write_date"] != "":
            query = query.replace(
                "{11}",
                SELECT_DETELIST_CONDITION_11.replace(
                    "{end_dete_req_write_date}",
                    searchData["search_end_dete_req_write_date"],
                ),
            )
        else:
            query = query.replace("{11}", "")

        if searchData["search_dete_req_writer"] != "":
            query = query.replace(
                "{12}",
                SELECT_DETELIST_CONDITION_12.replace(
                    "{dete_req_writer}", searchData["search_dete_req_writer"]
                ),
            )
        else:
            query = query.replace("{12}", "")

        if searchData["search_dete_res_doc_num"] != "":
            query = query.replace(
                "{13}",
                SELECT_DETELIST_CONDITION_13.replace(
                    "{dete_res_doc_num}", searchData["search_dete_res_doc_num"]
                ),
            )
        else:
            query = query.replace("{13}", "")

        if searchData["search_start_dete_date"] != "":
            query = query.replace(
                "{14}",
                SELECT_DETELIST_CONDITION_14.replace(
                    "{start_dete_date}", searchData["search_start_dete_date"]
                ),
            )
        else:
            query = query.replace("{14}", "")

        if searchData["search_end_dete_date"] != "":
            query = query.replace(
                "{15}",
                SELECT_DETELIST_CONDITION_15.replace(
                    "{end_dete_date}", searchData["search_end_dete_date"]
                ),
            )
        else:
            query = query.replace("{15}", "")

        if searchData["search_dete_result"] != "":
            query = query.replace(
                "{16}",
                SELECT_DETELIST_CONDITION_16.replace(
                    "{dete_result}", searchData["search_dete_result"]
                ),
            )
        else:
            query = query.replace("{16}", "")

        if searchData["search_instruction"] != "":
            query = query.replace(
                "{17}",
                SELECT_DETELIST_CONDITION_17.replace(
                    "{instruction}", searchData["search_instruction"]
                ),
            )
        else:
            query = query.replace("{17}", "")

        if searchData["search_co_name"] != "":
            query = query.replace(
                "{18}",
                SELECT_DETELIST_CONDITION_18.replace(
                    "{co_name}", searchData["search_co_name"]
                ),
            )
        else:
            query = query.replace("{18}", "")

        if searchData["search_cont_tester"] != "":
            query = query.replace(
                "{19}",
                SELECT_DETELIST_CONDITION_19.replace(
                    "{cont_tester}", searchData["search_cont_tester"]
                ),
            )
        else:
            query = query.replace("{19}", "")

        if searchData["search_supe_tester"] != "":
            query = query.replace(
                "{20}",
                SELECT_DETELIST_CONDITION_20.replace(
                    "{supe_tester}", searchData["search_supe_tester"]
                ),
            )
        else:
            query = query.replace("{20}", "")

        if searchData["search_dete_res_writer"] != "":
            query = query.replace(
                "{23}",
                SELECT_DETELIST_CONDITION_23.replace(
                    "{dete_res_writer}", searchData["search_dete_res_writer"]
                ),
            )
        else:
            query = query.replace("{23}", "")

        if searchData["search_start_dete_res_write_date"] != "":
            query = query.replace(
                "{24}",
                SELECT_DETELIST_CONDITION_24.replace(
                    "{start_dete_res_write_date}",
                    searchData["search_start_dete_res_write_date"],
                ),
            )
        else:
            query = query.replace("{24}", "")

        if searchData["search_end_dete_res_write_date"] != "":
            query = query.replace(
                "{25}",
                SELECT_DETELIST_CONDITION_25.replace(
                    "{end_dete_res_write_date}",
                    searchData["search_end_dete_res_write_date"],
                ),
            )
        else:
            query = query.replace("{25}", "")

        if searchData["search_req_state_cd"] != "":
            query = query.replace(
                "{26}",
                SELECT_DETELIST_CONDITION_26.replace(
                    "{req_state_cd}", searchData["search_req_state_cd"]
                ),
            )
        else:
            query = query.replace("{26}", "")

        if searchData["search_res_state_cd"] != "":
            query = query.replace(
                "{27}",
                SELECT_DETELIST_CONDITION_27.replace(
                    "{res_state_cd}", searchData["search_res_state_cd"]
                ),
            )
        else:
            query = query.replace("{27}", "")

        queryTmp = SELECT_DETELIST_CONDITION_21.replace(
            "{sort_column}", searchData["sort_column"]
        )
        queryTmp = queryTmp.replace("{sort_type}", searchData["sort_type"])
        query = query.replace("{21}", queryTmp)

        queryTmp = SELECT_DETELIST_CONDITION_22.replace(
            "{start_num}", searchData["start_num"]
        )
        queryTmp = queryTmp.replace("{end_num}", searchData["end_num"])
        query = query.replace("{22}", queryTmp)

        return query

    # 검측 리스트 개수를 조회 한다.
    def sSearchDetectionInfoListCnt(self, userInfo, userAuth, jobAuth, searchData):

        query = "SELECT COUNT(*) AS cnt FROM ("

        query += SELECT_DETECTIONLIST_INFO

        query = query.replace(
            "{1}",
            SELECT_DETELIST_CONDITION_1.replace(
                "{cons_code}", searchData["search_cons_code"]
            ),
        )

        if jobAuth == None:
            if (
                userAuth == constants.USER_AUTH_CONTRACTOR
                or userAuth == constants.USER_AUTH_CONTRACTOR_MONITOR
                or userAuth == constants.USER_AUTH_SUPERVISOR
                or userAuth == constants.USER_AUTH_SUPERVISOR_MONITOR
            ):
                qryTmp = SELECT_DETELIST_CONDITION_2_3.replace(
                    "{coCode}", userInfo["co_code"]
                )
                qryTmp = qryTmp.replace("{cons_code}", searchData["search_cons_code"])

                query = query.replace("{2}", qryTmp)
            elif (
                userAuth == constants.USER_AUTH_DESIGNER
                or userAuth == constants.USER_AUTH_CONTRACTION
                or userAuth == constants.USER_AUTH_SUPERVISING
                or userAuth == constants.USER_AUTH_INOCCUPATION
            ):
                query = query.replace(
                    "{2}",
                    SELECT_DETELIST_CONDITION_2_1.replace(
                        "{loginUserId}", userInfo["id"]
                    ),
                )
            else:
                query = query.replace("{2}", "")
        elif (jobAuth["job_title_code"] == constants.JOB_TITLE_CD_BUYER) or (
            jobAuth["job_title_code"] == constants.JOB_TITLE_CD_WHITEHALL
        ):
            query = query.replace("{2}", "")
        else:
            query = query.replace(
                "{2}",
                SELECT_DETELIST_CONDITION_2_1.replace("{loginUserId}", userInfo["id"]),
            )

        if searchData["search_dete_req_doc_num"] != "":
            query = query.replace(
                "{3}",
                SELECT_DETELIST_CONDITION_3.replace(
                    "{dete_req_doc_num}", searchData["search_dete_req_doc_num"]
                ),
            )
        else:
            query = query.replace("{3}", "")

        if searchData["search_constr_type_code"] != "":
            query = query.replace(
                "{4}",
                SELECT_DETELIST_CONDITION_4.replace(
                    "{constr_type_cd}", searchData["search_constr_type_code"]
                ),
            )
        else:
            query = query.replace("{4}", "")

        if searchData["search_detail_constr_type_code"] != "":
            query = query.replace(
                "{5}",
                SELECT_DETELIST_CONDITION_5.replace(
                    "{detail_constr_type_cd}",
                    searchData["search_detail_constr_type_code"],
                ),
            )
        else:
            query = query.replace("{5}", "")

        if searchData["search_location"] != "":
            query = query.replace(
                "{6}",
                SELECT_DETELIST_CONDITION_6.replace(
                    "{location}", searchData["search_location"]
                ),
            )
        else:
            query = query.replace("{6}", "")

        if searchData["search_start_dete_req_date"] != "":
            query = query.replace(
                "{7}",
                SELECT_DETELIST_CONDITION_7.replace(
                    "{start_dete_req_date}", searchData["search_start_dete_req_date"]
                ),
            )
        else:
            query = query.replace("{7}", "")

        if searchData["search_end_dete_req_date"] != "":
            query = query.replace(
                "{8}",
                SELECT_DETELIST_CONDITION_8.replace(
                    "{end_dete_req_date}", searchData["search_end_dete_req_date"]
                ),
            )
        else:
            query = query.replace("{8}", "")

        if searchData["search_dete_area"] != "":
            query = query.replace(
                "{9}",
                SELECT_DETELIST_CONDITION_9.replace(
                    "{dete_area}", searchData["search_dete_area"]
                ),
            )
        else:
            query = query.replace("{9}", "")

        if searchData["search_start_dete_req_write_date"] != "":
            query = query.replace(
                "{10}",
                SELECT_DETELIST_CONDITION_10.replace(
                    "{start_dete_req_write_date}",
                    searchData["search_start_dete_req_write_date"],
                ),
            )
        else:
            query = query.replace("{10}", "")

        if searchData["search_end_dete_req_write_date"] != "":
            query = query.replace(
                "{11}",
                SELECT_DETELIST_CONDITION_11.replace(
                    "{end_dete_req_write_date}",
                    searchData["search_end_dete_req_write_date"],
                ),
            )
        else:
            query = query.replace("{11}", "")

        if searchData["search_dete_req_writer"] != "":
            query = query.replace(
                "{12}",
                SELECT_DETELIST_CONDITION_12.replace(
                    "{dete_req_writer}", searchData["search_dete_req_writer"]
                ),
            )
        else:
            query = query.replace("{12}", "")

        if searchData["search_dete_res_doc_num"] != "":
            query = query.replace(
                "{13}",
                SELECT_DETELIST_CONDITION_13.replace(
                    "{dete_res_doc_num}", searchData["search_dete_res_doc_num"]
                ),
            )
        else:
            query = query.replace("{13}", "")

        if searchData["search_start_dete_date"] != "":
            query = query.replace(
                "{14}",
                SELECT_DETELIST_CONDITION_14.replace(
                    "{start_dete_date}", searchData["search_start_dete_date"]
                ),
            )
        else:
            query = query.replace("{14}", "")

        if searchData["search_end_dete_date"] != "":
            query = query.replace(
                "{15}",
                SELECT_DETELIST_CONDITION_15.replace(
                    "{end_dete_date}", searchData["search_end_dete_date"]
                ),
            )
        else:
            query = query.replace("{15}", "")

        if searchData["search_dete_result"] != "":
            query = query.replace(
                "{16}",
                SELECT_DETELIST_CONDITION_16.replace(
                    "{dete_result}", searchData["search_dete_result"]
                ),
            )
        else:
            query = query.replace("{16}", "")

        if searchData["search_instruction"] != "":
            query = query.replace(
                "{17}",
                SELECT_DETELIST_CONDITION_17.replace(
                    "{instruction}", searchData["search_instruction"]
                ),
            )
        else:
            query = query.replace("{17}", "")

        if searchData["search_co_name"] != "":
            query = query.replace(
                "{18}",
                SELECT_DETELIST_CONDITION_18.replace(
                    "{co_name}", searchData["search_co_name"]
                ),
            )
        else:
            query = query.replace("{18}", "")

        if searchData["search_cont_tester"] != "":
            query = query.replace(
                "{19}",
                SELECT_DETELIST_CONDITION_19.replace(
                    "{cont_tester}", searchData["search_cont_tester"]
                ),
            )
        else:
            query = query.replace("{19}", "")

        if searchData["search_supe_tester"] != "":
            query = query.replace(
                "{20}",
                SELECT_DETELIST_CONDITION_20.replace(
                    "{supe_tester}", searchData["search_supe_tester"]
                ),
            )
        else:
            query = query.replace("{20}", "")

        if searchData["search_dete_res_writer"] != "":
            query = query.replace(
                "{23}",
                SELECT_DETELIST_CONDITION_23.replace(
                    "{dete_res_writer}", searchData["search_dete_res_writer"]
                ),
            )
        else:
            query = query.replace("{23}", "")

        if searchData["search_start_dete_res_write_date"] != "":
            query = query.replace(
                "{24}",
                SELECT_DETELIST_CONDITION_24.replace(
                    "{start_dete_res_write_date}",
                    searchData["search_start_dete_res_write_date"],
                ),
            )
        else:
            query = query.replace("{24}", "")

        if searchData["search_end_dete_res_write_date"] != "":
            query = query.replace(
                "{25}",
                SELECT_DETELIST_CONDITION_25.replace(
                    "{end_dete_res_write_date}",
                    searchData["search_end_dete_res_write_date"],
                ),
            )
        else:
            query = query.replace("{25}", "")

        if searchData["search_req_state_cd"] != "":
            query = query.replace(
                "{26}",
                SELECT_DETELIST_CONDITION_26.replace(
                    "{req_state_cd}", searchData["search_req_state_cd"]
                ),
            )
        else:
            query = query.replace("{26}", "")

        if searchData["search_res_state_cd"] != "":
            query = query.replace(
                "{27}",
                SELECT_DETELIST_CONDITION_27.replace(
                    "{res_state_cd}", searchData["search_res_state_cd"]
                ),
            )
        else:
            query = query.replace("{27}", "")

        query = query.replace("{21}", "")
        query = query.replace("{22}", "")

        query += ") H"
        return query
