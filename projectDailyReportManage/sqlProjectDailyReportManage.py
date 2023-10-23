#### 공사일지 ERD 설계 ####

"""
공사일지 TABLE - PROJECT_DAILY_REPORT

CONS_CODE (PK)  : 공사코드
CO_CODE (PK)    : 회사코드
CONS_DATE (PK)  : 작업일
UUID (UQ) : 공사일지 코드
NUMBER : 연번
WRITER_NAME : 작성자
MANAGER_NAME : 관리소장
REMARKS : 비고
TEMP : 온도
SKY : 날씨
PTY : 구름
"""

INSERT_DAILY_REPORT = " ".join(
    [
        "INSERT INTO PROJECT_DAILY_REPORT",
        "(CONS_CODE, CO_CODE, CONS_DATE, UUID, WRITER_ID, MANAGER_NAME, REMARKS, TEMP, SKY, PTY)",
        "VALUES({})",
    ]
)

SELECT_DAILY_REPORT = " ".join(
    [
        "SELECT",
        "D.CONS_CODE as cons_code,",
        "D.NUMBER as number,",
        "D.CO_CODE as co_code,",
        "date_format(D.CONS_DATE, %s) as cons_date,",
        "HEX(D.UUID) as uuid,",
        "U.USER_NAME as writer_name,",
        "D.MANAGER_NAME as manager_name,",
        "D.REMARKS as remarks,",
        "D.TEMP as temp,",
        "D.SKY as sky,",
        "D.PTY as pty,",
        "date_format(D.REG_DATE, %s) as reg_date",
        "FROM PROJECT_DAILY_REPORT D",
        "JOIN USER U",
        "ON D.WRITER_ID = U.ID",
        "WHERE 1=1",
        "{}",
        "ORDER BY D.CONS_DATE DESC",
    ]
)

UPDATE_DAILY_REPORT = " ".join(
    [
        "UPDATE PROJECT_DAILY_REPORT",
        "SET {}",
        "WHERE 1=1",
        "{}",
    ]
)

DELETE_DAILY_REPORT = " ".join(
    [
        "DELETE FROM PROJECT_DAILY_REPORT",
        "WHERE 1=1",
        "{}",
    ]
)

"""
공사일지 자재반출입 현황 TABLE - PROJECT_MATERIAL_LOG

UUID (PK) : 공사일지
DESCRIPTION (PK) : 품목
STANDARD (PK) : 규격
UNIT : 단위
QUANTITY : 수량 (반입 : +, 반출 : - )
REMARKS: 자재현황내용
"""

INSERT_MATERIAL = " ".join(
    [
        "INSERT INTO PROJECT_MATERIAL_LOG",
        "(UUID, DESCRIPTION, STANDARD, UNIT, QUANTITY, REMARKS)",
        "VALUES({})",
    ]
)

SELECT_MATERIAL = " ".join(
    [
        "SELECT",
        "DESCRIPTION as description,",
        "STANDARD as standard,",
        "UNIT as unit,",
        "QUANTITY as quantity,",
        "REMARKS as remarks",
        "FROM PROJECT_MATERIAL_LOG",
        "WHERE 1=1",
        "{}",
    ]
)

UPDATE_MATERIAL = " ".join(
    [
        "UPDATE PROJECT_MATERIAL_LOG",
        "SET {}",
        "WHERE 1=1",
        "{}",
    ]
)

DELETE_MATERIAL = " ".join(
    [
        "DELETE FROM PROJECT_MATERIAL_LOG",
        "WHERE 1=1",
        "{}",
    ]
)

"""
공사일지 인력작업내용 현황 TABLE - PROJECT_WORKFORCE_LOG

UUID (PK) : 공사일지
DAY_TYPE (PK) : 금일: 0 / 명일 : 1
PC_NAME (PK) : 공종
CONTENT : 작업 내용
HEAD : 투입 인원수
REMARKS : 비고
"""

INSERT_WORKFORCE = " ".join(
    [
        "INSERT INTO PROJECT_WORKFORCE_LOG",
        "(UUID, DAY_TYPE, PC_NAME, HEAD, REMARKS)",
        "VALUES({})",
    ]
)

COUNT_WORKFORCE = " ".join(
    [
        "SELECT",
        "CAST(IFNULL(SUM(W.HEAD), 0) AS UNSIGNED) as total_head",
        "FROM PROJECT_DAILY_REPORT D",
        "JOIN PROJECT_WORKFORCE_LOG W",
        "ON D.UUID = W.UUID",
        "WHERE 1=1",
        "{}",
    ]
)

