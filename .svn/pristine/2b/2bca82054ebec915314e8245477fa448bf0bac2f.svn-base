# _*_coding: utf-8 -*-
from common import constants

INSERT_MATERIALPERMISSION_INFO = """INSERT INTO MATERIAL_PERMISSION(CONS_CODE, MPR_DOC_NUM, CO_CODE, CONSTR_TYPE_CD, MATERIAL_NUM, SYS_DOC_NUM) """

DELETE_MATERIALPERMISSION_INFO = """DELETE MATERIAL_PERMISSION WHERE 1=1 """


UPDATE_MATERIALPERMISSION_INFO = """UPDATE MATERIAL_PERMISSION SET """


SELECT_MATERIALSELECTLIST_INFO = """
	SELECT
			MPAQ.CONS_CODE AS cons_code, MPAQ.CONS_NAME AS cons_name,
			MPAQ.CONSTR_TYPE_CD AS constr_type_cd, MPAQ.CONSTR_TYPE_NAME AS constr_type_name,
			MPAQ.MATERIAL_NUM AS material_num, MPAQ.MATERIAL_NAME AS material_name,
			MPAQ.JUDGMENT_CODE AS judgment_code, MPAQ.FACT_SYS_DOC_NUM AS fact_sys_doc_num,
			MPAQ.REQ_SYS_DOC_NUM AS req_sys_doc_num, MPAQ.REQ_DOC_NUM AS req_doc_num, MPAQ.REQ_WRITER AS req_writer,MPAQ.REQ_WRITER_NAME AS req_writer_name, 
			MPAQ.REQ_PR_DATE AS req_pr_date, MPAQ.REQ_STATE_CODE AS req_state_code, MPAQ.REQ_STATE_NAME AS req_state_name, MPAQ.REQ_PC_DATE AS req_pc_date,
			MPAQ.RES_SYS_DOC_NUM AS res_sys_doc_num, MPAQ.RES_DOC_NUM AS res_doc_num, MPAQ.RES_WRITER AS res_writer, MPAQ.RES_WRITER_NAME AS res_writer_name,
			MPAQ.RES_PR_DATE AS res_pr_date, MPAQ.RES_STATE_CODE AS res_state_code, MPAQ.RES_STATE_NAME AS res_state_name, MPAQ.RES_PC_DATE AS res_pc_date
			FROM 
				(SELECT 
					MP.CONS_CODE, (SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = MP.CONS_CODE) AS CONS_NAME,
					MP.CONSTR_TYPE_CD, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = MP.CONSTR_TYPE_CD) AS CONSTR_TYPE_NAME,
					MP.MATERIAL_NUM, (SELECT MATERIAL_NAME FROM MATERIAL_MANAGE WHERE MATERIAL_NUM = MP.MATERIAL_NUM) AS MATERIAL_NAME,
					MP.JUDGMENT_CODE, SUB3.FACT_SYS_DOC_NUM,
					MP.SYS_DOC_NUM AS REQ_SYS_DOC_NUM,  MP.MPR_DOC_NUM AS REQ_DOC_NUM, 
					SUB1.REQ_WRITER, SUB1.REQ_WRITER_NAME, SUB1.REQ_PR_DATE,
					SUB1.REQ_STATE_CODE, SUB1.REQ_STATE_NAME, SUB1.REQ_PC_DATE,
					MP.MPN_DOC_NUM AS RES_SYS_DOC_NUM, SUB2.RES_DOC_NUM,
					SUB2.RES_WRITER, SUB2.RES_WRITER_NAME, SUB2.RES_PR_DATE,
					SUB2.RES_STATE_CODE, SUB2.RES_STATE_NAME, SUB2.RES_PC_DATE
				FROM MATERIAL_PERMISSION MP LEFT OUTER JOIN (SELECT 
																DM.CONS_CODE, DM.SYS_DOC_NUM AS REQ_SYS_DOC_NUM, DM.STATE_CODE AS REQ_STATE_CODE, 
																(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = DM.STATE_CODE) AS REQ_STATE_NAME,
																DM.PR_DATE AS REQ_PR_DATE, DM.PC_DATE AS REQ_PC_DATE, DM.WRITER AS REQ_WRITER,
																(SELECT USER_NAME FROM USER WHERE ID = DM.WRITER) AS REQ_WRITER_NAME
															FROM DOC_MANAGE DM
															WHERE 1=1
															AND DM.CONS_CODE = {1}
															AND DM.DOC_CODE = 'CD000013'
															) SUB1 ON MP.CONS_CODE = SUB1.CONS_CODE AND MP.SYS_DOC_NUM = SUB1.REQ_SYS_DOC_NUM
											LEFT OUTER JOIN (SELECT 
																DM.CONS_CODE, DM.SYS_DOC_NUM AS RES_SYS_DOC_NUM, DM.DOC_NUM AS RES_DOC_NUM, DM.STATE_CODE AS RES_STATE_CODE, 
																(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = DM.STATE_CODE) AS RES_STATE_NAME,
																DM.PR_DATE AS RES_PR_DATE, DM.PC_DATE AS RES_PC_DATE, DM.WRITER AS RES_WRITER,
																(SELECT USER_NAME FROM USER WHERE ID = DM.WRITER) AS RES_WRITER_NAME,
																DLI.TO_SYS_DOC_NUM
															FROM DOC_MANAGE DM LEFT OUTER JOIN DOCUMENT_LINK_INFO DLI ON DM.SYS_DOC_NUM = DLI.SYS_DOC_NUM
															WHERE 1=1
															AND DM.CONS_CODE = {1}
															AND DM.DOC_CODE = 'SD000021'
															) SUB2 ON MP.CONS_CODE = SUB2.CONS_CODE AND MP.SYS_DOC_NUM = SUB2.TO_SYS_DOC_NUM
											LEFT OUTER JOIN (SELECT 
																MR.CONS_CODE, MR.SYS_DOC_NUM AS FACT_SYS_DOC_NUM, MR.DOC_CODE AS FACT_DOC_CODE,
																MR.DOC_NUM AS FACT_DOC_NUM,	MR.MATERIAL_NUM AS FACT_MATERIAL_NUM, DLI.TO_SYS_DOC_NUM
																FROM MANUFACTORY_REPORT MR LEFT OUTER JOIN DOCUMENT_LINK_INFO DLI ON MR.SYS_DOC_NUM = DLI.SYS_DOC_NUM
																WHERE 1=1
																AND MR.CONS_CODE = {1}
																) SUB3 ON MP.CONS_CODE = SUB3.CONS_CODE AND MP.SYS_DOC_NUM = SUB3.TO_SYS_DOC_NUM AND MP.MATERIAL_NUM = SUB3.FACT_MATERIAL_NUM
				WHERE MP.CONS_CODE = {1}
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
	{17}
	{18}
	{19}
	"""


