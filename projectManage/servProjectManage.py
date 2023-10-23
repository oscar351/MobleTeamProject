# _*_coding: utf-8 -*-
import os
import sys
import copy

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.logManage import logManage

from projectManage.sqlProjectManage import sqlProjectManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectManage:

    # 프로젝트 문서 설정 정보를 조회 한다.
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- coCode | String | 회사 코드
    def getProjDocNumCfg(self, consCode, coCode):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        # 쿼리 생성
        query = sProjMana.sGetProjDocNumCfg(consCode, coCode)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetProjDocNumCfg Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 프로젝트 문서 설정 정보를 업데이트 한다.
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- coCode | String | 회사 코드
    # 	- docInfo | Object | 업데이트 문서 정보
    def updateProjDocNumCfg(self, consCode, coCode, docInfo):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        # 쿼리 생성
        query = sProjMana.sUpdateProjDocNumCfg(consCode, coCode, docInfo)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sUpdateProjDocNumCfg Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 소방시설공사 정보를 관리 한다.
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- coCode | String | 회사 코드
    # 	- ffPlan | Object | 소방시설공사 정보
    def cfgFFPlan(self, consCode, coCode, ffPlan):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        if ffPlan["type"] == "A":
            query = sProjMana.iPutFFPlan(consCode, coCode, ffPlan)
        elif ffPlan["type"] == "C":
            query = sProjMana.uUpdateFFPlan(consCode, coCode, ffPlan)
        elif ffPlan["type"] == "D":
            # query = sProjMana.dDelFFPlanCheckList(consCode, coCode, ffPlan) # 체크리스트 삭제
            # resCd, msg, resData = dbms.execute(query)
            # if(resCd != 0):
            # 	return resCd, msg, resData
            query = sProjMana.dDelFFPlan(consCode, coCode, ffPlan)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "cfgFFPlan Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 소방시설공사 정보를 조회 한다.
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- loginUserInfo | Object | 사용자 정보
    def getFFPlan(self, consCode, userInfo):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.sGetFFPlan(consCode, userInfo)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "getFFPlan Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 공종에 따른 세부 공종 리스트를 조회 한다.
    # Parameter
    # 	- constrCode | String | 공사 종류 코드
    def getDetailConstrList(self, constrCode):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.sGetDetailConstrList(constrCode)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "getDetailConstrList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 세부공종에 따른 체크 리스트를 조회 한다.
    # Parameter
    # 	- constrCode | String | 공사 종류 코드
    # 	- detailConstrCode | String | 세부공사 종류 코드
    def getCheckList(self, constrCode, detailConstrCode):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.sGetCheckList(constrCode, detailConstrCode)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "getCheckList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 프로젝트 공종의 체크 리스트를 삭제 한다.
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- userInfo | Object | 사용자 정보
    def delProjDetectionChkList(self, consCode, userInfo, constrTypeCode):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.dDelProjDetectionChkList(
            consCode, userInfo["co_code"], constrTypeCode
        )

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelProjDetectionChkList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 프로젝트의 공종별/회사별/세부공종 별 체크 리스트를 추가 한다.
    # Parameter
    # 	- coCode | String | 회사 코드
    # 	- checkListInfo | Object | 체크 리스트 정보
    # 	    {
    # 			"cons_code" : "P00000000063",
    # 			"constr_code" : "FE000000",
    # 			"detailConstrList" : [{
    # 				"detail_constr_code" : "DF000013",
    # 				"chk_msg_list" : [{
    # 					"chk_msg" : "테스트입니다.",
    # 					"insp_crit_code" : "IC000019"
    # 				}, {
    # 					"chk_msg" : "테스트일까?",
    # 					"insp_crit_code" : "IC000019"
    # 				}]
    # 			},{
    # 				"detail_constr_code" : "DF000009",
    # 				"chk_msg_list" : [{
    # 					"chk_msg" : "000은 0000과 연결이 되어 있는가?",
    # 					"insp_crit_code" : "IC000019"
    # 				}, {
    # 					"chk_msg" : "000을 체크 하였습니까?",
    # 					"insp_crit_code" : ""
    # 				}]
    # 			}]
    # 		}
    def putProjDetectionChkList(self, coCode, checkListInfo):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        detailConstrList = checkListInfo["detailConstrList"]

        for detailConstr in detailConstrList:
            for chkmsg in detailConstr["chk_msg_list"]:
                query = sProjMana.iPutProjDetectionChkList(
                    checkListInfo["cons_code"],
                    coCode,
                    checkListInfo["constr_code"],
                    detailConstr["detail_constr_code"],
                    chkmsg["chk_msg"],
                    chkmsg["insp_crit_code"],
                )

                # 쿼리 생성
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "putProjDetectionChkList Query : " + query,
                )

                # 쿼리 실행
                resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 프로젝트별-획사별-공종별 체크 리스트를 추가 가져온다.
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    # 	- coCode | String | 회사 코드
    # 	- constrCode | String | 공종 코드
    def getProjDetectionChkList(self, consCode, coCode, constrCode):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.sGetProjDetectionChkList(consCode, coCode, constrCode)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetProjDetectionChkList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 프로젝트 참여 인력 현황을 조회 한다.
    # Parameter
    # 	- coCode | String | 회사 코드
    def getAreaProjPartManpStatus(self, coCode):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        constrCnt_p = 0
        supCnt_p = 0
        constrCnt_c = 0
        supCnt_c = 0

        query = sProjMana.sGetAreaProjPartManpStatusP(1, coCode)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetAreaProjPartManpStatusP Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)
        constrCnt_p = resData["cnt"]

        query = sProjMana.sGetAreaProjPartManpStatusP(2, coCode)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetAreaProjPartManpStatusP Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)
        supCnt_p = resData["cnt"]

        query = sProjMana.sGetAreaProjPartManpStatusC(1, coCode)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetAreaProjPartManpStatusC Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)
        constrCnt_c = resData["cnt"]

        query = sProjMana.sGetAreaProjPartManpStatusC(2, coCode)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetAreaProjPartManpStatusC Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)
        supCnt_c = resData["cnt"]

        resData = {
            "constrCnt_p": constrCnt_p,
            "constrCnt_c": constrCnt_c,
            "supCnt_p": supCnt_p,
            "supCnt_c": supCnt_c,
        }

        return resCd, msg, resData

    # 공사 기본 정보를 저장 한다.
    # Parameter
    # 	- dataInfo | Object | 공사 기본 정보
    # 	{
    # 	  "cons_code": "P00000000063",
    # 	  "location": "대전이 유성구 전민동 엑스포아파트 5단지",
    # 	  "cons_type": "아파트",
    # 	  "purpose": "PP000000",
    # 	  "building_name": "엑스포아파트 5단지",
    # 	  "location_contact": "042-1234-1234",
    # 	  "business_outline": "주거용 엑스포 아파트",
    # 	  "go_price": "100000000",
    # 	  "design_price": "20000000",
    # 	  "structure": "철근 콘크리트벽식구조",
    # 	  "ground": "35",
    # 	  "underground": "2",
    # 	  "main_building": "5",
    # 	  "sub_building": "1",
    # 	  "households": "1306",
    # 	  "site_area": "1927218311",
    # 	  "building_area": "3161826371",
    # 	  "total_area": "2692766508",
    # 	  "floor_area": "3618211",
    # 	  "add_info": ""
    # 	}
    def updateProjDefaultInfo(self, consCode, dataInfo, typeFlag):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "데이터구조 : " + str(dataInfo),
        )
        query = sProjMana.uUpdateProjDefaultInfo(consCode, dataInfo, typeFlag)

        if query == "":
            return -1, "수정된 내용이 없습니다.", None

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uUpdateProjDefaultInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 공사 기본 정보를 조회 한다.
    # Parameter
    # 	- consCode | String | 프로젝트 코드
    def getProjDefaultInfo(self, consCode):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.sGetProjDefaultInfo(consCode)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetProjDefaultInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 감리 기본 정보를 저장 한다.
    #
    # Parameter
    # 	- dataInfo | Object | 감리 기본 정보
    # 	{
    # 		"company_type" : "0",
    # 		"cons_code" : "P00000000063",
    # 		"co_code" : "CO000007",
    # 		"reside_class_code" : "SD010000",
    # 		"superv_contract_date" : "20220922000000",
    # 		"superv_price" : "300000000"
    # 	}
    def updateSupvDefaultInfo(self, consCode, dataInfo, typeFlag):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.uUpdateSupvDefaultInfo(consCode, dataInfo, typeFlag)

        if query == "":
            return -1, "수정된 내용이 없습니다.", None

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uUpdateSupvDefaultInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 시공 기본 정보를 저장 한다.
    #
    # Parameter
    # 	- dataInfo | Object | 시공 기본 정보
    # 	{
    # 		"company_type" : "1",
    # 		"cons_code" : "P00000000063",
    # 		"co_code" : "CO000007",
    # 		"contract_date" : "20220922000000",
    # 		"completion_date" : "20220922000000",
    # 		"start_date" : "20220922000000",
    # 		"subcontract_price" : "300000000",
    # 		"biddropping" : "49",
    # 		"bidway" : "경쟁",
    # 		"proc_details_name" : "공정상세내역서.csv",
    # 	}
    def putContDefaultInfo(self, dataInfo):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.iPutContDefaultInfo(dataInfo)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutContDefaultInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 공정상세 내역서 기준 정보를 저장 한다.
    def putBaseOnProcDetails(
        self, consCode, coCode, constrTypeCode, materialNum, unitCode, dataInfo, regDate
    ):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.iPutBaseOnProcDetails(
            consCode, coCode, constrTypeCode, materialNum, unitCode, dataInfo, regDate
        )

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutBaseOnProcDetails Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 공정상세 내역서 직종별 정보를 저장 한다.
    def putBaseOnOccupationDetails(
        self, consCode, coCode, constrTypeCode, occCode, unitCode, dataInfo, regDate
    ):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.iPutBaseOnOccupationDetails(
            consCode, coCode, constrTypeCode, occCode, unitCode, dataInfo, regDate
        )

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutBaseOnOccupationDetails Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 시공사 기본 정보를 수정 한다..
    def modifyContDefaultInfo(self, dataInfo):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.uModifyContDefaultInfo(dataInfo)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uModifyContDefaultInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 공정상세 내역서 기준 정보를 삭제 한다.
    def delBaseOnProcDetails(self, consCode, coCode):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.dDelBaseOnProcDetails(consCode, coCode)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelBaseOnProcDetails Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 감리원 기본 정보를 조회 한다.
    def getSupvDefaultInfo(self, consCode):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.sGetSupvDefaultInfo(consCode)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetSupvDefaultInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 시공사 기본 정보를 조회 한다.
    def getContDefaultInfo(self, consCode, coCode):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.sGetContDefaultInfo(consCode, coCode)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetContDefaultInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 프로젝트 리스트를 조회 한다.
    # def getProjectList(self, userId, projectStatus):
    def getProjectList(self, userInfo, projectStatus):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.sGetProjectList(userInfo, projectStatus)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetProjectList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 작업 일지 작성 기준 정보를 저장 한다.
    def putWorkLogWriteStandard(self, consCode, coCode, writeStandardCode):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.iPutWorkLogWriteStandard(consCode, coCode, writeStandardCode)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutWorkLogWriteStandard Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 작업 일지 작성 기준 정보를 조회 한다.
    def getWorkLogWriSta(self, consCode, coCode):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.sGetWorkLogWriSta(consCode, coCode)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetWorkLogWriSta Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 작업 일지 작성 기준 정보를 수정 한다.
    def modifyWorkLogWriSta(self, consCode, coCode, workLogWriSatCd):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.uModifyWorkLogWriSta(consCode, coCode, workLogWriSatCd)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uModifyWorkLogWriSta Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 프로젝트 이력 리스트 조회
    def getProjectHistoryList(self, userInfo):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.sGetProjectHistoryList(userInfo)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetProjectHistoryList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 프로젝트를 생성 한다.
    def putProject(self, projCd, projNm, supervCoCd):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.iPutProject(projCd, projNm, supervCoCd)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutProject Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 프로젝트를 삭제 한다.
    def delProject(self, projCd):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.dDelProject(projCd)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelProject Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 조현우 수정 전체적으로 인력 리스트를 수정한다
    def modifyJoinWorkforce(self, cons_code, addUser, putUser, delUser):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        queryList = list()
        for user in addUser:
            query = sProjMana.insert_join_workforce(
                cons_code,
                user["id"],
                user["authority_code"],
                user["co_code"],
                user["start_date"],
                user["end_date"],
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "insert_join_workforce Query : " + query,
            )
            queryList.append(query)
        for user in putUser:
            query = sProjMana.update_join_workforce(
                cons_code,
                user["id"],
                user["date"],
                user["start_date"],
                user["end_date"],
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "update_join_workforce Query : " + query,
            )
            queryList.append(query)
        for user in delUser:
            query = sProjMana.delete_join_workforce(cons_code, user["id"], user["date"])
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "delete_join_workforce Query : " + query,
            )
            queryList.append(query)

        return dbms.executeIter(queryList)

    # 인력 리스트를 저장 한다.
    def putJoinWorkforce(self, projCd, supervisorsList):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        # 공사기간으로 인력참여기간 초기화
        query = sProjMana.select_project_date(projCd)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_project_date Query : " + query,
        )
        resCd, msg, dateData = dbms.queryForObject(query)
        if resCd == 0:
            query = sProjMana.iPutJoinWorkforce(projCd, dateData["cons_start_date"], dateData["cons_end_date"], supervisorsList)

            # 쿼리 생성
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "iPutJoinWorkforce Query : " + query,
            )

            # 쿼리 실행
            resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 인력 리스트를 삭제하거나 종료일을 업데이트 한다.
    def delJoinWorkforce(self, projCd, userList):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "인력 삭제 시작",
        )
        delete_user_list = list()
        expel_user_list = list()
        for user in userList:
            if user["date"] == "":
                delete_user_list.append(user)
            else:
                expel_user_list.append(user)

        #### 무결성을 보장하기 위해 여러번 execute 후 한번의 commit ####
        queryList = list()

        #### 인력DB에서 삭제하는 쿼리 ####
        if delete_user_list:
            query = sProjMana.dDelJoinWorkforce(projCd, delete_user_list)
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "dDelJoinWorkforce Query : " + query,
            )
            queryList.append(query)

        #### 인력DB에서 종료일 업데이트하는 쿼리 ####
        if expel_user_list:
            query = sProjMana.expelJoinWorkforce(projCd, expel_user_list)
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "expelJoinWorkforce Query : " + query,
            )
            queryList.append(query)

        return dbms.executeIter(queryList)

        """
        query = sProjMana.dDelJoinWorkforce(projCd, userList)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "expelJoinWorkforce Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData
        """

    # 문서를 저장 한다.
    def putDocNumManage(self, projCd, coCd, docList):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.iPutDocNumManage(projCd, coCd, docList)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutDocNumManage Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 문서 정보를 삭제 한다.
    def delDocNumManage(self, projCd, coCode):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.dDelDocNumManage(projCd, coCode)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelNumManage Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 프로젝트 참여 인력을 가져온다.
    def getJoinWorkforceInfo(self, projCd, jobList):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.sGetJoinWorkforceInfo(projCd, jobList)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetJoinWorkforceInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 프로젝트 참여 인력 리스트를 업데이트 한다.
    def updateJoinWorkforce(self, projCd, supervisorsList):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        resCd, msg, resData = self.delJoinWorkforce(projCd, supervisorsList)
        if resCd != 0:
            return resCd, msg, None

        resCd, msg, resData = self.putJoinWorkforce(projCd, supervisorsList)
        if resCd != 0:
            return resCd, msg, None

        return resCd, msg, resData

    # 프로젝트를 중지 이력을 저장 한다.
    def putProjStopHis(self, dataInfo):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.iPutProjStopHis(dataInfo)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutProjStopHis Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 프로젝트를 중지 이력을 삭제 한다.
    def delProjStopHis(self, dataInfo):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.dDelProjStopHis(dataInfo)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelProjStopHis Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 프로젝트 정보를 업데이트 한다.
    def updateProjInfo(self, consCode, updateInfoList):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.uUpdateProjInfo(consCode, updateInfoList)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uUpdateProjInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 프로젝트 중지 이력의 재시작 날짜를 업데이트 한다.
    def updateProjRestartHis(self, dataInfo):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.uUpdateProjRestartHis(dataInfo)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uUpdateProjInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 조현우 추가 - 프로젝트 상태를 조회한다
    def getProjectStatus(self, cons_code):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.select_project_status(cons_code)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_project_status Query : " + query,
        )

        # 쿼리 실행
        return dbms.queryForObject(query)

    # 조현우 추가 - 프로젝트 상태를 조회한다
    def getProjectStatusBySysdocnum(self, sys_doc_num):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.select_project_status_by_sysdocnum(sys_doc_num)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_project_status_by_sysdocnum Query : " + query,
        )

        # 쿼리 실행
        return dbms.queryForObject(query)

    # 조현우 추가 - 참여인력 참여 시작기간 변경
    def putJoinWorkforceStart(self, cons_code, id, start_date):
        """참여인력 참여 시작기간 변경"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.update_join_workforce_start_date(cons_code, id, start_date)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_join_workforce_start_date Query : " + query,
        )

        # 쿼리 실행
        return dbms.execute(query)

    # 조현우 추가 - 참여인력 참여 종료기간 변경
    def putJoinWorkforceEnd(self, cons_code, id, end_date):
        """참여인력 참여 종료기간 변경"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.update_join_workforce_end_date(cons_code, id, end_date)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_join_workforce_end_date Query : " + query,
        )

        # 쿼리 실행
        return dbms.execute(query)

    def deleteJoinWorkforce(self, co_code, id):
        """참여인력 삭제처리"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sProjMana = sqlProjectManage()

        query = sProjMana.removeJoinWorkforce(co_code, id)

        # 쿼리 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "removeJoinWorkforce Query : " + query,
        )

        # 쿼리 실행
        return dbms.execute(query)