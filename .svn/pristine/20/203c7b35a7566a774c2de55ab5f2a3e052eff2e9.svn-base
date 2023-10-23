# _*_coding: utf-8 -*-

SELECT_PROJSTATUSSTATISTICS_INFO = """SELECT C.PROJ_STATUS_CD AS proj_status_cd, C.PROJ_STATUS_NM AS proj_status_nm, C.RESIDE_CLASS_CD AS reside_class_cd, C.RESIDE_CLASS_NM AS reside_class_nm, COALESCE(D.CNT, 0) AS cnt
FROM (SELECT A.FULLCODE AS PROJ_STATUS_CD, A.SUBCODE_NAME AS PROJ_STATUS_NM, B.FULLCODE AS RESIDE_CLASS_CD, B.SUBCODE_NAME AS RESIDE_CLASS_NM FROM 
			(SELECT FULLCODE, SUBCODE_NAME FROM SUBCODE_MANAGE WHERE CODE = "ST00" AND FULLCODE != "ST000000" ORDER BY FULLCODE) A,
				(SELECT FULLCODE, SUBCODE_NAME FROM SUBCODE_MANAGE WHERE CODE = "SD01" ORDER BY FULLCODE) B) C LEFT OUTER JOIN (SELECT COUNT(*) as CNT, PROJECT_STATUS, RESIDE_CLASS_CODE FROM PROJECT WHERE 1=1 AND CONS_CODE IN (SELECT CONS_CODE FROM JOIN_WORKFORCE WHERE ID = "{userId}")
					GROUP BY PROJECT_STATUS, RESIDE_CLASS_CODE) D ON C.PROJ_STATUS_CD = D.PROJECT_STATUS AND C.RESIDE_CLASS_CD = D.RESIDE_CLASS_CODE"""

#### 발주처, 시공사, 디자인은 본인이 속한 프로젝트만 ####
# COUNT_PROJECT_USERIN = " ".join(
#    [
#        "SELECT",
#        "P.PROJECT_STATUS as project_status,",
#        "COUNT(DISTINCT P.CONS_CODE) as count",
#        "FROM PROJECT P",
#        "JOIN JOIN_WORKFORCE W",
#        "ON P.CONS_CODE = W.CONS_CODE",
#        "AND P.SUPERV_CO_CODE = W.CO_CODE",
#        "WHERE 1=1",
#        "AND W.ID = '{}'",
#        "GROUP BY P.PROJECT_STATUS",
#    ]
# )

#### 발주처, 시공사, 디자인은 본인이 속한 프로젝트만 ####
# COUNT_PROJECT_USERIN = " ".join(
#    [
#        "SELECT",
#        "P.PROJECT_STATUS as project_status,",
#        "COUNT(DISTINCT P.CONS_CODE) as count",
#        "FROM PROJECT P",
#        "JOIN JOIN_WORKFORCE W",
#        "ON P.CONS_CODE = W.CONS_CODE",
#        "AND P.SUPERV_CO_CODE = W.CO_CODE",
#        "WHERE 1=1",
#        "AND W.ID = '{}'",
#        "GROUP BY P.PROJECT_STATUS",
#    ]
# )

# 2023-02-14 hjhwang 위 소스 주석 처리 함.
#### 발주처, 시공사, 디자인은 본인이 속한 프로젝트만 ####
COUNT_PROJECT_USERIN = " ".join(
    [
        "SELECT",
        "P.PROJECT_STATUS as status,",
        "COUNT(DISTINCT P.CONS_CODE) as count",
        "FROM PROJECT P",
        "JOIN JOIN_WORKFORCE W",
        "ON P.CONS_CODE = W.CONS_CODE",
        "AND W.ID = '{}'",
        "WHERE 1=1",
        "GROUP BY P.PROJECT_STATUS",
    ]
)

#### 마스터는 전부 다, 모니터링은 회사가 속한 프로젝트 전부 ####
COUNT_PROJECT_COMPANYIN = " ".join(
    [
        "SELECT",
        "P.PROJECT_STATUS as status,",
        "COUNT(DISTINCT P.CONS_CODE) as count",
        "FROM PROJECT P",
        "JOIN JOIN_WORKFORCE W",
        "ON P.CONS_CODE = W.CONS_CODE",
        "AND P.SUPERV_CO_CODE = W.CO_CODE",
        "WHERE 1=1",
        "{}",
        "GROUP BY P.PROJECT_STATUS",
    ]
)

COUNT_PROJECT_MASTER = " ".join(
    [
        "SELECT",
        "P.PROJECT_STATUS as status,",
        "COUNT(DISTINCT P.CONS_CODE) as count",
        "FROM PROJECT P",
        "GROUP BY P.PROJECT_STATUS",
    ]
)

COUNT_COMPANY_CONDITION = "AND W.CO_CODE = '{}'"


class sqlProjectStatisticsManage:
    def sGetProjStatusStatistics(self, userId):
        query = SELECT_PROJSTATUSSTATISTICS_INFO.replace("{userId}", userId)

        return query

    @staticmethod
    def count_project_userin(id):
        query = COUNT_PROJECT_USERIN.format(id).strip()

        return query

    @staticmethod
    def count_project_companyin(co_code):
        query = COUNT_PROJECT_COMPANYIN.format(
            COUNT_COMPANY_CONDITION.format(co_code),
        ).strip()

        return query

    @staticmethod
    def count_project_master():
        query = COUNT_PROJECT_MASTER.strip()

        return query
