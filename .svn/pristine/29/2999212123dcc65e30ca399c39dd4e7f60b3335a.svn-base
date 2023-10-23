import os
import shutil
import sys
import copy
import json
import re
import uuid

from allscapeAPIMain import db
from allscapeAPIMain import procCode
from allscapeAPIMain import procName
from allscapeAPIMain import spaceHome
from allscapeAPIMain import messageBoardFile

from common import constants
from common.logManage import logManage
from logManage.servLogManage import servLogManage
from projectMessageBoardManage.sqlProjectMessageBoardManage import (
    sqlProjectMessageBoardManage,
)

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectMessageBoardManage:
    """게시판 관리 Service Class"""

    def post_message(
        self, cons_code, writer_id, post_type, scope, category, title, content, files
    ):
        """게시글 작성"""

        #### 게시글 업로드 ####
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        post_uuid = str(uuid.uuid4()).replace("-", "")  # 게시글 uuid 생성
        query = sqlProjectMessageBoardManage.insert_message(
            cons_code, post_uuid, writer_id, post_type, scope
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "insert_message Query : " + query,
        )

        resCd, msg, _ = dbms.executeSpecial(query, [category, title, content])
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "insert_message resCd : " + str(resCd) + str(msg),
        )
        #### 게시글 uuid 정보를 추출하여 디렉토리 생성하기
        if resCd == 0 and files:
            file_path = "".join(
                [
                    spaceHome,
                    messageBoardFile.replace("{post_uuid}", post_uuid),
                ]
            )
            os.makedirs(file_path, exist_ok=True)

            #### 파일 정보를 받아 DB 및 디렉토리에 저장하기
            for key in files.keys():
                if not re.match("f_\d+", key):
                    continue
                file = files[key]
                ####  파일 기본정보 생성 및 저장 ####
                orig_name = file.filename
                _, ext = os.path.splitext(orig_name)
                chan_name = str(uuid.uuid4()).replace("-", "") + ext
                file.save(file_path + chan_name)

                #### 파일 DB에 업로드 ####
                query = sqlProjectMessageBoardManage.insert_message_file(
                    post_uuid,
                    file_path,
                    chan_name,
                )

                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "insert_message_file Query : " + query,
                )

                resCd, msg, _ = dbms.executeSpecial(query, orig_name)

                #### 파일 DB 등록 실패시 파일삭제 ####
                if resCd != 0:
                    os.remove(file_path + chan_name)

        return resCd, msg, post_uuid

    def get_message_list(
        self,
        cons_code,
        co_code,
        id,
        co_name,
        writer_name,
        post_type,
        category_keyword,
        title_keyword,
        content_keyword,
        issued,
        reg_date_start,
        reg_date_end,
    ):
        """게시글 리스트 조회"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectMessageBoardManage.select_message_list(
            cons_code,
            co_code,
            id,
            post_type,
            issued,
            reg_date_start,
            reg_date_end,
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_message_list Query : " + query,
        )

        return dbms.querySpecial(
            query,
            [
                "%Y%m%d%H%i%S",
                f"%{co_name}%",
                f"%{writer_name}%",
                f"%{category_keyword}%",
                f"%{title_keyword}%",
                f"%{content_keyword}%",
            ],
        )

    def get_message(self, cons_code, uuid):
        """게시글 조회"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectMessageBoardManage.select_message(cons_code, uuid)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_message Query : " + query,
        )

        resCd, msg, messageData = dbms.queryForObject(query)

        #### 첨부파일 정보 첨가하기 ####
        if resCd == 0 and messageData:
            query = sqlProjectMessageBoardManage.select_message_file(
                messageData["uuid"]
            )

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_message_file Query : " + query,
            )

            resCd, msg, fileData = dbms.query(query)
            if resCd == 0 and fileData:
                messageData["files"] = fileData

        return resCd, msg, messageData

    def put_message(
        self,
        cons_code,
        post_uuid,
        post_type,
        scope,
        category,
        title,
        content,
        deletes,
        files,
    ):
        """게시글 수정"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectMessageBoardManage.select_lock(cons_code, post_uuid)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_lock Query : " + query,
        )
        resCd, msg, data = dbms.queryForObject(query)
        if not data or data["issued"] == 1:
            return constants.REST_RESPONSE_CODE_DATAFAIL, "해당 게시글은 잠겨있습니다", None

        if post_type or title or content:
            query = sqlProjectMessageBoardManage.update_message(
                cons_code, post_uuid, post_type, scope
            )

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "update_message Query : " + query,
            )

            resCd, msg, _ = dbms.executeSpecial(query, [category, title, content])

        #### 파일 삭제 ####
        if resCd == 0 and deletes:
            delete_index = f"{','.join(str(num) for num in deletes)}"
            query = sqlProjectMessageBoardManage.delete_message_file(
                post_uuid, delete_index
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "delete_message_file Query : " + query,
            )
            resCd, msg, _ = dbms.execute(query)

        #### 파일 추가 ####
        #### 게시글 uuid 정보를 추출하여 디렉토리 생성하기 ####
        if resCd == 0 and files:
            file_path = "".join(
                [
                    spaceHome,
                    messageBoardFile.replace("{post_uuid}", post_uuid),
                ]
            )
            os.makedirs(file_path, exist_ok=True)

            #### 파일 정보를 받아 DB 및 디렉토리에 저장하기 ####
            for key in files.keys():
                if not re.match("f_\d+", key):
                    continue
                file = files[key]

                ####  파일 기본정보 생성 및 저장 ####
                orig_name = file.filename
                _, ext = os.path.splitext(orig_name)
                chan_name = str(uuid.uuid4()).replace("-", "") + ext
                file.save(file_path + chan_name)

                #### 파일 DB에 업로드 ####
                query = sqlProjectMessageBoardManage.insert_message_file(
                    post_uuid,
                    file_path,
                    chan_name,
                )

                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "insert_message_file Query : " + query,
                )

                resCd, msg, _ = dbms.executeSpecial(query, orig_name)

                #### 파일 DB 등록 실패시 파일삭제 ####
                if resCd != 0:
                    os.remove(file_path + chan_name)

        return resCd, msg, None

    def lock_message(self, cons_code, uuid, issued):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectMessageBoardManage.lock_message(cons_code, uuid, issued)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "lock_message Query : " + query,
        )

        return dbms.execute(query)

    def del_message(self, cons_code, uuid):
        """게시글 삭제"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectMessageBoardManage.select_lock(cons_code, uuid)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_lock Query : " + query,
        )
        resCd, msg, data = dbms.queryForObject(query)
        if not data or data["issued"] == 1:
            return constants.REST_RESPONSE_CODE_DATAFAIL, "해당 게시글은 잠겨있습니다", None

        query = sqlProjectMessageBoardManage.delete_message(cons_code, uuid)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delete_message Query : " + query,
        )

        resCd, msg, _ = dbms.execute(query)

        #### 관련 첨부파일 전부 삭제 - 비활성화 ####
        """
        if resCd == 0:
            file_path = "".join(
                [spaceHome, messageBoardFile.replace("{post_uuid}", uuid)]
            )
            shutil.rmtree(file_path, ignore_errors=True)
        """
        return resCd, msg, None

    def post_reply(self, post_uuid, parent_uuid, writer_id, content):
        """댓글 작성"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectMessageBoardManage.insert_reply(
            post_uuid, parent_uuid, writer_id
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "insert_reply Query : " + query,
        )

        return dbms.executeMultiSpeical(query, content)

    def get_reply(self, post_uuid, parent_uuid) -> dict:
        """댓글 조회"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectMessageBoardManage.select_reply(post_uuid, parent_uuid)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_reply Query : " + query,
        )

        return dbms.query(query)

    def put_reply(self, post_uuid, uuid, content) -> dict:
        """댓글 수정"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectMessageBoardManage.update_reply(post_uuid, uuid)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_reply Query : " + query,
        )

        return dbms.executeSpecial(query, content)

    def del_reply(self, post_uuid, uuid) -> dict:
        """댓글 삭제"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectMessageBoardManage.delete_reply(post_uuid, uuid)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delete_reply Query : " + query,
        )

        return dbms.execute(query)
