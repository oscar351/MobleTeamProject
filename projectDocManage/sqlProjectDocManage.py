# _*_coding: utf-8 -*-
import json
from common import constants


SELECT_DOCLIST_INFO_OLD_20230111 = """
							SELECT  
								E.CONS_CODE as cons_code, E.CONS_NAME AS cons_name, E.DOC_CODE as doc_code, E.DOC_NAME AS doc_name, E.DOC_NUM as doc_num, E.DOC_CREATEDATE as doc_createdate, E.STATE_CODE as state_code, 
								E.STATE_NAME AS state_name, E.PR_DATE as pr_date, E.PC_DATE as pc_date, E.WRITER as writer, E.WRITER_NAME AS writer_name, E.CO_CODE as co_code, E.CO_NAME AS co_name, E.SYS_DOC_NUM as sys_doc_num,
								B.ID AS cur_approver, B.CUR_APPROVER_NAME AS cur_approver_name,
								C.ID AS receiver, C.RECEIVER_NAME AS receiver_name
							FROM (SELECT
									   A.CONS_CODE,
									   (SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = A.CONS_CODE) AS CONS_NAME,
									   (SELECT PROJECT_STATUS FROM PROJECT WHERE CONS_CODE = A.CONS_CODE) AS PROJECT_STATUS_CD,
									   A.DOC_CODE,
									   (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.DOC_CODE) AS DOC_NAME,
									   A.DOC_NUM,
									   A.DOC_CREATEDATE,
									   A.STATE_CODE,
									   (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.STATE_CODE) AS STATE_NAME,
									   A.PR_DATE,
									   A.PC_DATE,
									   A.WRITER,
									   (SELECT USER_NAME FROM USER WHERE ID = A.WRITER) AS WRITER_NAME,
									   A.CO_CODE,
									   (SELECT CO_NAME FROM CO_INFO_MANAGE WHERE CO_CODE = A.CO_CODE) AS CO_NAME,
									   A.SYS_DOC_NUM
								  FROM DOC_MANAGE A
								  WHERE 1=1
								  AND A.SYS_DOC_NUM IN (SELECT DISTINCT SYS_DOC_NUM
														FROM APPROVAL_INFORMATION 
														WHERE 1=1
														{2}
														{1}
														AND (APPROVAL = "Y" OR CUR_APPROVAL = "Y")
													   )
								 ) E LEFT OUTER JOIN (SELECT SYS_DOC_NUM, ID, (SELECT USER_NAME FROM USER WHERE ID = AI.ID) AS CUR_APPROVER_NAME
													  FROM APPROVAL_INFORMATION AI
													  WHERE 1=1
													  AND AI.CUR_APPROVAL = "Y"
													  {2-1}
												     ) B ON B.SYS_DOC_NUM = E.SYS_DOC_NUM
									 LEFT OUTER JOIN (SELECT AI.SYS_DOC_NUM, AI.ID, (SELECT USER_NAME FROM USER WHERE ID = AI.ID) AS RECEIVER_NAME
													  FROM APPROVAL_INFORMATION AI
													  WHERE (AI.SYS_DOC_NUM, AI.ORDER_NUM) IN (SELECT SYS_DOC_NUM, MAX(ORDER_NUM) AS ORDER_NUM
																							   FROM APPROVAL_INFORMATION
																							   WHERE 1=1
																							   {2}
																							   GROUP BY SYS_DOC_NUM)
													  ORDER BY AI.SYS_DOC_NUM ASC, AI.ORDER_NUM DESC) C ON C.SYS_DOC_NUM  = E.SYS_DOC_NUM
							WHERE 1=1
							{2-2}
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
					   """

SELECT_DOCLIST_INFO = """
	SELECT  
		E.CONS_CODE as cons_code, E.CONS_NAME AS cons_name, E.DOC_CODE as doc_code, E.DOC_NAME AS doc_name, E.DOC_NUM as doc_num, E.DOC_CREATEDATE as doc_createdate, E.STATE_CODE as state_code, 
		E.STATE_NAME AS state_name, E.PR_DATE as pr_date, E.PC_DATE as pc_date, E.WRITER as writer, E.WRITER_NAME AS writer_name, E.CO_CODE as co_code, E.CO_NAME AS co_name, E.SYS_DOC_NUM as sys_doc_num,
		C.ID AS receiver, C.RECEIVER_NAME AS receiver_name
	FROM (
			SELECT
				A.CONS_CODE,
				(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = A.CONS_CODE) AS CONS_NAME,
				(SELECT PROJECT_STATUS FROM PROJECT WHERE CONS_CODE = A.CONS_CODE) AS PROJECT_STATUS_CD,
				A.DOC_CODE,
				(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.DOC_CODE) AS DOC_NAME,
				A.DOC_NUM,
				A.DOC_CREATEDATE,
				A.STATE_CODE,
				(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.STATE_CODE) AS STATE_NAME,
				A.PR_DATE,
				A.PC_DATE,
				A.WRITER,
				(SELECT USER_NAME FROM USER WHERE ID = A.WRITER) AS WRITER_NAME,
				A.CO_CODE,
				(SELECT CO_NAME FROM CO_INFO_MANAGE WHERE CO_CODE = A.CO_CODE) AS CO_NAME,
				A.SYS_DOC_NUM
			FROM DOC_MANAGE A
			WHERE 1=1
			AND A.SYS_DOC_NUM IN (
									SELECT DISTINCT SYS_DOC_NUM
									FROM APPROVAL_INFORMATION 
									WHERE 1=1
									{2}
									{1}
									{15}
								)
		) E  LEFT OUTER JOIN (
								SELECT AI.SYS_DOC_NUM, AI.ID, (
																SELECT USER_NAME FROM USER WHERE ID = AI.ID) AS RECEIVER_NAME
																FROM APPROVAL_INFORMATION AI
																WHERE (AI.SYS_DOC_NUM, AI.ORDER_NUM) IN (
																											SELECT SYS_DOC_NUM, MAX(ORDER_NUM) AS ORDER_NUM
																											FROM APPROVAL_INFORMATION
																											WHERE 1=1
																											{2}
																											GROUP BY SYS_DOC_NUM
																										)
								 ORDER BY AI.SYS_DOC_NUM ASC, AI.ORDER_NUM DESC
							) C ON C.SYS_DOC_NUM  = E.SYS_DOC_NUM
		WHERE 1=1
		{2-2}
		{3}
		{4}
		{5}
		{6}
		{7}
		{8}
		{9}
		{11}
		{12}
		{13}
		{14}
"""

