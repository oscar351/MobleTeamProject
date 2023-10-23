# _*_coding: utf-8 -*-

import sys
import os


from common import constants
from common.dataCommonManage import dataCommonManage

from common.logManage import logManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class messageService:
    # 1. server fail err message
    def getCustomMessage(self, resCode, msg=""):
        message = ""
        if resCode == constants.REST_RESPONSE_CODE_SERVERFAIL:
            message = "System Error가 발생하였습니다. 시스템 관리자에게 문의 바랍니다."
        elif resCode == constants.REST_RESPONSE_CODE_DATAFAIL:
            message = msg
        elif resCode == constants.REST_RESPONSE_CODE_453:
            message = "비밀번호가 틀렸습니다. 비밀번호 확인 후 재로그인 하시기 바랍니다."
        elif resCode == constants.REST_RESPONSE_CODE_454:
            message = "일치하는 ID가 없습니다. ID 확인 후 재시도 하여 주시기 바랍니다."
        elif resCode == constants.REST_RESPONSE_CODE_455:
            message = "로그인 된 사용자 정보가 없습니다. 로그인 후 이용해 주시기 바랍니다."
        elif resCode == constants.REST_RESPONSE_CODE_456:
            message = "System Code가 없습니다."
        elif resCode == constants.REST_RESPONSE_CODE_457:
            message = "Token이 없습니다."
        elif resCode == constants.REST_RESPONSE_CODE_458:
            message = "ID에 대한 사용자 정보가 없습니다."
        elif resCode == constants.MARIADB_ERR_CD_COLUMN:
            message = "Column명을 확인 하시기 바랍니다."
        elif resCode == constants.MARIADB_ERR_CD_TOOLONG:
            message = "입력 데이터의 길이가 너무 깁니다."
        else:
            message = msg

        return message
