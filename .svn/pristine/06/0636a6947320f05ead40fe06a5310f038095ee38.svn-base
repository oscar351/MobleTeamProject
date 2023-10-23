import os
import sys
import copy
import json
import re

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.commonService import commonService
from common.logManage import logManage

from common.commonService import commonService
from projectWorkReplyManage.sqlProjectWorkReplyManage import sqlProjectWorkReplyManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectWorkReplyManage:
    """작업일지 댓글 관리 Service Class"""

    def post_reply(self, sys_doc_num, parent_uuid, writer_id, content):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectWorkReplyManage.insert_reply(
            sys_doc_num, parent_uuid, writer_id, content
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "insert_reply Query : " + query,
        )

        return dbms.executeMulti(query)

    def get_reply(self, sys_doc_num, parent_uuid) -> dict:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectWorkReplyManage.select_reply(sys_doc_num, parent_uuid)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_reply Query : " + query,
        )

        return dbms.query(query)

    def check_reply(self, uuid, sys_doc_num, writer_id) -> dict:
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectWorkReplyManage.check_reply(uuid, sys_doc_num, writer_id)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "check_reply Query : " + query,
        )

        return dbms.queryForObject(query)

    def put_reply(self, content, uuid) -> dict:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectWorkReplyManage.update_reply(content, uuid)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_reply Query : " + query,
        )

        return dbms.execute(query)

    def del_reply(self, uuid) -> dict:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectWorkReplyManage.delete_reply(uuid)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delete_reply Query : " + query,
        )

        return dbms.execute(query)
