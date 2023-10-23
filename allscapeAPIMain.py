# _*_coding: utf-8 -*-

# API Service 구동
# 작성 날짜 : 2022. 7. 29
# 작성자 : 황희정
# 기능
# 	1. 환경 설정파일 Read
# 	2. DB 접속 설정
# 	3. API Service 구동
# 	4. 파일 관리 설정
# 변경 이력
# 	1. 2022. 07. 29 | 황희정 | 최조 작성
#   2. 2022. 08. 08 ~ 8. 12 | 황희정 | 추가 | 4. 파일관리 설정, 5. System 설정, commManageApi
#                                      수정 | REST API blueprint 등록 위치 변겅


# sys import
from flask import Flask
from flask_restx import Api, Resource
from flask_basicauth import BasicAuth  # swagger 접속을 위한 간단한 보안모듈
import configparser

# user import
from dbManage import dbManage
from common import mailService
from common import weatherService
from common import geoService

# from userManage.apiUserManage import userManageApi
# from commManage.apiCommManage import commManageApi

# 1. 환경 설정파일을 Read
config = configparser.ConfigParser()
config.read(
    "/home/capartner/CA_Projects/ALLSPACE/API/ver_beta/trunk/config/allscape_config.ini"
)

procCode = config.get("PROCESS", "procCode")
procName = config.get("PROCESS", "procName")
procIp = config.get("PROCESS", "procIp")
procPort = config.get("PROCESS", "procPort")

# 2. DB 접속 설정한다.
db_user = config.get("DB", "user")
db_passwd = config.get("DB", "passwd")
db_ip = config.get("DB", "ip")
db_port = int(config.get("DB", "port"))
db_dbname = config.get("DB", "dbname")
db = dbManage.dbManage(procName, db_user, db_passwd, db_ip, db_port, db_dbname)

# 4. 파일 관리 설정
fileHome = config.get("FILE", "fileHome")
userHome = config.get("FILE", "userHome")
typeUser = config.get("FILE", "typeUser")
typeEnterorise = config.get("FILE", "typeEnterorise")
projectHome = config.get("FILE", "projectHome")
procDetails = config.get("FILE", "procDetails")  # 공정 상세 내역서
projInsp = config.get("FILE", "projInsp")  # 현장 점검 첨부 파일
materialHome = config.get("FILE", "materialHome")
materialFile = config.get("FILE", "materialFile")
projDocFile = config.get("FILE", "projDocFile")  # 문서 파일 관리
projDesignBookFile = config.get("FILE", "projDesignBookFile")  # 설계도서 파일 관리
projDetailBookFile = config.get("FILE", "projDetailBookFile")  # 시공상세도 파일 관리
companyHome = config.get("FILE", "companyHome")  # 회사 파일 관리

# 4-1. 공간대장 파일
spaceHome = config.get("FILE", "spaceHome")  # 회사 파일 관리
workLogImgFile = config.get("FILE", "workLogImgFile")  # 작업 이미지 관리
messageBoardFile = config.get("FILE", "messageBoardFile")  # 메시지 보드 파일 관리
approvalBoardFile = config.get("FILE", "approvalBoardFile")  # 승인 보드 파일 관리
requestBoardFile = config.get("FILE", "requestBoardFile")  # 의뢰 보드 파일 관리
processDetailHome = config.get("FILE", "processDetailHome")  # 공정 상세 내역서 홈
processDetailFile = config.get("FILE", "processDetailFile")  # 공정 상세내역서 파일 관리
processChangeFile = config.get("FILE", "processChangeFile")  # 변경관리 파일 관리
dailyReportImage = config.get("FILE", "dailyReportImage")  # 사진대지 이미지 관리
mettingMinutesFile = config.get("FILE", "mettingMinutesFile")  # 회의록 파일 관리

# 5. SYSTEM 설정
coCode = config.get("SYSTEM", "coCode")

