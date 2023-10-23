# _*_coding: utf-8 -*-

import os
import sys

from allscapeAPIMain import procName

from common.commUtilService import commUtilService

from common import constants
from common.commonService import commonService
from common.logManage import logManage

# SELECT_OCCSTATLIST_INFO = u'''
# 	SELECT
# 		WLTWS.CONS_CODE AS cons_code,
# 		(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = WLTWS.CONS_CODE) AS cons_name,
# 		WLTWS.SYS_DOC_NUM AS sys_doc_num,
# 		WLTWS.CO_CODE AS co_code,
# 		(SELECT CO_NAME FROM COMPANY WHERE CO_CODE = WLTWS.CO_CODE) AS co_name,
# 		WLTWS.WORK_DATE AS work_date,
# 		WLTWS.OCC_CODE AS occ_code,
# 		(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = WLTWS.OCC_CODE) AS occ_name,
# 		WLTWS.PREV_DAY_TOTAL AS prev_day_total,
# 		WLTWS.TODAY_TOTAL AS today_total,
# 		WLTWS.TOTAL_RUNNING AS total_running
# 	FROM WORK_LOG_TODAY_WORKER_STATISTICS WLTWS, (SELECT SYS_DOC_NUM, MAX(WORK_DATE) FROM WORK_LOG_TODAY_WORKER_STATISTICS WHERE CONS_CODE = "{cons_code}" AND CO_CODE = "{co_code}") B
# 	WHERE 1=1
# 	AND WLTWS.SYS_DOC_NUM = B.SYS_DOC_NUM
#'''

SELECT_OCCSTATLIST_INFO = """
	SELECT
		WLTWS.CONS_CODE AS cons_code,
		(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = WLTWS.CONS_CODE) AS cons_name,
		WLTWS.SYS_DOC_NUM AS sys_doc_num,
		WLTWS.CO_CODE AS co_code,
		(SELECT CO_NAME FROM COMPANY WHERE CO_CODE = WLTWS.CO_CODE) AS co_name,
		WLTWS.WORK_DATE AS work_date,
		WLTWS.OCC_CODE AS occ_code,
		(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = WLTWS.OCC_CODE) AS occ_name,
		WLTWS.PREV_DAY_TOTAL AS prev_day_total,
		WLTWS.TODAY_TOTAL AS today_total,
		WLTWS.TOTAL_RUNNING AS total_running
	FROM WORK_LOG_TODAY_WORKER_STATISTICS WLTWS, (SELECT MAX(SYS_DOC_NUM) AS SYS_DOC_NUM FROM WORK_LOG_TODAY_WORKER_STATISTICS WHERE CONS_CODE = "{cons_code}" AND CO_CODE = "{co_code}") B
	WHERE 1=1
	AND WLTWS.SYS_DOC_NUM = B.SYS_DOC_NUM
"""

# SELECT_EQUSTATLIST_INFO = u'''
# 	SELECT
# 		WLTIES.CONS_CODE AS cons_code,
# 		(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = WLTIES.CONS_CODE) AS cons_name,
# 		WLTIES.SYS_DOC_NUM AS sys_doc_num,
# 		WLTIES.CO_CODE AS co_code,
# 		(SELECT CO_NAME FROM COMPANY WHERE CO_CODE = WLTIES.CO_CODE) AS co_name,
# 		WLTIES.INPUT_DATE AS input_date,
# 		WLTIES.EQUIP_CODE AS equip_code,
# 		(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = WLTIES.EQUIP_CODE) AS equip_name,
# 		WLTIES.PREV_DAY_TOTAL AS prev_day_total,
# 		WLTIES.TODAY_TOTAL AS today_total,
# 		WLTIES.TOTAL_RUNNING AS total_running
# 	FROM WORK_LOG_TODAY_INPUT_EQUIP_STATISTICS WLTIES, (SELECT SYS_DOC_NUM, MAX(INPUT_DATE) FROM WORK_LOG_TODAY_INPUT_EQUIP_STATISTICS WHERE CONS_CODE = "{cons_code}" AND CO_CODE = "{co_code}") B
# 	WHERE 1=1
# 	AND WLTIES.SYS_DOC_NUM = B.SYS_DOC_NUM
#'''

SELECT_EQUSTATLIST_INFO = """
	SELECT
		WLTIES.CONS_CODE AS cons_code,
		(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = WLTIES.CONS_CODE) AS cons_name,
		WLTIES.SYS_DOC_NUM AS sys_doc_num,
		WLTIES.CO_CODE AS co_code,
		(SELECT CO_NAME FROM COMPANY WHERE CO_CODE = WLTIES.CO_CODE) AS co_name,
		WLTIES.INPUT_DATE AS input_date,
		WLTIES.EQUIP_CODE AS equip_code,
		(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = WLTIES.EQUIP_CODE) AS equip_name,
		WLTIES.PREV_DAY_TOTAL AS prev_day_total,
		WLTIES.TODAY_TOTAL AS today_total,
		WLTIES.TOTAL_RUNNING AS total_running
	FROM WORK_LOG_TODAY_INPUT_EQUIP_STATISTICS WLTIES, (SELECT MAX(SYS_DOC_NUM) AS SYS_DOC_NUM FROM WORK_LOG_TODAY_INPUT_EQUIP_STATISTICS WHERE CONS_CODE = "{cons_code}" AND CO_CODE = "{co_code}") B
	WHERE 1=1
	AND WLTIES.SYS_DOC_NUM = B.SYS_DOC_NUM
"""

# SELECT_WORKLOADSTATLIST_INFO = u'''
# 	SELECT
# 		BOPD.CONS_CODE AS cons_code,
# 		(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = BOPD.CONS_CODE) AS cons_name,
# 		BOPD.CO_CODE AS co_code,
# 		(SELECT CO_NAME FROM COMPANY WHERE CO_CODE = BOPD.CO_CODE) AS co_name,
# 		BOPD.CONSTR_TYPE_CD AS constr_type_cd,
# 		(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = BOPD.CONSTR_TYPE_CD) AS constr_type_nm,
# 		BOPD.MATERIAL_NAME AS material_name,
# 		BOPD.MAT_TOT_CNT AS mat_tot_cnt,
# 		IFNULL(WLWL.AMOUNT_USE_PREV_DAY, 0) AS amount_use_prev_day,
# 		IFNULL(WLWL.PREV_DAY_COMPLET_RATE, 0) AS prev_day_complet_rate
# 	FROM BASED_ON_PROCESS_DETAILS BOPD LEFT OUTER JOIN
# 														(SELECT CONS_CODE, CONSTR_TYPE_CD, MATERIAL_NAME, AMOUNT_USE_PREV_DAY, PREV_DAY_COMPLET_RATE FROM WORK_LOG_WORK_LOAD WHERE CONS_CODE = "{cons_code}" AND CO_CODE = "{co_code}" AND WORK_DATE IN (SELECT MAX(WORK_DATE) FROM WORK_LOG_WORK_LOAD WHERE CONS_CODE = "{cons_code}" AND CO_CODE = "{co_code}")) WLWL
# 									   ON WLWL.CONS_CODE = BOPD.CONS_CODE
# 									   AND WLWL.CONSTR_TYPE_CD = BOPD.CONSTR_TYPE_CD
# 									   AND WLWL.MATERIAL_NAME = BOPD.MATERIAL_NAME
# 	WHERE 1=1
# 	AND BOPD.CONS_CODE = "{cons_code}"
# 	AND BOPD.CO_CODE = "{co_code}"
# 	ORDER BY constr_type_nm ASC
#'''

SELECT_WORKLOADSTATLIST_INFO = """
	SELECT
		BOPD.CONS_CODE AS cons_code,
		(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = BOPD.CONS_CODE) AS cons_name,
		BOPD.CO_CODE AS co_code,
		(SELECT CO_NAME FROM COMPANY WHERE CO_CODE = BOPD.CO_CODE) AS co_name,
		BOPD.CONSTR_TYPE_CD AS constr_type_cd,
		(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = BOPD.CONSTR_TYPE_CD) AS constr_type_nm,
		BOPD.MATERIAL_NAME AS material_name,
		BOPD.MAT_TOT_CNT AS mat_tot_cnt,
		IFNULL(WLWL.AMOUNT_USE_PREV_DAY, 0) AS amount_use_prev_day,
		IFNULL(WLWL.PREV_DAY_COMPLET_RATE, 0) AS prev_day_complet_rate
	FROM BASED_ON_PROCESS_DETAILS BOPD LEFT OUTER JOIN
														(SELECT CONS_CODE, CONSTR_TYPE_CD, MATERIAL_NAME, AMOUNT_USE_PREV_DAY, PREV_DAY_COMPLET_RATE FROM WORK_LOG_WORK_LOAD WHERE CONS_CODE = "{cons_code}" AND CO_CODE = "{co_code}" AND SYS_DOC_NUM IN (SELECT MAX(SYS_DOC_NUM) AS SYS_DOC_NUM FROM WORK_LOG_WORK_LOAD WHERE CONS_CODE = "{cons_code}" AND CO_CODE = "{co_code}")) WLWL
									   ON WLWL.CONS_CODE = BOPD.CONS_CODE
									   AND WLWL.CONSTR_TYPE_CD = BOPD.CONSTR_TYPE_CD
									   AND WLWL.MATERIAL_NAME = BOPD.MATERIAL_NAME
	WHERE 1=1
	AND BOPD.CONS_CODE = "{cons_code}"
	AND BOPD.CO_CODE = "{co_code}"
	ORDER BY constr_type_nm ASC
"""

INSERT_WORKLOG_INFO = """INSERT INTO WORK_LOG(CONS_CODE, SYS_DOC_NUM, DOC_NUM, DOC_CODE, WRITE_DATE, WEATHER, WRITE_STANDARD_CODE, CO_CODE) """

DELETE_WORKLOG_INFO = """DELETE FROM WORK_LOG WHERE 1=1 """


INSERT_WORKLOGTODAY_INFO = """INSERT INTO WORK_LOG_TODAY(CONS_CODE, SYS_DOC_NUM, WORK_ORDER, OCC_CODE, WORKER_NAME, WORK_UNIT, TODAY_WORK_LOAD, APT_BLOCK, FLOOR, AREA, CONSTR_TYPE_CD, DETAIL_CONSTR_TYPE_CD, GR_UNGR, CO_CODE, WORK_DATE) """

DELETE_WORKLOGTODAY_INFO = """DELETE FROM WORK_LOG_TODAY WHERE 1=1 """


INSERT_WORKLOGDRAWING_INFO = """INSERT INTO WORK_LOG_DRAWING(CONS_CODE, SYS_DOC_NUM, WORK_ORDER, DRAWING_ORDER, SYS_DRAWING_NUM) """

DELETE_WORKLOGDRAWING_INFO = """DELETE FROM WORK_LOG_DRAWING WHERE 1=1 """


INSERT_WORKLOGTODAYWORKERSTATISTICS_INFO = """INSERT INTO WORK_LOG_TODAY_WORKER_STATISTICS(CONS_CODE, SYS_DOC_NUM, WORK_DATE, OCC_CODE, PREV_DAY_TOTAL, TODAY_TOTAL, TOTAL_RUNNING, CO_CODE) """

DELETE_WORKLOGTODAYWORKERSTATISTICS_INFO = (
    """DELETE FROM WORK_LOG_TODAY_WORKER_STATISTICS WHERE 1=1 """
)


