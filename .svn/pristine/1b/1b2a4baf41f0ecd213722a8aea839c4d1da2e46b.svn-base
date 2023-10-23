"""
설계검토의견 가등록 DB

PLAN_REVIEW DB info
CONS_CODE (PK, FK)      : 공사코드 (= FLOOR_PLAN.CONS_CODE)
VER_INFO (PK, FK)       : 버전 정보 (= FLOOR_PLAN.VER_INFO)
NUMBER (PK)             : 연번
PAGE (FK)		        : 페이지 번호 (= FLOOR_PLAN.PAGE)
DATETIME                : 검토일자 (DATETIME TYPE)
X_POSPER                : 이미지상 x축 위치백분율
Y_POSPER                : 이미지상 y축 위치백분율
SHAPE                   : 이미지상 표시 형태
CATEGORY                : 구분
LOCATION                : 부위
PROBLEM                 : 문제점
REASON                  : 법적근거
SUPV_OPN                : 감리의견
"""

"""
설계검토의견 문서 DB
* 설계도면 이미지 DB 데이터 변경시 문서내용 문제 발생 (content 연동불가)

참조하는 DB:
DOC_MANAGE - 요청서와 통지서의 내용정보 저장
DOC_LINK_MANAGE - 요청서와 통지서의 연결관계 저장
DOC_FILE_MANAGE - 요청서와 통지서의 파일정보 저장 (지금은 사용안함)

설계도면 검토보고서 문서코드
"""

"""
INSERT
현재 작성하려는 의견의 연번을 정하기 위해 
같은 공사코드 및 문서버전에서 가장 큰 연번을 락 걸고 조회 후 (select for update),
해당 값에 +1하여 연번을 입력한다. 
완결성을 보장하기 위해 조회와 생성쿼리를 하나의 트랜잭션으로 묶는다(excute)
"""
INSERT_PLANREVIEW_BASE = " ".join(
    [
        "SELECT COUNT(*) INTO @count",
        "FROM PLAN_REVIEW",
        "WHERE 1=1",
        "{}",
        "{}",
        "FOR UPDATE;",
        "INSERT INTO",
        "PLAN_REVIEW",
        "(CONS_CODE, VER_INFO, NUMBER, PAGE, X_POSPER, Y_POSPER, SHAPE, CATEGORY, LOCATION, PROBLEM, REASON, SUPV_OPN)",
        "VALUES('{}', '{}', IFNULL(@count, 0) + 1, {}, {}, {}, '{}', '{}', '{}', '{}', '{}', '{}');",
    ]
)

SELECT_PLANREVIEW_BASE = " ".join(
    [
        "SELECT",
        "CONS_CODE as cons_code,",
        "VER_INFO as ver_info,",
        "NUMBER as number,",
        "PAGE as page,",
        "date_format(DATETIME, '%Y%m%d%H%i%S') as datetime,",
        "X_POSPER as x_posper,",
        "Y_POSPER as y_posper,",
        "SHAPE as shape,",
        "CATEGORY as category,",
        "LOCATION as location,",
        "PROBLEM as problem,",
        "REASON as reason,",
        "SUPV_OPN as supv_opn",
        "FROM PLAN_REVIEW",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "ORDER BY NUMBER ASC",
    ]
)

