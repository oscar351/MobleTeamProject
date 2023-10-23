"""
공정내역서 등록 DB

PROCESS_DETAIL DB info
CONS_CODE (PK)      : 공사코드
CO_CODE (PK)
LEVEL1 (pk)
LEVEL2 (pk)
LEVEL3 (pk)
LEVEL4 (PK)
PRODUCT (PK)
STANDARD (PK)
UN_CODE
QUANTITY
UNIT_PRICE
TOTAL_PRICE
REG_DATE
"""

INSERT_PCCODE = " ".join(
    [
        "INSERT INTO",
        "SUBCODE_MANAGE",
        "(SUBCODE, CODE, SUBCODE_NAME, SUBCODE_EXPLAIN, FULLCODE)",
        "VALUES('{}', 'PC00', '{}', '{}', '{}')",
    ]
)

INSERT_PROCESSDETAIL_HEAD = " ".join(
    [
        "INSERT INTO",
        "PROCESS_DETAIL",
        "(CONS_CODE, CO_CODE, LEVEL1, LEVEL2, LEVEL3, LEVEL4, LEVEL1_NAME, LEVEL2_NAME, LEVEL3_NAME,",
        "PC_CODE, PC_NAME, PRODUCT, STANDARD, UNIT, QUANTITY, MATERIAL_UNIT_PRICE, MATERIAL_PRICE, LABOR_UNIT_PRICE, LABOR_PRICE, START_DATE, END_DATE, UPDATED)",
        "VALUES",
    ]
)

INSERT_PROCESSDETAIL_BODY = " ".join(
    [
        "('{}', '{}', {}, {}, {}, {}, '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, 1)",
    ]
)

# 이미 데이터가 존재 시 업데이트
INSERT_PROCESSDETAIL_FOOT = " ".join(
    [
        "ON DUPLICATE KEY UPDATE",
        "LEVEL1_NAME = VALUES(LEVEL1_NAME),",
        "LEVEL2_NAME = VALUES(LEVEL2_NAME),",
        "LEVEL3_NAME = VALUES(LEVEL3_NAME),",
        "PC_CODE = VALUES(PC_CODE),",
        "PC_NAME = VALUES(PC_NAME),",
        "PRODUCT = VALUES(PRODUCT),",
        "STANDARD = VALUES(STANDARD),",
        "UNIT = VALUES(UNIT),",
        "QUANTITY = VALUES(QUANTITY),",
        "MATERIAL_UNIT_PRICE = VALUES(MATERIAL_UNIT_PRICE),",
        "MATERIAL_PRICE = VALUES(MATERIAL_PRICE),",
        "LABOR_UNIT_PRICE = VALUES(LABOR_UNIT_PRICE),",
        "LABOR_PRICE = VALUES(LABOR_PRICE),",
        "START_DATE = VALUES(START_DATE),",
        "END_DATE = VALUES(END_DATE),",
        "UPDATED = 2",
    ]
)

