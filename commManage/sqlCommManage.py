# _*_coding: utf-8 -*-

from common import constants

SELECT_INFO_SUBCODEMANAGE = """SELECT 
									SUBCODE_NAME as subcode_name,
									FULLCODE as fullcode,
									SUBCODE_EXPLAIN as subcode_explain
								FROM
									SUBCODE_MANAGE
								WHERE
									1=1
							"""

SELECT_INFO_CODENAME = """SELECT 
								SUBCODE_NAME as subcode_name
							FROM
								SUBCODE_MANAGE
							WHERE
								1=1
							"""

CONDITION_CODE_AND = 'AND CODE = "{code}" '
REPLACE_CODE = "{code}"


SELECT_CFGINFO_SYSTEMCONFIG = (
    "SELECT CFG_VALUE AS cfg_value FROM SYSTEM_CONFIG WHERE 1=1 "
)
SELECT_INFO_ADMINISTRATIVEDIVISION = """SELECT
											TYPE AS type,
											ADMIN_DIVISION_CD AS admin_division_cd,
											STAGE1 AS stage1,
											STAGE2 AS stage2,
											STAGE3 AS stage3,
											GRID_X AS grid_x,
											GRID_Y AS grid_y,
											LON_H AS lon_h,
											LON_M AS lon_m,
											LON_S AS lon_s,
											LAT_H AS lat_h,
											LAT_M AS lat_m,
											LAT_S AS lag_s,
											LON AS lon,
											LAT AS lat
										FROM
											ADMINISTRATIVE_DIVISION
										WHERE
											1=1
									"""

SELECT_CO_INFO = """SELECT 
						CO_CODE AS co_code, 
						CO_NAME AS co_name,
						CO_TYPE AS co_type,
						CEO AS co_ceo, 
						CONTACT AS co_contact,
						ADDRESS AS co_address,
						REGISNUM AS co_regisnum
					FROM COMPANY
					WHERE 1=1
					AND USE_TYPE = "Y" """


UPDATE_SYSTEMCONFIG_TABLE = "UPDATE SYSTEM_CONFIG SET "


CONDITION_CFGNAME_AND = 'AND CFG_NAME	= "{cfg_name}" '


REPLACE_CFGNAME = "{cfg_name}"


class sqlCommManage:

    # 1. 코드 리스트를 반환한다.
    #
    # Parameter
    # 	- reqType | String | 요청 타입
    def sGetCodeList(self, reqType):
        query = SELECT_INFO_SUBCODEMANAGE

        if reqType != "ALL":
            query += CONDITION_CODE_AND.replace(REPLACE_CODE, reqType)

        query += "ORDER BY FULLCODE ASC"
        return query

    # 2. 행정구역 정보를 반환 한다.
    #
    # Parameter
    # 	- index | int | 검색 단계
    # 	- arrAddress | Array | 단계별 주소
    def sGetLocationInfo(self, index, arrAddress):
        query = SELECT_INFO_ADMINISTRATIVEDIVISION

        query += 'AND STAGE1 = "' + arrAddress[0] + '" '

        if index == 2:
            query += 'AND STAGE2 = "' + arrAddress[1] + '" '
        elif index == 3:
            query += 'AND STAGE2 = "' + arrAddress[1] + '" '
            query += 'AND STAGE3 = "' + arrAddress[1] + '" '

        return query

    # 3. 시스템 환경 설정을 업데이트 한다.
    #
    # Parameter
    # 	- cfgName | String | 시스템 설정 명
    # 	- cfgValue| String | 시스템 설정 값
    def uModifySysCfg(self, cfgName, cfgValue):

        query = UPDATE_SYSTEMCONFIG_TABLE

        query += "CFG_VALUE = " + str(cfgValue) + " WHERE 1 = 1 "
        query += CONDITION_CFGNAME_AND.replace(REPLACE_CFGNAME, cfgName)

        return query

    # 4. 환경설정 값을 가지고 온다.
    # Parameter
    # 	- cfgName | String | 환경설정 명
    def sGetSysCfg(self, cfgName):
        query = SELECT_CFGINFO_SYSTEMCONFIG
        query += CONDITION_CFGNAME_AND.replace(REPLACE_CFGNAME, cfgName)

        return query

    # 회사 리스트를 가지고 온다.
    # Parameter
    # 	- cpName | String | 회사 명
    def sGetCoList(self, coName):
        query = SELECT_CO_INFO

        if coName != "ALL":
            query += 'AND CO_NAME LIKE "%' + coName + '%" '

        query += "ORDER BY CO_NAME ASC"

        return query

    # 코드 명을 제공 한다.
    def sGetCodeName(self, code):
        query = SELECT_INFO_CODENAME

        query += 'AND FULLCODE = "' + code + '"'

        return query
