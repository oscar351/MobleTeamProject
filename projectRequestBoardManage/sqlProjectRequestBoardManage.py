"""
의뢰게시판 글 TABLE
APPROVAL_BOARD

UUID	    의뢰게시판 UUID (UNHEX(REPLACE(UUID(),'-','') 사용), 가장 최근에 생성된 UUID @post_uuid에 저장
CONS_CODE   공사코드
WRITER_ID   작성자 ID
POST_TYPE   작성글 종류
TITLE	    제목
CONTENT	    내용
REG_DATE	등록일자
APR_DATE	결재일자
"""

from common import constants

INSERT_REQUEST = " ".join(
    [
        "INSERT INTO",
        "REQUEST_BOARD(CONS_CODE, UUID, WRITER_ID, POST_TYPE, TITLE, CONTENT)",
        "VALUES({}, {}, {}, {}, %s, %s)",
    ]
)

"""
의뢰글을 볼 수 있는 권한

1. 의뢰글 작성자
2. 의뢰글 결재자
3. 의뢰글 참조자
4. 결재가 완료된 의뢰글의 수신자
"""

SELECT_REQUEST_LIST = " ".join(
    [
        "SELECT",
        "HEX(M.UUID) as uuid,",
        "M.NUMBER as number,",
        "M.WRITER_ID as writer_id,",
        "U.USER_NAME as writer_name,",
        "C.CO_NAME as co_name,",
        "M.POST_TYPE as post_type,",
        "M.TITLE as title,",
        "GROUP_CONCAT(DISTINCT U3.USER_NAME SEPARATOR ', ') as approver,",
        "GROUP_CONCAT(DISTINCT U2.USER_NAME SEPARATOR ', ') as receiver,",
        "date_format(M.REG_DATE, %s) as reg_date,",
        "date_format(M.APR_DATE, %s) as apr_date,",
        "M.APR_INDEX as apr_index,",
        "M.AS_CODE as as_code",
        "FROM REQUEST_BOARD M",
        "JOIN USER U",
        "ON M.WRITER_ID = U.ID",
        "JOIN COMPANY C",
        "ON U.CO_CODE = C.CO_CODE",
        "JOIN REQUEST_BOARD_INFO F",
        "ON M.UUID = F.POST_UUID {}",
        "JOIN REQUEST_BOARD_INFO R",
        "ON M.UUID = R.POST_UUID AND R.APR_TYPE_CODE = 'AT000003'",
        "JOIN USER U2",
        "ON R.USER_ID = U2.ID",
        "LEFT JOIN REQUEST_BOARD_INFO R3",
        "ON M.UUID = R3.POST_UUID AND (R3.APR_TYPE_CODE = 'AT000002' OR R3.APR_TYPE_CODE = 'AT000003') AND M.APR_INDEX = R3.APR_INDEX",
        "LEFT JOIN USER U3",
        "ON R3.USER_ID = U3.ID",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
        "AND ACTIVE = 1",
        "GROUP BY M.UUID",
        "ORDER BY M.NUMBER DESC",
    ]
)

SELECT_REQUEST = " ".join(
    [
        "SELECT",
        "HEX(M.UUID) as uuid,",
        "M.NUMBER as number,",
        "M.WRITER_ID as writer_id,",
        "U.USER_NAME as writer_name,",
        "U.CO_CODE as co_code,",
        "M.POST_TYPE as post_type,",
        "M.TITLE as title,",
        "M.CONTENT as content,",
        "date_format(M.REG_DATE, '%Y%m%d%H%i%S') as reg_date,",
        "date_format(M.APR_DATE, '%Y%m%d%H%i%S') as apr_date,",
        "M.APR_INDEX as apr_index,",
        "M.AS_CODE as as_code",
        "FROM REQUEST_BOARD M",
        "JOIN USER U",
        "ON M.WRITER_ID = U.ID",
        "WHERE 1=1",
        "{}",
        "{}",
        "AND ACTIVE = 1",
    ]
)