DELETE_PROCESSDETAIL_OLD = " ".join(
    [
        "DELETE",
        "FROM PROCESS_DETAIL",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

UPDATE_PROCESSDETAIL_NEW = " ".join(
    [
        "UPDATE",
        "PROCESS_DETAIL",
        "SET UPDATED = 0",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

SELECT_PCCODE_INDEX = " ".join(
    ["SELECT", "COUNT(*) as count", "FROM SUBCODE_MANAGE", "WHERE CODE = 'PC00'"]
)

SELECT_PROCESSDETAIL_BASE = " ".join(
    [
        "SELECT",
        "CONS_CODE as cons_code,",
        "CO_CODE as co_code,",
        "PC_CODE as pc_code,",
        "PC_NAME as pc_name,",
        "LEVEL1 as level1,",
        "LEVEL2 as level2,",
        "LEVEL3 as level3,",
        "LEVEL4 as level4,",
        "LEVEL1_NAME as level1_name,",
        "LEVEL2_NAME as level2_name,",
        "LEVEL3_NAME as level3_name,",
        "PRODUCT as product,",
        "STANDARD as standard,",
        "UNIT as unit,",
        "QUANTITY as quantity,",
        "MATERIAL_UNIT_PRICE as material_unit_price,",
        "MATERIAL_PRICE as material_price,",
        "LABOR_UNIT_PRICE as labor_unit_price,",
        "LABOR_PRICE as labor_price,",
        "date_format(START_DATE, '%Y%m%d%H%i%S') as start_date,",
        "date_format(END_DATE, '%Y%m%d%H%i%S') as end_date",
        "FROM PROCESS_DETAIL",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

SELECT_PROCESSDETAIL = " ".join(
    [
        "SELECT",
        "CONS_CODE as cons_code,",
        "CO_CODE as co_code,",
        "PC_CODE as pc_code,",
        "0 as prev_work,",
        "LEVEL1 as level1,",
        "LEVEL2 as level2,",
        "LEVEL3 as level3,",
        "LEVEL4 as level4,",
        "CONCAT(LPAD(LEVEL1, 2, '0'), LPAD(LEVEL2, 2, '0'), LPAD(LEVEL3, 2, '0'), LPAD(LEVEL4, 3, '0')) as item_code,",
        "PRODUCT as product,",
        "STANDARD as standard,",
        "UNIT as unit,",
        "ROUND(CAST(QUANTITY / 100 AS FLOAT), 2) as quantity,",
        "ROUND(CAST(USED_QUANTITY / 100 AS FLOAT), 2) as used_quantity,",
        "ROUND(CAST(GREATEST(0.00, LEAST(1.00, (datediff(CURRENT_TIMESTAMP(), START_DATE) + 1) / (abs(datediff(END_DATE, START_DATE)) + 1))) * QUANTITY / 100 AS FLOAT), 2) as planned_quantity,"
        "ROUND(CAST(MATERIAL_UNIT_PRICE * QUANTITY / 100 AS UNSIGNED), 0) as material_price,",
        "ROUND(CAST(LABOR_UNIT_PRICE * QUANTITY / 100 AS UNSIGNED), 0) as labor_price,",
        "ROUND(CAST((MATERIAL_UNIT_PRICE + LABOR_UNIT_PRICE) * QUANTITY / 100 AS UNSIGNED), 0) as total_price,",
        "ROUND(CAST((MATERIAL_UNIT_PRICE + LABOR_UNIT_PRICE) * USED_QUANTITY / 100 AS UNSIGNED), 0) as used_price,"
        "ROUND(CAST(USED_QUANTITY / QUANTITY * 100 AS FLOAT), 2) as used_percent,",
        "date_format(START_DATE, '%Y%m%d') as start_date,",
        "date_format(END_DATE, '%Y%m%d') as end_date,",
        "abs(datediff(END_DATE, START_DATE)) + 1 as duration,",
        "LEVEL1_NAME as level1_name,",
        "LEVEL2_NAME as level2_name,",
        "LEVEL3_NAME as level3_name",
        "FROM PROCESS_DETAIL",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

SELECT_PROCESSDETAIL_ALL = " ".join(
    [
        "SELECT",
        "PC_CODE as pc_code,",
        "PC_NAME as pc_name,",
        "LEVEL1 as level1,",
        "LEVEL1_NAME as level1_name,",
        "COUNT(*) as count",
        "FROM PROCESS_DETAIL",
        "WHERE 1=1",
        "{}",
        "{}",
        "GROUP BY LEVEL1, PC_CODE",
    ]
)

DELETE_PROCESSDETAIL_ALL = " ".join(
    [
        "DELETE",
        "FROM PROCESS_DETAIL",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

SELECT_PROCESSDETAIL_NAME = " ".join(
    [
        "SELECT",
        "LEVEL1_NAME as level1_name,",
        "LEVEL2_NAME as level2_name,",
        "LEVEL3_NAME as level3_name",
        "FROM PROCESS_DETAIL",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
    ]
)

SELECT_PROCESSDETAIL_DATE = " ".join(
    [
        "SELECT",
        "date_format(START_DATE, '%Y%m%d') as start_date,",
        "date_format(END_DATE, '%Y%m%d') as end_date",
        "FROM PROCESS_DETAIL",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

INSERT_PROCESSCODE = " ".join(
    [
        "INSERT INTO",
        "SUBCODE_MANAGE(SUBCODE, CODE, SUBCODE_NAME, SUBCODE_EXPLAIN, FULLCODE)",
        "VALUES({}, {}, {}, {}, {})",
    ]
)

SELECT_PROCESSCODE = " ".join(
    [
        "SELECT",
        "FULLCODE as code,",
        "SUBCODE_NAME as name",
        "FROM SUBCODE_MANAGE",
        "WHERE 1=1",
        "AND CODE = 'PC00'",
    ]
)

SELECT_PROCESSCODE_LEVEL1 = " ".join(
    [
        "SELECT",
        "DISTINCT",
        "LEVEL1 as level1,",
        "LEVEL1_NAME as level1_name",
        "FROM PROCESS_DETAIL",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

SELECT_PROCESSCODE_LEVEL2 = " ".join(
    [
        "SELECT",
        "DISTINCT",
        "LEVEL2 as level2,",
        "LEVEL2_NAME as level2_name",
        "FROM PROCESS_DETAIL",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
    ]
)

SELECT_PROCESSCODE_LEVEL3 = " ".join(
    [
        "SELECT",
        "DISTINCT",
        "LEVEL3 as level3,",
        "LEVEL3_NAME as level3_name",
        "FROM PROCESS_DETAIL",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
    ]
)

SELECT_PROCESSCODE_LEVEL4 = " ".join(
    [
        "SELECT",
        "DISTINCT",
        "LEVEL4 as level4,",
        "PRODUCT as product,",
        "STANDARD as standard,",
        "UNIT as unit,",
        "QUANTITY as quantity,",
        "MATERIAL_UNIT_PRICE as material_unit_price,",
        "MATERIAL_PRICE as material_price,",
        "LABOR_UNIT_PRICE as labor_unit_price,",
        "LABOR_PRICE as labor_price,",
        "date_format(START_DATE, '%Y%m%d%H%i%S') as start_date,",
        "date_format(END_DATE, '%Y%m%d%H%i%S') as end_date",
        "FROM PROCESS_DETAIL",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
    ]
)

COUNT_PROCESSDETAIL_BYPC = " ".join(
    [
        "SELECT C.PC_NAME as pc_name,",
        "CAST(SUM(I.QUANTITY * (I.MATERIAL_UNIT_COST + I.LABOR_UNIT_COST + I.OTHER_UNIT_COST) / 100) as UNSIGNED) as pc_cost,",
        "date_format(C.START_DATE_1, '%Y%m%d') as start_date,",
        "GREATEST(",
        "date_format(C.END_DATE_1, '%Y%m%d'),",
        "CASE WHEN C.END_DATE_2 IS NOT NULL THEN date_format(C.END_DATE_2, '%Y%m%d') ELSE '00000000' END,",
        "CASE WHEN C.END_DATE_3 IS NOT NULL THEN date_format(C.END_DATE_3, '%Y%m%d') ELSE '00000000' END,",
        "CASE WHEN C.END_DATE_4 IS NOT NULL THEN date_format(C.END_DATE_4, '%Y%m%d') ELSE '00000000' END",
        ") as end_date",
        "FROM PROCESS_CHANGE_CODE C",
        "JOIN PROCESS_CHANGE_COST I ON C.PC_NAME = I.PC_NAME",
        "WHERE 1=1",
        "AND C.CONS_CODE = {}",
        "{}",
        "GROUP BY C.PC_NAME",
        "ORDER BY C.START_DATE_1, PC_NAME",
    ]
)

COUNT_PROCESSDETAIL = " ".join(
    [
        "SELECT",
        "date_format(D.CONS_DATE, '%Y%m%d') cons_date,",
        "CAST(SUM(L.TODAY_WORKLOAD * (P.MATERIAL_UNIT_PRICE + P.LABOR_UNIT_PRICE) / 100) AS UNSIGNED) AS used_price,",
        "CAST(SUM(SUM(L.TODAY_WORKLOAD * (P.MATERIAL_UNIT_PRICE + P.LABOR_UNIT_PRICE) / 100)) OVER (PARTITION BY D.CONS_CODE, D.CO_CODE ORDER BY D.CONS_DATE) AS UNSIGNED) AS acc_price",
        "FROM WORK_LOG_MANAGE L",
        "JOIN WORK_DIARY_MANAGE D",
        "ON L.SYS_DOC_NUM = D.SYS_DOC_NUM",
        "JOIN PROCESS_DETAIL P",
        "ON D.CONS_CODE = P.CONS_CODE AND D.CO_CODE = P.CO_CODE",
        "AND (L.WORK_LOG_CONS_LV1 = P.LEVEL1 AND L.WORK_LOG_CONS_LV2 = P.LEVEL2 AND L.WORK_LOG_CONS_LV3 = P.LEVEL3 AND L.WORK_LOG_CONS_LV4 = P.LEVEL4)",
        "WHERE 1=1",
        "{}",
        "{}",
        "GROUP BY D.CONS_CODE, D.CO_CODE, D.CONS_DATE",
        "ORDER BY D.CONS_CODE, D.CO_CODE, D.CONS_DATE",
    ]
)

COUNT_PROCESSBASE_BYLEVEL = " ".join(
    [
        "SELECT",
        "CONS_CODE as cons_code,",
        "CO_CODE as co_code,",
        "LEVEL1 as cons_num,",
        "LEVEL1_NAME as cons_name,",
        "date_format(date_add(MIN(START_DATE), interval -1 day), '%Y%m%d')  AS cons_date,",
        "0 as used_price,",
        "CAST(SUM(QUANTITY * (MATERIAL_UNIT_PRICE + LABOR_UNIT_PRICE) / 100) AS UNSIGNED) AS total_price,",
        "0 AS rate,",
        "date_format(MIN(START_DATE), '%Y%m%d')  AS start_date,",
        "date_format(MAX(END_DATE), '%Y%m%d') AS end_date",
        "FROM SPACEDB.PROCESS_DETAIL",
        "WHERE 1=1",
        "{}",
        "{}",
        "GROUP BY LEVEL1",
        "ORDER BY LEVEL1",
    ]
)

COUNT_PROCESSDETAIL_BYLEVEL = " ".join(
    [
        "SELECT",
        "L.WORK_LOG_CONS_LV1 as cons_num,",
        "P.LEVEL1_NAME as cons_name,",
        "date_format(D.CONS_DATE, '%Y%m%d') cons_date,",
        "CAST(SUM(L.TODAY_WORKLOAD * (P.MATERIAL_UNIT_PRICE + P.LABOR_UNIT_PRICE) / 100) AS UNSIGNED) AS used_price,",
        "CAST(SUM(L.TODAY_WORKLOAD * (P.MATERIAL_UNIT_PRICE + P.LABOR_UNIT_PRICE) / 100) OVER (PARTITION BY D.CONS_CODE, D.CO_CODE, L.WORK_LOG_CONS_LV1 ORDER BY  D.CONS_CODE, D.CO_CODE, D.CONS_DATE, L.WORK_LOG_CONS_LV1) AS UNSIGNED) as acc_price",
        "FROM WORK_LOG_MANAGE L",
        "JOIN WORK_DIARY_MANAGE D",
        "ON L.SYS_DOC_NUM = D.SYS_DOC_NUM",
        "JOIN PROCESS_DETAIL P",
        "ON D.CONS_CODE = P.CONS_CODE AND D.CO_CODE = P.CO_CODE",
        "AND (L.WORK_LOG_CONS_LV1 = P.LEVEL1 AND L.WORK_LOG_CONS_LV2 = P.LEVEL2 AND L.WORK_LOG_CONS_LV3 = P.LEVEL3 AND L.WORK_LOG_CONS_LV4 = P.LEVEL4)",
        "WHERE 1=1",
        "{}",
        "{}",
        "GROUP BY D.CONS_CODE, D.CO_CODE, L.WORK_LOG_CONS_LV1, D.CONS_DATE",
        "ORDER BY D.CONS_CODE, D.CO_CODE, L.WORK_LOG_CONS_LV1, D.CONS_DATE",
    ]
)
UPDATE_PROCESSDETAIL_AUTO = " ".join(
    [
        "SELECT SUM(L.TODAY_WORKLOAD) INTO @quantity",
        "FROM WORK_LOG_MANAGE L",
        "JOIN WORK_DIARY_MANAGE D",
        "ON L.SYS_DOC_NUM = D.SYS_DOC_NUM",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
        "{};",
        "UPDATE",
        "PROCESS_DETAIL",
        "SET",
        "USED_QUANTITY = IFNULL(@quantity, 0)",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
    ]
)

WORKDIARY_CONSCODE_CONDITION = "AND D.CONS_CODE = '{}'"
WORKDIARY_COSCODE_CONDITION = "AND D.CO_CODE = '{}'"
WORKLOG_LEVEL1_CONDITION = "AND L.WORK_LOG_CONS_LV1 = {}"
WORKLOG_LEVEL2_CONDITION = "AND L.WORK_LOG_CONS_LV2 = {}"
WORKLOG_LEVEL3_CONDITION = "AND L.WORK_LOG_CONS_LV3 = {}"
WORKLOG_LEVEL4_CONDITION = "AND L.WORK_LOG_CONS_LV4 = {}"


DELETE_PROCESSDETAIL = " ".join(
    [
        "DELETE",
        "FROM PROCESS_DETAIL",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

PROCESSDETAIL_CONSCODE_CONDITION_D = "AND D.CONS_CODE = '{}'"
PROCESSDETAIL_COSCODE_CONDITION_D = "AND D.CO_CODE = '{}'"
PROCESSDETAIL_INDEX_CONDITION_D = "AND D.FILE_INDEX = {}"
PROCESSDETAIL_CONSCODE_CONDITION = "AND CONS_CODE = '{}'"
PROCESSDETAIL_COSCODE_CONDITION = "AND CO_CODE = '{}'"
PROCESSDETAIL_INDEX_CONDITION = "AND FILE_INDEX = {}"
PROCESSDETAIL_PCCODE_CONDITION = "AND PC_CODE = '{}'"
PROCESSDETAIL_CONSTYPECD_CONDITION = "AND CONS_TYPE_CD = '{}'"
PROCESSDETAIL_CONSDATE_CONDITION = "AND CONS_DATE < '{}'"
PROCESSDETAIL_LEVEL1_CONDITION = "AND LEVEL1 = {}"
PROCESSDETAIL_LEVEL2_CONDITION = "AND LEVEL2 = {}"
PROCESSDETAIL_LEVEL3_CONDITION = "AND LEVEL3 = {}"
PROCESSDETAIL_LEVEL4_CONDITION = "AND LEVEL4 = {}"

PROCESSDETAIL_MAXINDEX_CONDITION_D = " ".join(
    [
        "AND (D.CONS_CODE, D.CO_CODE, D.FILE_INDEX)",
        "IN (SELECT CONS_CODE, CO_CODE, MAX(FILE_INDEX) FROM PROCESS_DETAIL GROUP BY CONS_CODE, CO_CODE)",
    ]
)
PROCESSDETAIL_MAXINDEX_CONDITION_P = " ".join(
    [
        "AND (P.CONS_CODE, P.CO_CODE, P.FILE_INDEX)",
        "IN (SELECT CONS_CODE, CO_CODE, MAX(FILE_INDEX) FROM PROCESS_DETAIL GROUP BY CONS_CODE, CO_CODE)",
    ]
)
PROCESSDETAIL_MAXINDEX_CONDITION = " ".join(
    [
        "AND (CONS_CODE, CO_CODE, FILE_INDEX)",
        "IN (SELECT CONS_CODE, CO_CODE, MAX(FILE_INDEX) FROM PROCESS_DETAIL GROUP BY CONS_CODE, CO_CODE)",
    ]
)


"""
공정내역서 파일 DB

PROCESS_DETAIL_FILE DB info
CONS_CODE (PK)  공사코드
CO_CODE (PK)    회사코드
FILE_INDEX (PK) 파일번호
ORIG_NAME       원본파일명
CHAN_NAME       변경파일명
"""

SELECT_PROCESS_DETAIL_FILE_LIST = " ".join(
    [
        "SELECT",
        "FILE_INDEX as file_index,",
        "FILE_PATH as file_path,",
        "ORIG_NAME as orig_name,",
        "CHAN_NAME as chan_name,",
        "UPLOADED as uploaded,",
        "date_format(REG_DATE, '%Y%m%d') AS reg_date",
        "FROM PROCESS_DETAIL_FILE",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

INSERT_PROCESS_DETAIL_FILE = " ".join(
    [
        "INSERT INTO",
        "PROCESS_DETAIL_FILE(CONS_CODE, CO_CODE, FILE_PATH, ORIG_NAME, CHAN_NAME, CHANGE_DATE, WRITER_ID, POST_UUID, UPLOADED)",
        "VALUES({}, {}, {}, {}, {}, {}, {}, {}, {})",
    ]
)

SELECT_PROCESS_DETAIL_FILE_INDEX = " ".join(
    [
        "SELECT",
        "FILE_INDEX as file_index",
        "FROM",
        "PROCESS_DETAIL_FILE",
        "WHERE 1=1",
        "{}",
    ]
)

SELECT_PROCESS_DETAIL_FILE = " ".join(
    [
        "SELECT",
        "FILE_INDEX as file_index,",
        "FILE_PATH as file_path,",
        "ORIG_NAME as orig_name,",
        "CHAN_NAME as chan_name,",
        "date_format(REG_DATE, '%Y%m%d') AS reg_date,",
        "date_format(CHANGE_DATE, '%Y%m%d') AS change_date",
        "FROM PROCESS_DETAIL_FILE",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

UPDATE_PROCESS_DETAIL_FILE_UPLOAD = " ".join(
    [
        "UPDATE",
        "PROCESS_DETAIL_FILE",
        "SET UPLOADED = CASE",
        "WHEN {} THEN 2",
        "WHEN UPLOADED != 0 THEN 1 ELSE 0 END",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

UPDATE_PROCESS_DETAIL_FILE_APPROVE = " ".join(
    [
        "UPDATE",
        "PROCESS_DETAIL_FILE",
        "SET UPLOADED = CASE",
        "WHEN {} THEN 2",
        "WHEN UPLOADED != 0 THEN 1 ELSE 0 END",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

DELETE_PROCESS_DETAIL_FILE = " ".join(
    [
        "DELETE",
        "FROM PROCESS_DETAIL_FILE",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

"""
공정내역서 품목 DB

PROCESS_CHANHE_COST DB info
CONS_CODE (PK)
CO_CODE (PK)
PC_NAME (PK)
DESCRIPTION (PK)
STANDARD
VENDOR
UNIT
QUANTITY
HEAD
MATERIAL_UNIT_COST
LABOR_UNIT_COST
OTHER_UNIT_COST
"""

INSERT_ITEM_HEAD = " ".join(
    [
        "INSERT",
        "INTO",
        "PROCESS_CHANGE_COST(CONS_CODE, CO_CODE, PC_NAME, DESCRIPTION, STANDARD,",
        "VENDOR, UNIT, QUANTITY, HEAD, MATERIAL_UNIT_COST, LABOR_UNIT_COST, OTHER_UNIT_COST)",
        "VALUES",
    ]
)

INSERT_ITEM_BODY = " ".join(["({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"])

INSERT_ITEM_FOOT = " ".join(
    [
        "ON DUPLICATE KEY UPDATE",
        "QUANTITY = QUANTITY + VALUES(QUANTITY)",
    ]
)

SELECT_ITEM = " ".join(
    [
        "SELECT",
        "PC_NAME as pc_name,",
        "DESCRIPTION as description,",
        "STANDARD as standard,",
        "VENDOR as vendor,",
        "UNIT as unit,",
        "QUANTITY as quantity,",
        "HEAD as head,",
        "MATERIAL_UNIT_COST as material_unit_cost,",
        "LABOR_UNIT_COST as labor_unit_cost,",
        "OTHER_UNIT_COST as other_unit_cost",
        "FROM",
        "PROCESS_CHANGE_COST",
        "WHERE 1=1",
        "AND CONS_CODE = {}",
        "AND CO_CODE = {}",
    ]
)

UPDATE_ITEM = " ".join(
    [
        "UPDATE",
        "PROCESS_CHANGE_COST",
        "SET VENDOR = {}, UNIT = {}, QUANTITY = {}, HEAD = {},",
        "MATERIAL_UNIT_COST = {}, LABOR_UNIT_COST = {}, OTHER_UNIT_COST = {}",
        "WHERE 1=1",
        "AND CONS_CODE = {}",
        "AND CO_CODE = {}",
        "AND PC_NAME = {}",
        "AND DESCRIPTION = {}",
        "AND STANDARD = {}",
    ]
)

DELETE_ITEM = " ".join(
    [
        "DELETE",
        "FROM",
        "PROCESS_CHANGE_COST",
        "WHERE 1=1",
        "AND CONS_CODE = {}",
        "AND CO_CODE = {}",
        "AND PC_NAME = {}",
        "AND DESCRIPTION = {}",
        "AND STANDARD = {}",
    ]
)

"""
공정내역서 공종 DB

PROCESS_CHANHE_CODE DB info
CONS_CODE (PK)
CO_CODE (PK)
PC_NAME (PK)
PC_EXPLAIN
START_DATE_1
END_DATE_1
CONTENT_1
START_DATE_2
END_DATE_2
CONTENT_2
START_DATE_3
END_DATE_3
CONTENT_3
START_DATE_4
END_DATE_4
CONTENT_4
"""

INSERT_PC_HEAD = " ".join(
    [
        "INSERT",
        "INTO",
        "PROCESS_CHANGE_CODE(CONS_CODE, CO_CODE, PC_NAME, PC_EXPLAIN,"
        "START_DATE_1, END_DATE_1, CONTENT_1, START_DATE_2, END_DATE_2, CONTENT_2,",
        "START_DATE_3, END_DATE_3, CONTENT_3, START_DATE_4, END_DATE_4, CONTENT_4)",
        "VALUES",
    ]
)

INSERT_PC_BODY = " ".join(
    ["({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"]
)

INSERT_PC_FOOT = " ".join(
    [
        "ON DUPLICATE KEY UPDATE",
        "PC_EXPLAIN = VALUES(PC_EXPLAIN),",
        "START_DATE_1 = VALUES(START_DATE_1),",
        "END_DATE_1 = VALUES(END_DATE_1),",
        "CONTENT_1 = VALUES(CONTENT_1),",
        "START_DATE_2 = VALUES(START_DATE_2),",
        "END_DATE_2 = VALUES(END_DATE_2),",
        "CONTENT_2 = VALUES(CONTENT_2),",
        "START_DATE_3 = VALUES(START_DATE_3),",
        "END_DATE_3 = VALUES(END_DATE_3),",
        "CONTENT_3 = VALUES(CONTENT_3),",
        "START_DATE_4 = VALUES(START_DATE_4),",
        "END_DATE_4 = VALUES(END_DATE_4),",
        "CONTENT_4 = VALUES(CONTENT_4)",
    ]
)

SELECT_PC = " ".join(
    [
        "SELECT",
        "PC_NAME as pc_name,",
        "PC_EXPLAIN as pc_explain,",
        "date_format(START_DATE_1, '%Y%m%d') as start_date_1,",
        "date_format(END_DATE_1, '%Y%m%d') as end_date_1,",
        "CONTENT_1 as content_1,",
        "date_format(START_DATE_2, '%Y%m%d') as start_date_2,",
        "date_format(END_DATE_2, '%Y%m%d') as end_date_2,",
        "CONTENT_2 as content_2,",
        "date_format(START_DATE_3, '%Y%m%d') as start_date_3,",
        "date_format(END_DATE_3, '%Y%m%d') as end_date_3,",
        "CONTENT_3 as content_3,",
        "date_format(START_DATE_4, '%Y%m%d') as start_date_4,",
        "date_format(END_DATE_4, '%Y%m%d') as end_date_4,",
        "CONTENT_4 as content_4",
        "FROM",
        "PROCESS_CHANGE_CODE",
        "WHERE 1=1",
        "AND CONS_CODE = {}",
        "AND CO_CODE = {}",
    ]
)

DELETE_PC_ALL = " ".join(
    [
        "DELETE",
        "FROM",
        "PROCESS_CHANGE_CODE",
        "WHERE 1=1",
        "AND CONS_CODE = {}",
        "AND CO_CODE = {}",
    ]
)


"""
20230417 조현우 추가
공종 설정 - global : SUBCODE_MANAGE, local : PROJECT_PROCESS_CODE

SUBCODE_MANAGE

SUBCODE         : 하위코드
CODE            : 상위코드
SUBCODE_NAME    : 코드명
SUBCODE_EXPLAIN : 코드설명
FULLCODE        : 전체코드

PROJECT_PROCESS_CODE

CONS_CODE (PK, FK)  : 프로젝트명
CO_CODE (PK, FK)    : 회사명
PC_CODE (PK, FK)    : 공종코드명
PC_NAME (FK)        : 공종명

"""

INSERT_GLOBAL_PC = " ".join(
    [
        "INSERT INTO",
        "SUBCODE_MANAGE(SUBCODE, CODE, SUBCODE_NAME, SUBCODE_EXPLAIN, FULLCODE)",
        "VALUES({}, {}, {}, {}, {})",
    ]
)

SELECT_GLOBAL_PC = " ".join(
    [
        "SELECT",
        "FULLCODE as pc_code,",
        "SUBCODE_NAME as pc_name,",
        "SUBCODE_EXPLAIN as pc_explain",
        "FROM SUBCODE_MANAGE",
        "WHERE CODE = 'PC00'",
        "ORDER BY SUBCODE",
    ]
)

UPDATE_GLOBAL_PC = " ".join(
    [
        "UPDATE",
        "SUBCODE_MANAGE",
        "SET SUBCODE_NAME = %s, SUBCODE_EXPLAIN = %s",
        "WHERE CODE = 'PC00'",
        "AND SUBCODE = {}",
    ]
)

DELETE_GLOBAL_PC = " ".join(
    [
        "DELETE",
        "FROM SUBCODE_MANAGE",
        "WHERE CODE = 'PC00'",
        "AND SUBCODE = {}",
    ]
)

INSERT_LOCAL_PC = " ".join(
    [
        "INSERT INTO",
        "PROJECT_PROCESS_CODE(CONS_CODE, CO_CODE, PC_CODE)",
        "VALUES({}, {}, {})",
    ]
)

SELECT_LOCAL_PC = " ".join(
    [
        "SELECT",
        "CONS_CODE as cons_code,",
        "CO_CODE as co_code,",
        "PC_CODE as pc_code,",
        "PC_NAME as pc_name,",
        "PC_EXPLAIN as pc_explain",
        "FROM PROJECT_PROCESS_CODE",
        "WHERE CONS_CODE = {}",
        "AND CO_CODE = {}",
        "ORDER BY PC_CODE",
    ]
)

DELETE_LOCAL_PC = " ".join(
    [
        "DELETE",
        "FROM PROJECT_PROCESS_CODE",
        "WHERE CONS_CODE = {}",
        "AND CO_CODE = {}",
        "AND PC_CODE = {}",
    ]
)


class sqlProjectProcessManage:
    """공정상세내역서 관리 Query Class"""

    @staticmethod
    def insert_PCcode(index, name, Excode):
        query = INSERT_PCCODE.format(f"{index:04}", name, Excode, f"PC00{index:04}")

        return query

    @staticmethod
    def insert_head():
        query = INSERT_PROCESSDETAIL_HEAD.strip()
        return query

    @staticmethod
    def insert_body(
        cons_code: str,
        co_code: str,
        pc_code: str,
        pc_name: str,
        level1: int,
        level2: int,
        level3: int,
        level4: int,
        level1_name: str,
        level2_name: str,
        level3_name: str,
        product: int,
        standard: str,
        unit: str,
        quantity: str,
        material_unit_price: str,
        material_price: str,
        labor_unit_price: int,
        labor_price: int,
        start_date: str,
        end_date: str,
    ) -> str:
        """공정상세내역서 추가 query"""

        query = INSERT_PROCESSDETAIL_BODY.format(
            cons_code,
            co_code,
            level1,
            level2,
            level3,
            level4,
            level1_name,
            level2_name,
            level3_name,
            f"'{pc_code}'" if pc_code != "" else "NULL",
            f"'{pc_name}'" if pc_name != "" else "NULL",
            product,
            standard,
            f"{unit}" if unit != "" else "개",
            quantity if quantity != 0 else 100,
            material_unit_price,
            material_price,
            labor_unit_price,
            labor_price,
            f"'{start_date}'" if start_date != "" else "NULL",
            f"'{end_date}'" if end_date != "" else "NULL",
        ).strip()

        return query

    @staticmethod
    def insert_foot():
        query = INSERT_PROCESSDETAIL_FOOT.strip()
        return query

    @staticmethod
    def delete_old(cons_code, co_code):
        "삭제 품목 제거"
        query = DELETE_PROCESSDETAIL_OLD.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'",
            f"AND UPDATED = 0",
        )
        return query

    @staticmethod
    def update_new(cons_code, co_code):
        "업데이트 완료 표시"
        query = UPDATE_PROCESSDETAIL_NEW.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'",
        )
        return query

    @staticmethod
    def select_base(cons_code, co_code):
        """공정상세내역서 기본데이터 추출"""
        query = SELECT_PROCESSDETAIL_BASE.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'",
        )

        return query

    @staticmethod
    def select(cons_code: str, co_code: str, pc_code: str, cons_date: str) -> str:
        """공정상세내역서 검색 query"""

        query = SELECT_PROCESSDETAIL.format(
            PROCESSDETAIL_CONSCODE_CONDITION.format(cons_code),
            PROCESSDETAIL_COSCODE_CONDITION.format(co_code),
            PROCESSDETAIL_PCCODE_CONDITION.format(pc_code),
            PROCESSDETAIL_CONSDATE_CONDITION.format(cons_date),
            PROCESSDETAIL_CONSCODE_CONDITION.format(cons_code),
            PROCESSDETAIL_COSCODE_CONDITION.format(co_code),
            PROCESSDETAIL_PCCODE_CONDITION.format(pc_code),
        ).strip()

        return query

    @staticmethod
    def select_all(cons_code: str, co_code: str, index: int) -> str:
        """공정상세내역서 전체 조회 query"""

        query = SELECT_PROCESSDETAIL_ALL.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'",
        ).strip()

        return query

    @staticmethod
    def delete_all(cons_code: str, co_code: str) -> str:
        """공정상세내역서 전체 삭제 query"""

        query = DELETE_PROCESSDETAIL_ALL.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'",
        ).strip()

        return query

    @staticmethod
    def select_names(
        cons_code: str, co_code: str, level1: int, level2: int, level3: int
    ) -> str:
        """공정상세내역서 검색 query"""

        query = SELECT_PROCESSDETAIL_NAME.format(
            PROCESSDETAIL_CONSCODE_CONDITION.format(cons_code),
            PROCESSDETAIL_COSCODE_CONDITION.format(co_code) if co_code != "" else "",
            PROCESSDETAIL_LEVEL1_CONDITION.format(level1),
            PROCESSDETAIL_LEVEL1_CONDITION.format(level2),
            PROCESSDETAIL_LEVEL1_CONDITION.format(level3),
        ).strip()

        return query

    @staticmethod
    def select_date(cons_code: str, co_code: str) -> str:
        """공정상세도 공사기간 조회 query"""

        query = SELECT_PROCESSDETAIL_DATE.format(
            PROCESSDETAIL_CONSCODE_CONDITION.format(cons_code),
            PROCESSDETAIL_COSCODE_CONDITION.format(co_code),
        ).strip()

        return query

    @staticmethod
    def select_PCcode() -> str:
        """공정상세명 검색 query"""

        query = SELECT_PROCESSCODE

        return query

    def select_PCcode_index() -> str:
        """공정코드 총 개수"""

        query = SELECT_PCCODE_INDEX

        return query

    @staticmethod
    def count_bypc(cons_code: str, co_code: str) -> str:
        """공정상세내역서 통계 query"""

        query = COUNT_PROCESSDETAIL_BYPC.format(
            f"'{cons_code}'",
            f"AND C.CO_CODE = '{co_code}'" if co_code != "" else "",
        ).strip()

        return query

    @staticmethod
    def select_level1(cons_code, co_code, pc_code) -> str:
        """공정상세도 level1 검색 query"""

        query = SELECT_PROCESSCODE_LEVEL1.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'",
            f"AND PC_CODE = '{pc_code}'",
        )

        return query

    @staticmethod
    def select_level2(cons_code, co_code, pc_code, level1_code) -> str:
        """공정상세도 level2 검색 query"""

        query = SELECT_PROCESSCODE_LEVEL2.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'",
            f"AND PC_CODE = '{pc_code}'",
            f"AND LEVEL1 = {level1_code}",
        )

        return query

    @staticmethod
    def select_level3(cons_code, co_code, pc_code, level1_code, level2_code) -> str:
        """공정상세도 level3 검색 query"""

        query = SELECT_PROCESSCODE_LEVEL3.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'",
            f"AND PC_CODE = '{pc_code}'",
            f"AND LEVEL1 = {level1_code}",
            f"AND LEVEL2 = {level2_code}",
        )

        return query

    @staticmethod
    def select_level4(
        cons_code, co_code, pc_code, level1_code, level2_code, level3_code
    ) -> str:
        """공정상세도 level4 검색 query"""

        query = SELECT_PROCESSCODE_LEVEL4.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'",
            f"AND PC_CODE = '{pc_code}'",
            f"AND LEVEL1 = {level1_code}",
            f"AND LEVEL2 = {level2_code}",
            f"AND LEVEL3 = {level3_code}",
        )

        return query

    @staticmethod
    def get_base_bylevel(cons_code: str, co_code: str) -> str:
        """공정상세내역서 통계 품목별 기본정보 query"""

        query = COUNT_PROCESSBASE_BYLEVEL.format(
            PROCESSDETAIL_CONSCODE_CONDITION.format(cons_code),
            PROCESSDETAIL_COSCODE_CONDITION.format(co_code) if co_code != "" else "",
        ).strip()

        return query

    @staticmethod
    def count_all(cons_code: str, co_code: str) -> str:
        """공정상세내역서 통계 전체 실사용 query"""

        query = COUNT_PROCESSDETAIL.format(
            PROCESSDETAIL_CONSCODE_CONDITION_D.format(cons_code),
            PROCESSDETAIL_COSCODE_CONDITION_D.format(co_code) if co_code != "" else "",
        ).strip()

        return query

    @staticmethod
    def count_bylevel(cons_code: str, co_code: str) -> str:
        """공정상세내역서 통계 품목별 query"""

        query = COUNT_PROCESSDETAIL_BYLEVEL.format(
            # PROCESSDETAIL_CONSCODE_CONDITION_D.format(cons_code),
            # PROCESSDETAIL_COSCODE_CONDITION_D.format(co_code) if co_code != "" else "",
            PROCESSDETAIL_CONSCODE_CONDITION_D.format(cons_code),
            PROCESSDETAIL_COSCODE_CONDITION_D.format(co_code) if co_code != "" else "",
        ).strip()

        return query

    @staticmethod
    def update_auto(
        cons_code: str, co_code: str, level1: int, level2: int, level3: int, level4: int
    ) -> str:
        """공정상세내역서 일지수정시 자동변경 query"""

        query = UPDATE_PROCESSDETAIL_AUTO.format(
            WORKDIARY_CONSCODE_CONDITION.format(cons_code),
            WORKDIARY_COSCODE_CONDITION.format(co_code),
            WORKLOG_LEVEL1_CONDITION.format(level1),
            WORKLOG_LEVEL2_CONDITION.format(level2),
            WORKLOG_LEVEL3_CONDITION.format(level3),
            WORKLOG_LEVEL4_CONDITION.format(level4),
            PROCESSDETAIL_CONSCODE_CONDITION.format(cons_code),
            PROCESSDETAIL_COSCODE_CONDITION.format(co_code),
            PROCESSDETAIL_LEVEL1_CONDITION.format(level1),
            PROCESSDETAIL_LEVEL2_CONDITION.format(level2),
            PROCESSDETAIL_LEVEL3_CONDITION.format(level3),
            PROCESSDETAIL_LEVEL4_CONDITION.format(level4),
        ).strip()

        return query

    @staticmethod
    def delete(cons_code: str, co_code: str) -> str:
        """공정상세내역서 삭제 query"""

        query = DELETE_PROCESSDETAIL.format(
            PROCESSDETAIL_CONSCODE_CONDITION.format(cons_code),
            PROCESSDETAIL_COSCODE_CONDITION.format(co_code),
        ).strip()

        return query

    @staticmethod
    def select_file_all(cons_code, co_code, id) -> str:
        """공정상세내역서 전체 파일 조회 query"""

        query = SELECT_PROCESS_DETAIL_FILE_LIST.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'",
            f"AND (WRITER_ID = '{id}' OR UPLOADED != 0)",
        )

        return query

    @staticmethod
    def insert_file(
        cons_code,
        co_code,
        file_path,
        orig_name,
        chan_name,
        change_date,
        id,
        post_uuid,
        uploaded,
    ) -> str:
        """공정상세내역서 파일 등록 query"""

        query = INSERT_PROCESS_DETAIL_FILE.format(
            f"'{cons_code}'",
            f"'{co_code}'",
            f"'{file_path}'",
            f"'{orig_name}'",
            f"'{chan_name}'",
            f"'{change_date}'" if change_date else "NULL",
            f"'{id}'",
            f"UNHEX('{post_uuid}')",
            f"{uploaded}",
        )

        return query

    @staticmethod
    def select_file_index(post_uuid) -> str:
        """공정상세내역서 파일 등록 query"""

        query = SELECT_PROCESS_DETAIL_FILE_INDEX.format(
            f"AND POST_UUID = UNHEX('{post_uuid}')",
        )

        return query

    @staticmethod
    def select_file(cons_code, co_code, index) -> str:
        """공정상세내역서 파일 index 조회 query"""

        query = SELECT_PROCESS_DETAIL_FILE.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'" if co_code != "" else "",
            f"AND FILE_INDEX = {index}",
        )

        return query

    @staticmethod
    def select_file_uuid(cons_code, co_code, uuid) -> str:
        """공정상세내역서 파일 uuid 조회 query"""

        query = SELECT_PROCESS_DETAIL_FILE.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'" if co_code != "" else "",
            f"AND HEX(POST_UUID) = '{uuid}'",
        )

        return query

    @staticmethod
    def delete_file(cons_code, co_code, index) -> str:
        """공정상세내역서 파일 삭제 query"""

        query = DELETE_PROCESS_DETAIL_FILE.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'",
            f"AND FILE_INDEX = {index}",
        )

        return query

    @staticmethod
    def upload_file(cons_code, co_code, index):
        query = UPDATE_PROCESS_DETAIL_FILE_UPLOAD.format(
            f"FILE_INDEX = {index}",
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'",
        )

        return query

    @staticmethod
    def approve_file(cons_code, co_code, post_uuid):
        query = UPDATE_PROCESS_DETAIL_FILE_APPROVE.format(
            f"POST_UUID = UNHEX('{post_uuid}')",
            f"AND CONS_CODE = '{cons_code}'",
            f"AND CO_CODE = '{co_code}'",
        )

        return query

    @staticmethod
    def insert_item_head():
        query = INSERT_ITEM_HEAD
        return query

    @staticmethod
    def insert_item_body(
        cons_code: str,
        co_code: str,
        pc_name: str,
        description: str,
        standard: str,
        vendor: str,
        unit: str,
        quantity: int,
        head: int,
        material_unit_cost: int,
        labor_unit_cost: int,
        other_unit_cost: int,
    ) -> str:
        """공사 품목 추가 query"""

        query = INSERT_ITEM_BODY.format(
            f"'{cons_code}'",
            f"'{co_code}'",
            f"'{pc_name}'",
            f"'{description}'",
            f"'{standard}'" if standard else "''",
            f"'{vendor}'" if vendor else "NULL",
            f"'{unit}'" if unit else "NULL",
            f"{quantity}",
            f"{head}",
            f"{material_unit_cost}",
            f"{labor_unit_cost}",
            f"{other_unit_cost}",
        ).strip()

        return query

    @staticmethod
    def insert_item_foot():
        query = INSERT_ITEM_FOOT.strip()
        return query

    @staticmethod
    def select_item(cons_code, co_code):
        query = SELECT_ITEM.format(
            f"'{cons_code}'",
            f"'{co_code}'",
        )

        return query

    @staticmethod
    def update_item(
        cons_code: str,
        co_code: str,
        pc_name: str,
        description: str,
        standard: str,
        vendor: str,
        unit: str,
        quantity: int,
        head: int,
        material_unit_cost: int,
        labor_unit_cost: int,
        other_unit_cost: int,
    ) -> str:

        query = UPDATE_ITEM.format(
            f"'{vendor}'" if vendor else "NULL",
            f"'{unit}'" if unit else "NULL",
            f"{quantity}",
            f"{head}",
            f"{material_unit_cost}",
            f"{labor_unit_cost}",
            f"{other_unit_cost}",
            f"'{cons_code}'",
            f"'{co_code}'",
            f"'{pc_name}'",
            f"'{description}'",
            f"'{standard}'" if standard else "''",
        ).strip()

        return query

    @staticmethod
    def delete_item(cons_code, co_code, pc_name, description, standard) -> str:
        query = DELETE_ITEM.format(
            f"'{cons_code}'",
            f"'{co_code}'",
            f"'{pc_name}'",
            f"'{description}'",
            f"'{standard}'",
        )

        return query

    @staticmethod
    def insert_pc_head():
        query = INSERT_PC_HEAD

        return query

    @staticmethod
    def insert_pc_body(
        cons_code,
        co_code,
        pc_name,
        pc_explain,
        start_date_1,
        end_date_1,
        content_1,
        start_date_2,
        end_date_2,
        content_2,
        start_date_3,
        end_date_3,
        content_3,
        start_date_4,
        end_date_4,
        content_4,
    ):
        query = INSERT_PC_BODY.format(
            f"'{cons_code}'",
            f"'{co_code}'",
            f"'{pc_name}'",
            f"'{pc_explain}'",
            f"{start_date_1}",
            f"{end_date_1}",
            f"'{content_1}'" if content_1 else "NULL",
            f"{start_date_2}" if start_date_2 else "NULL",
            f"{end_date_2}" if end_date_2 else "NULL",
            f"'{content_2}'" if content_2 else "NULL",
            f"{start_date_3}" if start_date_3 else "NULL",
            f"{end_date_3}" if end_date_3 else "NULL",
            f"'{content_3}'" if content_3 else "NULL",
            f"{start_date_4}" if start_date_4 else "NULL",
            f"{end_date_4}" if end_date_4 else "NULL",
            f"'{content_4}'" if content_4 else "NULL",
        )

        return query

    @staticmethod
    def insert_pc_foot():
        query = INSERT_PC_FOOT.strip()

        return query

    @staticmethod
    def select_pc(cons_code, co_code):
        query = SELECT_PC.format(
            f"'{cons_code}'",
            f"'{co_code}'",
        )

        return query

    @staticmethod
    def delete_pc(cons_code, co_code):
        query = DELETE_PC_ALL.format(
            f"'{cons_code}'",
            f"'{co_code}'",
        )

        return query

    @staticmethod
    def insert_pc_global(number):
        query = INSERT_GLOBAL_PC.format(
            f"'{int(number):04}'",
            "'PC00'",
            "%s",
            "%s",
            f"'PC00{int(number):04}'",
        )

        return query

    @staticmethod
    def select_pc_global():
        query = SELECT_GLOBAL_PC

        return query

    @staticmethod
    def update_pc_global(number):

        query = UPDATE_GLOBAL_PC.format(
            f"'{int(number):04}'",
        )

        return query

    @staticmethod
    def delete_pc_global(number):
        query = DELETE_GLOBAL_PC.format(
            f"'{int(number):04}'",
        )

        return query

    @staticmethod
    def insert_pc_local(cons_code, co_code, pc_code):
        query = INSERT_LOCAL_PC.format(
            f"'{cons_code}'",
            f"'{co_code}'",
            f"'{pc_code}'",
        )

        return query

    @staticmethod
    def select_pc_local(cons_code, co_code):
        query = SELECT_LOCAL_PC.format(
            f"'{cons_code}'",
            f"'{co_code}'",
        )

        return query

    @staticmethod
    def delete_pc_local(cons_code, co_code, pc_code):
        query = DELETE_LOCAL_PC.format(
            f"'{cons_code}'",
            f"'{co_code}'",
            f"'{pc_code}'",
        )

        return query
