import copy
import os
import sys
from allscapeAPIMain import db
from allscapeAPIMain import procName
from common import util_time
from common.logManage import logManage

UPDATE_PROJECT_STATE = " ".join(
    [
        "UPDATE",
        "PROJECT",
        "SET",
        "PROJECT_STATUS = 'ST000002'",
        "WHERE 1=1",
        "AND PROJECT_STATUS = 'ST000001'",
        "AND CONS_START_DATE <= '{}'",
    ]
)


def update_project_state():
    """프로젝트 진행상태 업데이트"""

    dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
    query = UPDATE_PROJECT_STATE.format(
        util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14)
    )
    return dbms.execute(query)


if __name__ == "__main__":
    update_project_state()
