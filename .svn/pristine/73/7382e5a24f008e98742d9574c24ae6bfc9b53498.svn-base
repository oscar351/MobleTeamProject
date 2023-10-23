"""
회의록 글 TABLE
METTING_MINUTES

UUID	    회의록 UUID (UNHEX(REPLACE(UUID(),'-','') 사용), 가장 최근에 생성된 UUID @post_uuid에 저장
CONS_CODE   공사코드
WRITER_ID   작성자 ID
TITLE	    제목
CONTENT	    내용
REG_DATE	등록일자
"""

INSERT_MESSAGE = " ".join(
    [
        "INSERT INTO",
        "METTING_MINUTES(CONS_CODE, UUID, WRITER_ID, TITLE, CONTENT)",
        "VALUES({}, {}, {}, %s, %s)",
    ]
)

SELECT_MESSAGE_LIST = " ".join(
    [
        "SELECT",
        "HEX(M.UUID) as uuid,",
        "M.NUMBER as number,",
        "M.WRITER_ID as writer_id,",
        "U.USER_NAME as writer_name,",
        "C.CO_NAME as co_name,",
        "M.TITLE as title,",
        "M.ISSUED as issued,",
        "(SELECT COUNT(*) FROM METTING_MINUTES_REPLY WHERE POST_UUID = M.UUID) as reply_count,",
        "date_format(M.REG_DATE, %s) as reg_date",
        "FROM METTING_MINUTES M",
        "JOIN USER U",
        "ON M.WRITER_ID = U.ID",
        "JOIN COMPANY C",
        "ON U.CO_CODE = C.CO_CODE",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
        "{}",
        "AND ACTIVE = 1",
        "ORDER BY M.REG_DATE DESC",
    ]
)

SELECT_MESSAGE = " ".join(
    [
        "SELECT",
        "HEX(M.UUID) as uuid,",
        "M.NUMBER as number,",
        "M.WRITER_ID as writer_id,",
        "U.USER_NAME as writer_name,",
        "U.CO_CODE as co_code,",
        "M.TITLE as title,",
        "M.CONTENT as content,",
        "M.ISSUED as issued,",
        "date_format(M.REG_DATE, '%Y%m%d%H%i%S') as reg_date",
        "FROM METTING_MINUTES M",
        "JOIN USER U",
        "ON M.WRITER_ID = U.ID",
        "WHERE 1=1",
        "{}",
        "{}",
        "AND ACTIVE = 1",
    ]
)

SELECT_LOCK = " ".join(
    [
        "SELECT",
        "ISSUED as issued",
        "FROM METTING_MINUTES",
        "WHERE 1=1",
        "{}",
        "{}",
        "AND ACTIVE = 1",
    ]
)

UPDATE_MESSAGE = " ".join(
    [
        "UPDATE",
        "METTING_MINUTES",
        "SET {}",
        "WHERE 1=1",
        "{}",
        "{}",
        "AND ISSUED = 0",
        "AND ACTIVE = 1",
    ]
)

LOCK_MESSAGE = " ".join(
    [
        "UPDATE",
        "METTING_MINUTES",
        "SET {}",
        "WHERE 1=1",
        "{}",
        "{}",
        "AND ACTIVE = 1",
    ]
)

DELETE_MESSAGE = " ".join(
    [
        "UPDATE",
        "METTING_MINUTES",
        "SET ACTIVE = 0",
        "WHERE 1=1",
        "{}",
        "{}",
        "AND ISSUED = 0",
        "AND ACTIVE = 1",
    ]
)

"""
회의록 첨부파일 TABLE
METTING_MINUTES_FILE

POST_UUID	게시글 UUID (UNHEX(REPLACE(UUID(),'-','') 사용)
FILE_INDEX	파일 번호
ORIG_NAME	원본파일명
CHAN_NAME   변경파일명
REG_DATE	등록일자
"""

