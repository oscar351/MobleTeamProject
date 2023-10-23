# _*_coding: utf-8 -*-

# 사용자 관리 Query Class
# 작성 날짜 : 2022. 7. 29
# 작성자 : 황희정
# 기능
# 	1. 2022. 07. 29 | 사용자 정보를 Read 한다.
# 	2. 2022. 07. 29 | 사용자 로그인 정보를 업데이트 한다.
# 	3. 2022. 07. 29 | 사용자 로그아웃 정보를 업데이터 한다.
# 	4. 2022. 08. 02 | 사용자 로그인 정보를 체크 한다.
# 변경 이력
# 	1. 2022. 07. 29 | 황희정 | 최조 작성
# 	2. 2022. 08. 02 | 황희정 | 추가 | 사용자 로그인 정보를 Return 한다.
# 	3. 2022. 08. 03 | 황희정 | 수정 | 필요한 Function에 시스템 코드 추가

import sys

from common import constants
from common.commUtilService import commUtilService

# 							A.WEB_TOKEN						AS web_token,
# 							A.APP_TOKEN						AS app_token,
# 							(SELECT CO_NAME FROM COMPANY WHERE CO_CODE = A.CO_CODE) AS co_name,
SELECT_INFO_USER = """
	SELECT 
		A.ID							AS id, 
		A.AUTHORITY_CODE				AS authority_code, 
		(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.AUTHORITY_CODE) AS authority_name,
		A.PASSWORD						AS password, 
		A.USER_NAME						AS user_name, 
		A.USER_POSITION					AS user_position, 
		A.USER_CONTACT					AS user_contact, 
		A.USER_EMAIL					AS user_email, 
		A.USER_STATE					AS user_state, 
		(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.USER_STATE) AS user_state_name,
		A.USE_TYPE						AS use_type, 
		A.JOIN_DATE						AS join_date,
		A.APPRO_DATE					AS appro_date,
		A.CO_APPRO_DATE					AS co_appro_date,
		IFNULL(A.CO_CODE, '')						AS co_code,
		IFNULL(CIM.CO_NAME,'')						AS co_name,
		IFNULL(CIM.CO_TYPE, '')					AS co_type,
		IFNULL(CIM.CEO, '')				AS co_ceo,
		IFNULL(CIM.CONTACT, '')			AS co_contact,
		IFNULL(CIM.ADDRESS, '')					AS co_address,
		IFNULL(CIM.REGISNUM, '')					AS co_regisnum,
		IFNULL(A.MANAGER_TYPE, '')		AS manager_type
	FROM USER A LEFT OUTER JOIN COMPANY CIM ON A.CO_CODE = CIM.CO_CODE
	WHERE 1 = 1
	"""

SELECT_COUNT_USER = "SELECT COUNT(*) AS cnt FROM USER WHERE 1=1 "

UPDATE_USER_TABLE = "UPDATE USER SET "

UPDATE_USERFILE_TABLE = "UPDATE USER_FILE SET "

INSERT_USER_INFO = """INSERT INTO USER(
							ID,
							AUTHORITY_CODE,
							PASSWORD,
							USER_NAME,
							USER_POSITION,
							USER_CONTACT,
							USER_EMAIL,
							JOIN_DATE,
							CO_CODE
							)
						"""
INSERT_USERFILE_INFO = """INSERT INTO USER_FILE(
								ID,
								USER_LICENSE_PATH,
								USER_LICENSE_ORIGINAL_NAME,
								USER_LICENSE_CHANGE_NAME,
								SIGN_PATH,
								SIGN_ORIGINAL_NAME,
								SIGN_CHANGE_NAME
								)
							"""
INSERT_FIELDRATING_INFO = """INSERT INTO FIELD_RATING(
								ID,
								FIELD,
								RATING
								)
							"""
INSERT_COINFOMANAGE_INFO = """INSERT INTO COMPANY(
									CO_CODE,
									NAME,
									TYPE,
									CEO,
									CONTACT,
									ADDRESS,
									REGISNUM,
									)
								"""

SELECT_COINFOMANAGE_INFO = """SELECT 
									CO_CODE		AS co_code, 
									CO_NAME		AS co_name, 
									CO_TYPE		AS co_type, 
									CEO			AS co_ceo, 
									CONTACT		AS co_contact, 
									ADDRESS		AS co_address, 
									REGISNUM	AS co_regisnum
								FROM COMPANY
								WHERE 1 = 1
								"""


SELECT_FILEDRATING_INFO = """SELECT
								ID AS id,
								FIELD AS field,
								(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = FIELD) AS field_name,
								RATING as rating,
								(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = RATING) AS rating_name
							FROM
								FIELD_RATING
							WHERE
								1 = 1
							"""