INSERT_WORKLOGTODAYINPUTEQUIPSTATUS_INFO = """INSERT INTO WORK_LOG_TODAY_INPUT_EQUIP_STATUS(CONS_CODE, SYS_DOC_NUM, EQUIP_ORDER, CONSTR_TYPE_CD, DETAIL_CONSTR_TYPE_CD, EQUIP_CODE, TODAY_INPUT_LOAD, INPUT_UNIT, CO_CODE) """

DELETE_WORKLOGTODAYINPUTEQUIPSTATUS_INFO = (
    """DELETE FROM WORK_LOG_TODAY_INPUT_EQUIP_STATUS WHERE 1=1 """
)


INSERT_WORKLOGTODAYINPUTEQUIPSTATISTICS_INFO = """INSERT INTO WORK_LOG_TODAY_INPUT_EQUIP_STATISTICS(CONS_CODE, SYS_DOC_NUM, INPUT_DATE, EQUIP_CODE, PREV_DAY_TOTAL, TODAY_TOTAL, TOTAL_RUNNING, CO_CODE) """

DELETE_WORKLOGTODAYINPUTEQUIPSTATISTICS_INFO = (
    """DELETE FROM WORK_LOG_TODAY_INPUT_EQUIP_STATISTICS WHERE 1=1 """
)


INSERT_WORKLOGUNIQUENESS_INFO = """INSERT INTO WORK_LOG_UNIQUENESS(CONS_CODE, SYS_DOC_NUM, UNIQ_ORDER, UNIQUENESS) """

DELETE_WORKLOGUNIQUENESS_INFO = """DELETE FROM WORK_LOG_UNIQUENESS WHERE 1=1 """


INSERT_WORKLOGEXCEPTEDWORKTOM_INFO = """INSERT INTO WORK_LOG_EXCEPTED_WORK_TOM(CONS_CODE, SYS_DOC_NUM, EXCEPT_WORK_ORDER, EXCEPT_WORK) """

DELETE_WORKLOGEXCEPTEDWORKTOM_INFO = (
    """DELETE FROM WORK_LOG_EXCEPTED_WORK_TOM WHERE 1=1 """
)

INSERT_WORKLOGWORKLOAD_INFO = """INSERT INTO WORK_LOG_WORK_LOAD(CONS_CODE, SYS_DOC_NUM, CONSTR_TYPE_CD, MATERIAL_NAME, AMOUNT_USE_PREV_DAY, PREV_DAY_COMPLET_RATE, AMOUNT_USE_TODAY, TODAY_COMPLET_RATE, CO_CODE, WORK_DATE) """

DELETE_WORKLOGWORKLOAD_INFO = """DELETE FROM WORK_LOG_WORK_LOAD WHERE 1=1 """


SELECT_WORKLOGLIST_INFO = """
	SELECT
		DB1.CONS_CODE AS cons_code, DB1.CONS_NAME AS cons_name,
		DB1.SYS_DOC_NUM AS sys_doc_num, DB1.DOC_NUM AS doc_num,
		DB1.DOC_CODE AS doc_code, DB1.DOC_NAME AS doc_name,
		DB1.WRITE_DATE AS write_date, DB1.WEATHER AS weather,
		DB1.WRITE_STANDARD_CODE AS write_standard_code, DB1.WRITE_STANDARD_NAME AS write_standard_name,
		DB1.CO_CODE AS co_code, DB1.CO_NAME AS co_name,
		DB1.WRITER AS writer, DB1.WRITER_NAME AS writer_name,
		DB1.PC_DATE AS pc_date, DB1.WORK_DATE AS work_date,
		DB1.STATE_CODE AS state_code, DB1.STATE_NAME AS state_name
		FROM
			(SELECT
				WL.CONS_CODE, (SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = WL.CONS_CODE) AS CONS_NAME,
				WL.SYS_DOC_NUM, WL.DOC_NUM,
				WL.DOC_CODE, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = WL.DOC_CODE) AS DOC_NAME,
				WL.WRITE_DATE, WL.WEATHER,
				WL.WRITE_STANDARD_CODE, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = WL.WRITE_STANDARD_CODE) AS WRITE_STANDARD_NAME,
				WL.CO_CODE, (SELECT CO_NAME FROM COMPANY WHERE CO_CODE = WL.CO_CODE) AS CO_NAME,
				(SELECT PROJECT_STATUS FROM PROJECT WHERE CONS_CODE = WL.CONS_CODE) AS PROJECT_STATUS_CD,
				DM.WRITER, (SELECT USER_NAME FROM USER WHERE ID = DM.WRITER) AS WRITER_NAME,
				DM.PC_DATE, WLT.WORK_DATE,
				DM.STATE_CODE, (SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = DM.STATE_CODE) AS STATE_NAME
			FROM
				DOC_MANAGE DM LEFT OUTER JOIN WORK_LOG WL ON WL.SYS_DOC_NUM = DM.SYS_DOC_NUM
			     	  		  {16}
			WHERE 1=1
			{1}
			{2}
			{3}
			{4}
			) DB1
		WHERE 1=1
		{15}

		{1_1}

		{7}
		{8}
		{9}
		{10}
		{11}
		{12}
		{13}
		{14}
"""

SELECT_WORKLOGLIST_CONDITION_1 = 'AND WL.CONS_CODE = "{cons_code}" '
SELECT_WORKLOGLIST_CONDITION_2 = 'AND WL.WRITE_DATE >= "{start_write_date}" '
SELECT_WORKLOGLIST_CONDITION_3 = 'AND WL.WRITE_DATE <= "{end_write_date}" '
SELECT_WORKLOGLIST_CONDITION_4 = 'AND WL.CO_CODE = "{co_code}" '
SELECT_WORKLOGLIST_CONDITION_5 = 'AND DB1.CONSTR_TYPE_CD = "{constr_type_cd}" '
SELECT_WORKLOGLIST_CONDITION_6 = (
    'AND DB1.DETAIL_CONSTR_TYPE_CD = "{detail_constr_type_cd}" '
)
SELECT_WORKLOGLIST_CONDITION_7 = 'AND DB1.WRITER_NAME LIKE "%{writer_name}%" '
SELECT_WORKLOGLIST_CONDITION_8 = 'AND DB1.PC_DATE >= "{start_pc_date}" '
SELECT_WORKLOGLIST_CONDITION_9 = 'AND DB1.PC_DATE <= "{end_pc_date}" '
SELECT_WORKLOGLIST_CONDITION_10 = 'AND DB1.WORK_DATE >= "{start_work_date}" '
SELECT_WORKLOGLIST_CONDITION_11 = 'AND DB1.WORK_DATE <= "{end_work_date}" '
SELECT_WORKLOGLIST_CONDITION_12 = 'AND DB1.STATE_CODE = "{state_code}" '
SELECT_WORKLOGLIST_CONDITION_13 = "ORDER BY DB1.{sort_column} {sort_type} "
SELECT_WORKLOGLIST_CONDITION_14 = "limit {start_num}, {end_num} "
SELECT_WORKLOGLIST_CONDITION_15_1 = 'AND DB1.SYS_DOC_NUM IN ((SELECT SYS_DOC_NUM FROM APPROVAL_INFORMATION WHERE DOC_CODE = "CD000014" AND ID = "{loginUserId}"))'
SELECT_WORKLOGLIST_CONDITION_15_2 = 'AND DB1.SYS_DOC_NUM IN (SELECT DISTINCT SYS_DOC_NUM FROM APPROVAL_INFORMATION WHERE CONS_CODE = "{cons_code}" AND ID IN (SELECT ID FROM USER WHERE CO_CODE IN (SELECT CO_CODE FROM USER WHERE ID = "{loginUserId}")) AND (APPROVAL = "Y" OR CUR_APPROVAL = "Y"))'
SELECT_WORKLOGLIST_CONDITION_15_3 = 'AND DB1.SYS_DOC_NUM IN ((SELECT SYS_DOC_NUM FROM APPROVAL_INFORMATION WHERE DOC_CODE = "CD000014" AND CO_CODE = "{coCode}"))'
SELECT_WORKLOGLIST_CONDITION_16 = 'LEFT OUTER JOIN (SELECT DISTINCT WORK_DATE, SYS_DOC_NUM FROM WORK_LOG_TODAY WHERE CONS_CODE = "{cons_code}") WLT ON WLT.SYS_DOC_NUM = DM.SYS_DOC_NUM'
SELECT_WORKLOGLIST_CONDITION_1_1 = (
    'AND DB1.PROJECT_STATUS_CD IN ("ST000001", "ST000002")'
)


# AND WI.CO_CODE = "{co_code}"
SELECT_WORKIMGLIST_INFO = """
	SELECT
		WI.CONS_CODE AS cons_code,
        WI.CO_CODE AS co_code,
        WI.CONS_DATE AS cons_date,
        WI.WORK_LOG_CONS_CODE AS item_code,
        PD.PRODUCT AS product,
        PD.STANDARD AS standard,
        WI.CONS_TYPE_CD AS pc_code,
        SC.SUBCODE_NAME AS pc_name,
		WI.IMAGE_TITLE AS image_title,
		WI.IMAGE_PATH AS image_path,
		WI.IMAGE_ORIG_NAME AS image_orig_name,
		WI.IMAGE_CHAN_NAME AS image_chan_name,
		date_format(WI.UPLOAD_DATE, '%Y%m%d%H%i%S') AS upload_date,
        WI.FILE_INDEX AS file_index
	FROM
		WORK_IMAGE_MANAGE WI
        JOIN PROCESS_DETAIL PD
        ON WI.CONS_CODE = PD.CONS_CODE
        AND WI.CO_CODE = PD.CO_CODE
        AND WI.WORK_LOG_CONS_CODE = concat(lpad(PD.LEVEL1, 2, '0'), lpad(PD.LEVEL2, 2, '0'), lpad(PD.LEVEL3, 2, '0'), lpad(PD.LEVEL4, 3, '0'))
        JOIN SUBCODE_MANAGE SC
        ON WI.CONS_TYPE_CD = SC.FULLCODE
	WHERE
		1=1
	AND WI.CONS_CODE = "{cons_code}"
	{}
	{start_upload_date}
	{end_upload_date}
    AND PD.PRODUCT like "%{product}%"
    AND SC.SUBCODE_NAME like "%{pc_name}%"
	ORDER BY CONS_DATE DESC
"""

# 0203 희정 추가
INSERT_WORK_DIARY_INFO = """
	INSERT INTO WORK_DIARY_MANAGE(CONS_CODE, CO_CODE, SYS_DOC_NUM, CONS_DATE, WORK_TITLE, WORK_DIARY_CONTENT, WRITE_DATE, ID, TODAY_CONTENT, NEXT_CONTENT, TEMPERATURE, SKY_RESULT, PTY_RESULT)
"""

UPDATE_WORK_DIARY_INFO = " ".join(
    [
        "UPDATE",
        "WORK_DIARY_MANAGE",
        "SET",
        "WORK_DIARY_CONTENT = '{}',",
        "ID = '{}',",
        "TODAY_CONTENT = '{}',",
        "NEXT_CONTENT = '{}',",
        "TEMPERATURE = {},",
        "SKY_RESULT = {},",
        "PTY_RESULT = {}",
        "WHERE 1=1",
        "AND SYS_DOC_NUM = {}",
    ]
)
DELETE_WORK_DIARY = " ".join(
    [
        "DELETE",
        "FROM",
        "WORK_DIARY_MANAGE",
        "WHERE 1=1",
        "AND SYS_DOC_NUM = {}",
    ]
)