SELECT_WORKFORCE = " ".join(
    [
        "SELECT",
        "DAY_TYPE as day_type,",
        "PC_NAME as pc_name,",
        "HEAD as head,",
        "REMARKS as remarks",
        "FROM PROJECT_WORKFORCE_LOG",
        "WHERE 1=1",
        "{}",
    ]
)

UPDATE_WORKFORCE = " ".join(
    [
        "UPDATE PROJECT_WORKFORCE_LOG",
        "SET {}",
        "WHERE 1=1",
        "{}",
    ]
)

DELETE_WORKFORCE = " ".join(
    [
        "DELETE FROM PROJECT_WORKFORCE_LOG",
        "WHERE 1=1",
        "{}",
    ]
)

"""
공사일지 인력작업내용 현황 TABLE - PROJECT_CONTENT_LOG

UUID (PK) : 공사일지
DAY_TYPE (PK) : 금일: 0 / 명일 : 1
PC_NAME (PK) : 공종
CONTENT : 작업 내용
"""

INSERT_CONTENT = " ".join(
    [
        "INSERT INTO PROJECT_CONTENT_LOG",
        "(UUID, DAY_TYPE, PC_NAME, CONTENT)",
        "VALUES({})",
    ]
)

SELECT_CONTENT = " ".join(
    [
        "SELECT",
        "DAY_TYPE as day_type,",
        "PC_NAME as pc_name,",
        "NUMBER as number,",
        "CONTENT as content",
        "FROM PROJECT_CONTENT_LOG",
        "WHERE 1=1",
        "{}",
    ]
)

UPDATE_CONTENT = " ".join(
    [
        "UPDATE PROJECT_CONTENT_LOG",
        "SET CONTENT = %s",
        "WHERE 1=1",
        "{}",
    ]
)

DELETE_CONTENT = " ".join(
    [
        "DELETE FROM PROJECT_CONTENT_LOG",
        "WHERE 1=1",
        "{}",
    ]
)

"""
공사일지 사진대지 TABLE - PROJECT_PHOTO_LOG

UUID (PK)   : 공사일지 UUID
FILE_INDEX  : 연번
PC_NAME (PK)    : 공종
CONTENT     : 내용
LOCATION    : 위치
FILE_PATH   : 사진 경로
ORIG_NAME   : 원본 파일명
CHAN_NAME   : 변경 파일명
"""

INSERT_PHOTO = " ".join(
    [
        "INSERT INTO PROJECT_PHOTO_LOG",
        "(UUID, PC_NAME, CONTENT, LOCATION, FILE_PATH, ORIG_NAME, CHAN_NAME)",
        "VALUES({})",
    ]
)

SELECT_PHOTO_LIST = " ".join(
    [
        "SELECT",
        "D.CONS_CODE as cons_code,",
        "D.CO_CODE as co_code,",
        "date_format(D.CONS_DATE, %s) as cons_date,",
        "U.USER_NAME as writer_name,",
        "P.PC_NAME as pc_name,",
        "P.CONTENT as content,",
        "P.LOCATION as location,",
        "P.FILE_PATH as file_path,",
        "P.ORIG_NAME as orig_name,",
        "P.CHAN_NAME as chan_name",
        "FROM PROJECT_PHOTO_LOG P",
        "JOIN PROJECT_DAILY_REPORT D",
        "ON P.UUID = D.UUID",
        "JOIN USER U",
        "ON D.WRITER_ID = U.ID",
        "WHERE 1=1",
        "{}",
        "ORDER BY D.CONS_DATE DESC, P.PC_NAME",
    ]
)

SELECT_PHOTO = " ".join(
    [
        "SELECT",
        "FILE_INDEX as file_index,",
        "PC_NAME as pc_name,",
        "CONTENT as content,",
        "LOCATION as location,",
        "FILE_PATH as file_path,",
        "ORIG_NAME as orig_name,",
        "CHAN_NAME as chan_name",
        "FROM PROJECT_PHOTO_LOG",
        "WHERE 1=1",
        "{}",
    ]
)

UPDATE_PHOTO = " ".join(
    [
        "UPDATE PROJECT_PHOTO_LOG",
        "SET {}",
        "WHERE 1=1",
        "{}",
    ]
)

DELETE_PHOTO = " ".join(
    [
        "DELETE FROM PROJECT_PHOTO_LOG",
        "WHERE 1=1",
        "{}",
    ]
)

#### 공사일지 수정 권한 부여 ####

