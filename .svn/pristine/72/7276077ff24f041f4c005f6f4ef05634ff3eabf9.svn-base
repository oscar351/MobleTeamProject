import typing
import json
import re
import os
import sys
from abc import ABC, abstractmethod

from allscapeAPIMain import db
from allscapeAPIMain import procName

from common.logManage import logManage
from common import constants
from common import util_time
from projectFloorPlanManage.servProjectFloorPlanManage import servProjectFloorPlanManage
from projectPlanReviewManage.servProjectPlanReviewManage import (
    servProjectPlanReviewManage,
)
from projectDocManage.servProjectDocManage import servProjectDocManage
from common.commUtilService import commUtilService
from common.commonService import commonService
from userManage.servUserManage import servUserManage
from commManage.servCommManage import servCommManage
from companyManage.servCompanyManage import servCompanyManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당

#### 문서 작성관리 서비스 ####
"""
클래스에서 reqDocContent의 기초문서 정보를 입력받아 문서 Content를 완성한 후 get_result를 호출해 결과를 얻는다.
자식클래스에서 각각의 문서에서의 Content를 구현한다
"""


class docContentService(ABC):
    """문서내용 공통 service 추상클래스"""

    servCommMana = servCommManage()
    servUserMana = servUserManage()
    servCompanyMana = servCompanyManage()
    commServ = commonService()
    commUtilServ = commUtilService()
    servProjDocMana = servProjectDocManage()
    servProjFPMana = servProjectFloorPlanManage()
    servProjPRMana = servProjectPlanReviewManage()

    def __init__(
        self, reqDocContent: dict, reqDocInfo: dict, docDefaultInfo=None, req=None
    ):
        """기초정보를 입력받고 문서내용을 작성"""

        self.reqDocInfo = reqDocInfo
        self.reqDocContent = reqDocContent  # 업데이트 대상
        self.docDefaultInfo = docDefaultInfo
        self.req = req
        self._make_content()

    def _read_constr_type_cd(self) -> str:
        """공종코드로 공종명을 가져온다"""

        resCd, _, constrTypeCdData = self.servCommMana.getCodeName(
            self.reqDocContent["constr_type_cd"]
        )
        if resCd == 0 and constrTypeCdData:
            return constrTypeCdData["subcode_name"]
        raise ValueError("해당 공종코드에 해당하는 공종이름이 없습니다")

    def _read_user_info(self, ID: str) -> str:
        """유저 ID로 유저 이름를 가져온다"""

        resCd, _, userInfo = self.servUserMana.getUserInfo(1, ID, None)
        if resCd == 0 and userInfo:
            return userInfo["user_name"]
        raise ValueError("해당 ID에 해당하는 유저가 없습니다")

    def _read_company_info(self, co_code: str) -> str:
        """CO code로 회사 이름을 가져온다"""
        resCd, _, companyInfo = self.servCompanyMana.get_company_by_code(co_code)
        if resCd == 0 and companyInfo:
            return companyInfo["CO_NAME"]
        raise ValueError("해당 코드에 해당하는 회사가 없습니다")

    #### 설계도면 필요 검색조건: cons_code, ver_info, page ####
    def _read_floor_plan_info(self, fpInfo: dict) -> None:
        """설계도면이 존재하는지 확인한다"""

        resCd, _, floorPlanInfo = self.servProjFPMana.getFloorPlan(fpInfo)
        if resCd == 0 and floorPlanInfo:
            return
        raise ValueError("해당 조건에 해당하는 설계도면이 없습니다")

    #### 시공상세도 저장 ####
    def _read_constr_detail_info(self) -> str:
        """시공상세도 첨부파일들을 저장한다"""

        if len(self.reqDocContent["constr_detail_list"]) > 0:
            resCd, msg, resData = self.servProjDocMana.docFileManage(
                self.reqDocInfo["cons_code"],
                self.docDefaultInfo["sysDocNum"],
                self.reqDocInfo["doc_code"],
                self.docDefaultInfo["documentNumber"],
                "constr_detail",
                self.reqDocContent["constr_detail_list"],
                self.req,
            )

            if resCd != 0:
                self.servProjDocMana.removeDocFileManage(
                    self.reqDocInfo["cons_code"], self.docDefaultInfo["sysDocNum"]
                )
                raise ValueError("시공상세도 첨부가 실패했습니다")

            self.reqDocContent["constr_detail_list"] = resData

    #### 설계도면 검토의견 필요 검색조건: cons_code, ver_info ####
    def _read_plan_review_info(self, prInfo: dict) -> list:
        resCd, _, planReviewInfo = self.servProjPRMana.getPlanReviewAll(prInfo)
        if resCd == 0 and planReviewInfo:
            return planReviewInfo
        raise ValueError("해당 조건에 해당하는 설계도면 검토의견이 없습니다")

    #### 문서내용작성 추상메소드 ####
    @abstractmethod
    def _make_content(self) -> tuple:
        """DOC_MANAGE에 저장될 문서 content를 만든다. -> 자식 클래스에서 구현"""

        raise NotImplementedError

    #### 입력받은 기본내용작성 추상메소드 ####
    @abstractmethod
    def _check_content(self) -> None:
        """reqDocContent의 무결성을 검사한다. -> 자식 클래스에서 구현"""

        raise NotImplementedError

    def get_result(self) -> tuple:
        """처리 결과를 반환하는 함수"""

        return self.resCd, self.msg, self.reqDocContent