SELECT_MATERSELLIST_CONDITION_1 = '"{cons_code}"'
SELECT_MATERSELLIST_CONDITION_2_1 = 'AND MPAQ.REQ_SYS_DOC_NUM IN (SELECT SYS_DOC_NUM FROM APPROVAL_INFORMATION WHERE 1=1 AND (DOC_CODE = "CD000013" OR DOC_CODE = "SD000021" OR DOC_CODE = "SD000007") AND ID = "{loginUserId}")'
SELECT_MATERSELLIST_CONDITION_2_2 = 'AND MPAQ.REQ_SYS_DOC_NUM IN (SELECT DISTINCT SYS_DOC_NUM FROM APPROVAL_INFORMATION    WHERE 1=1 AND CONS_CODE = "{cons_code}" AND (DOC_CODE = "CD000013" OR DOC_CODE = "SD000021" OR DOC_CODE = "SD000007") AND ID IN (SELECT ID FROM USER WHERE CO_CODE IN (SELECT CO_CODE FROM USER WHERE ID = "{loginUserId}")) AND (APPROVAL = "Y" OR CUR_APPROVAL = "Y"))'
SELECT_MATERSELLIST_CONDITION_2_3 = 'AND MPAQ.REQ_SYS_DOC_NUM IN (SELECT DISTINCT SYS_DOC_NUM FROM APPROVAL_INFORMATION    WHERE 1=1 AND CONS_CODE = "{cons_code}" AND (DOC_CODE = "CD000013" OR DOC_CODE = "SD000021" OR DOC_CODE = "SD000007") AND CO_CODE = "{coCode}")'
SELECT_MATERSELLIST_CONDITION_3 = 'AND MPAQ.MATERIAL_NAME LIKE "%{material_name}%"'
SELECT_MATERSELLIST_CONDITION_4 = 'AND MPAQ.CONSTR_TYPE_CD = "{constr_type_cd}"'
SELECT_MATERSELLIST_CONDITION_5 = 'AND MPAQ.JUDGMENT_CODE = "{judgment_code}"'
SELECT_MATERSELLIST_CONDITION_6 = 'AND MPAQ.REQ_WRITER_NAME = "{req_writer}"'
SELECT_MATERSELLIST_CONDITION_7 = 'AND MPAQ.REQ_PR_DATE >= "{req_pr_start_date}"'
SELECT_MATERSELLIST_CONDITION_8 = 'AND MPAQ.REQ_PR_DATE <= "{req_pr_end_date}"'
SELECT_MATERSELLIST_CONDITION_9 = 'AND MPAQ.REQ_PC_DATE >= "{req_pc_start_date}"'
SELECT_MATERSELLIST_CONDITION_10 = 'AND MPAQ.REQ_PC_DATE <= "{req_pc_end_date}"'
SELECT_MATERSELLIST_CONDITION_11 = 'AND MPAQ.REQ_STATE_CODE = "{req_state_cd}"'
SELECT_MATERSELLIST_CONDITION_12 = 'AND MPAQ.RES_WRITER_NAME = "{res_writer}"'
SELECT_MATERSELLIST_CONDITION_13 = 'AND MPAQ.RES_PR_DATE >= "{res_pr_start_date}"'
SELECT_MATERSELLIST_CONDITION_14 = 'AND MPAQ.RES_PR_DATE <= "{res_pr_end_date}"'
SELECT_MATERSELLIST_CONDITION_15 = 'AND MPAQ.RES_PC_DATE >= "{res_pc_start_date}"'
SELECT_MATERSELLIST_CONDITION_16 = 'AND MPAQ.RES_PC_DATE <= "{res_pc_end_date}"'
SELECT_MATERSELLIST_CONDITION_17 = 'AND MPAQ.RES_STATE_CODE = "{res_state_cd}"'
SELECT_MATERSELLIST_CONDITION_18 = "ORDER BY MPAQ.{sort_column} {sort_type}"
SELECT_MATERSELLIST_CONDITION_19 = "LIMIT {start_num}, {end_num} "


