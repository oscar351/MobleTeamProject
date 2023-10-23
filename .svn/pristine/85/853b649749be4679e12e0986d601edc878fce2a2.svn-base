"""
FLOOR_PLAN DB info
CONS_CODE (PK, FK)      : 공사코드 (= DESIGN_BOOK_MANAGE.CONS_CODE)
VER_INFO (PK, FK)       : 버전 정보 (= DESIGN_BOOK_MANAGE.VER_INFO)
PAGE (PK)		        : 페이지 번호
SUBPAGE		            : 하위 페이지 번호 (0: Main page)
CODE                    : 설계도면 코드
TITLE			        : 도면 제목
PATH                    : 도면이미지 경로
"""

INSERT_FLOORPLAN_INFO = " ".join(
    [
        "INSERT INTO",
        "FLOOR_PLAN",
        "(CONS_CODE, VER_INFO, PAGE, SUBPAGE, CODE, TITLE, PATH)",
        "VALUES('{}', '{}', {}, {}, '{}', '{}', '{}')",
    ]
)

SELECT_FLOORPLAN_INFO = " ".join(
    [
        "SELECT",
        "CONS_CODE as cons_code,",
        "VER_INFO as ver_info,",
        "PAGE as page,",
        "SUBPAGE  as subpage,",
        "CODE as code,",
        "TITLE as title,",
        "PATH as path",
        "FROM FLOOR_PLAN",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "ORDER BY PAGE ASC",
    ]
)

DELETE_FLOORPLAN_INFO = " ".join(["DELETE", "FROM FLOOR_PLAN", "WHERE 1=1", "{}", "{}"])

FLOORPLAN_CONDITION1 = "AND CONS_CODE = '{}'"
FLOORPLAN_CONDITION2 = "AND VER_INFO = '{}'"
FLOORPLAN_CONDITION3 = "AND PAGE = {}"


class sqlProjectFloorPlanManage:
    """설계도면 이미지 관리 Query Class"""

    @staticmethod
    def insert(
        cons_code: str,
        ver_info: str,
        page: int,
        subpage: int,
        code: str,
        title: str,
        path: str,
    ) -> str:
        """설계도면 추가 query"""

        query = INSERT_FLOORPLAN_INFO.format(
            cons_code,
            ver_info,
            page,
            subpage,
            code,
            title,
            path,
        ).strip()

        return query

    @staticmethod
    def select(cons_code: str, ver_info: str, page: int) -> str:
        """특정 페이지 설계도면 검색 query"""

        query = SELECT_FLOORPLAN_INFO.format(
            FLOORPLAN_CONDITION1.format(cons_code),
            FLOORPLAN_CONDITION2.format(ver_info),
            FLOORPLAN_CONDITION3.format(page),
        ).strip()

        return query

    @staticmethod
    def select_all(cons_code: str, ver_info: str) -> str:
        """전체 설계도면 검색 query"""

        query = SELECT_FLOORPLAN_INFO.format(
            FLOORPLAN_CONDITION1.format(cons_code),
            FLOORPLAN_CONDITION2.format(ver_info),
            "",
        ).strip()

        return query

    @staticmethod
    def delete(cons_code: str, ver_info: str, page: int) -> str:
        """특정 페이지 설계도면 삭제 query"""

        query = DELETE_FLOORPLAN_INFO.format(
            FLOORPLAN_CONDITION1.format(cons_code),
            FLOORPLAN_CONDITION2.format(ver_info),
            FLOORPLAN_CONDITION3.format(page),
        ).strip()

        return query

    @staticmethod
    def delete_all(cons_code: str, ver_info: str) -> str:
        """전체 설계도면 삭제 query"""

        query = DELETE_FLOORPLAN_INFO.format(
            FLOORPLAN_CONDITION1.format(cons_code),
            FLOORPLAN_CONDITION2.format(ver_info),
            "",
        ).strip()

        return query
