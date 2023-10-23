# _*_coding: utf-8 -*-
from common import constants

INSERT_PROJECT_INFO = """INSERT INTO PROJECT(
							CONS_CODE,
							CONS_NAME,
							SUPERV_CO_CODE
						) """

UPDATE_PROJECTDEFAULT_INFO = """UPDATE PROJECT SET """

SELECT_PROJECT_INFO = """SELECT
								A.CONS_CODE AS cons_code,
								A.CONS_NAME AS cons_name,
								IFNULL(A.LOCATION, '') AS location,
								IFNULL(A.CONS_TYPE, '') AS cons_type,
								IFNULL((SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.CONS_TYPE), '') AS cons_type_name,
								IFNULL(A.BUILDING_NAME, '') AS building_name,
								IFNULL(A.LOCATION_CONTACT, '') AS location_contact,
								IFNULL(A.BUSINESS_OUTLINE, '') AS business_outline,
								IFNULL(A.GO_PRICE, '') AS go_price,
								IFNULL(A.DESIGN_PRICE, '') AS design_price,
								IFNULL(A.STRUCTURE, '') AS structure,
								IFNULL(A.UNDERGROUND, '') AS underground,
								IFNULL(A.GROUND, '') AS ground,
								IFNULL(A.MAIN_BUILDING, '') AS main_building,
								IFNULL(A.SUB_BUILDING, '') AS sub_building,
								IFNULL(A.ADD_INFO, '') AS add_info,
								IFNULL(A.HOUSEHOLDS, '') AS households,
								IFNULL(A.SITE_AREA, '') AS site_area,
								IFNULL(A.TOTAL_AREA, '') AS total_area,
								IFNULL(A.BUILDING_AREA, '') AS building_area,
								IFNULL(A.FLOOR_AREA, '') AS floor_area,
								IFNULL(A.RESIDE_CLASS_CODE, '') AS reside_class_code,
								(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.RESIDE_CLASS_CODE) AS reside_class_name,

								IFNULL(A.PURPOSE, '') AS purpose,
								IFNULL((SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.PURPOSE), '') AS purpose_name,
								A.PROJECT_STATUS AS project_status,
								(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.PROJECT_STATUS) AS project_status_name,
                                IFNULL(ROUND(CAST((SELECT SUM((MATERIAL_UNIT_PRICE + LABOR_UNIT_PRICE) * USED_QUANTITY) / SUM((MATERIAL_UNIT_PRICE + LABOR_UNIT_PRICE) * QUANTITY) * 100 FROM PROCESS_DETAIL WHERE CONS_CODE = A.CONS_CODE) AS FLOAT), 2), 0) AS project_progress,
								IFNULL(A.CONS_START_DATE, '') AS cons_start_date,
								IFNULL(A.CONS_END_DATE, '') AS cons_end_date,
								IFNULL(A.SUPERV_CONTRACT_DATE, '') AS superv_contract_date,
								CIM.CO_CODE AS co_code,
								CIM.CO_NAME AS co_name,
								CIM.CEO AS co_ceo,
								IFNULL(CIM.CONTACT, '') AS co_contact
						FROM
							PROJECT A LEFT OUTER JOIN COMPANY CIM ON A.SUPERV_CO_CODE = CIM.CO_CODE
						WHERE
							1 = 1 """

SELECT_PROJECT_DATE = " ".join([
    "SELECT",
    "CONS_START_DATE as cons_start_date,",
    "CONS_END_DATE as cons_end_date",
    "FROM",
    "PROJECT",
    "WHERE CONS_CODE = '{}'",
])

INSERT_JOINWORKSPACE_INFO = """ INSERT INTO JOIN_WORKFORCE(
									CONS_CODE,
									ID,
									AUTHORITY_CODE,
									CO_CODE,
                                    START_DATE,
                                    END_DATE
							) """

INSERT_DOCNUMMANAGE_INFO = """INSERT INTO DOCNUM_MANAGE(
								CONS_CODE,
								DOC_CODE,
								CO_CODE,
								ABB
							)"""


DELETE_PROJECT_INFO = "DELETE FROM PROJECT WHERE 1 = 1 "

UPDATE_JOINWORKFORCE_ENDDATE = (
    "UPDATE JOIN_WORKFORCE SET END_DATE = CURRENT_TIMESTAMP() WHERE 1 = 1 "
)
DELETE_JOINWORKFORCE_INFO = "DELETE FROM JOIN_WORKFORCE WHERE 1 = 1 "

SELECT_DOCNUMMANAGE_INFO = """SELECT
									A.CONS_CODE AS cons_code,
									(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = A.CONS_CODE) AS cons_name,
									A.DOC_CODE AS doc_code,
									(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.DOC_CODE) AS doc_name,
									A.CO_CODE AS co_code,
									(SELECT CO_NAME FROM COMPANY WHERE CO_CODE = A.CO_CODE) AS co_name,
									A.ABB AS abb
								FROM
									DOCNUM_MANAGE A
								WHERE
									1=1 """

SELECT_DOCNUMMANAGECNT_INFO = """SELECT COUNT(*) AS cnt FROM DOCNUM_MANAGE WHERE 1=1 """
UPDATE_DOCNUMMANAGE_INFO = """UPDATE DOCNUM_MANAGE SET ABB = "{abb}" WHERE 1=1 """
DELETE_DOCNUMMANAGE_INFO = """DELETE FROM DOCNUM_MANAGE WHERE 1=1  """


SELECT_JOINWORKFORCE_INFO = """SELECT
									A.CONS_CODE AS cons_code,
									(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = A.CONS_CODE) AS cons_name,
                                    A.CO_CODE AS CO_CODE,
									A.ID AS id,
									A.AUTHORITY_CODE AS authority_code
								FROM
									JOIN_WORKFORCE A
								WHERE 1 = 1 """


SELECT_JOINWORKFORCEVIEW_INFO = """SELECT
									A.CONS_CODE AS cons_code,
									(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = A.CONS_CODE) AS cons_name,
									A.JOB_TITLE_CODE AS job_title_code,
									(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.JOB_TITLE_CODE) AS job_title_name,
									A.ID AS id,
									A.AUTHORITY_CODE AS authority_code,
									(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.AUTHORITY_CODE) AS authority_name,
                                    date_format(A.START_DATE, '%Y%m%d%H%i%S') as start_date,
                                    date_format(A.END_DATE, '%Y%m%d%H%i%S') as end_date,
                                    A.ST_CODE as st_code,
									B.USER_NAME AS user_name,
									B.USER_POSITION AS user_position,
									B.USER_CONTACT AS user_contact,
									B.USER_EMAIL AS user_email,
									B.CO_CODE AS co_code,
									(SELECT CO_NAME FROM COMPANY WHERE CO_CODE = B.CO_CODE) AS co_name
								FROM
                                    PROJECT P
									JOIN JOIN_WORKFORCE A ON P.CONS_CODE = A.CONS_CODE
                                    JOIN USER B ON A.ID = B.ID
								WHERE 1 = 1 """

INSERT_CONSFFF_INFO = """INSERT INTO CONS_FFF(
								CONS_CODE,
								CO_CODE,
								FF_PLAN_CODE,
								CONS_START_DATE,
								CONS_END_DATE
		)"""

UPDATE_CONSFFF_INFO = """UPDATE CONS_FFF SET CONS_START_DATE = "{cons_start_date}", CONS_END_DATE = "{cons_end_date}" WHERE 1=1 """