INSERT_USER = " ".join(
    [
        "INSERT INTO PROJECT_REPORT_AUTH",
        "(UUID, USER_ID)",
        "VALUES({}, {})",
    ]
)

SELECT_USER = " ".join(
    [
        "SELECT",
        "USER_ID as user_id",
        "FROM PROJECT_REPORT_AUTH",
        "WHERE 1=1",
        "AND UUID = {}",
    ]
)

DELETE_USER = " ".join(
    [
        "DELETE FROM PROJECT_REPORT_AUTH",
        "WHERE 1=1",
        "AND UUID = {}",
        "AND USER_ID = {}",
    ]
)


#### 공사 현황 조회 ####

SELECT_DAILYREPORT_STATUS = " ".join(
    [
        "SELECT",
        "PL.PC_NAME as pc_name,",
        "DATE_FORMAT(PR.CONS_DATE,'%Y%m%d') as cons_date,",
        "CAST(SUM(PL.HEAD) AS UNSIGNED) as head",
        "FROM PROJECT_DAILY_REPORT PR",
        "JOIN PROJECT_WORKFORCE_LOG PL",
        "ON PR.UUID = PL.UUID",
        "WHERE PR.CONS_CODE = {}",
        "GROUP BY CONS_DATE, PC_NAME",
        "ORDER BY CONS_DATE, PC_NAME",
    ]
 )

#### 공사 기간 조회 ####

SELECT_PROJECT_DATES = " ".join([
    "SELECT",
    "CONS_START_DATE as cons_start_date,",
    "CONS_END_DATE as cons_end_date",
    "FROM PROJECT",
    "WHERE CONS_CODE = {}",
])

#### 공종 리스트 조회 ####

SELECT_PROJECT_PC_NAMES = " ".join([
    "SELECT",
    "PC_NAME as pc_name",
    "FROM PROJECT_PROCESS_CODE",
    "WHERE CONS_CODE = {}",
    "GROUP BY PC_NAME"
])

