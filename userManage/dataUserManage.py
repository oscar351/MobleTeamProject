# _*_coding: utf-8 -*-

# 사용자 데이터 관리 Class
# 작성 날짜 : 2022. 7. 29
# 작성자 : 황희정
# 기능
# 	1. 2022. 07. 29 | 로그인 결과 모델을 Return 한다.
# 	2. 2022. 07. 29 | 로그인 결과 데이터를 Object로 생성하여 Return 한다.
# 변경 이력
# 	1. 2022. 07. 29 | 황희정 | 최조 작성
# 	2. 2022. 08. 03 | 황희정 | 수정 | makeUserInfoResultModel, makeUserInfoResult 컬럼 수정

import uuid

# 사용자 데이터 관리 Class
class dataUserManage:

    # 1. 로그인 결과 모델을 Return 한다.
    def getLoginResultModel(self):
        return {"token": "", "status": ""}  # 1.token  # 2.사용자 상태

    # 2. 로그인 결과 데이터를 Object로 생성하여 Return 한다.
    def makeLoginResult(self, state):
        return {"token": str(uuid.uuid4()), "state": state}  # 1.token  # 2.사용자 상태

    def makeUserInfoResultModel(self):
        return {
            # u'user_regisnum'				: '',	# 1.주민등록번호
            "id": "",  # 2.아이디
            "authority_code": "",  # 3.권한코드(업무구분)
            "authority_name": "",  # 권한명
            "password": "",  # 4.패스워드
            "user_name": "",  # 5.이름
            "user_position": "",  # 6.직위
            "user_contact": "",  # 7.사용자 연락처
            "user_email": "",  # 8.사용자 이메일
            # 	u'web_token'					: '',	# 16.web 토큰
            "user_state": "",  # 17.사용자 상태
            "user_state_name": "",  # 사용자 상태 명
            # 	u'app_token'					: '',	# 18.app 토큰
            # 	u'use_type'						: '',	# 19.사용여부
            "user_type": "",  # 20.사용자 구분
            # 	u'user_type_name'				: '',	# 사용자 구분 명
            # 	u'employ_status'				: '',	# 21.재직여부
            # 	u'employ_status_name'			: '',	# 재직여부 명
            "join_date": "",  # 22.가입날짜
            "appro_date": "",  # 23.가입승인날짜
            "co_code": "",  # 회사 코드
            "co_name": "",  # 회사 명
            # 	u'field_rating'					: [],	# 24.분야등급
            # 	u'co_license_path'				: '',	# 25.사업자등록증 경로
            # 	u'co_license_original_name'		: '',	# 26.사업자등록증 원본 파일명
            # 	u'co_license_change_name'		: '',	# 27.사업자등록증 변경 파일명
            # 	u'bs_license_path'				: '',	# 28.공사업 등록수첩 경로
            # 	u'bs_license_original_name'		: '',	# 29.공사업 등록수첨 원본 파일명
            # 	u'bs_license_change_name'		: '',	# 30.공사업 등록수첨 변경 파일명
            # 	u'user_license_path'			: '',	# 31.등급수첩 경로
            # 	u'user_license_original_name'	: '',	# 32.등급수첩 원본 파일명
            # 	u'user_license_change_name'		: '',	# 33.등급수첩 변경 파일명
            # 	u'sign_path'					: '',	# 34.싸인 경로
            # 	u'sign_original_name'			: '',	# 35.싸인 원본 파일명
            # 	u'sign_change_name'				: ''	# 36.싸인 변경 파일명
        }

    def makeUserInfoResult(self, userInfo):
        return {
            # u'user_regisnum'				: userInfo['user_regisnum'],				# 1.주민등록번호
            "id": userInfo["id"],  # 2.아이디
            "authority_code": userInfo["authority_code"],  # 3.권한코드(업무구분)
            "authority_name": userInfo["authority_name"],  # 3.권한명(업무구분)
            "password": userInfo["password"],  # 4.패스워드
            "user_name": userInfo["user_name"],  # 5.이름
            "user_position": userInfo["user_position"],  # 6.직위
            "user_contact": userInfo["user_contact"],  # 7.사용자 연락처
            "user_email": userInfo["user_email"],  # 8.사용자 이메일
            "co_ceo": userInfo["co_ceo"],  # 10.회사 대표자
            "co_type": userInfo["co_type"],  # 11.업종
            "co_address": userInfo["co_address"],  # 12.회사 주소
            "co_contact": userInfo["co_contact"],  # 13.회사연락처
            "co_regisnum": userInfo["co_regisnum"],  # 14.사업자등록번호
            # 			u'regisnum'						: userInfo['regisnum'],						# 15.공사업등록번호
            # 			u'web_token'					: userInfo['web_token'],					# 16.web 토큰
            "user_state": userInfo["user_state"],  # 17.사용자 상태
            "user_state_name": userInfo["user_state_name"],  # 17.사용자 상태 명
            # 			u'app_token'					: userInfo['app_token'],					# 18.app 토큰
            "use_type": userInfo["use_type"],  # 19.사용여부
            # 			u'user_type'					: userInfo['user_type'],					# 20.사용자 구분
            # 			u'user_type_name'				: userInfo['user_type_name'],				# 20.사용자 구분 명
            # 			u'employ_status'				: userInfo['employ_status'],				# 21.재직여부
            # 			u'employ_status_name'			: userInfo['employ_status_name'],			# 21.재직여부 명
            "join_date": userInfo["join_date"],  # 22.가입날짜
            "appro_date": userInfo["appro_date"],  # 23.가입승인날짜
            "co_code": userInfo["co_code"],  # 회사 코드
            "co_name": userInfo["co_name"],  # 9.회사명
            # 			u'field_rating'					: [],										# 24.분야등급
            # 			u'co_license_path'				: userInfo['co_license_path'],				# 25.사업자등록증 경로
            # 			u'co_license_original_name'		: userInfo['co_license_original_name'],		# 26.사업자등록증 원본 파일명
            # 			u'co_license_change_name'		: userInfo['co_license_change_name'],		# 27.사업자등록증 변경 파일명
            # 			u'bs_license_path'				: userInfo['bs_license_path'],				# 28.공사업 등록수첩 경로
            # 			u'bs_license_original_name'		: userInfo['bs_license_original_name'],		# 29.공사업 등록수첨 원본 파일명
            # 			u'bs_license_change_name'		: userInfo['bs_license_change_name'],		# 30.공사업 등록수첨 변경 파일명
            "manager_type": userInfo["manager_type"],
            # 			u'user_license_path'			: userInfo['user_license_path'],			# 31.등급수첩 경로
            # 			u'user_license_original_name'	: userInfo['user_license_original_name'],	# 32.등급수첩 원본 파일명
            # 			u'user_license_change_name'		: userInfo['user_license_change_name'],		# 33.등급수첩 변경 파일명
            # 			u'sign_path'					: userInfo['sign_path'],					# 34.싸인 경로
            # 			u'sign_original_name'			: userInfo['sign_original_name'],			# 35.싸인 원본 파일명
            # 			u'sign_change_name'				: userInfo['sign_change_name']				# 36.싸인 변경 파일명
        }

    def makeUserCntResultModel(self):
        return {"cnt": 0}  # 총 개수

    def makeUserCntResult(self, userCnt):
        return {"cnt": userCnt["cnt"]}  # 총 개수

    def makeReqUserInfoModel(self):
        return {
            "id": "",  # 2.아이디 1
            "authority_code": "",  # 3.권한코드(업무구분)
            "password": "",  # 4.패스워드 3
            "user_name": "",  # 5.이름 2
            "user_position": "",  # 6.직위 6
            "user_contact": "",  # 7.사용자 연락처 4
            "user_email": "",  # 8.사용자 이메일 5
            "user_type": "",  # 20.사용자 구분
            "join_date": "",  # 22.가입날짜 7
            "appro_date": "",  # 23.가입승인날짜
            "co_code": "",  # 회사 코드
        }