UPDATE_PLANREVIEW_CONTENTS_BASE = " ".join(
    [
        "UPDATE",
        "PLAN_REVIEW",
        "SET",
        "PAGE = {},",
        "X_POSPER = {},",
        "Y_POSPER = {},",
        "SHAPE = '{}',",
        "CATEGORY = '{}',",
        "LOCATION = '{}',",
        "PROBLEM = '{}',",
        "REASON = '{}',",
        "SUPV_OPN = '{}'",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

"""
INSERT
현재 작성하려는 의견의 연번을 정하기 위해 
같은 공사코드 및 문서버전에서 가장 큰 연번을 락 걸고 조회 후 (select for update),
해당 값에 +1하여 연번을 입력한다. 
완결성을 보장하기 위해 조회와 생성쿼리를 하나의 트랜잭션으로 묶는다(START TRANSACTION, ... , COMMIT)
"""
DELETE_PLANREVIEW = " ".join(
    [
        "DELETE",
        "FROM PLAN_REVIEW",
        "WHERE 1=1",
        "{}",
        "{}",
        "{};",
        "UPDATE",
        "PLAN_REVIEW",
        "SET NUMBER = NUMBER - 1",
        "WHERE 1=1",
        "{}",
        "{}",
        "{};",
    ]
)

PLANREVIEW_CONSCODE_CONDITION = "AND CONS_CODE = '{}'"
PLANREVIEW_VERINFO_CONDITION = "AND VER_INFO = '{}'"
PLANREVIEW_NUMBER_CONDITION = "AND NUMBER = {}"
PLANREVIEW_OVER_NUMBER_CONDITION = "AND NUMBER > {}"

SELECT_PLANREVIEWPRT_BASE = " ".join(
    [
        "SELECT",
        "CONS_CODE as cons_code,",
        "SYS_DOC_NUM as sys_doc_num,",
        "CONTENT as content,",
        "PC_DATE as pc_date",
        "FROM DOC_MANAGE",
        "WHERE 1=1",
        "AND DOC_CODE = 'SD000012'",  # 도면검토 보고서의 문서코드는 SD000012
        "{}",
    ]
)

PLANREVIEWPRT_CONSCODE_CONDITION = "AND CONS_CODE = '{}'"


class sqlProjectPlanReviewManage:
    """설계도면 감리의견 관리 Query Class"""

    @staticmethod
    def insert(
        cons_code: str,
        ver_info: str,
        page: int,
        x_posper: int,
        y_posper: int,
        shape: str,
        category: str,
        location: str,
        problem: str,
        reason: str,
        supv_opn: str,
    ) -> str:
        """설계도면 감리의견 추가 query"""

        query = INSERT_PLANREVIEW_BASE.format(
            PLANREVIEW_CONSCODE_CONDITION.format(cons_code),
            PLANREVIEW_VERINFO_CONDITION.format(ver_info),
            cons_code,
            ver_info,
            page,
            x_posper,
            y_posper,
            shape,
            category,
            location,
            problem,
            reason,
            supv_opn,
        ).strip()

        return query

    @staticmethod
    def select(cons_code: str, ver_info: str, number: int) -> str:
        """설계도면 감리의견 검색 query"""

        query = SELECT_PLANREVIEW_BASE.format(
            PLANREVIEW_CONSCODE_CONDITION.format(cons_code),
            PLANREVIEW_VERINFO_CONDITION.format(ver_info),
            PLANREVIEW_NUMBER_CONDITION.format(number),
        ).strip()

        return query

    @staticmethod
    def select_all(cons_code: str, ver_info: str) -> str:
        """설계도면 전체 감리의견 검색 query"""

        query = SELECT_PLANREVIEW_BASE.format(
            PLANREVIEW_CONSCODE_CONDITION.format(cons_code),
            PLANREVIEW_VERINFO_CONDITION.format(ver_info),
            "",
        ).strip()

        return query

    @staticmethod
    def update(
        cons_code: str,
        ver_info: str,
        number: int,
        page: int,
        x_posper: int,
        y_posper: int,
        shape: str,
        category: str,
        location: str,
        problem: str,
        reason: str,
        supv_opn: str,
    ) -> str:
        """설계도면 감리의견 개정 query"""

        query = UPDATE_PLANREVIEW_CONTENTS_BASE.format(
            page,
            x_posper,
            y_posper,
            shape,
            category,
            location,
            problem,
            reason,
            supv_opn,
            PLANREVIEW_CONSCODE_CONDITION.format(cons_code),
            PLANREVIEW_VERINFO_CONDITION.format(ver_info),
            PLANREVIEW_NUMBER_CONDITION.format(number),
        ).strip()

        return query

    @staticmethod
    def delete(cons_code: str, ver_info: str, number: int) -> str:
        """설계도면 감리의견 삭제 query"""

        query = DELETE_PLANREVIEW.format(
            PLANREVIEW_CONSCODE_CONDITION.format(cons_code),
            PLANREVIEW_VERINFO_CONDITION.format(ver_info),
            PLANREVIEW_NUMBER_CONDITION.format(number),
            PLANREVIEW_CONSCODE_CONDITION.format(cons_code),
            PLANREVIEW_VERINFO_CONDITION.format(ver_info),
            PLANREVIEW_OVER_NUMBER_CONDITION.format(number),
        ).strip()

        return query

    @staticmethod
    def delete_all(cons_code: str, ver_info: str) -> str:
        """설계도면 전체 감리의견 삭제 query"""

        query = DELETE_PLANREVIEW.format(
            PLANREVIEW_CONSCODE_CONDITION.format(cons_code),
            PLANREVIEW_VERINFO_CONDITION.format(ver_info),
            "",
        ).strip()

        return query

    @staticmethod
    def select_prt(cons_code: str) -> str:
        """설계도면 검토보고서 검색 query"""

        query = SELECT_PLANREVIEWPRT_BASE.format(
            PLANREVIEWPRT_CONSCODE_CONDITION.format(cons_code),
        ).strip()

        return query