class ConstrDetailReq(docContentService):
    """시공상세도 검토요청서 내용작성 class"""

    """
    검토요청서 작성시 reqDocContent 필요 내용
    constr_type_cd - 공종
    floor_plan_list -설계도면 목록
    recv_ID - 수신자 ID
    location - 부위
    constr_detail_list - 시공상세도면 목록
    remarks - 특기사항
    charge_ID - 담당자 ID
    engineer_ID - 소방기술자 ID
    
    검토요청서 작성완료시 추가되는 값
    constr_type_name - 공사명
    recv_name - 수신자 이름
    charge_name - 담당자 이름
    engineer_name - 소방기술자 이름
    """

    def _make_content(self) -> None:
        """시공상세도 검토요청서 content생성"""

        #### 기초정보를 이용해 DB검색하여 나머지 값을 알아낸다. ####
        try:
            #### reqDocContent가 적절한지 검사한다 ####
            self._check_content()

            self.reqDocContent[
                "constr_type_name"
            ] = self._read_constr_type_cd()  # 공사이름 검색
            self.reqDocContent["recv_name"] = self._read_user_info(
                self.reqDocContent["recv_ID"]
            )  # 수신자 이름 검색

            #### 설계도면을 검색하여 존재하는지 확인한다 ####
            fp_cond = {"cons_code": self.reqDocInfo["cons_code"]}
            for floorPlan in self.reqDocContent["floor_plan_list"]:
                fp_cond["ver_info"] = floorPlan["ver_info"]
                fp_cond["page"] = floorPlan["page"]
                self._read_floor_plan_info(fp_cond)

            #### 시공상세도면 첨부파일들을 저장한다 ####
            self._read_constr_detail_info()

            self.reqDocContent["charge_name"] = self._read_user_info(
                self.reqDocContent["charge_ID"]
            )  # 시공담당자 이름 검색
            self.reqDocContent["engineer_name"] = self._read_user_info(
                self.reqDocContent["engineer_ID"]
            )  # 소방기술자 이름 검색
            self.resCd, self.msg = constants.REST_RESPONSE_CODE_ZERO, ""

        #### 문서 작성 도중 오류 시 400 error 처리 ####
        except Exception as e:
            self.resCd, self.msg = constants.REST_RESPONSE_CODE_DATAFAIL, str(e)

    def _check_content(self) -> None:
        """reqDocContent의 무결성을 검사하는 함수"""

        if not "constr_type_cd" in self.reqDocContent:
            raise ValueError("reqDocContent에 constr_type_cd가 없습니다")
        if not "recv_ID" in self.reqDocContent:
            raise ValueError("reqDocContent에 recv_ID가 없습니다")
        if not "floor_plan_name" in self.reqDocContent:
            raise ValueError("reqDocContent에 floor_plan_name이 없습니다")
        if not "floor_plan_list" in self.reqDocContent:
            raise ValueError("reqDocContent에 floor_plan_list가 없습니다")
        if not "location" in self.reqDocContent:
            raise ValueError("reqDocContent에 location이 없습니다")
        if not "constr_detail_name" in self.reqDocContent:
            raise ValueError("reqDocContent에 constr_detail_name이 없습니다")
        if not "constr_detail_list" in self.reqDocContent:
            raise ValueError("reqDocContent에 constr_detail_list가 없습니다")
        if not "remarks" in self.reqDocContent:
            raise ValueError("reqDocContent에 remarks가 없습니다")
        if not "charge_ID" in self.reqDocContent:
            raise ValueError("reqDocContent에 charge_ID가 없습니다")
        if not "engineer_ID" in self.reqDocContent:
            raise ValueError("reqDocContent에 engineer_ID가 없습니다")
        return