SELECT_DOCLIST_CONDITION_1_1 = 'AND ID = "{loginUserId}"'
SELECT_DOCLIST_CONDITION_1_2 = 'AND ID IN (SELECT ID FROM USER WHERE CO_CODE IN (SELECT CO_CODE FROM USER WHERE ID = "{loginUserId}"))'
SELECT_DOCLIST_CONDITION_1_3 = 'AND CO_CODE = "{coCode}"'
SELECT_DOCLIST_CONDITION_2 = 'AND CONS_CODE = "{cons_code}"'
SELECT_DOCLIST_CONDITION_2_1 = 'AND AI.CONS_CODE = "{cons_code}"'
SELECT_DOCLIST_CONDITION_2_2 = 'AND E.PROJECT_STATUS_CD IN ("ST000001", "ST000002")'
SELECT_DOCLIST_CONDITION_3 = 'AND E.PR_DATE >= "{search_start_writer_date}"'
SELECT_DOCLIST_CONDITION_4 = 'AND E.PR_DATE <= "{search_end_writer_date}"'
SELECT_DOCLIST_CONDITION_5 = 'AND E.PC_DATE >= "{search_start_completion_date}"'
SELECT_DOCLIST_CONDITION_6 = 'AND E.PC_DATE <= "{search_end_completion_date}"'
SELECT_DOCLIST_CONDITION_7 = 'AND E.DOC_CODE = "{search_doc_code}"'
SELECT_DOCLIST_CONDITION_8 = 'AND E.DOC_NUM LIKE "%{search_doc_num}%"'
SELECT_DOCLIST_CONDITION_9 = 'AND E.WRITER_NAME LIKE "%{search_writer}%"'
SELECT_DOCLIST_CONDITION_10 = 'AND B.CUR_APPROVER_NAME LIKE "%{search_cur_approver}%"'
SELECT_DOCLIST_CONDITION_11 = 'AND C.RECEIVER_NAME LIKE "%{search_receiver}%"'
SELECT_DOCLIST_CONDITION_12 = 'AND E.STATE_CODE = "{search_approval_status}"'
SELECT_DOCLIST_CONDITION_13 = "ORDER BY {sort_column} {sort_type}"
SELECT_DOCLIST_CONDITION_14 = "LIMIT {start_num}, {end_num}"
SELECT_DOCLIST_CONDITION_15_0 = 'AND APPROVAL = "N" AND CUR_APPROVAL = "Y"'
SELECT_DOCLIST_CONDITION_15_1 = "AND ORDER_NUM = 1"
SELECT_DOCLIST_CONDITION_15_2 = 'AND (APPROVAL, CUR_APPROVAL) NOT IN (("N", "N"))'
# SELECT_DOCLIST_CONDITION_15_2 = 'AND (APPROVAL != "N" OR CUR_APPROVAL != "N")'

SELECT_DOCDETAIL_INFO = """
							SELECT 
								A.CONS_CODE AS cons_code, 
								(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = A.CONS_CODE) AS cons_name,
								A.DOC_CODE AS doc_code, 
								(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.DOC_CODE) AS doc_name,
								A.DOC_NUM AS doc_num, A.CONTENT AS content, A.DOC_CREATEDATE AS doc_createdate,
								A.STATE_CODE AS state_code, 
								(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.STATE_CODE) AS state_name,
								A.PR_DATE AS pr_date, A.PC_DATE AS pc_date, 
								A.WRITER AS writer, 
								(SELECT USER_NAME FROM USER WHERE ID = A.WRITER) AS writer_name,
								A.CO_CODE AS co_code, 
								(SELECT CO_NAME FROM CO_INFO_MANAGE WHERE CO_CODE = A.CO_CODE) AS co_name,
								A.SYS_DOC_NUM AS sys_doc_num
							FROM DOC_MANAGE A, (SELECT DISTINCT SYS_DOC_NUM FROM APPROVAL_INFORMATION AI WHERE 1=1 {1} {2} {3}) B
							WHERE 1=1
							AND A.SYS_DOC_NUM = B.SYS_DOC_NUM
						"""

SELECT_DOCDETAIL_CONDITION_1 = 'AND CONS_CODE = "{cons_code}"'
SELECT_DOCDETAIL_CONDITION_2 = "AND SYS_DOC_NUM = {sys_doc_num}"
SELECT_DOCDETAIL_CONDITION_3_1 = 'AND ID = "{loginUserId}"'
SELECT_DOCDETAIL_CONDITION_3_2 = 'AND ID IN (SELECT ID FROM USER WHERE CO_CODE IN (SELECT CO_CODE FROM USER WHERE ID = "{loginUserId}"))'


