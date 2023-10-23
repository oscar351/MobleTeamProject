import os
import shutil
import sys
import copy
import json
import re
import uuid

from allscapeAPIMain import db
from allscapeAPIMain import procCode
from allscapeAPIMain import procName
from allscapeAPIMain import spaceHome
from allscapeAPIMain import dailyReportImage

from common import constants
from common.logManage import logManage
from logManage.servLogManage import servLogManage
from projectDailyReportManage.sqlProjectDailyReportManage import (
    sqlProjectDailyReportManage,
)

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectDailyReportManage:
    """공사일지 및 사진대지 관리 Service Class"""

    def post_daily_report(
        self,
        cons_code,
        co_code,
        cons_date,
        writer_id,
        manager_name,
        remarks,
        temp,
        sky,
        pty,
        material_data,
        workforce_data,
        content_data,
        photo_data,
        auth_id,
        files,
    ):
        """공사일지 작성"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query_list = list()
        data_list = list()

        #### uuid 생성 ####
        post_uuid = str(uuid.uuid4()).replace("-", "")

        #### 공사일지 작성 ####
        query = sqlProjectDailyReportManage.insert_daily_report(
            cons_code,
            co_code,
            cons_date,
            post_uuid,
            writer_id,
            temp,
            sky,
            pty,
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "insert_daily_report Query : " + query,
        )
        query_list.append(query)
        data_list.append([manager_name, remarks])

        #### 자재 반출입현황 추가 ####
        for material in material_data:
            query = sqlProjectDailyReportManage.insert_material(
                post_uuid,
                material["quantity"],
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "insert_material Query : " + query,
            )
            query_list.append(query)
            data_list.append(
                [
                    material["description"],
                    material["standard"],
                    material["unit"],
                    material["remarks"],
                ]
            )

        #### 인력 현황 추가 ####
        for workforce in workforce_data:
            query = sqlProjectDailyReportManage.insert_workforce(
                post_uuid,
                workforce["day_type"],
                workforce["pc_name"],
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "insert_workforce Query : " + query,
            )
            query_list.append(query)
            data_list.append([workforce["head"][0:10], workforce["remarks"]])

        #### 작업 현황 추가 ####
        for content in content_data:
            query = sqlProjectDailyReportManage.insert_content(
                post_uuid,
                content["day_type"],
                content["pc_name"],
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "insert_content Query : " + query,
            )
            query_list.append(query)
            data_list.append([content["content"]])

        image_path = spaceHome + dailyReportImage.replace("{uuid}", post_uuid)
        #### 사진 대지 추가 ####
        if photo_data:
            os.makedirs(image_path, exist_ok=True)
            for photo, file_key in zip(photo_data, files.keys()):
                image = files[file_key]
                orig_name = image.filename
                _, ext = os.path.splitext(orig_name)
                chan_name = str(uuid.uuid4()).replace("-", "") + ext
                image.save(image_path + chan_name)
                query = sqlProjectDailyReportManage.insert_photo(
                    post_uuid,
                    photo["pc_name"],
                    image_path,
                    chan_name,
                )
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "insert_photo Query : " + query,
                )
                query_list.append(query)
                data_list.append([photo["content"], photo["location"], orig_name])

        #### 위임목록 추가 ####
        if auth_id:
            for user in auth_id:
                query = sqlProjectDailyReportManage.insert_user(post_uuid, user)
                query_list.append(query)
                data_list.append([])

        resCd, msg, _ = dbms.executeIterSpecial(query_list, data_list)
        #### 등록 실패시 저장된 파일도 삭제 ####
        if resCd != 0:
            shutil.rmtree(image_path, ignore_errors=True)

        return resCd, msg, post_uuid

    def get_daily_report_list(
        self, cons_code, co_code, writer_name_keyword, start_date, end_date
    ):
        """공사일지 리스트 조회 및 키워드 검색"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectDailyReportManage.select_daily_report_list(
            cons_code, co_code, start_date, end_date
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_daily_report_list Query : " + query,
        )
        data = ["%Y%m%d", "%Y%m%d", f"%{writer_name_keyword}%"]
        if start_date:
            data.append(["%Y%m%d"])
        if end_date:
            data.append(["%Y%m%d"])
        return dbms.querySpecial(query, data)

    def get_daily_report(self, cons_code, uuid):
        """공사일지 상세조회"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectDailyReportManage.select_daily_report_uuid(cons_code, uuid)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_daily_report Query : " + query,
        )
        resCd, msg, data = dbms.queryForObjectSpeical(query, ["%Y%m%d", "%Y%m%d"])
        #### 공사일지를 찾았으면 자재, 인력, 사진대지 정보를 첨가한다 ####
        if resCd == 0 and data:
            query = sqlProjectDailyReportManage.select_material(data["uuid"])
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_material Query : " + query,
            )

            resCd, msg, data["material"] = dbms.query(query)

            query = sqlProjectDailyReportManage.select_workforce(data["uuid"])
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_workforce Query : " + query,
            )

            resCd, msg, data["workforce"] = dbms.query(query)

            query = sqlProjectDailyReportManage.select_content(data["uuid"])
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_content Query : " + query,
            )

            resCd, msg, data["content"] = dbms.query(query)

            query = sqlProjectDailyReportManage.select_photo(data["uuid"])
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_photo Query : " + query,
            )

            resCd, msg, data["photo"] = dbms.query(query)

            query = sqlProjectDailyReportManage.select_user(data["uuid"])
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_user Query : " + query,
            )

            resCd, msg, data["auth_id"] = dbms.query(query)

        return resCd, msg, data

    def put_daily_report(
        self,
        cons_code,
        co_code,
        cons_date,
        post_uuid,
        manager_name,
        remarks,
        temp,
        sky,
        pty,
        material_data,
        workforce_data,
        content_data,
        photo_data,
        auth_id,
        files,
    ):
        """공사일지 수정"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectDailyReportManage.select_daily_report_uuid(
            cons_code, post_uuid
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_daily_report Query : " + query,
        )
        resCd, msg, data = dbms.queryForObjectSpeical(
            query, ["%Y%m%d", "%Y%m%d"]
        )

        #### 공사일지를 찾았으면 자재, 인력, 사진대지 정보를 수정한다 ####
        if resCd == 0 and data:
            query_list = list()
            data_list = list()

            #### 공사일지 자체 수정 ####
            if any(var is not None for var in [cons_date, manager_name, remarks, temp, sky, pty]):
                query = sqlProjectDailyReportManage.update_daily_report(
                    data["uuid"], cons_date, temp, sky, pty
                )
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "update_daily_report Query : " + query,
                )
                query_list.append(query)
                data_list.append(["%Y%m%d", manager_name, remarks])

            #### 자재 반출입현황 수정 ####
            if material_data:
                for material in material_data:
                    if material["mode"] == "A":
                        query = sqlProjectDailyReportManage.insert_material(
                            data["uuid"],
                            material["quantity"],
                        )
                        logs.debug(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "insert_material Query : " + query,
                        )
                        query_list.append(query)
                        data_list.append(
                            [
                                material["description"],
                                material["standard"],
                                material["unit"],
                                material["remarks"],
                            ]
                        )
                    elif material["mode"] == "U":
                        query = sqlProjectDailyReportManage.update_material(
                            data["uuid"],
                            material["description"],
                            material["standard"],
                            material["unit"],
                            material["quantity"],
                            material["remarks"]
                        )
                        logs.debug(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            f"update_material Query {material['standard']}: " + query,
                        )
                        query_list.append(query)
                        data_list.append(
                            [
                                material["description"],
                                material["standard"],
                                material["unit"],
                                material["remarks"],
                                material["description"],
                                material["standard_ori"],
                            ]
                        )
                    elif material["mode"] == "D":
                        query = sqlProjectDailyReportManage.delete_material(
                            data["uuid"],
                        )
                        logs.debug(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "delete_material Query : " + query,
                        )
                        query_list.append(query)
                        data_list.append(
                            [material["description"], material["standard"]]
                        )

            #### 인력 현황 수정 ####
            if workforce_data:
                for workforce in workforce_data:
                    if workforce["mode"] == "A":
                        query = sqlProjectDailyReportManage.insert_workforce(
                            data["uuid"],
                            workforce["day_type"],
                            workforce["pc_name"],
                        )
                        logs.debug(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "insert_workforce Query : " + query,
                        )
                        query_list.append(query)
                        data_list.append([workforce["head"][:10], workforce["remarks"]])
                    elif workforce["mode"] == "U" and (
                        workforce["head"] or workforce["remarks"]
                    ):
                        query = sqlProjectDailyReportManage.update_workforce(
                            data["uuid"],
                            workforce["day_type"],
                            workforce["pc_name"],
                        )
                        logs.debug(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "update_workforce Query : " + query,
                        )
                        query_list.append(query)
                        data_list.append([workforce["head"][:10], workforce["remarks"]])
                    elif workforce["mode"] == "D":
                        query = sqlProjectDailyReportManage.delete_workforce(
                            data["uuid"], workforce["day_type"], workforce["pc_name"]
                        )
                        logs.debug(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "delete_workforce Query : " + query,
                        )
                        query_list.append(query)
                        data_list.append([])

            #### 작업 현황 수정 ####
            if content_data:
                for content in content_data:
                    if content["mode"] == "A":
                        query = sqlProjectDailyReportManage.insert_content(
                            data["uuid"],
                            content["day_type"],
                            content["pc_name"],
                        )
                        logs.debug(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "insert_content Query : " + query,
                        )
                        query_list.append(query)
                        data_list.append([content["content"]])
                    elif content["mode"] == "U" and content["content"]:
                        query = sqlProjectDailyReportManage.update_content(
                            data["uuid"],
                            content["day_type"],
                            content["pc_name"],
                            content["number"],
                        )
                        logs.debug(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "update_content Query : " + query,
                        )
                        query_list.append(query)
                        data_list.append([content["content"]])
                    elif content["mode"] == "D":
                        query = sqlProjectDailyReportManage.delete_content(
                            data["uuid"],
                            content["day_type"],
                            content["pc_name"],
                            content["number"],
                        )
                        logs.debug(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "delete_content Query : " + query,
                        )
                        query_list.append(query)
                        data_list.append([])

            #### 사진 대지 수정 ####
            add_photo_data = list()
            update_photo_data = list()
            delete_photo_data = list()
            for photo in photo_data:
                if photo["mode"] == "A":
                    add_photo_data.append(photo)
                elif photo["mode"] == "U":
                    if photo["pc_name"]:
                        update_photo_data.append(photo)
                elif photo["mode"] == "D":
                    delete_photo_data.append(photo)

            add_image_list = list()
            delete_image_list = list()

            if update_photo_data:
                for update_photo in update_photo_data:
                    query = sqlProjectDailyReportManage.update_photo(
                        data["uuid"], update_photo["index"], update_photo["pc_name"]
                    )
                    query_list.append(query)
                    data_list.append(
                        [update_photo["content"], update_photo["location"]]
                    )
            if add_photo_data:
                image_path = spaceHome + dailyReportImage.replace(
                    "{uuid}", data["uuid"]
                )
                os.makedirs(image_path, exist_ok=True)
                for add_photo, file_key in zip(add_photo_data, files.keys()):
                    image = files[file_key]
                    orig_name = image.filename
                    _, ext = os.path.splitext(orig_name)
                    chan_name = str(uuid.uuid4()).replace("-", "") + ext
                    image.save(image_path + chan_name)
                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        f"{os.path.exists(image_path + chan_name)}",
                    )
                    query = sqlProjectDailyReportManage.insert_photo(
                        data["uuid"],
                        add_photo["pc_name"],
                        image_path,
                        chan_name,
                    )
                    query_list.append(query)
                    data_list.append(
                        [add_photo["content"], add_photo["location"], orig_name]
                    )
                    add_image_list.append(image_path + chan_name)
            if delete_photo_data:
                image_path = spaceHome + dailyReportImage.replace(
                    "{uuid}", data["uuid"]
                )
                for delete_photo in delete_photo_data:
                    query = sqlProjectDailyReportManage.delete_photo(
                        data["uuid"], delete_photo["index"]
                    )
                    query_list.append(query)
                    data_list.append([])
                    delete_image_list.append(image_path + delete_photo["chan_name"])

            #### 수정권한 수정 ####
            if auth_id:
                for mode, id in auth_id:
                    if mode == "A":
                        query = sqlProjectDailyReportManage.insert_user(
                            data["uuid"], id
                        )
                    elif mode == "D":
                        query = sqlProjectDailyReportManage.delete_user(
                            data["uuid"], id
                        )
                    query_list.append(query)
                    data_list.append([])

            resCd, msg, _ = dbms.executeIterSpecial(query_list, data_list)

            #### 업데이트 실패시 추가하고자 한 파일 삭제
            if resCd != 0:
                for image in add_image_list:
                    if os.path.exists(image):
                        os.remove(image)

            #### 업데이트 성공시 삭제하고자 한 파일 삭제
            else:
                for image in delete_image_list:
                    if os.path.exists(image):
                        os.remove(image)

        return resCd, msg, data["uuid"]

    def delete_daily_report(self, cons_code, uuid):
        """공사일지 삭제"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        #### 삭제해야할 사진파일 위치 조회 ####
        query = sqlProjectDailyReportManage.select_photo(uuid)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_photo Query : " + query,
        )
        resCd, msg, image_data = dbms.query(query)

        if resCd == 0:
            query = sqlProjectDailyReportManage.delete_daily_report(cons_code, uuid)
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "delete_daily_report Query : " + query,
            )
            resCd, msg, _ = dbms.execute(query)

            #### 현장 일보 삭제 성공시 이미지 파일도 삭제 ####
            if resCd == 0:
                for image in image_data:
                    if os.path.exists(image["file_path"] + image["chan_name"]):
                        os.remove(image["file_path"] + image["chan_name"])

        return resCd, msg, None

    def get_photo_list(
        self,
        cons_code,
        co_code,
        writer_name,
        pc_name_keyword,
        content_keyword,
        location_keyword,
        start_date,
        end_date,
    ):
        """사진대지 리스트 조회 및 키워드 검색"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectDailyReportManage.select_photo_list(
            cons_code,
            co_code,
            start_date,
            end_date,
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_photo_list Query : " + query,
        )

        data = [
            "%Y%m%d",
            f"%{writer_name}%",
            f"%{pc_name_keyword}%",
            f"%{content_keyword}%",
            f"%{location_keyword}%",
        ]
        if start_date != "":
            data.append("%Y%m%d")
        if end_date != "":
            data.append("%Y%m%d")
        return dbms.querySpecial(query, data)

    def count_workforce(self, cons_code, co_code, cons_date, pc_name):
        """공종별 투입인원 조회"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectDailyReportManage.count_workforce(
            cons_code, co_code, cons_date, pc_name
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "count_workforce Query : " + query,
        )
        return dbms.queryForObject(query)


    #### 공사 현황 조회 ####
    def get_daily_report_status(self, cons_code):
        """공사 현황 조회"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectDailyReportManage.select_project_dates(cons_code)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_project_dates Query : " + query,
        )
        resCd, msg, dates = dbms.queryForObject(query)
        dataDict = dict()
        if resCd == 0 and dates:
            dataDict["cons_start_date"] = dates.get("cons_start_date")
            dataDict["cons_end_date"] = dates.get("cons_end_date")
            dataDict["status"] = list()
            dataDict["pc_name"] = list()
            query = sqlProjectDailyReportManage.select_project_pc_names(cons_code)
            logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_project_pc_names Query : " + query,
            )
            resCd, msg, pc_names = dbms.query(query)
            if resCd == 0 and pc_names: 
                query = sqlProjectDailyReportManage.select_dailyreport_status(cons_code)
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "get_daily_report_status Query : " + query,
                )

                resCd, msg, data = dbms.query(query)
                dataDict["status"] = [{"cons_date": item["cons_date"], "pc_name": item["pc_name"], "head": item["head"]} for item in data]
                dataDict["pc_name"] = [item["pc_name"] for item in pc_names]
        return resCd, msg, dataDict

