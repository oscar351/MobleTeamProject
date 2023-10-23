from asyncio import constants
import os
import shutil
import sys
import copy
import json
import re
import uuid
import io
import csv
import tempfile
from collections import Counter
from datetime import datetime

from allscapeAPIMain import db
from allscapeAPIMain import procCode
from allscapeAPIMain import procName
from allscapeAPIMain import spaceHome
from allscapeAPIMain import approvalBoardFile

from common import constants
from common.excelService import excelService
from common.logManage import logManage
from projectApprovalBoardManage.sqlProjectApprovalBoardManage import (
    sqlProjectApprovalBoardManage,
)
from logManage.servLogManage import servLogManage
from projectProcessManage.servProjectProcessManage import servProjectProcessManage
from projectProcessManage.sqlProjectProcessManage import sqlProjectProcessManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectApprovalBoardManage:
    """승인게시판 관리 Service Class"""

    def post_approval(
        self,
        cons_code,
        co_code,
        writer_id,
        post_type,
        title,
        content,
        approvals,
        files,
    ):
        """승인글 작성"""

        #### 승인글 업로드 ####
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        servProjProcMana = servProjectProcessManage()

        queryList = list()
        dataList = list()
        post_uuid = str(uuid.uuid4()).replace("-", "")  # 승인글 uuid 생성

        #### 승인글 작성 ####
        query = sqlProjectApprovalBoardManage.insert_approval(
            cons_code,
            post_uuid,
            writer_id,
            post_type,
            # title,
            # json.dumps(content, ensure_ascii=False),
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "insert_approval Query : " + query,
        )
        queryList.append(query)
        dataList.append([title, json.dumps(content, ensure_ascii=False)])
        #### 작성자 추가 ####
        query = sqlProjectApprovalBoardManage.insert_info(
            cons_code, post_uuid, writer_id, constants.APPRO_TYPE_CD_DRAFTER, 0
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "insert_approval_info Query : " + query,
        )
        queryList.append(query)
        dataList.append([])
        #### 기타 관련자 추가 ####

        if approvals:
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "approvals : " + str(approvals),
            )
            for _, approval in zip(range(1, len(approvals) + 1), approvals):
                for approver in approval:
                    query = sqlProjectApprovalBoardManage.insert_info(
                        cons_code,
                        post_uuid,
                        approver["id"],
                        approver["apr_type"],
                        approver["index"],
                    )
                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "insert_info Query : " + query,
                    )
                    queryList.append(query)
                    dataList.append([])

        resCd, msg, _ = dbms.executeIterSpecial(queryList, dataList)

        #### 승인글 uuid 정보를 추출하여 디렉토리 생성하기
        if resCd == 0:
            if files:
                file_path = "".join(
                    [
                        spaceHome,
                        approvalBoardFile.replace("{post_uuid}", post_uuid),
                    ]
                )
                os.makedirs(file_path, exist_ok=True)

                #### 파일 정보를 받아 DB 및 디렉토리에 저장하기
                file_dict = {
                    "f": 0,
                    "q": 1,
                }  # f: 기타, q: 견적
                for key in files.keys():
                    if not re.match("[f, q]_\d+", key):
                        continue
                    file_type = file_dict[key[0]]
                    upload_file = files[key]
                    ####  파일 기본정보 생성 및 저장 ####
                    orig_name = upload_file.filename
                    _, ext = os.path.splitext(orig_name)
                    chan_name = str(uuid.uuid4()).replace("-", "") + ext
                    upload_file.save(file_path + chan_name)

                    #### 파일 DB에 업로드 ####
                    query = sqlProjectApprovalBoardManage.insert_approval_file(
                        post_uuid,
                        file_path,
                        file_type,
                        chan_name,
                    )

                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "insert_approval_file Query : " + query,
                    )

                    resCd, msg, _ = dbms.executeSpecial(query, orig_name)

                    #### 파일 DB 등록 실패시 파일삭제 ####
                    if resCd != 0:
                        os.remove(file_path + chan_name)

        return resCd, msg, post_uuid

    def get_approval_list(
        self,
        id,
        cons_code,
        co_code,
        co_name,
        writer_name,
        post_type,
        title_keyword,
        content_keyword,
        reg_date_start,
        reg_date_end,
    ):
        """승인글 리스트 조회"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        servProcessMana = servProjectProcessManage()

        query = sqlProjectApprovalBoardManage.select_approval_list(
            id,
            cons_code,
            post_type,
            reg_date_start,
            reg_date_end,
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_approval_list Query : " + query,
        )

        resCd, msg, approvalList = dbms.querySpecial(
            query,
            [
                "%Y%m%d",
                "%Y%m%d",
                f"%{co_name}%",
                f"%{writer_name}%",
                f"%{title_keyword}%",
                f"%{content_keyword}%",
            ],
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_approval_list result : " + str(resCd) + str(msg),
        )
        return resCd, msg, approvalList

    def get_approval(self, id, cons_code, co_code, uuid):
        """승인글 조회"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        servProcessMana = servProjectProcessManage()

        #### 읽은 표시하기 ####
        query = sqlProjectApprovalBoardManage.update_readdate(cons_code, uuid, id)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_readdate Query : " + query,
        )
        resCd, msg, approvalData = dbms.execute(query)

        if resCd == 0:
            query = sqlProjectApprovalBoardManage.select_approval(cons_code, uuid)

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_approval Query : " + query,
            )

            resCd, msg, approvalData = dbms.queryForObject(query)
            try:
                jsonData = json.loads(approvalData["content"])
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "aaaaaaaaaaaaaaaaaaaaaaaa : " + jsonData,
                )
                approvalData = jsonData

                #approvalData['reason'] = jsonData['reason']
                #approvalData['content'] = jsonData['content']
                #approvalData['change_date'] = jsonData['change_date']


                approvalData.update(jsonData)
                #approvalData['content'] = jsonData

            except:
                pass

            #### 첨부파일 정보 첨가하기 ####
            if resCd == 0 and approvalData:
                query = sqlProjectApprovalBoardManage.select_approval_file(
                    approvalData["uuid"]
                )

                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "select_approval_file Query : " + query,
                )

                resCd, msg, fileData = dbms.query(query)
                if resCd == 0 and fileData:
                    approvalData["files"] = fileData

                #### 관련자 정보 첨가하기 ####
                if resCd == 0:
                    query = sqlProjectApprovalBoardManage.select_info_list(
                        cons_code, approvalData["uuid"]
                    )

                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "select_info_list Query : " + query,
                    )

                    resCd, msg, infoData = dbms.query(query)
                    if resCd == 0 and infoData:
                        approvalData["info"] = infoData

        return resCd, msg, approvalData

    def put_approval(
        self, cons_code, post_uuid, post_type, title, content, approvals, deletes, files
    ):
        """승인글 수정"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        queryList = list()

        #### 승인글 정보 초기화 ####
        query = sqlProjectApprovalBoardManage.update_approval_reset(
            cons_code, post_uuid
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_approval_reset Query : " + query,
        )
        queryList.append(query)

        #### 승인 상태 초기화 ####
        query = sqlProjectApprovalBoardManage.update_apr_reset(cons_code, post_uuid)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_apr_reset Query : " + query,
        )
        queryList.append(query)

        resCd, msg, _ = dbms.executeIter(queryList)

        #### 승인 초기화가 성공해야 수정작업 가능 ####
        if resCd == 0:

            #### 권한 수정 ####
            if approvals:
                query = sqlProjectApprovalBoardManage.delete_info_all(cons_code, post_uuid)
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "delete_info_all Query : " + query,
                )
                queryList.append(query)
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "approvals : " + str(approvals),
                )
                for _, approval in zip(range(1, len(approvals) + 1), approvals):
                    for approver in approval:
                        query = sqlProjectApprovalBoardManage.insert_info(
                            cons_code,
                            post_uuid,
                            approver["id"],
                            approver["apr_type"],
                            approver["index"],
                        )
                        logs.debug(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "insert_info Query : " + query,
                        )
                        queryList.append(query)

                resCd, msg, _ = dbms.executeIter(queryList)

            #### 승인글 수정 ####
            if post_type or title or content:
                query = sqlProjectApprovalBoardManage.update_approval(
                    cons_code,
                    post_uuid,
                    post_type,
                    # title,
                    # json.dumps({k: v.replace('\"', "'") for k, v in content.items()}, ensure_ascii=False),
                )

                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    f"update_approval Query : " + query,
                )

                resCd, msg, _ = dbms.executeSpecial(
                    query, [title, json.dumps(content, ensure_ascii=False)]
                )

            #### 파일 삭제 ####
            if deletes:
                delete_index = f"{','.join(str(num) for num in deletes)}"
                query = sqlProjectApprovalBoardManage.delete_approval_file(
                    post_uuid, delete_index
                )
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "delete_approval_file Query : " + query,
                )
                resCd, msg, _ = dbms.execute(query)

            #### 파일 추가 ####
            #### 승인글 uuid 정보를 추출하여 디렉토리 생성하기 ####
            if files:
                file_path = "".join(
                    [
                        spaceHome,
                        approvalBoardFile.replace("{post_uuid}", post_uuid),
                    ]
                )
                os.makedirs(file_path, exist_ok=True)

                #### 파일 정보를 받아 DB 및 디렉토리에 저장하기
                file_dict = {
                    "f": 0,
                    "q": 1,
                }  # f: 기타, q: 견적
                for key in files.keys():
                    if not re.match("[f, q]_\d+", key):
                        continue
                    file_type = file_dict[key[0]]
                    file = files[key]

                    ####  파일 기본정보 생성 및 저장 ####
                    orig_name = file.filename
                    _, ext = os.path.splitext(orig_name)
                    chan_name = str(uuid.uuid4()).replace("-", "") + ext
                    file.save(file_path + chan_name)

                    #### 파일 DB에 업로드 ####
                    query = sqlProjectApprovalBoardManage.insert_approval_file(
                        post_uuid,
                        file_path,
                        file_type,
                        chan_name,
                    )

                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "insert_approval_file Query : " + query,
                    )

                    resCd, msg, _ = dbms.executeSpecial(query, orig_name)

                    #### 파일 DB 등록 실패시 파일삭제 ####
                    if resCd != 0:
                        os.remove(file_path + chan_name)

        return resCd, msg, None

    def delete_approval(self, cons_code, uuid):
        """승인글 삭제"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectApprovalBoardManage.delete_approval(cons_code, uuid)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delete_approval Query : " + query,
        )

        resCd, msg, _ = dbms.execute(query)

        #### 관련 첨부파일 전부 삭제 ####
        """
        if resCd == 0:
            file_path = "".join(
                [spaceHome, approvalBoardFile.replace("{post_uuid}", uuid)]
            )
            shutil.rmtree(file_path, ignore_errors=True)
        """
        return resCd, msg, None

    def withdraw(self, cons_code, uuid):
        """승인글 철회"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectApprovalBoardManage.withdraw(cons_code, uuid)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "withdraw_approval Query : " + query,
        )

        resCd, msg, _ = dbms.execute(query)

        #### 관련 첨부파일 전부 삭제 ####
        """
        if resCd == 0:
            file_path = "".join(
                [spaceHome, approvalBoardFile.replace("{post_uuid}", uuid)]
            )
            shutil.rmtree(file_path, ignore_errors=True)
        """
        return resCd, msg, None

    def post_reply(self, post_uuid, parent_uuid, writer_id, content):
        """댓글 작성"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectApprovalBoardManage.insert_reply(
            post_uuid, parent_uuid, writer_id, content
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "insert_reply Query : " + query,
        )

        return dbms.executeMulti(query)

    def get_reply(self, post_uuid, parent_uuid) -> dict:
        """댓글 조회"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectApprovalBoardManage.select_reply(post_uuid, parent_uuid)

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
        query = sqlProjectApprovalBoardManage.update_reply(post_uuid, uuid, content)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_reply Query : " + query,
        )

        return dbms.execute(query)

    def del_reply(self, post_uuid, uuid) -> dict:
        """댓글 삭제"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectApprovalBoardManage.delete_reply(post_uuid, uuid)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delete_reply Query : " + query,
        )

        return dbms.execute(query)

    def draft(self, cons_code, post_uuid, id) -> dict:
        """결재 기안"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectApprovalBoardManage.update_drafted(cons_code, post_uuid, id)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_drafted Query : " + query,
        )

        return dbms.execute(query)

    def approve(self, cons_code, post_uuid, id, co_code, remarks) -> dict:
        """결재 승인"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectApprovalBoardManage.update_approved(cons_code, post_uuid, id)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_approve Query : " + query,
        )

        return dbms.executeSpecial(query, [remarks])

    def deny(self, cons_code, post_uuid, id, remarks) -> dict:
        """결재 거절"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectApprovalBoardManage.update_denied(cons_code, post_uuid, id)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_denied Query : " + query,
        )

        return dbms.executeSpecial(query, [remarks])
