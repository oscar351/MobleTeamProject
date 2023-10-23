import copy
import sys
import os

from allscapeAPIMain import db
from allscapeAPIMain import procName
from common import util_time
from common.logManage import logManage
from logManage.sqlLogManage import sqlLogManage

logs = logManage()


class servLogManage:
    @staticmethod
    def post_log(proc_code, log_level, title, content, id, resCd = 0, msg = ""):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sLogManage = sqlLogManage()
        log_data = {
            "proc_code": proc_code,
            "log_level": log_level,
            "log_title": title,
            "log_date": util_time.get_current_time(util_time.TIME_CURRENT_TYPE_14),
            "id": id,
            "resCd": resCd,
        }
        query = sLogManage.iLogData(log_data)
        
        #### 마스터의 조회는 로그기록 남기지않음 ####
        if id == 'master':
            return 0, "", None
        return dbms.executeSpecial(query, [content, msg])

    def get_log_list(self, log_id, title_keyword):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlLogManage.select_log_list(log_id, title_keyword)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_log_list Query : " + query,
        )

        data = list()
        if title_keyword:
            data.append(f"%{title_keyword}%")
        return dbms.querySpecial(query, data)

    def get_log(self, log_id):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlLogManage.select_log(log_id)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_log Query : " + query,
        )

        return dbms.queryForObject(query)
