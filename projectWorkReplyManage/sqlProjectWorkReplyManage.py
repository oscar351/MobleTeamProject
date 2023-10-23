"""
일일작업관리 댓글 DB
LOG_REPLY

ID	댓글 UUID (UNHEX(REPLACE(UUID(),'-','') 사용)
SYS_DOC_NUM 작업일보 연동번호
PARENT_ID	부모댓글 UUID
CHILD_COUNT	자식댓글 수 (0)
WRITER_ID	작성자 ID
CONTENT		댓글내용

"""

INSERT_REPLY = " ".join(
    [
        "UPDATE",
        "LOG_REPLY",
        "SET CHILD_COUNT = CHILD_COUNT + 1",
        "WHERE 1=1",
        "AND SYS_DOC_NUM = {}",
        "AND HEX(UUID) = '{}';",
        "INSERT INTO",
        "LOG_REPLY",
        "(UUID, SYS_DOC_NUM, PARENT_UUID, WRITER_ID, CONTENT)",
        "VALUES(UNHEX(REPLACE(UUID(),'-','')), {}, {}, '{}', '{}')",
    ]
)

SELECT_REPLY = " ".join(
    [
        "SELECT",
        "HEX(R.UUID) as uuid,",
        "R.SYS_DOC_NUM as sys_doc_num,",
        "HEX(R.PARENT_UUID) as parent_uuid,",
        "R.CHILD_COUNT as child_count,",
        "R.CONTENT as content,",
        "date_format(R.REG_DATE, '%Y%m%d%H%i%S') as reg_date,",
        "R.WRITER_ID as writer_id,",
        "U.USER_NAME as writer_name",
        "FROM LOG_REPLY R",
        "JOIN USER U",
        "ON R.WRITER_ID = U.ID",
        "WHERE 1=1",
        "{}",
        "{}",
    ]
)

CHECK_REPLY = " ".join(
    [
        "SELECT",
        "WRITER_ID as writer_id",
        "FROM LOG_REPLY",
        "WHERE 1=1",
        "{}",
        "{}",
        "{}",
    ]
)

UPDATE_REPLY = " ".join(
    [
        "UPDATE",
        "LOG_REPLY",
        "SET",
        "CONTENT = '{}',",
        "REG_DATE = CURRENT_TIMESTAMP()",
        "WHERE 1=1",
        "{}",
    ]
)

DELETE_REPLY = " ".join(
    [
        "UPDATE",
        "LOG_REPLY",
        "SET",
        "CONTENT = NULL,",
        "REG_DATE = CURRENT_TIMESTAMP()",
        "WHERE 1=1",
        "{}",
    ]
)

SELECT_SYSDOCNUM_CONDITION = "AND R.SYS_DOC_NUM = {}"
SELECT_PARENTUUID_CONDITION = "AND {}"
REPLY_UUID_CONDITION = "AND HEX(UUID) = '{}'"
REPLY_SYSDOCNUM_CONDITION = "AND SYS_DOC_NUM = {}"
REPLY_WRITERID_CONDITION = "AND WRITER_ID = '{}'"


class sqlProjectWorkReplyManage:
    """일지 댓글 관리 Query Class"""

    @staticmethod
    def insert_reply(sys_doc_num, parent_uuid, writer_id, content):

        query = INSERT_REPLY.format(
            sys_doc_num,
            parent_uuid,
            sys_doc_num,
            f"UNHEX('{parent_uuid}')" if parent_uuid else "NULL",
            writer_id,
            content,
        )

        return query

    @staticmethod
    def select_reply(sys_doc_num, parent_uuid):

        query = SELECT_REPLY.format(
            SELECT_SYSDOCNUM_CONDITION.format(sys_doc_num),
            f"AND R.PARENT_UUID = UNHEX('{parent_uuid}')"
            if parent_uuid
            else f"AND R.PARENT_UUID is NULL",
        )

        return query

    @staticmethod
    def check_reply(uuid, sys_doc_num, writer_id):
        query = CHECK_REPLY.format(
            REPLY_UUID_CONDITION.format(uuid),
            REPLY_SYSDOCNUM_CONDITION.format(sys_doc_num),
            REPLY_WRITERID_CONDITION.format(writer_id),
        )

        return query

    @staticmethod
    def update_reply(content, uuid):

        query = UPDATE_REPLY.format(content, REPLY_UUID_CONDITION.format(uuid))

        return query

    @staticmethod
    def delete_reply(uuid):

        query = DELETE_REPLY.format(REPLY_UUID_CONDITION.format(uuid))

        return query