SELECT_COMPANYUSER_INFO = """
	SELECT
		U_S.ID AS id, U_S.USER_NAME AS user_name, U_S.USER_CONTACT AS user_contact, 
		U_S.AUTHORITY_CODE AS authority_code, U_S.AUTHORITY_NAME AS authority_name,
		U_S.USE_TYPE AS use_type,
		U_S.CO_CODE AS co_code, U_S.CO_NAME AS co_name,
		U_S.USER_EMAIL AS user_email, U_S.USER_STATE AS user_state, U_S.USER_STATE_NAME AS user_state_name, U_S.MANAGER_TYPE AS manager_type,
		JWP_S.CONS_CODE AS cons_code, JWP_S.CONS_NAME AS cons_name,
		JWP_S.JOB_TITLE_CODE AS job_title_code, JWP_S.JOB_TITLE_NAME AS job_title_name
	FROM 
		(
			SELECT 
				U.ID, U.USER_NAME, U.USER_CONTACT, 
				U.AUTHORITY_CODE, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = U.AUTHORITY_CODE) AS AUTHORITY_NAME,
				U.USE_TYPE, U.USER_EMAIL, U.MANAGER_TYPE,
				U.USER_STATE, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = U.USER_STATE) AS USER_STATE_NAME,
				U.CO_CODE, (SELECT CO_NAME FROM COMPANY WHERE CO_CODE = U.CO_CODE) AS CO_NAME
			FROM USER U
			WHERE 1=1
			{1}
			ORDER BY U.AUTHORITY_CODE, U.USER_NAME ASC
		) U_S 
		LEFT OUTER JOIN 
		(
			SELECT
				JW_S.ID, JW_S.CONS_CODE, P_S.CONS_NAME,
				JW_S.JOB_TITLE_CODE, JW_S.JOB_TITLE_NAME
			FROM 
				(
					SELECT 
						JW.ID, JW.CONS_CODE, 
						JW.JOB_TITLE_CODE, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = JW.JOB_TITLE_CODE) AS JOB_TITLE_NAME
					FROM JOIN_WORKFORCE JW
					WHERE 1=1
					{2}
					ORDER BY JW.CONS_CODE ASC
				) JW_S,
				(
					SELECT 
						CONS_CODE, CONS_NAME
					FROM PROJECT
					WHERE 1=1
					AND PROJECT_STATUS IN ("ST000001","ST000002")
					ORDER BY CONS_CODE ASC
				) P_S
			WHERE 1=1
			AND JW_S.CONS_CODE = P_S.CONS_CODE
		) JWP_S ON U_S.ID = JWP_S.ID
	ORDER BY U_S.USER_NAME ASC
"""


DELETE_USER_INFO = """DELETE FROM USER WHERE 1=1 """
DELETE_USERFILE_INFO = """DELETE FROM USER_FILE WHERE 1=1 """
DELETE_FIELDRATING_INFO = """DELETE FROM FIELD_RATING WHERE 1=1 """


CONDITION_APPTOKEN_AND = 'AND APP_TOKEN	= "{appToken}" '
CONDITION_WEBTOKEN_AND = 'AND WEB_TOKEN	= "{webToken}" '
CONDITION_USERID_AND = 'AND ID			= "{userId}" '
CONDITION_USERNAME_AND = 'AND USER_NAME	= "{user_name}" '
CONDITION_USEREMAIL_AND = 'AND USER_EMAIL	= "{user_email}" '
CONDITION_CONAME_AND = 'AND CO_NAME		= "{co_name}" '
CONDITION_COCODE_AND = 'AND CO_CODE		= "{co_code}" '
CONDITION_AUTHORITY_AND = 'AND AUTHORITY_CODE	= "{authority_code}" '

SELECT_COMPANYUSER_INFO_COMPANY_AND_1 = 'AND U.CO_CODE = "{co_code}"'
SELECT_COMPANYUSER_INFO_USER_AND_1 = 'AND U.ID = "{userId}"'
SELECT_COMPANYUSER_INFO_COMPANY_AND_2 = (
    'AND JW.ID IN ( SELECT ID FROM USER WHERE CO_CODE = "{co_code}")'
)
SELECT_COMPANYUSER_INFO_USER_AND_2 = 'AND JW.ID = "{userId}"'

REPLACE_USERID = "{userId}"
REPLACE_USERNAME = "{user_name}"
REPLACE_USEREMAIL = "{user_email}"
REPLACE_WEBTOKEN = "{webToken}"
REPLACE_APPTOKEN = "{appToken}"
REPLACE_CONAME = "{co_name}"
REPLACE_COCODE = "{co_code}"
REPLACE_AUTHORITYCODE = "{authority_code}"

