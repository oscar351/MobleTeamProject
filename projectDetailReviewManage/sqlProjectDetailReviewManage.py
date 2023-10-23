"""
시공상세도 검토요청서, 검토통보서 문서 DB

참조하는 DB:
DOC_MANAGE - 요청서와 통보서의 내용정보 저장
DOC_LINK_MANAGE - 요청서와 통보서의 연결관계 저장
DOC_FILE_MANAGE - 요청서와 통보서의 파일정보 저장 (지금은 사용안함)

시공상세도 검토요청서 문서코드 : CD000011
시공상세도 검토통보서 문서코드 : SD000017

조회시 검토요청서는 무조건 존재해야 한다.
조회시 검토통보서는 있을 수도, 없을 수도 있다.
"""

SELECT_DETAILREVIEW_BASE = " ".join(
    [
        "SELECT",
        "REQ.CONS_CODE as cons_code,",
        "REQ.SYS_DOC_NUM as req_sys_doc_num,",
        "REQ.DOC_NUM as req_doc_num,",
        "REQ.CONTENT as req_content,",
        "REQ.PR_DATE as req_pr_date,",
        "REQ.PC_DATE as req_pc_date,",
        "REQ.STATE_CODE as req_state_code,",
        "NTC.SYS_DOC_NUM as ntc_sys_doc_num,",
        "NTC.DOC_NUM as ntc_doc_num,",
        "NTC.CONTENT as ntc_content,",
        "NTC.PR_DATE as ntc_pr_date,",
        "NTC.PC_DATE as ntc_pc_date,",
        "NTC.STATE_CODE as ntc_state_code",
        "FROM (SELECT * FROM DOC_MANAGE WHERE DOC_CODE = 'CD000011' {}) REQ",  # 검토요청서의 문서코드는 CD000011, 항상 조회
        "LEFT JOIN DOCUMENT_LINK_INFO LINK",
        "ON LINK.CONS_CODE = REQ.CONS_CODE",
        "AND LINK.SYS_DOC_NUM = REQ.SYS_DOC_NUM",
        "LEFT JOIN",
        "(SELECT * FROM DOC_MANAGE WHERE DOC_CODE = 'SD000017' {}) NTC",  # 검토통보서의 문서코드는 SD000017, 없을 수도 있다
        "ON LINK.CONS_CODE = NTC.CONS_CODE",
        "AND LINK.TO_SYS_DOC_NUM = NTC.SYS_DOC_NUM",
        "WHERE 1=1",
    ]
)

SELECT_CONSCODE_CONDITION = "AND CONS_CODE = '{}'"


class sqlProjectDetailReviewManage:
    """시공상세도 검토 관리 Query Class"""

    @staticmethod
    def select(cons_code: str) -> str:
        """시공상세도 검토 관련문서들을 조회하는 query"""

        query = SELECT_DETAILREVIEW_BASE.format(
            SELECT_CONSCODE_CONDITION.format(cons_code),
            SELECT_CONSCODE_CONDITION.format(cons_code),
        ).strip()
        return query