DELETE_CONSFFF_INFO = """DELETE FROM CONS_FFF WHERE 1 = 1 """
SELECT_CONSFFF_INFO = """SELECT
								A.CONS_CODE AS cons_code,
								(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = A.CONS_CODE) AS cons_name,
								A.CO_CODE AS co_code,
								(SELECT CO_NAME FROM COMPANY WHERE CO_CODE = A.CO_CODE) AS co_name,
								A.FF_PLAN_CODE AS ff_plan_code,
								(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.FF_PLAN_CODE) AS ff_plan_name,
								A.CONS_START_DATE AS cons_start_date,
								A.CONS_END_DATE AS cons_end_date
						FROM
							CONS_FFF A
						WHERE
							1 = 1 """


SELECT_DETAILCONSTR_INFO = """SELECT DISTINCT
								A.DETAIL_CONSTR_TYPE_CD AS detail_constr_type_cd,
								(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.DETAIL_CONSTR_TYPE_CD) AS detail_constr_type_name
							FROM
								DETECTION_CHECK_LIST_CATEGORY A
							WHERE
								1 = 1 """


SELECT_CHECKlIST_INFO = """SELECT
								A.CHK_MSG_CD AS chk_msg_cd,
								(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.CHK_MSG_CD) AS chk_msg_name,
								A.INSP_CRIT_CD AS insp_crit_cd,
								(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.INSP_CRIT_CD) AS insp_crit_name
							FROM
								DETECTION_CHECK_LIST_CATEGORY A
							WHERE
								1 = 1 """


DELETE_PROJDETECTIONCHKLIST_INFO = (
    """DELETE FROM PROJECT_DETECTION_CHECK_LIST WHERE 1 = 1 """
)
INSERT_PROJDETECTIONCHKLIST_INFO = """INSERT INTO PROJECT_DETECTION_CHECK_LIST(
		CONS_CODE, CO_CODE, CONSTR_TYPE_CD, DETAIL_CONSTR_TYPE_CD, CHK_MSG, INSP_CRIT_CD) """
SELECT_PROJDETECTIONCHKLIST_INFO = """SELECT
											A.CONS_CODE AS cons_code,
											(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = A.CONS_CODE) AS cons_name,
											A.CO_CODE AS co_code,
											(SELECT CO_NAME FROM COMPANY WHERE CO_CODE = A.CO_CODE) AS co_name,
											A.CONSTR_TYPE_CD AS constr_type_cd,
											(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.CONSTR_TYPE_CD) AS constr_type_name,
											A.DETAIL_CONSTR_TYPE_CD AS detail_constr_type_cd,
											(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.DETAIL_CONSTR_TYPE_CD) AS detail_constr_type_name,
											A.CHK_MSG AS chk_msg,
											A.INSP_CRIT_CD AS insp_crit_cd,
											(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.INSP_CRIT_CD) AS insp_crit_name
										FROM
											PROJECT_DETECTION_CHECK_LIST A
										WHERE
											1=1 """

SELECT_AREAPROJLISTP_INFO = """SELECT
									COUNT(C.ID) AS cnt
								FROM JOIN_WORKFORCE C
								WHERE C.CONS_CODE IN ((SELECT A.CONS_CODE FROM PROJECT A, (SELECT CONS_CODE FROM JOIN_WORKFORCE WHERE ID IN (SELECT ID FROM USER WHERE CO_CODE = "{co_code}")) B
				WHERE PROJECT_STATUS NOT IN ("ST000002", "ST000003") AND A.CONS_CODE = B.CONS_CODE)) AND C.JOB_TITLE_CODE IN ({job_title_code})
"""

SELECT_AREAPROJLISTC_INFO = """SELECT COUNT(E.CO_CODE) AS cnt FROM (
		SELECT DISTINCT (SELECT CO_CODE FROM USER WHERE ID = C.ID) AS CO_CODE FROM JOIN_WORKFORCE C
		WHERE C.CONS_CODE IN ((SELECT
					A.CONS_CODE
					FROM PROJECT A, (SELECT CONS_CODE FROM JOIN_WORKFORCE WHERE ID IN (SELECT ID FROM USER WHERE CO_CODE = "{co_code}")) B
					WHERE PROJECT_STATUS NOT IN ("ST000002", "ST000003")
					AND A.CONS_CODE = B.CONS_CODE))
		AND C.JOB_TITLE_CODE IN ({job_title_code})) E
"""

INSERT_CONTRACTORSBASIC_INFO = """INSERT INTO CONTRACTORS_BASIC_INFO(CONS_CODE, CO_CODE, CONTRACT_DATE,
																	COMPLETION_DATE, SUB_CONTRACT_PRICE, START_DATE,
																	BIDROPING, BIDWAY,
																	PROC_DETAILS_PATH,
																	PROC_DETAILS_ORIGINAL_NAME,
																	PROC_DETAILS_CHANGE_NAME) """

UPDATE_CONTRACTORSBASIC_INFO = """UPDATE CONTRACTORS_BASIC_INFO SET """


# INSERT_BASEONPROCDETAILS_INFO = u'''INSERT INTO BASED_ON_PROCESS_DETAILS(CONS_CODE, CO_CODE, CONSTR_TYPE_CD, MATERIAL_NUM, MATERIAL_NAME, STANDARD, UNIT, MAT_TOT_CNT, UNIT_PRICE, MAT_TOT_COST, REG_DATE)'''
INSERT_BASEONPROCDETAILS_INFO = """INSERT INTO BASED_ON_PROCESS_DETAILS(CONS_CODE, CO_CODE, CONSTR_TYPE_CD, MATERIAL_NAME, STANDARD, UNIT, MAT_TOT_CNT, UNIT_PRICE, MAT_TOT_COST, REG_DATE)"""

DELETE_BASEONPROCDETAILS_INFO = """DELETE FROM BASED_ON_PROCESS_DETAILS WHERE 1=1 """

INSERT_BASEONOCCAPTIONDETAILS_INFO = """INSERT INTO BASED_ON_OCCAPTION_DETAILS(CONS_CODE, CO_CODE, CONSTR_TYPE_CD, OCC_CD, OCC_NAME, STANDARD, UNIT, OCC_TOT_CNT, UNIT_PRICE, OCC_TOT_COST, REG_DATE)"""

DELETE_BASEONOCCAPTIONDETAILS_INFO = (
    """DELETE FROM BASED_ON_OCCAPTION_DETAILS WHERE 1=1 """
)
SELECT_SUPVDEFAULT_INFO = """SELECT
								IFNULL(A.SUPERV_CONTRACT_DATE, '') AS superv_contract_date,
								IFNULL(A.SUPERV_CO_CODE, '') AS superv_co_code,
								IFNULL(A.SUPERV_PRICE, '') AS superv_price,
								A.RESIDE_CLASS_CODE AS reside_class_code,
								(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.RESIDE_CLASS_CODE) AS reside_class_name
						FROM
							PROJECT A
						WHERE
							1 = 1 """

SELECT_CONTDEFAULT_INFO = """SELECT
								A.CONS_CODE AS cons_code,
								A.CO_CODE AS co_code,
								(SELECT CO_NAME FROM COMPANY WHERE CO_CODE = A.CO_CODE) AS co_name,
								A.CONTRACT_DATE AS contract_date,
								A.COMPLETION_DATE AS completion_date,
								A.SUB_CONTRACT_PRICE AS sub_contract_price,
								A.START_DATE AS start_date,
								A.BIDROPING AS bidroping,
								A.BIDWAY AS bidway,
								A.PROC_DETAILS_PATH AS proc_details_path,
								A.PROC_DETAILS_ORIGINAL_NAME AS proc_details_original_name,
								A.PROC_DETAILS_CHANGE_NAME AS proc_details_change_name
						FROM
							CONTRACTORS_BASIC_INFO A
						WHERE
							1 = 1 """