# 0203 희정 추가
DELETE_WORK_DIARY_INFO = """DELETE FROM WORK_DIARY_MANAGE WHERE 1=1 """

# 0203 희정 추가
# 	INSERT INTO WORK_LOG_MANAGE(CO_CODE, SYS_DOC_NUM, WORK_LOG_CONS_CODE, WORK_LOG_CONS_LV1, WORK_LOG_CONS_LV2, WORK_LOG_CONS_LV3, WORK_LOG_CONS_LV4, WORK_LOG_USE_AMOUNT, WORK_LOG_CONTENT)
INSERT_WORK_LOG_INFO = """
	INSERT INTO WORK_LOG_MANAGE(CO_CODE, SYS_DOC_NUM, WORK_LOG_CONS_CODE, WORK_LOG_CONS_LV1, WORK_LOG_CONS_LV2, WORK_LOG_CONS_LV3, WORK_LOG_CONS_LV4, CONS_TYPE_CD, TODAY_WORKLOAD, NEXT_WORKLOAD)
"""

INSERT_WORK_LOG = " ".join(
    [
        "INSERT",
        "INTO",
        "WORK_LOG_MANAGE(CO_CODE, SYS_DOC_NUM, WORK_LOG_CONS_CODE, WORK_LOG_CONS_LV1, WORK_LOG_CONS_LV2, WORK_LOG_CONS_LV3, WORK_LOG_CONS_LV4, CONS_TYPE_CD, TODAY_WORKLOAD, NEXT_WORKLOAD)",
        "VALUES('{}', {}, '{}', {}, {}, {}, {}, '{}', {}, {})",
    ]
)

#### 일지 등록시 직전작업량 업데이트 ####
#### 현 로그보다 오래된 모든 로그의 일일 작업량을 더하여 현 로그 prev_workload을 업데이트 한다 ####
# UPDATE_WORK_LOG_PREV_WORKLOAD_INIT = " ".join(
#    [
#        "SELECT SUM(TODAY_WORKLOAD) INTO @quantity",
#        "FROM WORK_LOG_MANAGE L",
#        "JOIN WORK_DIARY_MANAGE D",
#        "ON L.SYS_DOC_NUM = D.SYS_DOC_NUM",
#        "WHERE 1=1",
#        "{}",
#        "{}",
#        "{}",
#        "{}",
#        "FOR UPDATE;",
#        "SET",
#        "UPDATE",
#        "WORK_LOG_MANAGE L",
#        "JOIN WORK_DIARY_MANAGE D",
#        "ON L.SYS_DOC_NUM = D.SYS_DOC_NUM",
#        "SET",
#        "PREV_WORKLOAD = IFNULL(@quantity, 0)",
#        "WHERE 1=1",
#        "{}",
#        "{}",
#        "{}",
#        "{}",
#    ]
# )
UPDATE_WORK_LOG_PREV_WORKLOAD_INIT = " ".join(
    [
        "SET SQL_SAFE_UPDATES = 0;",
        "SELECT SUM(TODAY_WORKLOAD) INTO @quantity",
        "FROM WORK_LOG_MANAGE L",
        "JOIN WORK_DIARY_MANAGE D",
        "ON L.SYS_DOC_NUM = D.SYS_DOC_NUM",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "FOR UPDATE;",
        "UPDATE",
        "WORK_LOG_MANAGE L",
        "JOIN WORK_DIARY_MANAGE D",
        "ON L.SYS_DOC_NUM = D.SYS_DOC_NUM",
        "SET",
        "PREV_WORKLOAD = IFNULL(@quantity, 0)",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{};",
        "SET SQL_SAFE_UPDATES = 1;",
    ]
)

#### 일지 업데이트시 직전작업량 업데이트 ####
#### 현 로그보다 나중 건설일인 로그의 모든 prev_workload를 업데이트 한다 ####
UPDATE_WORK_LOG_PREV_WORKLOAD_CHAN = " ".join(
    [
        "SET SQL_SAFE_UPDATES = 0;",
        "SELECT {} - TODAY_WORKLOAD INTO @difference",
        "FROM WORK_LOG_MANAGE L ",
        "JOIN WORK_DIARY_MANAGE D",
        "ON L.SYS_DOC_NUM = D.SYS_DOC_NUM",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "FOR UPDATE;",
        "UPDATE",
        "WORK_LOG_MANAGE L",
        "JOIN WORK_DIARY_MANAGE D",
        "ON L.SYS_DOC_NUM = D.SYS_DOC_NUM",
        "SET",
        "PREV_WORKLOAD = PREV_WORKLOAD + IFNULL(@difference, 0)",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{};",
        "SET SQL_SAFE_UPDATES = 1;",
    ]
)

#### 이전일지 추가시 직전작업량 업데이트 ####
#### 현 로그보다 나중 건설일인 로그의 모든 prev_workload를 업데이트 한다 ####
UPDATE_WORK_LOG_PREV_WORKLOAD_CHAN2 = " ".join(
    [
        "SET SQL_SAFE_UPDATES = 0;",
        "SELECT TODAY_WORKLOAD INTO @difference",
        "FROM WORK_LOG_MANAGE L ",
        "JOIN WORK_DIARY_MANAGE D",
        "ON L.SYS_DOC_NUM = D.SYS_DOC_NUM",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "FOR UPDATE;",
        "UPDATE",
        "WORK_LOG_MANAGE L",
        "JOIN WORK_DIARY_MANAGE D",
        "ON L.SYS_DOC_NUM = D.SYS_DOC_NUM",
        "SET",
        "PREV_WORKLOAD = PREV_WORKLOAD + IFNULL(@difference, 0)",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{};",
        "SET SQL_SAFE_UPDATES = 1;",
    ]
)

CONSCODE_CONDITION_D = "AND D.CONS_CODE = '{}'"
COCODE_CONDITION_L = "AND L.CO_CODE = '{}'"
WORKLOGCONSCODE_CONDITON_L = "AND L.WORK_LOG_CONS_CODE = '{}'"
CONSDATE_UNDER_CONDITION_D = "AND D.CONS_DATE < '{}'"
CONSDATE_CONDITION_D = "AND D.CONS_DATE = '{}'"
CONSDATE_OVER_CONDITION_D = "AND D.CONS_DATE > '{}'"

UPDATE_WORK_LOG_INFO = " ".join(
    [
        "UPDATE",
        "WORK_LOG_MANAGE",
        "SET",
        "TODAY_WORKLOAD = {},",
        "NEXT_WORKLOAD = {}",
        "WHERE 1=1",
        "AND SYS_DOC_NUM = {}",
        "AND WORK_LOG_CONS_CODE = '{}'",
    ]
)

DELETE_WORK_LOG = " ".join(
    [
        "DELETE",
        "FROM",
        "WORK_LOG_MANAGE",
        "WHERE 1=1",
        "AND SYS_DOC_NUM = {}",
        "AND WORK_LOG_CONS_CODE = '{}'",
    ]
)
# 0203 희정 추가
DELETE_WORK_LOG_INFO = """DELETE FROM WORK_LOG_MANAGE WHERE 1=1 """

# 0203 희정 추가
INSERT_WORK_IMAGE_INFO = """
	INSERT INTO WORK_IMAGE_MANAGE(CONS_CODE, CO_CODE, CONS_DATE, SYS_DOC_NUM, WORK_LOG_CONS_CODE, IMAGE_TITLE, IMAGE_PATH, IMAGE_ORIG_NAME, IMAGE_CHAN_NAME, UPLOAD_DATE, FILE_INDEX, CONS_TYPE_CD)
"""

# 0203 희정 추가
DELETE_WORK_IMAGE_INFO = """DELETE FROM WORK_IMAGE_MANAGE WHERE 1=1 """

INSERT_WORK_MANPOWER_INFO = """
	INSERT INTO WORK_MANPOWER_MANAGE(CONS_CODE, CO_CODE, CONS_DATE, SYS_DOC_NUM, CONS_TYPE_CD, WORK_LOG_CONS_CODE, PREV_MANPOWER, TODAY_MANPOWER, NEXT_MANPOWER)
"""

INSERT_WORK_MANPOWER = " ".join(
    [
        "INSERT",
        "INTO",
        "WORK_MANPOWER_MANAGE(CONS_CODE, CO_CODE, CONS_DATE, SYS_DOC_NUM, CONS_TYPE_CD, WORK_LOG_CONS_CODE, PREV_MANPOWER, TODAY_MANPOWER, NEXT_MANPOWER)",
        "VALUES('{}', '{}', '{}', {}, '{}', '{}', {}, {}, {})",
    ]
)

UPDATE_WORK_MANPOWER_INFO = " ".join(
    [
        "UPDATE",
        "WORK_MANPOWER_MANAGE",
        "SET",
        "TODAY_MANPOWER = {},",
        "NEXT_MANPOWER = {}",
        "WHERE 1=1",
        "AND SYS_DOC_NUM = {}",
        "AND WORK_LOG_CONS_CODE = '{}'",
    ]
)

DELETE_WORK_MANPOWER = " ".join(
    [
        "DELETE",
        "FROM",
        "WORK_MANPOWER_MANAGE",
        "WHERE 1=1",
        "AND SYS_DOC_NUM = {}",
        "AND WORK_LOG_CONS_CODE = '{}'",
    ]
)

DELETE_WORK_MANPOWER_INFO = """DELETE FROM WORK_MANPOWER_MANAGE WHERE 1=1 """

# 0203 희정 추가
SELECT_WORK_DL_INFO = """
	SELECT
		CONS_CODE AS cons_code,
		CONS_DATE AS cons_date,
		SYS_DOC_NUM AS sys_doc_num,
		WORK_LOG_CONS_CODE AS work_log_cons_code,
		IMAGE_TITLE AS image_title,
		IMAGE_PATH AS image_path,
		IMAGE_ORIG_NAME AS image_orig_name,
		IMAGE_CHAN_NAME AS image_chan_name,
		UPLOAD_DATE AS upload_date,
		FILE_INDEX AS file_index
	FROM WORK_IMAGE_MANAGE
	WHERE 1=1
"""

#### 조현우 쿼리작성 ####
SELECT_WORKDIARY_MASTER = " ".join(
    [
        "SELECT",
        "A.CONS_DATE as cons_date,",
        "A.WORK_TITLE as work_title,",
        "date_format(A.WRITE_DATE, '%Y%m%d%H%i%S') as write_date,",
        "A.SYS_DOC_NUM AS sys_doc_num,",
        "A.ID as id,",
        "A.TEMPERATURE AS temperature,",
        "A.SKY_RESULT AS sky_result,",
        "A.PTY_RESULT AS pty_result,",
        "(SELECT USER_NAME FROM USER WHERE ID = A.ID) AS user_name",
        "FROM WORK_DIARY_MANAGE A",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "ORDER BY A.CONS_DATE DESC, A.SYS_DOC_NUM",
    ]
)

#### 조현우 쿼리작성 ####
SELECT_WORKDIARY = " ".join(
    [
        "SELECT",
        "A.CONS_DATE as cons_date,",
        "A.WORK_TITLE as work_title,",
        "date_format(A.WRITE_DATE, '%Y%m%d%H%i%S') as write_date,",
        "A.SYS_DOC_NUM AS sys_doc_num,",
        "A.ID as id,",
        "A.TEMPERATURE AS temperature,",
        "A.SKY_RESULT AS sky_result,",
        "A.PTY_RESULT AS pty_result,",
        "(SELECT USER_NAME FROM USER WHERE ID = A.ID) AS user_name",
        "FROM WORK_DIARY_MANAGE A",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "ORDER BY A.CONS_DATE DESC, A.SYS_DOC_NUM",
    ]
)