SELECT_DOCUMENT_INFO = """SELECT
								A.CONS_CODE AS cons_code,
								(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = A.CONS_CODE) AS cons_name,
								A.DOC_CODE AS doc_code,
								(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.DOC_CODE) AS doc_name,
								A.CO_CODE AS co_code,
								(SELECT CO_NAME FROM CO_INFO_MANAGE WHERE CO_CODE = A.CO_CODE) AS co_name
							FROM 
								DOCNUM_MANAGE A
							WHERE
								1=1 """

SELECT_DOCNUM_INFO = """SELECT
							A.DOC_NUM AS doc_num,
							A.ABB AS abb
						 FROM 
							DOCNUM_MANAGE A
						WHERE 1=1 """

UPDATE_DOCNUM_INFO = """UPDATE DOCNUM_MANAGE SET """


INSERT_DOCUMENT_INFO = """INSERT INTO DOC_MANAGE(CONS_CODE, DOC_CODE, DOC_NUM, CONTENT, DOC_CREATEDATE, STATE_CODE, PR_DATE, WRITER, CO_CODE, SYS_DOC_NUM) """
DELETE_DOCUMENT_INFO = """DELETE FROM DOC_MANAGE WHERE 1=1 """
UPDATE_DOCUMENT_INFO = """UPDATE DOC_MANAGE SET """


INSERT_DOCAPPROVAL_INFO = """INSERT INTO APPROVAL_INFORMATION(CONS_CODE, DOC_CODE, DOC_NUM, ORDER_NUM, ID, APPROVAL, APPROVAL_TYPE, CUR_APPROVAL, SYS_DOC_NUM, APPROVAL_DATE, CO_CODE) """
DELETE_DOCAPPROVAL_INFO = """DELETE FROM APPROVAL_INFORMATION WHERE 1=1 """
UPDATE_DOCAPPROVAL_INFO = """UPDATE APPROVAL_INFORMATION SET """


INSERT_LINKDOC_INFO = (
    """INSERT INTO DOCUMENT_LINK_INFO(CONS_CODE, SYS_DOC_NUM, TO_SYS_DOC_NUM) """
)
# INSERT_LINKDOC_INFO = u'''INSERT INTO DOCUMENT_LINK_INFO(CONS_CODE, DOC_CODE, DOC_NUM, TO_DOC_CODE, TO_DOC_NUM) '''
DELETE_LINKDOC_INFO = """DELETE FROM DOCUMENT_LINK_INFO WHERE 1=1 """
SELECT_LINKDOC_INFO = """SELECT A.DOC_CODE AS doc_code, A.DOC_NUM as doc_num, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.DOC_CODE) AS doc_name, A.SYS_DOC_NUM AS sys_doc_num
						  FROM DOC_MANAGE A
						  WHERE 1=1 
						  AND A.SYS_DOC_NUM IN (SELECT TO_SYS_DOC_NUM 
						                        FROM DOCUMENT_LINK_INFO 
						                        WHERE 1=1 
						                        AND CONS_CODE = "{cons_code}" 
						                        AND SYS_DOC_NUM = {sys_doc_num})
 					      ORDER BY A.DOC_NUM ASC"""


SELECT_APPROVAL_INFO = """
							SELECT 
								A.ORDER_NUM AS order_num, 
								A.ID AS id, 
								A.APPROVAL AS approval, 
								A.CUR_APPROVAL AS cur_approval, 
								A.APPROVAL_TYPE AS approval_type,
								(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.APPROVAL_TYPE) AS approval_name,
								A.APPROVAL_DATE AS approval_date,
								B.USER_NAME AS user_name,
								C.SIGN_PATH AS sign_path,
								C.SIGN_ORIGINAL_NAME AS sign_original_name,
								C.SIGN_CHANGE_NAME AS sign_change_name
							FROM 
								APPROVAL_INFORMATION A LEFT OUTER JOIN USER B ON A.ID = B.ID
													   LEFT OUTER JOIN USER_FILE C ON A.ID = C.ID
							WHERE 1=1 
							{1} 
							{2}
							ORDER BY A.ORDER_NUM ASC
					"""
SELECT_APPROVAL_CONDITION_1 = 'AND A.CONS_CODE = "{cons_code}"'
SELECT_APPROVAL_CONDITION_2 = "AND A.SYS_DOC_NUM = {sys_doc_num}"


INSERT_DOCFILEMANA_INFO = """INSERT INTO DOC_FILE_MANAGE(CONS_CODE, SYS_DOC_NUM, DOC_CODE, DOC_NUM, FILE_TYPE, FILE_NUM, FILE_PATH, FILE_ORIGINAL_NAME, FILE_CHANGE_NAME) """

SELECT_DOCFILEMANA_INFO = """SELECT 
									CONS_CODE AS cons_code,
									SYS_DOC_NUM AS sys_doc_num,
									DOC_CODE AS doc_code,
									DOC_NUM AS doc_num,
									FILE_TYPE AS file_type,
									FILE_NUM AS file_num,
									FILE_PATH AS file_path,
									FILE_ORIGINAL_NAME AS file_original_name,
									FILE_CHANGE_NAME AS file_change_name
								FROM DOC_FILE_MANAGE
								WHERE 1=1 """