INSERT_WORKLOGWRITESTANDARD_INFO = (
    """INSERT INTO WORK_LOG_WRITE_STANDARD(CONS_CODE, CO_CODE, WRITE_STANDARD_CD) """
)
SELECT_WORKLOGWRITESTANDARD_INFO = """
	SELECT
		WLWS.CONS_CODE AS cons_code,
		WLWS.CO_CODE AS co_code,
		WLWS.WRITE_STANDARD_CD AS write_standard_code,
		(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = WLWS.WRITE_STANDARD_CD) AS write_standard_name
	FROM
		WORK_LOG_WRITE_STANDARD WLWS
	WHERE 1=1 """

UPDATE_WORKLOGWRITESTANDARD_INFO = """UPDATE WORK_LOG_WRITE_STANDARD SET """


INSERT_PROJSTOPHIS_INFO = """
	INSERT INTO PROJECT_PROGRESS_MANAGE(CONS_CODE, PROJ_STOP_DATE, PROJ_STOP_CAUSE, PROJ_STOP_REG_DATE, REQ_CO_CODE, REQ_ID, PROJ_STOP_APPRO_DATE)
"""

UPDATE_PROJSTOPHIS_INFO = """
	UPDATE PROJECT_PROGRESS_MANAGE SET
"""

DELETE_PROJSTOPHIS_INFO = """
	DELETE FROM PROJECT_PROGRESS_MANAGE WHERE 1=1
"""

# SELECT_PROJECTHISTORY_INFO = u'''
# 	SELECT

#'''

#### 조현우 20230217 추가 프로젝트가 중지상태인지 확인 ####
SELECT_PROJECT_STATUS_INFO = " ".join(
    [
        "SELECT",
        "PROJECT_STATUS as status",
        "FROM PROJECT",
        "WHERE 1=1",
        "{}",
    ]
)

#### 조현우 20230217 추가 시스템 문서번호 해당 프로젝트가 중지상태인지 확인 ####
SELECT_SYSDOCNUM_PROJECT_STATUS_INFO = " ".join(
    [
        "SELECT",
        "P.PROJECT_STATUS as status",
        "FROM PROJECT P ",
        "JOIN WORK_DIARY_MANAGE D",
        "ON P.CONS_CODE = D.CONS_CODE",
        "WHERE 1=1",
        "{}",
    ]
)