UPDATE_REQUEST = " ".join(
    [
        "UPDATE",
        "REQUEST_BOARD",
        "SET {}",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

UPDATE_APRRESET = " ".join(
    [
        "UPDATE",
        "REQUEST_BOARD",
        "SET",
        "APR_DATE = NULL,",
        "AS_CODE = 'AS000000',",
        "APR_INDEX = 0",
        "WHERE 1=1",
        "{}",
        "{}",
        "AND ACTIVE = 1",
    ]
)

DELETE_REQUEST = " ".join(
    [
        "UPDATE",
        "REQUEST_BOARD",
        f"SET ACTIVE = 0",
        "WHERE 1=1",
        "{}",
        "{}",
        "AND ACTIVE = 1",
    ]
)

WITHDRAW_REQUEST = " ".join(
    [
        "UPDATE",
        "REQUEST_BOARD",
        f"SET AS_CODE = '{constants.APPRO_STATUS_CD_WITHDRAW}'",
        "WHERE 1=1",
        "{}",
        "{}",
        "AND ACTIVE = 1",
    ]
)

"""
의뢰게시판 첨부파일 TABLE
REQUEST_BOARD_FILE

POST_UUID	게시글 UUID (UNHEX(REPLACE(UUID(),'-','') 사용)
FILE_INDEX	파일 번호
ORIG_NAME	원본파일명
CHAN_NAME   변경파일명
REG_DATE	등록일자
"""

INSERT_REQUEST_FILE = " ".join(
    [
        "INSERT INTO",
        "REQUEST_BOARD_FILE",
        "(POST_UUID, FILE_PATH, FILE_TYPE, ORIG_NAME, CHAN_NAME)",
        "VALUES({}, {}, {}, %s, {})",
    ]
)

SELECT_REQUEST_FILE = " ".join(
    [
        "SELECT",
        "HEX(POST_UUID) as post_uuid,",
        "FILE_INDEX as file_index,",
        "FILE_PATH as file_path,",
        "FILE_TYPE as file_type,",
        "ORIG_NAME as orig_name,",
        "CHAN_NAME as chan_name,",
        "date_format(REG_DATE, '%Y%m%d%H%i%S') as reg_date",
        "FROM REQUEST_BOARD_FILE",
        "WHERE 1=1",
        "{}",
        "ORDER BY FILE_TYPE",
    ]
)

DELETE_REQUEST_FILE = " ".join(
    [
        "DELETE",
        "FROM",
        "REQUEST_BOARD_FILE",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

"""
의뢰게시판 의뢰정보 TABLE
REQUEST_BOARD_INFO

CONS_CODE       공사코드
POST_UUID   	의뢰게시판 UUID
USER_ID         결제자 ID
APR_TYPE_CODE   의뢰권한코드
READ_DATE       읽은날짜
APR_DATE        결재일자
"""

INSERT_INFO = " ".join(
    [
        "INSERT INTO",
        "REQUEST_BOARD_INFO",
        "(CONS_CODE, POST_UUID, USER_ID, APR_TYPE_CODE, READ_DATE, APR_INDEX)",
        "VALUES({}, {}, {}, {}, {}, {})",
    ]
)

SELECT_INFO_LIST = " ".join(
    [
        "SELECT",
        "F.CONS_CODE as cons_code,",
        "HEX(F.POST_UUID) as post_uuid,",
        "F.USER_ID as user_id,",
        "U.USER_NAME as user_name,",
        "C.CO_NAME as co_name,",
        "F.APR_TYPE_CODE as apr_type,",
        "F.APR_INDEX as apr_index,",
        "date_format(F.READ_DATE, '%Y%m%d%H%i%S') as read_date,",
        "date_format(F.APR_DATE, '%Y%m%d%H%i%S') as apr_date,",
        "F.APPROVED as approved,",
        "F.REMARKS as remarks",
        "FROM REQUEST_BOARD_INFO F",
        "JOIN USER U",
        "ON F.USER_ID = U.ID",
        "JOIN COMPANY C",
        "ON U.CO_CODE = C.CO_CODE",
        "WHERE 1=1",
        "{}",
        "{}",
        "ORDER BY F.APR_INDEX",
    ]
)

UPDATE_INFO_READDATE = " ".join(
    [
        "UPDATE",
        "REQUEST_BOARD_INFO",
        "SET",
        "READ_DATE = CURRENT_TIMESTAMP()",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "AND READ_DATE IS NULL",
    ]
)

UPDATE_DRAFTED = " ".join(
    [
        "UPDATE",
        "REQUEST_BOARD",
        "SET",
        "AS_CODE = 'AS000001', APR_INDEX = APR_INDEX + 1",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "AND APR_INDEX = 0",
    ]
)

UPDATE_APPROVED = " ".join(
    [
        "UPDATE",
        "REQUEST_BOARD_INFO",
        "SET",
        "APPROVED = 1, APR_DATE = CURRENT_TIMESTAMP() {}",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

UPDATE_DENIED = " ".join(
    [
        "UPDATE",
        "REQUEST_BOARD_INFO",
        "SET",
        "APPROVED = 0, APR_DATE = CURRENT_TIMESTAMP() {}",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

UPDATE_INFO_APRRESET = " ".join(
    [
        "UPDATE",
        "REQUEST_BOARD_INFO",
        "SET",
        "READ_DATE = NULL,",
        "APR_DATE = NULL,",
        "APPROVED = NULL",
        "WHERE 1=1",
        "{}",
        "{}",
        "AND APR_INDEX != 0",
    ]
)

DELETE_INFO = " ".join(
    [
        "DELETE",
        "FROM",
        "REQUEST_BOARD_INFO",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
    ]
)

DELETE_INFO_ALL = " ".join(
    [
        "DELETE",
        "FROM",
        "REQUEST_BOARD_INFO",
        "WHERE 1=1",
        "{}",
        "{}",
        "AND APR_INDEX != 0",
    ]
)

POSTUUID_CONDITION = "AND UUID = {}"
UUID_CONDITION = "AND UUID = {}"
PARENTUUID_CONDITION = "AND PARENT_UUID = {}"


class sqlProjectRequestBoardManage:
    """의뢰게시판 관리 Class"""

    @staticmethod
    def insert_request(cons_code, post_uuid, writer_id, post_type):

        query = INSERT_REQUEST.format(
            f"'{cons_code}'",
            f"UNHEX('{post_uuid}')",
            f"'{writer_id}'",
            f"'{post_type}'",
        ).strip()

        return query

    @staticmethod
    def select_request_list(
        id,
        cons_code,
        post_type,
        reg_date_start,
        reg_date_end,
    ):
        query = SELECT_REQUEST_LIST.format(
            f"AND F.USER_ID = '{id}'",
            "AND (F.APR_INDEX <= M.APR_INDEX)",
            f"AND M.CONS_CODE = '{cons_code}'",
            "AND C.CO_NAME like %s",
            "AND U.USER_NAME like %s",
            f"AND M.POST_TYPE = {post_type}" if post_type != "" else "",
            "AND M.TITLE like %s",
            "AND M.CONTENT like %s",
            f"AND M.REG_DATE >= '{reg_date_start}'" if reg_date_start != "" else "",
            f"AND M.REG_DATE <= '{reg_date_end}'" if reg_date_end != "" else "",
        ).strip()

        return query

    @staticmethod
    def select_request(cons_code, uuid):

        query = SELECT_REQUEST.format(
            f"AND M.CONS_CODE = '{cons_code}'",
            f"AND M.UUID = UNHEX('{uuid}')",
        ).strip()

        return query

    @staticmethod
    def update_request(cons_code, uuid, post_type):

        query = UPDATE_REQUEST.format(
            ", ".join(
                [
                    f"POST_TYPE = '{post_type}'" if post_type is not None else "",
                    "TITLE = %s",
                    "CONTENT = %s",
                ]
            ).strip(", "),
            f"AND CONS_CODE = '{cons_code}'",
            f"AND UUID = UNHEX('{uuid}')",
        ).strip()

        return query

    @staticmethod
    def update_request_reset(cons_code, post_uuid):
        query = UPDATE_APRRESET.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND UUID = UNHEX('{post_uuid}')",
        )

        return query

    @staticmethod
    def delete_request(cons_code, uuid):

        query = DELETE_REQUEST.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND UUID = UNHEX('{uuid}')",
        ).strip()

        return query
    
    @staticmethod
    def withdraw(cons_code, uuid):

        query = WITHDRAW_REQUEST.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND UUID = UNHEX('{uuid}')",
        ).strip()

        return query

    @staticmethod
    def insert_request_file(post_uuid, file_path, file_type, chan_name):

        query = INSERT_REQUEST_FILE.format(
            f"UNHEX('{post_uuid}')",
            f"'{file_path}'",
            f"'{file_type}'",
            f"'{chan_name}'",
        )

        return query

    @staticmethod
    def select_request_file(post_uuid):

        query = SELECT_REQUEST_FILE.format(
            f"AND POST_UUID = UNHEX('{post_uuid}')",
        )

        return query

    @staticmethod
    def delete_request_file(post_uuid, indexes):

        query = DELETE_REQUEST_FILE.format(
            f"AND POST_UUID = UNHEX('{post_uuid}')",
            f"AND FILE_INDEX IN ({indexes})",
        )

        return query

    @staticmethod
    def insert_info(cons_code, post_uuid, user_id, apr_type_code, index):
        query = INSERT_INFO.format(
            f"'{cons_code}'",
            f"UNHEX('{post_uuid}')",
            f"'{user_id}'",
            f"'{apr_type_code}'",
            "CURRENT_TIMESTAMP()"
            if apr_type_code == constants.APPRO_TYPE_CD_DRAFTER
            else "NULL",
            f"{index}",
        )

        return query

    @staticmethod
    def select_info_list(cons_code, post_uuid):
        query = SELECT_INFO_LIST.format(
            f"AND F.CONS_CODE = '{cons_code}'",
            f"AND F.POST_UUID = UNHEX('{post_uuid}')",
        )

        return query

    @staticmethod
    def update_readdate(cons_code, post_uuid, id):
        query = UPDATE_INFO_READDATE.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND POST_UUID = UNHEX('{post_uuid}')",
            f"AND USER_ID = '{id}'",
        )

        return query

    @staticmethod
    def update_drafted(cons_code, post_uuid, id):
        query = UPDATE_DRAFTED.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND UUID = UNHEX('{post_uuid}')",
            f"AND WRITER_ID = '{id}'",
        )

        return query

    @staticmethod
    def update_approved(cons_code, post_uuid, id):
        query = UPDATE_APPROVED.format(
            ", REMARKS = %s",
            f"AND CONS_CODE = '{cons_code}'",
            f"AND POST_UUID = UNHEX('{post_uuid}')",
            f"AND USER_ID = '{id}'",
        )

        return query

    @staticmethod
    def update_denied(cons_code, post_uuid, id):
        query = UPDATE_DENIED.format(
            ", REMARKS = %s",
            f"AND CONS_CODE = '{cons_code}'",
            f"AND POST_UUID = UNHEX('{post_uuid}')",
            f"AND USER_ID = '{id}'",
        )

        return query

    @staticmethod
    def update_apr_reset(cons_code, post_uuid):
        query = UPDATE_INFO_APRRESET.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND POST_UUID = UNHEX('{post_uuid}')",
        )

        return query

    @staticmethod
    def delete_info(cons_code, post_uuid, id, index):
        query = DELETE_INFO.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND POST_UUID = UNHEX('{post_uuid}')",
            f"AND USER_ID = '{id}'",
            f"AND APR_INDEX = {index}",
        )

        return query
    
    @staticmethod
    def delete_info_all(cons_code, post_uuid):
        query = DELETE_INFO_ALL.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND POST_UUID = UNHEX('{post_uuid}')",
        )

        return query