class ConstrDetailNtc(docContentService):
    """시공상세도 검토통보서 내용작성 class"""

    """
    검토통지서 필요 내용
    ntc_recv_ID - 수신자 ID
    review - 검토의견
    jugement - 판정
    ntc_remarks - 특기사항
    respon_ID - 책임감리원 ID
    assist_ID - 보조감리원 ID
    """

    def _make_content(self) -> None:
        """시공상세도 검토통보서 content생성"""

        try:
            #### reqDocContent가 적절한지 검사한다 ####
            self._check_content()

            self.reqDocContent["recv_name"] = self._read_user_info(
                self.reqDocContent["recv_ID"]
            )  # 수신자 이름 검색
            self.reqDocContent["respon_name"] = self._read_user_info(
                self.reqDocContent["respon_ID"]
            )  # 책임감리원 이름 검색
            self.reqDocContent["assist_name"] = self._read_user_info(
                self.reqDocContent["assist_ID"]
            )  # 보조감리원 이름 검색
            self.resCd, self.msg = constants.REST_RESPONSE_CODE_ZERO, ""

        #### 문서 작성 도중 오류 시 400 error 처리 ####
        except Exception as e:
            self.resCd, self.msg = constants.REST_RESPONSE_CODE_DATAFAIL, str(e)

    def _check_content(self) -> None:
        """reqDocContent의 무결성을 검사하는 함수"""

        if not "recv_ID" in self.reqDocContent:
            raise ValueError("reqDocContent에 recv_ID가 없습니다")
        if not "review" in self.reqDocContent:
            raise ValueError("reqDocContent에 review가 없습니다")
        if not "judgment" in self.reqDocContent:
            raise ValueError("reqDocContent에 judgment가 없습니다")
        if not "remarks" in self.reqDocContent:
            raise ValueError("reqDocContent에 remarks가 없습니다")
        if not "respon_ID" in self.reqDocContent:
            raise ValueError("reqDocContent에 respon_ID가 없습니다")
        if not "assist_ID" in self.reqDocContent:
            raise ValueError("reqDocContent에 assist_ID가 없습니다")
        return


