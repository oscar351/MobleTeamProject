# _*_coding: utf-8 -*-

# Log 관리 Query Class
# 작성 날짜 : 2022. 7. 29
# 작성자 : 황희정
# 기능
# 	1. 2022. 07. 29 | Log 저장 Query를 생성 한다.
# 변경 이력
# 	1. 2022. 07. 29 | 황희정 | 최조 작성

# Log 관리 Query Class

INSERT_LOG = " ".join(
    [
        "INSERT INTO",
        "LOG_MANAGE(PROC_CODE, LOG_LEVEL, TITLE, CONTENT, LOG_DATE, ID, RESCD, MESSAGE)",
        "VALUES('{}', '{}', '{}', %s, '{}', '{}', {}, %s)",
    ]
)

SELECT_LOG_LIST = " ".join(
    [
        "SELECT",
        "LOG_ID as log_id,",
        "PROC_CODE as proc_code,",
        "LOG_LEVEL as log_level,",
        "PROC_CODE as proc_code,",
        "RESCD as resCd,",
        "TITLE as title,",
        "LOG_DATE as log_date,",
        "ID as id",
        "FROM LOG_MANAGE",
        "WHERE 1=1",
        "{}",
        "{}",
        "ORDER BY LOG_ID DESC",
        "LIMIT 100;",
    ]
)

SELECT_LOG = " ".join(
    [
        "SELECT",
        "LOG_ID as log_id,",
        "PROC_CODE as proc_code,",
        "LOG_LEVEL as log_level,",
        "PROC_CODE as proc_code,",
        "RESCD as resCd,",
        "MESSAGE as msg,",
        "TITLE as title,",
        "CONTENT as content,",
        "LOG_DATE as log_date,",
        "ID as id",
        "FROM LOG_MANAGE",
        "WHERE 1=1",
        "{}",
    ]
)


class sqlLogManage:
    # 1. Log 저장 Query를 생성 한다.
    #
    # Parameter
    # 	- data | Object | 로그 Data
    def iLogData(self, data):
        query = INSERT_LOG.format(
            data["proc_code"],
            data["log_level"],
            data["log_title"],
            data["log_date"],
            data["id"],
            data["resCd"]
        )

        return query

    @staticmethod
    def select_log_list(log_id, title_keyword):
        query = SELECT_LOG_LIST.format(
            f"AND LOG_ID < {log_id}" if log_id else "",
            f"AND TITLE LIKE %s" if title_keyword else "",
        )

        return query

    @staticmethod
    def select_log(log_id):
        query = SELECT_LOG.format(f"AND LOG_ID = {log_id}")

        return query