WORKDIARY_CONSCODE_CONDITON_A = "AND A.CONS_CODE = '{}'"
WORKDIARY_COCODE_CONDITON_A = "AND A.CO_CODE = '{}'"
WORKDIARY_CONSDATE_CONDITON_A = "AND A.CONS_DATE = '{}'"
WORKDIARY_STARTDATE_CONDITON_A = "AND A.CONS_DATE >= '{}'"
WORKDIARY_ENDDATE_CONDITON_A = "AND A.CONS_DATE <= '{}'"

SELECT_WORKLOGCONSCODE = " ".join(
    [
        "SELECT",
        "D.CONS_DATE as cons_date," "L.WORK_LOG_CONS_CODE as work_log_cons_code",
        "FROM WORK_DIARY_MANAGE D",
        "JOIN WORK_LOG_MANAGE L",
        "ON D.SYS_DOC_NUM = L.SYS_DOC_NUM",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

WORKDIARY_CONSCODE_CONDITON_D = "AND D.CONS_CODE = '{}'"
WORKDIARY_COCODE_CONDITON_D = "AND D.CO_CODE = '{}'"
WORKDIARY_SYSDOCNUM_CONDITON_D = "AND D.SYS_DOC_NUM = {}"

DELETE_WORKDIARY = " ".join(
    [
        "DELETE",
        "FROM WORK_DIARY_MANAGE",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

WORKDIARY_CONSCODE_CONDITON = "AND CONS_CODE = '{}'"
WORKDIARY_COCODE_CONDITON = "AND CO_CODE = '{}'"
WORKDIARY_SYSDOCNUM_CONDITON = "AND SYS_DOC_NUM = {}"

# 검색키 값 cons_code, cons_date => sys_doc_num
# 하루에 여러 작업일지가 들어오면 가장 최신의 것만 조회
SELECT_WORKDIARY_SYSNUM = " ".join(
    [
        "SELECT",
        "A.SYS_DOC_NUM as sys_key",
        "FROM WORK_DIARY_MANAGE A",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "ORDER BY A.SYS_DOC_NUM DESC",
    ]
)

SELECT_WORKDIARY_DETAIL = " ".join(
    [
        "SELECT",
        "A.CONS_CODE AS cons_code,",
        "(SELECT CONS_NAME FROM PROJECT WHERE CONS_CODE = A.CONS_CODE) AS cons_name,",
        "A.CO_CODE AS co_code,",
        "(SELECT CO_NAME FROM COMPANY WHERE CO_CODE = A.CO_CODE) AS co_name,",
        "A.SYS_DOC_NUM AS sys_doc_num,",
        "A.CONS_DATE as cons_date,",
        "A.WORK_TITLE as work_title,",
        "A.WORK_DIARY_CONTENT as content,",
        "A.WRITE_DATE as write_date,",
        "A.ID as id,",
        "(SELECT USER_NAME FROM USER WHERE ID = A.ID) AS user_name,",
        "A.TODAY_CONTENT AS today_content,",
        "A.NEXT_CONTENT AS next_content,",
        "A.TEMPERATURE AS temp,",
        "A.PTY_RESULT as pty_result,",
        "A.SKY_RESULT as sky_result",
        "FROM WORK_DIARY_MANAGE A",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

SELECT_WORKDIARY_IMAGE = " ".join(
    [
        "SELECT",
        "A.FILE_INDEX as file_index,",
        "A.IMAGE_TITLE as title,",
        "A.IMAGE_PATH as path,",
        "A.IMAGE_ORIG_NAME as original_name,",
        "A.IMAGE_CHAN_NAME as change_name,",
        "A.UPLOAD_DATE as upload_date",
        "FROM WORK_IMAGE_MANAGE A",
        "WHERE 1=1",
        "{}",
        "{}",
        "AND A.WORK_LOG_CONS_CODE = ''",
    ]
)

#    "WORK_LOG_USE_AMOUNT as use_amount,",
#    "WORK_LOG_CONTENT as work_log_content",
#    "(SELECT PRODUCT FROM PROCESS_DETAIL WHERE WORK_LOG_CONS_LV1 = A.WORK_LOG_CONS_LV1 AND WORK_LOG_CONS_LV2 = A.WORK_LOG_CONS_LV2 AND WORK_LOG_CONS_LV3 = A.WORK_LOG_CONS_LV3 AND WORK_LOG_CONS_LV4 = A.WORK_LOG_CONS_LV4) as work_log_cons_name,",

SELECT_WOKRLOG_PREVWORKLOAD = " ".join(
    [
        "SELECT",
        "IFNULL(SUM(L.TODAY_WORKLOAD), 0) as raw_prev_workload",
        "FROM WORK_DIARY_MANAGE D",
        "JOIN WORK_LOG_MANAGE L",
        "ON L.SYS_DOC_NUM = D.SYS_DOC_NUM",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
    ]
)

SELECT_WORKLOG_DETAIL = " ".join(
    [
        "SELECT",
        "A.WORK_LOG_CONS_CODE as work_log_cons_code,",
        "A.CONS_TYPE_CD AS cons_type_cd,",
        "(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.CONS_TYPE_CD) AS cons_type_nm,",
        "(SELECT SUBCODE_EXPLAIN FROM SUBCODE_MANAGE WHERE FULLCODE = A.CONS_TYPE_CD) AS cons_type_explain,",
        "A.WORK_LOG_CONS_CODE AS work_log_cons_code,",
        # "A.WORK_LOG_CONS_LV1 AS work_log_cons_lv1,",
        # "A.WORK_LOG_CONS_LV2 AS work_log_cons_lv2,",
        # "A.WORK_LOG_CONS_LV3 AS work_log_cons_lv3,",
        # "A.WORK_LOG_CONS_LV4 AS work_log_cons_lv4,",
        "PD.PRODUCT AS product,",
        "PD.UNIT AS unit,",
        "PD.QUANTITY as raw_total,",
        "A.TODAY_WORKLOAD AS raw_today_workload,",
        "A.NEXT_WORKLOAD AS raw_next_workload,",
        "PD.LEVEL1_NAME AS level1_name,",
        "PD.LEVEL2_NAME AS level2_name,",
        "PD.LEVEL3_NAME AS level3_name",
        "FROM WORK_LOG_MANAGE A JOIN PROCESS_DETAIL AS PD",
        "ON PD.LEVEL1 = A.WORK_LOG_CONS_LV1",
        "AND PD.LEVEL2 = A.WORK_LOG_CONS_LV2",
        "AND PD.LEVEL3 = A.WORK_LOG_CONS_LV3",
        "AND PD.LEVEL4 = A.WORK_LOG_CONS_LV4",
        "{}",
        "{}",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

#### 시공자 또는 디자이너가 문서를 볼 수 있는지 확인한다(소속회사 작성 및 프로젝트 참여확인) ####
SELECT_WORKDIARY_USERIN = " ".join(
    [
        "SELECT",
        "'OK'",
        "FROM WORK_DIARY_MANAGE D",
        "JOIN JOIN_WORKFORCE J",
        "ON D.CO_CODE = J.CO_CODE",
        "WHERE 1=1",
        "AND D.SYS_DOC_NUM = {}",
        "AND J.ID = '{}'",
    ]
)

#### 본사 관리자가 문서를 볼 수 있는지 확인한다 (소속회사 작성 확인)####
SELECT_WORKDIARY_COMPANYIN = " ".join(
    [
        "SELECT",
        "'OK'",
        "FROM WORK_DIARY_MANAGE",
        "WHERE 1=1",
        "AND SYS_DOC_NUM = {}",
        "AND CO_CODE = '{}'",
    ]
)

#### 문서의 공사코드를 조회한다 ####
SELECT_WORKDIARY_CONSCODE = " ".join(
    [
        "SELECT",
        "CONS_CODE as cons_code",
        "FROM WORK_DIARY_MANAGE",
        "WHERE 1=1",
        "AND SYS_DOC_NUM = {}",
    ]
)
#### 소속확인 필요 조건문 ####

INSERT_WORKLOG_IMAGE = " ".join(
    [
        "INSERT",
        "INTO",
        "WORK_IMAGE_MANAGE(CONS_CODE, CO_CODE, CONS_DATE, SYS_DOC_NUM, WORK_LOG_CONS_CODE, CONS_TYPE_CD, FILE_INDEX, IMAGE_TITLE, IMAGE_PATH, IMAGE_ORIG_NAME, IMAGE_CHAN_NAME)",
        "VALUES('{}', '{}', '{}', {}, '{}', '{}', {}, '{}', '{}', '{}', '{}')",
    ]
)

SELECT_WORKLOG_IMAGE = " ".join(
    [
        "SELECT",
        "A.CONS_DATE AS cons_date,",
        "A.FILE_INDEX as file_index,",
        "A.IMAGE_TITLE as title,",
        "A.IMAGE_PATH as filePath,",
        "A.IMAGE_ORIG_NAME as orig_name,",
        "A.IMAGE_CHAN_NAME as chan_name,",
        "date_format(A.UPLOAD_DATE, '%Y%m%d%H%i%S') as upload_date,",
        "A.WORK_LOG_CONS_CODE AS work_log_cons_code,",
        "A.CONS_TYPE_CD AS cons_type_cd,",
        "(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.CONS_TYPE_CD) AS cons_type_nm,",
        "(SELECT SUBCODE_EXPLAIN FROM SUBCODE_MANAGE WHERE FULLCODE = A.CONS_TYPE_CD) AS cons_type_explain",
        "FROM WORK_IMAGE_MANAGE A",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
    ]
)

UPDATE_WORKLOG_IMAGE = " ".join(
    [
        "UPDATE",
        "WORK_IMAGE_MANAGE",
        "SET IMAGE_TITLE = '{}'",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
    ]
)

SELECT_WORKLOG_IMAGE_DELETE = " ".join(
    [
        "SELECT",
        "WORK_LOG_CONS_CODE as work_log_cons_code,",
        "IMAGE_PATH as img_path,",
        "IMAGE_CHAN_NAME as chan_name",
        "FROM WORK_IMAGE_MANAGE A",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
    ]
)
DELETE_CONSCODE_CONDITON = "AND CONS_CODE = '{}'"
DELETE_COCODE_CONDITON = "AND CO_CODE = '{}'"
DELETE_SYSDOCNUM_CONDITON = "AND SYS_DOC_NUM = {}"
DELETE_LOGCONSCODE_CONDITON = "AND WORK_LOG_CONS_CODE = '{}'"
DELETE_INDEX_CONDITION = "AND FILE_INDEX = {}"


DELETE_WORKLOG_IMAGE = " ".join(
    [
        "DELETE",
        "FROM",
        "WORK_IMAGE_MANAGE",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
    ]
)

DELETE_WORKLOG_IMAGE_DELETE = " ".join(
    [
        "DELETE",
        "FROM",
        "WORK_IMAGE_MANAGE",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
    ]
)

SELECT_WORKLOG_MANPOWER = " ".join(
    [
        "SELECT",
        "A.CONS_TYPE_CD AS cons_type_cd,",
        "(SELECT SUBCODE_NAME FROM SUBCODE_MANAGE WHERE FULLCODE = A.CONS_TYPE_CD) AS cons_type_nm,",
        "(SELECT SUBCODE_EXPLAIN FROM SUBCODE_MANAGE WHERE FULLCODE = A.CONS_TYPE_CD) AS cons_type_explain,",
        "A.PREV_MANPOWER AS prev_manpower,",
        "A.TODAY_MANPOWER AS today_manpower,",
        "A.NEXT_MANPOWER AS next_manpower,",
        "A.WORK_LOG_CONS_CODE AS work_log_cons_code,",
        "LVIF.WORK_LOG_CONS_LV1 AS work_log_cons_lv1,",
        "LVIF.WORK_LOG_CONS_LV2 AS work_log_cons_lv2,",
        "LVIF.WORK_LOG_CONS_LV3 AS work_log_cons_lv3,",
        "LVIF.WORK_LOG_CONS_LV4 AS work_log_cons_lv4,",
        "LVIF.LEVEL1_NAME AS level1_name,",
        "LVIF.LEVEL2_NAME AS level2_name,",
        "LVIF.LEVEL3_NAME AS level3_name,",
        "LVIF.PRODUCT AS product",
        "FROM WORK_MANPOWER_MANAGE A JOIN (",
        "SELECT PD.CONS_CODE, B.SYS_DOC_NUM, B.CONS_TYPE_CD, B.WORK_LOG_CONS_CODE, B.CO_CODE,",
        "B.WORK_LOG_CONS_LV1, B.WORK_LOG_CONS_LV2, B.WORK_LOG_CONS_LV3, B.WORK_LOG_CONS_LV4,",
        "PD.LEVEL1_NAME, PD.LEVEL2_NAME, PD.LEVEL3_NAME, PD.PRODUCT",
        "FROM WORK_LOG_MANAGE B ",
        "JOIN PROCESS_DETAIL as PD",
        "ON  PD.LEVEL1 = B.WORK_LOG_CONS_LV1",
        "AND PD.LEVEL2 = B.WORK_LOG_CONS_LV2",
        "AND PD.LEVEL3 = B.WORK_LOG_CONS_LV3",
        "AND PD.LEVEL4 = B.WORK_LOG_CONS_LV4",
        "{}",
        "{}",
        "WHERE 1=1",
        "{}",
        "{}",
        ") AS LVIF ON A.CONS_CODE = LVIF.CONS_CODE",
        "AND A.CO_CODE = LVIF.CO_CODE",
        "AND A.SYS_DOC_NUM = LVIF.SYS_DOC_NUM",
        "AND A.CONS_TYPE_CD = LVIF.CONS_TYPE_CD",
        "AND A.WORK_LOG_CONS_CODE = LVIF.WORK_LOG_CONS_CODE",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

CONSCODE_CONDITION_A = "AND A.CONS_CODE = '{}'"
CONSCODE_CONDITION_PD = "AND PD.CONS_CODE = '{}'"
SYSDOCNUM_CONDITION_A = "AND A.SYS_DOC_NUM = {}"
SYSDOCNUM_CONDITION_B = "AND B.SYS_DOC_NUM = {}"
COCODE_CONDITION_A = "AND A.CO_CODE = '{}'"
COCODE_CONDITION_PD = "AND PD.CO_CODE = '{}'"
COCODE_CONDITION_B = "AND B.CO_CODE = '{}'"
LOGCONSCODE_CONDITION_A = "AND A.WORK_LOG_CONS_CODE = '{}'"
CONSTYPECODE_CONDITION = "AND A.CONS_TYPE_CD = '{}'"
INDEX_CONDITION_A = "AND A.FILE_INDEX = {}"

CONSCODE_CONDITION = "AND CONS_CODE = '{}'"
COCODE_CONDITION = "AND CO_CODE = '{}'"
SYSDOCNUM_CONDITION = "AND SYS_DOC_NUM = {}"
LOGCONSCODE_CONDITION = "AND WORK_LOG_CONS_CODE = '{}'"
LOGCONSCODE_CONDITION_L = "AND WORK_LOG_CONS_CODE = '{}'"
INDEX_CONDITION = "AND FILE_INDEX = {}"

COUNT_WORKLOG_BYLEVEL = " ".join(
    [
        "SELECT",
        "D.CONS_DATE",
        "D.WORK_LOG_CONS_LV1",
        "FROM WORK_LOG_MANAGE L",
        "JOIN WORK_DIARY_MANAGE D",
        "ON L.SYS_DOC_NUM = D.SYS_DOC_NUM",
        "JOIN PROCESS_DETAIL",
        "ON D",
    ]
)

SELECT_WORKLOAD = " ".join(
    [
        "SELECT",
        "D.CONS_DATE as cons_date,",
        "L.WORK_LOG_CONS_LV1 as level1,",
        "L.WORK_LOG_CONS_LV2 as level2,",
        "L.WORK_LOG_CONS_LV3 as level3,",
        "L.WORK_LOG_CONS_LV4 as level4,",
        "L.CONS_TYPE_CD as pc_code,",
        "L.TODAY_WORKLOAD as today_quantity",
        "FROM WORK_DIARY_MANAGE D",
        "JOIN WORK_LOG_MANAGE L",
        "ON L.SYS_DOC_NUM = D.SYS_DOC_NUM",
        "WHERE 1=1",
        "{}",
        "{}",
        "ORDER BY CONS_DATE, PC_CODE",
    ]
)

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class sqlProjectWorkLogManage:

    # 직종 통계 정보를 조회 한다
    def sGetOccStatList(self, consCode, coCode):

        query = SELECT_OCCSTATLIST_INFO

        query = query.replace("{cons_code}", consCode)
        query = query.replace("{co_code}", coCode)

        return query

    # 장비 통계 정보를 조회 한다
    def sGetEquStatList(self, consCode, coCode):

        query = SELECT_EQUSTATLIST_INFO

        query = query.replace("{cons_code}", consCode)
        query = query.replace("{co_code}", coCode)

        return query

    # 자재 사용량 통계 정보를 가져온다.
    def sGetWorkLoadStatList(self, consCode, coCode):

        query = SELECT_WORKLOADSTATLIST_INFO

        query = query.replace("{cons_code}", consCode)
        query = query.replace("{co_code}", coCode)

        return query

    # 작업 일지 데이터를 저장 한다.
    def iPutWorkLog(self, params, docDefaultInfo, writeStandardName):
        commServ = commonService()

        try:
            query = INSERT_WORKLOG_INFO
            query += "VALUES("
            query += '"' + params["reqDocInfo"]["cons_code"] + '", '
            query += "" + str(docDefaultInfo["sysDocNum"]) + ", "
            query += '"' + docDefaultInfo["documentNumber"] + '", '
            query += '"' + params["reqDocInfo"]["doc_code"] + '", '
            query += '"' + docDefaultInfo["docCreateDate"] + '", '
            query += '"' + params["reqDocContent"]["weather"] + '", '
            query += '"' + writeStandardName + '", '
            query += '"' + docDefaultInfo["coCode"] + '"'
            query += ")"
            return query
        except KeyError as e:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )
        except NameError as e:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )
        except TypeError as e:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )
        except AttributeError as e:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )
        except Exception as e:
            result = commServ.makeReturnMessage(
                constants.REST_RESPONSE_CODE_DATAFAIL, str(e), None
            )

        logs.war(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "Response : " + commUtilServ.jsonDumps(result),
        )

        return None

    # 작업 일지를 삭제 한다.
    def dDelWorkLog(self, consCode, sysDocNum):
        query = DELETE_WORKLOG_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""

        return query

    # 금일 작업 내용 데이터 저장
    def iPutWorkLogToday(self, consCode, docDefaultInfo, workLogToday, workDate):
        query = INSERT_WORKLOGTODAY_INFO

        query += "VALUES("
        query += '"' + consCode + '", '
        query += "" + str(docDefaultInfo["sysDocNum"]) + ", "
        query += "" + str(workLogToday["order"]) + ", "
        query += '"' + workLogToday["occ_code"] + '", '
        query += '"' + workLogToday["worker_name"] + '", '
        query += '"' + workLogToday["work_unit"] + '", '
        query += '"' + workLogToday["today_work_load"] + '", '
        query += '"' + workLogToday["apt_block"] + '", '
        query += '"' + workLogToday["floor"] + '", '
        query += '"' + workLogToday["area"] + '", '
        query += '"' + workLogToday["constr_type_cd"] + '", '
        query += '"' + workLogToday["detail_constr_type_cd"] + '", '
        query += '"' + workLogToday["gr_ungr"] + '", '
        query += '"' + docDefaultInfo["coCode"] + '", '
        query += '"' + workDate + '"'
        query += ")"

        return query

    # 작업 일지를 삭제 한다.
    def dDelWorkLogToday(self, consCode, sysDocNum):
        query = DELETE_WORKLOGTODAY_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""

        return query

    # 관련 도면을 저장 한다.
    def iPutWorkLogDrawing(self, consCode, sysDocNum, workOrder, drawing):
        query = INSERT_WORKLOGDRAWING_INFO

        query += "VALUES("
        query += '"' + consCode + '", '
        query += "" + str(sysDocNum) + ", "
        query += "" + str(workOrder) + ", "
        query += "" + str(drawing["order"]) + ", "
        query += "" + str(drawing["sys_drawing_num"]) + ", "

        return query

    # 관련 도면을 삭제 한다.
    def dDelWorkLogDrawing(self, consCode, sysDocNum):
        query = DELETE_WORKLOGDRAWING_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""

        return query

    # 금일 인력 통계 정보를 저장 한다.
    def iPutWorkLogTodayWorkerStatistics(self, occStatData, coCode):
        query = INSERT_WORKLOGTODAYWORKERSTATISTICS_INFO

        query += "VALUES("
        query += '"' + occStatData["cons_code"] + '", '
        query += "" + str(occStatData["sys_doc_num"]) + ", "
        query += '"' + occStatData["work_date"] + '", '
        query += '"' + occStatData["occ_code"] + '", '
        query += "" + str(occStatData["prev_day_total"]) + ", "
        query += "" + str(occStatData["today_total"]) + ", "
        query += "" + str(occStatData["total_running"]) + ", "
        query += '"' + coCode + '" '
        query += ")"

        return query

    # 금일 인력 통계 정보를 삭제 한다.
    def dDelWorkLogTodayWorkerStatistics(self, consCode, sysDocNum):
        query = DELETE_WORKLOGTODAYWORKERSTATISTICS_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""

        return query

    # 금일 장비 투입 현황 데이터를 저장 한다.
    def iPutWorkLogTodayInputEquipStatus(
        self, consCode, docDefaultInfo, todayInputEquipStatus
    ):
        query = INSERT_WORKLOGTODAYINPUTEQUIPSTATUS_INFO

        query += "VALUES("
        query += '"' + consCode + '", '
        query += "" + str(docDefaultInfo["sysDocNum"]) + ", "
        query += "" + str(todayInputEquipStatus["order"]) + ", "
        query += '"' + todayInputEquipStatus["constr_type_cd"] + '", '
        query += '"' + todayInputEquipStatus["detail_constr_type_cd"] + '", '
        query += '"' + todayInputEquipStatus["equip_code"] + '", '
        query += '"' + todayInputEquipStatus["today_input_load"] + '", '
        query += '"' + todayInputEquipStatus["input_unit"] + '", '
        query += '"' + docDefaultInfo["coCode"] + '"'
        query += ")"

        return query

    # 금일 장비 투입 현황 데이터를 삭제 한다.
    def dDelWorkLogTodayInputEquipStatus(self, consCode, sysDocNum):
        query = DELETE_WORKLOGTODAYINPUTEQUIPSTATUS_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""

        return query

    # 금일 장비 통계 정보를 저장 한다.
    def iPutWorkLogTodayInputEquipStatistics(self, equipStatData, coCode):
        query = INSERT_WORKLOGTODAYINPUTEQUIPSTATISTICS_INFO

        query += "VALUES("
        query += '"' + equipStatData["cons_code"] + '", '
        query += "" + str(equipStatData["sys_doc_num"]) + ", "
        query += '"' + equipStatData["input_date"] + '", '
        query += '"' + equipStatData["equip_code"] + '", '
        query += "" + str(equipStatData["prev_day_total"]) + ", "
        query += "" + str(equipStatData["today_total"]) + ", "
        query += "" + str(equipStatData["total_running"]) + ", "
        query += '"' + coCode + '" '
        query += ")"

        return query

    # 금일 장비 통계 정보를 삭제 한다.
    def dDelWorkLogTodayInputEquipStatistics(self, consCode, sysDocNum):
        query = DELETE_WORKLOGTODAYINPUTEQUIPSTATISTICS_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""

        return query

    # 특이 사항 데이터 저장.
    def iPutWorkLogUniqueness(self, consCode, docDefaultInfo, uniqueness):
        query = INSERT_WORKLOGUNIQUENESS_INFO

        query += "VALUES("
        query += '"' + consCode + '", '
        query += "" + str(docDefaultInfo["sysDocNum"]) + ", "
        query += "" + str(uniqueness["order"]) + ", "
        query += '"' + str(uniqueness["uniquess"]) + '" '
        query += ")"

        return query

    # 특이 사항 데이터 삭제.
    def dDelWorkLogUniqueness(self, consCode, sysDocNum):
        query = DELETE_WORKLOGUNIQUENESS_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""

        return query

    # 명일 예상 작업 데이터 저장.
    def iPutWorkLogExceptedWorkTom(self, consCode, docDefaultInfo, exceptedWorkTom):
        query = INSERT_WORKLOGEXCEPTEDWORKTOM_INFO

        query += "VALUES("
        query += '"' + consCode + '", '
        query += "" + str(docDefaultInfo["sysDocNum"]) + ", "
        query += "" + str(exceptedWorkTom["order"]) + ", "
        query += '"' + str(exceptedWorkTom["except_work"]) + '" '
        query += ")"

        return query

    # 명일 예상 작업 데이터 삭제.
    def dDelWorkLogExceptedWorkTom(self, consCode, sysDocNum):
        query = DELETE_WORKLOGEXCEPTEDWORKTOM_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""

        return query

    # 자재 사용량 데이터 정보를 저장 한다.
    def iPutWorkLogWorkLoad(self, workLoadStat, workDate):
        query = INSERT_WORKLOGWORKLOAD_INFO

        query += "VALUES("
        query += '"' + workLoadStat["cons_code"] + '", '
        query += "" + str(workLoadStat["sys_doc_num"]) + ", "
        query += '"' + workLoadStat["constr_type_cd"] + '", '
        query += '"' + workLoadStat["material_name"] + '", '
        query += "" + str(workLoadStat["amount_use_prev_day"]) + ", "
        query += "" + str(workLoadStat["prev_day_complet_rate"]) + ", "
        query += "" + str(workLoadStat["amount_use_today"]) + ", "
        query += "" + str(workLoadStat["today_complet_rate"]) + ", "
        query += '"' + workLoadStat["co_code"] + '", '
        query += '"' + workDate + '" '
        query += ")"

        return query

    # 자재 사용량 데이터 정보를 삭제 한다.
    def dDelWorkLogWorkLoad(self, consCode, sysDocNum):
        query = DELETE_WORKLOGWORKLOAD_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""

        return query

    # 작업일지 리스트를 조회 한다.
    def sSearchWorkLogList(self, userInfo, userAuth, jobAuth, params):

        query = SELECT_WORKLOGLIST_INFO

        query = query.replace(
            "{16}",
            SELECT_WORKLOGLIST_CONDITION_16.replace(
                "{cons_code}", params["search_cons_code"]
            ),
        )

        if jobAuth == None:
            if (
                userAuth == constants.USER_AUTH_CONTRACTOR
                or userAuth == constants.USER_AUTH_CONTRACTOR_MONITOR
                or userAuth == constants.USER_AUTH_SUPERVISOR
                or userAuth == constants.USER_AUTH_SUPERVISOR_MONITOR
            ):
                query = query.replace(
                    "{15}",
                    SELECT_WORKLOGLIST_CONDITION_15_3.replace(
                        "{coCode}", userInfo["co_code"]
                    ),
                )
            elif (
                userAuth == constants.USER_AUTH_DESIGNER
                or userAuth == constants.USER_AUTH_CONTRACTION
                or userAuth == constants.USER_AUTH_SUPERVISING
                or userAuth == constants.USER_AUTH_INOCCUPATION
            ):
                query = query.replace(
                    "{15}",
                    SELECT_WORKLOGLIST_CONDITION_15_1.replace(
                        "{loginUserId}", userInfo["id"]
                    ),
                )
            else:
                query = query.replace("{15}", "")
        elif (jobAuth["job_title_code"] == constants.JOB_TITLE_CD_BUYER) or (
            jobAuth["job_title_code"] == constants.JOB_TITLE_CD_WHITEHALL
        ):
            query = query.replace("{15}", "")
        else:
            query = query.replace(
                "{15}",
                SELECT_WORKLOGLIST_CONDITION_15_1.replace(
                    "{loginUserId}", userInfo["id"]
                ),
            )

        if params["search_cons_code"] != "":
            query = query.replace(
                "{1}",
                SELECT_WORKLOGLIST_CONDITION_1.replace(
                    "{cons_code}", params["search_cons_code"]
                ),
            )
            query = query.replace("{1_1}", "")
        else:
            query = query.replace("{1}", "")
            query = query.replace("{1_1}", SELECT_WORKLOGLIST_CONDITION_1_1)

        if params["search_start_write_date"] != "":
            query = query.replace(
                "{2}",
                SELECT_WORKLOGLIST_CONDITION_2.replace(
                    "{start_write_date}", params["search_start_write_date"]
                ),
            )
        else:
            query = query.replace("{2}", "")

        if params["search_end_write_date"] != "":
            query = query.replace(
                "{3}",
                SELECT_WORKLOGLIST_CONDITION_3.replace(
                    "{end_write_date}", params["search_end_write_date"]
                ),
            )
        else:
            query = query.replace("{3}", "")

        if params["search_co_cd"] != "":
            query = query.replace(
                "{4}",
                SELECT_WORKLOGLIST_CONDITION_4.replace(
                    "{co_code}", params["search_co_cd"]
                ),
            )
        else:
            query = query.replace("{4}", "")

        # 		if(params['search_constr_type_cd'] != ''):
        # 			query = query.replace('{5}', SELECT_WORKLOGLIST_CONDITION_5.replace('{constr_type_cd}', params['search_constr_type_cd']))

        # 		if(params['search_detail_constr_type_cd'] != ''):
        # 			query = query.replace('{6}', SELECT_WORKLOGLIST_CONDITION_6.replace('{detail_constr_type_cd}', params['search_detail_constr_type_cd']))

        if params["search_writer_name"] != "":
            query = query.replace(
                "{7}",
                SELECT_WORKLOGLIST_CONDITION_7.replace(
                    "{writer_name}", params["search_writer_name"]
                ),
            )
        else:
            query = query.replace("{7}", "")

        if params["search_start_pc_date"] != "":
            query = query.replace(
                "{8}",
                SELECT_WORKLOGLIST_CONDITION_8.replace(
                    "{start_pc_date}", params["search_start_pc_date"]
                ),
            )
        else:
            query = query.replace("{8}", "")

        if params["search_end_pc_date"] != "":
            query = query.replace(
                "{9}",
                SELECT_WORKLOGLIST_CONDITION_9.replace(
                    "{end_pc_date}", params["search_end_pc_date"]
                ),
            )
        else:
            query = query.replace("{9}", "")

        if params["search_start_work_date"] != "":
            query = query.replace(
                "{10}",
                SELECT_WORKLOGLIST_CONDITION_10.replace(
                    "{start_work_date}", params["search_start_work_date"]
                ),
            )
        else:
            query = query.replace("{10}", "")

        if params["search_end_work_date"] != "":
            query = query.replace(
                "{11}",
                SELECT_WORKLOGLIST_CONDITION_11.replace(
                    "{end_work_date}", params["search_end_work_date"]
                ),
            )
        else:
            query = query.replace("{11}", "")

        if params["search_state_code"] != "":
            query = query.replace(
                "{12}",
                SELECT_WORKLOGLIST_CONDITION_12.replace(
                    "{state_code}", params["search_state_code"]
                ),
            )
        else:
            query = query.replace("{12}", "")

        query = query.replace(
            "{13}",
            SELECT_WORKLOGLIST_CONDITION_13.replace(
                "{sort_column}", params["sort_column"]
            ),
        )
        query = query.replace("{sort_type}", params["sort_type"])

        query = query.replace(
            "{14}",
            SELECT_WORKLOGLIST_CONDITION_14.replace("{start_num}", params["start_num"]),
        )
        query = query.replace("{end_num}", params["end_num"])

        return query

    # 작업일지 리스트 개수를 조회 한다.
    def sSearchWorkLogListCnt(self, userInfo, userAuth, jobAuth, params):
        query = "SELECT COUNT(*) AS cnt FROM ("
        query += SELECT_WORKLOGLIST_INFO

        query = query.replace(
            "{16}",
            SELECT_WORKLOGLIST_CONDITION_16.replace(
                "{cons_code}", params["search_cons_code"]
            ),
        )

        if jobAuth == None:
            if (
                userAuth == constants.USER_AUTH_CONTRACTOR
                or userAuth == constants.USER_AUTH_CONTRACTOR_MONITOR
                or userAuth == constants.USER_AUTH_SUPERVISOR
                or userAuth == constants.USER_AUTH_SUPERVISOR_MONITOR
            ):
                query = query.replace(
                    "{15}",
                    SELECT_WORKLOGLIST_CONDITION_15_3.replace(
                        "{coCode}", userInfo["co_code"]
                    ),
                )
            elif (
                userAuth == constants.USER_AUTH_DESIGNER
                or userAuth == constants.USER_AUTH_CONTRACTION
                or userAuth == constants.USER_AUTH_SUPERVISING
                or userAuth == constants.USER_AUTH_INOCCUPATION
            ):
                query = query.replace(
                    "{15}",
                    SELECT_WORKLOGLIST_CONDITION_15_1.replace(
                        "{loginUserId}", userInfo["id"]
                    ),
                )
            else:
                query = query.replace("{15}", "")
        elif (jobAuth["job_title_code"] == constants.JOB_TITLE_CD_BUYER) or (
            jobAuth["job_title_code"] == constants.JOB_TITLE_CD_WHITEHALL
        ):
            query = query.replace("{15}", "")
        else:
            query = query.replace(
                "{15}",
                SELECT_WORKLOGLIST_CONDITION_15_1.replace(
                    "{loginUserId}", userInfo["id"]
                ),
            )

        if params["search_cons_code"] != "":
            query = query.replace(
                "{1}",
                SELECT_WORKLOGLIST_CONDITION_1.replace(
                    "{cons_code}", params["search_cons_code"]
                ),
            )
            query = query.replace("{1_1}", "")
        else:
            query = query.replace("{1}", "")
            query = query.replace("{1_1}", SELECT_WORKLOGLIST_CONDITION_1_1)
        # query = query.replace('{1}', SELECT_WORKLOGLIST_CONDITION_1.replace('{cons_code}', params['search_cons_code']))

        if params["search_start_write_date"] != "":
            query = query.replace(
                "{2}",
                SELECT_WORKLOGLIST_CONDITION_2.replace(
                    "{start_write_date}", params["search_start_write_date"]
                ),
            )
        else:
            query = query.replace("{2}", "")

        if params["search_end_write_date"] != "":
            query = query.replace(
                "{3}",
                SELECT_WORKLOGLIST_CONDITION_3.replace(
                    "{end_write_date}", params["search_end_write_date"]
                ),
            )
        else:
            query = query.replace("{3}", "")

        if params["search_co_cd"] != "":
            query = query.replace(
                "{4}",
                SELECT_WORKLOGLIST_CONDITION_4.replace(
                    "{co_code}", params["search_co_cd"]
                ),
            )
        else:
            query = query.replace("{4}", "")

        # 		if(params['search_constr_type_cd'] != ''):
        # 			query = query.replace('{5}', SELECT_WORKLOGLIST_CONDITION_5.replace('{constr_type_cd}', params['search_constr_type_cd']))

        # 		if(params['search_detail_constr_type_cd'] != ''):
        # 			query = query.replace('{6}', SELECT_WORKLOGLIST_CONDITION_6.replace('{detail_constr_type_cd}', params['search_detail_constr_type_cd']))

        if params["search_writer_name"] != "":
            query = query.replace(
                "{7}",
                SELECT_WORKLOGLIST_CONDITION_7.replace(
                    "{writer_name}", params["search_writer_name"]
                ),
            )
        else:
            query = query.replace("{7}", "")

        if params["search_start_pc_date"] != "":
            query = query.replace(
                "{8}",
                SELECT_WORKLOGLIST_CONDITION_8.replace(
                    "{start_pc_date}", params["search_start_pc_date"]
                ),
            )
        else:
            query = query.replace("{8}", "")

        if params["search_end_pc_date"] != "":
            query = query.replace(
                "{9}",
                SELECT_WORKLOGLIST_CONDITION_9.replace(
                    "{end_pc_date}", params["search_end_pc_date"]
                ),
            )
        else:
            query = query.replace("{9}", "")

        if params["search_start_work_date"] != "":
            query = query.replace(
                "{10}",
                SELECT_WORKLOGLIST_CONDITION_10.replace(
                    "{start_work_date}", params["search_start_work_date"]
                ),
            )
        else:
            query = query.replace("{10}", "")

        if params["search_end_work_date"] != "":
            query = query.replace(
                "{11}",
                SELECT_WORKLOGLIST_CONDITION_11.replace(
                    "{end_work_date}", params["search_end_work_date"]
                ),
            )
        else:
            query = query.replace("{11}", "")

        if params["search_state_code"] != "":
            query = query.replace(
                "{12}",
                SELECT_WORKLOGLIST_CONDITION_12.replace(
                    "{state_code}", params["search_state_code"]
                ),
            )
        else:
            query = query.replace("{12}", "")

        query = query.replace("{13}", "")
        query = query.replace("{14}", "")

        query += ") TOTAL"
        return query

    # 작업 이미지 리스트를 조회 한다.
    def sSearchWorkImgList(
        self, consCode, authCode, co_code, searchStartDate, searchEndDate, search_name
    ):

        query = SELECT_WORKIMGLIST_INFO

        query = query.replace("{cons_code}", consCode)

        if authCode == constants.USER_BUYER:
            query = query.replace("{}", "")
        else:
            query = query.replace("{}", "AND WI.CO_CODE = '" + co_code + "'")

        query = query.replace(
            "{start_upload_date}",
            "AND WI.CONS_DATE >= {}".format(searchStartDate) if searchStartDate else "",
        )
        query = query.replace(
            "{end_upload_date}",
            "AND WI.CONS_DATE <= {}".format(searchEndDate) if searchEndDate else "",
        )
        query = query.replace("{product}", search_name["product_name"])
        query = query.replace("{pc_name}", search_name["pc_name"])
        return query

    def select_workdiary_master(self, cons_code, co_code, start_date, end_date):
        query = SELECT_WORKDIARY_MASTER.format(
            WORKDIARY_CONSCODE_CONDITON_A.format(cons_code),
            WORKDIARY_COCODE_CONDITON_A.format(co_code),
            WORKDIARY_STARTDATE_CONDITON_A.format(start_date)
            if start_date != ""
            else "",
            WORKDIARY_ENDDATE_CONDITON_A.format(end_date) if end_date != "" else "",
        )

        return query

    def select_workdiary(self, cons_code, co_code, start_date, end_date):
        query = SELECT_WORKDIARY.format(
            WORKDIARY_CONSCODE_CONDITON_A.format(cons_code),
            WORKDIARY_COCODE_CONDITON_A.format(co_code),
            WORKDIARY_STARTDATE_CONDITON_A.format(start_date)
            if start_date != ""
            else "",
            WORKDIARY_ENDDATE_CONDITON_A.format(end_date) if end_date != "" else "",
        )

        return query

    def select_worklogconscode(self, cons_code, co_code, sys_doc_num):
        query = SELECT_WORKLOGCONSCODE.format(
            WORKDIARY_CONSCODE_CONDITON_D.format(cons_code),
            WORKDIARY_COCODE_CONDITON_D.format(co_code),
            WORKDIARY_SYSDOCNUM_CONDITON_D.format(sys_doc_num),
        )

        return query

    def delete_workdiary(self, cons_code, co_code, sys_doc_num):
        query = DELETE_WORKDIARY.format(
            WORKDIARY_CONSCODE_CONDITON.format(cons_code),
            WORKDIARY_COCODE_CONDITON.format(co_code),
            WORKDIARY_SYSDOCNUM_CONDITON.format(sys_doc_num),
        )

        return query

    def select_sysnum(self, cons_code, co_code, cons_date):
        query = SELECT_WORKDIARY_SYSNUM.format(
            WORKDIARY_CONSCODE_CONDITON_A.format(cons_code),
            WORKDIARY_COCODE_CONDITON_A.format(co_code),
            WORKDIARY_CONSDATE_CONDITON_A.format(cons_date),
        )

        return query

    def select_workdiary_detail(self, cons_code, sysnum, co_code):
        query = SELECT_WORKDIARY_DETAIL.format(
            CONSCODE_CONDITION_A.format(cons_code),
            SYSDOCNUM_CONDITION_A.format(sysnum),
            COCODE_CONDITION_A.format(co_code) if co_code != "" else "",
        )

        return query

    def select_workdiary_image(self, sysnum, co_code):
        query = SELECT_WORKDIARY_IMAGE.format(
            SYSDOCNUM_CONDITION_A.format(sysnum),
            COCODE_CONDITION_A.format(co_code),
        )

        return query

    def select_worklog_prevwork(
        self, cons_code, co_code, cons_date, work_log_cons_code
    ):
        query = SELECT_WOKRLOG_PREVWORKLOAD.format(
            CONSCODE_CONDITION_D.format(cons_code),
            COCODE_CONDITION_L.format(co_code),
            CONSDATE_UNDER_CONDITION_D.format(cons_date),
            LOGCONSCODE_CONDITION_L.format(work_log_cons_code),
        )

        return query

    def select_worklog_detail(self, cons_code, sysnum, co_code):
        query = SELECT_WORKLOG_DETAIL.format(
            CONSCODE_CONDITION_PD.format(cons_code),
            COCODE_CONDITION_PD.format(co_code),
            SYSDOCNUM_CONDITION_A.format(sysnum),
            COCODE_CONDITION_A.format(co_code),
        )

        return query

    def insert_worklog_image(
        self,
        cons_code,
        co_code,
        cons_date,
        sys_doc_num,
        work_log_cons_code,
        cons_type_cd,
        file_index,
        image_title,
        image_path,
        image_orig_name,
        image_chan_name,
    ):
        query = INSERT_WORKLOG_IMAGE.format(
            cons_code,
            co_code,
            cons_date,
            sys_doc_num,
            work_log_cons_code,
            cons_type_cd,
            file_index,
            image_title,
            image_path,
            image_orig_name,
            image_chan_name,
        )

        return query

    def select_worklog_image(
        self, cons_code, sysnum, co_code, cons_type_code, work_log_cons_code
    ):
        query = SELECT_WORKLOG_IMAGE.format(
            CONSCODE_CONDITION_A.format(cons_code),
            SYSDOCNUM_CONDITION_A.format(sysnum),
            COCODE_CONDITION_A.format(co_code),
            CONSTYPECODE_CONDITION.format(cons_type_code),
            LOGCONSCODE_CONDITION_A.format(work_log_cons_code),
        )

        return query

    def update_worklog_image(
        self, cons_code, sysnum, co_code, cons_type_code, index, title
    ):
        query = UPDATE_WORKLOG_IMAGE.format(
            title,
            CONSCODE_CONDITION.format(cons_code),
            SYSDOCNUM_CONDITION.format(sysnum),
            COCODE_CONDITION.format(co_code),
            LOGCONSCODE_CONDITION.format(cons_type_code),
            INDEX_CONDITION.format(index),
        )

        return query

    def select_worklog_image_for_delete(
        self, cons_code, sysnum, co_code, work_log_cons_code, index
    ):
        query = SELECT_WORKLOG_IMAGE_DELETE.format(
            CONSCODE_CONDITION_A.format(cons_code),
            COCODE_CONDITION_A.format(co_code),
            SYSDOCNUM_CONDITION_A.format(sysnum),
            LOGCONSCODE_CONDITION_A.format(work_log_cons_code),
            INDEX_CONDITION_A.format(index),
        )

        return query

    def delete_worklog_image_for_delete(
        self, cons_code, sysnum, co_code, work_log_cons_code
    ):
        query = DELETE_WORKLOG_IMAGE_DELETE.format(
            DELETE_CONSCODE_CONDITON.format(cons_code),
            DELETE_SYSDOCNUM_CONDITON.format(sysnum),
            DELETE_COCODE_CONDITON.format(co_code),
            DELETE_LOGCONSCODE_CONDITON.format(work_log_cons_code),
        )

        return query

    def delete_worklog_image(
        self, cons_code, sysnum, co_code, work_log_cons_code, index
    ):
        query = DELETE_WORKLOG_IMAGE.format(
            DELETE_CONSCODE_CONDITON.format(cons_code),
            DELETE_SYSDOCNUM_CONDITON.format(sysnum),
            DELETE_COCODE_CONDITON.format(co_code),
            DELETE_LOGCONSCODE_CONDITON.format(work_log_cons_code),
            DELETE_INDEX_CONDITION.format(index),
        )

        return query

    def select_worklog_manp(self, cons_code, sysnum, co_code):
        query = SELECT_WORKLOG_MANPOWER.format(
            CONSCODE_CONDITION_PD.format(cons_code),
            COCODE_CONDITION_B.format(co_code),
            SYSDOCNUM_CONDITION_B.format(sysnum),
            COCODE_CONDITION_B.format(co_code),
            CONSCODE_CONDITION_A.format(cons_code),
            SYSDOCNUM_CONDITION_A.format(sysnum),
            COCODE_CONDITION_A.format(co_code),
        )

        return query

    #### 조현우 문서 수정/열람 권한 체크추가 0210 ####
    #### 유저가 해당문서 수정/열람 권한이 있는지 확인한다
    @staticmethod
    def check_sysnum_userin(sys_doc_num, id):
        query = SELECT_WORKDIARY_USERIN.format(sys_doc_num, id)

        return query

    #### 회사가 해당문서 수정/열람 권한이 있는지 확인한다
    @staticmethod
    def check_sysnum_companyin(sys_doc_num, co_code):
        query = SELECT_WORKDIARY_COMPANYIN.format(sys_doc_num, co_code)

        return query

    #### 해당문서의 공사코드를 불러온다 ####
    @staticmethod
    def select_conscode(sys_doc_num):
        query = SELECT_WORKDIARY_CONSCODE.format(sys_doc_num)

        return query

    # 0203 희정 추가
    # 작업일지 데이터를 저장 한다.
    def iPutDiaryInfo(self, diaryInfo):
        query = INSERT_WORK_DIARY_INFO

        query += "VALUES("
        query += '"' + diaryInfo["cons_code"] + '", '
        query += '"' + diaryInfo["co_code"] + '", '
        query += "" + str(diaryInfo["sys_doc_num"]) + ", "
        query += '"' + diaryInfo["cons_date"] + '", '
        query += '"' + diaryInfo["work_title"] + '", '
        query += '"' + diaryInfo["work_diary_content"] + '", '
        query += '"' + diaryInfo["write_date"] + '", '
        query += '"' + diaryInfo["id"] + '", '
        query += '"' + diaryInfo["today_content"] + '", '
        query += '"' + diaryInfo["next_content"] + '", '
        query += str(diaryInfo["temperature"]) + ", "
        query += str(diaryInfo["sky_result"]) + ", "
        query += str(diaryInfo["pty_result"])
        query += ")"
        return query

    def update_Diary(
        self,
        work_diary_content,
        id,
        today_content,
        next_content,
        temperature,
        sky_result,
        pty_result,
        sys_num,
    ):
        query = UPDATE_WORK_DIARY_INFO.format(
            work_diary_content,
            id,
            today_content,
            next_content,
            temperature,
            sky_result,
            pty_result,
            sys_num,
        )

        return query

    def delete_Diary(self, sys_num):
        query = DELETE_WORK_DIARY.format(sys_num)

        return query

    # 0203 희정 추가
    # 작업일보 데이터를 저장 한다.
    def iPutWorkLogInfo(self, workLogInfo):
        query = INSERT_WORK_LOG_INFO

        query += "VALUES("
        query += '"' + workLogInfo["co_code"] + '", '
        query += "" + str(workLogInfo["sys_doc_num"]) + ", "
        query += '"' + workLogInfo["work_log_cons_code"] + '", '
        query += "" + str(workLogInfo["work_log_cons_lv1"]) + ", "
        query += "" + str(workLogInfo["work_log_cons_lv2"]) + ", "
        query += "" + str(workLogInfo["work_log_cons_lv3"]) + ", "
        query += "" + str(workLogInfo["work_log_cons_lv4"]) + ", "
        # query += '"' + str(workLogInfo["work_log_use_amount"]) + '", '
        # query += '"' + workLogInfo["work_log_content"] + '" '
        query += '"' + workLogInfo["cons_type_cd"] + '", '
        query += "" + str(workLogInfo["today_workload"]) + ", "
        query += "" + str(workLogInfo["next_workload"]) + " "
        query += ")"

        return query

    def insert_WorkLog(
        self,
        co_code,
        sys_doc_num,
        work_log_cons_code,
        work_log_cons_lv1,
        work_log_cons_lv2,
        work_log_cons_lv3,
        work_log_cons_lv4,
        cons_type_cd,
        today_workload,
        next_workload,
    ):
        query = INSERT_WORK_LOG.format(
            co_code,
            sys_doc_num,
            work_log_cons_code,
            work_log_cons_lv1,
            work_log_cons_lv2,
            work_log_cons_lv3,
            work_log_cons_lv4,
            cons_type_cd,
            today_workload,
            next_workload,
        )

        return query

    def update_WorkLog(
        self, today_workload, next_workload, sys_doc_num, worklog_cons_code
    ):
        query = UPDATE_WORK_LOG_INFO.format(
            today_workload, next_workload, sys_doc_num, worklog_cons_code
        )

        return query

    def update_prevworkload_post_log(
        self, cons_code, co_code, worklog_cons_code, cons_date
    ):
        query = UPDATE_WORK_LOG_PREV_WORKLOAD_INIT.format(
            CONSCODE_CONDITION_D.format(cons_code),
            COCODE_CONDITION_L.format(co_code),
            WORKLOGCONSCODE_CONDITON_L.format(worklog_cons_code),
            CONSDATE_UNDER_CONDITION_D.format(cons_date),
            CONSCODE_CONDITION_D.format(cons_code),
            COCODE_CONDITION_L.format(co_code),
            WORKLOGCONSCODE_CONDITON_L.format(worklog_cons_code),
            CONSDATE_CONDITION_D.format(cons_date),
        )

        return query

    def update_prevworkload_put_log(
        self, cons_code, co_code, worklog_cons_code, cons_date, today_workload
    ):
        query = UPDATE_WORK_LOG_PREV_WORKLOAD_CHAN.format(
            today_workload,
            CONSCODE_CONDITION_D.format(cons_code),
            COCODE_CONDITION_L.format(co_code),
            WORKLOGCONSCODE_CONDITON_L.format(worklog_cons_code),
            CONSDATE_CONDITION_D.format(cons_date),
            CONSCODE_CONDITION_D.format(cons_code),
            COCODE_CONDITION_L.format(co_code),
            WORKLOGCONSCODE_CONDITON_L.format(worklog_cons_code),
            CONSDATE_OVER_CONDITION_D.format(cons_date),
        )

        return query

    def update_prevworkload_put_log2(
        self, cons_code, co_code, worklog_cons_code, cons_date
    ):
        query = UPDATE_WORK_LOG_PREV_WORKLOAD_CHAN2.format(
            CONSCODE_CONDITION_D.format(cons_code),
            COCODE_CONDITION_L.format(co_code),
            WORKLOGCONSCODE_CONDITON_L.format(worklog_cons_code),
            CONSDATE_CONDITION_D.format(cons_date),
            CONSCODE_CONDITION_D.format(cons_code),
            COCODE_CONDITION_L.format(co_code),
            WORKLOGCONSCODE_CONDITON_L.format(worklog_cons_code),
            CONSDATE_OVER_CONDITION_D.format(cons_date),
        )

        return query

    def delete_Worklog(self, sys_doc_num, worklog_cons_code):
        query = DELETE_WORK_LOG.format(sys_doc_num, worklog_cons_code)

        return query

    # 0203 희정 추가
    # 작업일보/일지 이미지를 저장 한다.
    def iPutWorkImageFileInfo(self, dataInfo, fileIndex, fileDesc, fileData):
        query = INSERT_WORK_IMAGE_INFO

        query += "VALUES("
        query += '"' + dataInfo["cons_code"] + '", '
        query += '"' + dataInfo["co_code"] + '", '
        query += '"' + dataInfo["cons_date"] + '", '
        query += "" + str(dataInfo["sys_doc_num"]) + ", "
        query += '"' + dataInfo["work_log_cons_code"] + '", '
        query += '"' + fileDesc + '", '
        query += '"' + fileData["file_path"] + '", '
        query += '"' + fileData["file_original_name"] + '", '
        query += '"' + fileData["file_change_name"] + '", '
        query += '"' + dataInfo["write_date"] + '", '
        query += "" + fileIndex + ", "
        query += '"' + dataInfo["cons_type_cd"] + '" '
        query += ")"

        return query

    # 0207 희정 추가
    # 투입 인력 정보를 저장 한다.
    def iPutWorkManpowerInfo(self, dataInfo):
        query = INSERT_WORK_MANPOWER_INFO

        query += "VALUES("
        query += '"' + dataInfo["cons_code"] + '", '
        query += '"' + dataInfo["co_code"] + '", '
        query += '"' + dataInfo["cons_date"] + '", '
        query += "" + str(dataInfo["sys_doc_num"]) + ", "
        query += '"' + dataInfo["cons_type_cd"] + '", '
        query += '"' + dataInfo["work_log_cons_code"] + '", '
        query += "" + str(dataInfo["prev_manpower"]) + ", "
        query += "" + str(dataInfo["today_manpower"]) + ", "
        query += "" + str(dataInfo["next_manpower"]) + " "
        query += ")"

        return query

    def insert_WorkManpower(
        self,
        cons_code,
        co_code,
        cons_date,
        sys_doc_num,
        cons_type_cd,
        work_log_cons_code,
        prev_manpower,
        today_manpower,
        next_manpower,
    ):
        query = INSERT_WORK_MANPOWER.format(
            cons_code,
            co_code,
            cons_date,
            sys_doc_num,
            cons_type_cd,
            work_log_cons_code,
            prev_manpower,
            today_manpower,
            next_manpower,
        )

        return query

    def update_WorkManpower(
        self, today_manpower, next_manpower, sys_num, worklog_cons_code
    ):
        query = UPDATE_WORK_MANPOWER_INFO.format(
            today_manpower, next_manpower, sys_num, worklog_cons_code
        )

        return query

    def delete_WorkManpower(self, sys_num, worklog_cons_code):
        query = DELETE_WORK_MANPOWER.format(sys_num, worklog_cons_code)

        return query

    # 0203 희정 추가
    # 작업일지 데이터를 삭제 한다.
    def dDelDiaryInfo(self, consCode, coCode, sysDocNum):
        query = DELETE_WORK_DIARY_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += 'AND CO_CODE = "' + coCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""

        return query

    # 0203 희정 추가
    # 작업일보 데이터를 삭제 한다.
    def dDelWorkLogInfo(self, consCode, coCode, sysDocNum):
        query = DELETE_WORK_LOG_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += 'AND CO_CODE = "' + coCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""

        return query

    # 0203 희정 추가
    # 작업 일지/일보 이미지 데이터를 삭제 한다.
    def dDelImageFileInfo(self, consCode, coCode, sysDocNum):
        query = DELETE_WORK_IMAGE_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += 'AND CO_CODE = "' + coCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""

        return query

    # 0203 희정 추가
    # 관련 이미지 파일을 모두 가져 온다.
    def sGetImageFileInfo(self, consCode, coCode, sysDocNum):
        query = SELECT_WORK_DL_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += 'AND CO_CODE = "' + coCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""

        return query

    # 0203 희정 추가
    # 투입 인력 정보를 삭제 한다.
    def dDelWorkManpowerInfo(self, consCode, coCode, sysDocNum):
        query = DELETE_WORK_MANPOWER_INFO

        query += 'AND CONS_CODE = "' + consCode + '" '
        query += 'AND CO_CODE = "' + coCode + '" '
        query += "AND SYS_DOC_NUM = " + str(sysDocNum) + ""

        return query

    @staticmethod
    def select_workload(cons_code, co_code):
        query = SELECT_WORKLOAD.format(
            f"AND D.CONS_CODE = '{cons_code}'",
            f"AND D.CO_CODE = '{co_code}'",
        )

        return query