SELECT_USER_APPROVALS = " ".join([
    "SELECT",
    "0 as type,",
    "AB.NUMBER as number,"
    "HEX(AB.UUID) as uuid",
    "FROM APPROVAL_BOARD AB",
    "JOIN APPROVAL_BOARD_INFO AF",
    "ON AB.UUID = AF.POST_UUID AND AB.APR_INDEX = AF.APR_INDEX AND AF.APR_TYPE_CODE IN ('AT000002', 'AT000003') AND AF.USER_ID = %s",
    "WHERE AB.CONS_CODE = '{}' AND AF.APPROVED is NULL",
    "UNION",
    "SELECT",
    "1 as type,",
    "RB.NUMBER as number,"
    "HEX(RB.UUID) as uuid",
    "FROM REQUEST_BOARD RB",
    "JOIN REQUEST_BOARD_INFO RF",
    "ON RB.UUID = RF.POST_UUID AND RB.APR_INDEX = RF.APR_INDEX AND RF.APR_TYPE_CODE IN ('AT000002', 'AT000003') AND RF.USER_ID = %s",
    "WHERE RB.CONS_CODE = '{}' AND RF.APPROVED IS NULL",
    "ORDER BY type, number DESC"
])
# 사용자 관리 Query Class
class sqlUserManage:

    # 1. 사용자 정보를 Read 한다.
    #
    # Parameter
    # 	- type | Integer | 1 = userId, 2 = userToken
    # 	- typeData | String | userId or userToken
    # 	- sysCd | String | system code
    def sGetUserInfo(self, type, typeData, sysCd):
        query = SELECT_INFO_USER

        if type == 1:
            query += (
                'AND A.ID = "' + REPLACE_USERID.replace(REPLACE_USERID, typeData) + '" '
            )
        elif type == 2:
            if sysCd == constants.SYS_CODE_APP:
                query += (
                    'AND A.APP_TOKEN = "'
                    + REPLACE_APPTOKEN.replace(REPLACE_APPTOKEN, typeData)
                    + '" '
                )
            elif sysCd == constants.SYS_CODE_WEB:
                query += (
                    'AND A.WEB_TOKEN = "'
                    + REPLACE_WEBTOKEN.replace(REPLACE_WEBTOKEN, typeData)
                    + '" '
                )
            else:
                query += (
                    'AND A.WEB_TOKEN = "'
                    + REPLACE_WEBTOKEN.replace(REPLACE_WEBTOKEN, typeData)
                    + '" '
                )

        return query

    def sGetCondictionUserInfo(self, auth, coCode):
        query = SELECT_INFO_USER

        query += CONDITION_AUTHORITY_AND.replace(REPLACE_AUTHORITYCODE, auth)
        query += CONDITION_COCODE_AND.replace(REPLACE_COCODE, coCode)

        return query

    # 2. 사용자 로그인 정보를 업데이트 한다.
    #
    # Parameter
    # 	- userId | String | 사용자 ID
    # 	- userToken | String | 사용자 Token
    # 	- sysCd | String | system code
    def uUserLogin(self, userId, userToken, sysCd):
        query = UPDATE_USER_TABLE

        if sysCd == constants.SYS_CODE_APP:
            query += 'APP_TOKEN = "' + userToken
        elif sysCd == constants.SYS_CODE_WEB:
            query += 'WEB_TOKEN = "' + userToken
        else:
            query += 'WEB_TOKEN = "' + userToken

        query += '" WHERE 1 = 1 ' + CONDITION_USERID_AND.replace(REPLACE_USERID, userId)

        return query

    # 3. 사용자 로그아웃 정보를 업데이트 한다.
    #
    # Parameter
    # 	- userToken | String | 사용자 token
    # 	- sysCd | String | system code
    def uUserLogout(self, userToken, sysCd):
        query = UPDATE_USER_TABLE

        if sysCd == constants.SYS_CODE_APP:
            query += "APP_TOKEN = NULL WHERE 1 = 1 "
        elif sysCd == constants.SYS_CODE_WEB:
            query += "WEB_TOKEN = NULL WHERE 1 = 1 "
        else:
            query += "WEB_TOKEN = NULL WHERE 1 = 1 "

        if sysCd == constants.SYS_CODE_APP:
            query += CONDITION_APPTOKEN_AND.replace(REPLACE_APPTOKEN, userToken)
        elif sysCd == constants.SYS_CODE_WEB:
            query += CONDITION_WEBTOKEN_AND.replace(REPLACE_WEBTOKEN, userToken)
        else:
            query += CONDITION_WEBTOKEN_AND.replace(REPLACE_WEBTOKEN, userToken)

        return query

    # 4. 사용자 로그인 했는지 여부를 Return 한다.
    #
    # Parameter
    # 	- userToken | String | 사용자 token
    # 	- sysCd | String | system code
    def sChkUserLoginInfo(self, userToken, sysCd):
        query = SELECT_COUNT_USER

        if sysCd == constants.SYS_CODE_APP:
            query += CONDITION_APPTOKEN_AND.replace(REPLACE_APPTOKEN, userToken)
        elif sysCd == constants.SYS_CODE_WEB:
            query += CONDITION_WEBTOKEN_AND.replace(REPLACE_WEBTOKEN, userToken)
        else:
            query += CONDITION_WEBTOKEN_AND.replace(REPLACE_WEBTOKEN, userToken)

        return query

    # 5. 사용자 ID 중복 여부를 Return 한다.
    #
    # Parameter
    # 	- userId | String | 사용자 ID
    def sChkUserId(self, userId):
        query = SELECT_COUNT_USER + CONDITION_USERID_AND.replace(REPLACE_USERID, userId)

        return query

    # 6. 사용자 정보를 저장한다.(사용자 등록)
    #
    # Parameter
    # 	- userInfo | Object | 사용자 정보
    def iPutUserInfo(self, userInfo):
        query = INSERT_USER_INFO

        query += "VALUES("
        query += '"' + userInfo["id"] + '", '
        query += '"' + userInfo["authority_code"] + '", '
        query += '"' + userInfo["password"] + '", '
        query += '"' + userInfo["user_name"] + '", '
        query += '"' + userInfo["user_position"] + '", '
        query += '"' + userInfo["user_contact"] + '", '
        query += '"' + userInfo["user_email"] + '", '
        query += '"' + userInfo["join_date"] + '", '
        query += '"' + userInfo["co_code"] + '"'
        query += ")"

        return query

    # 7. 사용자 파일 정보를 저장한다.
    #
    # Parameter
    # 	- fileInfo | Object | 파일 정보
    def iPutUserFileInfo(self, fileInfo):
        query = INSERT_USERFILE_INFO

        query += "VALUES("
        query += '"' + fileInfo["id"] + '", '
        query += '"' + fileInfo["user_license_path"] + '", '
        query += '"' + fileInfo["user_license_original_name"] + '", '
        query += '"' + fileInfo["user_license_change_name"] + '", '
        query += '"' + fileInfo["sign_path"] + '", '
        query += '"' + fileInfo["sign_original_name"] + '", '
        query += '"' + fileInfo["sign_change_name"] + '"'
        query += ")"

        return query

    # 8. 사용자 분야/등급을 저장한다.
    #
    # Parameter
    #    - fieldratingInfo | Array | 분야등급 정보
    def iPutUserFieldRatingInfo(self, userFieldRatingInfo):
        query = INSERT_FIELDRATING_INFO
        query += "VALUES"

        size = userFieldRatingInfo.__len__()

        # if(size == 0):
        # 	query += u'("' + ['id'] + u'", "", "")'
        # 	return query

        num = 0
        for data in userFieldRatingInfo:
            query += '("' + data["id"] + '", '
            query += '"' + data["field"] + '", '

            if num < size - 1:
                query += '"' + data["rating"] + '"),'
            else:
                query += '"' + data["rating"] + '")'

            num += 1

        return query

    # 9. 사용자를 테이블에서 삭제 한다.
    #
    # Parameter
    # 	- userId | String | 사용자 ID
    def dDelUserInfo(self, userId):
        query = DELETE_USER_INFO
        query += CONDITION_USERID_AND.replace(REPLACE_USERID, userId)

        return query

    # 10. 사용자 파일 정보를 테이블에서 삭제 한다.
    #
    # Parameter
    # 	- userId | String | 사용자 ID
    def dDelUserFileInfo(self, userId):
        query = DELETE_USERFILE_INFO
        query += CONDITION_USERID_AND.replace(REPLACE_USERID, userId)

        return query

    # 11. 등록된 회사를 검색 한다.
    # Parameter
    def sGetCoInfo(self, searchList):
        query = SELECT_COINFOMANAGE_INFO

        for searchInfo in searchList:
            query += " AND " + searchInfo["key"] + ' = "' + searchInfo["value"] + '"'

        return query

    # 13. 회사 정보 입력
    #
    # Parameter
    # 	- co_code_num | String | 회사 코드
    # 	- userInfo	  | Object | 사용자 정보
    def iSetCoCdNumber(self, co_code_num, userInfo):
        query = INSERT_COINFOMANAGE_INFO
        query += "VALUES"
        query += '("' + co_code_num + '", '
        query += '"' + userInfo["co_name"] + '", '
        query += '"' + userInfo["co_type"] + '", '
        query += '"' + userInfo["co_ceo"] + '", '
        query += '"' + userInfo["co_contact"] + '", '
        query += '"' + userInfo["co_address"] + '")'

        return query

    # 14. 사용자 테이블에 회사 코드를 업데이트 한다.
    #
    # Parameter
    # 	- co_code_num | String | 회사코드
    # 	- userId	  | String | 사용자 Id
    def uUpdateUserCoCdNum(self, co_code_num, userId):
        query = UPDATE_USER_TABLE

        query += 'CO_CODE = "' + co_code_num + '" WHERE 1 = 1 '
        query += CONDITION_USERID_AND.replace(REPLACE_USERID, userId)

        return query

    # 16. 등급/분야 데이터를 가져온다.
    #
    # Parameter
    # 	- type | int | 검색 구분
    # 	- id | String | 사용자 ID
    def sGetUserFieldRatingInfo(self, type, userId):
        query = SELECT_FILEDRATING_INFO

        if type == 1:
            query += CONDITION_USERID_AND.replace(REPLACE_USERID, userId)

        return query

    # 17. 내 정보 또는 회원 정보를 업데이트 한다.
    #
    # Parameter
    # 	- userInfo | Object | 사용자 정보
    # 	- type | Int | 권한 타입
    # def uModifyUserInfo(self, userInfo, type):
    def uUpdateUserInfo(self, userInfo):
        query = UPDATE_USER_TABLE
        # if(type == 2):	#  시스템 관리자
        query += 'password = "' + userInfo["password"] + '", '
        # 		query += u'user_position = "'	+ userInfo['user_position'] + u'", '
        query += 'user_contact = "' + userInfo["user_contact"] + '", '
        query += 'user_email = "' + userInfo["user_email"] + '" '

        if userInfo["authority_code"] != "":
            query += ', authority_code = "' + userInfo["authority_code"] + '" '

        if userInfo["user_position"] != "":
            query += ', user_position = "' + userInfo["user_position"] + '" '

        # 		query += u'user_state = "'		+ userInfo['user_state']		+ u'", '
        # 		query += u'use_type = "'		+ userInfo['use_type']			+ u'", '
        # 		query += u'user_type = "'		+ userInfo['user_type']			+ u'", '
        # 		query += u'employ_status = "'	+ userInfo['employ_status'] + u'", '
        # 		query += u'authority_code = "'	+ userInfo['authority_code']	+ u'" '

        # elif(type == 3):	# 시공사/감리자
        # if(userInfo['password'] != None and userInfo['password'] != ''):

        # 		if(userInfo['user_type'] == constants.USER_TYPE_CODE_ENTERPRISE):
        # 			query += u'co_type = "'		+ userInfo['co_type']		+ u'", '
        # 			query += u'co_regisnum = "' + userInfo['co_regisnum']	+ u'", '
        # 			query += u'regisnum = "'	+ userInfo['regisnum']		+ u'", '

        # 		query += u'co_name = "'			+ userInfo['co_name']		+ u'", '
        # 		query += u'co_ceo = "'			+ userInfo['co_ceo']		+ u'", '
        # 		query += u'co_address = "'		+ userInfo['co_address']	+ u'", '
        # 		query += u'co_contact = "'		+ userInfo['co_contact']	+ u'", '

        query += 'WHERE ID = "' + userInfo["id"] + '"'

        return query

    # 18. 분야/등급 정보를 삭제 한다.
    #
    # Parameter
    # 	- userId | String | 사용자 ID
    def dDelUserFieldRatingInfo(self, userId):
        query = DELETE_FIELDRATING_INFO
        query += CONDITION_USERID_AND.replace(REPLACE_USERID, userId)

        return query

    # 19. 파일 경로 정보를 수정 한다.
    #
    # Parameter
    # 	- userInfo | Object | 사용자 정보
    def uModifyFilePath(self, userInfo):
        query = UPDATE_USERFILE_TABLE

        query += 'CO_LICENSE_PATH = "' + userInfo["co_license_path"] + '", '
        query += 'BS_LICENSE_PATH = "' + userInfo["bs_license_path"] + '", '
        query += 'USER_LICENSE_PATH = "' + userInfo["user_license_path"] + '", '
        query += 'SIGN_PATH = "' + userInfo["sign_path"] + '" '
        query += "WHERE 1 = 1 "
        query += 'AND ID = "' + userInfo["id"] + '"'

        return query

    # 20. 파일 정보를 수정 한다.
    #
    # Parameter
    # 	- userInfo | Object | 사용자 정보
    def uUpdateUserFileInfo(self, userInfo):
        query = UPDATE_USERFILE_TABLE

        # 		query += u'CO_LICENSE_PATH = "'				+ userInfo['co_license_path']				+ '", '
        # 		query += u'CO_LICENSE_ORIGINAL_NAME = "'	+ userInfo['co_license_original_name']		+ '", '
        # 		query += u'CO_LICENSE_CHANGE_NAME = "'		+ userInfo['co_license_change_name']		+ '", '
        # 		query += u'BS_LICENSE_PATH = "'				+ userInfo['bs_license_path']				+ '", '
        # 		query += u'BS_LICENSE_ORIGINAL_NAME = "'	+ userInfo['bs_license_original_name']		+ '", '
        # 		query += u'BS_LICENSE_CHANGE_NAME = "'		+ userInfo['bs_license_change_name']		+ '", '
        query += 'USER_LICENSE_PATH = "' + userInfo["user_license_path"] + '", '
        query += (
            'USER_LICENSE_ORIGINAL_NAME = "'
            + userInfo["user_license_original_name"]
            + '", '
        )
        query += (
            'USER_LICENSE_CHANGE_NAME = "'
            + userInfo["user_license_change_name"]
            + '", '
        )
        query += 'SIGN_PATH = "' + userInfo["sign_path"] + '", '
        query += 'SIGN_ORIGINAL_NAME = "' + userInfo["sign_original_name"] + '", '
        query += 'SIGN_CHANGE_NAME = "' + userInfo["sign_change_name"] + '" '
        query += "WHERE 1 = 1 "
        query += 'AND ID = "' + userInfo["id"] + '"'

        return query

    # 21. 회원 가입을 승인 한다.
    #
    # Parameter
    # 	- userId | String | 사용자 ID
    # 	- date	 | String | 사용자 가입 승인 시간
    def uApprovalUser(self, userId, date):
        query = UPDATE_USER_TABLE

        query += 'USER_STATE = "US000001", '
        query += 'APPRO_DATE = "' + date + '"'
        query += 'WHERE ID = "' + userId + '"'

        return query

    # 22. 회원을 삭제 한다.
    #
    # Parameter
    # 	- userId | String | 사용자 ID
    def uDeleteUser(self, userId):
        query = UPDATE_USER_TABLE

        query += 'USE_TYPE = "N" '
        query += 'WHERE ID = "' + userId + '"'

        return query

    # 23. 사용자 정보를 검색한다.
    #
    # Parameter
    # 	- userInfo | Object | 사용자 정보
    # 	- params   | Object | 검색조건
    def sSearchUserList(self, userInfo, params):
        commUtilServ = commUtilService()
        query = "SELECT * FROM ("
        query += SELECT_INFO_USER
        query += "ORDER BY " + params["sort_column"] + " " + params["sort_type"] + " "
        query += ") C WHERE 1=1 "

        # if((userInfo['authority_code'] == constants.USER_AUTH_CONTRACTOR) or
        # 		(userInfo['authority_code'] == constants.USER_AUTH_CONTRACTOR_MONITOR) or
        # 		(userInfo['authority_code'] == constants.USER_AUTH_CONTRACTION) or
        # 		(userInfo['authority_code'] == constants.USER_AUTH_SUPERVISOR) or
        # 		(userInfo['authority_code'] == constants.USER_AUTH_SUPERVISOR_MONITOR) or
        # 		(userInfo['authority_code'] == constants.USER_AUTH_SUPERVISING)):
        # 	query += CONDITION_COCODE_AND.replace(REPLACE_COCODE, userInfo['co_code'])

        if (commUtilServ.dataCheck(params["user_type"]) != False) and (
            params["user_type"] != "ALL"
        ):  # 회원 구분
            query += 'AND USER_TYPE = "' + params["user_type"] + '" '
        if commUtilServ.dataCheck(params["id"]) != False:  # ID
            query += 'AND ID LIKE "%' + params["id"] + '%" '
        if commUtilServ.dataCheck(params["user_name"]) != False:  # 사용자 명
            query += 'AND USER_NAME LIKE "%' + params["user_name"] + '%" '
        if commUtilServ.dataCheck(params["user_regisnum"]) != False:  # 주민등록번호
            query += 'AND USER_REGISNUM LIKE "%' + params["user_regisnum"] + '%" '
        if commUtilServ.dataCheck(params["user_contact"]) != False:  # 사용자 연락처
            query += 'AND USER_CONTACT LIKE "%' + params["user_contact"] + '%" '
        if commUtilServ.dataCheck(params["user_email"]) != False:  # 사용자 이메일
            query += 'AND USER_EMAIL LIKE "%' + params["user_email"] + '%" '
        if (commUtilServ.dataCheck(params["authority_code"]) != False) and (
            params["authority_code"] != "ALL"
        ):  # 권한 코드
            query += 'AND AUTHORITY_CODE = "' + params["authority_code"] + '" '
        if (commUtilServ.dataCheck(params["user_state"]) != False) and (
            params["user_state"] != "ALL"
        ):  # 승인여부
            query += 'AND USER_STATE = "' + params["user_state"] + '" '
        if commUtilServ.dataCheck(params["co_name"]) != False:  # 회사명
            query += 'AND CO_NAME LIKE "%' + params["co_name"] + '%" '
        if commUtilServ.dataCheck(params["user_position"]) != False:  # 직위
            query += 'AND USER_POSITION LIKE "%' + params["user_position"] + '%" '
        if (
            commUtilServ.dataCheck(params["search_start_join_date"]) != False
        ):  # 가입 검색 시작 날짜
            query += 'AND JOIN_DATE >= "' + params["search_start_join_date"] + '" '
        if (
            commUtilServ.dataCheck(params["search_end_join_date"]) != False
        ):  # 가입 검색 종료 날짜
            query += 'AND JOIN_DATE <= "' + params["search_end_join_date"] + '" '
        if (
            commUtilServ.dataCheck(params["search_start_appro_date"]) != False
        ):  # 가입 검색 시작 날짜
            query += 'AND APPRO_DATE >= "' + params["search_start_appro_date"] + '" '
        if (
            commUtilServ.dataCheck(params["search_end_appro_date"]) != False
        ):  # 가입 검색 종료 날짜
            query += 'AND APPRO_DATE <= "' + params["search_end_appro_date"] + '" '

        query += "LIMIT " + params["start_num"] + ", " + params["end_num"]

        return query

    # 24. 사용자 ID 찾기
    #
    # Parameter
    # 	- params   | Object | 사용자 찾기 조건
    def sFindUserId(self, params):
        query = SELECT_INFO_USER

        query += CONDITION_USERNAME_AND.replace(REPLACE_USERNAME, params["user_name"])
        query += CONDITION_USEREMAIL_AND.replace(
            REPLACE_USEREMAIL, params["user_email"]
        )

        return query

    # 25. 사용자 정보 찾기
    #
    # Parameter
    # 	- params   | Object | 사용자 찾기 조건
    def sFindUserInfo(self, params):
        query = SELECT_INFO_USER

        query += (
            'AND A.ID = "' + REPLACE_USERID.replace(REPLACE_USERID, params["id"]) + '" '
        )

        query += CONDITION_USERNAME_AND.replace(REPLACE_USERNAME, params["user_name"])
        query += CONDITION_USEREMAIL_AND.replace(
            REPLACE_USEREMAIL, params["user_email"]
        )

        return query

    # 26. 비밀번호 저장
    #
    # Parameter
    # 	- params		| Object | 사용자 비밀번호 저장
    # 	- encPasswd		| String | 새로운 비밀번호
    def uInitPassword(self, params, encPasswd):
        query = UPDATE_USER_TABLE

        query += 'PASSWORD = "' + encPasswd + '" WHERE 1 = 1 '
        # query += u'USER_PASSWORD = "' + encPasswd + '" '
        query += CONDITION_USERID_AND.replace(REPLACE_USERID, params["id"])
        query += CONDITION_USERNAME_AND.replace(REPLACE_USERNAME, params["user_name"])
        query += CONDITION_USEREMAIL_AND.replace(
            REPLACE_USEREMAIL, params["user_email"]
        )

        return query

    # 27. 사용자 정보를 검색한다.(ID 리스트로 해당 사용자를 검색 한다.)
    #
    # Parameter
    # 	- userList | Array | 사용자 ID 리스트
    def sUserInfoList(self, userList):
        query = SELECT_INFO_USER

        query += "AND A.ID IN("

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

    # 28. 사용자 총 개수를 검색한다.
    #
    # Parameter
    # 	- userInfo | Object | 사용자 정보
    # 	- params   | Object | 검색조건
    def sSearchUserCnt(self, userInfo, params):
        commUtilServ = commUtilService()
        query = "SELECT COUNT(*) as cnt FROM ("
        query += SELECT_INFO_USER
        query += ") C WHERE 1=1 "

        # if((userInfo['authority_code'] == constants.USER_AUTH_CONTRACTOR) or
        # 		(userInfo['authority_code'] == constants.USER_AUTH_CONTRACTOR_MONITOR) or
        # 		(userInfo['authority_code'] == constants.USER_AUTH_CONTRACTION) or
        # 		(userInfo['authority_code'] == constants.USER_AUTH_SUPERVISOR) or
        # 		(userInfo['authority_code'] == constants.USER_AUTH_SUPERVISOR_MONITOR) or
        # 		(userInfo['authority_code'] == constants.USER_AUTH_SUPERVISING)):
        # 	query += CONDITION_COCODE_AND.replace(REPLACE_COCODE, userInfo['co_code'])

        if (commUtilServ.dataCheck(params["user_type"]) != False) and (
            params["user_type"] != "ALL"
        ):  # 회원 구분
            query += 'AND USER_TYPE = "' + params["user_type"] + '" '
        if commUtilServ.dataCheck(params["id"]) != False:  # ID
            query += 'AND ID LIKE "%' + params["id"] + '%" '
        if commUtilServ.dataCheck(params["user_name"]) != False:  # 사용자 명
            query += 'AND USER_NAME LIKE "%' + params["user_name"] + '%" '
        if commUtilServ.dataCheck(params["user_regisnum"]) != False:  # 주민등록번호
            query += 'AND USER_REGISNUM LIKE "%' + params["user_regisnum"] + '%" '
        if commUtilServ.dataCheck(params["user_contact"]) != False:  # 사용자 연락처
            query += 'AND USER_CONTACT LIKE "%' + params["user_contact"] + '%" '
        if commUtilServ.dataCheck(params["user_email"]) != False:  # 사용자 이메일
            query += 'AND USER_EMAIL LIKE "%' + params["user_email"] + '%" '
        if (commUtilServ.dataCheck(params["authority_code"]) != False) and (
            params["authority_code"] != "ALL"
        ):  # 권한 코드
            query += 'AND AUTHORITY_CODE = "' + params["authority_code"] + '" '
        if (commUtilServ.dataCheck(params["user_state"]) != False) and (
            params["user_state"] != "ALL"
        ):  # 승인여부
            query += 'AND USER_STATE = "' + params["user_state"] + '" '
        if commUtilServ.dataCheck(params["co_name"]) != False:  # 회사명
            query += 'AND CO_NAME LIKE "%' + params["co_name"] + '%" '
        if commUtilServ.dataCheck(params["user_position"]) != False:  # 직위
            query += 'AND USER_POSITION LIKE "%' + params["user_position"] + '%" '
        if (
            commUtilServ.dataCheck(params["search_start_join_date"]) != False
        ):  # 가입 검색 시작 날짜
            query += 'AND JOIN_DATE >= "' + params["search_start_join_date"] + '" '
        if (
            commUtilServ.dataCheck(params["search_end_join_date"]) != False
        ):  # 가입 검색 종료 날짜
            query += 'AND JOIN_DATE <= "' + params["search_end_join_date"] + '" '
        if (
            commUtilServ.dataCheck(params["search_start_appro_date"]) != False
        ):  # 가입 검색 시작 날짜
            query += 'AND APPRO_DATE >= "' + params["search_start_appro_date"] + '" '
        if (
            commUtilServ.dataCheck(params["search_end_appro_date"]) != False
        ):  # 가입 검색 종료 날짜
            query += 'AND APPRO_DATE <= "' + params["search_end_appro_date"] + '" '

        return query

    # 책임 감리원 전용 사용자 정보를 검색한다.
    #
    # Parameter
    # 	- params   | Object | 검색조건
    def sSearchFieldUserListAll(self, params):
        commUtilServ = commUtilService()
        query = "SELECT * FROM ("
        query += SELECT_INFO_USER
        query += "ORDER BY CIM.CO_NAME, A.USER_NAME ASC "
        query += ") C WHERE 1=1 "

        # 		if(params['job_type'] == 0):
        # 			query += u'AND AUTHORITY_CODE IN ("' + constants.USER_AUTH_BUYER + '") '
        # 		elif(params['job_type'] == 1):
        # 			query += u'AND AUTHORITY_CODE IN ("' + constants.USER_AUTH_DESIGNER + '") '
        # 		elif(params['job_type'] == 2):
        # 			query += u'AND AUTHORITY_CODE IN ("' + constants.USER_AUTH_CONTRACTOR + '",'
        # 			query += u'"' + constants.USER_AUTH_CONTRACTOR_MONITOR + '",'
        # 			query += u'"' + constants.USER_AUTH_CONTRACTION + '") '
        # 		elif(params['job_type'] == 3):
        # 			query += u'AND AUTHORITY_CODE IN ("' + constants.USER_AUTH_SUPERVISOR_MONITOR + '",'
        # 			query += u'"' + constants.USER_AUTH_SUPERVISING + '") '
        # 		elif(params['job_type'] == 4):
        # 			query += u'AND AUTHORITY_CODE IN ("' + constants.USER_AUTH_WHITEHALL + '") '
        # 		elif(params['job_type'] == 5):
        # 			query += u'AND AUTHORITY_CODE IN ("' + constants.USER_AUTH_SUPERVISOR + '") '

        if commUtilServ.dataCheck(params["user_name"]) != False:  # 사용자 명
            query += 'AND USER_NAME LIKE "%' + params["user_name"] + '%" '
        if commUtilServ.dataCheck(params["co_name"]) != False:  # 회사명
            query += 'AND CO_NAME LIKE "%' + params["co_name"] + '%" '

        return query

    # 회사 인력 정보를 조회 한다.
    def sGetCompUserInfo(self, coCode, userId):
        query = SELECT_COMPANYUSER_INFO

        if userId == "ALL":
            if coCode != "":
                query = query.replace(
                    "{1}",
                    SELECT_COMPANYUSER_INFO_COMPANY_AND_1.replace(
                        REPLACE_COCODE, coCode
                    ),
                )
                query = query.replace(
                    "{2}",
                    SELECT_COMPANYUSER_INFO_COMPANY_AND_2.replace(
                        REPLACE_COCODE, coCode
                    ),
                )
            else:
                query = query.replace(
                    "{1}",
                    SELECT_COMPANYUSER_INFO_USER_AND_1.replace(REPLACE_USERID, userId),
                )
                query = query.replace("{2}", "")

        else:
            query = query.replace(
                "{1}",
                SELECT_COMPANYUSER_INFO_USER_AND_1.replace(REPLACE_USERID, userId),
            )
            query = query.replace(
                "{2}",
                SELECT_COMPANYUSER_INFO_USER_AND_2.replace(REPLACE_USERID, userId),
            )

        return query

    # 사용자(관리자 및 회사 코드) 정보 수정
    def uUpdateUserCoInfo(self, userId, updateUserInfoList):
        query = UPDATE_USER_TABLE

        index = 0
        listSize = len(updateUserInfoList)
        for updateUserInfo in updateUserInfoList:
            if listSize > 1:
                if index < listSize - 1:
                    query += (
                        updateUserInfo["key"] + ' = "' + updateUserInfo["value"] + '", '
                    )
                else:
                    query += (
                        updateUserInfo["key"] + ' = "' + updateUserInfo["value"] + '" '
                    )

                index += 1
            else:
                query += updateUserInfo["key"] + ' = "' + updateUserInfo["value"] + '" '

        query += 'WHERE ID = "' + userId + '"'

        return query

    def sSearchUserInfoList(self, searchList):
        query = SELECT_INFO_USER

        index = 0
        listSize = len(searchList)
        for searchInfo in searchList:
            # if(listSize > 1):
            # 	if(index < listSize - 1):
            # 		query += 'AND A.' + searchInfo['key'] + ' = "' + searchInfo['value'] + '", '
            # 	else:
            # 		query += 'AND A.' + searchInfo['key'] + ' = "' + searchInfo['value'] + '" '

            # 	index += 1
            # else:
            # 	query += 'AND A.' + searchInfo['key'] + ' = "' + searchInfo['value'] + '" '
            query += "AND A." + searchInfo["key"] + ' = "' + searchInfo["value"] + '" '

        return query

    # 조현우 추가 해당 유저 결재필요 게시글 리스트 조회
    @staticmethod
    def select_approvals(cons_code):
        query = SELECT_USER_APPROVALS.format(cons_code, cons_code)

        return query