class PlanReviewRPT(docContentService):
    """설계검토 보고서 내용작성 class"""

    """
    설계검토 보고서 필요 내용
    ver_info: 설계도면 버전
    """

    def _make_content(self) -> None:
        """설계검토 보고서 content생성"""

        try:
            #### reqDocContent가 적절한지 검사한다 ####
            self._check_content()

            #### 설계도면 검토의견을 검색하여 리스트를 가져온다 ####
            pr_cond = {
                "cons_code": self.reqDocInfo["cons_code"],
                "ver_info": self.reqDocContent["ver_info"],
            }
            plan_reviews = self._read_plan_review_info(pr_cond)
            self.reqDocContent["plan_reviews"] = []
            for plan_review in plan_reviews:
                self.reqDocContent["plan_reviews"].append(
                    {
                        "catrgory": plan_review["category"],
                        "page": plan_review["page"],
                        "location": plan_review["location"],
                        "number": plan_review["number"],
                        "problem": plan_review["problem"],
                        "reason": plan_review["reason"],
                        "supv_opn": plan_review["supv_opn"],
                    }
                )
            self.resCd, self.msg = constants.REST_RESPONSE_CODE_ZERO, ""

        #### 문서 작성 도중 오류 시 400 error 처리 ####
        except Exception as e:
            self.resCd, self.msg = constants.REST_RESPONSE_CODE_DATAFAIL, str(e)

    def _check_content(self) -> None:
        """reqDocContent의 무결성을 검사하는 함수"""

        if not "ver_info" in self.reqDocContent:
            raise ValueError("reqDocContent에 ver_info가 없습니다")

        return


class OnSiteSituationRPT(docContentService):
    """현장실정 보고서 내용작성 class"""

    """
    현장실정 보고서 필요 내용
    change_count: 변경회수
    change_list: 변경 내용
    """

    def _make_content(self) -> None:
        """현장실정 보고서 content생성"""

        try:
            #### reqDocContent가 적절한지 검사한다 ####
            self._check_content()

            self.reqDocContent["constr_type_name"] = self._read_constr_type_cd()
            self.reqDocContent["increase_cost"] = float(
                self.reqDocContent["change_cost"]
            ) - float(self.reqDocContent["original_cost"])
            self.resCd, self.msg = constants.REST_RESPONSE_CODE_ZERO, ""

        #### 문서 작성 도중 오류 시 400 error 처리 ####
        except Exception as e:
            self.resCd, self.msg = constants.REST_RESPONSE_CODE_DATAFAIL, str(e)

    def _check_content(self) -> None:
        """reqDocContent의 무결성을 검사하는 함수"""

        if not "change_count" in self.reqDocContent:
            raise ValueError("reqDocContent에 change_count가 없습니다")
        if not "change_list" in self.reqDocContent:
            raise ValueError("reqDocContent에 change_list가 없습니다")
        if not "constr_type_cd" in self.reqDocContent["change_list"]:
            raise ValueError('reqDocContent["change_list"]에 constr_type_cd가 없습니다')
        if not "start_date" in self.reqDocContent["change_list"]:
            raise ValueError('reqDocContent["change_list"]에 start_date가 없습니다')
        if not "material" in self.reqDocContent["change_list"]:
            raise ValueError('reqDocContent["change_list"]에 material가 없습니다')
        if not "quantity_unit" in self.reqDocContent["change_list"]:
            raise ValueError('reqDocContent["change_list"]에 quantity_unit가 없습니다')
        if not "original_quantity" in self.reqDocContent["change_list"]:
            raise ValueError('reqDocContent["change_list"]에 original_quantity가 없습니다')
        if not "change_quantity" in self.reqDocContent["change_list"]:
            raise ValueError('reqDocContent["change_list"]에 change_quantity가 없습니다')
        if not "original_cost" in self.reqDocContent["change_list"]:
            raise ValueError('reqDocContent["change_list"]에 original_cost가 없습니다')
        if not "change_cost" in self.reqDocContent["change_list"]:
            raise ValueError('reqDocContent["change_list"]에 change_cost가 없습니다')
        if not "original_detail_list" in self.reqDocContent["change_list"]:
            raise ValueError('reqDocContent["change_list"]에 original_detail_list가 없습니다')
        if not "change_detail_list" in self.reqDocContent["change_list"]:
            raise ValueError('reqDocContent["change_list"]에 start_date가 없습니다')
        if not "reason" in self.reqDocContent["change_list"]:
            raise ValueError('reqDocContent["change_list"]에 reason가 없습니다')
        if not "note" in self.reqDocContent["change_list"]:
            raise ValueError('reqDocContent["change_list"]에 note가 없습니다')
        return


