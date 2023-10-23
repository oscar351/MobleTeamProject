# _*_coding: utf-8 -*-

import pandas as pd
import re
import openpyxl as xl
import string
import time
import json
import numpy as np
from datetime import datetime
import sys
import xlrd

from allscapeAPIMain import procName

from common.logManage import logManage

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당

import os
import sys


class excelService:
    @staticmethod
    def parse_level(row: pd.Series) -> int:
        """현재 셀의 표시레벨을 구한다"""

        if int(row[5]) == 0:
            if int(row[3]) == 0 and int(row[4]) == 0:
                return 1
            elif int(row[4]) == 0:
                return 2
            else:
                return 3
        else:
            if int(row[10]) != 0 or int(row[12]) != 0:
                return 4
        return 0

    @staticmethod
    def parse_row(row, level_names, PCcode_book, cons_code, co_code):
        level = excelService.parse_level(row)
        name = row[6]

        if level == 1:
            level_names[0], level_names[1], level_names[2] = name, "", ""
        elif level == 2:
            level_names[1], level_names[2] = name, ""
        elif level == 3:
            level_names[2] = name
        elif level == 4:
            return [
                cons_code,
                co_code,
                PCcode_book.get(row[0], {}).get("PCcode", ""),
                row[0],
                int(row[2]),
                int(row[3]),
                int(row[4]),
                int(row[5]),
                *level_names,
                row[6].replace("'", "").replace('"', ""),
                row[7].replace("'", "").replace('"', ""),
                row[8],
                int(float(row[9]) * 100),
                int(row[10]),
                int(row[11]),
                int(row[12]),
                int(row[13]),
                PCcode_book.get(row[0], {}).get("start", ""),
                PCcode_book.get(row[0], {}).get("end", ""),
            ]

    @staticmethod
    def parse_process_detail(file, cons_code, co_code, PCcode_book) -> list:
        """공정상세내역서 을지를 파싱한다"""

        #### 파일 유효성 검증 ####
        workbook = xl.load_workbook(file)


        from projectProcessManage.servProjectProcessManage import (
            servProjectProcessManage,
        )

        servProcMana = servProjectProcessManage()
        resCd, msg, indexData = servProcMana.get_process_code_count()
        if resCd == 0:
            index = int(indexData["count"])

            #### 공종코드 추가 ####
            if "3_Code List" in workbook.sheetnames:
                servProcMana = servProjectProcessManage()
                df = pd.read_excel(file, sheet_name="3_Code List", header=[0, 1])

                for _, row in df.iterrows():
                    if not row[1] in PCcode_book:
                        resCd, msg, result = servProcMana.post_PCcode(
                            index, row[1], row[3]
                        )
                        if resCd != 0:
                            raise ValueError(
                                f"{index}, {row[1]}, {row[3]} 코드삽입이 실패했습니다: {msg}"
                            )
                        index += 1

        #### 공종별 일정 가져오기 ####
        if not "2_공종별ITC-Sche_현장작성요청" in workbook.sheetnames:
            raise ValueError("공정내역서에 2_공종별ITC-Sche_현장작성요청이 없습니다")

        df = pd.read_excel(file, sheet_name="2_공종별ITC-Sche_현장작성요청", header=[0, 1, 2])
        for index, row in df.iterrows():
            if not row[1] in PCcode_book:
                continue
            PCcode_book[row[1]]["start"] = row[7].strftime("%Y%m%d%H%M%S")
            PCcode_book[row[1]]["end"] = row[8].strftime("%Y%m%d%H%M%S")

        #### 품목 가져오기 ####
        if not "1_을지_Activity based_data" in workbook.sheetnames:
            raise ValueError("공정내역서에 1_을지_Activity based_data가 없습니다")

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "읽기완료",
        )
        df = pd.read_excel(
            file, sheet_name="1_을지_Activity based_data", header=[0, 1], skiprows=[2]
        )

        integer_columns = [2, 3, 4, 5, 9, 10, 11, 12, 13]
        string_columns = [0, 1, 6, 7, 8]

        for col_index in integer_columns:
            df.iloc[:, col_index] = df.iloc[:, col_index].fillna(0)
        for col_index in string_columns:
            df.iloc[:, col_index] = df.iloc[:, col_index].fillna("")

        item_list = list()
        level_names = ["", "", ""]
        for _, row in df.iterrows():
            item = excelService.parse_row(
                row, level_names, PCcode_book, cons_code, co_code
            )
            if item:
                item_list.append(item)

        return item_list

    @staticmethod
    def convert_to_datetime(value, origin="1900-01-01"):

        if isinstance(value, (int, float)):
            return pd.to_datetime(value, unit="D", origin=origin)
        else:
            return pd.to_datetime(value)

    @staticmethod
    def parse_process_change(file):
        """공정내역서 파싱"""

        windows_excel_origin = "1900-01-01"
        #### 공종정보 가져오기 ####
        try:
            df = pd.read_excel(file, sheet_name="공종정보", header=[0, 1])
        except:
            raise ValueError("내역서에 공종정보 sheet가 없습니다")
        pc_list = list()
        for _, r in df.iterrows():
            if pd.isna(r[1]) or str(r[1]) == "예시" or pd.isna(r[2]):
                continue
            pc_list.append([str(r[1]), str(r[2]),
                        start_date_1 := excelService.convert_to_datetime(r[7]).strftime("%Y%m%d%H%M%S") if not pd.isna(r[7]) else None,
                        end_date_1 := excelService.convert_to_datetime(r[8]).strftime("%Y%m%d%H%M%S") if not pd.isna(r[8]) else None,
                        str(r[10]) if not pd.isna(r[10]) else None,
                        start_date_2 := excelService.convert_to_datetime(r[11]).strftime("%Y%m%d%H%M%S") if not pd.isna(r[11]) else None,
                        end_date_2 := excelService.convert_to_datetime(r[12]).strftime("%Y%m%d%H%M%S") if not pd.isna(r[12]) else None,
                        str(r[14]) if not pd.isna(r[14]) else None,
                        start_date_3 := excelService.convert_to_datetime(r[15]).strftime("%Y%m%d%H%M%S") if not pd.isna(r[15]) else None,
                        end_date_3 := excelService.convert_to_datetime(r[16]).strftime("%Y%m%d%H%M%S") if not pd.isna(r[16]) else None,
                        str(r[18]) if not pd.isna(r[18]) else None,
                        start_date_4 := excelService.convert_to_datetime(r[19]).strftime("%Y%m%d%H%M%S") if not pd.isna(r[19]) else None,
                        end_date_4 := excelService.convert_to_datetime(r[20]).strftime("%Y%m%d%H%M%S") if not pd.isna(r[20]) else None,
                        str(r[21]) if not pd.isna(r[21]) else None,
                        start_date := min([start_time for start_time in [start_date_1, start_date_2, start_date_3, start_date_4] if start_time is not None]),
                        end_date := max([end_time for end_time in [end_date_1, end_date_2, end_date_3, end_date_4] if end_time is not None]),
                        int((datetime.strptime(end_date, "%Y%m%d%H%M%S") - datetime.strptime(start_date, "%Y%m%d%H%M%S")).days) + 1
                        ])
        try:
            df = pd.read_excel(file, sheet_name="공정내역서", header=[0, 1])
        except:
            raise ValueError("내역서에 공정내역서 sheet가 없습니다")

        item_dict = dict()
        for index, r in df.iterrows():
            if str(r[2]) == 'nan' or str(r[0]) == "예시":
                continue

            key = (str(r[0]) if not pd.isna(r[0]) else None,
                str(r[2]),
                str(r[3]).replace("'", "").replace('"', "") if not pd.isna(r[3]) else None
                )

            if key in item_dict:
                item_dict[key][6] += int(float(r[6]) * 100) if not pd.isna(r[6]) else 0

            else:
                item_dict[key] = [key[0], key[1], key[2],
                                    str(r[4]) if not pd.isna(r[4]) else "",
                                    str(r[5]) if not pd.isna(r[5]) else "",
                                    int(float(r[6])* 100) if not pd.isna(r[6]) else 0,
                                    int(r[7]) if not pd.isna(r[7]) else 0,
                                    int(r[8]) if not pd.isna(r[8]) else 0,
                                    int(r[10]) if not pd.isna(r[10]) else 0,
                                    int(r[12]) if not pd.isna(r[12]) else 0,
                                    str(r[16]) if not pd.isna(r[16]) and str(r[16]) in ["추가", "변경", "삭제"] else ""
                                ]

        item_list = list(item_dict.values())
        return item_list, pc_list

    @staticmethod
    def append_to_excel(format_file, output_file, item_data, pc_data):
        wb = xl.load_workbook(format_file)

        # Append the data to the appropriate sheets
        item_sheet = wb["공정내역서"]
        pc_sheet = wb["공종정보"]

        # Find the last non-empty row in the item sheet
        item_row = 4

        accounting_format = '_-* #,##0_-;-* #,##0_-;_-* "-"_-;_-@_-'
        date_format = 'yyyy-mm-dd;@'

        # Append item data to the item sheet
        for item in item_data:
            item_sheet.cell(row=item_row, column=1).value = item["pc_name"]
            item_sheet.cell(row=item_row, column=2).value = f"=VLOOKUP(A{item_row},'공종정보'!$B$3:$C$10000, 2, FALSE)"
            item_sheet.cell(row=item_row, column=3).value = item["description"]
            item_sheet.cell(row=item_row, column=4).value = item["standard"]
            item_sheet.cell(row=item_row, column=5).value = item["vendor"]
            item_sheet.cell(row=item_row, column=6).value = item["unit"]
            item_sheet.cell(row=item_row, column=7).value = item["quantity"] / 100
            item_sheet.cell(row=item_row, column=8).value = item["head"]

            item_sheet.cell(row=item_row, column=9).value = item["material_unit_cost"]
            item_sheet.cell(row=item_row, column=9).number_format = accounting_format

            item_sheet.cell(row=item_row, column=10).value = f"=INT(G{item_row}*I{item_row})"
            item_sheet.cell(row=item_row, column=10).number_format = accounting_format

            item_sheet.cell(row=item_row, column=11).value = item["labor_unit_cost"]
            item_sheet.cell(row=item_row, column=11).number_format = accounting_format

            item_sheet.cell(row=item_row, column=12).value = f"=INT(G{item_row}*K{item_row})"
            item_sheet.cell(row=item_row, column=12).number_format = accounting_format

            item_sheet.cell(row=item_row, column=13).value = item["other_unit_cost"]
            item_sheet.cell(row=item_row, column=13).number_format = accounting_format

            item_sheet.cell(row=item_row, column=14).value = f"=INT(G{item_row}*M{item_row})"
            item_sheet.cell(row=item_row, column=14).number_format = accounting_format

            item_sheet.cell(row=item_row, column=15).value = f"=INT(M{item_row}+I{item_row}+K{item_row})"
            item_sheet.cell(row=item_row, column=15).number_format = accounting_format

            item_sheet.cell(row=item_row, column=16).value = f"=INT(G{item_row}*O{item_row})"
            item_sheet.cell(row=item_row, column=16).number_format = accounting_format

            item_sheet.cell(row=item_row, column=17).value = ""

            item_row += 1

        # Find the last non-empty row in the pc sheet
        pc_row = 4

        # Append pc data to the pc sheet
        for pc, index in zip(pc_data, range(1, len(pc_data) + 1)):
            pc_sheet.cell(row=pc_row, column=1).value = index
            pc_sheet.cell(row=pc_row, column=2).value = pc["pc_name"]
            pc_sheet.cell(row=pc_row, column=3).value = pc["pc_explain"]

            pc_sheet.cell(row=pc_row, column=4).value = f"=SUMIF('공정내역서'!$A$3:$A$10000, B{pc_row}, '공정내역서'!$J$3:$J$10000)"
            pc_sheet.cell(row=pc_row, column=4).number_format = accounting_format

            pc_sheet.cell(row=pc_row, column=5).value = f"=SUMIF('공정내역서'!$A$3:$A$10000, B{pc_row}, '공정내역서'!$L$3:$L$10000)"
            pc_sheet.cell(row=pc_row, column=5).number_format = accounting_format

            pc_sheet.cell(row=pc_row, column=6).value = f"=SUMIF('공정내역서'!$A$3:$A$10000, B{pc_row}, '공정내역서'!$N$3:$N$10000)"
            pc_sheet.cell(row=pc_row, column=6).number_format = accounting_format

            pc_sheet.cell(row=pc_row, column=7).value = f"=INT(D{pc_row}+E{pc_row}+F{pc_row})"
            pc_sheet.cell(row=pc_row, column=7).number_format = accounting_format

            pc_sheet.cell(row=pc_row, column=8).value = datetime.strptime(pc["start_date_1"], "%Y%m%d")
            pc_sheet.cell(row=pc_row, column=8).number_format = date_format
            pc_sheet.cell(row=pc_row, column=9).value = datetime.strptime(pc["end_date_1"], "%Y%m%d")
            pc_sheet.cell(row=pc_row, column=9).number_format = date_format

            pc_sheet.cell(row=pc_row, column=10).value = f'=IF(H{pc_row}="",0,I{pc_row}-H{pc_row}+1)'
            pc_sheet.cell(row=pc_row, column=11).value = pc["content_1"]

            pc_sheet.cell(row=pc_row, column=12).value = datetime.strptime(pc["start_date_2"], "%Y%m%d") if pc["start_date_2"] else None
            pc_sheet.cell(row=pc_row, column=12).number_format = date_format
            pc_sheet.cell(row=pc_row, column=13).value = datetime.strptime(pc["end_date_2"], "%Y%m%d") if pc["end_date_2"] else None
            pc_sheet.cell(row=pc_row, column=13).number_format = date_format

            pc_sheet.cell(row=pc_row, column=14).value = f'=IF(L{pc_row}="",0,M{pc_row}-L{pc_row}+1)'
            pc_sheet.cell(row=pc_row, column=15).value = pc["content_2"]

            pc_sheet.cell(row=pc_row, column=16).value = datetime.strptime(pc["start_date_3"], "%Y%m%d") if pc["start_date_3"] else None
            pc_sheet.cell(row=pc_row, column=16).number_format = date_format
            pc_sheet.cell(row=pc_row, column=17).value = datetime.strptime(pc["end_date_3"], "%Y%m%d") if pc["end_date_3"] else None
            pc_sheet.cell(row=pc_row, column=17).number_format = date_format

            pc_sheet.cell(row=pc_row, column=18).value = f'=IF(P{pc_row}="",0,Q{pc_row}-P{pc_row}+1)'
            pc_sheet.cell(row=pc_row, column=19).value = pc["content_3"]

            pc_sheet.cell(row=pc_row, column=20).value = datetime.strptime(pc["start_date_4"], "%Y%m%d%H%M%S") if pc["start_date_4"] else None
            pc_sheet.cell(row=pc_row, column=20).number_format = date_format
            pc_sheet.cell(row=pc_row, column=21).value = datetime.strptime(pc["end_date_4"], "%Y%m%d%H%M%S") if pc["end_date_4"] else None
            pc_sheet.cell(row=pc_row, column=21).number_format = date_format

            pc_sheet.cell(row=pc_row, column=22).value = f'=IF(T{pc_row}="",0,U{pc_row}-T{pc_row}+1)'
            pc_sheet.cell(row=pc_row, column=23).value = pc["content_4"]
            pc_sheet.cell(row=pc_row, column=24).value = f"=MIN(H{pc_row},L{pc_row},P{pc_row},T{pc_row})"
            pc_sheet.cell(row=pc_row, column=25).value = f"=MAX(I{pc_row},M{pc_row},Q{pc_row},U{pc_row})"
            pc_sheet.cell(row=pc_row, column=26).value = f"=J{pc_row}+N{pc_row}+R{pc_row}+V{pc_row}"
            pc_row += 1

        # Save the updated workbook
        wb.save(f"{output_file}.xlsx")