INSERT_MESSAGE_FILE = " ".join(
    [
        "INSERT INTO",
        "METTING_MINUTES_FILE",
        "(POST_UUID, FILE_PATH, ORIG_NAME, CHAN_NAME)",
        "VALUES({}, {}, %s, {})",
    ]
)

SELECT_MESSAGE_FILE = " ".join(
    [
        "SELECT",
        "HEX(POST_UUID) as post_uuid,",
        "FILE_INDEX as file_index,",
        "FILE_PATH as file_path,",
        "ORIG_NAME as orig_name,",
        "CHAN_NAME as chan_name,",
        "date_format(REG_DATE, '%Y%m%d%H%i%S') as reg_date",
        "FROM METTING_MINUTES_FILE",
        "WHERE 1=1",
        "{}",
    ]
)

DELETE_MESSAGE_FILE = " ".join(
    [
        "DELETE",
        "FROM",
        "METTING_MINUTES_FILE",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

"""
회의록 댓글 TABLE
METTING_MINUTES_REPLY

UUID	    댓글 UUID (UNHEX(REPLACE(UUID(),'-','') 사용)
POST_UUID   게시글 UUID (UNHEX(REPLACE(UUID(),'-','') 사용)
PARENT_UUID 부모 댓글 UUID (UNHEX(REPLACE(UUID(),'-','') 사용)
CHILD_COUNT 자식 댓글 수
WRITER_ID   작성자 ID
CONTENT	    내용
REG_DATE	등록일자
"""

INSERT_REPLY = " ".join(
    [
        "INSERT INTO",
        "METTING_MINUTES_REPLY",
        "(POST_UUID, PARENT_UUID, WRITER_ID, CONTENT)",
        "VALUES({}, {}, {}, %s);",
        "{}",
    ]
)

SELECT_REPLY = " ".join(
    [
        "SELECT",
        "HEX(R.UUID) as uuid,",
        "HEX(R.POST_UUID) as post_uuid,",
        "HEX(R.PARENT_UUID) as parent_uuid,",
        "R.CHILD_COUNT as child_count,",
        "R.CONTENT as content,",
        "date_format(R.REG_DATE, '%Y%m%d%H%i%S') as reg_date,",
        "R.WRITER_ID as writer_id,",
        "U.USER_NAME as writer_name,",
        "U.CO_CODE as co_code",
        "FROM METTING_MINUTES_REPLY R",
        "JOIN USER U",
        "ON R.WRITER_ID = U.ID",
        "WHERE 1=1",
        "{}",
        "{}",
        "ORDER BY R.REG_DATE DESC",
    ]
)

UPDATE_REPLY = " ".join(
    [
        "UPDATE",
        "METTING_MINUTES_REPLY",
        "SET",
        "CONTENT = %s,",
        "REG_DATE = CURRENT_TIMESTAMP()",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

DELETE_REPLY = " ".join(
    [
        "UPDATE",
        "METTING_MINUTES_REPLY",
        "SET",
        "CONTENT = NULL,",
        "REG_DATE = CURRENT_TIMESTAMP()",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

POSTUUID_CONDITION = "AND UUID = {}"
UUID_CONDITION = "AND UUID = {}"
PARENTUUID_CONDITION = "AND PARENT_UUID = {}"


class sqlProjectMettingMinutesManage:
    """회의록 관리 Class"""

    @staticmethod
    def insert_message(cons_code, post_uuid, writer_id):
        query = INSERT_MESSAGE.format(
            f"'{cons_code}'",
            f"UNHEX('{post_uuid}')",
            f"'{writer_id}'",
        ).strip()

        return query

    @staticmethod
    def select_message_list(
        cons_code,
        issued,
        reg_date_start,
        reg_date_end,
    ):
        query = SELECT_MESSAGE_LIST.format(
            f"AND M.CONS_CODE = '{cons_code}'",
            "AND C.CO_NAME like %s",
            "AND U.USER_NAME like %s",
            "AND M.TITLE LIKE %s",
            "AND M.CONTENT LIKE %s",
            f"AND M.ISSUED = {issued}" if issued != "" else "",
            f"AND M.REG_DATE >= '{reg_date_start}'" if reg_date_start != "" else "",
            f"AND M.REG_DATE <= '{reg_date_end}'" if reg_date_end != "" else "",
        ).strip()

        return query

    @staticmethod
    def select_message(cons_code, uuid):
        query = SELECT_MESSAGE.format(
            f"AND M.CONS_CODE = '{cons_code}'",
            f"AND M.UUID = UNHEX('{uuid}')",
        ).strip()

        return query

    @staticmethod
    def select_lock(cons_code, uuid):
        query = SELECT_LOCK.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND UUID = UNHEX('{uuid}')",
        ).strip()

        return query

    @staticmethod
    def update_message(cons_code, uuid):
        query = UPDATE_MESSAGE.format(
            ", ".join(
                filter(
                    lambda x: x is not None,
                    [
                        "TITLE = %s",
                        "CONTENT = %s",
                    ],
                )
            ),
            f"AND CONS_CODE = '{cons_code}'",
            f"AND UUID = UNHEX('{uuid}')",
        ).strip()

        return query

    @staticmethod
    def lock_message(cons_code, uuid, issued):
        query = LOCK_MESSAGE.format(
            f"ISSUED = {issued}",
            f"AND CONS_CODE = '{cons_code}'",
            f"AND UUID = UNHEX('{uuid}')",
        )

        return query

    @staticmethod
    def delete_message(cons_code, uuid):
        query = DELETE_MESSAGE.format(
            f"AND CONS_CODE = '{cons_code}'",
            f"AND UUID = UNHEX('{uuid}')",
        ).strip()

        return query

    @staticmethod
    def insert_message_file(post_uuid, file_path, chan_name):
        query = INSERT_MESSAGE_FILE.format(
            f"UNHEX('{post_uuid}')",
            f"'{file_path}'",
            f"'{chan_name}'",
        )

        return query

    @staticmethod
    def select_message_file(post_uuid):
        query = SELECT_MESSAGE_FILE.format(
            f"AND POST_UUID = UNHEX('{post_uuid}')",
        )

        return query

    @staticmethod
    def delete_message_file(post_uuid, indexes):
        query = DELETE_MESSAGE_FILE.format(
            f"AND POST_UUID = UNHEX('{post_uuid}')",
            f"AND FILE_INDEX IN ({indexes})",
        )

        return query

    @staticmethod
    def insert_reply(post_uuid, parent_uuid, writer_id):
        query = INSERT_REPLY.format(
            f"UNHEX('{post_uuid}')",
            f"UNHEX('{parent_uuid}')" if parent_uuid else "NULL",
            f"'{writer_id}'",
            f"UPDATE METTING_MINUTES_REPLY SET CHILD_COUNT = CHILD_COUNT + 1 WHERE UUID = UNHEX('{parent_uuid}')"
            if parent_uuid
            else "",
        ).strip()

        return query

    @staticmethod
    def select_reply(post_uuid, parent_uuid):
        query = SELECT_REPLY.format(
            f"AND R.POST_UUID = UNHEX('{post_uuid}')",
            f"AND R.PARENT_UUID = UNHEX('{parent_uuid}')"
            if parent_uuid
            else f"AND R.PARENT_UUID is NULL",
        ).strip()

        return query

    @staticmethod
    def update_reply(post_uuid, uuid):
        query = UPDATE_REPLY.format(
            f"AND POST_UUID = UNHEX('{post_uuid}')",
            f"AND UUID = UNHEX('{uuid}')",
        ).strip()

        return query

    @staticmethod
    def delete_reply(post_uuid, uuid):
        query = DELETE_REPLY.format(
            f"AND POST_UUID = UNHEX('{post_uuid}')", f"AND UUID = UNHEX('{uuid}')"
        ).strip()

        return query
