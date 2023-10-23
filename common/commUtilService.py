# _*_coding: utf-8 -*-
import json

# 공통으로 사용되는 Service 관리 Class
class commUtilService:
    def dataCheck(self, data):

        if (data == None) or (data == ""):
            return False

        return True

    def jsonDumps(self, data):
        return json.dumps(data, ensure_ascii=False)