# 문서 관리 Query Class
class sqlProjectDocManage:

    # 문서 정보를 가져 온다.(작성자가 작성할 수 잇는 문서인지 확인하기 위함)
    def sGetDocumentInfo(self, consCode, docCode, coCode):
        query = SELECT_DOCUMENT_INFO

        query += 'AND A.CONS_CODE = "' + consCode + '" '
        query += 'AND A.DOC_CODE = "' + docCode + '" '
        query += 'AND A.CO_CODE = "' + coCode + '" '

        return query

    # 문서 번호를 가져 온다.
    def sGetDocumentNumInfo(self, consCode, docCode, coCode):
        query = SELECT_DOCNUM_INFO

        query += 'AND A.CONS_CODE = "' + consCode + '" '
        query += 'AND A.DOC_CODE = "' + docCode + '" '
        query += 'AND A.CO_CODE = "' + coCode + '" '

        return query

    # 문서 번호를 업데이트 한다..
    def uModifyDocumentNumInfo(self, consCode, docCode, coCode, docNum):
        query = UPDATE_DOCNUM_INFO
        query += "DOC_NUM = " + str(docNum) + " "
        query += 'WHERE CONS_CODE = "' + consCode + '" '
        query += 'AND DOC_CODE = "' + docCode + '" '
        query += 'AND CO_CODE = "' + coCode + '" '

        return query

    # 문서 정보를 저장 한다.
    def iPutDocumentInfo(self, docDefaultInfo, dataInfo):
        query = INSERT_DOCUMENT_INFO

        query += "VALUES("
        query += '"' + dataInfo["reqDocInfo"]["cons_code"] + '", '
        query += '"' + dataInfo["reqDocInfo"]["doc_code"] + '", '
        query += '"' + docDefaultInfo["documentNumber"] + '", '
        query += "'" + json.dumps(dataInfo["reqDocContent"], ensure_ascii=False) + "', "
        query += '"' + docDefaultInfo["docCreateDate"] + '", '
        query += '"' + docDefaultInfo["stateCode"] + '", '
        query += '"' + docDefaultInfo["prDate"] + '", '
        query += '"' + docDefaultInfo["writer"] + '", '
        query += '"' + docDefaultInfo["coCode"] + '", '
        query += "" + str(docDefaultInfo["sysDocNum"]) + " "
        query += ")"

        return query

    # 문서 정보를 수정 한다.
    def uModifyDocumentInfo(self, uDataInfo):
        query = UPDATE_DOCUMENT_INFO

        query += (
            "CONTENT = '" + json.dumps(uDataInfo["content"], ensure_ascii=False) + "' "
        )
        query += "WHERE 1=1 "
        query += 'AND CONS_CODE = "' + uDataInfo["cons_code"] + '" '
        query += "AND SYS_DOC_NUM = " + str(uDataInfo["sys_doc_num"]) + " "

        return query

    # 문서 정보 를 삭제 한다.
    # def dDelDocumentInfo(self, consCode, docCode, docNum):
    def dDelDocumentInfo(self, sysDocNum):
        query = DELETE_DOCUMENT_INFO

        query += 'AND SYS_DOC_NUM = "' + sysDocNum + '" '
        # query += 'AND CONS_CODE = "' + consCode + '" '
        # query += 'AND DOC_CODE = "' + docCode + '" '
        # query += 'AND DOC_NUM = "' + docNum + '" '

        return query

    # 문서 결재 정보를 저장 한다.
    def iPutDocumentApprovalInfo(
        self, reqDocInfo, approval, docNum, sysDocNum, approvalDate
    ):
        query = INSERT_DOCAPPROVAL_INFO

        query += "VALUES("
        query += '"' + reqDocInfo["cons_code"] + '", '
        query += '"' + reqDocInfo["doc_code"] + '", '
        query += '"' + docNum + '", '
        query += "" + str(approval["order"]) + ", "
        query += '"' + approval["id"] + '", '
        query += '"' + approval["approval"] + '", '
        query += '"' + approval["approval_type"] + '", '
        query += '"' + approval["cur_approval"] + '", '
        query += "" + str(sysDocNum) + ", "
        query += '"' + approvalDate + '", '
        query += '"' + approval["co_code"] + '" '
        query += ")"

        return query

    # 문서 결재 정보를 삭제 한다.
    def dDelDocumentApprovalInfo(self, sysDocNum):
        query = DELETE_DOCAPPROVAL_INFO

        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + " "

        return query

    # 연결된 문서 정보 데이터를 저장 한다.
    def iPutLinkDocInfo(self, consCode, sysDocNum, linkSysDocNum):
        query = INSERT_LINKDOC_INFO

        query += "VALUES("
        query += '"' + consCode + '", '
        query += '"' + sysDocNum + '", '
        query += '"' + linkSysDocNum + '" '
        query += ")"

        return query

    # 연결된 문서 정보 데이터를 삭제 한다.
    def dDelLinkDocInfo(self, consCode, sysDocNum, toSysDocNum):
        query = DELETE_LINKDOC_INFO

        query += 'AND CONS_CODE = "' + consCode + '", '
        query += 'AND SYS_DOC_NUM = "' + sysDocNum + '", '
        query += 'AND TO_SYS_DOC_NUM = "' + toSysDocNum + '" '

        return query

    # 문서 리스트를 조회 한다.
    def sSearchDocList(self, userInfo, userAuth, jobAuth, searchCondition):
        query = SELECT_DOCLIST_INFO

        # if((userAuth == constants.USER_AUTH_SYSMANAGE)
        # 		or (userAuth == constants.USER_AUTH_BUYER)
        # 		or (userAuth == constants.USER_AUTH_SUPERVISOR)
        # 		or (userAuth == constants.USER_AUTH_WHITEHALL)):
        # 	query = query.replace('{1}', '')
        # else:

        if jobAuth == None:
            if (
                userAuth == constants.USER_AUTH_SYSMANAGE
                or userAuth == constants.USER_AUTH_BUYER
                or userAuth == constants.USER_AUTH_WHITEHALL
                or userAuth == constants.USER_AUTH_SUPERVISOR
                or userAuth == constants.USER_AUTH_SUPERVISOR_MONITOR
            ):
                query = query.replace("{1}", "")

            elif (
                userAuth == constants.USER_AUTH_CONTRACTOR
                or userAuth == constants.USER_AUTH_CONTRACTOR_MONITOR
            ):
                query = query.replace(
                    "{1}",
                    SELECT_DOCLIST_CONDITION_1_3.replace(
                        "{coCode}", userInfo["co_code"]
                    ),
                )
            else:
                query = query.replace(
                    "{1}",
                    SELECT_DOCLIST_CONDITION_1_1.replace(
                        "{loginUserId}", userInfo["id"]
                    ),
                )
            # query = query.replace('{1}', SELECT_DOCLIST_CONDITION_1_2.replace('{loginUserId}', userId))
        elif (jobAuth["job_title_code"] == constants.JOB_TITLE_CD_BUYER) or (
            jobAuth["job_title_code"] == constants.JOB_TITLE_CD_WHITEHALL
        ):
            query = query.replace("{1}", "")
        # elif((jobAuth['job_title_code'] == constants.JOB_TITLE_CD_CONTRACTOR)
        # 		or(jobAuth['job_title_code'] == constants.JOB_TITLE_CD_CONTRACTOR_MONITOR)
        # 		or(jobAuth['job_title_code'] == constants.JOB_TITLE_CD_SUPERVISOR)
        # 		or(jobAuth['job_title_code'] == constants.JOB_TITLE_CD_SUPERVISOR_MONITOR)):
        # 	query = query.replace('{1}', SELECT_DOCLIST_CONDITION_1_2.replace('{loginUserId}', userId))
        else:
            query = query.replace(
                "{1}",
                SELECT_DOCLIST_CONDITION_1_1.replace("{loginUserId}", userInfo["id"]),
            )

        if searchCondition["cons_code"] == "":
            query = query.replace("{2}", "")
            query = query.replace("{2-1}", "")
            query = query.replace("{2-2}", SELECT_DOCLIST_CONDITION_2_2)
        else:
            query = query.replace(
                "{2}",
                SELECT_DOCLIST_CONDITION_2.replace(
                    "{cons_code}", searchCondition["cons_code"]
                ),
            )
            query = query.replace(
                "{2-1}",
                SELECT_DOCLIST_CONDITION_2_1.replace(
                    "{cons_code}", searchCondition["cons_code"]
                ),
            )
            query = query.replace("{2-2}", "")

        if searchCondition["search_start_writer_date"] == "":
            query = query.replace("{3}", "")
        else:
            query = query.replace(
                "{3}",
                SELECT_DOCLIST_CONDITION_3.replace(
                    "{search_start_writer_date}",
                    searchCondition["search_start_writer_date"],
                ),
            )

        if searchCondition["search_end_writer_date"] == "":
            query = query.replace("{4}", "")
        else:
            query = query.replace(
                "{4}",
                SELECT_DOCLIST_CONDITION_4.replace(
                    "{search_end_writer_date}",
                    searchCondition["search_end_writer_date"],
                ),
            )

        if searchCondition["search_start_completion_date"] == "":
            query = query.replace("{5}", "")
        else:
            query = query.replace(
                "{5}",
                SELECT_DOCLIST_CONDITION_5.replace(
                    "{search_start_completion_date}",
                    searchCondition["search_start_completion_date"],
                ),
            )

        if searchCondition["search_end_completion_date"] == "":
            query = query.replace("{6}", "")
        else:
            query = query.replace(
                "{6}",
                SELECT_DOCLIST_CONDITION_6.replace(
                    "{search_end_completion_date}",
                    searchCondition["search_end_completion_date"],
                ),
            )

        if searchCondition["search_doc_code"] == "":
            query = query.replace("{7}", "")
        else:
            query = query.replace(
                "{7}",
                SELECT_DOCLIST_CONDITION_7.replace(
                    "{search_doc_code}", searchCondition["search_doc_code"]
                ),
            )

        if searchCondition["search_doc_num"] == "":
            query = query.replace("{8}", "")
        else:
            query = query.replace(
                "{8}",
                SELECT_DOCLIST_CONDITION_8.replace(
                    "{search_doc_num}", searchCondition["search_doc_num"]
                ),
            )

        if searchCondition["search_writer"] == "":
            query = query.replace("{9}", "")
        else:
            query = query.replace(
                "{9}",
                SELECT_DOCLIST_CONDITION_9.replace(
                    "{search_writer}", searchCondition["search_writer"]
                ),
            )

        # 		if(searchCondition['search_cur_approver'] == ''):
        # 			query = query.replace('{10}', '')
        # 		else:
        # 			query = query.replace('{10}', SELECT_DOCLIST_CONDITION_10.replace('{search_cur_approver}', searchCondition['search_cur_approver']))

        if searchCondition["search_receiver"] == "":
            query = query.replace("{11}", "")
        else:
            query = query.replace(
                "{11}",
                SELECT_DOCLIST_CONDITION_11.replace(
                    "{search_receiver}", searchCondition["search_receiver"]
                ),
            )

        if searchCondition["search_approval_status"] == "":
            query = query.replace("{12}", "")
        else:
            query = query.replace(
                "{12}",
                SELECT_DOCLIST_CONDITION_12.replace(
                    "{search_approval_status}",
                    searchCondition["search_approval_status"],
                ),
            )

        if searchCondition["search_doc_type"] == "0":
            query = query.replace("{15}", SELECT_DOCLIST_CONDITION_15_0)

        elif searchCondition["search_doc_type"] == "1":
            query = query.replace("{15}", SELECT_DOCLIST_CONDITION_15_1)

        elif searchCondition["search_doc_type"] == "2":
            query = query.replace("{15}", SELECT_DOCLIST_CONDITION_15_2)

        if searchCondition["sort_column"] == "WRITER_NAME":
            sortColumn = "E.WRITER_NAME"
        # 		elif(searchCondition['sort_column'] == 'CUR_APPROVER_NAME'):
        # 			sortColumn = 'B.CUR_APPROVER_NAME'
        elif searchCondition["sort_column"] == "RECEIVER_NAME":
            sortColumn = "C.RECEIVER_NAME"
        else:
            sortColumn = "E." + searchCondition["sort_column"]

        queryTmp = SELECT_DOCLIST_CONDITION_13.replace("{sort_column}", sortColumn)
        queryTmp = queryTmp.replace("{sort_type}", searchCondition["sort_type"])
        query = query.replace("{13}", queryTmp)

        queryTmp = SELECT_DOCLIST_CONDITION_14.replace(
            "{start_num}", searchCondition["start_num"]
        )
        queryTmp = queryTmp.replace("{end_num}", searchCondition["end_num"])
        query = query.replace("{14}", queryTmp)

        return query

    # 문서 리스트 개수를 조회 한다.
    def sSearchDocListCnt(self, userInfo, userAuth, jobAuth, searchCondition):
        query = "SELECT COUNT(*) AS cnt FROM ( "

        query += SELECT_DOCLIST_INFO

        # if((userAuth == constants.USER_AUTH_SYSMANAGE)
        # 		or (userAuth == constants.USER_AUTH_BUYER)
        # 		or (userAuth == constants.USER_AUTH_SUPERVISOR)
        # 		or (userAuth == constants.USER_AUTH_WHITEHALL)):
        # 	query = query.replace('{1}', '')
        # else:
        # 	query = query.replace('{1}', SELECT_DOCLIST_CONDITION_1.replace('{loginUserId}', userId))

        if jobAuth == None:
            if (
                userAuth == constants.USER_AUTH_SYSMANAGE
                or userAuth == constants.USER_AUTH_BUYER
                or userAuth == constants.USER_AUTH_WHITEHALL
                or userAuth == constants.USER_AUTH_SUPERVISOR
                or userAuth == constants.USER_AUTH_SUPERVISOR_MONITOR
            ):
                query = query.replace("{1}", "")

            elif (
                userAuth == constants.USER_AUTH_CONTRACTOR
                or userAuth == constants.USER_AUTH_CONTRACTOR_MONITOR
            ):
                query = query.replace(
                    "{1}",
                    SELECT_DOCLIST_CONDITION_1_3.replace(
                        "{coCode}", userInfo["co_code"]
                    ),
                )
            else:
                query = query.replace(
                    "{1}",
                    SELECT_DOCLIST_CONDITION_1_1.replace(
                        "{loginUserId}", userInfo["id"]
                    ),
                )
            # query = query.replace('{1}', SELECT_DOCLIST_CONDITION_1_2.replace('{loginUserId}', userId))
        elif (jobAuth["job_title_code"] == constants.JOB_TITLE_CD_BUYER) or (
            jobAuth["job_title_code"] == constants.JOB_TITLE_CD_WHITEHALL
        ):
            query = query.replace("{1}", "")
        else:
            query = query.replace(
                "{1}",
                SELECT_DOCLIST_CONDITION_1_1.replace("{loginUserId}", userInfo["id"]),
            )

        # 원본 ########################################################################################
        # if(jobAuth == None):
        # 	query = query.replace('{1}', SELECT_DOCLIST_CONDITION_1_1.replace('{loginUserId}', userId))
        # 	#query = query.replace('{1}', SELECT_DOCLIST_CONDITION_1_2.replace('{loginUserId}', userId))
        # elif((jobAuth['job_title_code'] == constants.JOB_TITLE_CD_BUYER)
        # 		or (jobAuth['job_title_code'] == constants.JOB_TITLE_CD_WHITEHALL)):
        # 	query = query.replace('{1}', '')
        # else:
        # 	query = query.replace('{1}', SELECT_DOCLIST_CONDITION_1_1.replace('{loginUserId}', userId))
        ################################################################################################

        # if((jobAuth['job_title_code'] == constants.JOB_TITLE_CD_BUYER)
        # 		or (jobAuth['job_title_code'] == constants.JOB_TITLE_CD_WHITEHALL)):
        # 	query = query.replace('{1}', '')
        # elif((jobAuth['job_title_code'] == constants.JOB_TITLE_CD_CONTRACTOR)
        # 		or(jobAuth['job_title_code'] == constants.JOB_TITLE_CD_CONTRACTOR_MONITOR)
        # 		or(jobAuth['job_title_code'] == constants.JOB_TITLE_CD_SUPERVISOR)
        # 		or(jobAuth['job_title_code'] == constants.JOB_TITLE_CD_SUPERVISOR_MONITOR)):
        # 	query = query.replace('{1}', SELECT_DOCLIST_CONDITION_1_2.replace('{loginUserId}', userId))
        # else:
        # 	query = query.replace('{1}', SELECT_DOCLIST_CONDITION_1_1.replace('{loginUserId}', userId))

        if searchCondition["cons_code"] == "":
            query = query.replace("{2}", "")
            query = query.replace("{2-1}", "")
            query = query.replace("{2-2}", SELECT_DOCLIST_CONDITION_2_2)
        else:
            query = query.replace(
                "{2}",
                SELECT_DOCLIST_CONDITION_2.replace(
                    "{cons_code}", searchCondition["cons_code"]
                ),
            )
            query = query.replace(
                "{2-1}",
                SELECT_DOCLIST_CONDITION_2_1.replace(
                    "{cons_code}", searchCondition["cons_code"]
                ),
            )
            query = query.replace("{2-2}", "")

        if searchCondition["search_start_writer_date"] == "":
            query = query.replace("{3}", "")
        else:
            query = query.replace(
                "{3}",
                SELECT_DOCLIST_CONDITION_3.replace(
                    "{search_start_writer_date}",
                    searchCondition["search_start_writer_date"],
                ),
            )

        if searchCondition["search_end_writer_date"] == "":
            query = query.replace("{4}", "")
        else:
            query = query.replace(
                "{4}",
                SELECT_DOCLIST_CONDITION_4.replace(
                    "{search_end_writer_date}",
                    searchCondition["search_end_writer_date"],
                ),
            )

        if searchCondition["search_start_completion_date"] == "":
            query = query.replace("{5}", "")
        else:
            query = query.replace(
                "{5}",
                SELECT_DOCLIST_CONDITION_5.replace(
                    "{search_start_completion_date}",
                    searchCondition["search_start_completion_date"],
                ),
            )

        if searchCondition["search_end_completion_date"] == "":
            query = query.replace("{6}", "")
        else:
            query = query.replace(
                "{6}",
                SELECT_DOCLIST_CONDITION_6.replace(
                    "{search_end_completion_date}",
                    searchCondition["search_end_completion_date"],
                ),
            )

        if searchCondition["search_doc_code"] == "":
            query = query.replace("{7}", "")
        else:
            query = query.replace(
                "{7}",
                SELECT_DOCLIST_CONDITION_7.replace(
                    "{search_doc_code}", searchCondition["search_doc_code"]
                ),
            )

        if searchCondition["search_doc_num"] == "":
            query = query.replace("{8}", "")
        else:
            query = query.replace(
                "{8}",
                SELECT_DOCLIST_CONDITION_8.replace(
                    "{search_doc_num}", searchCondition["search_doc_num"]
                ),
            )

        if searchCondition["search_writer"] == "":
            query = query.replace("{9}", "")
        else:
            query = query.replace(
                "{9}",
                SELECT_DOCLIST_CONDITION_9.replace(
                    "{search_writer}", searchCondition["search_writer"]
                ),
            )

        # 		if(searchCondition['search_cur_approver'] == ''):
        # 			query = query.replace('{10}', '')
        # 		else:
        # 			query = query.replace('{10}', SELECT_DOCLIST_CONDITION_10.replace('{search_cur_approver}', searchCondition['search_cur_approver']))

        if searchCondition["search_receiver"] == "":
            query = query.replace("{11}", "")
        else:
            query = query.replace(
                "{11}",
                SELECT_DOCLIST_CONDITION_11.replace(
                    "{search_receiver}", searchCondition["search_receiver"]
                ),
            )

        if searchCondition["search_approval_status"] == "":
            query = query.replace("{12}", "")
        else:
            query = query.replace(
                "{12}",
                SELECT_DOCLIST_CONDITION_12.replace(
                    "{search_approval_status}",
                    searchCondition["search_approval_status"],
                ),
            )

        if searchCondition["search_doc_type"] == "0":
            query = query.replace("{15}", SELECT_DOCLIST_CONDITION_15_0)

        elif searchCondition["search_doc_type"] == "1":
            query = query.replace("{15}", SELECT_DOCLIST_CONDITION_15_1)

        elif searchCondition["search_doc_type"] == "2":
            query = query.replace("{15}", SELECT_DOCLIST_CONDITION_15_2)

        query = query.replace("{13}", "")
        query = query.replace("{14}", "")
        query += ") C "

        return query

    # 연결된 문서 정보를 조회 한다.
    def sGetLinkDocList(self, consCode, sysDocNum):
        query = SELECT_LINKDOC_INFO

        query = query.replace("{cons_code}", consCode)
        query = query.replace("{sys_doc_num}", str(sysDocNum))

        return query

    # 문서 상세 정보를 조회 한다.
    def sGetDocDetailInfo(self, userInfo, userAuth, jobAuth, consCode, sysDocNum):
        query = SELECT_DOCDETAIL_INFO

        # if((userAuth == constants.USER_AUTH_SYSMANAGE)
        # 		or (userAuth == constants.USER_AUTH_BUYER)
        # 		or (userAuth == constants.USER_AUTH_SUPERVISOR)
        # 		or (userAuth == constants.USER_AUTH_WHITEHALL)):
        # 	query = query.replace('{3}', '')
        # else:
        # 	query = query.replace('{3}', SELECT_DOCDETAIL_CONDITION_3.replace('{loginUserId}', userId))

        if consCode == "":
            query = query.replace("{1}", "")
        else:
            query = query.replace(
                "{1}", SELECT_DOCDETAIL_CONDITION_1.replace("{cons_code}", consCode)
            )

        if consCode == "":
            query = query.replace("{2}", "")
        else:
            query = query.replace(
                "{2}", SELECT_DOCDETAIL_CONDITION_2.replace("{sys_doc_num}", sysDocNum)
            )

        if jobAuth == None:
            if (
                userAuth == constants.USER_AUTH_SYSMANAGE
                or userAuth == constants.USER_AUTH_BUYER
                or userAuth == constants.USER_AUTH_WHITEHALL
                or userAuth == constants.USER_AUTH_SUPERVISOR
                or userAuth == constants.USER_AUTH_SUPERVISOR_MONITOR
            ):
                query = query.replace("{3}", "")
            elif (
                userAuth == constants.USER_AUTH_CONTRACTOR
                or userAuth == constants.USER_AUTH_CONTRACTOR_MONITOR
                or userAuth == constants.USER_AUTH_SUPERVISOR
                or userAuth == constants.USER_AUTH_SUPERVISOR_MONITOR
            ):
                query = query.replace(
                    "{3}",
                    SELECT_DOCLIST_CONDITION_1_3.replace(
                        "{coCode}", userInfo["co_code"]
                    ),
                )
            else:
                query = query.replace(
                    "{3}",
                    SELECT_DOCLIST_CONDITION_1_1.replace(
                        "{loginUserId}", userInfo["id"]
                    ),
                )
        elif (jobAuth["job_title_code"] == constants.JOB_TITLE_CD_BUYER) or (
            jobAuth["job_title_code"] == constants.JOB_TITLE_CD_WHITEHALL
        ):
            query = query.replace("{3}", "")
        elif (
            (jobAuth["job_title_code"] == constants.JOB_TITLE_CD_CONTRACTOR)
            or (jobAuth["job_title_code"] == constants.JOB_TITLE_CD_CONTRACTOR_MONITOR)
            or (jobAuth["job_title_code"] == constants.JOB_TITLE_CD_SUPERVISOR)
            or (jobAuth["job_title_code"] == constants.JOB_TITLE_CD_SUPERVISOR_MONITOR)
        ):
            query = query.replace(
                "{3}",
                SELECT_DOCDETAIL_CONDITION_3_2.replace("{loginUserId}", userInfo["id"]),
            )
        else:
            query = query.replace(
                "{3}",
                SELECT_DOCDETAIL_CONDITION_3_1.replace("{loginUserId}", userInfo["id"]),
            )

        return query

    # 결재자 정보를 조회 한다.
    def sGetDocApprovalInfo(self, consCode, sysDocNum):
        query = SELECT_APPROVAL_INFO

        if consCode == "":
            query = query.replace("{1}", "")
        else:
            query = query.replace(
                "{1}", SELECT_APPROVAL_CONDITION_1.replace("{cons_code}", consCode)
            )

        if consCode == "":
            query = query.replace("{2}", "")
        else:
            query = query.replace(
                "{2}", SELECT_APPROVAL_CONDITION_2.replace("{sys_doc_num}", sysDocNum)
            )

        return query

    # 결재정보를 업데이트 한다.
    def uModifyDocumentApproval(self, updateApproval):
        query = UPDATE_DOCAPPROVAL_INFO

        query += 'APPROVAL = "' + updateApproval["approval"] + '", '
        query += 'CUR_APPROVAL = "' + updateApproval["cur_approval"] + '", '
        query += 'APPROVAL_DATE = "' + updateApproval["approval_date"] + '" '

        query += 'WHERE CONS_CODE = "' + updateApproval["cons_code"] + '" '
        query += "AND SYS_DOC_NUM = " + str(updateApproval["sys_doc_num"]) + " "
        query += 'AND ID = "' + updateApproval["id"] + '"'

        return query

    # 문서 결재 상태를 업데이트 한다.
    def uUpdateDocApprovalState(self, updateDocument):
        query = UPDATE_DOCUMENT_INFO

        query += 'STATE_CODE = "' + updateDocument["state_code"] + '", '
        query += 'PC_DATE = "' + updateDocument["pc_date"] + '" '

        query += 'WHERE CONS_CODE = "' + updateDocument["cons_code"] + '" '
        query += "AND SYS_DOC_NUM = " + str(updateDocument["sys_doc_num"]) + " "

        return query

    # 문서 파일 정보를 저장 한다.
    def iPutDocFileInfo(
        self, consCode, sysDocNum, docCode, docNum, fileType, index, fileData
    ):
        query = INSERT_DOCFILEMANA_INFO

        query += "VALUES("
        query += '"' + consCode + '", '
        query += "" + str(sysDocNum) + ", "
        query += '"' + docCode + '", '
        query += '"' + docNum + '", '
        query += '"' + fileType + '", '
        query += '"' + str(index) + '", '
        query += '"' + fileData["file_path"] + '", '
        query += '"' + fileData["file_original_name"] + '", '
        query += '"' + fileData["file_change_name"] + '" '
        query += ")"

        return query

    # 문서 파일 정보를 저장 한다.
    def dRemoveDocFileInfo(self, consCode, sysDocNum):
        query = SELECT_DOCFILEMANA_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + " "

        return query