INSERT_FACTORYVISIT_INFO = """INSERT INTO MANUFACTORY_REPORT(CONS_CODE, SYS_DOC_NUM, DOC_CODE, DOC_NUM, CONSTR_TYPE_CD, FACILITY_NAME, CO_NAME, FACTORY_NAME, PLACE, VISIT_DATE, INSPECTION_KEY_CONTENT, SPECIALTIES, INSPECTOR, INSPECTOR_ID, CHECKER, CHECKER_ID, MATERIAL_NUM) """
DELETE_FACTORYVISIT_INFO = """DELETE FROM MANUFACTORY_REPORT WHERE 1=1 """

SELECT_CHECKDOCVIEWAUTH_INFO = (
    """SELECT COUNT(*) AS cnt FROM APPROVAL_INFORMATION WHERE 1=1 """
)


SELECT_APPSELMATERLIST_INFO = """
								SELECT 
									MATERIAL_NUM AS material_num, MATERIAL_NAME AS material_name,
									STANDARD_NUM AS standard_num, STANDARD AS standard,
									UNIT AS unit, PRODUCE_CO AS produce_co,
									APPROVAL_NUM AS approval_num, APPROVAL_DATE AS approval_date,
									TYPE AS type, FORMAL_NAME AS formal_name, NOTE AS note,	DESIDE AS deside, KS_WHETHER AS ks_whether,
									KS_PERMIT_COPY_PATH AS ks_permit_copy_path,	KS_PERMIT_COPY_ORIGINAL_NAME AS ks_permit_copy_original_name, KS_PERMIT_COPY_CHANGE_NAME AS ks_permit_copy_change_name,
									CATALOG_PATH AS catalog, CATALOG_ORIGINAL_NAME AS catalog_original_name, CATALOG_CHANGE_NAME AS catalog_change_name,
									BUSINESS_LICENSE_PATH AS business_license_path,	BUSINESS_LICENSE_ORIGINAL_NAME AS business_license_original_name, BUSINESS_LICENSE_CHANGE_NAME AS business_change_name,
									TAX_PAYMENT_CERTIFICATE_PATH AS tax_payment_certificate_path, TAX_PAYMENT_CERTIFICATE_ORIGINAL_NAME AS tax_payment_certificate_original_name, TAX_PAYMENT_CERTIFICATE_CHANGE_NAME AS tax_payment_certificate_change_name,
									PERFORM_CERTIFICATE_PATH AS perform_certificate_path, PERFORM_CERTIFICATE_ORIGINAL_NAME AS perform_certificate_original_name, PERFORM_CERTIFICATE_CHANGE_NAME AS perform_certificate_change_name,
									KFI_CERTIFICATE_PATH AS kfi_certificate_path, KFI_CERTIFICATE_ORIGINAL_NAME AS kfi_certificate_original_name, KFI_CERTIFICATE_CHANGE_NAME AS kfi_certificate_change_name,
									FACTORY_CERTIFICATE_PATH AS factory_certificate_path, FACTORY_CERTIFICATE_ORIGINAL_NAME AS factory_certificate_original_name, FACTORY_CERTIFICATE_CHANGE_NAME AS factory_certificate_change_name,
									TEST_RESULT_PATH AS test_result_path, TEST_RESULT_ORIGINAL_NAME AS test_result_original_name, TEST_RESULT_CHANGE_NAME AS test_result_change_name,
									DELIVER_PERFORM_PATH AS deliver_perform_path, DELIVER_PERFORM_ORIGINAL_NAME AS deliver_perform_original_name, DELIVER_PERFORM_CHANGE_NAME AS deliver_perform_change_name,
									SAMPLE_PATH AS sample_path, SAMPLE_ORIGINAL_NAME AS sample_original_name, SAMPLE_CHANGE_NAME AS sample_change_name 
								FROM MATERIAL_MANAGE 
								WHERE 1=1
								AND MATERIAL_NUM IN (
														SELECT MATERIAL_NUM 
														FROM MATERIAL_PERMISSION 
														WHERE 1=1 
														{1}
														{2}
														AND (JUDGMENT_CODE = '1' OR JUDGMENT_CODE = '2')
													)
							   """