# 6. Mail Service 설정
smtpTrustValue = config.get("MAIL", "smtpTrustValue")
smtpTrustPort = config.get("MAIL", "smtpTrustPort")
smtpPassword = config.get("MAIL", "smtpPassword")
smtpLogin = config.get("MAIL", "smtpLogin")
mail = mailService.mailService(smtpTrustValue, smtpTrustPort, smtpPassword, smtpLogin)

# 7. Weather API 설정
apiUrl = config.get("WEATHER", "apiUrl")
serviceKey = config.get("WEATHER", "serviceKey")
numOfRows = config.get("WEATHER", "numOfRows")
pageNo = config.get("WEATHER", "pageNo")
dataType = config.get("WEATHER", "dataType")
weatherApi = weatherService.weatherService(
    apiUrl, serviceKey, numOfRows, pageNo, dataType
)

# 8. Geo API 설정
GeoUrl = config.get("GEO", "apiUrl")
GeoService = config.get("GEO", "service")
GeoRequest = config.get("GEO", "request")
GeoCrs = config.get("GEO", "crs")
GeoFormat = config.get("GEO", "format")
GeoType = config.get("GEO", "type")
GeoServiceKey = config.get("GEO", "serviceKey")
geoApi = geoService.geoService(
    GeoUrl, GeoService, GeoRequest, GeoCrs, GeoFormat, GeoType, GeoServiceKey
)

# app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False
# app.register_blueprint(userManageApi, url_prefix='/userManage')		# 사용자 관리 REST API
# app.register_blueprint(commManageApi, url_prefix='/commManage')		# 공통 관리 REST API

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

# 8. swagger 문서생성
api = Api(
    app,
    title="API 문서",
    description="Space api dev서버",
    port=procPort,
    doc="/space-api-docs",
)

from userManage.apiUserManage import userManageApi
from commManage.apiCommManage import commManageApi
from projectManage.apiProjectManage import projectManageApi
from projectInspManage.apiProjectInspManage import projectInspManageApi
from projectStatisticsManage.apiProjectStatisticsManage import (
    projectStatisticsManageApi,
)
from projectApproMaterManage.apiProjectApproMaterManage import (
    projectApproMaterManageApi,
)
from projectDocManage.apiProjectDocManage import projectDocManageApi
from projectUseMaterialManage.apiProjectUseMaterialManage import (
    projectUseMaterialManageApi,
)
from projectInspMaterManage.apiProjectInspMaterManage import projectInspMaterManageApi
from projectDetectionManage.apiProjectDetectionManage import projectDetectionManageApi
from projectWorkLogManage.apiProjectWorkLogManage import projectWorkLogManageApi
from projectDesignBookManage.apiProjectDesignBookManage import (
    projectDesignBookManageApi,
)
from projectFloorPlanManage.apiProjectFloorPlanManage import projectFloorPlanManageApi
from projectPlanReviewManage.apiProjectPlanReviewManage import (
    projectPlanReviewManageApi,
)
from projectDetailReviewManage.apiProjectDetailReviewManage import (
    projectDetailReviewManageApi,
)
from projectChangeReviewManage.apiProjectChangeReviewManage import (
    projectChangeReviewManageApi,
)
from commonApprovalManage.apiCommonApprovalManage import commonApprovalManageApi
from historyManage.apiHistoryManage import historyManageApi
from projectProcessManage.apiProjectProcessManage import projectProcessManageApi
from projectWorkReplyManage.apiProjectWorkReplyManage import projectWorkReplyManageApi
from projectMessageBoardManage.apiProjectMessageBoardManage import projectMessageBoardManageApi
from projectApprovalBoardManage.apiProjectApprovalBoardManage import projectApprovalBoardManageApi
from projectRequestBoardManage.apiProjectRequestBoardManage import projectRequestBoardManageApi
from projectDailyReportManage.apiProjectDailyReportManage import projectDailyReportManageApi
from projectMettingMinutesManage.apiProjectMettingMinutesManage import projectMettingMinutesManageApi
from logManage.apiLogManage import logManageApi