class sqlProjectDailyReportManage:
    #### 공사일지 CRUD ####

    @staticmethod
    def insert_daily_report(
        cons_code,
        co_code,
        cons_date,
        uuid,
        writer_id,
        temp,
        sky,
        pty,
    ):
        query = INSERT_DAILY_REPORT.format(
            ", ".join(
                [
                    f"'{cons_code}'",
                    f"'{co_code}'",
                    f"'{cons_date}'",
                    f"UNHEX('{uuid}')",
                    f"'{writer_id}'",
                    "%s",
                    "%s",
                    f"{temp}",
                    f"{sky}",
                    f"{pty}",
                ]
            )
        )
        return query

    @staticmethod
    def select_daily_report_list(cons_code, co_code, start_date, end_date):
        query = SELECT_DAILY_REPORT.format(
            " ".join(
                [
                    f"AND D.CONS_CODE = '{cons_code}'",
                    f"AND D.CO_CODE = '{co_code}'" if co_code != "" else "",
                    "AND U.USER_NAME LIKE %s",
                    f"AND D.CONS_DATE >= str_to_date('{start_date}', %s)"
                    if start_date
                    else "",
                    f"AND D.CONS_DATE <= str_to_date('{end_date}', %s)"
                    if end_date
                    else "",
                ]
            )
        )
        return query

    @staticmethod
    def select_daily_report(cons_code, co_code, cons_date):
        query = SELECT_DAILY_REPORT.format(
            " ".join(
                [
                    f"AND D.CONS_CODE = '{cons_code}'",
                    f"AND D.CO_CODE = '{co_code}'",
                    f"AND D.CONS_DATE = str_to_date('{cons_date}', %s)",
                ]
            )
        )
        return query

    @staticmethod
    def select_daily_report_uuid(cons_code, uuid):
        query = SELECT_DAILY_REPORT.format(
            " ".join(
                [
                    f"AND D.CONS_CODE = '{cons_code}'",
                    f"AND D.UUID = UNHEX('{uuid}')",
                ]
            )
        )
        return query

    @staticmethod
    def update_daily_report(uuid, cons_date, temp, sky, pty):
        query = UPDATE_DAILY_REPORT.format(
            ", ".join(
                filter(
                    lambda x: x is not None,
                    [
                        f"CONS_DATE = str_to_date('{cons_date}', %s)" if cons_date else None,
                        "MANAGER_NAME = %s",
                        "REMARKS = %s",
                        f"TEMP = {temp}" if temp else None,
                        f"SKY = {sky}" if sky else None,
                        f"PTY = {pty}" if pty else None,
                    ],
                )
            ),
            f"AND UUID = UNHEX('{uuid}')",
        )

        return query

    @staticmethod
    def delete_daily_report(cons_code, uuid):
        query = DELETE_DAILY_REPORT.format(
            " ".join(
                [
                    f"AND CONS_CODE = '{cons_code}'",
                    f"AND UUID = UNHEX('{uuid}')",
                ]
            )
        )
        return query

    #### 자재반출입 현황 CRUD ####

    @staticmethod
    def insert_material(uuid, quantity):
        query = INSERT_MATERIAL.format(
            ", ".join(
                [
                    f"UNHEX('{uuid}')",
                    "%s",
                    "%s",
                    "%s",
                    f"{quantity}" if quantity else "0",
                    "%s",
                ]
            )
        )
        return query

    @staticmethod
    def select_material(uuid):
        query = SELECT_MATERIAL.format(
            " ".join(
                [
                    f"AND UUID = UNHEX('{uuid}')",
                ]
            )
        )
        return query

    @staticmethod
    def update_material(uuid, description, standard, unit, quantity, remarks):
        query = UPDATE_MATERIAL.format(
            ", ".join(
                filter(
                    lambda x: x is not None,
                    [
                        "DESCRIPTION = %s" if description != '' else "",
                        "STANDARD = %s" if standard != '' else "" ,
                        "UNIT = %s",
                        f"QUANTITY = {quantity}" if quantity else None,
                        "REMARKS = %s",
                    ],
                )
            ),
            " ".join(
                [
                    f"AND UUID = UNHEX('{uuid}')",
                    "AND DESCRIPTION = %s",
                    "AND STANDARD = %s",
                ]
            ),
        )
        return query

    @staticmethod
    def delete_material(uuid):
        query = DELETE_MATERIAL.format(
            " ".join(
                [
                    f"AND UUID = UNHEX('{uuid}')",
                    f"AND DESCRIPTION = %s",
                    f"AND STANDARD = %s",
                ]
            )
        )
        return query

    #### 인력 현황 CRUD ####

    @staticmethod
    def insert_workforce(uuid, day_type, pc_name):
        query = INSERT_WORKFORCE.format(
            ", ".join(
                [
                    f"UNHEX('{uuid}')",
                    f"{day_type}",
                    f"'{pc_name}'",
                    "%s",
                    "%s",
                ]
            )
        )
        return query

    @staticmethod
    def count_workforce(cons_code, co_code, cons_date, pc_name):
        query = COUNT_WORKFORCE.format(
            " ".join(
                [
                    f"AND D.CONS_CODE = '{cons_code}'",
                    f"AND D.CO_CODE = '{co_code}'",
                    f"AND W.PC_NAME = '{pc_name}'",
                    f"AND D.CONS_DATE < str_to_date('{cons_date}', '%Y%m%d')"
                    if cons_date
                    else "",
                    "AND W.DAY_TYPE = 0",
                ]
            )
        )
        return query

    @staticmethod
    def select_workforce(uuid):
        query = SELECT_WORKFORCE.format(
            " ".join(
                [
                    f"AND UUID = UNHEX('{uuid}')",
                ]
            )
        )
        return query

    @staticmethod
    def update_workforce(uuid, day_type, pc_name):
        query = UPDATE_WORKFORCE.format(
            ", ".join(
                filter(
                    lambda x: x is not None,
                    [
                        "HEAD = %s",
                        "REMARKS = %s",
                    ],
                )
            ),
            " ".join(
                [
                    f"AND UUID = UNHEX('{uuid}')",
                    f"AND DAY_TYPE = {day_type}",
                    f"AND PC_NAME = '{pc_name}'",
                ]
            ),
        )
        return query

    @staticmethod
    def delete_workforce(uuid, day_type, pc_name):
        query = DELETE_WORKFORCE.format(
            " ".join(
                [
                    f"AND UUID = UNHEX('{uuid}')",
                    f"AND DAY_TYPE = '{day_type}'",
                    f"AND PC_NAME = '{pc_name}'",
                ]
            )
        )
        return query

    #### 공사내용 현황 CRUD ####

    @staticmethod
    def insert_content(uuid, day_type, pc_name):
        query = INSERT_CONTENT.format(
            ", ".join(
                [
                    f"UNHEX('{uuid}')",
                    f"{day_type}",
                    f"'{pc_name}'",
                    "%s",
                ]
            )
        )
        return query

    @staticmethod
    def select_content(uuid):
        query = SELECT_CONTENT.format(
            " ".join(
                [
                    f"AND UUID = UNHEX('{uuid}')",
                ]
            )
        )
        return query

    @staticmethod
    def update_content(uuid, day_type, pc_name, number):
        query = UPDATE_CONTENT.format(
            " ".join(
                [
                    f"AND UUID = UNHEX('{uuid}')",
                    f"AND DAY_TYPE = {day_type}",
                    f"AND PC_NAME = '{pc_name}'",
                    f"AND NUMBER = {number}",
                ]
            ),
        )
        return query

    @staticmethod
    def delete_content(uuid, day_type, pc_name, number):
        query = DELETE_CONTENT.format(
            " ".join(
                [
                    f"AND UUID = UNHEX('{uuid}')",
                    f"AND DAY_TYPE = '{day_type}'",
                    f"AND PC_NAME = '{pc_name}'",
                    f"AND NUMBER = {number}",
                ]
            )
        )
        return query

    #### 사진첨부 현황 CRUD UUID, PC_NAME, CONTENT, LOCATION, FILE_PATH, ORIG_NAME, CHAN_NAME####

    @staticmethod
    def insert_photo(uuid, pc_name, file_path, chan_name):
        query = INSERT_PHOTO.format(
            ", ".join(
                [
                    f"UNHEX('{uuid}')",
                    f"'{pc_name}'",
                    "%s",
                    "%s",
                    f"'{file_path}'",
                    "%s",
                    f"'{chan_name}'",
                ]
            )
        )

        return query

    @staticmethod
    def select_photo_list(
        cons_code,
        co_code,
        start_date,
        end_date,
    ):
        query = SELECT_PHOTO_LIST.format(
            " ".join(
                [
                    f"AND D.CONS_CODE = '{cons_code}'",
                    f"AND D.CO_CODE = '{co_code}'" if co_code else "",
                    "AND U.USER_NAME LIKE %s",
                    "AND P.PC_NAME LIKE %s",
                    "AND P.CONTENT LIKE %s",
                    "AND P.LOCATION LIKE %s",
                    f"AND D.CONS_DATE >= str_to_date('{start_date}', %s)"
                    if start_date != ""
                    else "",
                    f"AND D.CONS_DATE <= str_to_date('{end_date}', %s)"
                    if end_date != ""
                    else "",
                ]
            )
        )
        return query

    @staticmethod
    def select_photo(uuid):
        query = SELECT_PHOTO.format(
            " ".join(
                [
                    f"AND UUID = UNHEX('{uuid}')",
                ]
            )
        )
        return query

    @staticmethod
    def update_photo(uuid, index, pc_name):
        query = UPDATE_PHOTO.format(
            ", ".join(
                filter(
                    lambda x: x is not None,
                    [
                        f"PC_NAME = '{pc_name}'" if pc_name else None,
                        "CONTENT = %s",
                        "LOCATION = %s",
                    ],
                )
            ),
            " ".join(
                [
                    f"AND UUID = UNHEX('{uuid}')",
                    f"AND FILE_INDEX = {index}",
                ]
            ),
        )
        return query

    @staticmethod
    def delete_photo(uuid, index):
        query = DELETE_PHOTO.format(
            " ".join(
                [
                    f"AND UUID = UNHEX('{uuid}')",
                    f"AND FILE_INDEX = {index}",
                ]
            )
        )
        return query

    @staticmethod
    def insert_user(uuid, id):
        query = INSERT_USER.format(
            f"UNHEX('{uuid}')",
            f"'{id}'",
        )

        return query

    @staticmethod
    def select_user(uuid):
        query = SELECT_USER.format(
            f"UNHEX('{uuid}')",
        )

        return query

    @staticmethod
    def delete_user(uuid, id):
        query = DELETE_USER.format(
            f"UNHEX('{uuid}')",
            f"'{id}'",
        )

        return query



    #### 공사 투입 인력 현황 ####

    @staticmethod
    def select_dailyreport_status(cons_code):
        query = SELECT_DAILYREPORT_STATUS.format(
                f"'{cons_code}'",
        )

        return query
    
    #### 공사 기간 조회 ####

    @staticmethod
    def select_project_dates(cons_code):
        query = SELECT_PROJECT_DATES.format(f"'{cons_code}'",)

        return query

    #### 공종 리스트 조회 ####
    @staticmethod
    def select_project_pc_names(cons_code):
        query = SELECT_PROJECT_PC_NAMES.format(f"'{cons_code}'",)
        
        return query