class ConstrChangeReview(docContentService):
    """설계의견 검토의견서 내용작성 class"""

    """
    설계의견 검토의견서 필요 내용
    company_code: 감리회사 코드
    supv_ID_list: 감리원 ID 리스트
    review_list: 검토의견 리스트
    opinion: 종합의견
    """

    def _make_content(self) -> None:
        """설계의견 검토의견서 content생성"""

        try:
            #### reqDocContent가 적절한지 검사한다 ####
            self._check_content()

            self.reqDocContent["constr_type_name"] = self._read_constr_type_cd()
            self.reqDocContent["company_name"] = self._read_company_info(
                self.reqDocContent["company_code"]
            )
            self.resCd, self.msg = constants.REST_RESPONSE_CODE_ZERO, ""

        #### 문서 작성 도중 오류 시 400 error 처리 ####
        except Exception as e:
            self.resCd, self.msg = constants.REST_RESPONSE_CODE_DATAFAIL, str(e)

    def _check_content(self) -> None:
        """reqDocContent의 무결성을 검사하는 함수"""

        if not "company_code" in self.reqDocContent:
            raise ValueError("reqDocContent에 company_code가 없습니다")
        if not "supv_ID_list" in self.reqDocContent:
            raise ValueError("reqDocContent에 supv_ID_list가 없습니다")
        if not "review_list" in self.reqDocContent:
            raise ValueError("reqDocContent에 review_list가 없습니다")
        if not "opinion" in self.reqDocContent:
            raise ValueError("reqDocContent에 opinion가 없습니다")
        if not "category" in self.reqDocContent["review_list"]:
            raise ValueError('reqDocContent["review_list"]에 category가 없습니다')
        if not "before" in self.reqDocContent["review_list"]:
            raise ValueError('reqDocContent["review_list"]에 before가 없습니다')
        if not "after" in self.reqDocContent["review_list"]:
            raise ValueError('reqDocContent["review_list"]에 after가 없습니다')
        if not "reason" in self.reqDocContent["review_list"]:
            raise ValueError('reqDocContent["review_list"]에 reason가 없습니다')
        if not "judgement" in self.reqDocContent["review_list"]:
            raise ValueError('reqDocContent["review_list"]에 judgement가 없습니다')
        if not "note" in self.reqDocContent["review_list"]:
            raise ValueError('reqDocContent["review_list"]에 note가 없습니다')
        return


class ChangeManagementLedger(docContentService):
    """설계변경 관리대장 내용작성 class"""

    """
    설계변경 관리대장 필요 내용
    start_date: 시작기간
    end_date: 종료기간
    title: 제목
    change_list: 변경목록
    """

    def _make_content(self) -> None:
        """설계변경 관리대장 content생성"""

        try:
            #### reqDocContent가 적절한지 검사한다 ####
            self._check_content()

            self.resCd, self.msg = constants.REST_RESPONSE_CODE_ZERO, ""

        #### 문서 작성 도중 오류 시 400 error 처리 ####
        except Exception as e:
            self.resCd, self.msg = constants.REST_RESPONSE_CODE_DATAFAIL, str(e)

    def _check_content(self) -> None:
        """reqDocContent의 무결성을 검사하는 함수"""

        if not "company_code" in self.reqDocContent:
            raise ValueError("reqDocContent에 company_code가 없습니다")
        if not "supv_ID_list" in self.reqDocContent:
            raise ValueError("reqDocContent에 supv_ID_list가 없습니다")
        if not "review_list" in self.reqDocContent:
            raise ValueError("reqDocContent에 review_list가 없습니다")
        if not "opinion" in self.reqDocContent:
            raise ValueError("reqDocContent에 opinion가 없습니다")
        if not "category" in self.reqDocContent["review_list"]:
            raise ValueError('reqDocContent["review_list"]에 category가 없습니다')
        if not "before" in self.reqDocContent["review_list"]:
            raise ValueError('reqDocContent["review_list"]에 before가 없습니다')
        if not "after" in self.reqDocContent["review_list"]:
            raise ValueError('reqDocContent["review_list"]에 after가 없습니다')
        if not "reason" in self.reqDocContent["review_list"]:
            raise ValueError('reqDocContent["review_list"]에 reason가 없습니다')
        if not "judgement" in self.reqDocContent["review_list"]:
            raise ValueError('reqDocContent["review_list"]에 judgement가 없습니다')
        if not "note" in self.reqDocContent["review_list"]:
            raise ValueError('reqDocContent["review_list"]에 note가 없습니다')
        return