#### make flask app for gunicorn
def create_app():
    app = Flask(__name__)
    app.config["JSON_AS_ASCII"] = False

    # 8. swagger 문서생성
    api = Api(
        app,
        title="API 문서",
        description="Space api dev서버",
        port=procPort,
        doc="/space-api-docs",
    )

    #### blueprint -> namespace 이주작업 - 스웨거문서 등록 ####
    app.register_blueprint(userManageApi, url_prefix="/userManage")  # 사용자 관리 REST API
    app.register_blueprint(commManageApi, url_prefix="/commManage")  # 공통 관리 REST API
    #### namespace 이주중 ####
    app.register_blueprint(
        projectManageApi, url_prefix="/projManage"
    )  # 프로젝트 관리 REST API
    # api.add_namespace(projectContrManageApi, '/projContractorManage')		# 프로젝트 시공사 관리 REST API
    app.register_blueprint(projectInspManageApi, url_prefix="/projInspManage")  # 현장 점검 관리 REST API
    api.add_namespace(projectStatisticsManageApi, "/projStatistManage")  # 프로젝트 통계 관리 REST API
    app.register_blueprint(projectApproMaterManageApi, url_prefix="/projApproMaterManage")  # 승인 자재 관리 REST API
    app.register_blueprint(projectDocManageApi, url_prefix="/projDocManage")  # 문서 관리 REST API
    app.register_blueprint(projectUseMaterialManageApi, url_prefix="/projUseMaterManage")  # 자재 선정 요청/통보 문서 관리 REST API
    app.register_blueprint(projectInspMaterManageApi, url_prefix="/projInspMaterManage")  # 자재 검수 요청/통보 문서 관리 REST API
    app.register_blueprint(projectDetectionManageApi, url_prefix="/projDeteManage")  # 자재 검수 요청/통보 문서 관리 REST API
    app.register_blueprint(projectWorkLogManageApi, url_prefix="/projWorkLogManage")  # 작업일지 문서 관리 REST API
    app.register_blueprint(projectDesignBookManageApi, url_prefix="/projDesignBookManage")  # 설계도서 관리 REST API
    api.add_namespace(projectFloorPlanManageApi, "/projFloorPlanManage")  # 설계도면 관리 REST API
    api.add_namespace(projectPlanReviewManageApi, "/projPlanReviewManage")  # 설계도면 감리의견 관리 REST API
    api.add_namespace(projectDetailReviewManageApi, "/projDetailReviewManage")  # 시공상세도 검토 관리 REST API
    app.register_blueprint(projectChangeReviewManageApi, url_prefix="/projChangeReviewManage")  # 현장실정 보고서 검토 관리 REST API
    app.register_blueprint(commonApprovalManageApi, url_prefix="/commApproManage")  # 공통 승인 관리 REST API
    app.register_blueprint(historyManageApi, url_prefix="/historyManage")  # 이력 관리 REST API
    api.add_namespace(projectProcessManageApi, "/projProcessManage")  # 공정내역서 검토 관리 REST API
    api.add_namespace(projectWorkReplyManageApi, "/projWorkReplyManage")  # 작업일지 댓글 관리 REST API
    api.add_namespace(projectMessageBoardManageApi, "/projMessageBoardManage")  # Q&A 게시판 관리 REST API
    api.add_namespace(projectApprovalBoardManageApi, "/projApprovalBoardManage")  # 승인 게시판 관리 REST API
    api.add_namespace(projectRequestBoardManageApi, "/projRequestBoardManage")  # 의뢰서 게시판 관리 REST API
    api.add_namespace(projectDailyReportManageApi, "/projDailyReportManage")  # 작업일지 관리 REST API
    api.add_namespace(projectMettingMinutesManageApi, "/projMettingMinutesManage")  # 회의록 관리 REST API
    api.add_namespace(logManageApi, "/logManage")  # 시스템 로그 관리 REST API

    return app


if __name__ == "__main__":
    # 3. API Service 구동
    create_app().run(host=procIp, port=procPort, debug=True)
