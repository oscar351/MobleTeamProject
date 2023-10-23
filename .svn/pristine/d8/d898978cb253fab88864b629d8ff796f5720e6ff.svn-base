# _*_coding: utf-8 -*-
import os
import sys
import copy

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.logManage import logManage
from common import constants

from projectFloorPlanManage.sqlProjectFloorPlanManage import sqlProjectFloorPlanManage
from projectDesignBookManage.sqlProjectDesignBookManage import (
    sqlProjectDesignBookManage,
)


logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectFloorPlanManage:
    """설계도면 이미지 관리 Service Class"""

    def postFloorPlan(self, params: dict) -> dict:
        """설계도면 이미지 등록"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        # 해당 조건의 이미지 도면 등록
        query = sqlProjectFloorPlanManage.insert(
            params["cons_code"],
            params["ver_info"],
            params["page"],
            params["subpage"],
            params["code"],
            params["title"],
            params["img_path"],
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "postFloorPlan Query : " + query,
        )

        return dbms.execute(query)

    def getFloorPlan(self, params: dict) -> dict:
        """도면 이미지 보기"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        # 주어진 조건을 검색한다
        query = sqlProjectFloorPlanManage.select(
            params["cons_code"], params["ver_info"], params["page"]
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "getFloorPlan Query : " + query,
        )

        return dbms.queryForObject(query)

    def getFloorPlanAll(self, params: dict) -> dict:
        """도면 전체 이미지 보기"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        # 주어진 조건을 검색한다
        query = sqlProjectFloorPlanManage.select_all(
            params["cons_code"], params["ver_info"]
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "getFloorPlanAll Query : " + query,
        )

        return dbms.query(query)

    def delFloorPlan(self, params: dict) -> dict:
        """도면 이미지 삭제"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        # 주어진 조건을 삭제한다
        query = sqlProjectFloorPlanManage.delete(
            params["cons_code"], params["ver_info"], params["page"]
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delFloorPlan Query : " + query,
        )

        return dbms.execute(query)

    def delFloorPlanAll(self, params: dict) -> dict:
        """도면 전체 이미지 삭제"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        # 주어진 조건을 삭제한다
        query = sqlProjectFloorPlanManage.delete_all(
            params["cons_code"], params["ver_info"]
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delFloorPlanAll Query : " + query,
        )

        return dbms.execute(query)