"""
조현우 새 문서작성 기술 테스트 클래스
기존 docmanage에서 이루어졌던 방식을 획기적으로 개선해본다
이 클래스에서는 문서 작성에 필요한 모든 정보를 저장하고, 
필요한 기능들이 모두 메소드로써 구현된다.
클래스 인스턴스 하나당 현재 작성중인 문서에 대한 정보를 기록한다.
"""
#### 문서 작성 수정 서비스 ####
"""
클래스에서 문서 Content를 만든 후 params["reqDocContent"]를 업데이트 한다
자식클래스에서 각각의 문서에서의 Content handling을 구현한다
"""


class docContentServiceNew(ABC):
    """문서내용 공통 service 추상클래스"""

    servCommMana = servCommManage()
    servUserMana = servUserManage()
    commServ = commonService()
    commUtilServ = commUtilService()
    servProjDocMana = servProjectDocManage()

    def __init__(self, params: dict, docDefaultInfo: dict, userInfo: dict):
        """기초정보를 입력받고 문서내용을 작성"""

        self.params = params  # 업데이트 대상
        self._check_content()

        self.resCd, self.msg, self.params = self._make_content()

    def _read_constr_type_cd(self) -> str:
        """공종 정보를 가져온다"""

        resCd, _, constrTypeCdData = self.servCommMana.getCodeName(
            self.params["reqDocContent"]["constr_type_cd"]
        )
        if resCd == 0 and constrTypeCdData:
            return constrTypeCdData["subcode_name"]
        raise ValueError("해당 공종코드에 해당하는 공종이름이 없습니다")

    def _read_detail_constr_type_cd(self) -> str:
        """세부 공종 정보를 가져온다"""

        resCd, _, detailConstrTypeCdData = self.servCommMana.getCodeName(
            self.params["reqDocContent"]["detail_constr_type_cd"]
        )
        if resCd == 0 and detailConstrTypeCdData:
            return detailConstrTypeCdData["subcode_name"]
        raise ValueError("해당 세부공종코드에 해당하는 세부공종이름이 없습니다")

    def _read_user_info(self, ID: str) -> str:
        """유저 ID로 유저 정보를 가져온다"""

        resCd, _, userInfo = self.servUserMana.getUserInfo(1, ID, None)
        if resCd == 0 and userInfo:
            return userInfo["user_name"]
        raise ValueError("해당 ID에 해당하는 유저가 없습니다")

    @abstractmethod
    def _make_content(self) -> tuple:
        """DOC_MANAGE에 저장될 문서 content를 만든다. -> 자식 클래스에서 구현"""

        raise NotImplementedError

    @abstractmethod
    def _check_content(self) -> None:
        """content의 타입을 체크한다. -> 자식 클래스에서 구현"""

        raise NotImplementedError

    def get_result(self) -> tuple:
        """처리 결과를 반환하는 함수"""
        return self.resCd, self.msg, self.params
