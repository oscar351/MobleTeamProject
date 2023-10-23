# _*_coding: utf-8 -*-

from common.commUtilService import commUtilService

from common import constants


INSERT_INSPMATER_INFO = """INSERT INTO MATERIAL_INSPECTION(CONS_CODE, MIR_DOCNUM, CO_CODE, MATERIAL_NUM, STANDARD, UNIT, AMOUNT_CARRYIN, MANUFACT_INDUSTRY, SYS_DOC_NUM, MATERIAL_INDEX) """


UPDATE_MATERIALINSPECTION_INFO = """UPDATE MATERIAL_INSPECTION SET """


# MPAQ.MATERIAL_NUM AS material_num, MPAQ.MATERIAL_NAME AS material_name,
# MPAQ.STANDARD AS standard, MPAQ.UNIT AS unit, MPAQ.AMOUNT_CARRYIN AS amount_carryin, MPAQ.MANUFACT_INDUSTRY AS manufact_industry, MPAQ.IC_DATE AS ic_date, MPAQ.IC_RESULT AS ic_result
# MP.MATERIAL_NUM, (SELECT MATERIAL_NAME FROM MATERIAL_MANAGE WHERE MATERIAL_NUM = MP.MATERIAL_NUM) AS MATERIAL_NAME,
# MP.STANDARD, MP.UNIT, MP.AMOUNT_CARRYIN, MP.MANUFACT_INDUSTRY, MP.IC_DATE, MP.IC_RESULT,
SELECT_MATERIALINSPECTION_INFO = """
    SELECT
			MPAQ.CONS_CODE AS cons_code, MPAQ.CONS_NAME AS cons_name,
			MPAQ.REQ_SYS_DOC_NUM AS req_sys_doc_num, MPAQ.REQ_DOC_NUM AS req_doc_num, MPAQ.REQ_WRITER AS req_writer,MPAQ.REQ_WRITER_NAME AS req_writer_name,
			MPAQ.REQ_PR_DATE AS req_pr_date, MPAQ.REQ_STATE_CODE AS req_state_code, MPAQ.REQ_STATE_NAME AS req_state_name, MPAQ.REQ_PC_DATE AS req_pc_date,
			MPAQ.RES_SYS_DOC_NUM AS res_sys_doc_num, MPAQ.RES_DOC_NUM AS res_doc_num, MPAQ.RES_WRITER AS res_writer, MPAQ.RES_WRITER_NAME AS res_writer_name,
			MPAQ.RES_PR_DATE AS res_pr_date, MPAQ.RES_STATE_CODE AS res_state_code, MPAQ.RES_STATE_NAME AS res_state_name, MPAQ.RES_PC_DATE AS res_pc_date,
			MPAQ.IC_DATE AS ic_date, MPAQ.IC_RESULT AS ic_result
			FROM
				(SELECT DISTINCT
					MP.CONS_CODE, (SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = MP.CONS_CODE) AS CONS_NAME,
					MP.SYS_DOC_NUM AS REQ_SYS_DOC_NUM,  MP.MIR_DOCNUM AS REQ_DOC_NUM,
					MP.IC_DATE, MP.IC_RESULT,
					SUB1.REQ_WRITER, SUB1.REQ_WRITER_NAME, SUB1.REQ_PR_DATE,
					SUB1.REQ_STATE_CODE, SUB1.REQ_STATE_NAME, SUB1.REQ_PC_DATE,
					MP.MIN_DOCNUM AS RES_SYS_DOC_NUM, SUB2.RES_DOC_NUM,
					SUB2.RES_WRITER, SUB2.RES_WRITER_NAME, SUB2.RES_PR_DATE,
					SUB2.RES_STATE_CODE, SUB2.RES_STATE_NAME, SUB2.RES_PC_DATE
					FROM MATERIAL_INSPECTION MP LEFT OUTER JOIN (SELECT
																	DM.CONS_CODE, DM.SYS_DOC_NUM AS REQ_SYS_DOC_NUM, DM.STATE_CODE AS REQ_STATE_CODE,
																	(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = DM.STATE_CODE) AS REQ_STATE_NAME,
																	DM.PR_DATE AS REQ_PR_DATE, DM.PC_DATE AS REQ_PC_DATE, DM.WRITER AS REQ_WRITER,
																	(SELECT USER_NAME FROM USER WHERE ID = DM.WRITER) AS REQ_WRITER_NAME
																FROM DOC_MANAGE DM
																WHERE 1=1
																{1}
																AND DM.DOC_CODE = 'CD000012'
																) SUB1 ON MP.CONS_CODE = SUB1.CONS_CODE AND MP.SYS_DOC_NUM = SUB1.REQ_SYS_DOC_NUM
												LEFT OUTER JOIN (SELECT
																	DM.CONS_CODE, DM.SYS_DOC_NUM AS RES_SYS_DOC_NUM, DM.DOC_NUM AS RES_DOC_NUM, DM.STATE_CODE AS RES_STATE_CODE,
																	(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = DM.STATE_CODE) AS RES_STATE_NAME,
																	DM.PR_DATE AS RES_PR_DATE, DM.PC_DATE AS RES_PC_DATE, DM.WRITER AS RES_WRITER,
																	(SELECT USER_NAME FROM USER WHERE ID = DM.WRITER) AS RES_WRITER_NAME,
																	DLI.TO_SYS_DOC_NUM
																FROM DOC_MANAGE DM LEFT OUTER JOIN DOCUMENT_LINK_INFO DLI ON DM.SYS_DOC_NUM = DLI.SYS_DOC_NUM
																WHERE 1=1
																{1}
																AND DM.DOC_CODE = 'SD000020'
																) SUB2 ON MP.CONS_CODE = SUB2.CONS_CODE AND MP.SYS_DOC_NUM = SUB2.TO_SYS_DOC_NUM
				WHERE 1=1
				{21}
				) MPAQ
	WHERE 1=1
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
	{12}
	{13}
	{14}
	{15}
	{16}
	{20}
	{17}
	{18}
	{19}
"""