SELECT_APPSELMATERLIST_CONDITION_1 = 'AND CONS_CODE = "{cons_code}" '
SELECT_APPSELMATERLIST_CONDITION_2 = 'AND CO_CODE = "{co_code}" '


class sqlProjectUseMaterialManage:
    # 자재 선정 요청에 대한 자제 정보를 저장 한다.
    def iPutUseMaterialInfo(
        self, consCode, docNum, coCode, constrTypeCd, materialNum, sysDocNum
    ):
        query = INSERT_MATERIALPERMISSION_INFO

        query += "VALUES("
        query += '"' + consCode + '", '
        query += '"' + docNum + '", '
        query += '"' + coCode + '", '
        query += '"' + constrTypeCd + '", '
        query += "" + str(materialNum) + ", "
        query += "" + str(sysDocNum) + ""
        query += ")"

        return query

    # 자재 선정 요청에 대한 자재 정보를 삭제 한다.
    # def dDelUseMaterialInfo(self, consCode, docNum, coCode):
    def dDelUseMaterialInfo(self, sysDocNum):
        query = DELETE_MATERIALPERMISSION_INFO

        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""
        # query += 'AND CONS_CODE = "' + consCode + '"'
        # query += 'AND MPR_DOC_NUM = "' + docNum + '"'
        # query += 'AND CO_CODE = "' + co_Code + '"'

        return query

    # 자재 선정 리스트롤 조회 한다.
    def sSearchMaterialSelectList(self, userInfo, userAuth, jobAuth, searchData):
        query = SELECT_MATERIALSELECTLIST_INFO

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

        # if(userAuth == constants.USER_AUTH_CONTRACTOR) or (userAuth == constants.USER_AUTH_CONTRACTOR_MONITOR) or (userAuth == constants.USER_AUTH_CONTRACTION):
        # else:

        if searchData["search_material_name"] != "":
            query = query.replace(
                "{3}",
                SELECT_MATERSELLIST_CONDITION_3.replace(
                    "{material_name}", searchData["search_material_name"]
                ),
            )
        else:
            query = query.replace("{3}", "")

        if searchData["search_constr_type_cd"] != "":
            query = query.replace(
                "{4}",
                SELECT_MATERSELLIST_CONDITION_4.replace(
                    "{constr_type_cd}", searchData["search_constr_type_cd"]
                ),
            )
        else:
            query = query.replace("{4}", "")

        if searchData["search_judgment_code"] != "":
            query = query.replace(
                "{5}",
                SELECT_MATERSELLIST_CONDITION_5.replace(
                    "{judgment_code}", searchData["search_judgment_code"]
                ),
            )
        else:
            query = query.replace("{5}", "")

        if searchData["search_req_writer"] != "":
            query = query.replace(
                "{6}",
                SELECT_MATERSELLIST_CONDITION_6.replace(
                    "{req_writer}", searchData["search_req_writer"]
                ),
            )
        else:
            query = query.replace("{6}", "")

        if searchData["search_req_pr_start_date"] != "":
            query = query.replace(
                "{7}",
                SELECT_MATERSELLIST_CONDITION_7.replace(
                    "{req_pr_start_date}", searchData["search_req_pr_start_date"]
                ),
            )
        else:
            query = query.replace("{7}", "")

        if searchData["search_req_pr_end_date"] != "":
            query = query.replace(
                "{8}",
                SELECT_MATERSELLIST_CONDITION_8.replace(
                    "{req_pr_end_date}", searchData["search_req_pr_end_date"]
                ),
            )
        else:
            query = query.replace("{8}", "")

        if searchData["search_req_pc_start_date"] != "":
            query = query.replace(
                "{9}",
                SELECT_MATERSELLIST_CONDITION_9.replace(
                    "{req_pc_start_date}", searchData["search_req_pc_start_date"]
                ),
            )
        else:
            query = query.replace("{9}", "")

        if searchData["search_req_pc_end_date"] != "":
            query = query.replace(
                "{10}",
                SELECT_MATERSELLIST_CONDITION_10.replace(
                    "{req_pc_end_date}", searchData["search_req_pc_end_date"]
                ),
            )
        else:
            query = query.replace("{10}", "")

        if searchData["search_req_state_cd"] != "":
            query = query.replace(
                "{11}",
                SELECT_MATERSELLIST_CONDITION_11.replace(
                    "{req_state_cd}", searchData["search_req_state_cd"]
                ),
            )
        else:
            query = query.replace("{11}", "")

        if searchData["search_res_writer"] != "":
            query = query.replace(
                "{12}",
                SELECT_MATERSELLIST_CONDITION_12.replace(
                    "{res_writer}", searchData["search_res_writer"]
                ),
            )
        else:
            query = query.replace("{12}", "")

        if searchData["search_res_pr_start_date"] != "":
            query = query.replace(
                "{13}",
                SELECT_MATERSELLIST_CONDITION_13.replace(
                    "{res_pr_start_date}", searchData["search_res_pr_start_date"]
                ),
            )
        else:
            query = query.replace("{13}", "")

        if searchData["search_res_pr_end_date"] != "":
            query = query.replace(
                "{14}",
                SELECT_MATERSELLIST_CONDITION_14.replace(
                    "{res_pr_end_date}", searchData["search_res_pr_end_date"]
                ),
            )
        else:
            query = query.replace("{14}", "")

        if searchData["search_res_pc_start_date"] != "":
            query = query.replace(
                "{15}",
                SELECT_MATERSELLIST_CONDITION_15.replace(
                    "{res_pc_start_date}", searchData["search_res_pc_start_date"]
                ),
            )
        else:
            query = query.replace("{15}", "")

        if searchData["search_res_pc_end_date"] != "":
            query = query.replace(
                "{16}",
                SELECT_MATERSELLIST_CONDITION_16.replace(
                    "{res_pc_end_date}", searchData["search_res_pc_end_date"]
                ),
            )
        else:
            query = query.replace("{16}", "")

        if searchData["search_res_state_cd"] != "":
            query = query.replace(
                "{17}",
                SELECT_MATERSELLIST_CONDITION_17.replace(
                    "{res_state_cd}", searchData["search_res_state_cd"]
                ),
            )
        else:
            query = query.replace("{17}", "")

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

    # 자재 선정 리스트 개수롤 조회 한다.
    def sSearchMaterialSelectListCnt(self, userInfo, userAuth, jobAuth, searchData):
        query = "SELECT COUNT(*) AS cnt FROM ("

        query += SELECT_MATERIALSELECTLIST_INFO

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

        if searchData["search_constr_type_cd"] != "":
            query = query.replace(
                "{4}",
                SELECT_MATERSELLIST_CONDITION_4.replace(
                    "{constr_type_cd}", searchData["search_constr_type_cd"]
                ),
            )
        else:
            query = query.replace("{4}", "")

        if searchData["search_judgment_code"] != "":
            query = query.replace(
                "{5}",
                SELECT_MATERSELLIST_CONDITION_5.replace(
                    "{judgment_code}", searchData["search_judgment_code"]
                ),
            )
        else:
            query = query.replace("{5}", "")

        if searchData["search_req_writer"] != "":
            query = query.replace(
                "{6}",
                SELECT_MATERSELLIST_CONDITION_6.replace(
                    "{req_writer}", searchData["search_req_writer"]
                ),
            )
        else:
            query = query.replace("{6}", "")

        if searchData["search_req_pr_start_date"] != "":
            query = query.replace(
                "{7}",
                SELECT_MATERSELLIST_CONDITION_7.replace(
                    "{req_pr_start_date}", searchData["search_req_pr_start_date"]
                ),
            )
        else:
            query = query.replace("{7}", "")

        if searchData["search_req_pr_end_date"] != "":
            query = query.replace(
                "{8}",
                SELECT_MATERSELLIST_CONDITION_8.replace(
                    "{req_pr_end_date}", searchData["search_req_pr_end_date"]
                ),
            )
        else:
            query = query.replace("{8}", "")

        if searchData["search_req_pc_start_date"] != "":
            query = query.replace(
                "{9}",
                SELECT_MATERSELLIST_CONDITION_9.replace(
                    "{req_pc_start_date}", searchData["search_req_pc_start_date"]
                ),
            )
        else:
            query = query.replace("{9}", "")

        if searchData["search_req_pc_end_date"] != "":
            query = query.replace(
                "{10}",
                SELECT_MATERSELLIST_CONDITION_10.replace(
                    "{req_pc_end_date}", searchData["search_req_pc_end_date"]
                ),
            )
        else:
            query = query.replace("{10}", "")

        if searchData["search_req_state_cd"] != "":
            query = query.replace(
                "{11}",
                SELECT_MATERSELLIST_CONDITION_11.replace(
                    "{req_state_cd}", searchData["search_req_state_cd"]
                ),
            )
        else:
            query = query.replace("{11}", "")

        if searchData["search_res_writer"] != "":
            query = query.replace(
                "{12}",
                SELECT_MATERSELLIST_CONDITION_12.replace(
                    "{res_writer}", searchData["search_res_writer"]
                ),
            )
        else:
            query = query.replace("{12}", "")

        if searchData["search_res_pr_start_date"] != "":
            query = query.replace(
                "{13}",
                SELECT_MATERSELLIST_CONDITION_13.replace(
                    "{res_pr_start_date}", searchData["search_res_pr_start_date"]
                ),
            )
        else:
            query = query.replace("{13}", "")

        if searchData["search_res_pr_end_date"] != "":
            query = query.replace(
                "{14}",
                SELECT_MATERSELLIST_CONDITION_14.replace(
                    "{res_pr_end_date}", searchData["search_res_pr_end_date"]
                ),
            )
        else:
            query = query.replace("{14}", "")

        if searchData["search_res_pc_start_date"] != "":
            query = query.replace(
                "{15}",
                SELECT_MATERSELLIST_CONDITION_15.replace(
                    "{res_pc_start_date}", searchData["search_res_pc_start_date"]
                ),
            )
        else:
            query = query.replace("{15}", "")

        if searchData["search_res_pc_end_date"] != "":
            query = query.replace(
                "{16}",
                SELECT_MATERSELLIST_CONDITION_16.replace(
                    "{res_pc_end_date}", searchData["search_res_pc_end_date"]
                ),
            )
        else:
            query = query.replace("{16}", "")

        if searchData["search_res_state_cd"] != "":
            query = query.replace(
                "{17}",
                SELECT_MATERSELLIST_CONDITION_17.replace(
                    "{res_state_cd}", searchData["search_res_state_cd"]
                ),
            )
        else:
            query = query.replace("{17}", "")

        query = query.replace("{18}", "")
        query = query.replace("{19}", "")

        query += ") H"
        return query

    # 자재 선정 통보 정보를 저장 한다.
    def uModifyUseMaterialInfo(
        self, consCode, reqSysDocNum, constrTypeCd, approvalInfo, sysDocNum
    ):
        query = UPDATE_MATERIALPERMISSION_INFO

        query += "MPN_DOC_NUM = " + str(sysDocNum) + ", "
        query += 'JUDGMENT_CODE = "' + approvalInfo["judgment"] + '" '

        query += "WHERE 1=1 "
        query += 'AND CONS_CODE = "' + consCode + '" '
        query += 'AND CONSTR_TYPE_CD = "' + constrTypeCd + '" '
        query += "AND SYS_DOC_NUM = " + str(reqSysDocNum) + " "
        query += "AND MATERIAL_NUM = " + str(approvalInfo["material_num"])

        return query

    # 공장 방문 검사 결과 정보를 저장 한다.
    def iPutFactoryVisitResult(self, docDefaultInfo, params):
        query = INSERT_FACTORYVISIT_INFO

        query += "VALUES("
        query += '"' + params["reqDocInfo"]["cons_code"] + '", '
        query += "" + str(docDefaultInfo["sysDocNum"]) + ", "
        query += '"' + params["reqDocInfo"]["doc_code"] + '", '
        query += '"' + docDefaultInfo["documentNumber"] + '", '
        query += '"' + params["reqDocContent"]["constr_type_cd"] + '", '
        query += '"' + params["reqDocContent"]["facility_name"] + '", '
        query += '"' + params["reqDocContent"]["co_name"] + '", '
        query += '"' + params["reqDocContent"]["factory_name"] + '", '
        query += '"' + params["reqDocContent"]["place"] + '", '
        query += '"' + params["reqDocContent"]["visit_date"] + '", '
        query += '"' + params["reqDocContent"]["inspection_key_content"] + '", '
        query += '"' + params["reqDocContent"]["specialties"] + '", '
        query += '"' + params["reqDocContent"]["inspector"] + '", '
        query += '"' + params["reqDocContent"]["inspector_id"] + '", '
        query += '"' + params["reqDocContent"]["checker"] + '", '
        query += '"' + params["reqDocContent"]["checker_id"] + '", '
        query += '"' + params["reqDocContent"]["material_num"] + '" '
        query += ")"

        return query

    # 공장 방문 검사 결과 정보를 삭제 한다.
    def dDelFactoryVisitResult(self, consCode, sysDocNum):
        query = DELETE_FACTORYVISIT_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + " "

        return query

    # 해당 문서를 볼 수 있는지 확인 한다.
    def sCheckDocViewAuth(self, consCode, userId, sysDocNum):
        query = SELECT_CHECKDOCVIEWAUTH_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += 'AND ID = "' + userId + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + " "

        return query

    # 선정된 자재 리스트를 조회 한다.
    def sGetAppSelMaterialList(self, consCode, userInfo):
        query = SELECT_APPSELMATERLIST_INFO

        query = query.replace(
            "{1}", SELECT_APPSELMATERLIST_CONDITION_1.replace("{cons_code}", consCode)
        )
        query = query.replace(
            "{2}",
            SELECT_APPSELMATERLIST_CONDITION_2.replace(
                "{co_code}", userInfo["co_code"]
            ),
        )

        return query
