import os
import sys
import copy
import json
import re
from typing import Counter
import uuid
import shutil
import csv
import multiprocessing
import gzip
import io
import locale
from collections import Counter

from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import spaceHome
from allscapeAPIMain import processDetailHome
from allscapeAPIMain import processDetailFile

from common.logManage import logManage
from common import constants
from common.excelService import excelService
from common.commonService import commonService
from projectProcessManage.sqlProjectProcessManage import (
    sqlProjectProcessManage,
)
from projectWorkLogManage.sqlProjectWorkLogManage import sqlProjectWorkLogManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectProcessManage:
    """공정상세도 관리 Service Class"""

    def post_PCcode(self, index, name, Excode):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        if not index:
            query = sqlProjectProcessManage.select_PCcode()
            resCd, msg, pcData = dbms.query(query)
            if resCd != 0:
                return resCd, msg, None
            index = len(pcData) if pcData else 0
        query = sqlProjectProcessManage.insert_PCcode(index, name, Excode)

        return dbms.execute(query)

    def post_process(self, cons_code, co_code, index, uuid) -> dict:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        if index:
            query = sqlProjectProcessManage.upload_file(cons_code, co_code, index)
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "update_file Query : " + query,
            )
            resCd, msg, _ = dbms.execute(query)
            if resCd == 0:
                query = sqlProjectProcessManage.select_file(cons_code, co_code, index)
        else:
            query = sqlProjectProcessManage.approve_file(cons_code, co_code, uuid)
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "approve_file Query : " + query,
            )
            resCd, msg, _ = dbms.execute(query)
            if resCd == 0:
                query = sqlProjectProcessManage.select_file_uuid(
                    cons_code, co_code, uuid
                )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_file Query : " + query,
        )
        resCd, msg, Data = dbms.queryForObject(query)

        if resCd == 0 and Data:
            index = Data["file_index"]
            file_path = Data["file_path"]
            csv_name = os.path.splitext(Data["chan_name"])[0] + ".csv.gz"
            csv_name2 = os.path.splitext(Data["chan_name"])[0] + "2.csv.gz"

            item_data, pc_data = list(), list()
            with gzip.open(file_path + csv_name, "rt", encoding="utf-8") as gz_file:
                reader = csv.reader(gz_file)
                for row in reader:
                    item_data.append(row)
            with gzip.open(file_path + csv_name2, "rt", encoding="utf-8") as gz_file:
                reader = csv.reader(gz_file)
                for row in reader:
                    pc_data.append(row)

            query_list = list()
            query = sqlProjectProcessManage.upload_file(cons_code, co_code, index)
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "upload_file Query : " + query,
            )
            query_list.append(query)

            #### 품목 등록 ####
            item_dict = {"추가": list(), "변경": list(), "삭제": list()}

            for item in item_data:

                if item[10] in ["추가", "변경", "삭제"]:
                    item_dict[item[10]].append(item)
                else:
                    item_dict["추가"].append(item)

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "upload_file Query : " + str(item_data[-1]),
            )
            for item in item_dict["변경"]:
                query = sqlProjectProcessManage.update_item(
                    cons_code,
                    co_code,
                    *item[0:10],
                )
                query_list.append(query)

            if item_dict["추가"]:
                item_query_head = sqlProjectProcessManage.insert_item_head()
                item_query_body = list()

                for item in item_dict["추가"]:
                    query = sqlProjectProcessManage.insert_item_body(
                        cons_code,
                        co_code,
                        *item[0:10],
                    )
                    item_query_body.append(query)

                item_query_foot = sqlProjectProcessManage.insert_item_foot()
                query = f"{item_query_head} {', '.join(item_query_body[:5])} {item_query_foot}"
                query_list.append(query)

            for item in item_dict["삭제"]:
                query = sqlProjectProcessManage.delete_item(
                    cons_code, co_code, item[0], item[1], item[2]
                )
                query_list.append(query)

            #### 공종 등록 ####
            query = sqlProjectProcessManage.delete_pc(cons_code, co_code)
            query_list.append(query)
            if pc_data:
                pc_query_head = sqlProjectProcessManage.insert_pc_head()
                pc_query_body = list()
                for pc in pc_data:
                    query = sqlProjectProcessManage.insert_pc_body(
                        cons_code,
                        co_code,
                        *pc[0:14],
                    )
                    pc_query_body.append(query)

                pc_query_foot = sqlProjectProcessManage.insert_pc_foot()
                query = f"{pc_query_head} {', '.join(pc_query_body)} {pc_query_foot}"
                query_list.append(query)
            resCd, msg, _ = dbms.executeIter(query_list)

            #### 업데이트 된 내역서를 가져와서 양식을 채워둔다 ####
            if resCd == 0:
                query = sqlProjectProcessManage.select_item(cons_code, co_code)
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "품목 조회" + query,
                )
                resCd, msg, item_info = dbms.query(query)

                if resCd == 0:
                    query = sqlProjectProcessManage.select_pc(cons_code, co_code)
                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "공종 조회" + query,
                    )
                    resCd, msg, pc_info = dbms.query(query)
                    if resCd == 0:
                        form_file = spaceHome + processDetailHome + "process_form.xlsx"
                        output_file = file_path + "standard"
                        logs.debug(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "양식파일 업데이트",
                        )
                        excelService.append_to_excel(
                            form_file, output_file, item_info, pc_info
                        )

        return resCd, msg, None

    def get_process(self, cons_code, co_code, pc_code, cons_date) -> dict:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectProcessManage.select(cons_code, co_code, pc_code, cons_date)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select Query : " + query,
        )

        return dbms.query(query)

    def get_process_date(self, cons_code, co_code) -> dict:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectProcessManage.select_date(cons_code, co_code)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_date Query : " + query,
        )

        return dbms.query(query)

    def get_process_all(self, cons_code, co_code) -> dict:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectProcessManage.select_all(cons_code, co_code)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_all Query : " + query,
        )

        return dbms.query(query)

    def get_process_detail(self, cons_code, co_code, level1, level2, level3) -> dict:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectProcessManage.select_names(
            cons_code, co_code, level1, level2, level3
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "get_process_detail Query : " + query,
        )

        return dbms.query(query)

    def get_process_code_count(self):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectProcessManage.select_PCcode_index()
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_PCcode_index Query : " + query,
        )

        return dbms.queryForObject(query)

    def get_process_codes(self):
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectProcessManage.select_PCcode()
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "get_process_codes Query : " + query,
        )

        return dbms.query(query)

    def get_level_codes(self, cons_code, co_code, pc_code, level1, level2, level3):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        if not level1:
            query = sqlProjectProcessManage.select_level1(cons_code, co_code, pc_code)
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_level1 Query : " + query,
            )
        elif not level2:
            query = sqlProjectProcessManage.select_level2(
                cons_code, co_code, pc_code, level1
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_level2 Query : " + query,
            )
        elif not level3:
            query = sqlProjectProcessManage.select_level3(
                cons_code, co_code, pc_code, level1, level2
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_level3 Query : " + query,
            )
        else:
            query = sqlProjectProcessManage.select_level4(
                cons_code, co_code, pc_code, level1, level2, level3
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_level4 Query : " + query,
            )

        return dbms.query(query)

    def read_process_bypc(self, cons_code, co_code, index) -> dict:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectProcessManage.select_file(cons_code, co_code, index)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_file Query : " + query,
        )

        resCd, msg, fileData = dbms.queryForObject(query)
        if resCd == 0 and fileData:
            query = sqlProjectProcessManage.select_item(cons_code, co_code)
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_item Query : " + query,
            )
            resCd, msg, item_data = dbms.query(query)
            if resCd == 0:
                query = sqlProjectProcessManage.select_pc(cons_code, co_code)
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "select_pc Query : " + query,
                )
                resCd, msg, pc_data = dbms.query(query)
                if resCd == 0:
                    file_path, chan_name = fileData["file_path"], fileData["chan_name"]

                    #################################### .csv.gz 파일을 읽는다 ##########################
                    csv_name = os.path.splitext(chan_name)[0] + ".csv.gz"
                    csv_name2 = os.path.splitext(chan_name)[0] + "2.csv.gz"

                    change_pc = list()
                    change_item = {
                        str((item["pc_name"], item["description"], item["standard"])): [
                            item["quantity"],
                            item["material_unit_cost"],
                            item["labor_unit_cost"],
                            item["other_unit_cost"],
                        ]
                        for item in item_data
                    }
                    with gzip.open(
                        file_path + csv_name2, "rt", encoding="utf-8"
                    ) as gz_file:
                        reader = csv.reader(gz_file)
                        for row in reader:
                            if any(row[0] == pc["pc_name"] for pc in pc_data):
                                change_pc.append(row)
                    with gzip.open(
                        file_path + csv_name, "rt", encoding="utf-8"
                    ) as gz_file:
                        reader = csv.reader(gz_file)
                        for row in reader:
                            if any(row[0] == pc[0] for pc in change_pc):
                                if row[14] == "추가":
                                    change_item[(row[0], row[2], row[3])] = [
                                        row[6],
                                        row[7],
                                        row[8],
                                        row[9],
                                    ]
                                elif row[14] == "변경":
                                    change_item[(row[0], row[2], row[3])] = [
                                        row[6],
                                        row[7],
                                        row[8],
                                        row[9],
                                    ]
                                elif row[14] == "삭제":
                                    del change_item[(row[0], row[2], row[3])]

        return resCd, msg, [change_pc, change_item]

    def count_process_bypc(self, cons_code, co_code) -> dict:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectProcessManage.count_bypc(cons_code, co_code)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "count_process_bypc Query : " + query,
        )

        resCd, msg, baseData = dbms.query(query)
        total_cost = 0
        if resCd == 0 and baseData:
            for pc_data in baseData:
                total_cost += pc_data["pc_cost"]
            for pc_data in baseData:
                pc_data["ratio"] = round(pc_data["pc_cost"] / total_cost * 100, 4)

        return resCd, msg, baseData

    def count_process_bylevel(self, cons_code, co_code) -> dict:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectProcessManage.get_base_bylevel(cons_code, co_code)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "get_base_bylevel Query : " + query,
        )
        resCd, msg, baseData = dbms.query(query)
        if resCd == 0 and baseData:
            query = sqlProjectProcessManage.count_bylevel(cons_code, co_code)

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "count_process_bylevel Query : " + query,
            )
            resCd, msg, dateData = dbms.query(query)
            if resCd == 0 and dateData:
                total_price_dict = {
                    data["cons_num"]: data["total_price"] for data in baseData
                }
                for data in dateData:
                    data["total_price"] = total_price_dict[data["cons_num"]]
                    data["rate"] = round(
                        data["used_price"] / data["total_price"] * 100, 4
                    )
                    data["acc_rate"] = round(
                        data["acc_price"] / data["total_price"] * 100, 4
                    )

                baseData.extend(dateData)
        return resCd, msg, baseData

    def update_process_auto(self, cons_code, co_code, level_code) -> dict:

        level1, level2, level3, level4 = (
            int(level_code[0:2]),
            int(level_code[2:4]),
            int(level_code[4:6]),
            int(level_code[6:]),
        )
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        query = sqlProjectProcessManage.update_auto(
            cons_code, co_code, level1, level2, level3, level4
        )

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "update_process_auto Query : " + query,
        )

        return dbms.executeMulti(query)

    def delete_process(self, cons_code, co_code) -> dict:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectProcessManage.delete(cons_code, co_code)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delPlanReview Query : " + query,
        )

        return dbms.execute(query)

    def get_process_file_all(self, cons_code, co_code, id) -> dict:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectProcessManage.select_file_all(cons_code, co_code, id)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_file_all Query : " + query,
        )

        return dbms.query(query)

    def write_process_csv(
        self, cons_code, co_code, file_path, chan_name, csv_name, csv_name2
    ):
        try:
            item_data, pc_data = excelService.parse_process_change(
                file_path + chan_name
            )
        except Exception as e:
            return

        with open(file_path + csv_name, "wb") as csvfile:
            with gzip.GzipFile(fileobj=csvfile, mode="wb") as gz_file:
                text_writer = io.TextIOWrapper(gz_file, write_through=True)
                writer = csv.writer(text_writer)
                writer.writerows(item_data)

        with open(file_path + csv_name2, "wb") as csvfile:
            with gzip.GzipFile(fileobj=csvfile, mode="wb") as gz_file:
                text_writer = io.TextIOWrapper(gz_file, write_through=True)
                writer = csv.writer(text_writer)
                writer.writerows(pc_data)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "CSV gz file 작성 성공",
        )
        return

    def post_process_file(self, cons_code, co_code, id, change_date, file, updated):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        detail_path = processDetailFile.replace("{cons_code}", cons_code).replace(
            "{co_code}", co_code
        )
        file_path = spaceHome + detail_path
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "file_path detail : " + file_path,
        )
        os.makedirs(file_path, exist_ok=True)
        orig_name = file.filename
        _, ext = os.path.splitext(orig_name)
        post_uuid = str(uuid.uuid4()).replace("-", "")
        chan_name, csv_name, csv_name2 = (
            post_uuid + ext,
            post_uuid + ".csv.gz",
            post_uuid + "2.csv.gz",
        )
        file.save(file_path + chan_name)
        item_data, pc_data = excelService.parse_process_change(file_path + chan_name)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "item_len : " + str(len(item_data)),
        )
        query = sqlProjectProcessManage.insert_file(
            cons_code,
            co_code,
            file_path,
            orig_name,
            chan_name,
            change_date,
            id,
            post_uuid,
            updated,
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "insert_file Query : " + query,
        )
        resCd, msg, _ = dbms.execute(query)

        if resCd == 0:
            query = sqlProjectProcessManage.select_file_index(post_uuid)
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_file_index Query : " + query,
            )
            resCd, msg, data = dbms.queryForObject(query)
            if updated == 2:
                query_list = list()
                query = sqlProjectProcessManage.upload_file(
                    cons_code, co_code, data["file_index"]
                )
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "upload_file Query : " + query,
                )
                query_list.append(query)

                #### 내역 직접등록이므로 즉시 DB 반영 절차 시작 ####
                #### 품목 등록 ####
                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    f"item_dict : {str(item_data[0])} {str(len(item_data[0]))}",
                )

                item_query_head = sqlProjectProcessManage.insert_item_head()
                item_query_body = list()
                for item in item_data:
                    query = sqlProjectProcessManage.insert_item_body(
                        cons_code,
                        co_code,
                        *item[0:10],
                    )
                    item_query_body.append(query)
                item_query_foot = sqlProjectProcessManage.insert_item_foot()
                query = (
                    f"{item_query_head} {', '.join(item_query_body)} {item_query_foot}"
                )
                query_list.append(query)

                #### 공종 등록 ####
                query = sqlProjectProcessManage.delete_pc(cons_code, co_code)
                query_list.append(query)
                if pc_data:
                    pc_query_head = sqlProjectProcessManage.insert_pc_head()
                    pc_query_body = list()
                    for pc in pc_data:
                        query = sqlProjectProcessManage.insert_pc_body(
                            cons_code,
                            co_code,
                            *pc[0:14],
                        )
                        pc_query_body.append(query)

                    pc_query_foot = sqlProjectProcessManage.insert_pc_foot()
                    query = (
                        f"{pc_query_head} {', '.join(pc_query_body)} {pc_query_foot}"
                    )
                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "inser pc Query : " + query,
                    )
                    query_list.append(query)

                resCd, msg, _ = dbms.executeIter(query_list)

                #### 업데이트 된 내역서를 가져와서 양식을 채워둔다 ####
                if resCd == 0:
                    query = sqlProjectProcessManage.select_item(cons_code, co_code)
                    logs.debug(
                        procName,
                        os.path.basename(__file__),
                        sys._getframe(0).f_code.co_name,
                        "select_item Query : " + query,
                    )
                    resCd, msg, item_info = dbms.query(query)
                    if resCd == 0:
                        query = sqlProjectProcessManage.select_pc(cons_code, co_code)
                        logs.debug(
                            procName,
                            os.path.basename(__file__),
                            sys._getframe(0).f_code.co_name,
                            "select_pc Query : " + query,
                        )
                        resCd, msg, pc_info = dbms.query(query)

                        form_file = spaceHome + processDetailHome + "process_form.xlsx"
                        output_file = file_path + "standard"
                        excelService.append_to_excel(
                            form_file, output_file, item_info, pc_info
                        )

        if resCd != 0 and os.path.isfile(file_path + chan_name):
            os.remove(file_path + chan_name)
            return resCd, msg, None

        csv_writer = multiprocessing.Process(
            target=self.write_process_csv,
            args=(
                cons_code,
                co_code,
                file_path,
                chan_name,
                csv_name,
                csv_name2,
            ),
        )
        csv_writer.start()
        item_data = [item for item in item_data if item[10] in ["추가", "삭제", "변경"]]
        #### 현 DB와의 차이점 비교 시작 ####
        query = sqlProjectProcessManage.select_item(cons_code, co_code)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_item Query : " + query,
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_item Query : " + query,
        )
        resCd, msg, orig_items = dbms.query(query)
        new_diff_data = list()
        if resCd == 0:
            diff_data = {}
            for chan_item in item_data:
                if chan_item[10] not in ["추가", "삭제", "변경"]:
                    continue
                key = (chan_item[0], chan_item[1], chan_item[2] if chan_item[2] else "")
                value = [*chan_item[3:10]]
                diff_data[key] = [[], value]
            for orig_item in orig_items:
                key = (
                    orig_item["pc_name"],
                    orig_item["description"],
                    orig_item["standard"] if orig_item["standard"] else "",
                )
                value = [
                    orig_item["vendor"] if orig_item["vendor"] else "",
                    orig_item["unit"],
                    orig_item["quantity"],
                    orig_item["head"],
                    orig_item["material_unit_cost"],
                    orig_item["labor_unit_cost"],
                    orig_item["other_unit_cost"],
                ]
                if key in diff_data:
                    diff_data[key][0] = value
            for key, value in diff_data.items():
                new_diff_data.append([*key, *value[0]])
                new_diff_data.append([*key, *value[1]])
        return (
            resCd,
            msg,
            {
                "index": data["file_index"],
                "item": item_data,
                "pc": pc_data,
                "diff": new_diff_data,
            },
        )

    def get_process_file(self, cons_code, co_code, index) -> dict:
        """리스트에 등록된 파일을 파싱해 결과를 보여준다"""

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사
        servProjProcessMana = servProjectProcessManage()
        commServ = commonService()

        query = sqlProjectProcessManage.select_file(cons_code, co_code, index)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_file Query : " + query,
        )

        resCd, msg, fileData = dbms.queryForObject(query)
        item_data = list()
        pc_data = list()
        new_diff_data = list()
        if resCd == 0:
            file_path, chan_name = fileData["file_path"], fileData["chan_name"]

            #################################### .csv.gz 파일을 읽는다 ##########################
            csv_name, csv_name2 = (
                os.path.splitext(chan_name)[0] + ".csv.gz",
                os.path.splitext(chan_name)[0] + "2.csv.gz",
            )
            with gzip.open(file_path + csv_name, "rt", encoding="utf-8") as gz_file:
                reader = csv.reader(gz_file)
                for row in reader:
                    item_data.append(
                        [int(x) if i >= 5 and i < 10 else x for i, x in enumerate(row)]
                    )

            with gzip.open(file_path + csv_name2, "rt", encoding="utf-8") as gz_file:
                reader = csv.reader(gz_file)
                for row in reader:
                    pc_data.append(row)

            #### 현 DB와의 차이점 비교 시작 ####
            query = sqlProjectProcessManage.select_item(cons_code, co_code)
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "select_item Query : " + query,
            )
            resCd, msg, orig_items = dbms.query(query)

            if resCd == 0:
                diff_data = {}
                for chan_item in item_data:
                    if chan_item[10] not in ["추가", "삭제", "변경"]:
                        continue
                    key = (
                        chan_item[0],
                        chan_item[1],
                        chan_item[2] if chan_item[2] else "",
                    )
                    value = [*chan_item[3:10]]
                    diff_data[key] = [[], value]
                for orig_item in orig_items:
                    key = (
                        orig_item["pc_name"],
                        orig_item["description"],
                        orig_item["standard"] if orig_item["standard"] else "",
                    )
                    value = [
                        orig_item["vendor"] if orig_item["vendor"] else "",
                        orig_item["unit"],
                        orig_item["quantity"],
                        orig_item["head"],
                        orig_item["material_unit_cost"],
                        orig_item["labor_unit_cost"],
                        orig_item["other_unit_cost"],
                    ]
                    if key in diff_data:
                        diff_data[key][0] = value
                for key, value in diff_data.items():
                    new_diff_data.append([*key, *value[0]])
                    new_diff_data.append([*key, *value[1]])
        return resCd, msg, {"item": item_data, "pc": pc_data, "diff": new_diff_data}

    def put_process_file(self, cons_code, co_code, index, file) -> dict:
        """리스트에 등록된 파일을 업데이트 한다"""
        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectProcessManage.select_file(cons_code, co_code, index)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_file Query : " + query,
        )

        resCd, msg, fileData = dbms.queryForObject(query)

        if resCd == 0:

            detail_path = processDetailFile.replace("{cons_code}", cons_code).replace(
                "{co_code}", co_code
            )
            file_path = "".join([spaceHome, detail_path])
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "file_path detail : " + file_path,
            )
            os.makedirs(file_path, exist_ok=True)
            orig_name = file.filename
            _, ext = os.path.splitext(orig_name)
            uuid_value = str(uuid.uuid4()).replace("-", "")
            chan_name, csv_name = uuid_value + ext, uuid_value + ".csv.gz"
            file.save(file_path + chan_name)

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "insert_file Query : " + query,
            )

            resCd, msg, _ = dbms.execute(query)
            if resCd != 0 and os.path.isfile(file_path + chan_name):
                shutil.rmtree(file_path + chan_name, ignore_errors=True)
            csv_writer = multiprocessing.Process(
                target=self.write_process_csv,
                args=(
                    cons_code,
                    co_code,
                    file_path,
                    chan_name,
                    csv_name,
                ),
            )
            csv_writer.start()
            item_data, pc_data = excelService.parse_process_change(
                file_path + chan_name
            )
            data = {"item": item_data, "pc": pc_data}
            return resCd, msg, data

    def delete_process_file(self, cons_code, co_code, index) -> dict:

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectProcessManage.select_file(cons_code, co_code, index)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_file Query : " + query,
        )

        resCd, msg, fileData = dbms.queryForObject(query)
        if resCd == 0 and fileData:
            query = sqlProjectProcessManage.delete_file(cons_code, co_code, index)

            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "delete_file Query : " + query,
            )

            resCd, msg, _ = dbms.execute(query)
            if resCd == 0:
                if os.path.isfile(fileData["file_path"] + fileData["chan_name"]):
                    os.remove(fileData["file_path"] + fileData["chan_name"])
                csv_name = os.path.splitext(fileData["chan_name"])[0] + ".csv.gz"
                if os.path.isfile(fileData["file_path"] + csv_name):
                    os.remove(fileData["file_path"] + csv_name)

        return resCd, msg, None

    def post_process_diff(
        self, cons_code, co_code, change_date, diff, orig_name, id, post_uuid
    ):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectProcessManage.select_base(cons_code, co_code)
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            f"select_base Query: {query}",
        )

        resCd, msg, origData = dbms.query(query)
        origData = [list(data.values()) for data in origData]

        #### diff 를 이용해 data 변경 ####
        chanData = list()
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            f"chanlen : {str(len(chanData))} updatelen: {str(len(diff['update']))}, deletelen: {str(len(diff['delete']))}",
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            f"{str(origData[0])} vs {str(diff['delete'])} and {str(origData[0]) == str(diff['delete'])}",
        )

        def compare_rows(row1, row2):
            return row1[4:8] == row2[4:8]

        level_counter = Counter()
        orig_update = diff["update"][::2]
        chan_update = diff["update"][1::2]
        for data in origData:
            level_counter[tuple(data[4:7])] += 1
            if any(compare_rows(data, update_row) for update_row in orig_update):
                index = [
                    i
                    for i, update_row in enumerate(orig_update)
                    if compare_rows(data, update_row)
                ][0]
                chanData.append(chan_update[index])
            elif any(compare_rows(data, delete_row) for delete_row in diff["delete"]):
                continue
            else:
                chanData.append(data)

        for data in diff["add"]:
            level_counter[tuple(data[4:7])] += 1
            data[7] = level_counter[tuple(data[4:7])]
            chanData.append(data)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "origlen : " + str(len(origData)),
        )
        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "chan : " + str(chanData),
        )

        chanData.sort(key=lambda x: (x[2] is None, x[2], x[4], x[5], x[6], x[7]))

        if resCd == 0:
            detail_path = processDetailFile.replace("{cons_code}", cons_code).replace(
                "{co_code}", co_code
            )
            file_path = "".join([spaceHome, detail_path])
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "file_path detail : " + file_path,
            )
            os.makedirs(file_path, exist_ok=True)
            if not orig_name:
                orig_name = "공정내역서"
            _, ext = os.path.splitext(orig_name)
            uuid_value = str(uuid.uuid4()).replace("-", "")
            chan_name, csv_name = uuid_value + ext, uuid_value + ".csv.gz"
            query = sqlProjectProcessManage.insert_file(
                cons_code,
                co_code,
                file_path,
                orig_name,
                chan_name,
                change_date,
                id,
                post_uuid,
            )
            logs.debug(
                procName,
                os.path.basename(__file__),
                sys._getframe(0).f_code.co_name,
                "insert_file Query : " + query,
            )
            resCd, msg, _ = dbms.execute(query)

            if resCd == 0:
                with open(file_path + csv_name, "wb") as csvfile:
                    with gzip.GzipFile(fileobj=csvfile, mode="wb") as gz_file:
                        text_writer = io.TextIOWrapper(gz_file, write_through=True)
                        writer = csv.writer(text_writer)
                        writer.writerows(chanData)

                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "CSV gz file 작성 성공",
                )

        return resCd, msg, None

    def get_process_diff(self, cons_code, co_code, first_index, second_index):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        result = None
        query = sqlProjectProcessManage.select_file(cons_code, co_code, second_index)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_file Query : " + query,
        )
        resCd, msg, secondData = dbms.queryForObject(query)

        if resCd == 0:

            if first_index:
                query = sqlProjectProcessManage.select_file(
                    cons_code, co_code, first_index
                )

                logs.debug(
                    procName,
                    os.path.basename(__file__),
                    sys._getframe(0).f_code.co_name,
                    "select_file Query : " + query,
                )
                resCd, msg, firstData = dbms.queryForObject(query)

            if resCd == 0:
                file_path = secondData["file_path"]

                Data1, Data2 = dict(), dict()
                result = {"add": [], "update": [], "delete": []}

                if first_index:
                    first_csv = os.path.splitext(firstData["chan_name"])[0] + ".csv.gz"
                    with gzip.open(
                        file_path + first_csv, "rt", encoding="utf-8"
                    ) as gz_file:
                        reader = csv.reader(gz_file)
                        for row in reader:
                            if row[0] == cons_code and row[1] == co_code:
                                Data1[tuple(row[3:7])] = row

                second_csv = os.path.splitext(secondData["chan_name"])[0] + ".csv.gz"
                with gzip.open(
                    file_path + second_csv, "rt", encoding="utf-8"
                ) as gz_file:
                    reader = csv.reader(gz_file)
                    for row in reader:
                        if row[0] == cons_code and row[1] == co_code:
                            Data2[tuple(row[3:7])] = row

                for key, row1 in Data1.items():
                    row2 = Data2.get(key)
                    if row2:
                        if row1 != row2:
                            result["update"].append((row1, row2))
                        del Data2[key]
                    else:
                        result["delete"].append(row1)

                result["add"] = list(Data2.values())

        return resCd, msg, result

    def get_standard_path(self, cons_code, co_code, sample):

        if not sample:
            file_path = processDetailFile.replace("{cons_code}", cons_code).replace(
                "{co_code}", co_code
            )
            output_file = spaceHome + file_path + "standard.xlsx"
        else:
            file_path = processDetailHome
            output_file = spaceHome + file_path + "process_form.xlsx"

        return constants.REST_RESPONSE_CODE_ZERO, "", output_file

    def post_pc_global(self, number, code_name, code_explain):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectProcessManage.insert_pc_global(number)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "insert_pc_global Query : " + query,
        )

        return dbms.executeSpecial(query, [code_name, code_explain])

    def get_pc_global(self):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectProcessManage.select_pc_global()

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_pc_global Query : " + query,
        )

        return dbms.query(query)

    def put_pc_global(self, number, code_name, code_explain):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectProcessManage.update_pc_global(number)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_pc_global Query : " + query,
        )

        return dbms.executeSpecial(query, [code_name, code_explain])

    def delete_pc_global(self, number):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectProcessManage.delete_pc_global(number)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delete_pc_global Query : " + query,
        )

        return dbms.execute(query)

    def post_pc_local(self, cons_code, co_code, pc_code):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectProcessManage.insert_pc_local(cons_code, co_code, pc_code)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "insert_pc_local Query : " + query,
        )

        return dbms.execute(query)

    def get_pc_local(self, cons_code, co_code):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectProcessManage.select_pc_local(cons_code, co_code)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "select_pc_local Query : " + query,
        )

        return dbms.query(query)

    def delete_pc_local(self, cons_code, co_code, pc_code):

        dbms = copy.copy(db)  # DB 속성이 중복 되지 않도록 객체 복사

        query = sqlProjectProcessManage.delete_pc_local(cons_code, co_code, pc_code)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "delete_pc_local Query : " + query,
        )

        return dbms.execute(query)