SELECT_MATERSELLIST_CONDITION_1 = 'AND DM.CONS_CODE = "{cons_code}"'
SELECT_MATERSELLIST_CONDITION_2_1 = 'AND MPAQ.REQ_SYS_DOC_NUM IN (SELECT SYS_DOC_NUM FROM APPROVAL_INFORMATION WHERE 1=1 AND (DOC_CODE = "CD000012" OR DOC_CODE = "SD000020") AND ID = "{loginUserId}")'
SELECT_MATERSELLIST_CONDITION_2_2 = 'AND MPAQ.REQ_SYS_DOC_NUM IN (SELECT DISTINCT SYS_DOC_NUM FROM APPROVAL_INFORMATION    WHERE 1=1 AND CONS_CODE = "{cons_code}" AND (DOC_CODE = "CD000012" OR DOC_CODE = "SD000020") AND ID IN (SELECT ID FROM USER WHERE CO_CODE IN (SELECT CO_CODE FROM USER WHERE ID = "{loginUserId}")) AND (APPROVAL = "Y" OR CUR_APPROVAL = "Y"))'
SELECT_MATERSELLIST_CONDITION_2_3 = 'AND MPAQ.REQ_SYS_DOC_NUM IN (SELECT DISTINCT SYS_DOC_NUM FROM APPROVAL_INFORMATION    WHERE 1=1 AND CONS_CODE = "{cons_code}" AND (DOC_CODE = "CD000012" OR DOC_CODE = "SD000020" OR DOC_CODE = "SD000007") AND CO_CODE = "{coCode}")'
SELECT_MATERSELLIST_CONDITION_3 = 'AND MPAQ.MATERIAL_NAME LIKE "%{material_name}%"'
SELECT_MATERSELLIST_CONDITION_4 = 'AND MPAQ.REQ_WRITER_NAME LIKE "%{req_writer}%"'
SELECT_MATERSELLIST_CONDITION_5 = 'AND MPAQ.REQ_PR_DATE >= "{req_pr_start_date}"'
SELECT_MATERSELLIST_CONDITION_6 = 'AND MPAQ.REQ_PR_DATE <= "{req_pr_end_date}"'
SELECT_MATERSELLIST_CONDITION_7 = 'AND MPAQ.REQ_PC_DATE >= "{req_pc_start_date}"'
SELECT_MATERSELLIST_CONDITION_8 = 'AND MPAQ.REQ_PC_DATE <= "{req_pc_end_date}"'
SELECT_MATERSELLIST_CONDITION_9 = 'AND MPAQ.REQ_STATE_CODE = "{req_state_cd}"'
SELECT_MATERSELLIST_CONDITION_10 = 'AND MPAQ.RES_WRITER_NAME LIKE "%{res_writer}%"'
SELECT_MATERSELLIST_CONDITION_11 = 'AND MPAQ.RES_PR_DATE >= "{res_pr_start_date}"'
SELECT_MATERSELLIST_CONDITION_12 = 'AND MPAQ.RES_PR_DATE <= "{res_pr_end_date}"'
SELECT_MATERSELLIST_CONDITION_13 = 'AND MPAQ.RES_PC_DATE >= "{res_pc_start_date}"'
SELECT_MATERSELLIST_CONDITION_14 = 'AND MPAQ.RES_PC_DATE <= "{res_pc_end_date}"'
SELECT_MATERSELLIST_CONDITION_15 = 'AND MPAQ.RES_STATE_CODE = "{res_state_cd}"'
SELECT_MATERSELLIST_CONDITION_16 = 'AND MPAQ.IC_DATE >= "{ic_start_date}"'
SELECT_MATERSELLIST_CONDITION_20 = 'AND MPAQ.IC_DATE <= "{ic_end_date}"'
SELECT_MATERSELLIST_CONDITION_17 = 'AND MPAQ.IC_RESULT LIKE "%{ic_result}%"'
SELECT_MATERSELLIST_CONDITION_18 = "ORDER BY MPAQ.{sort_column} {sort_type}"
SELECT_MATERSELLIST_CONDITION_19 = "LIMIT {start_num}, {end_num} "
SELECT_MATERSELLIST_CONDITION_21 = 'AND MP.CONS_CODE = "{cons_code}" '