#### 조현우 20230223 추가 참여인력의 시작기간을 업데이트 한다. ####
UPDATE_WORKFORCE_STARTDATE_INFO = " ".join(
    [
        "UPDATE",
        "JOIN_WORKFORCE",
        "SET START_DATE = '{}'",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

#### 조현우 20230223 추가 참여인력의 종료기간을 업데이트 한다. ####
UPDATE_WORKFORCE_ENDDATE_INFO = " ".join(
    [
        "UPDATE",
        "JOIN_WORKFORCE",
        "SET END_DATE = '{}'",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

INSERT_WORKFORCE = " ".join(
    [
        "INSERT INTO JOIN_WORKFORCE",
        "(CONS_CODE, ID, AUTHORITY_CODE, CO_CODE, START_DATE, END_DATE)",
        "VALUES('{}', '{}', '{}', '{}', '{}', '{}')",
    ]
)

UPDATE_WORKFORCE = " ".join(
    [
        "UPDATE JOIN_WORKFORCE",
        "SET {}",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

DELETE_WORKFORCE = " ".join(
    [
        "DELETE",
        "FROM",
        "JOIN_WORKFORCE",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

CONSCODE_CONDITION = "AND CONS_CODE = '{}'"
ID_CONDITION = "AND ID = '{}'"
STARTDATE_CONDITION = "AND START_DATE = '{}' "
SYSDOCNUM_CONDITION_D = "AND D.SYS_DOC_NUM = {}"

CONDITION_CONSCODE_AND = 'AND CONS_CODE = "{cons_code}" '
CONDITION_CONSCODE_AND_NAME_A = 'AND A.CONS_CODE = "{cons_code}" '
CONDITION_ID_AND = 'AND ID = "{id}" '
CONDITION_ID_AND_NAME_A = 'AND A.ID = "{id}" '
CONDITION_COCODE_AND = 'AND CO_CODE = "{co_code}" '
CONDITION_COCODE_AND_NAME_A = 'AND A.CO_CODE = "{co_code}" '
CONDITION_DOCCODE_AND = 'AND DOC_CODE = "{doc_code}" '
CONDITION_FFPLANCODE_AND = 'AND FF_PLAN_CODE = "{ff_plan_code}" '
CONDITION_CNOSTRCODE_AND = 'AND CONSTR_TYPE_CD = "{constr_code}" '
CONDITION_CNOSTRCODE_AND_NAME_A = 'AND A.CONSTR_TYPE_CD = "{constr_code}" '
CONDITION_DETAILCNOSTRCODE_AND_NAME_A = (
    'AND A.DETAIL_CONSTR_TYPE_CD = "{detail_constr_code}" '
)

REPLACE_CONSCODE = "{cons_code}"
REPLACE_ID = "{id}"
REPLACE_COCODE = "{co_code}"
REPLACE_ABB = "{abb}"
REPLACE_DOCCODE = "{doc_code}"
REPLACE_CONSSTARTDATE = "{cons_start_date}"
REPLACE_CONSENDDATE = "{cons_end_date}"
REPLACE_FFPLANCODE = "{ff_plan_code}"
REPLACE_CONSTRCODE = "{constr_code}"
REPLACE_DETAILCONSTRCODE = "{detail_constr_code}"
REPLACE_JOBTITLECODE = "{job_title_code}"


# 프로젝트 관리 Query Class
class sqlProjectManage:

    # 1. 프로젝트를 생성 한다.
    #
    # Parameter
    # 	- projectCd | String | 프로젝트 코드
    # 	- projectNm | String | 프로젝트 명
    # def iAddProject(self, projectCd, projectNm, supervCoCode):
    def iPutProject(self, projectCd, projectNm, supervCoCode):
        query = INSERT_PROJECT_INFO

        query += "VALUES("
        query += '"' + projectCd + '", '
        query += '"' + projectNm + '", '
        query += '"' + supervCoCode + '" '
        query += ")"

        return query

    # 2. 프로젝트 참여 인력을 저장 한다.
    #
    # Parameter
    # 	- projectCd | String | 공사 코드
    # 	- userList | Array | 참여 인력 정보
    #   - start_date | String | 공사 시작기간
    #   - end_date | String | 공사 종료기간
    # def iAddJoinWorkforce(self, projectCd, start_date, end_date, userList):
    def iPutJoinWorkforce(self, projectCd, start_date, end_date, userList):
        query = INSERT_JOINWORKSPACE_INFO
        query += "VALUES"

        query += ", ".join([
            f"(\'{projectCd}\', \'{user['id']}\', \'{user['authority_code']}\', \'{user['co_code']}\', '{start_date}', '{end_date}')"
            for user in userList
            ])

        return query

    # 3. 프로젝트를 삭제 한다.
    #
    # Parameter
    # 	- projectCd  | String | 프로젝트 코드
    def dDelProject(self, projectCd):
        query = DELETE_PROJECT_INFO

        query += CONDITION_CONSCODE_AND.replace(REPLACE_CONSCODE, projectCd)

        return query

    # 4. 문서 번호를 생성 한다.
    #
    # Parameter
    # 	- projectCd | String | 공사 코드
    # 	- coCd | String | 회사 코드
    # 	- docList | Object | 문서 리스트
    # def iAddDocnumManage(self, projectCd, coCd, docList):
    def iPutDocNumManage(self, projectCd, coCd, docList):
        query = INSERT_DOCNUMMANAGE_INFO
        query += "VALUES"

        size = docList.__len__()
        num = 0

        for doc in docList:

            query += "("
            query += '"' + projectCd + '", '
            query += '"' + doc["fullcode"] + '", '
            query += '"' + coCd + '", '
            query += '"' + doc["subcode_explain"] + '" '

            if num < size - 1:
                query += "),"
            else:
                query += ")"

            num += 1

        return query

    # 5. 프로젝트 참여 인력 ID에 대한 직책 코드를 가져 온다.
    #
    # Parameter
    # 	- projectCd | String | 프로젝트 코드
    # 	- userId | String | 사용자 ID
    def sGetJobTitleCdObj(self, projectCd, userId, co_code=None):
        query = SELECT_JOINWORKFORCE_INFO

        query += CONDITION_CONSCODE_AND_NAME_A.replace(REPLACE_CONSCODE, projectCd)
        query += CONDITION_ID_AND_NAME_A.replace(REPLACE_ID, userId)
        query += (
            CONDITION_COCODE_AND_NAME_A.replace(REPLACE_COCODE, co_code)
            if co_code
            else ""
        )
        return query

    # 5. 프로젝트 회사참여 확인한다.
    #
    # Parameter
    # 	- projectCd | String | 프로젝트 코드
    # 	- userId | String | 사용자 ID
    def sGetCompanyin(self, projectCd, co_code=None):
        query = SELECT_JOINWORKFORCE_INFO

        query += CONDITION_CONSCODE_AND_NAME_A.replace(REPLACE_CONSCODE, projectCd)
        query += (
            CONDITION_COCODE_AND_NAME_A.replace(REPLACE_COCODE, co_code)
            if co_code
            else ""
        )

        return query

    # 6. 프로젝트 참여 인력 정보를 삭제 한다.
    #
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- userList | Array | 사용자 ID 리스트
    def dDelJoinWorkforce(self, consCode, userList):
        query = DELETE_JOINWORKFORCE_INFO

        query += CONDITION_CONSCODE_AND.replace(REPLACE_CONSCODE, consCode)

        query += "AND ID IN("
        size = userList.__len__()
        num = 0

        for info in userList:
            query += '"' + info["id"]
            if num < size - 1:
                query += '", '
            else:
                query += '" '

            num += 1

        query += ")"

        return query

    # 6-1. 프로젝트 참여 인력 정보를 삭제하는 대신 퇴사일을 맞춘다
    def expelJoinWorkforce(self, consCode, userList):
        query = UPDATE_JOINWORKFORCE_ENDDATE

        query += CONDITION_CONSCODE_AND.replace(REPLACE_CONSCODE, consCode)

        query += "AND ID IN("
        size = userList.__len__()
        num = 0

        for info in userList:
            query += '"' + info["id"]
            if num < size - 1:
                query += '", '
            else:
                query += '" '

            num += 1

        query += ")"

        return query

    # 6-2. 프로젝트 참여 인력을 삭제한다.
    def removeJoinWorkforce(self, co_code, user_id):
        query = DELETE_JOINWORKFORCE_INFO

        query += f" AND CO_CODE = '{co_code}'"
        query += f" AND ID = '{user_id}'"

        return query

    # 7. 프로젝트 참여 인력을 가져온다.
    #
    # Parameter
    # 	- projectCd | String | 프로젝트 코드
    # 	- jobList | Array | 직책 리스트
    def sGetJoinWorkforceInfo(self, projectCd, jobList):
        query = SELECT_JOINWORKFORCEVIEW_INFO

        query += 'AND A.CONS_CODE = "' + projectCd + '" '

        #        if jobList != None:
        #            query += "AND A.JOB_TITLE_CODE IN("
        #            size = jobList.__len__()
        #            num = 0

        #            for info in jobList:
        #                query += '"' + info
        #                if num < size - 1:
        #                    query += '", '
        #                else:
        #                    query += '" '
        #
        #                num += 1
        #
        #            query += ") "

        query += "AND A.ID = B.ID "
        # query += "ORDER BY A.AUTHORITY_CODE ASC "
        query += "ORDER BY B.CO_CODE ASC, A.AUTHORITY_CODE ASC "

        return query

    # 8. 프로젝트 내 등록된 문서가 있는지 확인 한다.
    #
    # Parameter
    # 	- projectCd | String | 프로젝트 코드
    # 	- coCode | String | 회사 코드
    def sCheckDocInProject(self, projectCd, coCode):
        query = SELECT_DOCNUMMANAGECNT_INFO
        query += CONDITION_CONSCODE_AND.replace(REPLACE_CONSCODE, projectCd)
        query += CONDITION_COCODE_AND.replace(REPLACE_COCODE, coCode)

        return query

    # 9. 프로젝트 문서 설정 정보를 조회 한다.
    #
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- coCode | String | 회사 코드
    def sGetProjDocNumCfg(self, consCode, coCode):
        query = SELECT_DOCNUMMANAGE_INFO
        query += CONDITION_CONSCODE_AND_NAME_A.replace(REPLACE_CONSCODE, consCode)
        query += CONDITION_COCODE_AND_NAME_A.replace(REPLACE_COCODE, coCode)

        return query

    # 10. 프로젝트 문서 설정 정보를 업데이트 한다.
    #
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- coCode | String | 회사 코드
    # 	- docInfo | Object | 업데이트 문서 정보
    def sUpdateProjDocNumCfg(self, consCode, coCode, docInfo):
        query = UPDATE_DOCNUMMANAGE_INFO.replace(REPLACE_ABB, docInfo["abb"])

        query += CONDITION_CONSCODE_AND.replace(REPLACE_CONSCODE, consCode)
        query += CONDITION_COCODE_AND.replace(REPLACE_COCODE, coCode)
        query += CONDITION_DOCCODE_AND.replace(REPLACE_DOCCODE, docInfo["doc_code"])

        return query

    # 소방시설공사 정보를 추가 한다.
    #
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- coCode | String | 회사 코드
    # 	- ffPlan | Object | 소방시설공사 정보
    def iPutFFPlan(self, consCode, coCode, ffPlan):
        query = INSERT_CONSFFF_INFO

        query += "VALUES("
        query += '"' + consCode + '", '
        query += '"' + coCode + '", '
        query += '"' + ffPlan["ff_plan_code"] + '", '
        query += '"' + ffPlan["cons_start_date"] + '", '
        query += '"' + ffPlan["cons_end_date"] + '"'
        query += ")"

        return query

    # 12. 소방시설공사 정보를 수정 한다.
    #
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- coCode | String | 회사 코드
    # 	- ffPlan | Object | 소방시설공사 정보
    def uUpdateFFPlan(self, consCode, coCode, ffPlan):
        query = UPDATE_CONSFFF_INFO.replace(
            REPLACE_CONSSTARTDATE, ffPlan["cons_start_date"]
        )
        query = query.replace(REPLACE_CONSENDDATE, ffPlan["cons_end_date"])

        query += CONDITION_CONSCODE_AND.replace(REPLACE_CONSCODE, consCode)
        query += CONDITION_COCODE_AND.replace(REPLACE_COCODE, coCode)
        query += CONDITION_FFPLANCODE_AND.replace(
            REPLACE_FFPLANCODE, ffPlan["ff_plan_code"]
        )

        return query

    # 13. 소방시설공사 정보를 삭제 한다.
    #
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- coCode | String | 회사 코드
    # 	- ffPlan | Object | 소방시설공사 정보
    def dDelFFPlan(self, consCode, coCode, ffPlan):
        query = DELETE_CONSFFF_INFO

        query += CONDITION_CONSCODE_AND.replace(REPLACE_CONSCODE, consCode)
        query += CONDITION_COCODE_AND.replace(REPLACE_COCODE, coCode)
        query += CONDITION_FFPLANCODE_AND.replace(
            REPLACE_FFPLANCODE, ffPlan["ff_plan_code"]
        )

        return query

    # 소방시설공사 정보를 조회 한다.
    #
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- loginUserInfo | Object | 사용자 정보
    def sGetFFPlan(self, consCode, userInfo):
        query = SELECT_CONSFFF_INFO

        query += CONDITION_CONSCODE_AND_NAME_A.replace(REPLACE_CONSCODE, consCode)

        if (
            (userInfo["authority_code"] == constants.USER_AUTH_CONTRACTOR)
            or (userInfo["authority_code"] == constants.USER_AUTH_CONTRACTOR_MONITOR)
            or (userInfo["authority_code"] == constants.USER_AUTH_CONTRACTION)
        ):
            query += CONDITION_COCODE_AND_NAME_A.replace(
                REPLACE_COCODE, userInfo["co_code"]
            )

        return query

    # 공종에 따른 세부 공종 리스트를 조회 한다.
    #
    # Parameter
    # 	- constrCode | String | 공사 종류 코드
    def sGetDetailConstrList(self, constrCode):
        query = SELECT_DETAILCONSTR_INFO

        query += CONDITION_CNOSTRCODE_AND_NAME_A.replace(REPLACE_CONSTRCODE, constrCode)

        return query

    # 세부 공종에 따른 체크 리스트를 조회 한다.
    #
    # Parameter
    # 	- constrCode | String | 공사 종류 코드
    # 	- detailConstrCode | String | 세부공사 종류 코드
    def sGetCheckList(self, constrCode, detailConstrCode):
        query = SELECT_CHECKlIST_INFO

        query += CONDITION_CNOSTRCODE_AND_NAME_A.replace(REPLACE_CONSTRCODE, constrCode)
        query += CONDITION_DETAILCNOSTRCODE_AND_NAME_A.replace(
            REPLACE_DETAILCONSTRCODE, detailConstrCode
        )

        return query

    # 프로젝트 공종의 체크 리스트를 삭제 한다.
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- coCode | String | 회사 코드
    def dDelProjDetectionChkList(self, consCode, coCode, constrTypeCode):
        query = DELETE_PROJDETECTIONCHKLIST_INFO

        query += CONDITION_CONSCODE_AND.replace(REPLACE_CONSCODE, consCode)
        query += CONDITION_COCODE_AND.replace(REPLACE_COCODE, coCode)
        query += CONDITION_CNOSTRCODE_AND.replace(REPLACE_CONSTRCODE, constrTypeCode)

        return query

    # 프로젝트의 공종별/회사별/세부공종 별 체크 리스트를 추가 한다.
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- coCode | String | 회사 코드
    # 	- constrCode | String | 공사종류
    # 	- detailConstrCode | String | 세부공사종류
    # 	- chkMsg | String | 체크메시지
    # 	- inspCritCode | String | 검사기준
    def iPutProjDetectionChkList(
        self, consCode, coCode, constrCode, detailConstrCode, chkMsg, inspCritCode
    ):
        query = INSERT_PROJDETECTIONCHKLIST_INFO

        query += "VALUES("
        query += '"' + consCode + '", '
        query += '"' + coCode + '", '
        query += '"' + constrCode + '", '
        query += '"' + detailConstrCode + '", '
        query += '"' + chkMsg + '", '
        query += '"' + inspCritCode + '"'
        query += ")"

        return query

    # 프로젝트별-획사별-공종별 체크 리스트를 추가 가져온다.
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- coCode | String | 회사 코드
    # 	- constrCode | String | 공종 코드
    def sGetProjDetectionChkList(self, consCode, coCode, constrCode):
        query = SELECT_PROJDETECTIONCHKLIST_INFO

        query += CONDITION_CONSCODE_AND.replace(REPLACE_CONSCODE, consCode)
        query += CONDITION_COCODE_AND.replace(REPLACE_COCODE, coCode)
        query += CONDITION_CNOSTRCODE_AND_NAME_A.replace(REPLACE_CONSTRCODE, constrCode)

        query += " ORDER BY A.DETAIL_CONSTR_TYPE_CD, A.CHK_MSG ASC"

        return query

    # 프로젝트 참여 인력 수를 조회 한다.
    # Parameter
    # 	- type | Integer | 시공 or 감리
    # 	- coCode | String | 회사 코드
    def sGetAreaProjPartManpStatusP(self, type, coCode):
        query = SELECT_AREAPROJLISTP_INFO.replace(REPLACE_COCODE, coCode)

        if type == 1:
            query = query.replace(
                REPLACE_JOBTITLECODE, '"JT000000", "JT000001", "JT000002"'
            )
        else:
            query = query.replace(
                REPLACE_JOBTITLECODE, '"JT000004", "JT000005", "JT000006"'
            )

        return query

    # 프로젝트 참여 인력 기업 수를 조회 한다.
    # Parameter
    # 	- type | Integer | 시공 or 감리
    # 	- coCode | String | 회사 코드
    def sGetAreaProjPartManpStatusC(self, type, coCode):
        query = SELECT_AREAPROJLISTC_INFO.replace(REPLACE_COCODE, coCode)

        if type == 1:
            query = query.replace(
                REPLACE_JOBTITLECODE, '"JT000000", "JT000001", "JT000002"'
            )
        else:
            query = query.replace(
                REPLACE_JOBTITLECODE, '"JT000004", "JT000005", "JT000006"'
            )

        return query

    # 공사 기본 정보를 갱신 한다.
    # Parameter
    # 	- dataInfo | Object | 공사 기본 정보
    def uUpdateProjDefaultInfo(self, consCode, dataInfo, typeFlag):
        query = UPDATE_PROJECTDEFAULT_INFO

        index = 0

        if "cons_name" in dataInfo:
            query += 'CONS_NAME = "' + dataInfo["cons_name"] + '"'
            index += 1

        if typeFlag == "U":
            if dataInfo["location"] != "":
                if index > 0:
                    query += ", "

                query += 'LOCATION = "' + dataInfo["location"] + '"'
                index += 1
        else:
            query += 'LOCATION = "' + dataInfo["location"] + '"'

        if typeFlag == "U":
            if dataInfo["cons_type"] != "":
                if index > 0:
                    query += ", "

                query += 'CONS_TYPE = "' + dataInfo["cons_type"] + '"'
                index += 1
        else:
            query += ', CONS_TYPE = "' + dataInfo["cons_type"] + '"'

        if typeFlag == "U":
            if dataInfo["purpose"] != "":
                if index > 0:
                    query += ", "

                query += 'PURPOSE = "' + dataInfo["purpose"] + '"'
                index += 1
        else:
            query += ', PURPOSE = "' + dataInfo["purpose"] + '"'

        if typeFlag == "U":
            if dataInfo["building_name"] != "":
                if index > 0:
                    query += ", "

                query += 'BUILDING_NAME = "' + dataInfo["building_name"] + '"'
                index += 1
        else:
            query += ', BUILDING_NAME = "' + dataInfo["building_name"] + '"'

        if typeFlag == "U":
            if dataInfo["location_contact"] != "":
                if index > 0:
                    query += ", "

                query += 'LOCATION_CONTACT = "' + dataInfo["location_contact"] + '"'
                index += 1
        else:
            query += ', LOCATION_CONTACT = "' + dataInfo["location_contact"] + '"'

        if typeFlag == "U":
            if dataInfo["business_outline"] != "":
                if index > 0:
                    query += ", "

                query += 'BUSINESS_OUTLINE = "' + dataInfo["business_outline"] + '"'
                index += 1
        else:
            query += ', BUSINESS_OUTLINE = "' + dataInfo["business_outline"] + '"'

        if typeFlag == "U":
            if dataInfo["go_price"] != "":
                if index > 0:
                    query += ", "

                query += 'GO_PRICE = "' + str(dataInfo["go_price"]) + '"'
                index += 1
        else:
            query += ', GO_PRICE = "' + str(dataInfo["go_price"]) + '"'

        if typeFlag == "U":
            if dataInfo["design_price"] != "":
                if index > 0:
                    query += ", "

                query += 'DESIGN_PRICE = "' + str(dataInfo["design_price"]) + '"'
                index += 1
        else:
            query += ', DESIGN_PRICE = "' + str(dataInfo["design_price"]) + '"'

        if typeFlag == "U":
            if dataInfo["structure"] != "":
                if index > 0:
                    query += ", "

                query += 'STRUCTURE = "' + dataInfo["structure"] + '"'
                index += 1
        else:
            query += ', STRUCTURE = "' + dataInfo["structure"] + '"'

        if typeFlag == "U":
            if dataInfo["ground"] != "":
                if index > 0:
                    query += ", "

                query += 'GROUND = "' + str(dataInfo["ground"]) + '"'
                index += 1
        else:
            query += ', GROUND = "' + str(dataInfo["ground"]) + '"'

        if typeFlag == "U":
            if dataInfo["underground"] != "":
                if index > 0:
                    query += ", "

                query += 'UNDERGROUND = "' + str(dataInfo["underground"]) + '"'
                index += 1
        else:
            query += ', UNDERGROUND = "' + str(dataInfo["underground"]) + '"'

        if typeFlag == "U":
            if dataInfo["main_building"] != "":
                if index > 0:
                    query += ", "

                query += 'MAIN_BUILDING = "' + str(dataInfo["main_building"]) + '"'
                index += 1
        else:
            query += ', MAIN_BUILDING = "' + str(dataInfo["main_building"]) + '"'

        if typeFlag == "U":
            if dataInfo["sub_building"] != "":
                if index > 0:
                    query += ", "

                query += 'SUB_BUILDING = "' + str(dataInfo["sub_building"]) + '"'
                index += 1
        else:
            query += ', SUB_BUILDING = "' + str(dataInfo["sub_building"]) + '"'

        if typeFlag == "U":
            if dataInfo["households"] != "":
                if index > 0:
                    query += ", "

                query += 'HOUSEHOLDS = "' + str(dataInfo["households"]) + '"'
                index += 1
        else:
            query += ', HOUSEHOLDS = "' + str(dataInfo["households"]) + '"'

        if typeFlag == "U":
            if dataInfo["site_area"] != "":
                if index > 0:
                    query += ", "

                query += 'SITE_AREA = "' + dataInfo["site_area"] + '"'
                index += 1
        else:
            query += ', SITE_AREA = "' + dataInfo["site_area"] + '"'

        if typeFlag == "U":
            if dataInfo["building_area"] != "":
                if index > 0:
                    query += ", "

                query += 'BUILDING_AREA = "' + dataInfo["building_area"] + '"'
                index += 1
        else:
            query += ', BUILDING_AREA = "' + dataInfo["building_area"] + '"'

        if typeFlag == "U":
            if dataInfo["total_area"] != "":
                if index > 0:
                    query += ", "

                query += 'TOTAL_AREA = "' + dataInfo["total_area"] + '"'
                index += 1
        else:
            query += ', TOTAL_AREA = "' + dataInfo["total_area"] + '"'

        if typeFlag == "U":
            if dataInfo["floor_area"] != "":
                if index > 0:
                    query += ", "

                query += 'FLOOR_AREA = "' + dataInfo["floor_area"] + '"'
                index += 1
        else:
            query += ', FLOOR_AREA = "' + dataInfo["floor_area"] + '"'

        if typeFlag == "U":
            if dataInfo["add_info"] != "":
                if index > 0:
                    query += ", "

                query += 'ADD_INFO = "' + dataInfo["add_info"] + '"'
                index += 1
        else:
            query += ', ADD_INFO = "' + dataInfo["add_info"] + '"'

        if typeFlag == "U":
            if dataInfo["cons_start_date"] != "":
                if index > 0:
                    query += ", "

                query += 'CONS_START_DATE = "' + dataInfo["cons_start_date"] + '"'
                index += 1
        else:
            query += ', CONS_START_DATE = "' + dataInfo["cons_start_date"] + '"'

        if typeFlag == "U":
            if dataInfo["cons_end_date"] != "":
                if index > 0:
                    query += ", "

                query += 'CONS_END_DATE = "' + dataInfo["cons_end_date"] + '"'
                index += 1
        else:
            query += ', CONS_END_DATE = "' + dataInfo["cons_end_date"] + '"'

        query += ' WHERE CONS_CODE = "' + consCode + '"'

        if typeFlag == "U":
            if index == 0:
                return ""

        return query

    # 공사 기본 정보를 조회 한다.
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    def sGetProjDefaultInfo(self, consCode):
        query = SELECT_PROJECT_INFO

        query += CONDITION_CONSCODE_AND_NAME_A.replace(REPLACE_CONSCODE, consCode)

        return query

    # 감리 기본 정보를 저장 한다.
    # Parameter
    # 	- dataInfo | Object | 감리 기본 정보
    """
    def uUpdateSupvDefaultInfo(self, consCode, dataInfo, typeFlag):
        query = UPDATE_PROJECTDEFAULT_INFO

        index = 0
        if typeFlag == "U":
            if dataInfo["reside_class_code"] != "":
                query += 'RESIDE_CLASS_CODE = "' + dataInfo["reside_class_code"] + '"'
                index += 1
        else:
            query += 'RESIDE_CLASS_CODE = "' + dataInfo["reside_class_code"] + '"'

        if typeFlag == "U":
            if dataInfo["superv_contract_date"] != "":
                if index > 0:
                    query += ", "

                query += (
                    'SUPERV_CONTRACT_DATE = "' + dataInfo["superv_contract_date"] + '"'
                )
                index += 1
        else:
            query += (
                ', SUPERV_CONTRACT_DATE = "' + dataInfo["superv_contract_date"] + '"'
            )

        if typeFlag == "U":
            if dataInfo["superv_price"] != "":
                if index > 0:
                    query += ", "

                query += 'SUPERV_PRICE = "' + dataInfo["superv_price"] + '"'
                index += 1
        else:
            query += ', SUPERV_PRICE = "' + dataInfo["superv_price"] + '"'

        if typeFlag == "U":
            if dataInfo["superv_start_date"] != "":
                if index > 0:
                    query += ", "

                query += 'SUPERV_START_DATE = "' + dataInfo["superv_start_date"] + '"'
                index += 1
        else:
            query += ', SUPERV_START_DATE = "' + dataInfo["superv_start_date"] + '"'

        if typeFlag == "U":
            if dataInfo["superv_end_date"] != "":
                if index > 0:
                    query += ", "

                query += 'SUPERV_END_DATE = "' + dataInfo["superv_end_date"] + '"'
                index += 1
        else:
            query += ', SUPERV_END_DATE = "' + dataInfo["superv_end_date"] + '"'

        # query += 'WHERE CONS_CODE = "'			+ dataInfo['cons_code']				+ '"'
        query += 'WHERE CONS_CODE = "' + consCode + '"'

        if typeFlag == "U":
            if index == 0:
                return ""

        return query
    """
    # 시공 기본 정보를 저장 한다.
    # Parameter
    # 	- dataInfo | Object | 시공 기본 정보
    def iPutContDefaultInfo(self, dataInfo):
        query = INSERT_CONTRACTORSBASIC_INFO

        query += "VALUES("
        query += '"' + dataInfo["cons_code"] + '", '
        query += '"' + dataInfo["co_code"] + '", '
        query += '"' + dataInfo["contract_date"] + '", '
        query += '"' + dataInfo["completion_date"] + '", '
        query += '"' + dataInfo["sub_contract_price"] + '", '
        query += '"' + dataInfo["start_date"] + '", '
        query += '"' + dataInfo["bidroping"] + '", '
        query += '"' + dataInfo["bidway"] + '", '
        query += '"' + dataInfo["proc_details_path"] + '", '
        query += '"' + dataInfo["proc_details_original_name"] + '", '
        query += '"' + dataInfo["proc_details_change_name"] + '" '
        query += ")"

        return query

    # 공정상세 내역서 기준 정보를 저장 한다.
    def iPutBaseOnProcDetails(
        self, consCode, coCode, constrTypeCode, materialNum, unitCode, dataInfo, regDate
    ):
        query = INSERT_BASEONPROCDETAILS_INFO

        query += "VALUES("
        query += '"' + consCode + '", '  # 프로젝트 코드
        query += '"' + coCode + '", '  # 회사 코드
        query += '"' + constrTypeCode + '", '  # 공종 코드
        # query += u'"' + str(materialNum) + u'", '				# 자재 코드
        query += '"' + dataInfo["mat_nm_info"] + '", '  # 자재명
        query += '"' + dataInfo["mat_st_info"] + '", '  # 규격
        query += '"' + unitCode + '", '  # 단위
        query += '"' + str(dataInfo["mat_cu_info"]) + '", '  # 자재 총 개수
        query += '"' + str(dataInfo["mat_cs_info"]) + '", '  # 자재 단가
        query += '"' + str(dataInfo["mat_to_info"]) + '", '  # 자재 총 비용
        query += '"' + regDate + '"'  # 등록 날짜
        query += ")"

        return query

    # 공정상세 내역서 기준 직종별 정보를 저장 한다.
    def iPutBaseOnOccupationDetails(
        self, consCode, coCode, constrTypeCode, occCode, unitCode, dataInfo, regDate
    ):
        query = INSERT_BASEONOCCUPATIONDETAILS_INFO

        query += "VALUES("
        query += '"' + consCode + '", '
        query += '"' + coCode + '", '
        query += '"' + constrTypeCode + '", '
        query += '"' + occCode + '", '
        query += '"' + dataInfo["mat_nm_info"] + '", '
        query += '"' + dataInfo["mat_st_info"] + '", '
        query += '"' + unitCode + '", '  # 단위
        query += '"' + str(dataInfo["mat_cu_info"]) + '", '  # 직종별 인부 총 인원
        query += '"' + str(dataInfo["mat_cs_info"]) + '", '  # 직종별 단가
        query += '"' + str(dataInfo["mat_to_info"]) + '", '  # 직종별 총 비용
        query += '"' + regDate + '"'  # 등록 날짜
        query += ")"

        return query

    # 시공 기본 정보를 수정 한다.
    # Parameter
    # 	- dataInfo | Object | 시공 기본 정보
    def uModifyContDefaultInfo(self, dataInfo):
        query = UPDATE_CONTRACTORSBASIC_INFO

        query += 'CONTRACT_DATE = "' + dataInfo["contract_date"] + '", '
        query += 'COMPLETION_DATE = "' + dataInfo["completion_date"] + '", '
        query += 'SUB_CONTRACT_PRICE = "' + dataInfo["sub_contract_price"] + '", '
        query += 'START_DATE = "' + dataInfo["start_date"] + '", '
        query += 'BIDROPING = "' + dataInfo["bidroping"] + '", '
        query += 'BIDWAY = "' + dataInfo["bidway"] + '" '

        if dataInfo["proc_details_status"] == "C":
            query += ',PROC_DETAILS_PATH = "' + dataInfo["proc_details_path"] + '", '
            query += (
                'PROC_DETAILS_ORIGINAL_NAME = "'
                + dataInfo["proc_details_original_name"]
                + '", '
            )
            query += (
                'PROC_DETAILS_CHANGE_NAME  = "'
                + dataInfo["proc_details_change_name"]
                + '" '
            )
        elif dataInfo["proc_details_status"] == "D":
            query += ',PROC_DETAILS_PATH = ""'
            query += 'PROC_DETAILS_ORIGINAL_NAME = ""'
            query += 'PROC_DETAILS_CHANGE_NAME  = ""'

        query += 'WHERE CONS_CODE = "' + dataInfo["cons_code"] + '" '
        query += 'AND CO_CODE = "' + dataInfo["co_code"] + '" '

        return query

    # 공정상세 내역서 기준 정보를 삭제 한다.
    def dDelBaseOnProcDetails(self, consCode, coCode):
        query = DELETE_BASEONPROCDETAILS_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += 'AND CO_CODE  = "' + coCode + '" '

        return query

    # 감리 기본 정보를 조회 한다.
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    def sGetSupvDefaultInfo(self, consCode):
        query = SELECT_SUPVDEFAULT_INFO

        query += CONDITION_CONSCODE_AND_NAME_A.replace(REPLACE_CONSCODE, consCode)

        return query

    # 시공사 기본 정보를 조회 한다.
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- coCode | String | 회사 코드
    def sGetContDefaultInfo(self, consCode, coCode):
        query = SELECT_CONTDEFAULT_INFO

        query += CONDITION_CONSCODE_AND_NAME_A.replace(REPLACE_CONSCODE, consCode)

        if coCode != "":
            query += CONDITION_COCODE_AND_NAME_A.replace(REPLACE_COCODE, coCode)

        query += "ORDER BY co_name ASC"

        return query

    # 프로젝트 리스트를 조회 한다.
    # Parameter
    # 	- userId | String | 사용자 ID
    # 	- projectStatus | String | 프로젝트 상태 코드
    # def sGetProjectList(self, userId, projectStatus):
    def sGetProjectList(self, userInfo, projectStatus):
        query = SELECT_PROJECT_INFO

        if (
            userInfo["authority_code"] == constants.USER_MASTER
            or userInfo["authority_code"] == constants.USER_MONITOR
        ):
            query += (
                'AND A.CONS_CODE IN (SELECT CONS_CODE FROM JOIN_WORKFORCE WHERE CO_CODE = "'
                + userInfo["co_code"]
                + '") '
            )
            #query += 'AND A.SUPERV_CO_CODE = "' + userInfo["co_code"] + '"'

        #        elif (
        #            userInfo["authority_code"] == constants.USER_AUTH_BUYER
        #            or userInfo["authority_code"] == constants.USER_AUTH_DESIGNER
        #            or userInfo["authority_code"] == constants.USER_AUTH_CONTRACTION
        #            or userInfo["authority_code"] == constants.USER_AUTH_SUPERVISING
        #            or userInfo["authority_code"] == constants.USER_AUTH_WHITEHALL
        #            or userInfo["authority_code"] == constants.USER_AUTH_INOCCUPATION
        #        ):
        else:
            query += (
                'AND A.CONS_CODE IN (SELECT CONS_CODE FROM JOIN_WORKFORCE WHERE ID = "'
                + userInfo["id"]
                + '") '
            )
        #        elif (
        #            userInfo["authority_code"] == constants.USER_AUTH_CONTRACTOR
        #            or userInfo["authority_code"] == constants.USER_AUTH_CONTRACTOR_MONITOR
        #        ):
        #            query += (
        #                'AND A.CONS_CODE IN (SELECT DISTINCT CONS_CODE FROM JOIN_WORKFORCE WHERE CO_CODE = "'
        #                + userInfo["co_code"]
        #                + '") '
        #            )

        if projectStatus != constants.PROJECT_STATUS_CD_ALL:
            query += 'AND A.PROJECT_STATUS = "' + projectStatus + '" '

        query += " ORDER BY A.CONS_START_DATE DESC, A.CONS_NAME ASC"

        return query

    # 작업 일지 작성 기준 정보를 저장 한다.
    def iPutWorkLogWriteStandard(self, consCode, coCode, writeStandardCode):
        query = INSERT_WORKLOGWRITESTANDARD_INFO

        query += "VALUES("
        query += '"' + consCode + '", '
        query += '"' + coCode + '", '
        query += '"' + writeStandardCode + '"'
        query += ")"

        return query

    # 작업 일지 작성 기준 정보를 조회 한다.
    def sGetWorkLogWriSta(self, consCode, coCode):
        query = SELECT_WORKLOGWRITESTANDARD_INFO

        query += ' AND WLWS.CONS_CODE = "' + consCode + '"'
        query += ' AND WLWS.CO_CODE = "' + coCode + '"'

        return query

    # 작업 일지 작성 기준 정보를 수정 한다.
    def uModifyWorkLogWriSta(self, consCode, coCode, workLogWriSatCd):
        query = UPDATE_WORKLOGWRITESTANDARD_INFO

        query += ' WRITE_STANDARD_CD = "' + workLogWriSatCd + '" '

        query += "WHERE 1=1 "
        query += 'AND CONS_CODE = "' + consCode + '"'
        query += 'AND CO_CODE = "' + coCode + '"'

        return query

    @staticmethod
    def select_project_date(cons_code):
        query = SELECT_PROJECT_DATE.format(cons_code)

        return query

    # 프로젝트 이력 리스트를 조회 한다.
    def sGetProjectHistoryList(self, userInfo):
        query = SELECT_PROJECT_INFO

        query += (
            ' AND A.CONS_CODE IN (SELECT CONS_CODE FROM JOIN_WORKFORCE WHERE ID = "'
            + userInfo["id"]
            + '")'
        )
        query += (
            ' AND (A.CONS_START_DATE > "'
            + userInfo["co_appro_date"]
            + '" OR A.CONS_END_DATE > "'
            + userInfo["co_appro_date"]
            + '")'
        )

        #        query += (
        #            'AND A.CONS_CODE IN (SELECT CONS_CODE FROM CONTRACTORS_BASIC_INFO WHERE CONS_CODE IN (SELECT CONS_CODE FROM JOIN_WORKFORCE WHERE ID = "'
        #            + userInfo["id"]
        #            + '") AND COMPLETION_DATE > "'
        #            + userInfo["co_appro_date"]
        #            + '") '
        #        )

        query += "ORDER BY A.CONS_CODE ASC"

        return query

    def dDelDocNumManage(self, projCd, coCode):
        query = DELETE_DOCNUMMANAGE_INFO

        query += CONDITION_CONSCODE_AND.replace(REPLACE_CONSCODE, projCd)
        query += CONDITION_COCODE_AND.replace(REPLACE_COCODE, coCode)

        return query

    # 프로젝트 중지 이력을 저장 한다.
    def iPutProjStopHis(self, dataInfo):

        query = INSERT_PROJSTOPHIS_INFO
        query += "VALUES( "
        query += '"' + dataInfo["cons_code"] + '",'
        query += '"' + dataInfo["proj_stop_date"] + '",'
        query += '"' + dataInfo["proj_stop_cause"] + '",'
        query += '"' + dataInfo["proj_stop_reg_date"] + '",'
        query += '"' + dataInfo["req_co_code"] + '",'
        query += '"' + dataInfo["req_id"] + '",'
        query += '"' + dataInfo["proj_stop_appro_date"] + '"'
        query += ")"

        return query

    # 프로젝트 중지 이력을 삭제 한다.
    def dDelProjStopHis(self, dataInfo):
        query = DELETE_PROJSTOPHIS_INFO

        query += 'AND CONS_CODE = "' + dataInfo["cons_code"] + '"'
        query += 'AND PROJ_STOP_REG_DATE = "' + dataInfo["proj_stop_reg_date"] + '"'

        return query

    # 프로젝트  정보를 업데이트 한다.
    def uUpdateProjInfo(self, consCode, updateInfoList):
        query = UPDATE_PROJECTDEFAULT_INFO
        index = 0
        listSize = len(updateInfoList)
        for updateInfo in updateInfoList:
            if listSize > 1:
                if index < listSize - 1:
                    query += updateInfo["key"] + ' = "' + updateInfo["value"] + '", '
                else:
                    query += updateInfo["key"] + ' = "' + updateInfo["value"] + '" '

                index += 1
            else:
                query += updateInfo["key"] + ' = "' + updateInfo["value"] + '" '

        query += 'WHERE CONS_CODE = "' + consCode + '"'
        return query

    # 프로젝트  중지 이력 정보를 업데이트 한다.
    def uUpdateProjRestartHis(self, dataInfo):
        query = UPDATE_PROJSTOPHIS_INFO

        query += 'PROJ_RESTART_DATE = "' + dataInfo["proj_restart_date"] + '" '

        query += 'WHERE CONS_CODE = "' + dataInfo["cons_code"] + '"'
        query += "AND PROJ_RESTART_DATE IS NULL"

        return query

    # 조현우 추가 프로젝트의 상태를 가져온다
    def select_project_status(self, cons_code):
        query = SELECT_PROJECT_STATUS_INFO.format(CONSCODE_CONDITION.format(cons_code))

        return query

    # 조현우 추가 프로젝트의 상태를 가져온다
    def select_project_status_by_sysdocnum(self, sys_doc_num):
        query = SELECT_SYSDOCNUM_PROJECT_STATUS_INFO.format(
            SYSDOCNUM_CONDITION_D.format(sys_doc_num)
        )

        return query

    # 조현우 프로젝트 인력의 참여 시작일을 변경한다
    def update_join_workforce_start_date(self, cons_code, id, start_date):
        query = UPDATE_WORKFORCE_STARTDATE_INFO.format(
            start_date,
            CONSCODE_CONDITION.format(cons_code) if cons_code else "",
            ID_CONDITION.format(id),
        )
        return query

    # 조현우 프로젝트 인력의 참여 종료일을 변경한다
    def update_join_workforce_end_date(self, cons_code, id, end_date):
        query = UPDATE_WORKFORCE_ENDDATE_INFO.format(
            end_date,
            CONSCODE_CONDITION.format(cons_code) if cons_code else "",
            ID_CONDITION.format(id),
        )
        return query

    # 조현우 인력추가
    def insert_join_workforce(
        self, cons_code, id, authority_code, co_code, start_date, end_date
    ):
        query = INSERT_WORKFORCE.format(
            cons_code, id, authority_code, co_code, start_date, end_date
        )
        return query

    # 조현우 인력 기간수정
    def update_join_workforce(self, cons_code, id, date, start_date, end_date):
        query = UPDATE_WORKFORCE.format(
            "START_DATE = '{}', END_DATE = '{}'".format(start_date, end_date)
            if start_date and end_date
            else " ".join(
                [
                    "START_DATE = '{}'".format(start_date) if start_date else "",
                    "END_DATE = '{}'".format(end_date) if end_date else "",
                ]
            ),
            CONSCODE_CONDITION.format(cons_code),
            ID_CONDITION.format(id),
            STARTDATE_CONDITION.format(date),
        )
        return query

    # 조현우 인력 삭제
    def delete_join_workforce(self, cons_code, id, date):
        query = DELETE_WORKFORCE.format(
            CONSCODE_CONDITION.format(cons_code),
            ID_CONDITION.format(id),
            STARTDATE_CONDITION.format(date) if date else "",
        )
        return query
