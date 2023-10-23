# _*_coding: utf-8 -*-
import os
import sys
import copy
from unicodedata import decimal
import uuid
import shutil
from decimal import *

from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import spaceHome
from allscapeAPIMain import workLogImgFile

from common.logManage import logManage

from projectWorkLogManage.sqlProjectWorkLogManage import sqlProjectWorkLogManage
from projectProcessManage.servProjectProcessManage import servProjectProcessManage
from common.commonService import commonService

from common import constants

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectWorkLogManage:
    # 직종 통계 정보를 가져 온다.
    def getOccStatList(self, consCode, coCode):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.sGetOccStatList(consCode, coCode)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetOccStatList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 장비 통계 정보를 가져 온다.
    def getEquStatList(self, consCode, coCode):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.sGetEquStatList(consCode, coCode)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetEquStatList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 자재 사용량 통계 정보를 가져온다.
    def getWorkLoadStatList(self, consCode, coCode):
        commServ = commonService()
        errMsg = ""
        try:
            dbms = copy.copy(db)
            sProjWorkLogMana = sqlProjectWorkLogManage()

            query = sProjWorkLogMana.sGetWorkLoadStatList(consCode, coCode)

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "sGetWorkLoadStatList Query : " + query,
            )

            # 쿼리 실행
            resCd, msg, resData = dbms.query(query)

            return resCd, msg, resData
        except KeyError as e:
            errMsg = str(e)
        except NameError as e:
            errMsg = str(e)
        except TypeError as e:
            errMsg = str(e)
        except AttributeError as e:
            errMsg = str(e)
        except Exception as e:
            errMsg = str(e)

        return constants.REST_RESPONSE_CODE_DATAFAIL, errMsg, None

    # 작업 일지 데이터를 저장 한다.
    def putWorkLog(self, params, docDefaultInfo, writeStandardName):
        commServ = commonService()
        errMsg = ""
        try:
            dbms = copy.copy(db)
            sProjWorkLogMana = sqlProjectWorkLogManage()

            query = sProjWorkLogMana.iPutWorkLog(
                params, docDefaultInfo, writeStandardName
            )
            if query == None:
                return (
                    constants.REST_RESPONSE_CODE_DATAFAIL,
                    "Query를 생성 할 수 없습니다.",
                    None,
                )

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "iPutWorkLog Query : " + query,
            )

            # 쿼리 실행
            resCd, msg, resData = dbms.execute(query)

            return resCd, msg, resData
        except KeyError as e:
            errMsg = str(e)
        except NameError as e:
            errMsg = str(e)
        except TypeError as e:
            errMsg = str(e)
        except AttributeError as e:
            errMsg = str(e)
        except Exception as e:
            errMsg = str(e)

        return constants.REST_RESPONSE_CODE_DATAFAIL, errMsg, None

    # 작업 일지 데이터를 삭제 한다.
    def delWorkLog(self, consCode, sysDocNum):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.dDelWorkLog(consCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelWorkLog Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

        # 금일 작업 내용 데이터 저장

    def putWorkLogToday(self, consCode, workLogToday, docDefaultInfo, workDate):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.iPutWorkLogToday(
            consCode, docDefaultInfo, workLogToday, workDate
        )  # 금일 작업 내용 저장
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutWorkLogToday Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)
        if resCd != 0:
            return resCd, msg, resData

        if len(workLogToday["drawingList"]) > 0:
            drawingList = workLogToday["drawingList"]

            for drawing in drawingList:
                query = sProjWorkLogMana.iPutWorkLogDrawing(
                    params["reqDocInfo"]["cons_code"],
                    docDefaultInfo["sysDocNum"],
                    workLogToday["order"],
                    drawing,
                )  # 관련 도면 저장
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "iPutWorkLogDrawing Query : " + query,
                )

                # 쿼리 실행
                resCd, msg, resData = dbms.execute(query)
                if resCd != 0:
                    return resCd, msg, resData

        return resCd, msg, resData

    # 작업 일지 데이터를 삭제 한다.
    def delWorkLogToday(self, consCode, sysDocNum):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.dDelWorkLogToday(consCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelWorkLogToday Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

        # 관련 도면을 삭제 한다.

    def delWorkLogDrawing(self, consCode, sysDocNum):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.dDelWorkLogDrawing(consCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelWorkLogDrawing Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

    # 금일 인력 통계 정보를 저장 한다.
    def putWorkLogTodayWorkerStatistics(self, occStatData, coCode):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.iPutWorkLogTodayWorkerStatistics(occStatData, coCode)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutWorkLogTodayWorkerStatistics Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 금일 인력 통계 정보를 삭제 한다.
    def delWorkLogTodayWorkerStatistics(self, consCode, sysDocNum):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.dDelWorkLogTodayWorkerStatistics(consCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelWorkLogTodayWorkerStatistics Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

        # 금일 장비 투입 현황 데이터 저장

    def putWorkLogTodayInputEquipStatus(
        self, consCode, todayInputEquipStatus, docDefaultInfo
    ):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.iPutWorkLogTodayInputEquipStatus(
            consCode, docDefaultInfo, todayInputEquipStatus
        )  # 금일 작업 내용 저장

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutWorkLogTodayInputEquipStatus Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 금일 장비 투입 현황 데이터를 삭제 한다.
    def delWorkLogTodayInputEquipStatus(self, consCode, sysDocNum):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.dDelWorkLogTodayInputEquipStatus(consCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelWorkLogTodayInputEquipStatus Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 금일 장비 통계 정보를 저장 한다.
    def putWorkLogTodayInputEquipStatistics(self, equipStatData, coCode):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.iPutWorkLogTodayInputEquipStatistics(
            equipStatData, coCode
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutWorkLogTodayInputEquipStatistics Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 금일 장비 통계 정보를 삭제 한다.
    def delWorkLogTodayInputEquipStatistics(self, consCode, sysDocNum):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.dDelWorkLogTodayInputEquipStatistics(
            consCode, sysDocNum
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelWorkLogTodayInputEquipStatistics Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

        # 특이 사항 데이터 저장

    def putWorkLogUniqueness(self, params, docDefaultInfo):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        uniquenessList = params["reqDocContent"]["uniquenessList"]

        for uniqueness in uniquenessList:
            query = sProjWorkLogMana.iPutWorkLogUniqueness(
                params["reqDocInfo"]["cons_code"], docDefaultInfo, uniqueness
            )

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "iPutWorkLogUniqueness Query : " + query,
            )

            # 쿼리 실행
            resCd, msg, resData = dbms.execute(query)
            if resCd != 0:
                return resCd, msg, None

        return resCd, msg, resData

    # 특이 사항 데이터 삭제
    def delWorkLogUniqueness(self, consCode, sysDocNum):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.dDelWorkLogUniqueness(consCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelWorkLogUniqueness Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

        # 명일 예상 작업 데이터 저장

    def putWorkLogExceptedWorkTom(self, params, docDefaultInfo):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        exceptedWorkTomList = params["reqDocContent"]["exceptedWorkTomList"]

        for exceptedWorkTom in exceptedWorkTomList:
            query = sProjWorkLogMana.iPutWorkLogExceptedWorkTom(
                params["reqDocInfo"]["cons_code"], docDefaultInfo, exceptedWorkTom
            )

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "iPutWorkLogExceptedWorkTom Query : " + query,
            )

            # 쿼리 실행
            resCd, msg, resData = dbms.execute(query)
            if resCd != 0:
                return resCd, msg, None

        return resCd, msg, resData

    # 명일 예상 작업 데이터 삭제
    def delWorkLogExceptedWorkTom(self, consCode, sysDocNum):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.dDelWorkLogExceptedWorkTom(consCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelWorkLogExceptedWorkTom Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)
        return resCd, msg, resData

    # 자재 사용량 데이터 정보를 저장 한다.
    def putWorkLogWorkLoad(self, workLoadStat, workDate):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.iPutWorkLogWorkLoad(workLoadStat, workDate)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutWorkLogWorkLoad Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 자재 사용량 데이터 정보를 삭제 한다.
    def delWorkLogWorkLoad(self, consCode, sysDocNum):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.dDelWorkLogWorkLoad(consCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelWorkLogWorkLoad Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 작업일지 리스트를 조회 한다..
    def searchWorkLogList(self, userInfo, userAuth, jobAuth, params):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.sSearchWorkLogList(userInfo, userAuth, jobAuth, params)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchWorkLogList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 작업일지 리스트 개수를 조회 한다..
    def searchWorkLogListCnt(self, userInfo, userAuth, jobAuth, params):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.sSearchWorkLogListCnt(
            userInfo, userAuth, jobAuth, params
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchWorkLogListCnt Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 작업 이미지 리스트를 조회 한다.
    def searchWorkImgList(
        self, consCode, authCode, co_code, searchStartDate, searchEndDate, search_name
    ):

        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.sSearchWorkImgList(
            consCode, authCode, co_code, searchStartDate, searchEndDate, search_name
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchWorkImgList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 본사관리자 전용 작업일지 리스트 조회: 참여날짜에 구애받지 않고 작업일지 리스트를 조회한다
    def get_workdiary_master(self, cons_code, co_code, start_date, end_date):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.select_workdiary_master(
            cons_code, co_code, start_date, end_date
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "get_workdiary_master Query : " + query,
        )

        return dbms.query(query)

    # 작업일지 리스트를 조회한다
    def get_workdiary(self, cons_code, co_code, start_date, end_date):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.select_workdiary(
            cons_code, co_code, start_date, end_date
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "get_workdiary Query : " + query,
        )

        return dbms.query(query)

    # 작업일지를 삭제한다
    #### 작업로그들의 내용을 삭제 전 반영제거
    def del_workdiary(self, cons_code, co_code, sys_doc_num):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()
        servProjProMana = servProjectProcessManage()
        servProjWorkLogMana = servProjectWorkLogManage()

        #### 일지에 포함된 품목을 검색 ####
        query = sProjWorkLogMana.select_worklogconscode(cons_code, co_code, sys_doc_num)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "get_worklogconscode Query : " + query,
        )

        resCd, msg, resData = dbms.query(query)
        if resCd == 0:
            if resData:
                for data in resData:
                    resCd, msg, _ = servProjWorkLogMana.changePrevWorkloadPutLog(
                        cons_code,
                        co_code,
                        data["work_log_cons_code"],
                        data["cons_date"],
                        0,
                    )
                    if resCd == 0:
                        resCd, msg, _ = servProjProMana.update_process_auto(
                            cons_code, co_code, data["work_log_cons_code"]
                        )
            query = sProjWorkLogMana.delete_workdiary(cons_code, co_code, sys_doc_num)

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "delete_workdiary Query : " + query,
            )

            resCd, msg, _ = dbms.execute(query)

            ##### 삭제 성공 시 관련 이미지 파일도 삭제 ####
            if resCd == 0:
                path = workLogImgFile.replace("{consCode}", cons_code)
                path = path.replace("{sysDocNum}", sys_doc_num)
                path = spaceHome + path

                if os.path.exists(path):
                    shutil.rmtree(path)

        return resCd, msg, resData

    # 일일 작업일지 및 작업로그들을 조회한다
    def get_workdetails(self, cons_code, sys_doc_num, co_code):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()
        servProcessMana = servProjectProcessManage()

        # 		query = sProjWorkLogMana.select_sysnum(cons_code, co_code, cons_date)

        # 		logs.debug(procName,
        # 				os.path.basename(__file__),
        # 				sys._getframe(0).f_code.co_name,
        # 				"select_sysnum : " + query)

        # 		# 시스템 코드 탐색
        # 		resCd, msg, keyData = dbms.queryForObject(query)
        # 		if resCd != 0:
        # 			return resCd, msg, None

        # 		if not keyData:
        # 			return constants.REST_RESPONSE_CODE_DATAFAIL, "해당일 기록이 없습니다", None

        # syskey = keyData["sys_key"]
        # result = {"cons_code": cons_code, "co_code": co_code, "cons_date": cons_date}

        # 작업일지 내용 검색
        query = sProjWorkLogMana.select_workdiary_detail(
            cons_code, sys_doc_num, co_code
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "workdiary_detail : " + query,
        )

        resCd, msg, WDcontent = dbms.queryForObject(query)
        if resCd != 0 or not WDcontent:
            return resCd, msg, None

        # 작업일지 이미지 검색
        # query = sProjWorkLogMana.select_workdiary_image(syskey, co_code)
        # logs.debug(procName,
        # 		os.path.basename(__file__),
        # 		sys._getframe(0).f_code.co_name,
        # 		"workdiary_image : " + query)

        # resCd, msg, WDimage = dbms.query(query)
        # if resCd != 0:
        # 	return resCd, msg, None

        # diaryData = {"content": WDcontent, "imageList": WDimage}
        # result["diary"] = diaryData

        resultData = {
            "cons_code": WDcontent["cons_code"],
            "cons_name": WDcontent["cons_name"],
            "cons_date": WDcontent["cons_date"],
            "cons_work_info": [],
            "cons_content_info": {
                "temperature": WDcontent["temp"],
                "pty_result": WDcontent["pty_result"],
                "sky_result": WDcontent["sky_result"],
                "today_content": WDcontent["today_content"],
                "next_content": WDcontent["next_content"],
            },
            "cons_manp_info": [],
            "work_diary": WDcontent["content"],
            "id": WDcontent["id"],
        }

        # 작업로그 내용 검색
        query = sProjWorkLogMana.select_worklog_detail(cons_code, sys_doc_num, co_code)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "worklog_detail_last : " + query,
        )

        resCd, msg, WLcontents = dbms.query(query)
        if resCd != 0:
            return resCd, msg, None

        # 작업로그 별 이미지 및 공사명 검색
        logData = list()
        for WLcontent in WLcontents:

            # 			level1, level2, level3 = WLcontent["cons_code"][0:2], WLcontent["cons_code"][2:4], WLcontent["cons_code"][4:6]

            # 			logs.debug(procName,
            # 					os.path.basename(__file__),
            # 					sys._getframe(0).f_code.co_name,
            # 					"do get_process_names")
            #
            # 			resCd, msg, WLnames = servProcessMana.get_process_names(cons_code, co_code, level1, level2, level3)
            #
            # 			if resCd != 0:
            # 				return resCd, msg, None

            # 			WLcontent["level1_name"], WLcontent["level2_name"], WLcontent["level3_name"] = WLnames["level1_name"], WLnames["level2_name"], WLnames["level3_name"]
            #### 전일 작업량 계산 ####
            query = sProjWorkLogMana.select_worklog_prevwork(
                cons_code,
                co_code,
                WDcontent["cons_date"],
                WLcontent["work_log_cons_code"],
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_worklog_prevwork : " + query,
            )
            resCd, msg, prevData = dbms.queryForObject(query)
            if resCd == 0:
                prev_workload = Decimal(prevData["raw_prev_workload"])
                today_workload = Decimal(WLcontent["raw_today_workload"])
                next_workload = Decimal(WLcontent["raw_next_workload"])
                total = Decimal(WLcontent["raw_total"])
                WLcontent["prev_workload"] = round(prev_workload / 100, 2)
                WLcontent["today_workload"] = round(today_workload / 100, 2)
                WLcontent["next_workload"] = round(next_workload / 100, 2)
                WLcontent["quantity"] = round(total / 100, 2)
                WLcontent["prev_acc_percent"] = (
                    round(prev_workload / total * 100, 1) if total != 0 else 0
                )
                WLcontent["today_acc_percent"] = (
                    round((prev_workload + today_workload) / total * 100, 1)
                    if total != 0
                    else 0
                )
                query = sProjWorkLogMana.select_worklog_image(
                    cons_code,
                    sys_doc_num,
                    co_code,
                    WLcontent["cons_type_cd"],
                    WLcontent["work_log_cons_code"],
                )

                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "select_worklog_image : " + query,
                )

                resCd, msg, WLimage = dbms.query(query)
                if resCd != 0:
                    return resCd, msg, None

                WLcontent["imageList"] = WLimage
                logData.append(WLcontent)

        resultData["cons_work_info"] = logData

        # 투입 인력 정보를 조회 한다.
        query = sProjWorkLogMana.select_worklog_manp(cons_code, sys_doc_num, co_code)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_worklog_manp : " + query,
        )

        resCd, msg, WLmanp = dbms.query(query)
        if resCd != 0:
            return resCd, msg, None

        resultData["cons_manp_info"] = WLmanp

        return resCd, msg, resultData

        # 0203 희정 추가

    # 작업 일지를 저장 한다.
    def putDiaryInfo(self, diaryInfo):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.iPutDiaryInfo(diaryInfo)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutDiaryInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 작업 일지를 수정 한다.
    def changeDiaryInfo(self, id, diaryInfo, sys_num):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.update_Diary(
            diaryInfo["work_diary_content"],
            id,
            diaryInfo["today_content"],
            diaryInfo["next_content"],
            diaryInfo["temperature"],
            diaryInfo["sky_result"],
            diaryInfo["pty_result"],
            sys_num,
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_DiaryInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData
        # 0203 희정 추가

    # 작업 일지를 삭제 한다.
    def deleteDiaryInfo(self, sys_num):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.delete_Diary(sys_num)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delete_Diary Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 작업 일보를 저장 한다.
    def putWorkLogInfo(self, workLogInfo):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.iPutWorkLogInfo(workLogInfo)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutWorkLogInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

        # 0203 희정 추가

    #### 작업 로그 수정
    #### 1. 작업로그에 작성 시도
    #### 2. 관련 이미지 파일 저장
    #### 3. 관련 이미지 DB 등록
    #### 4. DB 등록 실패시 관련 이미지 파일 삭제
    def postWorkLogInfo(self, cons_code, co_code, LogInfo, sys_doc_num, files):
        dbms = copy.copy(db)
        commServ = commonService()
        sProjWorkLogMana = sqlProjectWorkLogManage()

        lv1, lv2, lv3, lv4 = (
            int(LogInfo["work_log_cons_code"][0:2]),
            int(LogInfo["work_log_cons_code"][2:4]),
            int(LogInfo["work_log_cons_code"][4:6]),
            int(LogInfo["work_log_cons_code"][6:]),
        )

        query = sProjWorkLogMana.insert_WorkLog(
            co_code,
            sys_doc_num,
            LogInfo["work_log_cons_code"],
            lv1,
            lv2,
            lv3,
            lv4,
            LogInfo["cons_type_cd"],
            LogInfo["today_workload"],
            LogInfo["next_workload"],
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_WorkLog Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)
        if resCd == 0:
            path = workLogImgFile.replace("{consCode}", cons_code)
            path = path.replace("{sysDocNum}", sys_doc_num)
            path = spaceHome + path
            for index, file in zip(range(len(files)), files):
                orig_name = file.filename
                _, ext = os.path.splitext(orig_name)
                chan_name = str(uuid.uuid4()) + ext
                file.save(path + chan_name)
                query = sProjWorkLogMana.insert_worklog_image(
                    cons_code,
                    co_code,
                    LogInfo["cons_date"],
                    sys_doc_num,
                    LogInfo["work_log_cons_code"],
                    LogInfo["cons_type_cd"],
                    index,
                    LogInfo["title"][index],
                    path,
                    orig_name,
                    chan_name,
                )
                resCd, msg, resData = dbms.execute(query)
                if resCd != 0:
                    os.remove(path + chan_name)

        return resCd, msg, resData

    def changeWorkLogInfo(self, LogInfo, sys_doc_num):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.update_WorkLog(
            LogInfo["today_workload"],
            LogInfo["next_workload"],
            sys_doc_num,
            LogInfo["work_log_cons_code"],
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_WorkLog Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    #### 로그 작성시 해당 로그 이전 작업량 업데이트 ####
    def changePrevWorkloadPostLog(
        self, cons_code, co_code, worklog_cons_code, cons_date
    ):
        """로그 작성시 해당 로그 prev_workload 업데이트"""
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.update_prevworkload_post_log(
            cons_code, co_code, worklog_cons_code, cons_date
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_prevworkload_post_log Query : " + query,
        )

        return dbms.executeMulti(query)

    #### 로그 수정시 해당 로그 이후인 로그들 이전 작업량 업데이트 ####
    def changePrevWorkloadPutLog(
        self, cons_code, co_code, worklog_cons_code, cons_date, today_workload
    ):
        """로그 작성/수정시 해당 로그 이후인 로그들 prev_workload 업데이트"""
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.update_prevworkload_put_log(
            cons_code, co_code, worklog_cons_code, cons_date, today_workload
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_prevworkload_put_log Query : " + query,
        )

        return dbms.executeMulti(query)

    #### 로그 추가시 해당 로그 이후인 로그들 이전 작업량 업데이트 ####
    def changePrevWorkloadPutLog2(
        self, cons_code, co_code, worklog_cons_code, cons_date
    ):
        """로그 작성/수정시 해당 로그 이후인 로그들 prev_workload 업데이트"""
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.update_prevworkload_put_log2(
            cons_code, co_code, worklog_cons_code, cons_date
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_prevworkload_put_log2 Query : " + query,
        )

        return dbms.executeMulti(query)

    def deleteWorkLogInfo(self, cons_code, co_code, LogInfo, sys_doc_num):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.select_worklog_image_for_delete(
            cons_code,
            sys_doc_num,
            co_code,
            LogInfo["cons_type_cd"],
            LogInfo["work_log_cons_code"],
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_worklog_image Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, logimages = dbms.query(query)
        if resCd == 0:
            for image in logimages:
                if os.path.exists(image["img_path"] + image["chan_name"]):
                    os.remove(image["img_path"] + image["chan_name"])

            query = sProjWorkLogMana.delete_worklog_image_for_delete(
                cons_code, sys_doc_num, co_code, LogInfo["work_log_cons_code"]
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "delete_worklog_image_for_delete Query : " + query,
            )

            # 쿼리 실행
            resCd, msg, logimages = dbms.query(query)
            if resCd == 0:
                query = sProjWorkLogMana.delete_Worklog(
                    sys_doc_num,
                    LogInfo["work_log_cons_code"],
                )

                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "delete_Worklog Query : " + query,
                )

                # 쿼리 실행
                resCd, msg, _ = dbms.execute(query)

        return resCd, msg, None

    def postWorkLogImage(self, cons_code, co_code, ImageInfo, sys_doc_num, index, file):
        dbms = copy.copy(db)
        commServ = commonService()

        sProjWorkLogMana = sqlProjectWorkLogManage()

        path = workLogImgFile.replace("{consCode}", cons_code)
        path = path.replace("{sysDocNum}", sys_doc_num)
        path = spaceHome + path
        orig_name = file.filename
        _, ext = os.path.splitext(orig_name)
        chan_name = str(uuid.uuid4()) + ext
        if not os.path.exists(path):
            os.makedirs(path)
        file.save(path + chan_name)
        query = sProjWorkLogMana.insert_worklog_image(
            cons_code,
            co_code,
            ImageInfo["cons_date"],
            sys_doc_num,
            ImageInfo["work_log_cons_code"],
            ImageInfo["cons_type_cd"],
            index,
            ImageInfo["title"],
            path,
            orig_name,
            chan_name,
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "insert_worklog_image Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)
        if resCd != 0:
            if os.path.exists(path + chan_name):
                os.remove(path + chan_name)
        return resCd, msg, resData

    def putWorkLogImage(
        self, cons_code, co_code, sys_doc_num, work_log_cons_code, index, title
    ):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.update_worklog_image(
            cons_code, sys_doc_num, co_code, work_log_cons_code, index, title
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_worklog_image Query : " + query,
        )

        return dbms.execute(query)

    def deleteWorkLogImage(
        self, cons_code, co_code, sys_doc_num, work_log_cons_code, index
    ):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.select_worklog_image_for_delete(
            cons_code, sys_doc_num, co_code, work_log_cons_code, index
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_worklog_image_for_delete Query : " + query,
        )
        resCd, msg, resData = dbms.queryForObject(query)
        if resCd == 0:
            path, chan_name = resData["img_path"], resData["chan_name"]
            query = sProjWorkLogMana.delete_worklog_image(
                cons_code,
                sys_doc_num,
                co_code,
                work_log_cons_code,
                index,
            )

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "delete_worklog_image Query : " + query,
            )

            resCd, msg, resData = dbms.execute(query)
            if resCd == 0:
                if os.path.exists(path + chan_name):
                    os.remove(path + chan_name)
        return resCd, msg, resData

    # 작업 투입 인력 정보를 저장 한다.
    def putWorkManpowerInfo(self, manpowerInfo):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.iPutWorkManpowerInfo(manpowerInfo)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPupWorkManpowerInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

        # 0203 희정 추가

    def postManpowerInfo(self, cons_code, co_code, manpowerInfo, sys_doc_num):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.insert_WorkManpower(
            cons_code,
            co_code,
            manpowerInfo["cons_date"],
            sys_doc_num,
            manpowerInfo["cons_type_cd"],
            manpowerInfo["work_log_cons_code"],
            manpowerInfo["prev_manpower"],
            manpowerInfo["today_manpower"],
            manpowerInfo["next_manpower"],
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_WorkManpower Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    def changeManpowerInfo(self, manpowerInfo, sys_num):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.update_WorkManpower(
            manpowerInfo["today_manpower"],
            manpowerInfo["next_manpower"],
            sys_num,
            manpowerInfo["work_log_cons_code"],
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_WorkManpower Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    def deleteManpowerInfo(self, manpowerInfo, sys_num):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.delete_WorkManpower(
            sys_num,
            manpowerInfo["work_log_cons_code"],
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delete_WorkManpower Query : " + query,
        )

        # 쿼리 실행
        return dbms.execute(query)

    # 작업 일지를 삭제 한다.
    def delDiaryInfo(self, consCode, coCode, sysDocNum):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.dDelDiaryInfo(consCode, coCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelDiaryInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

        # 0203 희정 추가

    # 작업 일보를 삭제 한다.
    def delWorkLogInfo(self, consCode, coCode, sysDocNum):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.dDelWorkLogInfo(consCode, coCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelWorkLogInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

        # 0203 희정 추가

    # 작업 일지/일보 이미지를 관리 한다.
    def imageFileManage(self, saveType, dataInfo, fileList, req):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjWorkLogMana = sqlProjectWorkLogManage()
        commServ = commonService()

        result = []
        index = 0
        sysDocNum = dataInfo["sys_doc_num"]
        sysDocNum = str(sysDocNum)
        path = workLogImgFile.replace("{consCode}", dataInfo["cons_code"])
        path = path.replace("{sysDocNum}", sysDocNum)

        for fileInfo in fileList:
            if fileInfo["file_type"] == "A":
                lpath = spaceHome + path
                origName =  fileInfo["file_name"]
                _, ext = os.path.splitext(origName)
                changeName = str(uuid.uuid4()) + ext

                fileData = {
                    "file_path": lpath,
                    "file_original_name": origName,
                    "file_change_name": changeName,
                }

                result.append(fileData)

                commServ.createDir(lpath)

                recvFileName = ""

                if saveType == "Diary":
                    recvFileName = "f_" + fileInfo["file_index"] + "_diary"
                elif saveType == "Log":
                    recvFileName = (
                        "f_"
                        + dataInfo["log_index"]
                        + "_"
                        + fileInfo["file_index"]
                        + "_log"
                    )

                commServ.saveFile(req.files[recvFileName], lpath, changeName)

                query = sProjWorkLogMana.iPutWorkImageFileInfo(
                    dataInfo, fileInfo["file_index"], fileInfo["file_desc"], fileData
                )
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "iPutWorkImageFileInfo Query : " + query,
                )

                resCd, msg, resData = dbms.execute(query)
                if resCd != 0:
                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "message : " + msg,
                    )
                    return resCd, msg, resData

            index += 1

        return constants.REST_RESPONSE_CODE_ZERO, "", result

        # 0203 희정 추가

    # 작업 일보를 삭제 한다.
    def delImageFileInfo(self, consCode, coCode, sysDocNum):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.dDelImageFileInfo(consCode, coCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelImageFileInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

        # 0207 희정 추가

    # 작업 투입 인력 정보를 삭제 한다.
    def delWorkManpowerInfo(self, consCode, coCode, sysDocNum):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.dDelWorkManpowerInfo(consCode, coCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelWorkManpowerInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

        # 0203 희정 추가

    # 관련 이미지 파일을 모두 가져 온다.
    def getImageFileInfo(self, consCode, coCode, sysDocNum):
        dbms = copy.copy(db)
        sProjWorkLogMana = sqlProjectWorkLogManage()

        query = sProjWorkLogMana.sGetImageFileInfo(consCode, coCode, sysDocNum)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetImageFileInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

        # 0203 희정 추가

    # 관련 이미지 파일을 스토리지에서 모두 삭제 한다.
    def removeImageFile(self, fileInfoList):
        commServ = commonService()

        for fileInfo in fileInfoList:
            commServ.removeFile(fileInfo["image_path"], fileInfo["image_chan_name"])

    # folder, ext = os.path.splitext(
    # 					fileInfo["image_path"] + fileInfo["image_chan_name"]
    # 					)

    #### 0210 조현우 추가
    #### 유저가 해당 문서 권한(해당 프로젝트에 속함)이 있는지 확인한다

    def check_sysnum_userauth(self, sys_doc_num, id):
        dbms = copy.copy(db)

        query = sqlProjectWorkLogManage.check_sysnum_userin(sys_doc_num, id)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_sysnum_userin : " + query,
        )

        return dbms.queryForObject(query)

    #### 회사가 해당 문서 권한이 있는지 확인한다
    def check_sysnum_companyauth(self, sys_doc_num, co_code):
        dbms = copy.copy(db)

        query = sqlProjectWorkLogManage.check_sysnum_companyin(sys_doc_num, co_code)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_sysnum_companyin : " + query,
        )

        return dbms.queryForObject(query)

    #### 해당문서의 공사코드를 조회한다 ####

    def get_conscode(self, sys_doc_num):
        dbms = copy.copy(db)

        query = sqlProjectWorkLogManage.select_conscode(sys_doc_num)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_conscode : " + query,
        )

        return dbms.queryForObject(query)