class sqlProjectInspMaterManage:

    # 승인 자재 리스트를 조회 한다
    def iPutInspMaterInfo(self, consCode, material, docDefaultInfo, coCode, index):

        query = INSERT_INSPMATER_INFO

        query += "VALUES("
        query += '"' + consCode + '", '
        query += '"' + docDefaultInfo["documentNumber"] + '", '
        query += '"' + coCode + '", '
        query += '"' + material["material_num"] + '", '
        query += '"' + material["standard"] + '", '
        query += '"' + material["unit"] + '", '
        query += '"' + material["amount_carryin"] + '", '
        query += '"' + material["manufact_industry"] + '", '
        query += "" + str(docDefaultInfo["sysDocNum"]) + ", "
        query += "" + str(index) + ") "

        return query

    # 자재 검수 통보 정보 저장
    def uModifyInspMaterInfo(
        self, consCode, reqSysDocNum, inspResult, inspDate, sysDocNum
    ):
        query = UPDATE_MATERIALINSPECTION_INFO

        query += "MIN_DOCNUM = " + str(sysDocNum) + ", "
        query += 'IC_DATE = "' + inspDate + '", '
        query += 'IC_RESULT = "' + inspResult + '" '

        query += "WHERE 1=1 "
        query += 'AND CONS_CODE = "' + consCode + '" '
        query += "AND SYS_DOC_NUM = " + str(reqSysDocNum)

        return query

    # 검수 자재  리스트를 조회 한다.
    def sSearchInspMaterList(self, userInfo, userAuth, jobAuth, searchData):
        query = SELECT_MATERIALINSPECTION_INFO

        query = query.replace(
            "{1}",
            SELECT_MATERSELLIST_CONDITION_1.replace(
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
                qryTmp = SELECT_MATERSELLIST_CONDITION_2_3.replace(
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
                    SELECT_MATERSELLIST_CONDITION_2_1.replace(
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
                SELECT_MATERSELLIST_CONDITION_2_1.replace(
                    "{loginUserId}", userInfo["id"]
                ),
            )

        if searchData["search_material_name"] != "":
            query = query.replace(
                "{3}",
                SELECT_MATERSELLIST_CONDITION_3.replace(
                    "{material_name}", searchData["search_material_name"]
                ),
            )
        else:
            query = query.replace("{3}", "")

        if searchData["search_req_writer"] != "":
            query = query.replace(
                "{4}",
                SELECT_MATERSELLIST_CONDITION_4.replace(
                    "{req_writer}", searchData["search_req_writer"]
                ),
            )
        else:
            query = query.replace("{4}", "")

        if searchData["search_req_pr_start_date"] != "":
            query = query.replace(
                "{5}",
                SELECT_MATERSELLIST_CONDITION_5.replace(
                    "{req_pr_start_date}", searchData["search_req_pr_start_date"]
                ),
            )
        else:
            query = query.replace("{5}", "")

        if searchData["search_req_pr_end_date"] != "":
            query = query.replace(
                "{6}",
                SELECT_MATERSELLIST_CONDITION_6.replace(
                    "{req_pr_end_date}", searchData["search_req_pr_end_date"]
                ),
            )
        else:
            query = query.replace("{6}", "")

        if searchData["search_req_pc_start_date"] != "":
            query = query.replace(
                "{7}",
                SELECT_MATERSELLIST_CONDITION_7.replace(
                    "{req_pc_start_date}", searchData["search_req_pc_start_date"]
                ),
            )
        else:
            query = query.replace("{7}", "")

        if searchData["search_req_pc_end_date"] != "":
            query = query.replace(
                "{8}",
                SELECT_MATERSELLIST_CONDITION_8.replace(
                    "{req_pc_end_date}", searchData["search_req_pc_end_date"]
                ),
            )
        else:
            query = query.replace("{8}", "")

        if searchData["search_req_state_cd"] != "":
            query = query.replace(
                "{9}",
                SELECT_MATERSELLIST_CONDITION_9.replace(
                    "{req_state_cd}", searchData["search_req_state_cd"]
                ),
            )
        else:
            query = query.replace("{9}", "")

        if searchData["search_res_writer"] != "":
            query = query.replace(
                "{10}",
                SELECT_MATERSELLIST_CONDITION_10.replace(
                    "{res_writer}", searchData["search_res_writer"]
                ),
            )
        else:
            query = query.replace("{10}", "")

        if searchData["search_res_pr_start_date"] != "":
            query = query.replace(
                "{11}",
                SELECT_MATERSELLIST_CONDITION_11.replace(
                    "{res_pr_start_date}", searchData["search_res_pr_start_date"]
                ),
            )
        else:
            query = query.replace("{11}", "")

        if searchData["search_res_pr_end_date"] != "":
            query = query.replace(
                "{12}",
                SELECT_MATERSELLIST_CONDITION_12.replace(
                    "{res_pr_end_date}", searchData["search_res_pr_end_date"]
                ),
            )
        else:
            query = query.replace("{12}", "")

        if searchData["search_res_pc_start_date"] != "":
            query = query.replace(
                "{13}",
                SELECT_MATERSELLIST_CONDITION_13.replace(
                    "{res_pc_start_date}", searchData["search_res_pc_start_date"]
                ),
            )
        else:
            query = query.replace("{13}", "")

        if searchData["search_res_pc_end_date"] != "":
            query = query.replace(
                "{14}",
                SELECT_MATERSELLIST_CONDITION_14.replace(
                    "{res_pc_end_date}", searchData["search_res_pc_end_date"]
                ),
            )
        else:
            query = query.replace("{14}", "")

        if searchData["search_res_state_cd"] != "":
            query = query.replace(
                "{15}",
                SELECT_MATERSELLIST_CONDITION_15.replace(
                    "{res_state_cd}", searchData["search_res_state_cd"]
                ),
            )
        else:
            query = query.replace("{15}", "")

        if searchData["search_ic_start_date"] != "":
            query = query.replace(
                "{16}",
                SELECT_MATERSELLIST_CONDITION_16.replace(
                    "{ic_start_date}", searchData["search_ic_start_date"]
                ),
            )
        else:
            query = query.replace("{16}", "")

        if searchData["search_ic_end_date"] != "":
            query = query.replace(
                "{20}",
                SELECT_MATERSELLIST_CONDITION_20.replace(
                    "{ic_end_date}", searchData["search_ic_end_date"]
                ),
            )
        else:
            query = query.replace("{20}", "")

        if searchData["search_ic_result"] != "":
            query = query.replace(
                "{17}",
                SELECT_MATERSELLIST_CONDITION_17.replace(
                    "{ic_result}", searchData["search_ic_result"]
                ),
            )
        else:
            query = query.replace("{17}", "")

        query = query.replace(
            "{21}",
            SELECT_MATERSELLIST_CONDITION_21.replace(
                "{cons_code}", searchData["search_cons_code"]
            ),
        )

        queryTmp = SELECT_MATERSELLIST_CONDITION_18.replace(
            "{sort_column}", searchData["sort_column"]
        )
        queryTmp = queryTmp.replace("{sort_type}", searchData["sort_type"])
        query = query.replace("{18}", queryTmp)

        queryTmp = SELECT_MATERSELLIST_CONDITION_19.replace(
            "{start_num}", searchData["start_num"]
        )
        queryTmp = queryTmp.replace("{end_num}", searchData["end_num"])
        query = query.replace("{19}", queryTmp)

        return query

    # 검수 자재  리스트 개수를 조회 한다.
    def sSearchInspMaterListCnt(self, userInfo, userAuth, jobAuth, searchData):

        query = "SELECT COUNT(*) AS cnt FROM ("

        query += SELECT_MATERIALINSPECTION_INFO

        query = query.replace(
            "{1}",
            SELECT_MATERSELLIST_CONDITION_1.replace(
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
                qryTmp = SELECT_MATERSELLIST_CONDITION_2_3.replace(
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
                    SELECT_MATERSELLIST_CONDITION_2_1.replace(
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
                SELECT_MATERSELLIST_CONDITION_2_1.replace(
                    "{loginUserId}", userInfo["id"]
                ),
            )

        if searchData["search_material_name"] != "":
            query = query.replace(
                "{3}",
                SELECT_MATERSELLIST_CONDITION_3.replace(
                    "{material_name}", searchData["search_material_name"]
                ),
            )
        else:
            query = query.replace("{3}", "")

        if searchData["search_req_writer"] != "":
            query = query.replace(
                "{4}",
                SELECT_MATERSELLIST_CONDITION_4.replace(
                    "{req_writer}", searchData["search_req_writer"]
                ),
            )
        else:
            query = query.replace("{4}", "")

        if searchData["search_req_pr_start_date"] != "":
            query = query.replace(
                "{5}",
                SELECT_MATERSELLIST_CONDITION_5.replace(
                    "{req_pr_start_date}", searchData["search_req_pr_start_date"]
                ),
            )
        else:
            query = query.replace("{5}", "")

        if searchData["search_req_pr_end_date"] != "":
            query = query.replace(
                "{6}",
                SELECT_MATERSELLIST_CONDITION_6.replace(
                    "{req_pr_end_date}", searchData["search_req_pr_end_date"]
                ),
            )
        else:
            query = query.replace("{6}", "")

        if searchData["search_req_pc_start_date"] != "":
            query = query.replace(
                "{7}",
                SELECT_MATERSELLIST_CONDITION_7.replace(
                    "{req_pc_start_date}", searchData["search_req_pc_start_date"]
                ),
            )
        else:
            query = query.replace("{7}", "")

        if searchData["search_req_pc_end_date"] != "":
            query = query.replace(
                "{8}",
                SELECT_MATERSELLIST_CONDITION_8.replace(
                    "{req_pc_end_date}", searchData["search_req_pc_end_date"]
                ),
            )
        else:
            query = query.replace("{8}", "")

        if searchData["search_req_state_cd"] != "":
            query = query.replace(
                "{9}",
                SELECT_MATERSELLIST_CONDITION_9.replace(
                    "{req_state_cd}", searchData["search_req_state_cd"]
                ),
            )
        else:
            query = query.replace("{9}", "")

        if searchData["search_res_writer"] != "":
            query = query.replace(
                "{10}",
                SELECT_MATERSELLIST_CONDITION_10.replace(
                    "{res_writer}", searchData["search_res_writer"]
                ),
            )
        else:
            query = query.replace("{10}", "")

        if searchData["search_res_pr_start_date"] != "":
            query = query.replace(
                "{11}",
                SELECT_MATERSELLIST_CONDITION_11.replace(
                    "{res_pr_start_date}", searchData["search_res_pr_start_date"]
                ),
            )
        else:
            query = query.replace("{11}", "")

        if searchData["search_res_pr_end_date"] != "":
            query = query.replace(
                "{12}",
                SELECT_MATERSELLIST_CONDITION_12.replace(
                    "{res_pr_end_date}", searchData["search_res_pr_end_date"]
                ),
            )
        else:
            query = query.replace("{12}", "")

        if searchData["search_res_pc_start_date"] != "":
            query = query.replace(
                "{13}",
                SELECT_MATERSELLIST_CONDITION_13.replace(
                    "{res_pc_start_date}", searchData["search_res_pc_start_date"]
                ),
            )
        else:
            query = query.replace("{13}", "")

        if searchData["search_res_pc_end_date"] != "":
            query = query.replace(
                "{14}",
                SELECT_MATERSELLIST_CONDITION_14.replace(
                    "{res_pc_end_date}", searchData["search_res_pc_end_date"]
                ),
            )
        else:
            query = query.replace("{14}", "")

        if searchData["search_res_state_cd"] != "":
            query = query.replace(
                "{15}",
                SELECT_MATERSELLIST_CONDITION_15.replace(
                    "{res_state_cd}", searchData["search_res_state_cd"]
                ),
            )
        else:
            query = query.replace("{15}", "")

        if searchData["search_ic_start_date"] != "":
            query = query.replace(
                "{16}",
                SELECT_MATERSELLIST_CONDITION_16.replace(
                    "{ic_start_date}", searchData["search_ic_start_date"]
                ),
            )
        else:
            query = query.replace("{16}", "")

        if searchData["search_ic_end_date"] != "":
            query = query.replace(
                "{20}",
                SELECT_MATERSELLIST_CONDITION_20.replace(
                    "{ic_end_date}", searchData["search_ic_end_date"]
                ),
            )
        else:
            query = query.replace("{20}", "")

        if searchData["search_ic_result"] != "":
            query = query.replace(
                "{17}",
                SELECT_MATERSELLIST_CONDITION_17.replace(
                    "{ic_result}", searchData["search_ic_result"]
                ),
            )
        else:
            query = query.replace("{17}", "")

        query = query.replace(
            "{21}",
            SELECT_MATERSELLIST_CONDITION_21.replace(
                "{cons_code}", searchData["search_cons_code"]
            ),
        )

        query = query.replace("{18}", "")
        query = query.replace("{19}", "")

        query += ") H"
        return query
