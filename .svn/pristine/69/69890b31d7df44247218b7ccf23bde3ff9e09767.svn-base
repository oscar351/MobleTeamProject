# _*_coding: utf-8 -*-

# Log 데이터 관리 Class
# 작성 날짜 : 2022. 7. 29
# 작성자 : 황희정
# 기능
# 	1. 2022. 07. 29 | Log 데이터 모델 반환
# 	2. 2022. 07. 29 | Log 데이터 반환
# 변경 이력
# 	1. 2022. 07. 29 | 황희정 | 최조 작성


class dataLogManage:
    # 1. Log 데이터 모델 반환
    def getLogDataModel(self):
        return {
            "prco_code": "",
            "log_level": "",
            "log_title": "",
            "log_content": "",
            "log_date": "",
            "id": "",
        }

    # 2. Log 데이터 반환
    #
    # Parameter
    # 	- proc_code | String | 프로세스 코드
    # 	- log_level | String | 로그 레벨
    # 	- log_content | String | 로그 내용
    # 	- log_date | String | 로그 날짜
    # 	- id | String | 로그 작성 ID
    def makeLogData(
        self, proc_code, log_level, log_title, log_date, id, log_content="", resCd=0, msg=""
    ):
        return {
            "proc_code": proc_code,
            "log_level": log_level,
            "log_title": log_title,
            "log_content": log_content,
            "log_date": log_date,
            "id": id,
            "resCd":resCd,
            "msg":msg
        }
