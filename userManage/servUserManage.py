# _*_coding: utf-8 -*-
import os
import sys
import copy

from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import projectHome
from allscapeAPIMain import userHome
from allscapeAPIMain import typeUser


from common.commonService import commonService

from common.logManage import logManage

from userManage.sqlUserManage import sqlUserManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servUserManage:

    # 회원 수를 조회 한다.
    #
    # Parameter
    # 	- userInfo | Object | 사용자 정보
    # 	- params   | Object | 검색조건
    def searchUserCnt(self, userInfo, params):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sUserMana = sqlUserManage()

        # 쿼리 생성
        query = sUserMana.sSearchUserCnt(userInfo, params)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchUserCnt Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 회원 관리를 위한 회원 리스트를 조회 한다.
    #
    # Parameter
    # 	- userInfo | Object | 사용자 정보
    # 	- params   | Object | 검색조건
    def searchUserList(self, userInfo, params):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sUserMana = sqlUserManage()

        # 쿼리 생성
        query = sUserMana.sSearchUserList(userInfo, params)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchUserList Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 분야별 전체 회원 리스트를 조회 한다.
    #
    # Parameter
    # 	- params | array | 검색조건
    def searchFieldUserListAll(self, params):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sUserMana = sqlUserManage()

        # 쿼리 생성
        query = sUserMana.sSearchFieldUserListAll(params)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchFieldUserListAll Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 사용자 정보를 가져온다.
    #
    # Parameter
    # 	- type | Integer | 1 = userId, 2 = userToken
    # 	- typeData | String | userId or userToken
    # 	- sysCd | String | system code
    def getUserInfo(self, type, typeData, sysCd):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sUserMana = sqlUserManage()

        # 쿼리 생성
        query = sUserMana.sGetUserInfo(type, typeData, sysCd)  # 사용자 정보 Read Query 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetUserInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    def getCondictionUserInfo(self, auth, coCode):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sUserMana = sqlUserManage()

        # 쿼리 생성
        query = sUserMana.sGetCondictionUserInfo(auth, coCode)  # 사용자 정보 Read Query 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetCondictionUserInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # Token 정보를 업데이트 한다.
    #
    # Parameter
    # 	- type | Integer | 1 = userId, 2 = userToken
    # 	- typeData | String | userId or userToken
    # 	- sysCd | String | system code
    # def updateTokenInfo(self, userId, token, sysCd):
    # 	dbms            = copy.copy(db)         # DB 속성이 중복 되지 않도록 객체 복사
    # 	sUserMana       = sqlUserManage()

    # 쿼리 생성
    # 	query = sUserManage.sGetUserInfo(type, typeData, sysCd)	# 사용자 정보 Read Query 생성
    # 	logs.debug(procName,
    # 			os.path.basename(__file__),
    # 			sys._getframe(0).f_code.co_name,
    # 			u'sGetUserInfo Query : ' + query)

    # 쿼리 실행
    # 	resCd, msg, resData = dbms.queryForObj(query)

    # 	return resCd, msg, resData

    def getCompUserInfo(self, coCode, userId):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sUserMana = sqlUserManage()

        # 쿼리 생성
        query = sUserMana.sGetCompUserInfo(coCode, userId)  # 회사 인력 정보 Read Query 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetCompUserInfo Query : " + query,
        )

        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    def getCoInfo(self, searchList):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sUserMana = sqlUserManage()

        # 쿼리 생성
        query = sUserMana.sGetCoInfo(searchList)  # 회사 정보 조회 Query 생성
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetCoInfo Query : " + query,
        )

        # 쿼리 실행		resCd, msg, resData = dbms.queryForObject(query)
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    def userFileNameManage(self, userId, params, key):
        commServ = commonService()
        path = typeUser.replace("{userId}", userId)

        lpath, origName, changeName = commServ.createFilePathAndName(
            userHome, "", path, params, key
        )

        return lpath, origName, changeName

    # 사용자 기본 정보를 저장 한다.
    def putUserInfo(self, data_user_info_manage):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlUserMana = sqlUserManage()

        # 쿼리 생성
        query = sqlUserMana.iPutUserInfo(data_user_info_manage)  # 사용자 정보 저장 Query
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutUserInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 사용자 기본 정보를 삭제 한다.
    def delUserInfo(self, userId):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlUserMana = sqlUserManage()

        # 쿼리 생성
        query = sqlUserMana.dDelUserInfo(userId)  # 사용자 정보 삭제 Query
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelUserInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 사용자 분야/등급 정보를 저장 한다.
    def putUserFieldRatingInfo(self, data_user_field_rating_info_manage):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlUserMana = sqlUserManage()

        # 쿼리 생성
        query = sqlUserMana.iPutUserFieldRatingInfo(
            data_user_field_rating_info_manage
        )  # 사용자 분야/등급 정보 저장 Query
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutUserFieldRatingInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 사용자 분야/등급 정보를 조회 한다.
    def getUserFieldRatingInfo(self, type, userId):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlUserMana = sqlUserManage()

        # 쿼리 생성
        query = sqlUserMana.sGetUserFieldRatingInfo(
            type, userId
        )  # 사용자 분야/등급 정보 조회 Query
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetUserFieldRatingInfo Query : " + query,
        )

        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 사용자 분야/등급 정보를 삭제 한다.
    def delUserFieldRatingInfo(self, userId):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlUserMana = sqlUserManage()

        # 쿼리 생성
        query = sqlUserMana.dDelUserFieldRatingInfo(userId)  # 사용자 분야/등급 정보 삭제 Query
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelUserFieldRatingInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 사용자 파일 정보를 저장 한다.
    def putUserFileInfo(self, data_user_file_info_manage):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlUserMana = sqlUserManage()

        # 쿼리 생성
        query = sqlUserMana.iPutUserFileInfo(
            data_user_file_info_manage
        )  # 사용자 파일 정보 저장 Query
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutUserFileInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 사용자 파일 정보를 삭제 한다.
    def delUserFileInfo(self, userId):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlUserMana = sqlUserManage()

        # 쿼리 생성
        query = sqlUserMana.dDelUserFileInfo(userId)  # 사용자 파일 정보 삭제 Query
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "dDelUserFileInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 사용자 파일 정보를 수정 한다.
    def updateUserFileInfo(self, userInfo):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlUserMana = sqlUserManage()

        # 쿼리 생성
        query = sqlUserMana.uUpdateUserFileInfo(userInfo)  # 사용자 파일 정보 삭제 Query
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uUpdateUserFileInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 사용자 정보를 수정 한다.
    def updateUserInfo(self, userInfo):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlUserMana = sqlUserManage()

        # 쿼리 생성
        # query = sqlUserMana.uUpdateUserInfo(userInfo, type)
        query = sqlUserMana.uUpdateUserInfo(userInfo)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uUpdateUserInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 사용자(관리자 및 회사 코드) 정보 수정
    def updateUserCoInfo(self, userId, updateUserInfoList):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlUserMana = sqlUserManage()

        query = sqlUserMana.uUpdateUserCoInfo(userId, updateUserInfoList)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uUpdateUserCoInfo Query : " + query,
        )

        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 사용자를 검색한다.(검색 조건이 List로 넘어간다.)
    def searchUserInfoList(self, searchList):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        sqlUserMana = sqlUserManage()

        query = sqlUserMana.sSearchUserInfoList(searchList)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sSearchUserInfoList Query : " + query,
        )

        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    def get_user_approvals(self, id, cons_code):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlUserManage.select_approvals(cons_code)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_approvals Query : " + query,
        )

        return dbms.querySpecial(query, [id, id])      